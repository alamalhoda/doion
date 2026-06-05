#!/usr/bin/env bash
# Run script: activates venv if needed and starts Django dev server

# Check if virtual environment is already activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Virtual environment not activated. Activating..."
    source backend/.venv/bin/activate
fi

# Ensure we are in the project root
cd "$(dirname "$0")/backend"

# Run the Django development server
python manage.py runserver