from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from tracker.models import Activity, Profile, Team, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with sample OctoFit Tracker data.'

    def handle(self, *args, **options):
        User = get_user_model()

        sample_users = [
            {
                'username': 'student1',
                'email': 'student1@example.com',
                'password': 'pass1234',
                'display_name': 'Student One',
                'bio': 'Loves running and team challenges.',
            },
            {
                'username': 'student2',
                'email': 'student2@example.com',
                'password': 'pass1234',
                'display_name': 'Student Two',
                'bio': 'Enjoys yoga and keeping active.',
            },
            {
                'username': 'coach',
                'email': 'coach@example.com',
                'password': 'pass1234',
                'display_name': 'Coach Cat',
                'bio': 'Supports students and tracks team progress.',
            },
        ]

        users = {}
        for data in sample_users:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={'email': data['email']},
            )
            user.set_password(data['password'])
            user.save()
            
            # Ensure profile exists
            profile, created_profile = Profile.objects.get_or_create(user=user)
            if created_profile:
                profile.display_name = data['display_name']
                profile.bio = data['bio']
                profile.save()
            users[data['username']] = user

        teams = [
            {
                'name': 'Team Octo',
                'description': 'The first student fitness team.',
                'captain_username': 'coach',
            },
            {
                'name': 'Team Hydra',
                'description': 'A competitive group focused on wellness.',
                'captain_username': 'student1',
            },
        ]

        team_objects = {}
        for data in teams:
            team_data = {
                'description': data['description'],
                'captain': users[data['captain_username']],
            }
            team, _ = Team.objects.get_or_create(
                name=data['name'],
                defaults=team_data,
            )
            team_objects[data['name']] = team

        users['student1'].profile.team = team_objects['Team Octo']
        users['student1'].profile.save()

        users['student2'].profile.team = team_objects['Team Hydra']
        users['student2'].profile.save()

        activities = [
            {
                'user': users['student1'],
                'activity_type': Activity.RUNNING,
                'duration_minutes': 28,
                'distance_km': 4.4,
                'calories_burned': 320,
                'notes': 'Morning run around the track.',
            },
            {
                'user': users['student1'],
                'activity_type': Activity.STRENGTH,
                'duration_minutes': 45,
                'distance_km': None,
                'calories_burned': 260,
                'notes': 'Strength training circuit.',
            },
            {
                'user': users['student2'],
                'activity_type': Activity.WALKING,
                'duration_minutes': 35,
                'distance_km': 3.2,
                'calories_burned': 180,
                'notes': 'Evening walk with friends.',
            },
            {
                'user': users['student2'],
                'activity_type': Activity.YOGA,
                'duration_minutes': 40,
                'distance_km': None,
                'calories_burned': 140,
                'notes': 'Relaxing yoga session.',
            },
        ]

        for activity_data in activities:
            Activity.objects.get_or_create(
                user=activity_data['user'],
                activity_type=activity_data['activity_type'],
                duration_minutes=activity_data['duration_minutes'],
                notes=activity_data['notes'],
                defaults={
                    'distance_km': activity_data['distance_km'],
                    'calories_burned': activity_data['calories_burned'],
                },
            )

        Workout.objects.get_or_create(
            name='Full Body Circuit',
            defaults={
                'description': 'A full-body workout that blends strength and cardio.',
                'difficulty': Workout.MEDIUM,
                'recommended_activity': Activity.STRENGTH,
                'duration_minutes': 40,
            },
        )
        Workout.objects.get_or_create(
            name='Morning Cardio',
            defaults={
                'description': 'A light cardio routine for daily energy.',
                'difficulty': Workout.LOW,
                'recommended_activity': Activity.WALKING,
                'duration_minutes': 30,
            },
        )

        for user in users.values():
            profile = getattr(user, 'profile', None)
            if profile:
                profile.refresh_total_points()

        self.stdout.write(self.style.SUCCESS('Sample OctoFit Tracker data has been populated.'))
