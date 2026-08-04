# Backend Demo, Seed & Data Modes  
# دمو، Seed و حالت‌های داده در بک‌اند

**As of:** 2026-08-02  
**Scope:** فقط بک‌اند `doion`. Mock فرانت (`VITE_USE_MOCK`) جداگانه در UI فعال و در [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md) توضیح داده شده است.

## خلاصه (فارسی)

| مفهوم | در بک‌اند؟ | معنی |
|--------|------------|------|
| **Mock API / شبیه‌ساز داخل‌پردازه‌ای** | **خیر** | برخلاف UI، Django پشت یک فلگ پاسخ جعلی به API نمی‌دهد. Endpointها واقعاً به ORM و سرویس‌ها می‌زنند. |
| **دادهٔ دمو / Seed** | **بله** | دستور `manage.py seed_demo` داخل یک دیتابیس **واقعی** کاربر، آگهی و یک match نمونه می‌سازد. |
| **Stub برای سیستم‌های خارجی** | **بله (محدود)** | بعضی یکپارچه‌سازی‌ها عمداً stub هستند (مثل ارسال SMS یا فرمول قیمت‌گذاری)، ولی مسیر کد Django واقعی است. |
| **فایل جدا `db.demo.sqlite3`** | **بله (لوکال)** | با `DJANGO_DEMO_DATABASE=1` در `local.py` فعال می‌شود. برای **چابکان**: به‌جای SQLite، Postgres جدا + `seed_demo` توصیه می‌شود. |

### `$DEMO_SEED_PASSWORD` چیست؟

این یک **متغیر محیطی پیشنهادی** (اختیاری) است؛ خود جنگو آن را خودکار نمی‌خواند مگر شما آن را به دستور بدهید.

- **هدف:** یک رمز عبور **ثابت و قابل تکرار** برای همهٔ کاربران دمو (`holder1`, `investor1`, `moderator1`, `admin1`) تا بتوانید هر بار با همان رمز لاگین کنید یا در اسکریپت/E2E استفاده کنید.
- **نحوهٔ استفاده:**

```bash
# در شل (یا داخل backend/.env فقط برای راحتی خودتان؛ در production نگذارید)
export DEMO_SEED_PASSWORD='MyLocalDemoPass1'

python manage.py seed_demo --password "$DEMO_SEED_PASSWORD"
```

- **رمز کاربران دمو چه می‌شود؟**
  - اگر `--password ...` بدهید → **همان مقدار** برای **همه** کاربران دمو set می‌شود.
  - اگر `--password` ندهید → دستور یک رشتهٔ تصادفی ۱۲ کاراکتری می‌سازد، روی همهٔ کاربران دمو اعمال می‌کند، و **همان را در خروجی ترمینال چاپ می‌کند**. باید آن را از لاگ کپی کنید؛ در غیر این صورت رمز را نمی‌دانید.
- **رمز پیش‌فرض hard-code در ریپو وجود ندارد** (عمدی، به‌خاطر سیاست secret). برای کار روزمره محلی، `DEMO_SEED_PASSWORD` را خودتان انتخاب کنید.

نمونه لاگین بعد از seed با رمز ثابت:

| Username | Password |
|----------|----------|
| `holder1` | مقدار `$DEMO_SEED_PASSWORD` (یا همان رمزی که در خروجی چاپ شد) |
| `investor1` | همان |
| `moderator1` | همان |
| `admin1` | همان |

---

## Short answer (EN)

| Concept | Backend? | What it means |
|---------|----------|---------------|
| **Mock API / in-process simulator** | **No** | Unlike the UI, Django does **not** fake REST responses behind a flag. Endpoints hit the real ORM and business services. |
| **Demo / seed data** | **Yes** | `manage.py seed_demo` fills a real database with holders, investors, listings, and a sample match (via domain factories). |
| **Stubs for external systems** | **Yes (limited)** | Some integrations are intentionally stubbed (e.g. SMS send, pricing suggestion formula) but still run through real Django code paths. |
| **Separate `db.demo.sqlite3`** | **Yes (local)** | Toggle with `DJANGO_DEMO_DATABASE=1` in `local.py`. For Chabokan demos prefer a separate Postgres + `seed_demo`, not SQLite. |

