"""
Tests for OctoFit Tracker application.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import (
    UserProfile, Activity, Team, Leaderboard,
    LeaderboardEntry, WorkoutSuggestion
)


class UserProfileTestCase(TestCase):
    """Test cases for UserProfile model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_profile_creation(self):
        """Test creating a user profile."""
        profile = UserProfile.objects.create(
            user=self.user,
            age=25,
            height=180,
            weight=75,
            activity_level='moderate'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.age, 25)
        self.assertEqual(str(profile), f"{self.user.username} Profile")


class ActivityTestCase(TestCase):
    """Test cases for Activity model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_activity_creation(self):
        """Test creating an activity."""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Morning Run',
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300,
            activity_date=date.today()
        )
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.duration_minutes, 30)

    def test_activity_ordering(self):
        """Test that activities are ordered by date."""
        yesterday = date.today() - timedelta(days=1)
        today = date.today()

        Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Yesterday Run',
            duration_minutes=30,
            activity_date=yesterday
        )

        Activity.objects.create(
            user=self.user,
            activity_type='cycling',
            title='Today Ride',
            duration_minutes=45,
            activity_date=today
        )

        activities = Activity.objects.all()
        self.assertEqual(activities[0].title, 'Today Ride')


class TeamTestCase(TestCase):
    """Test cases for Team model."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )

    def test_team_creation(self):
        """Test creating a team."""
        team = Team.objects.create(
            name='Fitness Warriors',
            description='A team of fitness enthusiasts',
            creator=self.user1
        )
        team.members.add(self.user1, self.user2)
        self.assertEqual(team.name, 'Fitness Warriors')
        self.assertEqual(team.members.count(), 2)


class LeaderboardTestCase(TestCase):
    """Test cases for Leaderboard and LeaderboardEntry models."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.leaderboard = Leaderboard.objects.create(
            leaderboard_type='weekly',
            period_start=date.today(),
            period_end=date.today() + timedelta(days=7)
        )

    def test_leaderboard_entry_creation(self):
        """Test creating a leaderboard entry."""
        entry = LeaderboardEntry.objects.create(
            leaderboard=self.leaderboard,
            user=self.user,
            rank=1,
            total_points=500,
            total_distance_km=25.0,
            total_calories=2000
        )
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.rank, 1)
        self.assertEqual(entry.total_points, 500)


class WorkoutSuggestionTestCase(TestCase):
    """Test cases for WorkoutSuggestion model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_workout_suggestion_creation(self):
        """Test creating a workout suggestion."""
        suggestion = WorkoutSuggestion.objects.create(
            user=self.user,
            title='Morning Yoga',
            description='Relaxing yoga session',
            suggested_activity_type='yoga',
            difficulty_level='beginner',
            estimated_duration_minutes=30,
            reason='Based on your activity history'
        )
        self.assertEqual(suggestion.user, self.user)
        self.assertEqual(suggestion.suggested_activity_type, 'yoga')
        self.assertFalse(suggestion.is_completed)


class ActivityAPITestCase(APITestCase):
    """Test cases for Activity API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_activity(self):
        """Test creating an activity via API."""
        data = {
            'activity_type': 'running',
            'title': 'Morning Run',
            'duration_minutes': 30,
            'distance_km': 5.0,
            'calories_burned': 300,
            'intensity': 'moderate',
            'activity_date': date.today()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)


class UserAPITestCase(APITestCase):
    """Test cases for User API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_users(self):
        """Test listing users."""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
