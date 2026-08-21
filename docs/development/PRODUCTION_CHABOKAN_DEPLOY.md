# Production deploy (Chabokan) — MVP v1

This is the **product** runtime path (server), not daily laptop development. Daily Postgres-in-Docker + host `runserver` is documented in [`LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](./LOCAL_DEV_AND_PRODUCT_RUNTIME.md).

API and SPA are **separate** services. Do not serve the Vue app from Django nginx.

Product API constraints: `config.settings.production`, **PostgreSQL only** (SQLite raises at startup), Gunicorn via [`backend/Dockerfile`](../../backend/Dockerfile). Secrets live in the Chabokan panel, not in git.

Current ship path for `chequeyar-back` is still `chabok deploy` from `backend/` (source). A GitHub **Release** workflow can push tagged images to GHCR (`ghcr.io/alamalhoda/doion-api` and `ghcr.io/alamalhoda/chequeyar-front`); that does not change the live Chabokan services. Owner-approved CD is a later step. How to tag (education): [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md).

## Architecture

```text
Browser → https://chequeyar-front… (static SPA)
                │  VITE_API_BASE_URL
                ▼
         https://chequeyar-back…/api/v1  (Django + Gunicorn)
                │
         Postgres + Redis (panel)
```

## D1 — API (`chequeyar-back`)

From [`backend/`](../../backend/) after release to `main` (or approved production branch):

```bash
cd backend
chabok login
chabok deploy
```

Pre-start (`chabok-pre-start.sh`): `migrate` + `collectstatic`.

### Panel env (required)

| Key | Notes |
|-----|--------|
| `DATABASE_URL` | Postgres (never SQLite for real prod) |
| `REDIS` / cache URL | Per `production.py` |
| `SECRET_KEY`, JWT, email | Secrets only in panel |
| `CORS_ALLOWED_ORIGINS` | Must include SPA origin, e.g. `https://chequeyar-front.chbkn.dev` |
| `DJANGO_ADMIN_URL` | Non-default admin path |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |

**Never** run `seed_demo --reset` on the production user database.

### HSTS

`SECURE_HSTS_SECONDS` in [`production.py`](../../backend/config/settings/production.py) should be raised after HTTPS is verified (start from short TTL, ramp to long).

## D2 — SPA (`chequeyar-front`)

Build from [checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai) (pull AI Studio `main`):

```bash
cd /path/to/checkyar-googleai
git pull origin main
printf 'VITE_USE_MOCK=false\nVITE_API_BASE_URL=https://<api-host>/api/v1\n' > .env.production.local
bun install
bun run build
```

Deploy `dist/` to the static front service on Chabokan (separate from `chequeyar-back`). Confirm mock chrome is absent.

## D3 — Acceptance checklist

- [ ] Register / login with a real user
- [ ] Holder: KYC (when UI Phase A landed) → create listing → docs upload
- [ ] Investor: express interest → holder accept/decline
- [ ] Moderator: listing approve/reject + KYC decision
- [ ] Admin: stats / feature-flags / audit
- [ ] No simulator header / mock switch on production build

## Related

- Daily vs product runtimes: [`LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](./LOCAL_DEV_AND_PRODUCT_RUNTIME.md)
- Backend staging notes: [`backend/README.md`](../../backend/README.md)
- Demo vs prod DB: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
- Active UI policy: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md)
- Phase A Studio UI blockers: [`V1_PHASE_A_STUDIO_PROMPT.md`](./V1_PHASE_A_STUDIO_PROMPT.md)
