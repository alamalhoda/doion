# doion

Doion Project

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)

## درباره پروژه

پروژه doion با استفاده از **Cookiecutter Django** ساخته شده و از بهترین شیوه‌های توسعه Django پیروی می‌کند.

### مشخصات فنی
- **Python**: 3.12
- **Django**: 5.2.14 (LTS)
- **مدیریت وابستگی**: uv
- **دیتابیس توسعه**: SQLite
- **زبان پیش‌فرض**: انگلیسی (en-us)
- **Timezone**: Asia/Tehran
- **احراز هویت**: django-allauth
- **API**: Django REST Framework + drf-spectacular

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

### ۳. اعمال Migrationها و ایجاد کاربر ادمین

```bash
python manage.py migrate
python manage.py createsuperuser
```

### ۴. اجرای سرور

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
├── .env                            ← متغیرهای محیطی
├── .editorconfig                   ← تنظیمات ویرایشگر
├── .gitignore                      ← فایل‌های نادیده‌گرفته‌شده توسط Git
├── .gitattributes                  ← ویژگی‌های Git
├── manage.py                       ← اسکریپت مدیریت Django
├── pyproject.toml                  ← مدیریت وابستگی‌ها و تنظیمات ابزارها
├── uv.lock                         ← قفل وابستگی‌های uv
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
| `/api/auth-token/` | دریافت توکن احراز هویت |
| `/api/schema/` | اسکیمای API |
| `/api/docs/` | مستندات Swagger |

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