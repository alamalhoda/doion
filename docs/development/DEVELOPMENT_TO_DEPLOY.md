# از توسعه تا استقرار — راهنمای آموزشی چک‌یار

**مخاطب:** مالک یا همکار که می‌خواهد کل مسیر را یک‌جا بفهمد.  
**تاریخ هم‌ترازی:** ۲۱ اوت ۲۰۲۶.

جزئیات عملیاتی (دکمه به دکمه، env پنل، SemVer) در اسناد پیوندشده است. این فایل **نقشهٔ ذهنی** است: محیط‌ها چیستند، بک‌اند با فرانت چه فرقی دارد، و یک تغییر چگونه از لپ‌تاپ به کاربر می‌رسد.

---

## ۱. یک محصول، دو ریپو، چهار سرویس

مرورگر کاربر فقط سایت را می‌بیند. پشت صحنه دو ریپوی گیت و چند سرویس چابکان است.

| لایه | ریپو | چه کسی کد می‌زند | کجا زنده می‌شود |
|------|------|------------------|------------------|
| API (Django) | [doion](https://github.com/alamalhoda/doion) | Cursor + GitFlow از `develop` | سرویس `chequeyar-back` |
| SPA (Vue) | [checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai) | **فقط Google AI Studio** به `main`؛ Cursor سورس UI را پوش نمی‌کند | محصول: `chequeyar-front` — دمو mock: `chequeyar-front-demo` |
| Postgres | — | پنل چابکان | `chequeyar-db` (سایت نیست) |

```text
مرورگر  →  https://royasoft.dev          SPA محصول (Static)
                │  آدرس API در بیلد قفل شده
                ▼
         https://chequeyar-back.chbkn.dev/api/v1
                │
         Postgres + Redis در پنل
```

قرارداد REST فقط [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md) است. فرانت و بک‌اند جدا به‌روز می‌شوند؛ اگر API عوض شود باید UI در Studio هم‌خوان شود.

---

## ۲. محیط‌ها (چه چیزی «محیط» است)

staging جدا در این نسخه **ساخته نشده**. این‌ها محیط‌های واقعی شما هستند:

| محیط | مخاطب | بک‌اند | فرانت | داده | چطور بالا می‌آید |
|------|--------|--------|--------|------|-------------------|
| **لوکال روزانه** | شما روی مک | `runserver` + `config.settings.local` | Vite (`bun run dev`) روی `127.0.0.1:3000` | Postgres در Docker **یا** SQLite | دستی؛ بدون Actions |
| **لوکال زنده علیه API لوکال** | شما | همان `runserver` | Vite با `VITE_USE_MOCK=false` و `VITE_API_BASE_URL=http://localhost:8000/api/v1` | همان DB لوکال | `.env` کلون UI |
| **لوکال mock** | شما بدون Django | لازم نیست | Vite با `VITE_USE_MOCK=true` | شبیه‌ساز در مرورگر | پیش‌فرض دمو |
| **CI بک‌اند** | GitHub | pytest + Ruff | — | **فقط Postgres** سرویس Actions | هر PR به `develop` |
| **CI فرانت** | GitHub | — | typecheck، Vitest، دو `vite build` (پیش‌فرض + live)، `docker build` | — | push/PR روی `main` و PR به `product` |
| **E2E** | GitHub (doion) | API تست در workflow | checkout SHA فرانت (`ui_sha` یا پین) | دادهٔ تست E2E | غیرمسدودکننده برای merge بک‌اند |
| **دمو mock میزبانی‌شده** | نمایش به دیگران بدون API واقعی | به API محصول وصل **نمی‌شود** | باندل `VITE_USE_MOCK=true` | mock | هر push به `main` → **CD Demo** → [royasoftgroup.ir](https://royasoftgroup.ir/) |
| **محصول** | کاربر واقعی | Gunicorn، `production`، Postgres پنل | باندل `VITE_USE_MOCK=false` | دادهٔ واقعی | **CD Backend** (تگ) + **CD Product** (شاخه `product`) |

تفاوت مهم: **دمو روی دامنهٔ جدا** است نه «staging API». محصول [royasoft.dev](https://royasoft.dev/) است؛ دمو [royasoftgroup.ir](https://royasoftgroup.ir/).

---

## ۳. بک‌اند: توسعه در برابر استقرار

### توسعه (هر روز)

- شاخه از `develop`: `feature/…` سپس PR به `develop`. روی `main`/`develop` مستقیم commit نکنید.
- محیط مجازی: `source backend/.venv/bin/activate` قبل از هر `python` / `pytest` / `manage.py`.
- اپ روی **میزبان** است (`uv` + `runserver`)، نه داخل ایمیج Docker روزانه.
- تنظیمات: `local`؛ Redis لازم نیست.
- داده: مسیر توصیه‌شده Postgres در Compose؛ SQLite بدون Docker هنوز معتبر است. جزئیات: [`LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](./LOCAL_DEV_AND_PRODUCT_RUNTIME.md).
- تست لوکال: `uv run ruff check .` و `uv run pytest`. اگر `DATABASE_URL` پستگرس نباشد، pytest فایل SQLite می‌سازد — با CI یکی نیست.
- اسرار در `.env` لوکال؛ در گیت نرود.

### تست خودکار بک‌اند

- PR به `develop`: jobهای **Ruff** و **pytest روی Postgres**. هر دو باید سبز باشند. Fallback به SQLite در Actions وجود ندارد.
- E2E Playwright **gate ادغام PR بک‌اند نیست**. بعد از push فرانت به `main`، doion با `ui_sha` اجرا می‌شود؛ پین [`e2e/ui-pin`](../../e2e/ui-pin) فقط با PR به `develop` عوض می‌شود.

### استقرار بک‌اند (محصول)

این‌ها **سه عمل جدا** هستند. هیچ‌کدام خودکار روی merge نیستند.

```text
PR → develop     ≠  سرور عوض نمی‌شود
Release (تگ)     ≠  سرور عوض نمی‌شود؛ فقط تگ + ایمیج GHCR
CD Backend       =  سورس همان تگ با CLI به chequeyar-back
```

1. **Release** (`workflow_dispatch` روی doion): ورودی SemVer مثل `0.1.0-test.2` → تگ `v…` + GitHub Release + ایمیج `doion-api` و `chequeyar-front` روی GHCR. آموزش: [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md).
2. **CD Backend**: همان تگ را می‌گیرد؛ اگر Release و ایمیج و CI Backend سبز باشند، `chabok deploy` از **سورس Django همان تگ** به `chequeyar-back`. پنل هنوز ایمیج GHCR را pull نمی‌کند. قبل از Gunicorn: `migrate` + `collectstatic`.
3. تنظیمات محصول: `config.settings.production`، فقط Postgres، Redis، اسرار در **پنل** نه در گیت. `CORS_ALLOWED_ORIGINS` باید origin مرورگر SPA را داشته باشد (`https://royasoft.dev`).

بازیابی اگر CD قرمز شد: همان workflow را با **آخرین تگ موفقی** که می‌شناسید دوباره بزنید. تگ را force نکنید.

نقش کاربر در SPA از `users.User.role` می‌آید؛ در ادمین جنگو Users فیلد Role دیده می‌شود و با Profile هم‌تراز می‌شود.

---

## ۴. فرانت: توسعه در برابر استقرار

### توسعه

- کد UI فقط در **Google AI Studio** نوشته و به `main` پوش می‌شود. Cursor به `checkyar-googleai` commit/push نمی‌کند (Studio remote را pull نمی‌کند).
- Package manager: **Bun** و `bun.lock`. `package-lock.json` نسازید.
- لوکال بعد از `git pull`: `bun install` سپس ترجیحاً  
  `bun run dev -- --host 127.0.0.1 --port 3000`.
- دو حالت بیلد/اجرا:
  - **Mock:** `VITE_USE_MOCK=true` — بدون Django؛ فلگ لندینگ در شبیه‌ساز روشن است.
  - **Live لوکال:** `VITE_USE_MOCK=false` و API روی `http://localhost:8000/api/v1`.
- روی محصول، `VITE_*` در **زمان بیلد GitHub** پخته می‌شود. تغییر env پنل Static آن را عوض نمی‌کند. سرویس فرانت **Static** است نه Vue PaaS (روی سرور `npm run build` نمی‌زند). `nginx.conf` باید آپلود شود (`root /usr/share/nginx/html/dist`)؛ در `.chabokignore` نباشد.

سیاست یک‌طرفه: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md).

### شاخه‌های فرانت

```text
Studio  --push-->  main          ← ورودی + CD Demo (mock) خودکار
                     │
                     │  PR (Merge اگر CI سبز)
                     ▼
                  product        ← خط تولید؛ CD Product دستی
                     │
                     ▼
              chequeyar-front / royasoft.dev
```

`main` خام به محصول deploy نمی‌شود.

### استقرار فرانت (دو مقصد)

| | CD Demo | CD Product |
|--|---------|------------|
| کی | هر push به `main` | فقط Run workflow |
| شاخه | `main` | **`product`** |
| باندل | mock | live (`VITE_USE_MOCK=false`، API چابکان) |
| سرویس | `chequeyar-front-demo` | `chequeyar-front` |
| سایت | royasoftgroup.ir | royasoft.dev |

فایل committed `chabok.json` نام دمو را دارد. CD Product روی runner قبل از deploy آن را به `chequeyar-front` عوض می‌کند؛ وگرنه CLI فلگ `-s` را نادیده می‌گیرد و به دمو می‌رود.

ایمیج Docker SPA در **Release** doion از SHA پین E2E ساخته می‌شود؛ چابکان فعلاً آن ایمیج را pull نمی‌کند — استقرار زنده همان آپلود Static است.

---

## ۵. نقشهٔ یک تغییر از ایده تا کاربر

### بک‌اند (مثلاً نقش ادمین)

```text
feature/*  →  PR به develop  →  Ruff+pytest سبز  →  Merge
     →  (اختیاری) Release تگ جدید
     →  CD Backend با همان تگ
     →  chequeyar-back  →  کاربر API جدید را می‌بیند
     →  خروج/ورود در SPA تا JWT نقش تازه بگیرد
```

### فرانت (مثلاً صفحهٔ معرفی)

```text
Studio → push main → CI + CD Demo (mock روی royasoftgroup.ir)
     →  PR main→product → CI روی آن PR
     →  Merge به product  ≠  هنوز royasoft.dev عوض نشده
     →  CD Product روی شاخه product
     →  chequeyar-front
```

اگر قابلیت به فلگ API وابسته است (مثل `show_landing_page`)، بیلد SPA کافی نیست؛ فلگ را در `/admin/feature-flags` روشن کنید. دمو mock این فلگ را در شبیه‌ساز روشن دارد؛ محصول پیش‌فرض خاموش است.

### وقتی API و UI با هم لازم‌اند

ترتیب پیشنهادی: اول CD Backend (قرارداد روی سرور)، بعد CD Product (باندلی که همان API را صدا می‌زند). اجباری نیست اگر فقط یکی عوض شده.

---

## ۶. تست‌ها از نزدیک به دور

| لایه | کجا | چه چیزی ثابت می‌شود |
|------|-----|----------------------|
| واحد / قرارداد بک‌اند | pytest لوکال و CI | مدل، API، دسترسی |
| کیفیت بک‌اند | Ruff در لوکال و CI | سبک و خطای ایستا |
| واحد فرانت | Vitest در CI UI | منطق Vue |
| بیلد فرانت | دو vite build + docker build در CI | mock و live هر دو جمع می‌شوند |
| E2E | Playwright در doion | مسیرهای حیاتی مرورگر علیه SHA مشخص UI |
| پذیرش محصول | دستی روی royasoft.dev | لاگین واقعی، بدون نوار شبیه‌ساز |

Runbook E2E لوکال: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md).

---

## ۷. چه کسی چه دکمه‌ای را می‌زند

| کار | Cursor / چت | شما (مالک) |
|-----|-------------|------------|
| کد بک‌اند، PR به `develop` | بله | Merge اگر Checks سبز |
| کد UI | خیر (پرامپت Studio) | پوش Studio؛ Merge PR به `product` |
| تگ SemVer / Release | فقط بعد از تأیید نسخه | Run workflow یا «تگ بزن» در چت |
| CD Backend / CD Product | فقط اگر صریح بگویید | Run workflow |
| راز `CHABOKAN_TOKEN` | هرگز در گیت/چت | Secrets هر دو ریپو |
| `seed_demo --reset` روی DB محصول | ممنوع | نکنید |

دکمه به دکمهٔ CD: [`CHABOKAN_CD_AND_PRODUCT_BRANCH.md`](./CHABOKAN_CD_AND_PRODUCT_BRANCH.md).  
Env و دامنه و نوع PaaS: [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md).

---

## ۸. اشتباه‌های رایج

| فرض | واقعیت |
|-----|--------|
| Merge به `develop` یعنی API روی چابکان عوض شد | فقط git؛ تا CD Backend نه |
| تگ یعنی سایت عوض شد | تگ = آرتیفکت؛ CD جدا است |
| پوش Studio به `main` یعنی royasoft.dev عوض شد | فقط دمو mock؛ محصول از `product` است |
| فرانت و بک‌اند یک نوع سرویس چابکان دارند | API Django/سورس؛ هر دو SPA **Static** |
| env پنل Static مقدار `VITE_*` را عوض می‌کند | فقط بیلد Actions |
| Role در Identity → Profile برای منوی ادمین SPA کافی است | SPA از `User.role` می‌خواند |
| `chequeyar-front.chbkn.dev` همیشه همان سایت کاربر است | دامنهٔ کاربر royasoft.dev است؛ CORS باید همان origin را داشته باشد |
| Staging جدا برای این ویژگی وجود دارد | خیر؛ پایلوت همان سرویس‌های محصول/دمو است |

---

## ۹. چک‌لیست ذهنی «آماده‌ام استقرار کنم؟»

بک‌اند:

- [ ] PR روی `develop` سبز است (Ruff + pytest Postgres)
- [ ] تگ Release برای همین commit وجود دارد (یا همین الان می‌سازید)
- [ ] می‌دانید کدام تگ را به CD می‌دهید
- [ ] پنل: Postgres، Redis، CORS شامل `https://royasoft.dev`

فرانت:

- [ ] تغییر در Studio روی `main` است و CI سبز
- [ ] PR `main` → `product` merge شده
- [ ] CD Product را روی شاخه **`product`** می‌زنید
- [ ] View Source ریشه `/src/main.ts` نیست (یعنی باندل Vite سرو می‌شود)
- [ ] نوار شبیه‌ساز روی royasoft.dev نیست

---

## ۱۰. نقشهٔ اسناد (جزئیات این‌جا تکرار نمی‌شود)

| سند | نقش |
|-----|-----|
| **همین فایل** | نقشهٔ آموزشی سر تا ته |
| [`LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](./LOCAL_DEV_AND_PRODUCT_RUNTIME.md) | لوکال: میزبان + Postgres Docker در برابر ایمیج محصول |
| [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md) | Studio یک‌طرفه، Bun، پورت Vite |
| [`CHABOKAN_CD_AND_PRODUCT_BRANCH.md`](./CHABOKAN_CD_AND_PRODUCT_BRANCH.md) | دکمه‌های GitHub و وضعیت زنده |
| [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md) | SemVer و workflow Release |
| [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md) | پنل، دامنه، CORS، نوع Static |
| [`backend/README.md`](../../backend/README.md) | Ruff، pytest، CD Backend، CLI چابکان |
| [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md) | Playwright لوکال |
| [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md) | seed دمو در برابر DB محصول |
| [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md) | تنها SSOT قرارداد REST |
| [`ai-documents/features/cicd-chabokan-prod/implementation_plan.md`](../../ai-documents/features/cicd-chabokan-prod/implementation_plan.md) | سابقهٔ گام‌های CI/CD نسخهٔ فعلی (تمام) |
| [`CICD_NEXT_ROADMAP.md`](./CICD_NEXT_ROADMAP.md) | نقشه راه CI/CD بعدی (هنوز اجرا نشده) |
