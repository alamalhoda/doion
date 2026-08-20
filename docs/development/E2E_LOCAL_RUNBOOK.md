# E2E Local Runbook

**As of:** 2026-08-06  
**Scope:** Playwright harness in this monorepo (`e2e/`) against the active UI (`checkyar-googleai`) and `doion` backend — smoke + critical-path.

## Ownership

| Piece | Location | Who changes it |
|-------|----------|----------------|
| E2E harness (Playwright, scripts, smoke/critical specs) | `doion/e2e/` | This monorepo (GitFlow) |
| Backend + `seed_demo` | `doion/backend/` | This monorepo |
| Active UI source | External `checkyar-googleai` | **Only via Google AI Studio → GitHub**; local = `git pull` only |
| Stable selectors (`data-testid`) | UI | Smoke: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md); critical: [`AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md`](./AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md) |

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

This sets `DJANGO_DEMO_DATABASE=1`, migrates `backend/db.demo.sqlite3`, and runs `seed_demo --reset` (rich fixtures: 22 published, 12 pending, 12 holder notifications — see [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)).

### 2) Start backend (demo DB)

```bash
cd backend
source .venv/bin/activate
export DJANGO_DEMO_DATABASE=1
python manage.py runserver 8000
```

### 3) Start UI (separate terminal)

Bind Vite to loopback (avoids VPN/TUN `ERR_CONNECTION_TIMED_OUT` on `0.0.0.0` — details: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md#local-vite-host-recommended)):

```bash
cd /path/to/checkyar-googleai
git pull
bun install
bun run dev -- --host 127.0.0.1 --port 3000
```

UI: `http://127.0.0.1:3000` (set `FRONTEND_URL=http://127.0.0.1:3000` for Playwright if needed)

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

### 5) Run critical-path

Prefer after AI Studio applies [`AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md`](./AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md) (testid-first; Persian fallbacks still present):

```bash
cd e2e
export DEMO_SEED_PASSWORD='password123'
./scripts/run-critical.sh
# or: npm run test:critical
```

Critical specs mutate demo data. Re-run `./e2e/scripts/prepare-backend.sh` (and restart backend if needed) between full critical suite runs.

On newer CI hosts you may set `PLAYWRIGHT_CHANNEL=chromium` after `npx playwright install chromium`.

## Smoke coverage (current)

| Spec | User | Assert |
|------|------|--------|
| `login-holder.spec.ts` | `holder1` | lands on `/marketplace` |
| `login-investor-marketplace.spec.ts` | `investor1` | marketplace + at least one listing |
| `login-moderator.spec.ts` | `moderator1` | lands on `/moderation` |
| `matches-holder.spec.ts` | `holder1` | `/matches` + at least one `match-card` |
| `matches-investor.spec.ts` | `investor1` | `/matches` sent tab + at least one `match-card` |
| `moderation-queue.spec.ts` | `moderator1` | `/moderation` without pagination/filter errors |
| `listings-my-holder.spec.ts` | `holder1` | `/listings/my` table without crash |
| `login-failed.spec.ts` | `holder1` + bad password | stays on `/login` + error message |
| `landing-guest.spec.ts` | guest (Live API) | flag off → no landing; flag on → `/` → `/landing`, key sections, listing card → `/login` |

Requires `show_landing_page` seed (develop / PR #31). Spec toggles the flag via admin API and restores `is_enabled=false` in `afterAll`. **UI must run with `VITE_USE_MOCK=false`** (mock simulator always enables the landing flag). Run only this file:

```bash
npx playwright test tests/smoke/landing-guest.spec.ts
```

## Critical-path coverage

| Spec | User | Assert |
|------|------|--------|
| `express-interest.spec.ts` | `investor1` | marketplace pagination active; express interest on serial `2000…0022` → sent match card |
| `accept-match.spec.ts` | `holder1` | accept seeded pending match on `2000…0001` → accepted |
| `decline-match.spec.ts` | `holder1` | decline seeded pending match on `2000…0002` |
| `moderation-approve.spec.ts` | `moderator1` | approve pending via review page → holder sees published |
| `moderation-reject.spec.ts` | `moderator1` | reject pending serial `3000…0012` → status rejected |
| `create-listing.spec.ts` | `holder1` | UI submit preferred; API fallback if create form does not navigate |
| `notifications-mark-read.spec.ts` | `holder1` | pagination + mark one unread as read |
| `kyc-approve.spec.ts` | `moderator1` | approve pending KYC for `holderkyc1` (needs Live KYC review UI) |

Also smoke: `admin-surfaces.spec.ts` for `admin1` stats / feature-flags / audit.

Stable serials / counts: `e2e/support/constants.ts` (`SEED`) and `seed_demo`.

Selectors prefer `data-testid` when present; fallbacks use Persian labels/placeholders.

`e2e/support/auth.ts` still seeds a guest localStorage user without tokens before login so `/login` is reachable even if older UI builds re-seed mock auth.

## Demo users

Same as `seed_demo`: `holder1`, `investor1`, `moderator1`, `admin1`, `holderkyc1` (pending KYC) — password = `$DEMO_SEED_PASSWORD`.

## CI

GitHub Actions: [`.github/workflows/ci-e2e.yml`](../../.github/workflows/ci-e2e.yml) — seeds demo backend, starts UI from `alamalhoda/checkyar-googleai`, runs smoke + critical with Chromium.

This workflow is **not** a merge gate for PRs to `develop` (do not add it to required checks). It still may run on those PRs using the pin in `e2e/ui-pin` so you see a non-blocking status.

The default UI checkout is **pinned to a full commit SHA** in [`e2e/ui-pin`](../../e2e/ui-pin), not a floating branch tip and not inside the workflow YAML. GitHub’s `GITHUB_TOKEN` cannot push edits to `.github/workflows/*.yml`; the sidecar file keeps the pin bump on GitFlow PRs.

To run E2E against a specific UI commit **without** changing the pin (manual):

```bash
gh workflow run "CI E2E Playwright" --repo alamalhoda/doion -f ui_sha=<full-or-short-sha>
```

`repository_dispatch` type `frontend-e2e` with JSON `{"ui_sha":"<sha>"}` does the same (used by the UI repo after push to `main`; PAT lives in that repo, not here). Missing `ui_sha` on that event fails the job; it does not fall back to the pin.

After that dispatched E2E **succeeds**, job `open pin PR` opens `feature/e2e-ui-pin-<sha>` → `develop` to set `e2e/ui-pin` to the resolved 40-character commit. It never pushes the pin to `develop` or `main`. PR/push E2E does not open a pin PR (those runs already use the file pin). If the pin already matches, or a PR for that branch exists, the job no-ops.

Manual bump (if you skip the bot PR):

```bash
cd /path/to/checkyar-googleai && git pull && git rev-parse HEAD
# then put that SHA in e2e/ui-pin on a feature branch and PR to develop
```

## Out of scope (follow-ups)

- Full KYC submit→approve UI path until Phase A Studio lands
- Visual regression
- Settlement / SMS real providers

## Related

- Demo / seed SSOT: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
- UI policy: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md)
- AI Studio smoke prep: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md)
- AI Studio critical-path prep: [`AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md`](./AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md)
