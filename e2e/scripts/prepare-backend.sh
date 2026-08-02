#!/usr/bin/env bash
# Prepare isolated demo SQLite + seed for E2E (does not start runserver).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"

cd "${BACKEND_DIR}"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
else
  echo "error: backend/.venv not found. Create/activate the project venv first." >&2
  exit 1
fi

export DJANGO_DEMO_DATABASE=1
export DEMO_SEED_PASSWORD="${DEMO_SEED_PASSWORD:-password123}"

echo "==> migrate (db.demo.sqlite3)"
python manage.py migrate

echo "==> seed_demo --reset"
python manage.py seed_demo --reset --password "${DEMO_SEED_PASSWORD}"

echo "Demo DB ready. Start API with:"
echo "  cd backend && source .venv/bin/activate && export DJANGO_DEMO_DATABASE=1 && python manage.py runserver 8000"
echo "Password for demo users: ${DEMO_SEED_PASSWORD}"
