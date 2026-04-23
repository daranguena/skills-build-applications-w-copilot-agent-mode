from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from tracker.models import Activity, Profile, Team, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()

        # Borrar datos existentes
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Crear equipos
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Crear usuarios
        tony = User.objects.create_user(username='tony', email='tony@stark.com', password='pass1234')
        steve = User.objects.create_user(username='steve', email='steve@rogers.com', password='pass1234')
        bruce = User.objects.create_user(username='bruce', email='bruce@wayne.com', password='pass1234')
        clark = User.objects.create_user(username='clark', email='clark@kent.com', password='pass1234')

        # Asignar equipos a los perfiles
        for user, team in [
            (tony, marvel),
            (steve, marvel),
            (bruce, dc),
            (clark, dc),
        ]:
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.team = team
            profile.save()

        # Crear actividades
        Activity.objects.create(user=tony, activity_type=Activity.RUNNING, duration_minutes=30, distance_km=5.0, calories_burned=320)
        Activity.objects.create(user=steve, activity_type=Activity.WALKING, duration_minutes=45, distance_km=6.0, calories_burned=300)
        Activity.objects.create(user=bruce, activity_type=Activity.YOGA, duration_minutes=60, calories_burned=200)
        Activity.objects.create(user=clark, activity_type=Activity.STRENGTH, duration_minutes=20, calories_burned=150)

        # Crear workouts
        Workout.objects.create(
            name='Full Body Circuit',
            description='A full-body workout that blends strength and cardio.',
            difficulty=Workout.MEDIUM,
            recommended_activity=Activity.STRENGTH,
            duration_minutes=40,
        )
        Workout.objects.create(
            name='Morning Cardio',
            description='A light cardio routine for daily energy.',
            difficulty=Workout.LOW,
            recommended_activity=Activity.WALKING,
            duration_minutes=30,
        )

        for user in [tony, steve, bruce, clark]:
            profile = getattr(user, 'profile', None)
            if profile:
                profile.refresh_total_points()

        self.stdout.write(self.style.SUCCESS('Base de datos poblada con datos de prueba.'))
