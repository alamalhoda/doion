#!/bin/bash
# Chabokan pre-start hook: run before Gunicorn starts.
# Docs: https://docs.chabokan.net/cloud-hosting/django/migrations/
set -euo pipefail

python manage.py migrate --noinput
python manage.py collectstatic --noinput
