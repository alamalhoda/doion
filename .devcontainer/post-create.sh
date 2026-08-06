#!/usr/bin/env bash
# Codespaces / Dev Container bootstrap for doion + optional UI clone.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}/backend"

echo "==> Install uv + sync backend"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="${HOME}/.local/bin:${PATH}"
uv sync

echo "==> Migrate + seed demo DB"
export DJANGO_DEMO_DATABASE="${DJANGO_DEMO_DATABASE:-1}"
export DEMO_SEED_PASSWORD="${DEMO_SEED_PASSWORD:-password123}"
uv run python manage.py migrate --noinput
uv run python manage.py seed_demo --password "${DEMO_SEED_PASSWORD}" --reset

UI_DIR="${ROOT}/../checkyar-googleai"
if [[ ! -d "${UI_DIR}" ]]; then
  echo "==> Clone active UI next to workspace (if token/network allows)"
  git clone https://github.com/alamalhoda/checkyar-googleai.git "${UI_DIR}" || {
    echo "warn: could not clone UI; clone manually beside doion and bun install"
  }
fi

if [[ -d "${UI_DIR}" ]]; then
  if ! command -v bun >/dev/null 2>&1; then
    curl -fsSL https://bun.sh/install | bash
    export PATH="${HOME}/.bun/bin:${PATH}"
  fi
  cd "${UI_DIR}"
  printf 'VITE_USE_MOCK=false\nVITE_API_BASE_URL=http://127.0.0.1:8000/api/v1\n' > .env
  bun install
  echo "==> UI ready. Run: bun run dev -- --host 127.0.0.1 --port 3000"
fi

echo "==> Backend: uv run python manage.py runserver 127.0.0.1:8000"
echo "Codespaces = development only. Production = Chabokan (see docs/development/PRODUCTION_CHABOKAN_DEPLOY.md)."
