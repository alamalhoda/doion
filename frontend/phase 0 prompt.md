# Phase 0 — Frontend Platform Scaffold (doion)

> **مرجع معماری (انسان / تیم):** [`ARCHITECTURE.md`](./ARCHITECTURE.md) — این فایل مشخصات **اجرایی** فاز ۰ برای پیاده‌سازی است.

You are implementing **Phase 0 only**: a production-ready **platform scaffold** for the doion monorepo. Do NOT implement real business-domain CRUD beyond platform shells, auth, dashboard placeholders, and documented stubs.

The canonical frontend root is **`frontend/`** (not `frontend`). Cursor rules under `.cursor/rules/frontend/**` may still reference `frontend` in globs — treat **`frontend/`** as the source of truth for this task.

Follow `.cursor/rules/share/**` (especially `offline-no-cdn-policy.mdc`, `engineering-principles.mdc`, `code-quality-baseline.mdc`). Align with frontend rules where they do not conflict; prefer this document.

---

## Context

- **Monorepo:** Django + DRF backend in `backend/`
- **App type:** Form-driven business SPA (admin desktop-first, user mobile-friendly)
- **No SEO, no SSR**
- **Architecture:** **Feature-based from Phase 0.** All business functionality must live under `src/features/<feature-name>/`. Do **not** place feature-specific code in global folders (except platform infrastructure defined below).
- **Development model:** Phase 0 = platform + feature module shells; later work adds vertical slices inside `features/<name>/` in parallel with backend.

---

## Mandatory Technology Stack

| Area | Choice |
|------|--------|
| Core | Vue 3 (Composition API + `<script setup>` only), Vite (latest stable), TypeScript (strict; avoid `any`) |
| UI | Naive UI; theme via `src/plugins/naive-ui.ts` + CSS variables — **NO Tailwind**, **NO external CSS frameworks** |
| State & routing | Pinia, Vue Router 4 |
| HTTP | Axios |
| i18n | vue-i18n (fa + en, RTL) |
| Forms | VeeValidate 4 + Zod (`@vee-validate/zod`) |
| PWA | vite-plugin-pwa |
| Utilities | VueUse (only what Phase 0 uses) |
| Dates | **Day.js only** — see Date Strategy |

---

## Critical Policies

### No-CDN / offline-first (runtime)

- **No** Google Fonts, unpkg, jsdelivr, cdnjs, or external runtime scripts/stylesheets.
- Fonts: local only under `public/fonts/` (assume present or document placeholders).
- Font Awesome Pro: local only under `public/fontawesome-pro-7.1.0-web/` — wire paths only; **do not generate proprietary assets**.
- Images: `public/images/` or `src/assets/`.

### Environment variables

Define in `frontend/.env.example`; read app-level values **only** via `src/config/app.ts` (see App Config). Never commit real `.env`.

| Variable | Purpose |
|----------|---------|
| `VITE_API_BASE_URL` | API origin (or empty when using dev proxy) |
| `VITE_APP_NAME` | App title / PWA manifest name |
| `VITE_DEFAULT_LOCALE` | Default locale (`fa` or `en`) |

`src/api/client.ts` may use `appConfig.apiBaseUrl`. Do **not** scatter `import.meta.env.VITE_*` across the codebase.

### App config (mandatory)

Create **`src/config/app.ts`**:

```ts
export const appConfig = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
  appName: import.meta.env.VITE_APP_NAME,
  defaultLocale: import.meta.env.VITE_DEFAULT_LOCALE,
} as const
```

- i18n, document title, PWA manifest, and other app metadata must use `appConfig`.
- Document fallbacks for missing env values in README.

### Route constants (mandatory)

Create **`src/constants/routes.ts`**:

```ts
export const ROUTES = {
  LOGIN: '/login',
  ADMIN_DASHBOARD: '/admin',
  USER_DASHBOARD: '/app',
  NOT_FOUND: '/:pathMatch(.*)*',
} as const

export type AppRoute = (typeof ROUTES)[keyof typeof ROUTES]
```

**Rules:**

- **Do not hardcode route path strings** in components, views, stores, guards, or services.
- Import from `ROUTES` for navigation, redirects, and route registration.
- Feature `routes.ts` files must use `ROUTES` for shared paths.

---

## Feature-based architecture (mandatory from Phase 0)

