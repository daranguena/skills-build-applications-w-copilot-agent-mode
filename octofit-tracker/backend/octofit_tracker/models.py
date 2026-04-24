"""
Models for OctoFit Tracker application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for fitness tracking."""
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Light Activity'),
        ('moderate', 'Moderate Activity'),
        ('very_active', 'Very Active'),
        ('extremely_active', 'Extremely Active'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES,
        default='moderate'
    )
    fitness_goal = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="User's primary fitness goal"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    class Meta:
        db_table = 'user_profiles'


class Activity(models.Model):
    """Activity logging for users."""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('gym', 'Gym'),
        ('yoga', 'Yoga'),
        ('sports', 'Sports'),
        ('hiking', 'Hiking'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    distance_km = models.FloatField(null=True, blank=True, help_text="Distance in kilometers")
    calories_burned = models.IntegerField(null=True, blank=True)
    intensity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('moderate', 'Moderate'),
            ('high', 'High'),
        ],
        default='moderate'
    )
    logged_at = models.DateTimeField(auto_now_add=True)
    activity_date = models.DateField(help_text="Date when activity was performed")

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.activity_date}"

    class Meta:
        db_table = 'activities'
        ordering = ['-activity_date', '-logged_at']


class Team(models.Model):
    """Team for group fitness challenges."""
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'teams'


class Leaderboard(models.Model):
    """Leaderboard for competitive tracking."""
    LEADERBOARD_TYPES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('all_time', 'All Time'),
    ]

    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='leaderboard', null=True, blank=True)
    leaderboard_type = models.CharField(max_length=20, choices=LEADERBOARD_TYPES, default='weekly')
    period_start = models.DateField()
    period_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.leaderboard_type} Leaderboard - {self.period_start} to {self.period_end}"

    class Meta:
        db_table = 'leaderboards'


class LeaderboardEntry(models.Model):
    """Individual entry in a leaderboard."""
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.IntegerField()
    total_points = models.IntegerField(default=0)
    total_distance_km = models.FloatField(default=0.0)
    total_calories = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}"

    class Meta:
        db_table = 'leaderboard_entries'
        unique_together = ('leaderboard', 'user')
        ordering = ['rank']


class WorkoutSuggestion(models.Model):
    """Personalized workout suggestions."""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_suggestions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    suggested_activity_type = models.CharField(
        max_length=20,
        choices=Activity.ACTIVITY_TYPES
    )
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    estimated_duration_minutes = models.IntegerField()
    reason = models.TextField(help_text="Why this workout is suggested")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Suggestion for {self.user.username}: {self.title}"

    class Meta:
        db_table = 'workout_suggestions'
        ordering = ['-created_at']
