#!/bin/bash
# Vercel build script - runs pip install + collectstatic + migrate

set -e  # Exit immediately if any command fails

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Build complete!"
