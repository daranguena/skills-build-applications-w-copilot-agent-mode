# OctoFit Tracker Backend - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Applications                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  React Web   │  │  Mobile App  │  │ Admin Panel  │           │
│  │   Frontend   │  │  (Future)    │  │             │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└────────────────────────┬──────────────────────────────────────────┘
                         │ HTTPS/HTTP
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                    Django REST API                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Routing (urls.py)                        │ │
│  │  /api/users/           /api/activities/                    │ │
│  │  /api/teams/           /api/leaderboard/                   │ │
│  │  /api/workout-suggestions/                                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                         │                                         │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │            REST Framework ViewSets (views.py)            │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │  │
│  │  │   User       │ │   Activity   │ │    Teams     │     │  │
│  │  │   ViewSet    │ │   ViewSet    │ │   ViewSet    │     │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘     │  │
│  │  ┌──────────────┐ ┌──────────────┐                       │  │
│  │  │ Leaderboard  │ │   Workout    │                       │  │
│  │  │   ViewSet    │ │  Suggestion  │                       │  │
│  │  └──────────────┘ │   ViewSet    │                       │  │
│  │                   └──────────────┘                       │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          │                                       │
│  ┌───────────────────────▼──────────────────────────────────┐  │
│  │          Serializers (serializers.py)                    │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │ Data Validation & Transformation                 │  │  │
│  │  │ ObjectId → String conversion (MongoDB)           │  │  │
│  │  │ Nested relationships handling                    │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          │                                       │
│  ┌───────────────────────▼──────────────────────────────────┐  │
│  │           Permission & Authentication                    │  │
│  │  • IsAuthenticated on all endpoints                      │  │
│  │  • User-scoped data access                              │  │
│  │  • Token & Session authentication                       │  │
│  └───────────────────────┬──────────────────────────────────┘  │
│                          │                                       │
└──────────────────────────┼───────────────────────────────────────┘
                           │ ORM
┌──────────────────────────▼───────────────────────────────────────┐
│                   Django ORM Models (models.py)                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Model Layer (6 Models)                                  │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │  │
│  │  │ UserProfile  │ │   Activity   │ │    Team      │    │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘    │  │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │  │
│  │  │ Leaderboard  │ │ LeaderboardE │ │   Workout    │    │  │
│  │  │              │ │   ntry       │ │ Suggestion   │    │  │
│  │  └──────────────┘ └──────────────┘ └──────────────┘    │  │
│  │                                                          │  │
│  │  Field Types:                                          │  │
│  │  • CharField, IntegerField, FloatField                │  │
│  │  • DateField, DateTimeField                           │  │
│  │  • ForeignKey, ManyToManyField                        │  │
│  │  • Choices for enums                                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                          │                                      │
└──────────────────────────┼──────────────────────────────────────┘
                           │ Djongo
┌──────────────────────────▼──────────────────────────────────────┐
│           Djongo ORM - MongoDB Adapter                           │
│  Converts Django models to MongoDB collections                  │
│  with proper serialization and deserialization                  │
└──────────────────────────┼──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│              MongoDB Database (octofit_db)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Collections:                                            │  │
│  │  • user_profiles        • activities                    │  │
│  │  • teams                • leaderboards                  │  │
│  │  • leaderboard_entries  • workout_suggestions           │  │
│  │  • Django system collections                            │  │
│  │                                                         │  │
│  │  Document Format: BSON (Binary JSON)                    │  │
│  │  Storage: /data/db                                      │  │
│  │  Port: 27017                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
REQUEST FLOW (from client to database):
═══════════════════════════════════════

Client Request
     │
     ▼
HTTP/HTTPS (REST)
     │
     ▼
Django URL Router (urls.py)
     │
     ▼
View/ViewSet (views.py)
     │
     ├──► Check Authentication
     │    └──► IsAuthenticated
     │
     ├──► Check Permissions
     │    └──► User-scoped data
     │
     ▼
Request Processing
     │
     ├──► GET Request ──► Fetch from DB ──┐
     ├──► POST Request ──► Validate ──┬───┤
     ├──► PUT Request ──► Transform ──┤   ├──► Serializer (serializers.py)
     └──► DELETE Request ──────────────┘   │   │
                                           │   ├──► ObjectId ↔ String
                                           │   ├──► Validation
                                           │   └──► Transformation
                                           │
                                           ▼
                                    ORM Query
                                           │
                                           ▼
                                       Djongo ORM
                                           │
                                           ▼
                                    MongoDB Collection
                                           │
                                           ▼
                                    Database Response
                                           │
                                           ▼
                                       Serializer
                                    (Convert to JSON)
                                           │
                                           ▼
                                    HTTP Response
                                    (JSON + Status Code)
                                           │
                                           ▼
                                        Client
