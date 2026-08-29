# پرامپت ۰۵ — CD محصول از `product` به `chequeyar-front`

خروجی Step 12 از [`implementation_plan.md`](../implementation_plan.md). مرجع رفتار: [`feature_spec.md`](../feature_spec.md) قوانین ۹–۱۵، ۱۸، ۲۳ و سناریو ۹/۱۱/۱۲/۱۴؛ برش فرانت: [`cicd-frontend.md`](../cicd-frontend.md).

## قاعده اجرا

این متن **فقط در Google AI Studio** روی ریپوی فعال UI (`checkyar-googleai`) اجرا می‌شود. از Cursor یا کلون لوکال روی این ریپو commit/push نکنید.

فقط بلوک `text` پایین را در Studio بچسبانید.

## کار مالک بعد از پوش Studio (Verify)

1. workflow جدید را در Actions ببینید؛ روی push به `main` اجرا نشود.
2. `cd-demo.yml` و سرویس `chequeyar-front-demo` مثل قبل روی push به `main` کار کنند.
3. **تا خودتان تأیید نکنید** `Run workflow` نزنید — آن دکمه سرویس زندهٔ `chequeyar-front` را عوض می‌کند.
4. بعد از merge شدن PR `main` → `product` و سبز بودن CI، از Actions → همان workflow → Run workflow روی شاخهٔ `product`.

## پوشش این پرامپت

- Deploy تأییدشدهٔ SPA زنده (غیرmock) به `chequeyar-front`.
- فقط `workflow_dispatch` (بدون deploy خودکار روی push).
- استقرار از شاخهٔ `product`؛ از `main` خام deploy نشود.

خارج از این گام: تغییر `cd-demo.yml`، SemVer روی این ریپو، push ایمیج به GHCR، تغییر منطق Vue.

## تصمیم‌های قفل‌شده

- Package manager: Bun (`bun.lock`). `package-lock.json` ساخته نشود.
- `.github/workflows/cd-demo.yml` و `dispatch-doion-e2e.yml` و `ci.yml` دست نخورده بمانند.
- `chabok.json` همان سرویس دمو بماند (`chequeyar-front-demo`) تا deploy دمو نشکند؛ محصول با `-s chequeyar-front` مشخص شود.
- باندل محصول: `VITE_USE_MOCK=false` و `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1`.
- راز همان `CHABOKAN_TOKEN` موجود؛ مقدار را در git نگذارید.
- GitHub Environments، Dependabot، و پین SHA اکشن‌های سوم‌شخص لازم نیستند.
- سرویس چابکان فعلی استاتیک است (مثل دمو): `dist/` آپلود می‌شود. ایمیج GHCR `chequeyar-front` در ریپوی doion آرتیفکت نسخه است؛ این گام آن را به پنل چابکان pull نمی‌کند مگر سرویس از قبل Docker-image باشد (نیست).

---

```text
Goal: add an owner-triggered GitHub Actions workflow that deploys a live (non-mock) SPA build to the existing Chabokan service chequeyar-front. Trigger is workflow_dispatch only. Default git ref for a real ship is branch product, not main. Do not change mock demo CD, do not deploy on every push, do not tag this repo.

Before coding: if a workflow already exists that is workflow_dispatch-only, builds with VITE_USE_MOCK=false and VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1, and runs `chabok deploy -s chequeyar-front`, and cd-demo.yml is untouched, stop and say so.

## Context

- This repo is the active Cheque Yar UI: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun lockfile only (`bun.lock`). Never create or commit `package-lock.json`.
- Studio pushes to `main`. Production git line is `product`. Product SPA service is `chequeyar-front`. Mock demo is `chequeyar-front-demo` via `cd-demo.yml` (push to main, VITE_USE_MOCK=true). Leave that demo path unchanged.
- Compile-time mock gate: `String(import.meta.env.VITE_USE_MOCK) === 'true'` in `src/api/client.ts`. Product deploy MUST bake VITE_USE_MOCK=false.
- Live API URL: `https://chequeyar-back.chbkn.dev/api/v1`
- Existing demo CD (pattern to copy, not to edit): checkout, Bun, lint, test, mock build, setup-node 24, `npm install -g @chabokan.net/cli`, strip `dist/` from `.gitignore` on the runner, `chabok login -t "$CHABOKAN_TOKEN"`, `chabok deploy -s chequeyar-front-demo`.
- `chabok.json` currently names `chequeyar-front-demo`. Do not change that file. Product deploy must pass `-s chequeyar-front`.
- Doion holds SemVer tags and GHCR images. This UI repo does not git-tag. Do not add a Release workflow here.
- Backend/Django/doion workflows: do not change.

