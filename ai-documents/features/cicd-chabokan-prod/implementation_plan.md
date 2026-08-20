# Implementation Plan — CI/CD محصول روی چابکان

## Architecture Summary

اتوماسیون در دو ریپو جدا می‌ماند و قرارداد REST محصول عوض نمی‌شود. در `doion` GitFlow برقرار است: PR به `develop` با pytest روی PostgreSQL سرویس GitHub Actions و Ruff به‌عنوان Check اجباری؛ مسیر لوکال SQLite بدون Docker حفظ می‌شود و Postgres داخل Compose فقط انتخاب همکار است. محصول و CI هرگز به SQLite برنمی‌گردند. فرانت فقط از AI Studio تغییر می‌کند: CI روی `main` شامل build زنده (`VITE_USE_MOCK=false`) است؛ شاخهٔ `product` مسیر تولید است؛ `cd-demo.yml` دست نمی‌خورد. E2E Playwright gate ادغام بک‌اند نیست؛ بعد از push به `main` فرانت با `ui_sha` در doion اجرا می‌شود و bump پین YAML فقط با PR به `develop` است نه push مستقیم. انتشار بعدی: ایمیج Docker هر دو سرویس، GitHub Release با SemVer، و deploy به چابکان فقط با تأیید مالک (`workflow_dispatch`). Staging ساخته نمی‌شود.

Scope: FULL-STACK (AUTOMATION؛ لایهٔ محصول UI/API بدون تغییر رفتار کسب‌وکار)

Chat 2 فقط یک گام از لیست زیر را در هر نوبت پیاده می‌کند و منتظر تأیید می‌ماند.

## Implementation Steps

### گام اول اجرایی (فقط CI تست PR) — طبق قانون ۲۵ spec

- [x] **Step 1 — cicd-backend: پاک‌سازی Ruff و CI اجباری pytest+Ruff روی Postgres**  
  ریپو: `doion`.  
  - بدهی `ruff check` روی `backend/` را طوری برطرف کن که CI بدون ignore سراسری جدید سبز شود؛ ignore نقطه‌ای فقط برای فایل تولیدشده (مثل migrations) اگر لازم باشد.  
  - `.github/workflows/ci-backend.yml`: سرویس PostgreSQL؛ `DATABASE_URL` به آن؛ pytest؛ job جدا یا همان job برای `uv run ruff check .`؛ هر دو باید برای سبز بودن Check موفق باشند. اگر Postgres بالا نیاید Check شکست می‌خورد (بدون fallback SQLite).  
  - مسیر لوکال پیش‌فرض (`config.settings.local` / SQLite) را خراب نکن.  
  - `backend/README.md`: Ruff در CI اجباری است؛ لوکال SQLite همچنان معتبر است.  
  - E2E را به `required` این PR تبدیل نکن.  
  **Verify:** `uv run ruff check .` و pytest لوکال روی SQLite؛ در Actions روی PR به `develop` هر دو job/گام سبز با Postgres.  
  **REVIEW NOTE:** (2026-08-19) `uv run ruff check .` پاک است؛ `uv run pytest` لوکال ۲۰۸ تست روی SQLite (`config.settings.test` بدون `GITHUB_ACTIONS`) پاس شد. مسیر `config.settings.local` دست نخورده. CI: job جدا `ruff` + `pytest` با سرویس Postgres 16 و `DATABASE_URL`؛ اگر `GITHUB_ACTIONS` باشد و engine پستگرس نباشد `RuntimeError`. E2E required نشده. تناقض spec: `test.py` قبلاً SQLite قفل بود — اصلاح شد. `DJ001` روی چند CharField nullable بدون migration (خط noqa). `line-length=119` (هم‌تراز djLint؛ ignore جدید سراسری اضافه نشد). رجیستری Docker مربوط به Step 10 است.

