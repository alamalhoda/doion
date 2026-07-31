# Frontend Legacy — doion (ARCHIVED)

> **Status: archived / documentation only / not maintained**  
> Archived on **2026-07-31**. This tree is kept for historical reference and docs (architecture notes, phase-0 prompts, prior scaffold). Do **not** treat it as the product UI.

## Active frontend (current)

| Item | Value |
|------|--------|
| Active UI repository | [alamalhoda/checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai) |
| Authored in | [Google AI Studio](https://aistudio.google.com/) |
| Sync model | **One-way:** AI Studio → GitHub → local (`git pull` only). Do not push UI edits from local to that repo while Studio is the source of truth. |
| Backend / API SSOT | This monorepo: `backend/` + [`docs/development/MASTER_API_CONTRACT.md`](../docs/development/MASTER_API_CONTRACT.md) |
| Full policy | [`docs/development/FRONTEND_DEVELOPMENT_STATUS.md`](../docs/development/FRONTEND_DEVELOPMENT_STATUS.md) |

## What this folder is

Former SPA scaffold for doion (Vue 3 + Vite + TypeScript + Naive UI), previously at `frontend/`. Renamed to `frontend-legacy/` so the path `frontend/` can later hold the adopted active UI after leaving AI Studio.

## Legacy docs (reference)

| Document | Description |
|----------|-------------|
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | Upstream architecture notes for this archived tree |
| **[phase 0 prompt.md](./phase%200%20prompt.md)** | Phase-0 scaffold specification |

## Run (reference only)

Not recommended for product work. If you must inspect the old app:

```bash
cd frontend-legacy
cp .env.example .env
npm install
npm run dev
```

## Structure (historical)

```
src/
├── api/              # Axios client, interceptors, error normalization
├── config/           # appConfig
├── constants/        # routes, storage
├── services/         # uploadService
├── features/         # auth, dashboard, users, tasks
├── router/           # Vue Router + guards
├── layouts/          # AuthLayout, AdminLayout, UserLayout
├── components/       # UI components + common
├── composables/      # useLocaleDirection, usePagination
├── plugins/          # Pinia, i18n, Naive UI setup
├── i18n/             # Translations
├── styles/           # CSS variables, themes, RTL
├── utils/            # date.ts, permissions.ts
└── main.ts           # Entry point
```

## Features at archive time (Phase 0)

- Auth — Login, store, guards, interceptors  
- Dashboard — Admin (desktop) + User (mobile)  
- Platform — i18n (fa/en), themes, form validation, API layer  
- Users / Tasks — shells only  

## Cursor rules

- `.cursor/rules/frontend/` — frontend engineering rules (globs may still say `frontend/**`; this archive path is `frontend-legacy/`)
- `.cursor/rules/share/offline-no-cdn-policy.mdc` — no CDN at runtime

## Backend

- Prefer current contract: [`docs/development/MASTER_API_CONTRACT.md`](../docs/development/MASTER_API_CONTRACT.md)
- Backend guide: [`../backend/README.md`](../backend/README.md)
