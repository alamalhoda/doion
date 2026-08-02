# E2E Local Runbook

**As of:** 2026-08-02  
**Scope:** Playwright smoke harness in this monorepo (`e2e/`) against the active UI (`checkyar-googleai`) and `doion` backend.

## Ownership

| Piece | Location | Who changes it |
|-------|----------|----------------|
| E2E harness (Playwright, scripts, smoke specs) | `doion/e2e/` | This monorepo (GitFlow) |
| Backend + `seed_demo` | `doion/backend/` | This monorepo |
| Active UI source | External `checkyar-googleai` | **Only via Google AI Studio → GitHub**; local = `git pull` only |
| Stable selectors (`data-testid`) | UI | Paste prompt from [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md) into AI Studio |

Do **not** commit UI source from the local `checkyar-googleai` clone.

## Prerequisites

- Backend venv: `backend/.venv`
- Bun on `PATH` for the UI clone (see [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md))
- UI `.env` (local, not committed):

```env
VITE_USE_MOCK=false
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

- Demo password for seed + E2E (pick one value and reuse):

```bash
export DEMO_SEED_PASSWORD='password123'
```

## One-shot local flow

### 1) Prepare isolated demo DB

From repo root:

```bash
./e2e/scripts/prepare-backend.sh
```

This sets `DJANGO_DEMO_DATABASE=1`, migrates `backend/db.demo.sqlite3`, and runs `seed_demo --reset`.

### 2) Start backend (demo DB)

```bash
cd backend
source .venv/bin/activate
export DJANGO_DEMO_DATABASE=1
python manage.py runserver 8000
```

### 3) Start UI (separate terminal)

```bash
cd /path/to/checkyar-googleai
git pull
bun install
bun run dev
```

UI: `http://localhost:3000`

### 4) Run smoke

```bash
cd e2e
export DEMO_SEED_PASSWORD='password123'
./scripts/run-smoke.sh
```

Or after `npm install` once (Playwright uses system **Google Chrome** by default via `channel: chrome` — needed on macOS 13 where bundled Chromium is unsupported):

```bash
cd e2e
npm install
npm run test:smoke
```

On newer CI hosts you may set `PLAYWRIGHT_CHANNEL=chromium` after `npx playwright install chromium`.
## Smoke coverage (current)

| Spec | User | Assert |
|------|------|--------|
| `login-holder.spec.ts` | `holder1` | lands on `/marketplace` |
| `login-investor-marketplace.spec.ts` | `investor1` | marketplace + at least one listing |
| `login-moderator.spec.ts` | `moderator1` | lands on `/moderation` |

Selectors prefer `data-testid` (after Studio prompt); fallbacks use current Persian labels/placeholders.

Until AI Studio applies prompt item **0** (`loadSavedUser` must not invent mock tokens when Live API is on), the harness uses a temporary guest localStorage seed in `e2e/support/auth.ts` so `/login` stays reachable.

## Demo users

Same as `seed_demo`: `holder1`, `investor1`, `moderator1`, `admin1` — password = `$DEMO_SEED_PASSWORD`.

Note: until AI Studio renames the mock persona, UI quick-login may still show `mod1`; E2E uses the form with `moderator1`.

## Out of scope (follow-ups)

- Critical-path flows (express interest, accept/reject, moderation decision)
- CI job for Playwright
- Visual regression

## Related

- Demo / seed SSOT: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
- UI policy: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md)
- AI Studio prep prompt: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md)
