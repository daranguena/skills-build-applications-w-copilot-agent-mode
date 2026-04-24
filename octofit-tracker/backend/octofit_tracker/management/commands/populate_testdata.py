"""
Management command to populate OctoFit Tracker with test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from octofit_tracker.models import (
    UserProfile, Activity, Team, Leaderboard,
    LeaderboardEntry, WorkoutSuggestion
)


class Command(BaseCommand):
    help = 'Populates the OctoFit database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate test data...'))

        # Clear existing data
        self.clear_data()

        # Create test users
        users = self.create_users()

        # Create user profiles
        self.create_profiles(users)

        # Create activities
        self.create_activities(users)

        # Create teams
        teams = self.create_teams(users)

        # Create leaderboards and entries
        self.create_leaderboards(users, teams)

        # Create workout suggestions
        self.create_workout_suggestions(users)

        self.stdout.write(self.style.SUCCESS('✓ Test data population completed successfully!'))

    def clear_data(self):
        """Clear existing test data."""
        self.stdout.write('Clearing existing data...')
        User.objects.filter(username__startswith='testuser').delete()
        self.stdout.write('✓ Data cleared')

    def create_users(self):
        """Create test users."""
        self.stdout.write('Creating test users...')
        users = []
        usernames = ['alice', 'bob', 'charlie', 'diana', 'evan']
        
        for i, username in enumerate(usernames, 1):
            user = User.objects.create_user(
                username=f'testuser_{username}',
                email=f'{username}@octofit.test',
                password='OctoFit@2024',
                first_name=username.capitalize(),
                last_name='Fitness'
            )
            users.append(user)
            self.stdout.write(f'  ✓ Created user: {user.username}')

        return users

    def create_profiles(self, users):
        """Create user profiles."""
        self.stdout.write('Creating user profiles...')
        activity_levels = ['sedentary', 'light', 'moderate', 'very_active', 'extremely_active']
        goals = [
            'Lose weight',
            'Build muscle',
            'Improve endurance',
            'Increase flexibility',
            'General fitness'
        ]

        for i, user in enumerate(users):
            profile = UserProfile.objects.create(
                user=user,
                age=20 + (i * 5),
                height=160 + (i * 5),
                weight=60 + (i * 10),
                activity_level=activity_levels[i],
                fitness_goal=goals[i]
            )
            self.stdout.write(f'  ✓ Created profile for {user.username}')

    def create_activities(self, users):
        """Create test activities."""
        self.stdout.write('Creating activities...')
        activity_types = ['running', 'cycling', 'swimming', 'gym', 'yoga']
        
        for user in users:
            # Create 5 activities for each user
            for j in range(5):
                activity_date = date.today() - timedelta(days=j*2)
                activity = Activity.objects.create(
                    user=user,
                    activity_type=activity_types[j % len(activity_types)],
                    title=f'{activity_types[j % len(activity_types)].capitalize()} Session {j+1}',
                    description=f'Great {activity_types[j % len(activity_types)]} workout',
                    duration_minutes=30 + (j * 10),
                    distance_km=5.0 + (j * 2),
                    calories_burned=200 + (j * 50),
                    intensity='moderate',
                    activity_date=activity_date
                )
                self.stdout.write(f'  ✓ Created activity: {user.username} - {activity.title}')

    def create_teams(self, users):
        """Create test teams."""
        self.stdout.write('Creating teams...')
        teams = []
        
        # Create team 1
        team1 = Team.objects.create(
            name='Morning Runners',
            description='A team for early morning runner enthusiasts',
            creator=users[0]
        )
        team1.members.set(users[0:3])
        teams.append(team1)
        self.stdout.write(f'  ✓ Created team: {team1.name}')

        # Create team 2
        team2 = Team.objects.create(
            name='Gym Warriors',
            description='Dedicated gym and strength training team',
            creator=users[1]
        )
        team2.members.set(users[1:4])
        teams.append(team2)
        self.stdout.write(f'  ✓ Created team: {team2.name}')

        # Create team 3
        team3 = Team.objects.create(
            name='All Stars',
            description='Best of all fitness activities',
            creator=users[4]
        )
        team3.members.set(users)
        teams.append(team3)
        self.stdout.write(f'  ✓ Created team: {team3.name}')

        return teams

    def create_leaderboards(self, users, teams):
        """Create leaderboards and entries."""
        self.stdout.write('Creating leaderboards...')
        
        # Create weekly leaderboard
        leaderboard = Leaderboard.objects.create(
            leaderboard_type='weekly',
            period_start=date.today() - timedelta(days=7),
            period_end=date.today(),
            team=teams[0]
        )
        self.stdout.write(f'  ✓ Created leaderboard: {leaderboard.leaderboard_type}')

        # Create entries for the leaderboard
        for i, user in enumerate(users):
            LeaderboardEntry.objects.create(
                leaderboard=leaderboard,
                user=user,
                rank=i + 1,
                total_points=500 - (i * 50),
                total_distance_km=25.0 - (i * 2),
                total_calories=2000 - (i * 200),
                total_activities=5
            )
            self.stdout.write(f'  ✓ Created leaderboard entry for {user.username}')

    def create_workout_suggestions(self, users):
        """Create workout suggestions."""
        self.stdout.write('Creating workout suggestions...')
        suggestions = [
            ('Morning Yoga', 'Start your day with a relaxing yoga session', 'yoga', 'beginner', 30),
            ('HIIT Training', 'High intensity interval training for cardio', 'gym', 'advanced', 45),
            ('Long Distance Run', 'Build your endurance with a longer run', 'running', 'intermediate', 60),
            ('Swimming Workout', 'Low impact full body swimming session', 'swimming', 'intermediate', 45),
            ('Cycling Tour', 'Enjoy a scenic cycling adventure', 'cycling', 'intermediate', 90),
        ]

        for i, user in enumerate(users):
            suggestion_data = suggestions[i % len(suggestions)]
            suggestion = WorkoutSuggestion.objects.create(
                user=user,
                title=suggestion_data[0],
                description=suggestion_data[1],
                suggested_activity_type=suggestion_data[2],
                difficulty_level=suggestion_data[3],
                estimated_duration_minutes=suggestion_data[4],
                reason='Based on your fitness profile and activity history'
            )
            self.stdout.write(f'  ✓ Created suggestion for {user.username}: {suggestion.title}')
