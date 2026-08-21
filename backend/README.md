# چک‌یار (Cheque Yar) — Backend

بک‌اند Django مونورپوی [doion](https://github.com/alamalhoda/doion) برای محصول چک‌یار.

**وضعیت محصول:** v1 لایه ۱ آماده پایلوت — نه در حال ساخت MVP، نه v1 لانچ‌شده.  
مرجع: [`docs/سند پایه پروژه (Core Brief).md`](../docs/سند%20پایه%20پروژه%20(Core%20Brief).md) · کار باز: [`TODO.md`](TODO.md)

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

## درباره پروژه

API لایه ۱ Marketplace: ثبت‌نام و KYC، آگهی چک، moderation، بازارچه، Match، تسویه **بیرون از پلتفرم**، اعلان، audit و Feature Flag. پشته از Cookiecutter Django است؛ دامنه زیر `doion/` است.

### Frontend (وضعیت فعلی)

| نقش | مکان |
|-----|------|
| Backend + قرارداد API (SSOT) | این repo (`backend/`, `docs/development/MASTER_API_CONTRACT.md`) |
| UI فعال | [alamalhoda/checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai) — توسعه در [AI Studio](https://aistudio.google.com/)؛ لوکال با **Bun** (`bun install` / `bun run dev`) |

**قانون یک‌طرفه UI:** AI Studio → GitHub → لوکال (`git pull`). از لوکال روی repo فرانت فعال push نکنید. Package manager UI فعال: **Bun** (`bun.lock`؛ نه `package-lock.json`). جزئیات: [`docs/development/FRONTEND_DEVELOPMENT_STATUS.md`](../docs/development/FRONTEND_DEVELOPMENT_STATUS.md).

### مشخصات فنی
- **Python**: 3.12
- **Django**: 5.2.14 (LTS)
- **مدیریت وابستگی**: uv
- **دیتابیس توسعهٔ لوکال روزانه:** PostgreSQL در Docker؛ اپ روی میزبان با `uv`
- **دیتابیس محصول و CI:** فقط PostgreSQL (بدون fallback به SQLite)
- **SQLite لوکال:** معتبر اگر Docker نخواهید؛ مسیر توصیه‌شده برای کار روزمره نیست
- جزئیات: [`docs/development/LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](../docs/development/LOCAL_DEV_AND_PRODUCT_RUNTIME.md)
- **زبان پیش‌فرض**: انگلیسی (en-us)
- **Timezone**: Asia/Tehran
- **احراز هویت:** django-allauth (جلسات قالب) + SimpleJWT برای `/api/v1/`
- **API:** Django REST Framework + drf-spectacular
- **پس‌زمینه:** Celery (انقضای آگهی؛ SMS stub)
- **CORS:** django-cors-headers (development allows all origins; specific origins listed in `config/settings/local.py`)

---

## راه‌اندازی سریع (Local Development)

توضیح دو مسیر **روزانه** (Postgres در Docker + اپ روی میزبان) و **محصول** (ایمیج Gunicorn): [`docs/development/LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](../docs/development/LOCAL_DEV_AND_PRODUCT_RUNTIME.md).

روزانهٔ توصیه‌شده: از ریشه `docker compose up -d`، در `.env` مقدار `DATABASE_URL=postgres://doion@localhost:5432/doion`، بعد دستورهای زیر. SQLite بدون Docker هنوز معتبر است اگر Compose را روشن نکنید.

### ۱. فعال کردن محیط مجازی

```bash
cd /path/to/doion/backend
source .venv/bin/activate
```

### ۲. نصب وابستگی‌ها

```bash
uv sync
```

### ۳. متغیرهای محیطی (لوکال)

```bash
cp .env.example .env
# در صورت نیاز مقادیر را ویرایش کنید
```

`config/settings/base.py` در صورت وجود، `backend/.env` را بارگذاری می‌کند. متغیرهای سیستم / پنل چابکان همیشه اولویت دارند. روی چابکان فایل `.env` آپلود نکنید؛ همان کلیدها را در پنل سرویس تنظیم کنید.

### ۴. اعمال Migrationها و ایجاد کاربر ادمین

```bash
python manage.py migrate
python manage.py createsuperuser
```

### ۵. اجرای سرور

```bash
python manage.py runserver
```

سپس به آدرس [http://localhost:8000/](http://localhost:8000/) بروید.

جزئیات مسیرها، pytest، امتحان ایمیج (`--profile app`) و ساخت `docker build -t doion-api ./backend`: [`LOCAL_DEV_AND_PRODUCT_RUNTIME.md`](../docs/development/LOCAL_DEV_AND_PRODUCT_RUNTIME.md).

---

## CI (GitHub Actions)

روی هر `pull_request` و `push` به شاخه `develop`، workflowی [`.github/workflows/ci-backend.yml`](../.github/workflows/ci-backend.yml) در پوشه `backend/` دو job اجباری اجرا می‌کند:

1. `uv run ruff check .`
2. `uv run pytest` روی **PostgreSQL** سرویس Actions (`DATABASE_URL`؛ اگر Postgres آماده نباشد Check ناموفق است و به SQLite برنمی‌گردد)

معادل لوکال روزانه (از داخل `backend/` با `DATABASE_URL` پستگرس Compose):

```bash
uv sync --frozen
uv run ruff check .
uv run pytest
```

بدون `postgres` در `DATABASE_URL`، pytest لوکال روی `test_db.sqlite3` می‌ماند. CI گیت‌هاب هرگز به SQLite برنمی‌گردد.

E2E Playwright در [`.github/workflows/ci-e2e.yml`](../.github/workflows/ci-e2e.yml) هست و **gate ادغام PR به `develop` نیست**. اجرای دستی علیه یک commit فرانت: `gh workflow run "CI E2E Playwright" -f ui_sha=<sha>`. رویداد `repository_dispatch` با type‏ `frontend-e2e` و `client_payload.ui_sha` همان کار را می‌کند. بعد از E2E موفقِ dispatch، job جدا PR به `develop` باز می‌کند و فقط [`e2e/ui-pin`](../e2e/ui-pin) را عوض می‌کند (نه فایل workflow؛ `GITHUB_TOKEN` اجازهٔ ویرایش YAML را ندارد).

### انتشار تگ‌شده (GHCR)

ایمیج API و SPA با یک تگ SemVer روی [GitHub Container Registry](https://github.com/alamalhoda/doion/pkgs) ساخته می‌شود؛ رجیستری چابکان در پنل ست نشده بود. فقط با اجرای دستی workflow [`Release`](../.github/workflows/release.yml) (نه روی هر merge به `develop`).

در GitHub: Actions → **Release** → Run workflow → شاخه (معمولاً `develop`) و نسخه مثل `0.1.0-test.1`.

```bash
gh workflow run Release --ref develop -f version=0.1.0-test.1
```

تگ تکراری رد می‌شود. نسخهٔ با پسوند (`-test.1`) به‌صورت prerelease ساخته می‌شود. SPA از SHA داخل [`e2e/ui-pin`](../e2e/ui-pin) بیلد می‌شود.

### CD تأییدشده به `chequeyar-back`

محیط زنده با merge به `develop` عوض نمی‌شود. مالک workflow [`CD Backend`](../.github/workflows/cd-backend.yml) را دستی اجرا می‌کند و تگ موجود را می‌دهد (مثلاً `v0.1.0-test.2`). Job فقط اگر Release و ایمیج GHCR آن تگ موجود باشند و آخرین `CI Backend` روی همان commit سبز باشد، سورس همان تگ را با CLI چابکان به سرویس `chequeyar-back` می‌فرستد (`CHABOKAN_TOKEN` در Secrets ریپو). Postgres از پنل سرویس می‌آید؛ این workflow `DATABASE_URL` را عوض نمی‌کند.

```bash
gh workflow run "CD Backend" --ref develop -f tag=v0.1.0-test.2
```

اگر job قرمز شد، محصول را با اجرای دوبارهٔ همین workflow روی **آخرین تگ موفقی** که می‌شناسید برگردانید؛ rollback خودکار چابکان در این نسخه نیست. آموزش دکمه به دکمه: [`CHABOKAN_CD_AND_PRODUCT_BRANCH.md`](../docs/development/CHABOKAN_CD_AND_PRODUCT_BRANCH.md).

---

## Staging روی چابکان (PaaS)

این ویژگی CI/CD **محیط staging جدیدی نساخت.** مسیر زیر همان CLI دستی از داخل `backend/` به سرویس Django موجود است (پایلوت)، جدا از workflow **CD Backend**.

```bash
chabok login
chabok deploy
```

فایل‌های مرتبط:

| فایل | نقش |
|------|-----|
| `chabok.json` | نام سرویس Django (`chequeyar-back`) |
| `.chabokignore` | حذف `.venv` / `.env` / SQLite / `staticfiles` از آپلود |
| `nginx.conf` | سرو `/static/` از `staticfiles/` (نه `/app/static/`) |
| `chabok-pre-start.sh` | `migrate` + `collectstatic` قبل از Gunicorn |

Secrets و `DATABASE_URL` فقط در پنل سرویس تنظیم شوند؛ فایل `.env` آپلود نشود.

این محیط **staging/پایلوت** است، نه لانچ عمومی. Production جدا (سرویس API + SPA) در [`docs/development/PRODUCTION_CHABOKAN_DEPLOY.md`](../docs/development/PRODUCTION_CHABOKAN_DEPLOY.md) آمده است. Postgres برای staging/پایلوت الزامی است؛ SQLite فقط لوکال/دمو.

---

## دستورات مفید

### اجرای تست‌ها
```bash
uv run pytest
```

### اجرای تست‌ها با coverage
```bash
uv run pytest --cov=doion --cov-report=term-missing --cov-report=html
```
خروجی HTML در `htmlcov/index.html` ساخته می‌شود.

### چک کردن نوع‌ها (Type Checking)
```bash
uv run mypy doion
```

### اجرای سرور با uv
```bash
uv run python manage.py runserver
```

### ایجاد Superuser
```bash
python manage.py createsuperuser
```

### Factories (تست و دمو)

Factoryهای دامنه در ماژول‌های اپ (خارج از `tests/`) هستند تا هم تست و هم دستورات management مثل seed دمو بتوانند از همان SSOT استفاده کنند:

| ماژول | Factoryها |
|-------|-----------|
| `doion.users.factories` | `UserFactory` (+ traits: `as_investor`, `as_moderator`, `as_admin`) |
| `doion.banks.factories` | `BankFactory` |
| `doion.checks.factories` | `IssuerProfileFactory`, `ChequeListingFactory` |
| `doion.identity.factories` | `ProfileFactory`, `VerificationFactory` |
| `doion.notifications.factories` | `NotificationFactory`, `NotificationPreferenceFactory` |
| `doion.matching.factories` | `MatchFactory` |
| `doion.moderation.factories` | `ModerationDecisionFactory` |

نمونه:
```python
from doion.checks.factories import ChequeListingFactory
from doion.users.factories import UserFactory

holder = UserFactory.create()
investor = UserFactory.create(as_investor=True)
listing = ChequeListingFactory.create(published=True, owner=holder)
```

### Seed دمو (محلی / دستی / آماده‌سازی E2E)

توسعه روزمره روی `db.sqlite3` است. برای دمو قابل‌پاک‌سازی بدون دست زدن به DB شخصی:

```bash
export DJANGO_DEMO_DATABASE=1
uv run python manage.py migrate
uv run python manage.py seed_demo --reset --password "$DEMO_SEED_PASSWORD"
uv run python manage.py runserver
```

بدون فلگ دمو (همان DB عادی):

```bash
uv run python manage.py seed_demo
# یا با پسورد ثابت برای سناریوهای تکراری:
uv run python manage.py seed_demo --password "$DEMO_SEED_PASSWORD"
# بازنشانی کاربران دمو و seed دوباره (روی DB فعلی — مراقب دادهٔ شخصی باشید):
uv run python manage.py seed_demo --reset --password "$DEMO_SEED_PASSWORD"
```
کاربران: `holder1`, `investor1`, `moderator1`, `admin1` — پسورد در خروجی دستور چاپ می‌شود.

توضیح کامل (mock فرانت، seed، `DJANGO_DEMO_DATABASE`، چابکان):  
[`docs/development/BACKEND_DEMO_SEED_AND_DATA.md`](../docs/development/BACKEND_DEMO_SEED_AND_DATA.md)

### آماده‌سازی E2E (smoke)

Harness Playwright در ریشهٔ مونورپو (`e2e/`) است، نه در ریپوی UI. برای seed ایزولهٔ دمو قبل از تست:

```bash
./e2e/scripts/prepare-backend.sh
# سپس runserver با DJANGO_DEMO_DATABASE=1 و UI با VITE_USE_MOCK=false
./e2e/scripts/run-smoke.sh
```

جزئیات: [`docs/development/E2E_LOCAL_RUNBOOK.md`](../docs/development/E2E_LOCAL_RUNBOOK.md).

---

## ساختار پروژه

```
backend/                            ← ریشه بک‌اند (Django)
│
├── config/                         ← تنظیمات مرکزی پروژه
│   ├── __init__.py
│   ├── settings/                   ← تنظیمات محیطی (ماژول‌بندی شده)
│   │   ├── __init__.py
│   │   ├── base.py                 ← تنظیمات پایه (مشترک بین همه محیط‌ها)
│   │   ├── local.py                ← تنظیمات محیط توسعه
│   │   ├── production.py           ← تنظیمات محیط تولید
│   │   └── test.py                 ← تنظیمات محیط تست
│   ├── urls.py                     ← مسیریابی اصلی URL
│   ├── api_router.py               ← مسیریابی API (DefaultRouter / SimpleRouter)
│   └── wsgi.py                     ← نقطه ورود WSGI
│
├── doion/                          ← دایرکتوری اپلیکیشن‌ها (APPS_DIR)
│   ├── __init__.py
│   ├── conftest.py                 ← تنظیمات تست پایه
│   │
│   ├── users/                      ← اپ مدیریت کاربران (+ JWT login/refresh)
│   ├── core/                       ← مدل‌های پایه، permissions، seed_demo
│   ├── identity/                   ← Profile, Verification, register/me
│   ├── documents/                  ← Document
│   ├── checks/                     ← ChequeListing, IssuerProfile
│   ├── pricing/                    ← موتور stub نرخ پیشنهادی
│   ├── marketplace/                ← جست‌وجو/فیلتر آگهی‌های published
│   ├── matching/                   ← Match + تسویه off-platform
│   ├── moderation/                 ← صف آگهی و KYC
│   ├── notifications/              ← اعلان درون‌برنامه‌ای
│   ├── compliance/                 ← AuditEvent, FeatureFlag, stats
│   ├── integrations/               ← SMS stub
│   │
│   ├── contrib/                    ← کدهای کمکی
│   │   └── sites/                  ← اپ sites جنگو
│   │       └── migrations/
│   │           ├── 0001_initial.py
│   │           ├── 0002_alter_domain_unique.py
│   │           ├── 0003_set_site_domain_and_name.py
│   │           └── 0004_alter_options_ordering_domain.py
│   │
│   ├── static/                     ← فایل‌های استاتیک
│   │   ├── css/
│   │   │   └── project.css
│   │   ├── fonts/
│   │   │   └── .gitkeep
│   │   ├── images/
│   │   │   └── favicons/
│   │   │       └── favicon.ico
│   │   └── js/
│   │       └── project.js
│   │
│   └── templates/                  ← قالب‌های HTML
│       ├── base.html               ← قالب پایه سایت
│       ├── 403.html                ← خطای 403
│       ├── 403_csrf.html           ← خطای CSRF
│       ├── 404.html                ← خطای 404
│       ├── 500.html                ← خطای 500
│       ├── pages/
│       │   ├── home.html           ← صفحه اصلی
│       │   └── about.html          ← صفحه درباره ما
│       ├── account/
│       │   └── base_manage_password.html
│       ├── allauth/                ← قالب‌های django-allauth
│       │   ├── elements/           ← المان‌های UI (alert, badge, button, field, ...)
│       │   └── layouts/            ← لایه‌های اصلی (entrance, manage)
│       └── users/                  ← قالب‌های پروفایل کاربر
│           ├── user_detail.html
│           └── user_form.html
│
├── .env                            ← متغیرهای لوکال (gitignored؛ از .env.example کپی شود)
├── .env.example                    ← نمونه کلیدهای محیطی (لوکال + مثال چابکان)
├── .editorconfig                   ← تنظیمات ویرایشگر
├── .gitignore                      ← فایل‌های نادیده‌گرفته‌شده توسط Git
├── .gitattributes                  ← ویژگی‌های Git
├── manage.py                       ← اسکریپت مدیریت Django
├── pyproject.toml                  ← مدیریت وابستگی‌ها و تنظیمات ابزارها
├── uv.lock                         ← قفل وابستگی‌های uv
├── requirements.txt                ← وابستگی‌های pip برای استقرار (مثلاً چابکان)
└── README.md                       ← همین فایل 📄
```

---

## مسیرهای URL

| مسیر | توضیح |
|------|-------|
| `/` | صفحه اصلی (home) |
| `/about/` | صفحه درباره ما |
| `/admin/` | پنل مدیریت Django |
| `/users/` | مسیرهای کاربران (پروفایل، ویرایش) |
| `/accounts/` | مسیرهای allauth (ورود، ثبت‌نام، ...) |
| `/api/` | نقطه ورود API |
| `/api/users/` | API کاربران (لیست، جزئیات، ویرایش) |
| `/api/users/me/` | اطلاعات کاربر جاری |
| `/api/v1/auth/login/` | ورود با JWT |
| `/api/v1/auth/refresh/` | تمدید توکن |
| `/api/v1/identity/register/` | ثبت‌نام |
| `/api/v1/identity/me/` | اطلاعات کاربر جاری (UserMe) |
| `/api/v1/identity/profile/` | پروفایل کاربر جاری (Profile) |
| `/api/v1/verifications/` | احراز هویت (KYC) |
| `/api/v1/listings/` | آگهی‌های چک |
| `/api/v1/listings/my/` | آگهی‌های من |
| `/api/v1/marketplace/listings/` | مارکت‌پلیس |
| `/api/v1/marketplace/listings/latest/` | ۴ آگهی آخر |
| `/api/v1/matches/` | تطابق‌ها |
| `/api/v1/matches/my/` | تطابق‌های من |
| `/api/v1/notifications/` | اعلان‌ها |
| `/api/v1/moderation/queue/` | صف نظارت |
| `/api/v1/compliance/stats/` | آمار ادمین |
| `/api/v1/compliance/feature-flags/` | فلگ‌های قابلیت |
| `/api/v1/issuer-profiles/` | پروفایل صادرکننده |
| `/api/v1/moderation/kyc/` | صف KYC |
| `/api/v1/compliance/audit/` | رویدادهای audit |
| `/api/schema/` | اسکیمای API |
| `/api/docs/` | مستندات Swagger |

مرجع قرارداد کامل API (SSOT): [`docs/development/MASTER_API_CONTRACT.md`](../docs/development/MASTER_API_CONTRACT.md)

---

## ابزارهای توسعه

| ابزار | کاربرد |
|-------|--------|
| **ruff** | Linter و formatter |
| **mypy** | بررسی نوع‌ها (Type checking) |
| **pytest** | فریمورک تست |
| **coverage** | پوشش کد |
| **pre-commit** | هوک‌های Git |
| **djlint** | فرمت‌دهی قالب‌های Django |
| **django-debug-toolbar** | ابزار دیباگ |
| **django-extensions** | ابزارهای کمکی Django |

---

## وابستگی‌های اصلی

| پکیج | نسخه | کاربرد |
|------|------|--------|
| django | 5.2.14 | فریمورک اصلی |
| djangorestframework | 3.15 - 3.18 | ساخت API |
| django-allauth | 64.0 - 66.0 | احراز هویت قالب |
| djangorestframework-simplejwt | (pyproject) | JWT برای `/api/v1/` |
| celery | 5.4+ | job پس‌زمینه |
| drf-spectacular | 0.29.0 | مستندسازی API |
| django-cors-headers | 4.9.0 | مدیریت CORS |
| django-crispy-forms | 2.5+ | فرم‌های Bootstrap 5 |
| whitenoise | 6.12.0 | سرو فایل‌های استاتیک |
| argon2-cffi | 25.1.0 | هش کردن رمز عبور |
| django-redis | 6.0.0 | کش با Redis |

---

## Deployment

استقرار فعلی روی **چابکان** است (نه Railway/Render/Fly):

| محیط | وضعیت |
|------|--------|
| لوکال | SQLite + `runserver` (دمو: `DJANGO_DEMO_DATABASE=1` + `seed_demo`) |
| Staging / پایلوت | `chabok deploy` از `develop` روی `chequeyar-back` — Postgres در پنل |
| Production | runbook موجود؛ **لانچ عمومی نشده** — [`PRODUCTION_CHABOKAN_DEPLOY.md`](../docs/development/PRODUCTION_CHABOKAN_DEPLOY.md) |

تگ SemVer محصول (GitHub Release + ایمیج GHCR، بدون deploy خودکار) در [`GIT_TAGS_AND_RELEASES.md`](../docs/development/GIT_TAGS_AND_RELEASES.md) آموزش داده شده است.

هرگز `seed_demo --reset` روی دیتابیس کاربران واقعی اجرا نکنید.

---

## توسعه

- Debug Toolbar فعال است (در محیط لوکال)
- از `django-debug-toolbar` برای دیباگ استفاده کنید
- زبان پیش‌فرض انگلیسی و timezone روی تهران تنظیم شده است
- مدیریت وابستگی‌ها با `uv` انجام می‌شود

- کار باز بک‌اند: [`TODO.md`](TODO.md)

---

**چک‌یار — v1 لایه ۱ آماده پایلوت.**