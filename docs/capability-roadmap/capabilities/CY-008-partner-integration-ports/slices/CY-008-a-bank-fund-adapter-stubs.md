---
id: CY-008-a
parent: CY-008
status: draft
scope: BACKEND-ONLY
capability_types:
  - API / SERVICE
  - DATA LAYER
  - AUTOMATION
blocked_by: [CY-003-a]
impl_path: null
updated: 2026-08-30
---

# CY-008-a — Port و stub چندنهاد

## معرفی و هدف

اینترفیس داخلی دستورات (ایجاد قفل امانی، استعلام وضعیت، ثبت خرید صندوق) با پیاده‌سازی stub per `institution_id` و پیکربندی فلگ زنده/خاموش. بدون HTTP واقعی به بانک.

## مجوز

ارث از CY-008.

## نیازمندی‌ها و پیش‌نیازها

- CY-003-a.
- الگوی `doion.integrations`.

## سناریو (کاربر و پلتفرم)

سرویس matching به Port صدا می‌زند؛ stub پاسخ قطعی می‌دهد. نهاد اشتباه → خطا. فلگ live خاموش است.

## شرایط پذیرش

- [ ] matching به URL بانک hard-code ندارد.
- [ ] دو نهاد stub جدا بدون تداخل وضعیت.
- [ ] تست واحد بدون شبکه.
- [ ] کلید پیکربندی per institution در settings/env نه در کد دامنه.

## User Story (برای start-prompt)

```text
Feature Scope: BACKEND-ONLY
Capability Types: API / SERVICE · DATA LAYER · AUTOMATION

User Story:
به عنوان توسعه‌دهنده بک‌اند
می‌خواهم دستورات امانی و خرید صندوق را از طریق یک Port با stub per نهاد صدا بزنم
تا اتصال بانک دوم بدون بازنویسی matching اضافه شود.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio در صورت لمس UI — این برش UI ندارد
- ریل تسویه: n/a (زیرساخت)
- خارج از محدودهٔ این برش: وب‌هوک امضاشدهٔ واقعی، شتاب، OpenAPI بانک مشخص
- اسناد والد: docs/capability-roadmap/capabilities/CY-008-partner-integration-ports/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
```
