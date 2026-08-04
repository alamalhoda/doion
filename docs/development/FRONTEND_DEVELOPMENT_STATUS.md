# Frontend Development Status

**As of:** 2026-07-31

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
| Dev server | `bun run dev` (port `3000`) |
| Lint / build | `bun run lint` / `bun run build` |

On macOS, ensure Bun is on `PATH` for login shells (Cursor terminals often load `~/.zprofile`):

```bash
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

## Integration testing (local)

1. Run `doion` backend (typically `http://localhost:8000`).
2. Prefer seeded demo data for realistic roles/listings: `python manage.py seed_demo` (see [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)). Backend has **no** in-process API mock flag comparable to `VITE_USE_MOCK`.
3. Pull latest `checkyar-googleai`, then `bun install` and `bun run dev` (typically `http://localhost:3000`) with `VITE_USE_MOCK=false`.
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

## Related docs

- Legacy UI: [`../../frontend-legacy/README.md`](../../frontend-legacy/README.md)
- Active UI repo README: https://github.com/alamalhoda/checkyar-googleai
- API SSOT: [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md)
- Backend demo / seed / (no) mock: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
- E2E local runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)
- AI Studio UI docs bootstrap prompt: [`AI_STUDIO_DOCS_BOOTSTRAP_PROMPT.md`](./AI_STUDIO_DOCS_BOOTSTRAP_PROMPT.md)
- AI Studio E2E prep prompt: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md)
- AI Studio E2E critical-path prompt: [`AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md`](./AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md)
