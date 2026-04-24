"""
Django admin configuration for octofit_tracker.
"""
from django.contrib import admin
from .models import (
    UserProfile, Activity, Team, Leaderboard,
    LeaderboardEntry, WorkoutSuggestion
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'weight', 'activity_level', 'created_at')
    list_filter = ('activity_level', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'title', 'activity_date', 'duration_minutes', 'logged_at')
    list_filter = ('activity_type', 'intensity', 'activity_date')
    search_fields = ('user__username', 'title')
    readonly_fields = ('logged_at',)
    ordering = ('-activity_date', '-logged_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'get_member_count', 'created_at')
    search_fields = ('name', 'creator__username')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('members',)

    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Members'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'leaderboard_type', 'period_start', 'period_end', 'get_team_name')
    list_filter = ('leaderboard_type', 'period_start')
    readonly_fields = ('created_at', 'updated_at')

    def get_team_name(self, obj):
        return obj.team.name if obj.team else 'Global'
    get_team_name.short_description = 'Team'


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'total_points', 'total_distance_km', 'total_calories')
    list_filter = ('rank', 'leaderboard')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'suggested_activity_type', 'difficulty_level', 'is_completed', 'created_at')
    list_filter = ('difficulty_level', 'is_completed', 'suggested_activity_type')
    search_fields = ('user__username', 'title')
    readonly_fields = ('created_at', 'updated_at')
