---
id: CY-001-a
parent: CY-001
status: draft
scope: BACKEND-ONLY
capability_types:
  - API / SERVICE
  - DATA LAYER
blocked_by: []
impl_path: null
updated: 2026-08-30
---

# CY-001-a — آداپتر SMS واقعی پشت اینترفیس موجود

## معرفی و هدف

جایگزینی stub `send_sms` با ارائه‌دهندهٔ پیکربندی‌شده، بدون تغییر قرارداد دامنهٔ اعلان. وندار / یوآیدی / فراشناسا / فینوتک در پژوهش هویت **پیامک نیستند**؛ vendor جدا لازم است.

## مجوز

ارث از CY-001. ابلاغ OTP مجوز بانکی نمی‌خواهد.

## نیازمندی‌ها و پیش‌نیازها

- اینترفیس فعلی `doion.integrations` و مدل `SMSLog`.
- انتخاب و قرارداد vendor پیامک: [`vendor-landscape.md`](../../../vendor-landscape.md) بخش ۲.۴ (هنوز باز).
- Secret فقط از env.

## سناریو (کاربر و پلتفرم)

سیستم OTP/اعلان را از همان نقطهٔ فراخوانی فعلی می‌فرستد. در production متن پیام در لاگ نیست. قطع vendor → خطا برای فراخواننده + ردیف لاگ شکست، نه چاپ OTP.

## شرایط پذیرش

- [ ] با فلگ خاموش، رفتار stub فعلی حفظ می‌شود.
- [ ] با فلگ روشن، ارسال واقعی رخ می‌دهد و `SMSLog` وضعیت موفقیت/شکست دارد.
- [ ] کلید API در ریپو یا لاگ ظاهر نمی‌شود.

## User Story (برای start-prompt)

```text
Feature Scope: BACKEND-ONLY
Capability Types: API / SERVICE · DATA LAYER

User Story:
به عنوان پلتفرم
می‌خواهم SMS از ارائه‌دهندهٔ پیکربندی‌شده پشت اینترفیس فعلی send_sms ارسال شود
تا OTP در production در لاگ چاپ نشود و اعلان واقعی برسد.

Additional Context:
- ریپو: بک‌اند doion؛ UI لمس نمی‌شود
- ریل تسویه: n/a
- خارج از محدودهٔ این برش: KYC، انتخاب vendor هویت
- اسناد والد: docs/capability-roadmap/capabilities/CY-001-live-kyc-sms-adapters/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
- انتخاب vendor: docs/capability-roadmap/vendor-landscape.md بخش ۲.۴ + پرامپت تحقیق همان فایل؛ دامنه را قفل نکن
```
