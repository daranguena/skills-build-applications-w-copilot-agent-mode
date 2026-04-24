from django.contrib import admin

from .models import Activity, Profile, Team, Workout, WorkoutSuggestion


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


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout', 'suggested_date', 'status', 'completed_at')
    list_filter = ('status', 'suggested_date', 'workout__difficulty')
    search_fields = ('user__username', 'workout__name')
    readonly_fields = ('completed_at',)
    list_select_related = ('user', 'workout')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'workout')
