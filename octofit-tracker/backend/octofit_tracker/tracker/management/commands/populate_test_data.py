from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from datetime import date, timedelta

from tracker.models import Activity, Team, Workout, WorkoutSuggestion


class Command(BaseCommand):
    help = 'Populate the octofit_db database with sample OctoFit Tracker data.'

    def handle(self, *args, **options):
        User = get_user_model()

        # Clear existing sample data
        sample_usernames = ['student1', 'student2', 'coach', 'tony_stark', 'steve_rogers', 'bruce_wayne', 'clark_kent']
        User.objects.filter(username__in=sample_usernames).delete()
        Team.objects.filter(name__in=['Team Octo', 'Team Hydra', 'Marvel', 'DC']).delete()
        Activity.objects.all().delete()
        Workout.objects.filter(name__in=['Full Body Circuit', 'Morning Cardio', 'Morning Cardio Blast', 'Strength Training Basics', 'Relaxing Yoga Flow', 'Evening Walk']).delete()
        WorkoutSuggestion.objects.all().delete()

        # Create teams
        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel', description='Superhero team from Marvel Comics')
        dc = Team.objects.create(name='DC', description='Superhero team from DC Comics')
        self.stdout.write(f'Created {Team.objects.count()} teams.')

        # Create users
        self.stdout.write('Creating users...')
        sample_users = [
            {
                'username': 'tony_stark',
                'email': 'tony@stark.com',
                'password': 'password123',
                'first_name': 'Tony',
                'last_name': 'Stark',
            },
            {
                'username': 'steve_rogers',
                'email': 'steve@rogers.com',
                'password': 'password123',
                'first_name': 'Steve',
                'last_name': 'Rogers',
            },
            {
                'username': 'bruce_wayne',
                'email': 'bruce@wayne.com',
                'password': 'password123',
                'first_name': 'Bruce',
                'last_name': 'Wayne',
            },
            {
                'username': 'clark_kent',
                'email': 'clark@kent.com',
                'password': 'password123',
                'first_name': 'Clark',
                'last_name': 'Kent',
            },
        ]

        users = {}
        for data in sample_users:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            users[data['username']] = user
        self.stdout.write(f'Created {User.objects.count()} users.')

        # Set team relationships
        self.stdout.write('Setting team relationships...')
        # Create profiles for users and assign to teams
        from tracker.models import Profile
        
        # Marvel team
        profile, created = Profile.objects.get_or_create(user=users['tony_stark'], defaults={'team': marvel})
        if not created:
            profile.team = marvel
            profile.save()
            
        profile, created = Profile.objects.get_or_create(user=users['steve_rogers'], defaults={'team': marvel})
        if not created:
            profile.team = marvel
            profile.save()
        
        # DC team  
        profile, created = Profile.objects.get_or_create(user=users['bruce_wayne'], defaults={'team': dc})
        if not created:
            profile.team = dc
            profile.save()
            
        profile, created = Profile.objects.get_or_create(user=users['clark_kent'], defaults={'team': dc})
        if not created:
            profile.team = dc
            profile.save()
        
        self.stdout.write('Team relationships set.')

        # Create activities
        self.stdout.write('Creating activities...')
        Activity.objects.create(
            user=users['tony_stark'],
            activity_type=Activity.RUNNING,
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300
        )
        Activity.objects.create(
            user=users['steve_rogers'],
            activity_type=Activity.STRENGTH,
            duration_minutes=45,
            calories_burned=250
        )
        Activity.objects.create(
            user=users['bruce_wayne'],
            activity_type=Activity.YOGA,
            duration_minutes=60,
            calories_burned=150
        )
        Activity.objects.create(
            user=users['clark_kent'],
            activity_type=Activity.WALKING,
            duration_minutes=20,
            distance_km=2.5,
            calories_burned=100
        )
        self.stdout.write(f'Created {Activity.objects.count()} activities.')

        # Create workouts
        self.stdout.write('Creating workouts...')
        workout1 = Workout.objects.create(
            name='Morning Cardio Blast',
            description='High-intensity cardio workout to start your day',
            difficulty=Workout.HIGH,
            recommended_activity=Activity.RUNNING,
            duration_minutes=45
        )
        workout2 = Workout.objects.create(
            name='Strength Training Basics',
            description='Fundamental strength exercises for beginners',
            difficulty=Workout.LOW,
            recommended_activity=Activity.STRENGTH,
            duration_minutes=30
        )
        workout3 = Workout.objects.create(
            name='Relaxing Yoga Flow',
            description='Gentle yoga sequence for stress relief',
            difficulty=Workout.LOW,
            recommended_activity=Activity.YOGA,
            duration_minutes=60
        )
        workout4 = Workout.objects.create(
            name='Evening Walk',
            description='Leisurely walking workout for recovery',
            difficulty=Workout.LOW,
            recommended_activity=Activity.WALKING,
            duration_minutes=30
        )
        self.stdout.write(f'Created {Workout.objects.count()} workouts.')

        # Create workout suggestions
        self.stdout.write('Creating workout suggestions...')
        WorkoutSuggestion.objects.create(
            user=users['tony_stark'],
            workout=workout1,
            suggested_date=date.today(),
            reason='Based on your running activity pattern'
        )
        WorkoutSuggestion.objects.create(
            user=users['steve_rogers'],
            workout=workout2,
            suggested_date=date.today() + timedelta(days=1),
            reason='Recommended for strength training beginners'
        )
        WorkoutSuggestion.objects.create(
            user=users['bruce_wayne'],
            workout=workout3,
            suggested_date=date.today(),
            reason='Perfect for your yoga routine'
        )
        WorkoutSuggestion.objects.create(
            user=users['clark_kent'],
            workout=workout4,
            suggested_date=date.today() + timedelta(days=2),
            reason='Light activity to complement your walking'
)
