# دو مسیر اجرا: روزانه و محصول

این سند منبع یکتای «کجا Django اجرا می‌شود و داده کجاست» است. قرارداد REST (`/api/v1/`) عوض نمی‌شود.

روی مک برای اتصال از **میزبان** به پورت Docker همیشه `localhost` بگذارید نه `127.0.0.1`.

---

## تصویر کلی

| | روزانه (توسعه و تست شما) | محصول (سرور) |
|---|---|---|
| هدف | کدنویسی سریع، reload، pytest | همان ایمیج/تنظیماتی که روی چابکان باید باشد |
| اپ Django | روی **مک** با `uv` و `runserver` | **Gunicorn** داخل ایمیج `backend/Dockerfile` |
| تنظیمات | `config.settings.local` | `config.settings.production` |
| داده | **PostgreSQL در Docker** | **فقط PostgreSQL** (پنل چابکان؛ SQLite ممنوع) |
| Redis | لازم نیست (کش لوکال) | لازم (پنل یا Compose برای امتحان ایمیج) |
| ساخت ایمیج در هر تست | **خیر** | فقط وقتی Dockerfile/`uv.lock`/سورس ایمیج عوض شود |
| اینترنت بعد از بار اول | تقریباً هیچ (لایهٔ Postgres کش شده) | pull اولیهٔ پایهٔ Python/uv یک‌بار |

SQLite بدون Docker هنوز برای همکارانی که Docker نمی‌خواهند معتبر است؛ مسیر توصیه‌شدهٔ روزانهٔ شما Postgres در Docker است.

GitHub Actions (pytest روی PR به `develop`) همیشه Postgres است و به SQLite برنمی‌گردد.

---

## مسیر ۱ — روزانه: Postgres در Docker، اپ روی میزبان

این همان چیزی است که باید هر روز باز کنید. ایمیج API محصول را نمی‌سازد؛ فقط کانتینر سبک Postgres (اولین بار ایمیج `postgres:16` دانلود می‌شود و بعد روی دیسک می‌ماند).

### یک‌بار

از ریشهٔ مونورپو:

```bash
docker compose up -d
```

فقط سرویس `postgres` بالا می‌آید. در `backend/.env`:

```bash
DJANGO_SETTINGS_MODULE=config.settings.local
DATABASE_URL=postgres://doion@localhost:5432/doion
```

سپس یک‌بار:

```bash
cd backend
source .venv/bin/activate
uv sync
python manage.py migrate
```

### هر روز

```bash
docker compose up -d
cd backend && source .venv/bin/activate
python manage.py runserver
```

API: [http://localhost:8000/](http://localhost:8000/)

تست (همان Postgres؛ Django دیتابیس تست جدا می‌سازد):

```bash
cd backend
source .venv/bin/activate
uv run pytest
```

اگر `DATABASE_URL` پستگرس نباشد، pytest لوکال روی فایل `test_db.sqlite3` می‌ماند. برای تست روزانهٔ هم‌تراز با CI، همان URL پستگرس را بگذارید.

توقف فقط دیتابیس (اختیاری):

```bash
docker compose stop
```

حجم داده در volume با نام `doion_pgdata` می‌ماند تا `docker compose down -v` نزنید.

اگر پورت `5432` روی مک اشغال است، در `docker-compose.yml` سمت چپ را مثلاً `5433:5432` کنید و همان پورت را در `DATABASE_URL` بگذارید.

### چرا این مسیر برای Cursor + Docker سبک است؟

Docker فقط Postgres را نگه می‌دارد. مفسر پایتون، pytest و hot-reload روی میزبان‌اند؛ با هر ذخیره ایمیج دوباره ساخته نمی‌شود و چیزی از اینترنت کشیده نمی‌شود مگر خودتان `--build` بزنید (در این مسیر لازم نیست).

---

## مسیر ۲ — محصول: ایمیج Gunicorn روی سرور

این مسیر «چگونه روی چابکان باید اجرا شود» است، نه جایگزین `runserver`.

- تنظیمات: `config.settings.production` (اگر engine اسکیولایت باشد استارت قطع می‌شود)
- ورود: [`backend/Dockerfile`](../../backend/Dockerfile) + [`backend/docker-entrypoint.sh`](../../backend/docker-entrypoint.sh) → `migrate`، `collectstatic`، Gunicorn
- داده و کش: Postgres و Redis در **پنل** سرویس `chequeyar-back`؛ رازها فقط در پنل
- استقرار از سورس با CLI چابکان یا workflow تأییدشدهٔ **CD Backend** در [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md) است؛ بدون `workflow_dispatch` مالک سرویس زنده عوض نمی‌شود. آموزش تگ/SemVer: [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md)

لوکال **نباید** هر تست را با `docker build` بزنید. ایمیج را وقتی می‌سازید که بخواهید ایمیج محصول را چک کنید یا برای گام انتشار آماده کنید:

```bash
docker build -t doion-api ./backend
```

بعد از بار اول، لایه‌ها کش‌اند؛ `--build` دوباره فقط لایه‌های عوض‌شده را می‌سازد.

---

## امتحان ایمیج محصول روی مک (اختیاری، نه روزانه)

اگر بخواهید همان Dockerfile را با Postgres و Redis کنار هم ببینید (Gunicorn، نه `runserver`):

```bash
# runserver روی 8000 را ببندید
docker compose --profile app up -d --build
```

سپس [http://localhost:8000/](http://localhost:8000/). این استک برای «نزدیک به سرور» است؛ با هر تغییر کد اگر بخواهید داخل ایمیج بیاید باید دوباره `--build` بزنید — برای همین روزانه نیست.

توقف API و Redis (Postgres مسیر روزانه می‌ماند):

```bash
docker compose --profile app stop api redis
```

---

## SQLite بدون Docker (همچنان معتبر)

اگر Compose را روشن نکنید و `DATABASE_URL` با `postgres` شروع نشود، `config.settings.local` از `db.sqlite3` استفاده می‌کند. برای کار روزمرهٔ شما توصیه نمی‌شود؛ برای لپ‌تاپ بدون Docker یا دموی فایل‌محور کافی است.

---

## چک‌لیست سریع

- روزانه: `docker compose up -d` + `uv` + `runserver` / `pytest` + `DATABASE_URL=postgres://doion@localhost:5432/doion`
- محصول روی سرور: Postgres (+ Redis) در پنل، `production`، بدون SQLite؛ ایمیج در `backend/Dockerfile`
- هر روز `docker compose --profile app --build` نزنید
- `seed_demo --reset` روی دیتابیس کاربران محصول نزنید
