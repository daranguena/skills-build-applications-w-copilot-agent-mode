"""
Serializers for OctoFit Tracker API.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Activity, Team, Leaderboard, 
    LeaderboardEntry, WorkoutSuggestion
)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'age', 'height', 'weight', 'activity_level',
            'fitness_goal', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with profile."""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'profile'
        ]
        read_only_fields = ['date_joined']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model."""
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_username', 'activity_type', 'title',
            'description', 'duration_minutes', 'distance_km', 'calories_burned',
            'intensity', 'logged_at', 'activity_date'
        ]
        read_only_fields = ['logged_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model."""
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'creator', 'creator_username',
            'member_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_member_count(self, obj):
        """Return the number of members in the team."""
        return obj.members.count()


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    """Serializer for LeaderboardEntry model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = LeaderboardEntry
        fields = [
            'id', 'leaderboard', 'user', 'user_username', 'rank',
            'total_points', 'total_distance_km', 'total_calories',
            'total_activities', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model."""
    entries = LeaderboardEntrySerializer(many=True, read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True, allow_null=True)

    class Meta:
        model = Leaderboard
        fields = [
            'id', 'team', 'team_name', 'leaderboard_type', 'period_start',
            'period_end', 'entries', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for WorkoutSuggestion model."""
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = WorkoutSuggestion
        fields = [
            'id', 'user', 'user_username', 'title', 'description',
            'suggested_activity_type', 'difficulty_level',
            'estimated_duration_minutes', 'reason', 'is_completed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
