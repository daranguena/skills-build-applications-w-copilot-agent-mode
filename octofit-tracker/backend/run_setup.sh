#!/bin/bash
# Setup script for OctoFit Tracker Django backend

set -e

PYTHON="/workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend/venv/bin/python"
MANAGE="$PYTHON /workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend/manage.py"
BACKEND_DIR="/workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend"

echo "========================================="
echo "OctoFit Tracker Django Setup"
echo "========================================="

cd "$BACKEND_DIR"

# Check if MongoDB is running
echo ""
echo "Checking MongoDB connection..."
if pgrep -x "mongod" > /dev/null; then
    echo "✓ MongoDB is running"
else
    echo "⚠ MongoDB might not be running. Make sure MongoDB is started."
fi

# Run migrations
echo ""
echo "Running Django migrations..."
$MANAGE makemigrations octofit_tracker
$MANAGE migrate

# Create superuser
echo ""
echo "Creating superuser (admin/admin123)..."
$PYTHON << END
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_project.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@octofit.test', 'admin123')
    print("✓ Superuser created: admin (password: admin123)")
else:
    print("✓ Superuser already exists")
END

# Populate test data
echo ""
echo "Populating test data..."
$MANAGE populate_testdata

echo ""
echo "========================================="
echo "✓ Setup completed successfully!"
echo "========================================="
echo ""
echo "Django Development Server:"
echo "  Run: python manage.py runserver 0.0.0.0:8000"
echo ""
echo "API Endpoints:"
echo "  Base URL: http://localhost:8000/api/"
echo "  Users: http://localhost:8000/api/users/"
echo "  Activities: http://localhost:8000/api/activities/"
echo "  Teams: http://localhost:8000/api/teams/"
echo "  Admin: http://localhost:8000/admin/ (admin/admin123)"
echo ""
