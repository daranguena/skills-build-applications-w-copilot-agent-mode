from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Activity, Profile, Team, Workout, WorkoutSuggestion
from .serializers import (
    ActivitySerializer,
    LeaderboardEntrySerializer,
    ProfileSerializer,
    TeamLeaderboardSerializer,
    TeamSerializer,
    UserSerializer,
    WorkoutSerializer,
    WorkoutSuggestionSerializer,
)


User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user', 'team').all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        team = serializer.save(captain=self.request.user)
        if hasattr(self.request.user, 'profile'):
            self.request.user.profile.team = team
            self.request.user.profile.save(update_fields=['team'])

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return queryset.filter(
                Q(members__user=self.request.user) | Q(captain=self.request.user)
            ).distinct()
        return queryset


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related('user', 'user__profile').all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkoutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.AllowAny]


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    queryset = WorkoutSuggestion.objects.select_related('user', 'workout').all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_suggestions(self, request):
        """Generate personalized workout suggestions for the current user."""
        user = request.user
        suggested_workouts = Workout.suggest_for_user(user)
        
        suggestions = []
        for workout in suggested_workouts:
            # Check if suggestion already exists for today
            existing = WorkoutSuggestion.objects.filter(
                user=user,
                workout=workout,
                suggested_date=timezone.now().date(),
                status=WorkoutSuggestion.PENDING
            ).exists()
            
            if not existing:
                suggestion = WorkoutSuggestion.objects.create(
                    user=user,
                    workout=workout,
                    reason=f"Personalized suggestion based on your activity patterns"
                )
                suggestions.append(suggestion)
        
        serializer = self.get_serializer(suggestions, many=True)
        return Response(serializer.data)


class LeaderboardView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        profile_rows = (
            Profile.objects.select_related('user', 'team')
            .order_by('-total_points')[:10]
        )
        users = [
            {
                'username': profile.user.username,
                'display_name': profile.display_name or profile.user.username,
                'total_points': profile.total_points,
                'team_name': profile.team.name if profile.team else None,
            }
            for profile in profile_rows
        ]

        team_rows = (
            Team.objects.annotate(
                annotated_points_total=Sum('members__total_points'),
                annotated_member_count=Count('members'),
            )
            .order_by('-annotated_points_total')[:5]
        )
        teams = [
            {
                'name': team.name,
                'total_points': getattr(team, 'annotated_points_total', None) or team.points_total,
                'member_count': getattr(team, 'annotated_member_count', None) or team.member_count,
            }
            for team in team_rows
        ]

        return Response(
            {
                'users': LeaderboardEntrySerializer(users, many=True).data,
                'teams': TeamLeaderboardSerializer(teams, many=True).data,
            }
        )