```
src/features/
├── auth/           # Login, token, auth store, auth service, auth routes
├── dashboard/      # Admin + User dashboard placeholders (Phase 0)
├── users/          # Shell only — future user management (NO dashboard)
├── tasks/          # Placeholder only (.gitkeep)
└── ...
```

### Per-feature layout

```text
src/features/<feature-name>/
├── components/     # optional
├── composables/    # optional
├── services/       # feature API (framework-agnostic)
├── stores/         # feature Pinia stores (if needed)
├── types/
├── views/
├── routes.ts       # exported for global router
└── index.ts        # optional public API
```

### Phase 0 feature requirements

**`features/auth/`** — full implementation: login view (VeeValidate + Zod), `authService`, auth Pinia store, `routes.ts`.

**`features/dashboard/`** — dashboard placeholders only:

```text
src/features/dashboard/
├── views/
│   ├── AdminDashboardView.vue
│   └── UserDashboardView.vue
└── routes.ts
```

- `AdminDashboardView` → rendered inside global **`AdminLayout`** (desktop-first).
- `UserDashboardView` → rendered inside global **`UserLayout`** (mobile-friendly).
- **Do NOT** put dashboard views under `features/users/`.

**`features/users/`** — shell for **future user management** only (types, optional empty service stub). No dashboard, no CRUD in Phase 0.

**`features/tasks/`** — `.gitkeep` or minimal README note; no business logic.

### Global folders (platform only)

| Path | Allowed content |
|------|-----------------|
| `src/api/` | Axios client, interceptors, error normalization, shared API types |
| `src/config/` | `app.ts` — env access |
| `src/constants/` | `routes.ts`, `storage.ts`, app constants |
| `src/router/` | Aggregates feature routes; guards use permission helpers + `ROUTES` |
| `src/layouts/` | `AuthLayout`, `AdminLayout`, `UserLayout` |
| `src/plugins/` | `naive-ui.ts`, pinia, i18n setup |
| `src/styles/` | tokens, themes, rtl, global |
| `src/i18n/` | Core i18n + `locales/fa.json`, `en.json` |
| `src/components/ui/` | Naive UI wrappers (design system) |
| `src/components/common/` | LanguageSwitcher, PageHeader, EmptyState |
| `src/composables/` | **Platform-only** (e.g. `useLocaleDirection`, `usePagination`) |
| `src/utils/` | `permissions.ts`, `date.ts`, pure helpers |
| `src/types/` | Platform shared types only |
| `src/services/uploadService.ts` | Cross-cutting upload placeholder only |
| `src/views/NotFoundView.vue` | Optional global 404 with zero business logic |

**Forbidden:** feature-specific views, services, stores, or business components directly under global `views/`, `services/`, or `stores/` (except `uploadService.ts` and optional `NotFoundView.vue`).

### Atomic design (practical)

- Atoms/molecules → `components/ui/`
- Shared organisms → `components/common/`
- Templates → `layouts/`
- Feature pages → `features/<name>/views/`

---

## Theme architecture

```
src/styles/
├── tokens.css          # design tokens (CSS variables)
├── themes/
│   ├── light.css
│   └── dark.css
├── rtl.css
└── global.css          # imports tokens + active theme + base styles
```

- Toggle via `data-theme="light" | "dark"` on `<html>` or root container.
- Import order in `main.ts`: `tokens.css` → active theme → `rtl.css` → `global.css`.

### Naive UI theme override layer (single source of truth)

Create **`src/plugins/naive-ui.ts`**:

- Export setup used in `main.ts`.
- Configure `NConfigProvider` theme overrides aligned with CSS variables.
- Integrate locale + `dir` with i18n (no scattered Naive theme config in components).
- Document how UI components consume tokens vs Naive overrides.

---

## API layer (strict)

### `src/api/`

| File | Responsibility |
|------|----------------|
| `client.ts` | Axios instance; `baseURL` from `appConfig.apiBaseUrl`; dev proxy documented |
| `interceptors.ts` | Auth header; 401 handling (clear session via store adapter — no Vue imports in services) |
| `errors.ts` | `normalizeApiError()` — see Error contract |
| `types.ts` | `ApiError`, `NormalizedError`, pagination types |

### Services rules (framework-agnostic)

