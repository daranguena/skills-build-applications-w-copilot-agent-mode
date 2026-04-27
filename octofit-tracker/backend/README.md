# OctoFit Tracker Backend

Django REST API backend for the OctoFit Tracker fitness application.

## Project Structure

```
backend/
├── venv/                          # Python virtual environment
├── octofit_project/               # Django project configuration
│   ├── settings.py               # Django settings (MongoDB with Djongo)
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI configuration
│   ├── asgi.py                   # ASGI configuration
│   └── __init__.py
├── octofit_tracker/               # Main Django app
│   ├── models.py                 # Database models
│   ├── serializers.py            # DRF serializers
│   ├── views.py                  # Views and ViewSets
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Test cases
│   ├── management/
│   │   └── commands/
│   │       └── populate_testdata.py  # Management command to populate test data
│   └── __init__.py
├── manage.py                      # Django management script
├── setup_db.py                    # Database setup script
└── verify_db.py                   # Database verification script
```

## Installation & Setup

### 1. Activate Virtual Environment

```bash
source /workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend/venv/bin/activate
```

### 2. Run Setup Script

The setup script performs all database initialization and populates test data:

```bash
cd /workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend
python setup_db.py
```

This script will:
- Create Django migrations
- Apply migrations to MongoDB
- Create a superuser (admin/admin123)
- Populate the database with test data

### 3. Run the Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The API will be available at: `http://localhost:8000/api/`

## Database

- **Type**: MongoDB (via Djongo ORM)
- **Name**: `octofit_db`
- **Host**: localhost:27017

### Test Data

The setup includes test data for:
- 5 test users (testuser_alice, testuser_bob, etc.)
- User profiles with fitness goals
- 25 activity records (5 per user)
- 3 team records
- Weekly leaderboard
- Workout suggestions

## API Endpoints

All endpoints require authentication (token or session).

### Users
- `GET /api/users/` - List users
- `GET /api/users/{id}/` - Get user details
- `POST /api/auth/registration/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### Activities
- `GET /api/activities/` - List user's activities
- `POST /api/activities/` - Create new activity
- `GET /api/activities/{id}/` - Get activity details
- `PUT /api/activities/{id}/` - Update activity
- `DELETE /api/activities/{id}/` - Delete activity

### Teams
- `GET /api/teams/` - List teams
- `POST /api/teams/` - Create team
- `GET /api/teams/{id}/` - Get team details
- `PUT /api/teams/{id}/` - Update team
- `DELETE /api/teams/{id}/` - Delete team

### Leaderboard
- `GET /api/leaderboard/` - List leaderboards
- `GET /api/leaderboard/{id}/` - Get leaderboard details

### Workout Suggestions
- `GET /api/workout-suggestions/` - List suggestions
- `POST /api/workout-suggestions/` - Create suggestion
- `GET /api/workout-suggestions/{id}/` - Get suggestion details
- `PATCH /api/workout-suggestions/{id}/` - Mark as completed

## Django Admin

Access the admin interface at: `http://localhost:8000/admin/`

**Credentials:**
- Username: `admin`
- Password: `admin123`

## Testing

### Run All Tests

```bash
python manage.py test
```

### Run Tests for Specific App

```bash
python manage.py test octofit_tracker
```

### Run Specific Test Class

```bash
python manage.py test octofit_tracker.tests.UserProfileTestCase
```

## Database Verification

To verify that all data was properly populated:

```bash
python verify_db.py
```

This will show:
- MongoDB connection status
- Collections and document counts
- Sample data from each model

## Models

### UserProfile
- Extended user information (age, height, weight, activity level)
- Fitness goals

### Activity
- User activities (running, cycling, swimming, etc.)
- Duration, distance, calories burned
- Activity date and logging timestamp

### Team
- Team name and description
- Creator and members

### Leaderboard
- Weekly/monthly/yearly competitive rankings
- Team or global leaderboards

### LeaderboardEntry
- Individual user rankings
- Points, distance, calories, activity count

### WorkoutSuggestion
- Personalized workout recommendations
- Difficulty level and estimated duration

## Environment Variables

The application uses environment variables for Codespace support:

- `CODESPACE_NAME`: Automatically detected for GitHub Codespaces
- ALLOWED_HOSTS and CORS settings are updated accordingly

## Troubleshooting

### MongoDB Connection Error

Ensure MongoDB is running:

```bash
ps aux | grep mongod
```

If not running, start MongoDB:

```bash
mongod --dbpath /data/db
```

### Migration Issues

Reset and re-migrate:

```bash
python manage.py migrate octofit_tracker zero
python manage.py migrate octofit_tracker
```

### Create Superuser Manually

```bash
python manage.py createsuperuser
```

## Development Notes

- Database: Djongo ORM with MongoDB backend
- Authentication: Session and Token-based (via dj-rest-auth)
- CORS enabled for frontend development
- User permissions enforced at ViewSet level
