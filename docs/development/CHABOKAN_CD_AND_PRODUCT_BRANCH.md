# راهنمای آموزشی: استقرار محصول روی چابکان (CD)

**مخاطب:** مالک پروژه که این مسیر برایش تازه است.  
**هدف:** بدانی تگ، شاخهٔ `product`، و دکمهٔ **Run workflow** چه فرقی دارند؛ چه کاری را Cursor انجام می‌دهد؛ و **کدام دکمه را فقط تو باید بزنی.**

تگ و SemVer جداست: [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md).  
جزئیات پنل و env: [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md).

---

## ۱. دو ریپو، سرویس‌های چابکان، دامنه

| چیز | سرویس چابکان (`-s`) | آدرس کاربر |
|-----|---------------------|------------|
| API (Django) | `chequeyar-back` | https://chequeyar-back.chbkn.dev |
| SPA محصول | `chequeyar-front` (**Static**) | **https://royasoft.dev** — پنل [Yq40OKq](https://hub.chabokan.net/fa/services/detail/Yq40OKq) |
| SPA دمو mock | `chequeyar-front-demo` | **https://royasoftgroup.ir** |
| Postgres | `chequeyar-db` | سایت نیست؛ دیتابیس `chequeyar-back` |

CD همان **نام سرویس** را هدف می‌گیرد، نه دامنه. دامنه فقط برچسب روی همان سرویس است.

مرورگر روی `royasoft.dev` است؛ باندل فعلی API را از `https://chequeyar-back.chbkn.dev/api/v1` می‌زند. در پنل `chequeyar-back` مقدار `CORS_ALLOWED_ORIGINS` باید شامل `https://royasoft.dev` باشد وگرنه مرورگر درخواست را قطع می‌کند.

لینک پنل و جدول کامل: [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md).

Studio فقط به `checkyar-googleai` پوش می‌کند. Cursor سورس UI را پوش نمی‌کند.

---

## ۲. چهار workflow که شبیه هم به نظر می‌رسند

| نام در Actions | ریپو | کی اجرا می‌شود | سرور زنده؟ |
|----------------|------|-----------------|------------|
| **Release** | doion | دستی؛ ورودی نسخه | خیر — فقط تگ + ایمیج GHCR |
| **CD Backend** | doion | دستی؛ ورودی تگ | **بله** — `chequeyar-back` |
| **CD Product (Chabokan live)** | checkyar-googleai | دستی؛ شاخه را تو انتخاب می‌کنی | **بله** — `chequeyar-front` |
| **CD Demo (Chabokan mock)** | checkyar-googleai | خودکار روی هر push به `main` | فقط دمو mock |

