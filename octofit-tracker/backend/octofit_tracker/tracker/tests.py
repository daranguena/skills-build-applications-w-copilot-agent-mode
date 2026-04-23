from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Activity, Team, Workout


class TrackerApiTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='student',
            email='student@example.com',
            password='pass1234',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.team = Team.objects.create(
            name='Team Octo',
            description='Student wellness team',
            captain=self.user,
        )
        self.user.profile.display_name = 'Student One'
        self.user.profile.team = self.team
        self.user.profile.save()

    def test_create_activity_updates_profile_points(self):
        payload = {
            'activity_type': 'running',
            'duration_minutes': 30,
            'distance_km': '5.00',
            'calories_burned': 280,
            'notes': 'Morning run',
        }
        response = self.client.post('/api/activities/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        activity = Activity.objects.get(user=self.user)
        self.assertEqual(activity.points, 30 * 5 + 50)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.total_points, activity.points)

    def test_leaderboard_endpoint_returns_user_and_team_rankings(self):
        Activity.objects.create(
            user=self.user,
            activity_type='walking',
            duration_minutes=20,
            distance_km=2.0,
        )
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('users', data)
        self.assertIn('teams', data)
        self.assertGreaterEqual(len(data['users']), 1)
        self.assertEqual(data['users'][0]['username'], self.user.username)
        self.assertEqual(data['teams'][0]['name'], self.team.name)

    def test_team_list_api_includes_created_team(self):
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)
        self.assertEqual(data[0]['name'], self.team.name)

    def test_api_root_redirects_to_api(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('profiles', response.json())

    def test_workout_list_api_returns_sample_workout(self):
        Workout.objects.create(
            name='Full Body',
            description='Balanced strength and cardio circuit.',
            difficulty=Workout.MEDIUM,
            recommended_activity=Activity.STRENGTH,
            duration_minutes=40,
        )
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
