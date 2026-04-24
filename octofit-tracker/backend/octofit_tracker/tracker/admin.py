from django.contrib import admin

from .models import Activity, Profile, Team, Workout


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'team', 'total_points', 'updated_at')
    list_select_related = ('user', 'team')
    search_fields = ('user__username', 'display_name', 'bio')
    list_filter = ('team',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'captain', 'member_count', 'total_points', 'created_at')
    readonly_fields = ('member_count', 'total_points')
    search_fields = ('name', 'description', 'captain__username')
    list_select_related = ('captain',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'recommended_activity', 'duration_minutes', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('difficulty', 'recommended_activity')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration_minutes', 'distance_km', 'points', 'date')
    search_fields = ('user__username', 'activity_type', 'notes')
    list_filter = ('activity_type', 'date')
    list_select_related = ('user',)