قانون: **تگ ≠ استقرار.** تگ فعلی آزمایشی [`v0.1.0-test.2`](https://github.com/alamalhoda/doion/releases/tag/v0.1.0-test.2) است. چابکان عوض نمی‌شود مگر **CD Backend** / **CD Product** را بزنی.

دمو mock با هر پوش Studio به `main` خودش به‌روز می‌شود. این طبیعی است و به معنی به‌روز شدن `chequeyar-front` نیست.

---

## ۳. شاخه‌ها به زبان ساده

**doion**

- `develop` = محل ادغام کار روزانه (با PR)
- تگ `v0.1.0-test.2` = عکس `develop` در لحظهٔ آخرین Release (شامل همگام نقش User/Profile)

**checkyar-googleai**

- `main` = هر چیزی که Studio می‌فرستد (ورودی)
- `product` = خط تولید SPA؛ از `main` خام به `chequeyar-front` deploy نمی‌شود
- برای اینکه `cd-product.yml` روی تولید باشد، باید commitهای `main` با **Pull Request** به `product` بروند

```text
Studio  --push-->  main
                     │
                     │  PR (تو Merge می‌کنی اگر Checks سبز باشد)
                     ▼
                  product  --(Run workflow CD Product)-->  chequeyar-front
```

---

## ۴. الان کجا هستیم؟ (۲۱ اوت ۲۰۲۶، شب)

ویژگی CI/CD چابکان (گام‌های ۱–۱۲) روی محیط زنده **Verify** شده است.

- تگ [`v0.1.0-test.2`](https://github.com/alamalhoda/doion/releases/tag/v0.1.0-test.2) + GHCR؛ **CD Backend** با همین تگ روی `chequeyar-back` اجرا شده (نقش `User`/`Profile` هم‌تراز)
- **CD Product** از `product` به سرویس Static `chequeyar-front` ([royasoft.dev](https://royasoft.dev/))؛ دمو mock جدا روی [royasoftgroup.ir](https://royasoftgroup.ir/)
- پین E2E: `4bcf1a1` ([doion#56](https://github.com/alamalhoda/doion/pull/56))
- Django Users در ادمین فیلد Role دارد؛ SPA از `User.role` می‌خواند

کار محصولی باز (خارج از pipeline): فلگ `show_landing_page` روی API پیش‌فرض خاموش است؛ `/landing` زنده تا روشن شدن فلگ به بازارچه/لاگین می‌رود.

---

## ۵. کارهایی که تو در GitHub می‌کنی

Cursor می‌تواند PR باز کند و چک‌ها را گزارش کند. **Merge** روی GitHub و **Run workflow** برای سرویس زنده را تو تأیید می‌کنی (یا صریح در چت می‌گویی «merge کن / CD را بزن»).

### الف) راز `CHABOKAN_TOKEN`

باید روی **هر دو** ریپو باشد: [doion](https://github.com/alamalhoda/doion/settings/secrets/actions) برای CD Backend؛ [checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai/settings/secrets/actions) برای CD Product/Demo. مقدار را در چت نفرست.

### ب) استقرار API (سرور زنده)

1. اول **Release** با نسخهٔ SemVer جدید (اگر تگ هنوز نیست)
2. [doion Actions → CD Backend](https://github.com/alamalhoda/doion/actions/workflows/cd-backend.yml) → **Run workflow** → Branch `develop` → `tag` مثلاً `v0.1.0-test.2`

یا در چت: «CD Backend را با v0.1.0-test.2 بزن».

### ج) استقرار SPA (سرور زنده)

1. PR سبز `main` → `product` را merge کن
2. [CD Product (Chabokan live)](https://github.com/alamalhoda/checkyar-googleai/actions) → **Run workflow** → Branch **`product`** (نه `main`)

یا در چت: «CD Product را روی product بزن».

ترتیب پیشنهادی وقتی API و SPA هر دو عوض می‌شوند: اول API (ب)، بعد SPA (ج).

---

## ۶. اگر job قرمز شد

Check ناموفق است؛ چابکان rollback خودکار ندارد.

- API: دوباره **CD Backend** را با **آخرین تگی که می‌دانی خوب کار می‌کرد** اجرا کن.
- SPA: دوباره **CD Product** را روی همان SHA/`product` قبلی که خوب بود اجرا کن.

تگ را force نکن؛ اگر تگ اشتباه بود نسخهٔ بعدی (`test.2`) بزن.

---

## ۷. تلهٔ CLI: `chabok.json` برنده‌تر از `-s` است

کد CLI چابکان اگر در ریشهٔ پروژه `chabok.json` با `"service"` باشد، **فلگ `-s` را نادیده می‌گیرد**.

در ریپوی UI فایل committed می‌گوید `chequeyar-front-demo`. بنابراین `chabok deploy -s chequeyar-front` در Actions به **دمو** رفت. لاگ سبز [CD Product #1](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32469027546): `Deployed to chequeyar-front-demo`. پنل `chequeyar-front` استقرار جدید نداشت.

اصلاح: پرامپت [`prompts/06-fix-cd-product-chabok-json.md`](../../ai-documents/features/cicd-chabokan-prod/prompts/06-fix-cd-product-chabok-json.md) — روی runner قبل از deploy، `chabok.json` موقت با `chequeyar-front`؛ فایل git همان دمو بماند.

اثر جانبی run اول: باندل **زنده** ممکن است روی `chequeyar-front-demo` / royasoftgroup.ir نشسته باشد. بعد از فیکس، یک‌بار CD Demo (یا پوش بعدی به `main`) دموی mock را برمی‌گرداند.

---

## ۸. کارهایی که نکن

| کار | چرا |
|-----|-----|
| Run workflow روی `main` برای CD Product | خط تولید `product` است |
| انتظار اینکه Merge PR خودش چابکان را عوض کند | فقط git عوض می‌شود |
| فرض نوع **Vue** برای `chequeyar-front` | سرویس فعلی **Static** است |
| اتصال دامنه قبل از دیدن SPA روی deploy | اول CD Product، بعد دامنه |
| `git tag` روی کلون UI | نسخهٔ محصول تگ doion است |
| `seed_demo --reset` روی دیتابیس واقعی | دادهٔ کاربر پاک می‌شود |

---

## ۹. نقشهٔ اسناد

| سند | نقش |
|-----|-----|
| **همین فایل** | آموزش انسان برای CD و `product` |
| [`DEVELOPMENT_TO_DEPLOY.md`](./DEVELOPMENT_TO_DEPLOY.md) | نقشهٔ آموزشی توسعه تا استقرار |
| [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md) | آموزش تگ / Release / GHCR |
| [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md) | env پنل، دامنهٔ سفارشی، لینک هاب |
| [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md) | Studio یک‌طرفه؛ `main` در برابر `product` |
