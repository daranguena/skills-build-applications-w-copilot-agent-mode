from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Activity, Profile, Team, Workout
from .serializers import (
    ActivitySerializer,
    LeaderboardEntrySerializer,
    ProfileSerializer,
    TeamLeaderboardSerializer,
    TeamSerializer,
    WorkoutSerializer,
)


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
        serializer.save(captain=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return queryset.filter(members__user=self.request.user).distinct()
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
