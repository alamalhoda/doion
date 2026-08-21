# راهنمای آموزشی: تگ گیت، SemVer و انتشار محصول

**مخاطب:** مالک پروژه که قبلاً از تگ گیت استفاده نکرده.  
**وضعیت:** تگ محصول با workflow [`Release`](../../.github/workflows/release.yml) ساخته می‌شود. تا آن فایل روی `develop` نیاید، دستورهای Actions را اجرا نکنید.

سیاست اجرایی برای Cursor: [`.cursor/skills/semver-release/SKILL.md`](../../.cursor/skills/semver-release/SKILL.md).  
Changelog داخل اپ (آینده): [`PRODUCT_CHANGELOG.md`](./PRODUCT_CHANGELOG.md).

---

## ۱. تگ چیست؟

شاخه (`develop`, `feature/login`) مثل یک نشانگر **متحرک** است: با هر commit جلو می‌رود.

**تگ** یک نام ثابت روی **یک commit مشخص** است. بعد از شش ماه هنوز می‌گویید «`v0.1.0` همان snapshot است»، حتی اگر `develop` خیلی جلوتر رفته باشد.

در این پروژه تگ محصول معمولاً این شکل است: `v0.1.0` یا `v0.1.0-test.1`.

روی GitHub، **Release** همان تگ است به‌علاوهٔ عنوان، تاریخ، و یادداشت انسانی. ایمیج‌های Docker هم باید **همان رشته** را به‌عنوان تگ ایمیج داشته باشند تا «نسخهٔ N» مبهم نباشد.

```text
commit abc123  ←  تگ v0.1.0-test.1
                ←  GitHub Release v0.1.0-test.1
                ←  ghcr.io/…/doion-api:v0.1.0-test.1
                ←  ghcr.io/…/chequeyar-front:v0.1.0-test.1
```

---

## ۲. چه زمانی تگ بزنیم؟ چه زمانی نزنیم؟

| بزنید | نزنید |
|--------|--------|
| می‌خواهید یک بستهٔ قابل بازگشت داشته باشید (ایمیج + یادداشت) | هر کامیت روی `feature/*` |
| feat/fix به `develop` رسیده و می‌خواهید «نسخه» اعلام کنید | هر PR اسنادی / rule / CI-only |
| UI قابل‌دیدن کاربر به شاخهٔ `product` رسیده و می‌خواهید با API یک شماره داشته باشید | هر push استودیو به `main` |
| قبل از deploy تأییدشده (گام‌های بعدی CD) | اصلاح غلط املایی |

قانون ساده: **تگ = انتشار آرتیفکت، نه ذخیرهٔ کار روزانه.**

---

## ۳. SemVer به زبان ساده

قالب: `MAJOR.MINOR.PATCH` — تگ گیت با پیشوند `v`.

| تغییر | مثال ورودی workflow | تگ گیت |
|--------|---------------------|--------|
| آزمایش اول، بدون دست زدن به سرور زنده | `0.1.0-test.1` | `v0.1.0-test.1` (prerelease) |
| باگ، قرارداد API عوض نشده | `0.1.1` | `v0.1.1` |
| قابلیت جدید سازگار | `0.2.0` | `v0.2.0` |
| ناسازگاری `/api/v1/` | `1.0.0` یا major بعدی | فقط با آگاهی |

پسوند `-test.1` یعنی «این را به کاربران محصول وصل نکن». اگر تگ اشتباه بود، همان را پاک/جابه‌جا نکنید؛ `test.2` بزنید.

یک شماره برای **کل محصول** است: Django و Vue جدا نسخه‌گذاری نمی‌شوند.

---

## ۴. مسیر درست در این ریپو (نه `git tag` روی فیچر)

دستی `git tag` روی `feature/*` ایمیج GHCR نمی‌سازد و ممکن است با workflow تداخل کند (تگ تکراری).

### پیش‌نیاز

1. تغییرات بک‌اند با PR روی `develop` باشند.
2. اگر SPA هم در این نسخه است: SHA فرانت روی `product` باشد و [`e2e/ui-pin`](../../e2e/ui-pin) همان SHA را داشته باشد.
3. فایل `.github/workflows/release.yml` روی همان ref که اجرا می‌کنید وجود داشته باشد.

### اجرا (بعد از آمدن workflow روی `develop`)

از UI: GitHub → **Actions** → **Release** → **Run workflow** → شاخه `develop` → نسخه مثلاً `0.1.0-test.1`.

از ترمینال:

```bash
gh workflow run Release --ref develop -f version=0.1.0-test.1
```

در چت Cursor می‌توانید بگویید: «تگ بزن» یا «Release روی develop اجرا کن»؛ Skill نسخه پیشنهاد می‌کند و **بدون تأیید شما** dispatch نمی‌کند.

### بعد از موفقیت

- [Releases ریپوی doion](https://github.com/alamalhoda/doion/releases)
- پکیج‌های GHCR: `doion-api` و `chequeyar-front` با همان تگ
- این مرحله **سرویس چابکان را عوض نمی‌کند**

گلوله‌های changelog (متن PR بک‌اند + گلوله‌های Studio) را در یادداشت همان Release، بخش Backend / Frontend بگذارید.

---

## ۵. بک‌اند در برابر فرانت

```text
بک‌اند (doion)
  feature → PR → develop → (اختیاری) Release روی همان SHA

فرانت (checkyar-googleai)
  Studio → main → PR به product
  Cursor تگ نمی‌زند
  همان Release دویون SPA را از e2e/ui-pin می‌سازد
```

تگ روی ریپوی UI لازم نیست و از Cursor ممنوع است. شاخهٔ `product` را حذف نکنید؛ خط تولید فرانت است نه یک تگ.

---

## ۶. دیدن تگ‌ها (آشنایی با گیت)

```bash
git fetch origin --tags
git tag -l 'v*'
git show v0.1.0-test.1
```

روی GitHub: سمت راست صفحهٔ ریپو → **Releases**، یا `Code` → منوی شاخه‌ها → تب **Tags**.

---

## ۷. اشتباه‌های رایج

| کار | چرا بد است |
|-----|------------|
| `git tag` روی فیچر و `git push --tags` به‌عنوان انتشار | ایمیج و Release هماهنگ نمی‌شوند |
| تگ روی هر merge به `develop` | نویز؛ SemVer بی‌معنی می‌شود |
| `--force` روی تگ منتشرشده | کسانی که ایمیج کشیده‌اند گم می‌شوند |
| فراموش کردن bump پین UI | ایمیج فرانت SHA قدیمی می‌سازد |
| انتظار اینکه تگ خودش چابکان را به‌روز کند | CD جدا است (تأیید مالک) |

---

## ۸. نقشهٔ اسناد

| سند | نقش |
|-----|-----|
| **همین فایل** | آموزش انسان |
| [`PRODUCT_CHANGELOG.md`](./PRODUCT_CHANGELOG.md) | قرارداد نمایش «چه خبر» داخل اپ (هنوز پیاده نشده) |
| [`.cursor/skills/semver-release/SKILL.md`](../../.cursor/skills/semver-release/SKILL.md) | دستور کار Cursor هنگام تگ |
| [`.cursor/skills/ai-studio-ui-fix-loop/SKILL.md`](../../.cursor/skills/ai-studio-ui-fix-loop/SKILL.md) | بذر changelog از Studio؛ یادآوری تگ بعد از `product` |
| [`PRODUCTION_CHABOKAN_DEPLOY.md`](./PRODUCTION_CHABOKAN_DEPLOY.md) | استقرار زنده؛ جدا از ساخت تگ |
