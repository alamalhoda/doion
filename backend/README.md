# doion

Doion Project

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

## درباره پروژه

پروژه doion با استفاده از **Cookiecutter Django** ساخته شده و از بهترین شیوه‌های توسعه Django پیروی می‌کند.

### Frontend (وضعیت فعلی)

| نقش | مکان |
|-----|------|
| Backend + قرارداد API (SSOT) | این repo (`backend/`, `docs/development/MASTER_API_CONTRACT.md`) |
| UI فعال | [alamalhoda/checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai) — توسعه در [AI Studio](https://aistudio.google.com/)؛ لوکال با **Bun** (`bun install` / `bun run dev`) |
| UI آرشیو | `frontend-legacy/` در همین مونورپو (فقط مستندات/مرجع) |

**قانون یک‌طرفه UI:** AI Studio → GitHub → لوکال (`git pull`). از لوکال روی repo فرانت فعال push نکنید. Package manager UI فعال: **Bun** (`bun.lock`؛ نه `package-lock.json`). جزئیات: [`docs/development/FRONTEND_DEVELOPMENT_STATUS.md`](../docs/development/FRONTEND_DEVELOPMENT_STATUS.md).

### مشخصات فنی
- **Python**: 3.12
- **Django**: 5.2.14 (LTS)
- **مدیریت وابستگی**: uv
- **دیتابیس توسعه**: SQLite
- **زبان پیش‌فرض**: انگلیسی (en-us)
- **Timezone**: Asia/Tehran
- **احراز هویت**: django-allauth
- **API**: Django REST Framework + drf-spectacular
- **CORS**: django-cors-headers (development allows all origins; specific origins listed in `config/settings/local.py`)

---

## راه‌اندازی سریع (Local Development)

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

سپس به آدرس [http://127.0.0.1:8000/](http://127.0.0.1:8000/) بروید.

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
│   ├── users/                      ← اپ مدیریت کاربران
│   │   ├── __init__.py
│   │   ├── models.py               ← مدل User سفارشی (AbstractUser)
│   │   ├── views.py                ← ویوهای کاربر (Detail, Update, Redirect)
│   │   ├── urls.py                 ← URLهای مربوط به کاربران
│   │   ├── admin.py                ← تنظیمات پنل ادمین
│   │   ├── forms.py                ← فرم‌های ثبت‌نام و احراز هویت
│   │   ├── adapters.py             ← آداپتورهای django-allauth
│   │   ├── apps.py                 ← تنظیمات اپ
│   │   ├── context_processors.py   ← پردازشگرهای زمینه
│   │   ├── api/                    ← لایه REST API برای کاربران
│   │   │   ├── __init__.py
│   │   │   ├── views.py            ← UserViewSet (Retrieve, List, Update, Me)
│   │   │   └── serializers.py      ← UserSerializer
│   │   └── migrations/             ← مایگریشن‌های دیتابیس
│   │       ├── __init__.py
│   │       └── 0001_initial.py
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
| django-allauth | 64.0 - 66.0 | احراز هویت |
| drf-spectacular | 0.29.0 | مستندسازی API |
| django-cors-headers | 4.9.0 | مدیریت CORS |
| django-crispy-forms | 2.5+ | فرم‌های Bootstrap 5 |
| whitenoise | 6.12.0 | سرو فایل‌های استاتیک |
| argon2-cffi | 25.1.0 | هش کردن رمز عبور |
| django-redis | 6.0.0 | کش با Redis |

---

## Deployment (آینده)

پروژه برای Docker و PaaSها (مانند Railway, Render, Fly.io) آماده‌سازی خواهد شد.

---

## توسعه

- Debug Toolbar فعال است (در محیط لوکال)
- از `django-debug-toolbar` برای دیباگ استفاده کنید
- زبان پیش‌فرض انگلیسی و timezone روی تهران تنظیم شده است
- مدیریت وابستگی‌ها با `uv` انجام می‌شود

---

**خوش‌آمدید به پروژه doion!** 🚀