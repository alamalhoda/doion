# Backend Demo, Seed & Data Modes

**As of:** 2026-08-02  
**Scope:** `doion` backend only. Frontend mock (`VITE_USE_MOCK`) is documented separately in the active UI repo and in [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md).

## Short answer

| Concept | Backend? | What it means |
|---------|----------|---------------|
| **Mock API / in-process simulator** | **No** | Unlike the UI, Django does **not** fake REST responses behind a flag. Endpoints hit the real ORM and business services. |
| **Demo / seed data** | **Yes** | `manage.py seed_demo` fills a real database with holders, investors, listings, and a sample match (via domain factories). |
| **Stubs for external systems** | **Yes (limited)** | Some integrations are intentionally stubbed (e.g. SMS send, pricing suggestion formula) but still run through real Django code paths. |
| **Separate `db.demo.sqlite3`** | **Optional / not implemented yet** | Idea: isolate demo data from day-to-day `db.sqlite3`. Deferred until we need a disposable demo DB without touching local dev data. |

---

## Database files (local)

| File | Settings | Purpose |
|------|----------|---------|
| `backend/db.sqlite3` | `config.settings.local` | Default **local development** database. |
| `backend/test_db.sqlite3` | `config.settings.test` | Pytest / Django test runner DB (gitignored). Ephemeral for automated tests. |
| `backend/db.demo.sqlite3` | *not wired yet* | **Proposed** optional demo-only SQLite so `seed_demo --reset` never wipes your personal local DB. See [Optional demo DB](#optional-demo-db-dbdemosqlite3). |

Production / Chabokan uses PostgreSQL via `DATABASE_URL` (`config.settings.production`), not these SQLite files.

---

## Recommended local demo flow (backend + real UI)

This is the supported way to “simulate” product scenarios on the server side:

```bash
cd backend
source .venv/bin/activate   # or: uv run …

# 1) migrate the local DB (db.sqlite3 under local settings)
python manage.py migrate

# 2) seed deterministic demo users + listings + one match
python manage.py seed_demo --password "$DEMO_SEED_PASSWORD"
# first-time or clean slate:
# python manage.py seed_demo --reset --password "$DEMO_SEED_PASSWORD"

# 3) run API
python manage.py runserver
```

Then point the active UI at the real API:

```env
VITE_USE_MOCK=false
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

Demo users created by `seed_demo` (same password for all, printed if you omit `--password`):

| Username | Role |
|----------|------|
| `holder1` | check_holder |
| `investor1` | investor |
| `moderator1` | moderator |
| `admin1` | admin |

Also seeded: issuer profile, listings in `pending_moderation` / `published` / `rejected`, and one pending match.

Command details and flags: [`backend/README.md`](../../backend/README.md) (section Seed دمو).

---

## Backend has no `VITE_USE_MOCK` equivalent

### Frontend mock (UI repo)

- Flag: `VITE_USE_MOCK`
- Behavior: axios client may route to an **in-browser simulator** (`useBackendSimulatorStore`) without calling Django.
- Use: AI Studio / offline UI demos.
- **Not** a substitute for API contract or backend tests.

### Backend “simulation”

Use one of these instead of inventing a mock server mode:

1. **Seeded real DB** (`seed_demo`) — preferred for manual QA and future E2E against `/api/v1/`.
2. **Factories in tests** (`doion/<app>/factories.py`) — SSOT for pytest; same factories feed `seed_demo`.
3. **Integration stubs** — e.g. SMS logging stub, pricing `calculate_suggested_rate` stub: real endpoints, fake external provider.

Do **not** add a Django setting that returns canned JSON for all APIs. That would diverge from `MASTER_API_CONTRACT.md` and hide regressions.

---

## Optional demo DB (`db.demo.sqlite3`)

### Why it was proposed

- `seed_demo --reset` deletes demo usernames and related rows in the **current** database.
- If developers also keep personal scratch data in `db.sqlite3`, a reset can be surprising.
- A dedicated `db.demo.sqlite3` would let you wipe/reseed demo without touching the main local file.

### Current status

- **Not implemented.** Local settings always use `db.sqlite3`.
- `seed_demo` is **idempotent** by username / cheque serial when run without `--reset`; use `--reset` only when you intend to recreate demo users.
- Tracked as optional in [`backend/TODO.md`](../../backend/TODO.md).

### If we implement it later (sketch)

1. Add `config.settings.demo` (or env `DJANGO_DEMO_DATABASE=1`) pointing `NAME` to `BASE_DIR / "db.demo.sqlite3"`.
2. Document:

```bash
DJANGO_SETTINGS_MODULE=config.settings.demo python manage.py migrate
DJANGO_SETTINGS_MODULE=config.settings.demo python manage.py seed_demo --reset --password "$DEMO_SEED_PASSWORD"
DJANGO_SETTINGS_MODULE=config.settings.demo python manage.py runserver
```

3. Gitignore `db.demo.sqlite3` (like other local SQLite files).
4. Keep production on Postgres only.

Until then: use `db.sqlite3` + `seed_demo`, or a separate Postgres schema/DB for heavier isolation.

---

## Related docs

- API contract SSOT: [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md)
- Active UI + when to disable mock: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md)
- Backend commands / factories: [`backend/README.md`](../../backend/README.md)