```

---

## Database Schema

```
USER_PROFILES Collection
═══════════════════════════════════
{
  _id: ObjectId
  user_id: Integer (FK)
  age: Integer
  height: Float
  weight: Float
  activity_level: String (enum)
  fitness_goal: String
  created_at: DateTime
  updated_at: DateTime
}

ACTIVITIES Collection
══════════════════════════════════
{
  _id: ObjectId
  user_id: Integer (FK)
  activity_type: String (enum)
  title: String
  description: String
  duration_minutes: Integer
  distance_km: Float
  calories_burned: Integer
  intensity: String (enum)
  logged_at: DateTime
  activity_date: Date
}

TEAMS Collection
═══════════════════════════════════
{
  _id: ObjectId
  name: String
  description: String
  creator_id: Integer (FK)
  members_ids: Array[Integer] (MM)
  created_at: DateTime
  updated_at: DateTime
}

LEADERBOARDS Collection
═══════════════════════════════════
{
  _id: ObjectId
  team_id: ObjectId (FK, optional)
  leaderboard_type: String (enum)
  period_start: Date
  period_end: Date
  created_at: DateTime
  updated_at: DateTime
}

LEADERBOARD_ENTRIES Collection
═══════════════════════════════════
{
  _id: ObjectId
  leaderboard_id: ObjectId (FK)
  user_id: Integer (FK)
  rank: Integer
  total_points: Integer
  total_distance_km: Float
  total_calories: Integer
  total_activities: Integer
  created_at: DateTime
  updated_at: DateTime
}

WORKOUT_SUGGESTIONS Collection
═══════════════════════════════════
{
  _id: ObjectId
  user_id: Integer (FK)
  title: String
  description: String
  suggested_activity_type: String
  difficulty_level: String (enum)
  estimated_duration_minutes: Integer
  reason: String
  is_completed: Boolean
  created_at: DateTime
  updated_at: DateTime
}
```

---

## REST API Endpoint Structure

```
API Root: /api/
│
├── Users Management
│   ├── GET    /api/users/               → List all users (paginated)
│   ├── POST   /api/users/               → Create user (registration)
│   ├── GET    /api/users/{id}/          → Get user details
│   ├── PUT    /api/users/{id}/          → Update user (full)
│   └── PATCH  /api/users/{id}/          → Update user (partial)
│
├── Activities
│   ├── GET    /api/activities/          → List user's activities
│   ├── POST   /api/activities/          → Create activity
│   ├── GET    /api/activities/{id}/     → Get activity details
│   ├── PUT    /api/activities/{id}/     → Update activity (full)
│   └── DELETE /api/activities/{id}/     → Delete activity
│
├── Teams
│   ├── GET    /api/teams/               → List teams
│   ├── POST   /api/teams/               → Create team
│   ├── GET    /api/teams/{id}/          → Get team details
│   ├── PUT    /api/teams/{id}/          → Update team (full)
│   └── DELETE /api/teams/{id}/          → Delete team
│
├── Leaderboards
│   ├── GET    /api/leaderboard/         → List leaderboards
│   ├── POST   /api/leaderboard/         → Create leaderboard
│   └── GET    /api/leaderboard/{id}/    → Get leaderboard details
│
├── Workout Suggestions
│   ├── GET    /api/workout-suggestions/ → List suggestions
│   ├── POST   /api/workout-suggestions/ → Create suggestion
│   ├── GET    /api/workout-suggestions/{id}/     → Get details
│   ├── PATCH  /api/workout-suggestions/{id}/     → Mark complete
│   └── DELETE /api/workout-suggestions/{id}/     → Delete
│
└── Authentication
    ├── POST   /api/auth/login/          → Token login
    ├── POST   /api/auth/logout/         → Token logout
    ├── POST   /api/auth/registration/   → User registration
    └── GET    /api-auth/login/          → Session login page
```

---

## Authentication Flow

```
Authentication Methods:
════════════════════════

