# نقشه راه CI/CD بعدی

**وضعیت:** طرح برای اجرا در آینده — پیاده‌سازی نشده.  
**پلن اجرایی (چک‌باکس و Verify):** [`ai-documents/features/cicd-next/implementation_plan.md`](../../ai-documents/features/cicd-next/implementation_plan.md)  
**قفل‌ها و خارج از محدوده:** [`ai-documents/features/cicd-next/feature_spec.md`](../../ai-documents/features/cicd-next/feature_spec.md)

نسخهٔ فعلی محصول روی چابکان تمام است: [`cicd-chabokan-prod`](../../ai-documents/features/cicd-chabokan-prod/implementation_plan.md) (گام ۱–۱۳). مسیر آموزشی زنده: [`DEVELOPMENT_TO_DEPLOY.md`](./DEVELOPMENT_TO_DEPLOY.md).

این فایل همان نقشه را برای انسان جمع می‌کند. اجرا یعنی رفتن سراغ پلن `cicd-next`، یک گام در هر نشست، با GitFlow روی `doion` و پرامپت Studio برای UI.

---

## الان چه دارید

```text
PR develop  →  Ruff + pytest (Postgres)
Studio main →  CI فرانت + E2E غیرمسدودکننده در doion
Release     →  تگ SemVer + ایمیج GHCR (محصول را عوض نمی‌کند)
CD Backend  →  تأیید شما → بیلد سورس Django روی چابکان
CD Product  →  تأیید شما از شاخه product → Static روی royasoft.dev
CD Demo     →  خودکار mock؛ محصول نیست
```

شکاف اصلی: **تگ ایمیج می‌سازید اما سرور هنوز از سورس/باندل CLI بیلد می‌کند.**

---

## فازها

| فاز | نام | چه عوض می‌شود | چه عوض نمی‌شود |
|-----|-----|----------------|-----------------|
| **A** | سخت‌کاری | CORS/دامنه، required CI روی `develop`، Node اکشن‌ها، `chabok.json` محصول | مدل CD، نوع سرویس Static |
| **B** | ایمنی دکمه | GitHub Environment برای CD | pull ایمیج |
| **C** | آرتیفکت = سرور | API (و در صورت تصمیم، SPA) از GHCR | دمو mock؛ تأیید دستی deploy |
| **D** | کیفیت انتشار | پین UI قبل از تگ؛ E2E به‌عنوان gate **انتشار** نه هر PR | Playwright داخل Vue |
| **E** | تأمین و «چه خبر» | پین SHA اکشن‌ها؛ changelog داخل اپ؛ HSTS آرام | تگ روی ریپوی UI |

ترتیب پیشنهادی: A → B → تصمیم پنل → C → D → E. اگر فقط یک جهش: **حفاظت `develop` (A2) و بعد pull ایمیج API (C)** پس از اینکه چابکان GHCR را بکشد.

---

## تصمیم‌هایی که باید شما بگویید (قبل از فاز C)

1. آیا `chequeyar-back` می‌تواند ایمیج خصوصی `ghcr.io/alamalhoda/doion-api` را pull کند؟
2. فرانت محصول **Static** بماند یا دوباره سرویس Docker شود؟
3. برای Environment تولید، علاوه بر Run workflow، reviewer دوم می‌خواهید؟

بدون این سه، Chat نباید نوع سرویس چابکان یا مسیر ایمیج را عوض کند.

---

## نسازید مگر جلسهٔ جدا

- staging  
- deploy با هر merge به `develop` / `product`  
- `git tag` روی `checkyar-googleai`  
- قاطی کردن دمو mock با CD محصول
