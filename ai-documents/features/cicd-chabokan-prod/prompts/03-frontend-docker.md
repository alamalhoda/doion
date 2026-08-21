# پرامپت ۰۳ — Dockerfile ایمیج SPA زنده (بدون CD محصول)

خروجی Step 8 از [`implementation_plan.md`](../implementation_plan.md). مرجع رفتار: [`feature_spec.md`](../feature_spec.md) قوانین ۷، ۸، ۱۷، ۱۸، ۲۳ و سناریو ۱۱/۱۳ (فقط آرتیفکت ایمیج؛ deploy محصول گام ۱۲ است)؛ برش فرانت: [`cicd-frontend.md`](../cicd-frontend.md).

## قاعده اجرا

این متن **فقط در Google AI Studio** روی ریپوی فعال UI (`checkyar-googleai`) اجرا می‌شود. از Cursor یا کلون لوکال روی این ریپو commit/push نکنید.

فقط بلوک `text` پایین را در Studio بچسبانید.

## پوشش این پرامپت

- ایمیج Docker که SPA را با باندل **زنده** سرو می‌کند (`VITE_USE_MOCK=false` در زمان build).
- Compose لوکال **اختیاری** فقط برای امتحان همان ایمیج.
- توسعه روزانه بدون Docker (`bun run dev`) معتبر بماند.
- یک اثبات `docker build` در CI یا دستور مستند معادل.

خارج از این گام: شاخهٔ `product`، SemVer/رجیستری، deploy به `chequeyar-front`، تغییر `cd-demo.yml`.

## تصمیم‌های قفل‌شده

- Package manager: Bun (`bun.lock`). `package-lock.json` ساخته نشود.
- `.github/workflows/cd-demo.yml` و `dispatch-doion-e2e.yml` دست نخورده بمانند.
- چهار گام فعلی `ci.yml` (lint، test، build پیش‌فرض، build زنده) حذف یا جایگزین نشوند.
- URL پیش‌فرض باندل محصول در ایمیج: `https://chequeyar-back.chbkn.dev/api/v1`
- فایل موجود `nginx.conf` را نگه دارید مگر root با COPY ایمیج ناسازگار باشد؛ SPA history باید `try_files` به `index.html` داشته باشد.
- ایمیج را به رجیستری push نکنید و به چابکان deploy نکنید.

---

```text
Goal: add a production Docker image that serves this Vue SPA as a non-mock (live) static bundle behind nginx, plus an optional local compose file to run that image. Keep bun/vite-on-the-host as the valid daily path. Prove `docker build` in CI. Do not add a product branch, registry push, Chabokan deploy, SemVer, or any change to mock demo CD.

Before coding: if a root Dockerfile already multi-stage-builds with Bun, bakes VITE_USE_MOCK=false plus VITE_API_BASE_URL at build time, copies dist into nginx with SPA fallback, CI already runs docker build, and cd-demo.yml is untouched, stop and say so.

## Context

- This repo is the active Cheque Yar UI: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun lockfile only (`bun.lock`). Never create or commit `package-lock.json`. Never use npm as the package manager of record for app deps.
- Studio pushes to `main`. Daily PRs are not required.
- Compile-time mock gate: `String(import.meta.env.VITE_USE_MOCK) === 'true'` in `src/api/client.ts`. The product image MUST bake `VITE_USE_MOCK=false`. Vite env is compile-time; do not try to flip mock mode with a runtime nginx env var.
- Default live API for the image build-args: `https://chequeyar-back.chbkn.dev/api/v1`
- For optional local compose, the browser on the host talks to Django; therefore the baked `VITE_API_BASE_URL` for a laptop smoke should be `http://localhost:8000/api/v1` (reachable from the browser), not a Docker-internal hostname.
- Vue Router uses `createWebHistory`. nginx must fall back to index.html.
- File `nginx.conf` already exists and points `root` at `/usr/share/nginx/html/dist` with `try_files $uri $uri/ /index.html`. Prefer keeping that file and copying `dist/` to that root. Only edit nginx.conf if the image layout cannot match; keep SPA fallback.
- Backend is a separate Django monorepo (doion). Do NOT change Django, doion workflows, or Playwright.
- Hosted mock demo CD must keep working unchanged (`chequeyar-front-demo`).

## Current CI (do not drop or reorder)

`.github/workflows/ci.yml` today:

- name: CI
- on: push and pull_request to `main`
- job `lint-test-build`: checkout, setup Bun, `bun install --frozen-lockfile`, `bun run lint`, `bun run test`, `bun run build`, then live build with `VITE_USE_MOCK=false` and `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1`

Keep those four verification steps. Add Docker image build AFTER them (same job is fine). A Docker failure may fail this CI job; that is intended for this step. Do not replace the live `bun run build` step with Docker.

