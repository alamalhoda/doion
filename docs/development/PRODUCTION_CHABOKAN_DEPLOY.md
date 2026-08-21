# Production deploy (Chabokan) — MVP v1

This is the **product** runtime path (server), not daily laptop development. Daily Postgres-in-Docker + host `runserver` is documented in [`LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](./LOCAL_DEV_AND_PRODUCT_RUNTIME.md).

API and SPA are **separate** services. Do not serve the Vue app from Django nginx.

Product API constraints: `config.settings.production`, **PostgreSQL only** (SQLite raises at startup), Gunicorn via [`backend/Dockerfile`](../../backend/Dockerfile). Secrets live in the Chabokan panel, not in git.

Current ship path for `chequeyar-back` is still Chabokan CLI from `backend/` source (local `chabok deploy`, or owner-triggered GitHub workflow **CD Backend** with an existing SemVer tag). GHCR images from **Release** are versioned artifacts; this service type still builds the tagged Django source on Chabokan, not a GHCR pull. How to tag: [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md).

## Live hostnames (custom domains)

Chabokan **service name** (CLI `-s`, panel) is not always the URL users type. Custom domains on the SPA services:

| PaaS service | Type | Public site | Panel |
|--------------|------|-------------|--------|
| `chequeyar-front` | **Static** | https://royasoft.dev | [hub …/Yq40OKq](https://hub.chabokan.net/fa/services/detail/Yq40OKq) |
| `chequeyar-front-demo` | **Static** | https://royasoftgroup.ir | [hub …/Gwj1p2q](https://hub.chabokan.net/fa/services/detail/Gwj1p2q) |
| `chequeyar-back` | Django (source CLI) | https://chequeyar-back.chbkn.dev (no custom domain recorded) | [hub …/yz06Brq](https://hub.chabokan.net/fa/services/detail/yz06Brq) |
| `chequeyar-db` | Postgres | not a website — PostgreSQL for `chequeyar-back` | [hub …/Rz36Kow](https://hub.chabokan.net/fa/services/detail/Rz36Kow) |

The previous Vue-type `chequeyar-front` was deleted and recreated as Static with the **same service name**. Do not use Vue PaaS nginx (`root /app/dist`) or panel `VITE_*` for this host. Uploaded `nginx.conf` uses `root /usr/share/nginx/html/dist` ([Chabokan Static nginx](https://docs.chabokan.net/cloud-hosting/static/nginx-config/)). Keep `nginx.conf` out of `.chabokignore` while both front services are Static.

SPA `VITE_*` is baked in at GitHub Actions build time. Chabokan Static does not run `npm run build` on the server.

The live SPA bundle is compiled with `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1`. Changing only the front domain does **not** change that API URL. If the product site is `https://royasoft.dev`, the API CORS list on `chequeyar-back` must include that origin (and `https://www.royasoft.dev` if you use www):

`CORS_ALLOWED_ORIGINS` example: `https://royasoft.dev,https://chequeyar-front.chbkn.dev`

Do not run `chabok deploy` against `chequeyar-db`.

## Architecture

```text
Browser → https://royasoft.dev          (chequeyar-front)
                │  VITE_API_BASE_URL
                ▼
         https://chequeyar-back.chbkn.dev/api/v1
                │
         chequeyar-db (Postgres) + Redis in panel
```

## D1 — API (`chequeyar-back`)

From [`backend/`](../../backend/) after an approved tag, either locally or via Actions **CD Backend** (`workflow_dispatch`, input `tag`):

```bash
cd backend
chabok login
chabok deploy
```

```bash
gh workflow run "CD Backend" --ref develop -f tag=v0.1.0-test.2
```

Pre-start (`chabok-pre-start.sh`): `migrate` + `collectstatic`.

### Panel env (required)

| Key | Notes |
|-----|--------|
| `DATABASE_URL` | Postgres (never SQLite for real prod) |
| `REDIS` / cache URL | Per `production.py` |
| `SECRET_KEY`, JWT, email | Secrets only in panel |
| `CORS_ALLOWED_ORIGINS` | Must include the **browser** origin of the live SPA, e.g. `https://royasoft.dev` (keep `https://chequeyar-front.chbkn.dev` if that host is still used) |
| `DJANGO_ADMIN_URL` | Non-default admin path |
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |

**Never** run `seed_demo --reset` on the production user database.

### HSTS

`SECURE_HSTS_SECONDS` in [`production.py`](../../backend/config/settings/production.py) should be raised after HTTPS is verified (start from short TTL, ramp to long).

## D2 — SPA (`chequeyar-front`, Static)

Owner path: merge `main` → `product`, then **CD Product (Chabokan live)** on branch `product` (`chabok deploy -s chequeyar-front`). GitHub Actions builds with `VITE_USE_MOCK=false` and `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1`. Confirm mock chrome is absent. Do not edit `cd-demo.yml` for product deploys.

`/landing` is gated by API flag `show_landing_page` (seed default **off**). Mock demo enables that flag in the simulator; live does not until an admin toggles it.

SPA login/JWT uses `users.User.role`, not only Identity → Profile. Django Users admin shows **Role**; saving User or Profile copies the role to the other row.

Manual equivalent (Cursor must not push UI):

```bash
cd /path/to/checkyar-googleai
git pull origin product
printf 'VITE_USE_MOCK=false\nVITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1\n' > .env.production.local
bun install
bun run build
# owner: chabok deploy -s chequeyar-front
```

## D3 — Acceptance checklist

- [ ] Register / login with a real user
- [ ] Holder: KYC (when UI Phase A landed) → create listing → docs upload
- [ ] Investor: express interest → holder accept/decline
- [ ] Moderator: listing approve/reject + KYC decision
- [ ] Admin: stats / feature-flags / audit
- [ ] No simulator header / mock switch on production build

## Related

- End-to-end teaching map (dev → test → deploy): [`DEVELOPMENT_TO_DEPLOY.md`](./DEVELOPMENT_TO_DEPLOY.md)
- Daily vs product runtimes: [`LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](./LOCAL_DEV_AND_PRODUCT_RUNTIME.md)
- Backend staging notes: [`backend/README.md`](../../backend/README.md)
- Demo vs prod DB: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
- Active UI policy: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md)
- Phase A Studio UI blockers: [`V1_PHASE_A_STUDIO_PROMPT.md`](./V1_PHASE_A_STUDIO_PROMPT.md)
- Human CD / `product` branch how-to: [`CHABOKAN_CD_AND_PRODUCT_BRANCH.md`](./CHABOKAN_CD_AND_PRODUCT_BRANCH.md)
