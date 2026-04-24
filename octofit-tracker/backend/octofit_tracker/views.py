"""
Views and ViewSets for OctoFit Tracker API.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import (
    UserProfile, Activity, Team, Leaderboard,
    LeaderboardEntry, WorkoutSuggestion
)
from .serializers import (
    UserSerializer, UserProfileSerializer, ActivitySerializer,
    TeamSerializer, LeaderboardSerializer, LeaderboardEntrySerializer,
    WorkoutSuggestionSerializer
)


@api_view(['GET'])
def api_root(request):
    """API root endpoint providing overview of available endpoints."""
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'users': 'http://localhost:8000/api/users/',
            'activities': 'http://localhost:8000/api/activities/',
            'teams': 'http://localhost:8000/api/teams/',
            'leaderboard': 'http://localhost:8000/api/leaderboard/',
            'workout-suggestions': 'http://localhost:8000/api/workout-suggestions/',
        }
    })


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see themselves unless they are staff."""
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for managing activities."""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own activities unless they are staff."""
        user = self.request.user
        if user.is_staff:
            return Activity.objects.all()
        return Activity.objects.filter(user=user)

    def perform_create(self, serializer):
        """Automatically set the current user when creating an activity."""
        serializer.save(user=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for managing teams."""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can see teams they're part of or created."""
        user = self.request.user
        if user.is_staff:
            return Team.objects.all()
        return Team.objects.filter(members=user) | Team.objects.filter(creator=user)

    def perform_create(self, serializer):
        """Automatically set the current user as creator when creating a team."""
        serializer.save(creator=self.request.user)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for managing leaderboards."""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """All authenticated users can see leaderboards."""
        return Leaderboard.objects.all()


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing workout suggestions."""
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own suggestions unless they are staff."""
        user = self.request.user
        if user.is_staff:
            return WorkoutSuggestion.objects.all()
        return WorkoutSuggestion.objects.filter(user=user)

    def perform_create(self, serializer):
        """Automatically set the current user when creating a suggestion."""
        serializer.save(user=self.request.user)
