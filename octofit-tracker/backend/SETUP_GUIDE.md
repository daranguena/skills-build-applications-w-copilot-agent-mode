# OctoFit Tracker Backend - Complete Setup Guide

## Prerequisites

- Python 3.8+
- MongoDB running on localhost:27017
- Virtual environment already created with required packages

## Step-by-Step Setup

### Step 1: Navigate to Backend Directory

```bash
cd /workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend
```

### Step 2: Verify Virtual Environment

```bash
source venv/bin/activate
which python
```

You should see the venv path in the output.

### Step 3: Verify MongoDB is Running

```bash
ps aux | grep mongod
```

If MongoDB is not running, start it:
```bash
mongod --dbpath /data/db
```

### Step 4: Run Database Setup

This script will handle everything:

```bash
python setup_db.py
```

**What this does:**
1. Creates Django migrations for all models
2. Applies migrations to MongoDB
3. Creates superuser account (admin/admin123)
4. Clears any previous test data
5. Populates fresh test data
6. Displays summary statistics

### Step 5: Verify Database Population

```bash
python verify_db.py
```

This will show:
- MongoDB connection status
- Document counts per collection
- Sample data from each model

### Step 6: Start Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

The server will start on `http://localhost:8000`

### Step 7: Access the Application

**API Root:**
- http://localhost:8000/api/

**Django Admin:**
- http://localhost:8000/admin/
- Username: `admin`
- Password: `admin123`

**API Documentation (via browsable API):**
- Visit any endpoint and you'll see the browsable API interface

## Database Schema

### Collections Created

1. **user_profiles** - Extended user information
2. **activities** - Activity logs
3. **teams** - Team groupings
4. **leaderboards** - Competitive leaderboards
5. **leaderboard_entries** - Individual rankings
6. **workout_suggestions** - Personalized suggestions
7. Django system collections (auth, contenttypes, etc.)

### Test Data Created

| Model | Count | Details |
|-------|-------|---------|
| Users | 6 | 1 admin + 5 test users |
| UserProfiles | 5 | Varied ages and fitness goals |
| Activities | 25 | 5 activities per user |
| Teams | 3 | Different member compositions |
| Leaderboards | 1 | Weekly leaderboard |
| LeaderboardEntries | 5 | Ranked entries for team 1 |
| WorkoutSuggestions | 5 | 1 per test user |

## Testing the API

### Authentication

Most endpoints require authentication. Test with curl:

```bash
# Get CSRF token from login page
curl -c cookies.txt http://localhost:8000/api-auth/login/

# Login with credentials
curl -b cookies.txt -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser_alice", "password": "OctoFit@2024"}'

# Use token in requests
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/users/
```

### Example API Calls

**List all users:**
```bash
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Create an activity:**
```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "activity_type": "running",
    "title": "Morning Jog",
    "duration_minutes": 30,
    "distance_km": 5.0,
    "intensity": "moderate",
    "activity_date": "2024-04-23"
  }'
```

**Get leaderboard:**
```bash
curl -X GET http://localhost:8000/api/leaderboard/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Troubleshooting

### Issue: MongoDB Connection Error

**Error:** `Cannot connect to MongoDB`

**Solution:**
```bash
# Check if MongoDB is running
ps aux | grep mongod

# If not, start MongoDB (adjust path as needed)
mongod --dbpath /data/db &

# Verify connection
mongosh
> show databases
> use octofit_db
> show collections
```

### Issue: Django Migration Error

**Error:** `No changes detected in app 'octofit_tracker'`

**Solution:**
```bash
# Clear migrations and start fresh
rm octofit_tracker/migrations/0*.py
python manage.py makemigrations octofit_tracker
python manage.py migrate
python setup_db.py
```

### Issue: Superuser Already Exists

**Error:** `IntegrityError: E11000 duplicate key error`

**Solution:**
The script checks if admin exists before creating. Delete test data:
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(username='admin').delete()
>>> exit()
```

Then run setup_db.py again.

### Issue: Port 8000 Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Run on different port
python manage.py runserver 0.0.0.0:8001

# Or find and kill the process
lsof -i :8000
kill -9 <PID>
```

## Development Workflow

### Creating a New API Endpoint

1. **Add Model** (if needed):
   ```python
   # octofit_tracker/models.py
   class YourModel(models.Model):
       # fields...
       class Meta:
           db_table = 'your_models'
   ```

2. **Create Serializer**:
   ```python
   # octofit_tracker/serializers.py
   class YourModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = YourModel
           fields = ['id', 'field1', 'field2']
   ```

3. **Create ViewSet**:
   ```python
   # octofit_tracker/views.py
   class YourModelViewSet(viewsets.ModelViewSet):
       queryset = YourModel.objects.all()
       serializer_class = YourModelSerializer
       permission_classes = [IsAuthenticated]
   ```

4. **Register Route**:
   ```python
   # octofit_project/urls.py
   router.register(r'your-models', YourModelViewSet, basename='yourmodel')
   ```

5. **Create Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Add Tests**:
   ```python
   # octofit_tracker/tests.py
   class YourModelTestCase(TestCase):
       def test_creation(self):
           # your test...
   ```

### Running Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test octofit_tracker

# With verbose output
python manage.py test -v 2

# Specific test class
python manage.py test octofit_tracker.tests.ActivityAPITestCase
```

## Project Files Summary

| File | Purpose |
|------|---------|
| `manage.py` | Django CLI tool |
| `setup_db.py` | Complete database initialization |
| `verify_db.py` | Data verification and statistics |
| `octofit_project/settings.py` | Django configuration (MongoDB) |
| `octofit_project/urls.py` | URL routing and API root |
| `octofit_project/wsgi.py` | WSGI application |
| `octofit_tracker/models.py` | Data models |
| `octofit_tracker/serializers.py` | REST API serializers |
| `octofit_tracker/views.py` | API views and viewsets |
| `octofit_tracker/admin.py` | Admin interface configuration |
| `octofit_tracker/tests.py` | Unit and integration tests |

## Next Steps

1. ✅ Backend structure set up
2. ✅ Database configured and populated
3. Next: Set up React frontend in `/octofit-tracker/frontend`
4. Configure CORS for frontend communication
5. Implement additional features (notifications, analytics, etc.)

## Useful Commands Reference

```bash
# Development server
python manage.py runserver 0.0.0.0:8000

# Interactive shell
python manage.py shell

# Database shell
mongosh

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Check deployment
python manage.py check --deploy

# Monitor MongoDB
mongosh octofit_db
> db.activities.count()
```

## Support

For issues or questions:
1. Check MongoDB is running
2. Verify virtual environment is activated
3. Review test output from `python manage.py test`
4. Check Django debug output with DEBUG=True in settings.py
