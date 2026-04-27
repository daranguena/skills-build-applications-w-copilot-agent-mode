from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tracker.models import Team, Activity, Workout, WorkoutSuggestion
from datetime import date, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        WorkoutSuggestion.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()  # Keep superuser
        Team.objects.all().delete()
        self.stdout.write('Data cleared.')

        # Create teams
        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel', description='Superhero team from Marvel Comics')
        dc = Team.objects.create(name='DC', description='Superhero team from DC Comics')
        self.stdout.write(f'Created {Team.objects.count()} teams.')

        # Create users
        self.stdout.write('Creating users...')
        tony = User.objects.create_user(
            username='tony_stark',
            email='tony@stark.com',
            first_name='Tony',
            last_name='Stark',
            password='password123'
        )
        steve = User.objects.create_user(
            username='steve_rogers',
            email='steve@rogers.com',
            first_name='Steve',
            last_name='Rogers',
            password='password123'
        )
        bruce = User.objects.create_user(
            username='bruce_wayne',
            email='bruce@wayne.com',
            first_name='Bruce',
            last_name='Wayne',
            password='password123'
        )
        clark = User.objects.create_user(
            username='clark_kent',
            email='clark@kent.com',
            first_name='Clark',
            last_name='Kent',
            password='password123'
        )
        self.stdout.write(f'Created {User.objects.count()} users.')

        # Set team captains and add members
        self.stdout.write('Setting team relationships...')
        marvel.captain = tony
        marvel.save()
        marvel.members.add(tony, steve)

        dc.captain = bruce
        dc.save()
        dc.members.add(bruce, clark)
        self.stdout.write('Team relationships set.')

        # Create activities
        self.stdout.write('Creating activities...')
        Activity.objects.create(
            user=tony,
            activity_type=Activity.RUNNING,
            duration_minutes=30,
            distance_km=5.0,
            calories_burned=300
        )
        Activity.objects.create(
            user=steve,
            activity_type=Activity.STRENGTH,
            duration_minutes=45,
            calories_burned=250
        )
        Activity.objects.create(
            user=bruce,
            activity_type=Activity.YOGA,
            duration_minutes=60,
            calories_burned=150
        )
        Activity.objects.create(
            user=clark,
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
            user=tony,
            workout=workout1,
            suggested_date=date.today(),
            reason='Based on your running activity pattern'
        )
        WorkoutSuggestion.objects.create(
            user=steve,
            workout=workout2,
            suggested_date=date.today() + timedelta(days=1),
            reason='Recommended for strength training beginners'
        )
        WorkoutSuggestion.objects.create(
            user=bruce,
            workout=workout3,
            suggested_date=date.today(),
            reason='Perfect for your yoga routine'
        )
        WorkoutSuggestion.objects.create(
            user=clark,
            workout=workout4,
            suggested_date=date.today() + timedelta(days=2),
            reason='Light activity to complement your walking'
        )
        self.stdout.write(f'Created {WorkoutSuggestion.objects.count()} workout suggestions.')

        self.stdout.write(self.style.SUCCESS('Database populated with test data successfully!'))
        self.stdout.write(f'Created {Team.objects.count()} teams')
        self.stdout.write(f'Created {User.objects.count()} users')
        self.stdout.write(f'Created {Activity.objects.count()} activities')
        self.stdout.write(f'Created {Workout.objects.count()} workouts')
        self.stdout.write(f'Created {WorkoutSuggestion.objects.count()} workout suggestions')
