# Frontend Development Status

**As of:** 2026-08-06

This document is the SSOT for *where* active UI work happens and how it relates to this monorepo.

## Roles

| Component | Location | Role |
|-----------|----------|------|
| **Backend + API contract** | This repo (`doion`) — `backend/`, `docs/development/MASTER_API_CONTRACT.md` | Source of truth for API; developed with GitFlow (`feature/*` → PR → `develop`) |
| **Active frontend** | External: [alamalhoda/checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai) | Product UI under active development |
| **Legacy frontend** | `frontend-legacy/` in this repo | Archived; documentation and historical reference only — **not maintained** |
| **Cursor frontend rules** | `.cursor/rules/frontend/` | Still apply to future `frontend/` code and to edits under `frontend-legacy/` when touched |

## One-way sync rule (mandatory while AI Studio is the UI source)

Active UI is authored in [Google AI Studio](https://aistudio.google.com/), which can **push** to GitHub but does **not** pull remote changes.

```text
[Google AI Studio]  --push-->  github.com/alamalhoda/checkyar-googleai
                                        |
                                        v  (git pull only)
                                 local machine / integration with doion backend
```

### Do

- Develop UI **only** in AI Studio until a stable release is accepted.
- On a local clone of `checkyar-googleai`: `git pull` to receive Studio pushes; use local `.env` to point at `doion` backend (`VITE_USE_MOCK=false`, `VITE_API_BASE_URL=http://localhost:8000/api/v1`).
- Install and run the active UI with **Bun** (see [Package manager](#package-manager-active-ui)).
- Keep API contract changes in `doion` (`MASTER_API_CONTRACT.md` + backend) via normal GitFlow.
- Mirror contract changes into the UI **inside AI Studio** (do not rely on local commits to the UI repo).

### Do not

- Commit or push UI source changes from local/Cursor to `checkyar-googleai` (AI Studio will not see them → divergence).
- Use `npm install` / commit `package-lock.json` for the active UI (creates drift vs AI Studio’s `bun.lock`).
- Treat `frontend-legacy/` as the active app or wire CI/deploy to it.
- Copy the active UI into this monorepo until leaving AI Studio (planned exit: adopt into `frontend/` via a feature PR, then archive the external repo).

## Package manager (active UI)

| Item | Value |
|------|--------|
| Package manager | **Bun** (SSOT; matches Google AI Studio) |
| Lockfile in git | `bun.lock` |
| Ignored | `package-lock.json` (must stay out of git) |
| Install | `bun install` |
| Dev server | Prefer `bun run dev -- --host 127.0.0.1 --port 3000` (see [Local Vite host](#local-vite-host-recommended)) |
| Lint / build | `bun run lint` / `bun run build` |

On macOS, ensure Bun is on `PATH` for login shells (Cursor terminals often load `~/.zprofile`):

```bash
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

### Local Vite host (recommended)

Default `bun run dev` in this UI often binds Vite to `0.0.0.0` (all interfaces). On machines with a VPN / TUN client (e.g. v2box, Clash — interfaces like `utun*` / `198.18.0.1`), that binding commonly breaks browser access: Vite prints “ready”, but `http://localhost:3000/` fails with `ERR_CONNECTION_TIMED_OUT` while TCP stays in `SYN_SENT` / `SYN_RCVD`.

**Use this local command instead:**

```bash
cd /path/to/checkyar-googleai
bun run dev -- --host 127.0.0.1 --port 3000
```

Then open **`http://127.0.0.1:3000/`** (or `http://localhost:3000/` once loopback works).

| Part | Meaning |
|------|---------|
| `bun run dev` | Runs the `dev` script from `package.json` (Vite). |
| `--` | Ends Bun/npm args; everything after is passed to Vite. |
| `--host 127.0.0.1` | Bind only to loopback so VPN TUN does not hijack the listener. |
| `--port 3000` | Keep the usual UI port (matches E2E / CORS expectations). |

Do **not** commit this host change into `checkyar-googleai` from local/Cursor (one-way AI Studio rule). Keep it as a local run flag.

If it still times out with VPN on: bypass `localhost` / `127.0.0.1` in the VPN app, or temporarily disable TUN / Enhanced Mode.

## Integration testing (local)

1. Run `doion` backend (typically `http://localhost:8000`).
2. Prefer seeded demo data for realistic roles/listings: `python manage.py seed_demo` (see [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)). Backend has **no** in-process API mock flag comparable to `VITE_USE_MOCK`.
3. Pull latest `checkyar-googleai`, then `bun install` and `bun run dev -- --host 127.0.0.1 --port 3000` (open `http://127.0.0.1:3000`) with `VITE_USE_MOCK=false`.
4. Fix API/backend issues in `doion`; fix UI issues only via AI Studio → GitHub → local pull.

### E2E smoke (Playwright harness in doion)

Browser smoke tests live in this monorepo under `e2e/` (not in `checkyar-googleai`). They hit the Live UI against a seeded demo backend.

- Runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)
- AI Studio selector/username prep (paste into Studio only): [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md)

## Exit criteria (later)

When the active UI is acceptable:

1. Final `git pull` on `checkyar-googleai`.
2. Feature branch on `doion`: place code in `frontend/`, keep `frontend-legacy/` as archive.
3. PR → `develop`; then archive the `checkyar-googleai` GitHub repository.
4. From then on, UI GitFlow is two-way inside this monorepo only.

## MVP v1 execution status (2026-08-06)

| Track | Status |
|-------|--------|
| Backend gates (KYC, issuer ownership, register throttle, ordering) | Landed on `feature/v1-backend-mvp-gates` (PR #23) |
| UI Live blockers (KYC submit/review, moderation details, doc upload bytes) | Landed in UI `70c80e74` — follow-up tsc: [`V1_PHASE_A_FOLLOWUP_TSC_PROMPT.md`](./V1_PHASE_A_FOLLOWUP_TSC_PROMPT.md) |
| E2E expansion + CI Playwright | Specs + `.github/workflows/ci-e2e.yml` |
| Chabokan production | Runbook: [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md) |
| Codespaces | `.devcontainer/` in doion (dev only; not production host) |

UI remains external + one-way until after MVP acceptance. Do **not** migrate into `doion/frontend` for v1.

## Related docs

- Legacy UI: [`../../frontend-legacy/README.md`](../../frontend-legacy/README.md)
- Active UI repo README: https://github.com/alamalhoda/checkyar-googleai
- API SSOT: [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md)
- Backend demo / seed / (no) mock: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
- E2E local runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)
- AI Studio UI docs bootstrap prompt: [`AI_STUDIO_DOCS_BOOTSTRAP_PROMPT.md`](./AI_STUDIO_DOCS_BOOTSTRAP_PROMPT.md)
- AI Studio CI (GitHub Actions) prompt: [`AI_STUDIO_CI_GITHUB_ACTIONS_PROMPT.md`](./AI_STUDIO_CI_GITHUB_ACTIONS_PROMPT.md)
- AI Studio E2E prep prompt: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md)
- AI Studio E2E critical-path prompt: [`AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md`](./AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md)
- V1 Phase A Studio prompt (KYC / upload / moderation Live): [`V1_PHASE_A_STUDIO_PROMPT.md`](./V1_PHASE_A_STUDIO_PROMPT.md)
- Production Chabokan: [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md)
