# OctoFit Tracker Backend - Quick Start Guide

## 🚀 30-Second Setup

```bash
# 1. Navigate to backend
cd /workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend

# 2. Activate environment (if needed)
source venv/bin/activate

# 3. Run setup
python setup_db.py

# 4. Start server
python manage.py runserver 0.0.0.0:8000
```

✅ Done! Visit http://localhost:8000/api/

---

## 📊 What Was Created

### Database
- **Type**: MongoDB (`octofit_db`)
- **Collections**: 7 (UserProfile, Activity, Team, Leaderboard, LeaderboardEntry, WorkoutSuggestion, + Django system)
- **Test Records**: 55+

### API Endpoints
- 6 main resources (users, activities, teams, leaderboards, workout-suggestions)
- 40+ total endpoints
- All require authentication

### Admin Interface
- Django admin at `/admin/`
- Credentials: `admin` / `admin123`
- Full CRUD for all models

---

## 🔧 Useful Commands

### Development
```bash
# Run server
python manage.py runserver 0.0.0.0:8000

# Run tests
python manage.py test

# Enter shell
python manage.py shell

# Create superuser
python manage.py createsuperuser
```

### Database
```bash
# Make migrations
python manage.py makemigrations octofit_tracker

# Apply migrations
python manage.py migrate

# Check status
python verify_db.py

# Populate test data
python manage.py populate_testdata
```

---

## 🔐 Test Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Test Users:** (password: `OctoFit@2024`)
- testuser_alice
- testuser_bob
- testuser_charlie
- testuser_diana
- testuser_evan

---

## 📡 API Quick Reference

### Authentication
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Register
curl -X POST http://localhost:8000/api/auth/registration/ \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "email": "user@test.com", "password1": "pass123", "password2": "pass123"}'
```

### Get Data
```bash
# List activities (replace TOKEN with actual token)
curl -H "Authorization: Token TOKEN" \
  http://localhost:8000/api/activities/

# List teams
curl -H "Authorization: Token TOKEN" \
  http://localhost:8000/api/teams/

# Get leaderboard
curl -H "Authorization: Token TOKEN" \
  http://localhost:8000/api/leaderboard/
```

### Create Data
```bash
# Create activity
curl -X POST http://localhost:8000/api/activities/ \
  -H "Authorization: Token TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "activity_type": "running",
    "title": "Morning Run",
    "duration_minutes": 30,
    "distance_km": 5.0,
    "intensity": "moderate",
    "activity_date": "2024-04-23"
  }'
```

---

## 🐛 Troubleshooting

**MongoDB not running?**
```bash
ps aux | grep mongod
# If not found, start it
mongod --dbpath /data/db
```

**Port 8000 in use?**
```bash
python manage.py runserver 0.0.0.0:8001
```

**Reset database?**
```bash
# Delete test data
rm octofit_tracker/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
python setup_db.py
```

**Tests failing?**
```bash
python manage.py test -v 2
# See detailed output for debugging
```

---

## 📂 File Structure

```
backend/
├── manage.py                  ← Main Django script
├── setup_db.py               ← Initialize everything
├── verify_db.py              ← Check database
├── run_setup.sh              ← Shell script version
├── octofit_project/          ← Django config
│   ├── settings.py          ← MongoDB config
│   ├── urls.py              ← API routes
│   ├── wsgi.py
│   └── asgi.py
└── octofit_tracker/          ← Main app
    ├── models.py            ← 6 data models
    ├── serializers.py       ← REST serializers
    ├── views.py             ← 6 ViewSets
    ├── admin.py             ← Admin config
    ├── tests.py             ← Test suite
    ├── migrations/          ← Django migrations
    └── management/commands/ ← Management commands
```

---

## 🎯 Next Steps

1. ✅ **Backend Setup** (DONE)
   - Models created
   - API endpoints working
   - Test data populated
   - Admin interface ready

2. 📱 **Frontend Setup** (Next)
   - React app in `/frontend/`
   - Connect to API
   - Implement UI

3. 🚀 **Deployment** (Later)
   - Production settings
   - Environment variables
   - Database backup

---

## 📚 Full Documentation

- `README.md` - Detailed overview
- `SETUP_GUIDE.md` - Complete setup instructions
- `IMPLEMENTATION_SUMMARY.md` - What was built

---

## ✨ Features Ready to Use

- ✅ User authentication & profiles
- ✅ Activity logging & tracking  
- ✅ Team creation & management
- ✅ Leaderboard tracking
- ✅ Personalized workout suggestions
- ✅ Django admin interface
- ✅ Comprehensive test suite
- ✅ Full API documentation (browsable)

---

**Ready to go! Visit http://localhost:8000/api/** 🎉