- Feature services: `src/features/<feature>/services/`
- Cross-cutting: `src/services/uploadService.ts` only in Phase 0
- Services **must NEVER** import: Vue components, Pinia stores, Vue Router, or any Vue runtime API
- Services may import: `src/api/*`, `src/types`, feature types, pure `utils`
- Views/composables/stores call services; services return data or throw normalized errors

### Error handling contract

Implement **`normalizeApiError(error: unknown): NormalizedError`** in `src/api/errors.ts`:

| Source | Code / behavior |
|--------|-----------------|
| DRF ValidationError | `VALIDATION_ERROR` + `fieldErrors` |
| PermissionDenied (403) | `FORBIDDEN` |
| AuthenticationFailed / 401 | `UNAUTHENTICATED` |
| Network / generic | `NETWORK_ERROR` or `UNKNOWN` |

```ts
interface NormalizedError {
  code: string
  message: string              // i18n key or safe fallback
  fieldErrors?: Record<string, string[]>
  status?: number
  raw?: unknown                // dev logging only
}
```

- Response interceptor normalizes before reject.
- Login must demonstrate validation + generic error via i18n + Naive feedback.

### Pagination

- `normalizeListResponse<T>()` for DRF `{ count, next, previous, results }`
- Design so a future `{ data, errors, meta }` wrapper changes only `src/api/`, not feature services

---

## Date strategy

- Configure Day.js once in **`src/utils/date.ts`** (locales/plugins for `fa` and `en`)
- Export: `formatDate`, `formatDateTime`, `parseDate`, etc.
- **Do not** use native `Date` formatting in components/views
- All features import date helpers from this module only

---

## Upload strategy (Phase 0 placeholder)

**`src/services/uploadService.ts`**:

- Framework-agnostic stub: `uploadFile(file: File): Promise<{ url: string }>`
- Use `normalizeApiError` on failure; `TODO` for real endpoint and multipart
- Document future integration with api client + auth header

---

## Permissions architecture

**`src/utils/permissions.ts`**:

```ts
function canAccessAdmin(user: User | null): boolean
function canAccessUser(user: User | null): boolean
```

**Temporary mapping** (until backend exposes `role` — document in README):

- `canAccessAdmin` → `user?.is_staff === true`
- `canAccessUser` → authenticated user for user area (define rule clearly, e.g. authenticated && !is_staff OR all authenticated for `/app` — pick one and document)

**Rules:**

- **`src/router/guards.ts`** uses `canAccessAdmin` / `canAccessUser` and `ROUTES` only
- **Never** check `is_staff` directly in views or components
- Auth store computed flags must delegate to the same helpers

---

## Backend integration (DRF Token — not JWT)

| Action | Endpoint |
|--------|----------|
| Obtain token | `POST /api/auth-token/` — body: `username`, `password` → `{ "token": "..." }` |
| Current user | `GET /api/users/me/` — header: `Authorization: Token <token>` |

- Store token in `sessionStorage` (document XSS tradeoff in README)
- Vite dev proxy: `/api` → Django; document CORS (`django-cors-headers`)

---

## Complete folder structure

```text
frontend/
├── public/
│   ├── fonts/
│   ├── fontawesome-pro-7.1.0-web/
│   └── images/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── interceptors.ts
│   │   ├── errors.ts
│   │   └── types.ts
│   ├── config/
│   │   └── app.ts
│   ├── constants/
│   │   ├── routes.ts
│   │   └── storage.ts
│   ├── services/
│   │   └── uploadService.ts
│   ├── features/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   │   ├── views/
│   │   │   │   ├── AdminDashboardView.vue
│   │   │   │   └── UserDashboardView.vue
│   │   │   └── routes.ts
│   │   ├── users/
│   │   └── tasks/
│   ├── router/
│   │   ├── index.ts
│   │   └── guards.ts
│   ├── layouts/
│   │   ├── AuthLayout.vue
│   │   ├── AdminLayout.vue
│   │   └── UserLayout.vue
│   ├── views/
│   │   └── NotFoundView.vue
│   ├── components/
│   │   ├── ui/
│   │   └── common/
│   ├── composables/
│   ├── plugins/
│   │   ├── naive-ui.ts
│   │   ├── pinia.ts
│   │   └── i18n.ts
│   ├── i18n/
│   │   └── locales/
│   │       ├── fa.json
│   │       └── en.json
│   ├── styles/
│   │   ├── tokens.css
│   │   ├── themes/
│   │   │   ├── light.css
│   │   │   └── dark.css
│   │   ├── rtl.css
│   │   └── global.css
│   ├── types/
│   ├── utils/
│   │   ├── date.ts
│   │   └── permissions.ts
│   ├── assets/
│   ├── App.vue
│   └── main.ts
├── .env.example
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── eslint.config.js
└── README.md
```

