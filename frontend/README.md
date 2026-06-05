# Frontend — doion

واسط کاربری SPA پروژه doion (Vue 3 + Vite + TypeScript + Naive UI).

## مستندات

| سند | توضیح |
|-----|--------|
| **[ARCHITECTURE.md](./ARCHITECTURE.md)** | **مرجع معماری بالادستی** — لایه‌ها، feature modules، API، auth، تم، قراردادها |
| **[phase 0 prompt.md](./phase%200%20prompt.md)** | مشخصات اجرایی scaffold فاز ۰ (برای AI یا پیاده‌سازی اولیه) |

## نصب سریع

```bash
cd frontend
npm install
npm run dev
```

سپس `.env.example` را به `.env.local` کپی کنید و مقادیر را تنظیم کنید.

## ساختار پروژه

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

## Features Phase 0

✅ **Auth** — Login, store, guards, interceptors  
✅ **Dashboard** — Admin (desktop) + User (mobile)  
✅ **Platform** — i18n (fa/en), themes, form validation, API layer  
⏳ **Users** — Shell (Phase 1+)  
⏳ **Tasks** — Shell (Phase 1+)

## مطالعه بیشتر

- [ARCHITECTURE.md](./ARCHITECTURE.md) — معماری بالادستی
- [phase 0 prompt.md](./phase%200%20prompt.md) — نیازمندی‌های تفصیلی

## وضعیت

فاز ۰ (platform scaffold) طبق `phase 0 prompt.md` — در صورت نبود `package.json`، هنوز scaffold نشده است.

## شروع سریع (پس از scaffold)

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

متغیرهای محیط: `VITE_API_BASE_URL`, `VITE_APP_NAME`, `VITE_DEFAULT_LOCALE` — جزئیات در [ARCHITECTURE.md §14](./ARCHITECTURE.md#14-پیکربندی-محیط).

## قوانین توسعه

- `.cursor/rules/frontend/` — قوانین Cursor (برخی globها ممکن است هنوز `frontend` باشند؛ مسیر canonical: **`frontend/`**)
- `.cursor/rules/share/offline-no-cdn-policy.mdc` — بدون CDN در runtime

## Backend

- Token: `POST /api/auth-token/`
- کاربر جاری: `GET /api/users/me/`
- راهنمای backend: [`../backend/README.md`](../backend/README.md)
