from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    captain = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='captained_teams',
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()

    @property
    def points_total(self):
        return self.members.aggregate(total=Sum('total_points'))['total'] or 0

    @property
    def total_points(self):
        return getattr(self, 'points_total', None)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    display_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    team = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='members',
    )
    total_points = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_points', 'display_name']

    def __str__(self):
        return self.display_name or self.user.username

    @property
    def team_name(self):
        return self.team.name if self.team else None

    def refresh_total_points(self):
        total = self.user.activities.aggregate(total=Sum('points'))['total'] or 0
        self.total_points = total
        self.save(update_fields=['total_points'])


class Activity(models.Model):
    RUNNING = 'running'
    WALKING = 'walking'
    STRENGTH = 'strength'
    YOGA = 'yoga'
    ACTIVITY_CHOICES = [
        (RUNNING, 'Running'),
        (WALKING, 'Walking'),
        (STRENGTH, 'Strength Training'),
        (YOGA, 'Yoga'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities',
    )
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    duration_minutes = models.PositiveIntegerField()
    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Optional distance in kilometers',
    )
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.user.username} {self.activity_type} on {self.date.date()}'

    def calculate_points(self):
        points = self.duration_minutes * 5
        if self.activity_type == self.RUNNING:
            points += int((self.distance_km or 0) * 10)
        elif self.activity_type == self.WALKING:
            points += int((self.distance_km or 0) * 5)
        elif self.activity_type == self.STRENGTH:
            points += 15
        elif self.activity_type == self.YOGA:
            points += 8
        return max(points, 0)

    def save(self, *args, **kwargs):
        self.points = self.calculate_points()
        super().save(*args, **kwargs)


class Workout(models.Model):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    DIFFICULTY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]

    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=MEDIUM,
    )
    recommended_activity = models.CharField(
        max_length=20,
        choices=Activity.ACTIVITY_CHOICES,
        null=True,
        blank=True,
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def suggest_for_user(cls, user, limit=3):
        """Generate workout suggestions for a user based on their activity patterns."""
        suggestions = []
        
        # Get user's recent activities
        recent_activities = Activity.objects.filter(
            user=user,
            date__gte=timezone.now() - timezone.timedelta(days=30)
        ).values('activity_type').annotate(count=Count('activity_type'))
        
        # Get user's profile for personalization
        profile = getattr(user, 'profile', None)
        
        # Suggest workouts based on activity patterns
        if recent_activities:
            # Suggest complementary workouts
            activity_types = [act['activity_type'] for act in recent_activities]
            
            if 'running' in activity_types and 'strength' not in activity_types:
                # Suggest strength training to complement running
                strength_workouts = cls.objects.filter(
                    recommended_activity='strength',
                    difficulty__in=['medium', 'low']
                )
                if strength_workouts.exists():
                    suggestions.append(strength_workouts.first())
            
            if 'yoga' not in activity_types:
                # Suggest yoga for recovery
                yoga_workouts = cls.objects.filter(recommended_activity='yoga')
                if yoga_workouts.exists():
                    suggestions.append(yoga_workouts.first())
        else:
            # New user - suggest beginner workouts
            beginner_workouts = cls.objects.filter(difficulty='low')[:2]
            suggestions.extend(beginner_workouts)
        
        # Team-based suggestions
        if profile and profile.team:
            # Suggest team-based workouts
            team_workouts = cls.objects.filter(difficulty='medium')[:1]
            suggestions.extend(team_workouts)
        
        # Remove duplicates and limit
        seen_names = set()
        unique_suggestions = []
        for workout in suggestions:
            if workout.name not in seen_names:
                seen_names.add(workout.name)
                unique_suggestions.append(workout)
        
        return unique_suggestions[:limit]


class WorkoutSuggestion(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'
    SKIPPED = 'skipped'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (SKIPPED, 'Skipped'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workout_suggestions',
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='suggestions',
    )
    suggested_date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    reason = models.TextField(
        blank=True,
        help_text='Why this workout was suggested',
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-suggested_date', '-created_at']
        unique_together = ['user', 'workout', 'suggested_date']

    def __str__(self):
        return f'{self.user.username} - {self.workout.name} ({self.status})'

    def mark_completed(self):
        """Mark the suggestion as completed."""
        self.status = self.COMPLETED
        self.completed_at = timezone.now()
        self.save()

    def mark_skipped(self):
        """Mark the suggestion as skipped."""
        self.status = self.SKIPPED
        self.save()


@receiver(models.signals.post_save, sender=Activity)
def update_profile_points_on_activity_save(sender, instance, **kwargs):
    if hasattr(instance.user, 'profile'):
        instance.user.profile.refresh_total_points()


@receiver(models.signals.post_delete, sender=Activity)
def update_profile_points_on_activity_delete(sender, instance, **kwargs):
    if hasattr(instance.user, 'profile'):
        instance.user.profile.refresh_total_points()


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except Exception:
            # Handle djongo conversion issues on user creation
            pass
