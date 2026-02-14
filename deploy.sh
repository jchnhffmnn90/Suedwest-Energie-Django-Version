#!/bin/bash

# Südwest Energie Deployment Script
# This script automates common production setup tasks.

echo "--- Starting Deployment Preparation ---"

# 1. Install/Update dependencies
if [ -d "venv" ]; then
    echo "Using existing virtual environment..."
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

echo "Installing requirements..."
pip install -r requirements.txt

# 2. Run Migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# 3. Collect Static Files
echo "Collecting static files (Whitenoise)..."
python manage.py collectstatic --noinput

# 4. Security Check
echo "Running Django security check..."
python manage.py check --deploy

echo "--- Preparation Complete ---"
echo "Next steps:"
echo "1. Ensure your .env file is correctly configured."
echo "2. Start the application using Gunicorn:"
echo "   gunicorn suedwest_project.wsgi:application"
echo "3. Configure Nginx and SSL (Certbot)."
