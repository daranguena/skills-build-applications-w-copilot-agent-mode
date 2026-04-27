#!/usr/bin/env python
"""
Setup script for OctoFit Tracker database and test data.
"""
import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_project.settings')

# Setup Django
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import User
from octofit_tracker.models import (
    UserProfile, Activity, Team, Leaderboard,
    LeaderboardEntry, WorkoutSuggestion
)
from datetime import date, timedelta

print("=" * 50)
print("OctoFit Tracker Database Setup")
print("=" * 50)

# Run migrations
print("\n1. Running migrations...")
try:
    call_command('makemigrations', 'octofit_tracker', interactive=False, verbosity=0)
    print("   ✓ Migrations created")
    call_command('migrate', verbosity=0)
    print("   ✓ Migrations applied")
except Exception as e:
    print(f"   ✗ Migration error: {e}")

# Create superuser
print("\n2. Creating superuser...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@octofit.test', 'admin123')
    print("   ✓ Superuser created: admin (password: admin123)")
else:
    print("   ✓ Superuser already exists")

# Clear and create test data
print("\n3. Creating test data...")
User.objects.filter(username__startswith='testuser_').delete()
print("   ✓ Cleared existing test data")

# Create test users
print("   Creating users...")
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
    print(f"     ✓ {user.username}")

# Create user profiles
print("   Creating user profiles...")
activity_levels = ['sedentary', 'light', 'moderate', 'very_active', 'extremely_active']
goals = ['Lose weight', 'Build muscle', 'Improve endurance', 'Increase flexibility', 'General fitness']
for i, user in enumerate(users):
    profile = UserProfile.objects.create(
        user=user,
        age=20 + (i * 5),
        height=160 + (i * 5),
        weight=60 + (i * 10),
        activity_level=activity_levels[i],
        fitness_goal=goals[i]
    )
    print(f"     ✓ Profile for {user.username}")

# Create activities
print("   Creating activities...")
activity_types = ['running', 'cycling', 'swimming', 'gym', 'yoga']
for user in users:
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
print(f"     ✓ Created {Activity.objects.count()} activities")

# Create teams
print("   Creating teams...")
team1 = Team.objects.create(
    name='Morning Runners',
    description='A team for early morning runner enthusiasts',
    creator=users[0]
)
team1.members.set(users[0:3])
print(f"     ✓ {team1.name}")

team2 = Team.objects.create(
    name='Gym Warriors',
    description='Dedicated gym and strength training team',
    creator=users[1]
)
team2.members.set(users[1:4])
print(f"     ✓ {team2.name}")

team3 = Team.objects.create(
    name='All Stars',
    description='Best of all fitness activities',
    creator=users[4]
)
team3.members.set(users)
print(f"     ✓ {team3.name}")

teams = [team1, team2, team3]

# Create leaderboards
print("   Creating leaderboards...")
leaderboard = Leaderboard.objects.create(
    leaderboard_type='weekly',
    period_start=date.today() - timedelta(days=7),
    period_end=date.today(),
    team=teams[0]
)
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
print(f"     ✓ Created 1 leaderboard with {LeaderboardEntry.objects.count()} entries")

# Create workout suggestions
print("   Creating workout suggestions...")
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
print(f"     ✓ Created {WorkoutSuggestion.objects.count()} workout suggestions")

# Print summary
print("\n4. Database Statistics:")
print(f"   Users: {User.objects.count()}")
print(f"   User Profiles: {UserProfile.objects.count()}")
print(f"   Activities: {Activity.objects.count()}")
print(f"   Teams: {Team.objects.count()}")
print(f"   Leaderboards: {Leaderboard.objects.count()}")
print(f"   Leaderboard Entries: {LeaderboardEntry.objects.count()}")
print(f"   Workout Suggestions: {WorkoutSuggestion.objects.count()}")

print("\n" + "=" * 50)
print("✓ Setup completed successfully!")
print("=" * 50)
print("\nNext steps:")
print("1. Run the development server:")
print("   python manage.py runserver 0.0.0.0:8000")
print("\n2. Access the admin interface:")
print("   http://localhost:8000/admin/")
print("   Username: admin")
print("   Password: admin123")
print("\n3. Test the API endpoints at:")
print("   http://localhost:8000/api/")