---

## فایل‌های دیتابیس محلی

| فایل | Settings | کاربرد |
|------|----------|--------|
| `backend/db.sqlite3` | `config.settings.local` | دیتابیس پیش‌فرض **توسعه محلی**. |
| `backend/test_db.sqlite3` | `config.settings.test` | دیتابیس pytest (gitignore). موقت و مخصوص تست خودکار. |
| `backend/db.demo.sqlite3` | `config.settings.local` + `DJANGO_DEMO_DATABASE=1` | دیتابیس جدا برای دمو لوکال (gitignore). بخش [دیتابیس دمو لوکال](#دیتابیس-دمو-لوکال-dbdemosqlite3). |

Production / چابکان از PostgreSQL با `DATABASE_URL` استفاده می‌کند، نه این فایل‌های SQLite.

---

## جریان پیشنهادی دمو محلی (بک‌اند + UI واقعی)

روش توصیه‌شده برای دمو بدون دست زدن به `db.sqlite3` شخصی:

```bash
cd backend
source .venv/bin/activate   # یا: uv run …

export DJANGO_DEMO_DATABASE=1
export DEMO_SEED_PASSWORD='MyLocalDemoPass1'   # اختیاری ولی توصیه‌شده

python manage.py migrate
python manage.py seed_demo --reset --password "$DEMO_SEED_PASSWORD"
python manage.py runserver
```

اگر عمداً می‌خواهید روی همان DB روزمره seed کنید، `DJANGO_DEMO_DATABASE` را set نکنید (یا `=0`).

سپس UI فعال را به API واقعی وصل کنید:

```env
VITE_USE_MOCK=false
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

علاوه بر کاربران دمو، `seed_demo` این fixtureهای پایدار را هم می‌سازد (برای دمو دستی و E2E critical-path):

| نوع | تعداد / شناسه پایدار | کاربرد |
|-----|----------------------|--------|
| آگهی `published` | ۲۲ عدد با سریال `2000…0001` … `2000…0022` | pagination مارکت‌پلیس (`PAGE_SIZE=20` → صفحه ۲) |
| آگهی `pending_moderation` | ۱۲ عدد با سریال `3000…0001` … `3000…0012` | صف نظارت + pagination جدول UI (`pageSize=10`) |
| آگهی `rejected` | ۱ عدد سریال `4000…0001` | وضعیت ردشده |
| Match `pending` | روی سریال `2000…0001` (`investor1` → `holder1`) | E2E accept-match |
| Express target | سریال `2000…0022` بدون match از `investor1` | E2E express-interest |
| Notification (holder1) | ۱۲ ردیف unread (`status=sent`) | E2E mark-read + pagination نوتیف |

نکته: `created_at` آگهی‌های seed به ۲ روز قبل backdate می‌شود تا سقف ۱۰ آگهی/روز برای تست create باقی بماند.

جزئیات فلگ‌ها: [`backend/README.md`](../../backend/README.md) (بخش Seed دمو). E2E: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md).

---

## بک‌اند معادل `VITE_USE_MOCK` ندارد

### Mock فرانت (ریپوی UI)

- فلگ: `VITE_USE_MOCK`
- رفتار: کلاینت axios ممکن است بدون زدن به Django به **شبیه‌ساز داخل مرورگر** برود.
- کاربرد: دمو در AI Studio / کار آفلاین UI.
- **جایگزین قرارداد API یا تست بک‌اند نیست.**

### «شبیه‌سازی» سمت بک‌اند

به‌جای ساختن حالت Mock سراسری برای API:

1. **دیتابیس seedشده** (`seed_demo`) — ترجیح برای QA دستی و E2E آینده روی `/api/v1/`.
2. **Factory در تست** (`doion/<app>/factories.py`) — SSOT برای pytest؛ همان‌ها به `seed_demo` هم سرویس می‌دهند.
3. **Stub یکپارچه‌سازی** — مثلاً SMS یا pricing: endpoint واقعی، سرویس خارجی جعلی.

یک setting جنگو که برای همهٔ APIها JSON آماده برگرداند اضافه نکنید؛ از `MASTER_API_CONTRACT.md` منحرف می‌شود و باگ را پنهان می‌کند.

---

## دیتابیس دمو لوکال (`db.demo.sqlite3`)

### چرا جدا شد؟

- `seed_demo --reset` کاربران دمو و ردیف‌های وابسته را در **همان دیتابیس فعلی** پاک می‌کند.
- اگر در `db.sqlite3` دادهٔ شخصی/آزمایشی هم نگه داشته باشید، reset ممکن است غافلگیرکننده باشد.
- با `DJANGO_DEMO_DATABASE=1` دمو روی فایل جدا می‌رود و DB روزمره دست‌نخورده می‌ماند.

### وضعیت فعلی (پیاده‌سازی‌شده)

- در `config/settings/local.py`:
  - `DJANGO_DEMO_DATABASE` خالی / `False` / `0` → `db.sqlite3`
  - `DJANGO_DEMO_DATABASE=True` / `1` → `db.demo.sqlite3`
- `DJANGO_SETTINGS_MODULE` همان `config.settings.local` می‌ماند.
- `db.demo.sqlite3` در `backend/.gitignore` است.
- بدون `--reset`، `seed_demo` تقریباً **idempotent** است (بر اساس username و شماره صیاد).
- Migration `sites.0003` فقط روی PostgreSQL sequence را sync می‌کند؛ روی SQLite دیگر با خطای `django_site_id_seq` fail نمی‌شود (لازم برای `db.demo.sqlite3` تازه).

```bash
# توسعه عادی
unset DJANGO_DEMO_DATABASE   # یا =0
python manage.py runserver

# دمو محلی جدا
export DJANGO_DEMO_DATABASE=1
python manage.py migrate
python manage.py seed_demo --reset --password "$DEMO_SEED_PASSWORD"
python manage.py runserver
```

برای آماده‌سازی خودکار همان DB دمو قبل از smoke E2E: [`../../e2e/scripts/prepare-backend.sh`](../../e2e/scripts/prepare-backend.sh) (جزئیات: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)).

نمونه در `.env` لوکال (اختیاری):

```env
DJANGO_DEMO_DATABASE=True
DEMO_SEED_PASSWORD=MyLocalDemoPass1
```

### دمو روی چابکان / محیط محصول — الان چه امکان دارد؟

**الان به‌صورت امن و پشتیبانی‌شده: SQLite دمو روی سرویس production چابکان پیشنهاد/پیکربندی نشده است.**

شواهد فعلی کد:

- `config.settings.local` → SQLite لوکال (`db.sqlite3` یا `db.demo.sqlite3`).
- `config.settings.production` → `DATABASE_URL` (معمولاً **Postgres**) + Redis/کش؛ برای استقرار واقعی طراحی شده.
- `seed_demo` روی **هر** دیتابیسی که settings فعلی به آن وصل است کار می‌کند (Postgres هم شامل می‌شود)، ولی این به معنی «SQLite روی چابکان» نیست.

| سناریو | الان ممکن؟ | توصیه |
|--------|------------|--------|
| لوکال: `db.sqlite3` + `seed_demo` | بله | توسعه روزمره |
| لوکال: `db.demo.sqlite3` با `DJANGO_DEMO_DATABASE=1` | بله | جداسازی دمو لوکال |
| چابکان: **Postgres جدا (staging/demo)** + `seed_demo` | بله از نظر کد (migrate + seed روی همان `DATABASE_URL`) | **بهترین گزینه برای دمو موقت به مشتری** |
| چابکان production: عوض کردن DB به SQLite فقط برای دمو | از نظر تئوری با دستکاری `DATABASE_URL=sqlite:///...` ممکن است، ولی **خطرناک و توصیه نمی‌شود** | نکنید |

چرا SQLite روی چابکان/production بد است؟

1. **چند worker / Gunicorn:** SQLite برای نوشتن همزمان ضعیف است (قفل فایل).
2. **دیسک موقت:** بسیاری از PaaSها فایل سیستم را ephemeral می‌دانند؛ با redeploy دیتای SQLite از بین می‌رود.
3. **امنیت/پایداری:** settings production فرض Postgres، SSL، Redis و … دارد؛ قاطی کردن SQLite با آن محیط، مسیر خطای پنهان می‌سازد.
4. **تداخل با داده واقعی:** اگر روی همان سرویس production seed کنید، دادهٔ واقعی و دمو قاطی می‌شوند.

### اگر دمو موقت روی چابکان می‌خواهید چه کار کنید؟ (توصیه)

**گزینه A — Staging/Demo app جدا (ترجیح)**

1. یک سرویس/اپ جدا روی چابکان (یا همان اپ با DB جدا) با Postgres اختصاصی.
2. `DJANGO_SETTINGS_MODULE=config.settings.production` و `DATABASE_URL` همان Postgres دمو.
3. یک‌بار: `migrate` سپس `seed_demo --password "$DEMO_SEED_PASSWORD"`.
4. UI را موقتاً به همان API دمو بزنید (`VITE_USE_MOCK=false`).
5. بعد از ارائه، سرویس/DB دمو را خاموش یا reset کنید.

**گزینه B — همان Postgres staging بدون SQLite**

- فقط `seed_demo --reset` روی staging (با آگاهی که کاربران دمو پاک/بازنویسی می‌شوند).
- نیازی به SQLite نیست.

**گزینه C — فقط لوکال SQLite دمو + تونل/اسکرین**

- برای ارائه سریع روی لپ‌تاپ: `DJANGO_DEMO_DATABASE=1` + `seed_demo` + UI لوکال.
- برای مشتری ریموت، گزینه A بهتر است.

### اگر بعداً اصرار به SQLite روی سرور باشد (توصیه نمی‌شود)

حداقل این کارها لازم است و باز هم fragile است:

1. مسیر پایدار و قابل‌نوشتن برای فایل SQLite روی سرور (volume پایدار، نه فقط `/tmp`).
2. یک worker تکی (یا جلوگیری از نوشتن موازی).
3. settings صریح مثل `config.settings.demo_host` جدا از production — نه قاطی کردن با production واقعی.
4. gitignore / عدم commit فایل DB؛ migrate + seed در release/start.
5. مستند واضح: «این محیط دمو است، داده persistence ندارد مگر volume وصل باشد.»

**جمع‌بندی محصولی:** برای چابکان، دمو = **Postgres جدا + `seed_demo`**. SQLite دمو را برای **لوکال** با `DJANGO_DEMO_DATABASE` نگه دارید.

---

## Follow-ups (بعداً — خارج از PR فعلی)

این فهرست عمداً برای بعد از merge branch تست/دمو نگه داشته شده تا فراموش نشود. چک‌لیست عملیاتی در [`backend/TODO.md`](../../backend/TODO.md) هم هست.

| اولویت | کار | دامنه |
|--------|-----|--------|
| انجام‌شده | CI: `pytest` روی PR/push به `develop` (`.github/workflows/ci-backend.yml`) | automation |
| متوسط | Staging/demo چابکان با Postgres + `seed_demo` | ops |
| متوسط | `order_by` برای رفع warningهای pagination در تست/API | quality |
| پایین‌تر | پوشش بیشتر matching views / document edge cases | tests |
| جدا | E2E smoke harness در `e2e/` (شروع‌شده؛ runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)) — critical path + CI هنوز باز | cross |
| جدا | تست‌های بیشتر UI در AI Studio (نه mock به‌جای قرارداد)؛ پرامپت selector: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md) | frontend |

---

## Related docs

- API contract SSOT: [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md)
- Active UI + when to disable mock: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md)
- Backend commands / factories: [`backend/README.md`](../../backend/README.md)
- Backend TODO / follow-ups checklist: [`backend/TODO.md`](../../backend/TODO.md)
- E2E runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)
- AI Studio E2E prep prompt: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md)
