#!/usr/bin/env bash
# Run critical-path specs. Prerequisites: backend (:8000) + UI (:3000, VITE_USE_MOCK=false) already up.
# Prefer: ./scripts/prepare-backend.sh then start both servers, then this script.
set -euo pipefail

E2E_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${E2E_DIR}"

FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}"
API_URL="${API_URL:-http://localhost:8000/api/v1}"

echo "==> checking frontend ${FRONTEND_URL}"
curl --connect-timeout 5 -m 10 -sf -o /dev/null "${FRONTEND_URL}/" || {
  echo "error: frontend not reachable at ${FRONTEND_URL}" >&2
  echo "tip: bind Vite to loopback if needed: bun run dev -- --host 127.0.0.1 --port 3000" >&2
  exit 1
}

echo "==> checking API login"
LOGIN_CODE=$(curl --connect-timeout 5 -m 10 -s -o /tmp/e2e-login-probe.json -w "%{http_code}" -X POST "${API_URL}/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{\"identifier\":\"holder1\",\"password\":\"${DEMO_SEED_PASSWORD:-password123}\"}")
if [[ "${LOGIN_CODE}" != "200" ]]; then
  echo "error: login probe HTTP ${LOGIN_CODE}. Is backend seeded and running with DJANGO_DEMO_DATABASE=1?" >&2
  exit 1
fi

if [[ ! -d node_modules ]]; then
  echo "==> npm install"
  npm install
fi

echo "==> playwright critical (channel=chrome on macOS 13)"
export FRONTEND_URL
export API_URL
export DEMO_SEED_PASSWORD="${DEMO_SEED_PASSWORD:-password123}"
npm run test:critical
