#!/bin/bash
set -e

# Run migrations
poetry run python manage.py migrate

# Collect static files if not already done
poetry run python manage.py collectstatic --noinput

# Start the server
poetry run python manage.py runserver 0.0.0.0:8000