from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Activity, Profile, Team, Workout


User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'display_name', 'team_name']

    def get_team_name(self, obj):
        return obj.team.name if obj.team else None


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ['id', 'username', 'email', 'profile']


class TeamSerializer(serializers.ModelSerializer):
    captain = UserSerializer(read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    total_points = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'description',
            'captain',
            'member_count',
            'total_points',
            'members',
            'created_at',
        ]
        read_only_fields = ['id', 'captain', 'member_count', 'total_points', 'members', 'created_at']

    def get_total_points(self, obj):
        return getattr(obj, 'points_total', None) or obj.points_total

    def get_members(self, obj):
        return [
            {
                'id': profile.id,
                'display_name': profile.display_name or profile.user.username,
                'username': profile.user.username,
                'team_name': profile.team.name if profile.team else None,
            }
            for profile in obj.members.all()
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'display_name',
            'bio',
            'team',
            'total_points',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'total_points', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id',
            'user',
            'activity_type',
            'duration_minutes',
            'distance_km',
            'calories_burned',
            'date',
            'notes',
            'points',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'points', 'created_at', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = [
            'id',
            'name',
            'description',
            'difficulty',
            'recommended_activity',
            'duration_minutes',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class LeaderboardEntrySerializer(serializers.Serializer):
    username = serializers.CharField()
    display_name = serializers.CharField()
    total_points = serializers.IntegerField()
    team_name = serializers.CharField(allow_null=True)


class TeamLeaderboardSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_points = serializers.IntegerField()
    member_count = serializers.IntegerField()
