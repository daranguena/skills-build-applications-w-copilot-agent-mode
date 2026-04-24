#!/usr/bin/env python
"""
Verification script for OctoFit Tracker database.
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

from django.contrib.auth.models import User
from octofit_tracker.models import (
    UserProfile, Activity, Team, Leaderboard,
    LeaderboardEntry, WorkoutSuggestion
)
from pymongo import MongoClient

print("=" * 60)
print("OctoFit Tracker Database Verification")
print("=" * 60)

# Check MongoDB connection
print("\n1. MongoDB Connection Status:")
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.server_info()
    db = client['octofit_db']
    print("   ✓ MongoDB is running and accessible")
    print(f"   ✓ Database: octofit_db")
    
    # List collections
    collections = db.list_collection_names()
    print(f"   ✓ Collections in database: {len(collections)}")
    for collection in collections:
        count = db[collection].count_documents({})
        print(f"     - {collection}: {count} documents")
except Exception as e:
    print(f"   ✗ MongoDB Error: {e}")
    sys.exit(1)

# Check Django ORM data
print("\n2. Django ORM Data:")
users_count = User.objects.count()
profiles_count = UserProfile.objects.count()
activities_count = Activity.objects.count()
teams_count = Team.objects.count()
leaderboards_count = Leaderboard.objects.count()
entries_count = LeaderboardEntry.objects.count()
suggestions_count = WorkoutSuggestion.objects.count()

print(f"   Users: {users_count}")
print(f"   User Profiles: {profiles_count}")
print(f"   Activities: {activities_count}")
print(f"   Teams: {teams_count}")
print(f"   Leaderboards: {leaderboards_count}")
print(f"   Leaderboard Entries: {entries_count}")
print(f"   Workout Suggestions: {suggestions_count}")

# Detailed data samples
print("\n3. Sample Data:")

if users_count > 0:
    print("\n   Test Users:")
    test_users = User.objects.filter(username__startswith='testuser_')[:5]
    for user in test_users:
        profile = user.profile if hasattr(user, 'profile') else None
        print(f"     • {user.username} ({user.email})")
        if profile:
            print(f"       Age: {profile.age}, Goal: {profile.fitness_goal}")

if activities_count > 0:
    print("\n   Recent Activities:")
    activities = Activity.objects.all()[:5]
    for activity in activities:
        print(f"     • {activity.user.username}: {activity.title}")
        print(f"       Type: {activity.activity_type}, Duration: {activity.duration_minutes}min")

if teams_count > 0:
    print("\n   Teams:")
    teams = Team.objects.all()
    for team in teams:
        print(f"     • {team.name} (Created by: {team.creator.username})")
        print(f"       Members: {team.members.count()}")

if entries_count > 0:
    print("\n   Leaderboard Top Entries:")
    entries = LeaderboardEntry.objects.order_by('rank')[:5]
    for entry in entries:
        print(f"     #{entry.rank} {entry.user.username}")
        print(f"       Points: {entry.total_points}, Distance: {entry.total_distance_km}km")

if suggestions_count > 0:
    print("\n   Workout Suggestions:")
    suggestions = WorkoutSuggestion.objects.all()[:5]
    for suggestion in suggestions:
        print(f"     • {suggestion.user.username}: {suggestion.title}")
        print(f"       Type: {suggestion.suggested_activity_type}, Duration: {suggestion.estimated_duration_minutes}min")

# Summary
print("\n" + "=" * 60)
total_records = (users_count + profiles_count + activities_count + 
                 teams_count + leaderboards_count + entries_count + suggestions_count)
if total_records > 0:
    print(f"✓ Database verification successful! Total records: {total_records}")
else:
    print("✗ No data found in database. Run setup_db.py first.")
print("=" * 60)