- [x] **Step 2 — cicd-frontend: پرامپت Studio برای CI تست PR (بدون CD)**  
  ریپو: `checkyar-googleai` فقط از Studio. Cursor push نمی‌کند.  
  - فایل پرامپت را در `ai-documents/features/cicd-chabokan-prod/prompts/01-ci-live-build.md` بنویس و کاربر در Studio پیست کند.  
  - CI موجود: typecheck، Vitest، `vite build`؛ افزودن build جدا با `VITE_USE_MOCK=false` و `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1`.  
  - `cd-demo.yml` و سرویس دمو را تغییر نده.  
  - شاخهٔ `product` و Docker و deploy در این گام نیست.  
  **Verify:** پس از SHA پوش Studio، CI روی `main` هر چهار گام را نشان می‌دهد؛ دمو mock مثل قبل deploy می‌شود.  
  **REVIEW NOTE:** (2026-08-19) SHA `20a999d` روی `main`. `ci.yml` چهار گام دارد؛ `cd-demo.yml` در diff نیست. Actions: [CI success](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32293613427) و [CD Demo success](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32293613525). Docs EN+FA به‌روز. Cursor به UI push نکرد.

### onboarding لوکال (اختیاری Postgres)

- [x] **Step 3 — cicd-backend: Compose اختیاری Postgres برای همکار**  
  ریپو: `doion`.  
  - Compose (یا معادل) فقط سرویس Postgres (+ در صورت نیاز حجم/پورت مستند)؛ اپ Django لوکال می‌تواند همچنان روی میزبان با `uv` اجرا شود.  
  - سند کوتاه: مسیر A = SQLite بدون Docker؛ مسیر B = `DATABASE_URL` به Postgres کانتینر. هیچ‌کدام را تنها مسیر نکن.  
  **Verify:** مسیر A بدون Docker کار می‌کند؛ مسیر B با کانتینر به Postgres وصل می‌شود.  
  **REVIEW NOTE:** (2026-08-19) Compose فقط Postgres 16 + trust. مسیر A: pytest ۲۰۸ پاس SQLite. مسیر B: `migrate` روی میزبان با `DATABASE_URL=postgres://doion@localhost:5432/doion` موفق شد. `127.0.0.1` روی Docker Desktop مک timeout داد؛ سند از `localhost` استفاده می‌کند. TUN/`utun` هم می‌تواند پورت Docker را خراب کند.

### همگام E2E غیرمسدودکننده