## Current CI (do not drop)

`.github/workflows/ci.yml` already runs on push/PR to `main` and `product`: bun install frozen, lint, test, default build, live build, docker build. Leave `ci.yml` unchanged.

## Required changes

1. Add `.github/workflows/cd-product.yml` (name it clearly, e.g. `CD Product`).
   - `on: workflow_dispatch` only. No `push`. No `pull_request`.
   - Job on ubuntu-latest:
     - checkout (the ref the owner selected in Run workflow; they should pick `product`)
     - setup Bun, `bun install --frozen-lockfile`
     - `bun run lint`
     - `bun run test`
     - Build live bundle: env `VITE_USE_MOCK: "false"` and `VITE_API_BASE_URL: "https://chequeyar-back.chbkn.dev/api/v1"`, then `bun run build`
     - setup-node 24
     - Deploy with `CHABOKAN_TOKEN: ${{ secrets.CHABOKAN_TOKEN }}`:
       - fail if the secret is empty
       - `npm install -g @chabokan.net/cli`
       - same `.gitignore` `dist/` strip as demo CD (otherwise the CLI skips the build)
       - `chabok login -t "$CHABOKAN_TOKEN"`
       - `chabok deploy -s chequeyar-front`
   - Do not deploy `chequeyar-front-demo` from this workflow.
   - Do not add GitHub Environments.

2. Files you must not edit: `.github/workflows/cd-demo.yml`, `.github/workflows/dispatch-doion-e2e.yml`, `.github/workflows/ci.yml`, `chabok.json`.

3. Docs (this repo only, EN+FA, commit with the workflow)
   - `docs/TESTING.md` / `docs/TESTING.fa.md`: product SPA CD is a separate workflow, manual, from `product`, live env, service `chequeyar-front`. Mock demo CD unchanged.
   - `docs/ARCHITECTURE.md` / `docs/ARCHITECTURE.fa.md`: one short sentence that `chequeyar-front` is updated only by owner-triggered CD from `product`, not from raw `main`.
   - README.md: only if it already describes CD; then mention the new workflow. Keep it short.

## Recovery

If this job fails, the Check is red. Restore by running the same workflow again on the last known-good `product` SHA (or a previous successful run’s ref). No automatic Chabokan rollback.

## Do not

- Touch `cd-demo.yml` or `chequeyar-front-demo`.
- Auto-deploy on push to `main` or `product`.
- `git tag` / GitHub Release in this repo.
- Change Vue, mock gating, or API client just to add CD.
- `package-lock.json`, npm as app package manager, new app dependencies.
- Playwright in this repo.
- Commit secrets.

## Done when

- New workflow file exists and is dispatch-only.
- Demo CD file is byte-for-byte unchanged (or you report any accidental diff).
- Docs EN+FA mention owner-triggered product CD vs mock demo CD.
- You pushed to `main` from Studio. Paste the commit SHA. Do not merge to `product` or run the new workflow unless the owner asked in chat.

## After you push

Reply with: commit SHA, workflow filename, confirmation that cd-demo.yml was not modified, and that you did not click Run workflow.
```