**Naming:** PascalCase for `.vue` components; camelCase for services, stores, composables.

---

## Phase 0 functional requirements

### i18n & RTL

- Locales: `fa`, `en`; default from `appConfig.defaultLocale`
- `useLocaleDirection` + Naive provider dir/locale via `plugins/naive-ui.ts`
- `LanguageSwitcher` in `components/common/`; persist locale via `constants/storage.ts`

### Auth (`features/auth/`)

- Login with VeeValidate + Zod
- Auth store: token, user, `isAuthenticated`; admin/user flags via permission helpers
- Interceptors: attach token; 401 → logout + redirect to `ROUTES.LOGIN`
- Guards: `requiresAuth`, `requiresAdmin` (`canAccessAdmin`), `requiresUser` (`canAccessUser`)

### Layouts & dashboards

- `AuthLayout` → login
- `AdminLayout` → `AdminDashboardView` at `ROUTES.ADMIN_DASHBOARD`
- `UserLayout` → `UserDashboardView` at `ROUTES.USER_DASHBOARD`
- `NotFoundView` for unknown routes

### UI building blocks

- `components/ui/`: at least AppButton + form field wrapper
- `components/common/`: LanguageSwitcher, optional PageHeader
- `usePagination` + table shell (server-side `page`, `page_size`, `ordering` ready)
- Light/dark toggle → `data-theme` + Naive overrides

### PWA

- `vite-plugin-pwa`: manifest + service worker
- Cache static shell only; **do not** cache API responses aggressively

### Dev quality

- ESLint (+ vue + typescript-eslint) + Prettier
- Vitest + `@vue/test-utils` with at least one smoke test (preferred)
- `npm run build` must succeed

---

## Frontend coding rules (mandatory)

**Vue**

- Composition API only; **`<script setup>` only**
- **Do not use Options API**

**TypeScript**

- Prefer typed composables
- Avoid `any` unless absolutely necessary (comment why)
- Prefer explicit `interface` over large inline object types

**Structure & logic**

- Keep components **under ~300 lines** when possible
- **No business logic in components** — composables / services / stores
- **Views orchestrate; services fetch; stores manage state**
- **Do not hardcode route strings** — use `src/constants/routes.ts`
- **Do not read `import.meta.env` outside `src/config/app.ts` and `src/api/client.ts`**

**Dates & permissions**

- No raw `Date` formatting in UI — use `src/utils/date.ts`
- No `is_staff` checks in views/components — use `src/utils/permissions.ts`

---

## Explicitly OUT OF SCOPE

- Real tasks/users business CRUD
- JWT (unless backend already provides it — it does not; use Token)
- E2E test suite
- Generating Font Awesome Pro or licensed font files
- Backend code changes (README integration notes only)
- Secrets in repository

---

## Deliverables

1. Complete `frontend/` Phase 0 scaffold per this document.
2. **`frontend/README.md`**: prerequisites, install/dev/build, env vars, feature conventions, auth flow, permissions mapping, error contract, date/upload placeholders, how to add Phase 1 feature slice.
3. **`frontend/.env.example`** with all `VITE_*` variables.
4. **Architecture decisions** (features vs platform, api/services, theme layer, permissions, errors, Day.js, `appConfig`, `ROUTES`).
5. **Dependency list** with one-line justification per major package.
6. **Phase 0 completion checklist** (pass/fail) + **Phase 1 TODOs** for first real feature.

---

## Git (if committing)

- Do not commit directly to `main` or `develop`.
- Branch: `feature/frontend-phase-0-scaffold` from `develop`
- Commit: `feat(frontend): scaffold phase 0 platform with feature modules`

---

## Quality bar

- Production-grade, readable, maintainable TypeScript
- User-visible errors via i18n + `NormalizedError`
- Minimal scope: working platform scaffold, not a bloated demo app