`.github/workflows/dispatch-doion-e2e.yml` and `.github/workflows/cd-demo.yml`: do not edit.

## Required changes

1. `Dockerfile` at repo root (multi-stage)
   - Stage `build`: official Bun image (pin a current `oven/bun:1` tag, Debian-based if native deps need it). `WORKDIR /app`. Copy `package.json` and `bun.lock` first, then `bun install --frozen-lockfile`. Copy the rest of the app. Build with:
     - `ARG`/`ENV` `VITE_USE_MOCK` default `"false"`
     - `ARG`/`ENV` `VITE_API_BASE_URL` default `https://chequeyar-back.chbkn.dev/api/v1`
     - `bun run build`
   - Stage `runtime`: `nginx:1.27-alpine` (or current 1.27 alpine). Copy `nginx.conf` to `/etc/nginx/conf.d/default.conf`. Copy `dist/` from the build stage to `/usr/share/nginx/html/dist` so the existing nginx root matches. Do not run Bun or Node in the runtime stage. `EXPOSE 80`. No secrets in the image. Do not COPY `.env`, `.env.local`, or `GEMINI_API_KEY`.
   - Do not use `uv run` or Python. Do not serve the SPA from Vite preview in production.

2. `.dockerignore`
   - Ignore `node_modules`, `dist`, `.git`, `.env`, `.env.*` (keep `.env.example` if you want). Ignore editor junk. Do not ignore `nginx.conf`, `package.json`, `bun.lock`, or `src/`.

3. Optional `docker-compose.yml` (or `compose.yaml`) at repo root
   - One service, e.g. `spa`, `profiles: [app]` OR a short comment that this file is optional smoke only — pick one approach and document it.
   - `build.context: .` with build-args `VITE_USE_MOCK=false` and `VITE_API_BASE_URL=http://localhost:8000/api/v1` so a laptop browser can hit host Django on port 8000.
   - Publish `3000:80` (host 3000 matches current `bun run dev` port).
   - Do not add Postgres, Redis, or Django. Do not require this compose for daily UI work.

4. `.github/workflows/ci.yml`
   - After the live Vite build step, add a step `Build SPA Docker image` that runs:
     `docker build --build-arg VITE_USE_MOCK=false --build-arg VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1 -t cheque-yar-spa:${{ github.sha }} .`
   - Do not docker login, do not push, do not deploy.
   - Do not add GitHub Environments, Dependabot, or SHA-pinned third-party Actions beyond what already exists.

5. Docs (this repo only, EN+FA, same commit as Docker files)
   - `docs/TESTING.md` and `docs/TESTING.fa.md`: CI now also builds the SPA image; daily path remains `bun install` / `bun run dev` without Docker. Document:
     `docker build --build-arg VITE_USE_MOCK=false --build-arg VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1 -t cheque-yar-spa:local .`
     Optional compose command you actually added. Keep Playwright-lives-in-doion. Keep cd-demo mock note.
   - `docs/ARCHITECTURE.md` and `docs/ARCHITECTURE.fa.md`: one short paragraph: product SPA image is nginx + live-baked Vite env; demo service is still mock via `cd-demo.yml`; Docker is not required for local Vite. No Django internals.
   - README.md: if it lists how to run locally, state that Docker is optional and `bun run dev` remains valid. Do not write a long new guide. Do not tell people to stop using Bun on the host.

## Do not

- Touch `cd-demo.yml`, `dispatch-doion-e2e.yml`, Chabokan tokens, or `chequeyar-front-demo`.
- Create branch `product`, GitHub Release, image registry push, or product CD (later prompts).
- Change Vue views, API client, mock gating, router, or the four existing bun CI commands.
- `package-lock.json`, npm as app package manager, new runtime app dependencies (nginx in Docker is fine).
- Unrelated refactors.
- Playwright in this repo.
- Hard-code any PAT, password, or API key. Do not put credential-like strings in YAML comments.
- Bake `VITE_USE_MOCK=true` into the product image default.
- Use `host.docker.internal` as the default `VITE_API_BASE_URL` for the image (browsers on the host would not use that hostname the way the container would).

## Acceptance

- `docker build` with the two live build-args succeeds on CI for this commit.
- Runtime stage is nginx serving the SPA; opening a deep Vue route would be served via try_files (do not need a live container in CI if the Dockerfile + nginx.conf clearly do this).
- `cd-demo.yml` and `dispatch-doion-e2e.yml` are byte-for-byte unchanged.
- Four bun CI steps still run before Docker.
- README/docs still describe `bun run dev` as valid without Docker.
- No secrets in git.

## After you finish

Commit: `ci: add live SPA Docker image and optional compose`

Reply with: commit SHA, files changed, whether cd-demo.yml and dispatch-doion-e2e.yml were untouched, the docker build command that CI runs, and the default baked VITE_* values.
```