1. Token Authentication (API)
   ┌─────────────────────┐
   │  Client: POST login │
   │  { username, pw }   │
   └──────────┬──────────┘
              │
              ▼
        ┌─────────────────┐
        │  Verify Creds   │
        │  (Django Auth)  │
        └────────┬────────┘
                 │
                 ▼
         ┌──────────────────┐
         │ Generate Token   │
         │ (DRF Token Auth) │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Return Token     │
         │ to Client        │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Client stores    │
         │ token locally    │
         └────────┬─────────┘
                  │
         Subsequent Requests:
         Header: Authorization: Token <token>
                  │
                  ▼
         ┌──────────────────┐
         │ Verify Token     │
         │ in request       │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Grant Access     │
         │ to endpoint      │
         └──────────────────┘

2. Session Authentication (Web Browser)
   ├── POST /api-auth/login/
   ├── Cookie-based session
   ├── Auto-included in requests
   └── CSRF token required for modifications
```

---

## Permission & Authorization

```
Permission Hierarchy:
════════════════════════

All API Endpoints
    │
    └──► IsAuthenticated Required
         ├──► Get user from request.user
         │
         ├── UserViewSet
         │   └──► Users see only themselves (unless staff)
         │
         ├── ActivityViewSet
         │   └──► Users see only their activities
         │
         ├── TeamViewSet
         │   └──► Users see teams they're members of
         │
         ├── WorkoutSuggestionViewSet
         │   └──► Users see only their suggestions
         │
         └── LeaderboardViewSet
             └──► All authenticated users can view

Staff Users (/admin/)
    ├──► Can view/edit all data
    ├──► Can create users
    ├──► Can manage permissions
    └──► Full database access
```

---

## Development Workflow

```
Setup Development Environment:
═════════════════════════════════

1. Clone/Access Repository
   └──► /workspaces/skills-build-applications-w-copilot-agent-mode/

2. Navigate to Backend
   └──► octofit-tracker/backend/

3. Activate Virtual Environment
   └──► source venv/bin/activate

4. Install Dependencies (already done)
   └──► pip install -r requirements.txt

5. Configure Environment
   ├──► MongoDB running on localhost:27017
   └──► Django settings configured (octofit_project/settings.py)

6. Initialize Database
   └──► python setup_db.py
        ├──► Creates migrations
        ├──► Applies migrations
        ├──► Creates superuser
        └──► Populates test data

7. Run Development Server
   └──► python manage.py runserver 0.0.0.0:8000

8. Access Application
   ├──► API: http://localhost:8000/api/
   ├──► Admin: http://localhost:8000/admin/
   └──► Shell: python manage.py shell

9. Run Tests
   └──► python manage.py test

10. Verify Database
    └──► python verify_db.py
```

---

## Technology Stack

```
Backend Framework:
  • Django 4.1.7 - Web framework
  • Django REST Framework 3.14.0 - REST API
  • Djongo 1.3.6 - ORM for MongoDB

Database:
  • MongoDB 5.0+ - NoSQL database
  • PyMongo 3.12 - MongoDB driver

Authentication:
  • dj-rest-auth 2.2.6 - REST auth endpoints
  • django-allauth 0.51.0 - Auth backends
  • Django Session Auth - Built-in

API Features:
  • django-cors-headers 4.5.0 - CORS support
  • DRF Pagination - Built-in
  • DRF Browsable API - Built-in

Development:
  • Python 3.10.12
  • Virtual Environment (venv)
```

---

## Scalability Considerations

```
Current Architecture:
  • Single Django instance
  • Single MongoDB instance
  • Suitable for development/low-traffic

Scaling Paths:
  1. Horizontal Scaling
     ├──► Multiple Django servers
     ├──► Load balancer (nginx)
     └──► Shared MongoDB instance

  2. Vertical Scaling
     ├──► Larger server instance
     ├──► Database indexing
     └──► Query optimization

  3. Caching Layer
     ├──► Redis for session storage
     ├──► Cache frequent queries
     └──► Cache API responses

  4. Database Optimization
     ├──► Proper MongoDB indexing
     ├──► Query optimization
     └──► Sharding for large datasets
```

---

This architecture provides:
✅ Clear separation of concerns
✅ RESTful API design
✅ Proper authentication & permissions
✅ MongoDB integration via Djongo
✅ Scalable foundation
✅ Django admin for management
✅ Comprehensive test coverage