- [x] **Step 4 — cicd-backend: E2E با `ui_sha` بدون gate روی PR develop**  
  ریپو: `doion`.  
  - `workflow_dispatch` / `repository_dispatch` با ورودی commit فرانت؛ checkout همان SHA؛ E2E موجود.  
  - `pull_request` به `develop` این job را required نکند.  
  - پین داخل YAML را در همین گام به‌صورت خودکار روی `develop` push نکن.  
  **Verify:** اجرای دستی با یک SHA مشخص؛ PR بک‌اند بدون این Check هم قابل ادغام از نظر پیکربندی branch است (یا حداقل job fail آن required نیست).  
  **REVIEW NOTE:** (2026-08-20) `ci-e2e.yml`: ورودی `ui_sha` روی `workflow_dispatch`؛ `repository_dispatch` type‏ `frontend-e2e` با `client_payload.ui_sha` (بدون SHA شکست، نه fallback به پین). PR/push به `develop` همچنان پین `PINNED_UI_SHA` را چک‌اوت می‌کند. این workflow پین را push نمی‌کند. `develop` branch protection ندارد (rulesets خالی) پس E2E نمی‌تواند merge-block باشد. اجرای دستی: [run 32331636536](https://github.com/alamalhoda/doion/actions/runs/32331636536) روی `feature/cicd-chabokan-prod`، `workflow_dispatch`، `ui_sha=20a999d037cabe0a7223efa8cd09e69da2117597` (نه پین `d518d20`)، smoke+critical سبز در ۲ دقیقه. هشدار Actions: Node 20 deprecated روی checkout/setup-node — خارج از scope این گام.

- [x] **Step 5 — cicd-frontend: پرامپت Studio برای تریگر E2E بعد از push به main**  
  - پرامپت: `prompts/02-dispatch-doion-e2e.md`.  
  - بعد از CI سبز `main`، رویداد به doion با SHA همان commit.  
  - نیاز به راز/PAT در ریپوی فرانت اگر `repository_dispatch` لازم باشد؛ در پرامپت صریح بگو، مقدار راز را hard-code نکن.  
  **Verify:** یک push Studio → run E2E در doion روی همان SHA.  
  **REVIEW NOTE:** (2026-08-20) SHA Studio `5053b986dc9ee993de1f8224b82135f048164ff6`. `dispatch-doion-e2e.yml` جدا؛ `ci.yml`/`cd-demo.yml` در آن commit نیستند. CI چهار گام سبز. CD Demo سبز. PR [#36](https://github.com/alamalhoda/doion/pull/36) روی `develop`. PAT اول 401 بود؛ بعد از تعویض secret، همان run از نوع `workflow_run` دوباره اجرا شد و سبز شد: [32375579812](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32375579812) با HTTP 204 و `ui_sha=5053b98…`. E2E دویون از Actions: [32403989662](https://github.com/alamalhoda/doion/actions/runs/32403989662). قانون ۲۴ (bump پین) گام ۶ است.

- [ ] **Step 6 — cicd-backend: bump پین E2E فقط با PR به develop**  
  - یا سند دستی bump بعد از هر UI موفق، یا job که PR باز می‌کند (نه commit مستقیم به `develop`/`main`).  
  **Verify:** پین با GitFlow عوض می‌شود.  
  **REVIEW NOTE:** (2026-08-20) Job `bump-pin` بعد از E2E موفق فقط روی `repository_dispatch` یا `workflow_dispatch` با `ui_sha` غیرخالی، برنچ `feature/e2e-ui-pin-<12>` می‌سازد و PR به `develop` باز می‌کند؛ به `develop`/`main` push نمی‌کند. PR/push به develop پین را bump نمی‌کند. SHA کامل از `git rev-parse` بعد از checkout UI. Verify زنده: این YAML باید روی `develop` باشد (یا `workflow_dispatch` روی این feature branch) تا PR پین دیده شود.

### Docker تصاویر محصول (هنوز بدون deploy خودکار)

- [ ] **Step 7 — cicd-backend: Dockerfile بک‌اند**  
  - ایمیج قابل اجرای Gunicorn/تنظیمات production؛ SQLite پیش‌فرض محصول نباشد.  
  - `.dockerignore` مناسب.  
  - README: build لوکال ایمیج اختیاری است؛ توسعه SQLite سر جایش.  
  **Verify:** `docker build` بک‌اند موفق؛ کانتینر با `DATABASE_URL` پستگرس (Compose یا CI) migrate/run می‌شود.  
  **REVIEW NOTE:**

- [ ] **Step 8 — cicd-frontend: پرامپت Dockerfile فرانت**  
  - `prompts/03-frontend-docker.md`.  
  - ایمیج سرو SPA زنده (غیرmock در باندل محصول).  
  - Compose لوکال فرانت اختیاری؛ توسعه بدون Docker معتبر بماند.  
  **Verify:** پس از SHA Studio، `docker build` در CI یا دستور مستند موفق است.  
  **REVIEW NOTE:**

### مسیر تولید فرانت (`product`) و انتشار

- [ ] **Step 9 — cicd-frontend: پرامپت شاخه `product` و CI روی PR به آن**  
  - `prompts/04-product-branch.md`.  
  - `main` همچنان هدف پوش Studio؛ `product` تولید.  
  - همان تست‌های اجباری Step 2 روی PR به `product`.  
  - از `main` خام به `chequeyar-front` deploy نشود.  
  **Verify:** کاربر می‌تواند PR `main` → `product` باز کند و Checks سبز ببیند.  
  **REVIEW NOTE:**

- [ ] **Step 10 — cicd-backend: GitHub Release / SemVer و ایمیج تگ‌شده**  
  - تگ SemVer + Release برای commit بک‌اند؛ build/push ایمیج با همان تگ (رجیستری: چابکان یا GHCR — در REVIEW NOTE ثبت شود اگر رجیستری در پنل از قبل معلوم است).  
  - فقط با اقدام عمدی مالک (مثلاً `workflow_dispatch`)، نه روی هر merge به `develop`.  
  **Verify:** یک تگ آزمایشی Release + ایمیج با همان تگ (محیط محصول را در این گام عوض نکن مگر کاربر بخواهد).  
  **REVIEW NOTE:**

- [ ] **Step 11 — cicd-backend: CD تأییدشده به `chequeyar-back`**  
  - `workflow_dispatch` (تأیید مالک = اجرای دستی workflow).  
  - فقط اگر تست اجباری همان commit/تگ سبز بوده.  
  - Postgres در پنل چابکان؛ SQLite نه.  
  - `cd-demo` فرانت را لمس نکن.  
  - شکست job: Check قرمز؛ بازیابی = اجرای مجدد deploy آخرین تگ موفق (سند یک پاراگراف در README).  
  **Verify:** dry-run یا deploy واقعی فقط با تأیید صریح کاربر در Chat 2.  
  **REVIEW NOTE:**

- [ ] **Step 12 — cicd-frontend: پرامپت CD از `product` به `chequeyar-front`**  
  - `prompts/05-cd-product-front.md`.  
  - ایمیج زنده؛ `workflow_dispatch` پس از merge به `product`.  
  - `cd-demo.yml` بدون تغییر.  
  **Verify:** پس از SHA Studio و تأیید مالک، سرویس محصول SPA (نه دمو) به‌روز می‌شود.  
  **REVIEW NOTE:**

### مستندات پایانی doion

- [ ] **Step 13 — docs در doion**  
  - `backend/README.md` و در صورت نیاز `docs/development/PRODUCTION_CHABOKAN_DEPLOY.md`: دو مسیر لوکال، CI=Postgres، محصول=Postgres، بدون staging، جریان `product` فرانت، بازیابی دستی.  
  - `MASTER_API_CONTRACT.md` را برای این ویژگی عوض نکن مگر رفتار API عوض شده باشد (نباید شده باشد).  
  **Verify:** سند با spec یکی است.  
  **REVIEW NOTE:**

## Key Decisions & Assumptions

- GitHub Environments و Dependabot و پین SHA اکشن‌ها عمداً در این نسخه نیستند؛ تأیید deploy = `workflow_dispatch` توسط مالک.
- E2E: `ui_sha` در رویداد؛ بدون required check روی PR `develop`؛ bump پین فقط PR به `develop`.
- Compose لوکال حداقل Postgres است؛ لازم نیست از روز اول کل Django داخل همان Compose باشد اگر مسیر B با `DATABASE_URL` کافی و مستند باشد.
- رجیستری ایمیج تا Step 10 اگر در ریپو مشخص نباشد، Chat 2 باید از کاربر بپرسد (GHCR در برابر رجیستری چابکان) و در REVIEW NOTE بنویسد.
- مخاطب استقرار محصول در این نسخه فقط مالک است؛ همکاران از Compose/CI استفاده می‌کنند نه از دکمهٔ deploy.
- Cookiecutter/چابکان فعلی (`chabok deploy` از سورس) در Steps 11–12 ممکن است به استقرار ایمیج تغییر کند؛ رفتار قابل مشاهده برای کاربر: همان سرویس‌های `chequeyar-back` / `chequeyar-front` با Postgres و SPA غیرmock.

## Open Questions

هیچ ⚠️ باز در `feature_spec.md` نمانده.

مواردی که Chat 2 نباید حدس بزند:

- نام دقیق رجیستری Docker اگر در پنل چابکان از قبل ست شده (Step 10).
- اجرای واقعی deploy روی سرویس زنده فقط با تأیید جدا در همان گام Chat 2.
