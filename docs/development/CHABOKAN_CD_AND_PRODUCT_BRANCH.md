# راهنمای آموزشی: استقرار محصول روی چابکان (CD)

**مخاطب:** مالک پروژه که این مسیر برایش تازه است.  
**هدف:** بدانی تگ، شاخهٔ `product`، و دکمهٔ **Run workflow** چه فرقی دارند؛ چه کاری را Cursor انجام می‌دهد؛ و **کدام دکمه را فقط تو باید بزنی.**

تگ و SemVer جداست: [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md).  
جزئیات پنل و env: [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md).

---

## ۱. دو ریپو، دو سرویس زنده

| چیز | کجاست | سرویس چابکان |
|-----|--------|----------------|
| API (Django) | ریپوی [doion](https://github.com/alamalhoda/doion) | `chequeyar-back` |
| UI (Vue) | ریپوی [checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai) | `chequeyar-front` |
| دمو mock | همان ریپوی UI، workflow دیگر | `chequeyar-front-demo` |

مرورگر کاربر به فرانت می‌رود؛ فرانت به `https://chequeyar-back.chbkn.dev/api/v1` حرف می‌زند. این دو سرویس **جدا** به‌روز می‌شوند.

Studio فقط به `checkyar-googleai` پوش می‌کند. Cursor سورس UI را پوش نمی‌کند.

---

## ۲. چهار workflow که شبیه هم به نظر می‌رسند

| نام در Actions | ریپو | کی اجرا می‌شود | سرور زنده؟ |
|----------------|------|-----------------|------------|
| **Release** | doion | دستی؛ ورودی نسخه | خیر — فقط تگ + ایمیج GHCR |
| **CD Backend** | doion | دستی؛ ورودی تگ | **بله** — `chequeyar-back` |
| **CD Product (Chabokan live)** | checkyar-googleai | دستی؛ شاخه را تو انتخاب می‌کنی | **بله** — `chequeyar-front` |
| **CD Demo (Chabokan mock)** | checkyar-googleai | خودکار روی هر push به `main` | فقط دمو mock |

قانون: **تگ ≠ استقرار.** `v0.1.0-test.1` الان وجود دارد ولی API/SPA محصول را عوض نکرده مگر CD را بزنی.

دمو mock با هر پوش Studio به `main` خودش به‌روز می‌شود. این طبیعی است و به معنی به‌روز شدن `chequeyar-front` نیست.

---

## ۳. شاخه‌ها به زبان ساده

**doion**

- `develop` = محل ادغام کار روزانه (با PR)
- تگ `v0.1.0-test.1` = یک عکس ثابت از `develop` در لحظهٔ Release

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

## ۴. الان کجا هستیم؟ (۲۱ اوت ۲۰۲۶)

انجام شده:

- تگ آزمایشی [`v0.1.0-test.1`](https://github.com/alamalhoda/doion/releases/tag/v0.1.0-test.1)
- workflow **CD Backend** روی `develop` (هنوز Run نشده)
- workflow **CD Product** روی `main` با SHA `bb2b72b` (هنوز Run نشده؛ روی `product` نیست تا PR ادغام شود)
- پین E2E: [doion#49](https://github.com/alamalhoda/doion/pull/49)

انجام نشده (محیط زنده محصول):

- اجرای **CD Backend**
- Merge `main` → `product`
- اجرای **CD Product** روی `product`

---

## ۵. کارهایی که تو در GitHub می‌کنی

Cursor می‌تواند PR باز کند و چک‌ها را گزارش کند. **Merge** روی GitHub و **Run workflow** برای سرویس زنده را تو تأیید می‌کنی (یا صریح در چت می‌گویی «merge کن / CD را بزن»).

### الف) PRهای doion (بدون تغییر سرور)

1. [PR 49](https://github.com/alamalhoda/doion/pull/49) — پین UI برای E2E. Merge اگر Checks سبز است.
2. [PR 50](https://github.com/alamalhoda/doion/pull/50) — یادداشت پلن + این راهنما. Merge اگر Checks سبز است.

روی صفحهٔ PR: **Merge pull request** → **Confirm merge**.

### ب) PR فرانت `main` → `product` (هنوز سرور زنده نیست)

بعد از باز شدن PR در checkyar-googleai:

1. صبر کن Checks (CI) سبز شود.
2. Merge کن. شاخهٔ `product` فایل `cd-product.yml` را می‌گیرد.
3. هنوز `chequeyar-front` عوض نمی‌شود تا گام د را بزنی.

### ج) راز `CHABOKAN_TOKEN` روی doion

دموی فرانت از قبل با همین نام راز کار می‌کند. **CD Backend** از راز **ریپوی doion** می‌خواند.

یک‌بار چک کن: [doion → Settings → Secrets](https://github.com/alamalhoda/doion/settings/secrets/actions) باید `CHABOKAN_TOKEN` داشته باشد (همان توکن API چابکان). مقدار را در چت نفرست.

اگر نباشد، CD Backend با پیام خالی بودن راز قرمز می‌شود؛ سرویس عوض نمی‌شود.

### د) استقرار API (سرور زنده)

فقط وقتی خواستی `chequeyar-back` همان کد تگ آزمایشی را بگیرد:

1. [doion Actions → CD Backend](https://github.com/alamalhoda/doion/actions/workflows/cd-backend.yml)
2. **Run workflow**
3. Branch: `develop`
4. `tag`: `v0.1.0-test.1`
5. Run. صبر کن job سبز شود.

یا در چت بگو: «CD Backend را با v0.1.0-test.1 بزن».

### ه) استقرار SPA (سرور زنده)

فقط **بعد از** merge شدن `main` به `product`:

1. [checkyar-googleai Actions → CD Product](https://github.com/alamalhoda/checkyar-googleai/actions)
2. workflow **CD Product (Chabokan live)**
3. **Run workflow**
4. Branch را **`product`** بگذار (نه `main`)
5. Run.

یا در چت بگو: «CD Product را روی product بزن».

ترتیب پیشنهادی: اول API (د)، بعد SPA (ه)، تا فرانت به API تگ‌شده حرف بزند. اجباری نیست اگر فعلاً فقط یکی را می‌خواهی.

---

## ۶. اگر job قرمز شد

Check ناموفق است؛ چابکان rollback خودکار ندارد.

- API: دوباره **CD Backend** را با **آخرین تگی که می‌دانی خوب کار می‌کرد** اجرا کن.
- SPA: دوباره **CD Product** را روی همان SHA/`product` قبلی که خوب بود اجرا کن.

تگ را force نکن؛ اگر تگ اشتباه بود نسخهٔ بعدی (`test.2`) بزن.

---

## ۷. کارهایی که نکن

| کار | چرا |
|-----|-----|
| Run workflow روی `main` برای CD Product | خط تولید `product` است |
| انتظار اینکه Merge PR خودش چابکان را عوض کند | فقط git عوض می‌شود |
| دست زدن به **CD Demo** | دمو mock است |
| `git tag` روی کلون UI | نسخهٔ محصول تگ doion است |
| `seed_demo --reset` روی دیتابیس واقعی | دادهٔ کاربر پاک می‌شود |

---

## ۸. نقشهٔ اسناد

| سند | نقش |
|-----|-----|
| **همین فایل** | آموزش انسان برای CD و `product` |
| [`GIT_TAGS_AND_RELEASES.md`](./GIT_TAGS_AND_RELEASES.md) | آموزش تگ / Release / GHCR |
| [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md) | env پنل و معماری سرویس‌ها |
| [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md) | Studio یک‌طرفه؛ `main` در برابر `product` |
