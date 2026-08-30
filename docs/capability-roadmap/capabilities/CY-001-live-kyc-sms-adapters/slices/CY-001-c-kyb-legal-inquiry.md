---
id: CY-001-c
parent: CY-001
status: draft
scope: BACKEND-ONLY
capability_types:
  - API / SERVICE
  - DATA LAYER
blocked_by: [CY-001-b]
impl_path: null
updated: 2026-08-30
---

# CY-001-c — استعلام KYB برای حقوقی

## معرفی و هدف

برای `Profile.user_type=legal` استعلام شناسهٔ ملی شرکت (نام، ثبت، نوع، نشانی) و در حد سیاست پایلوت فهرست امضاداران/هیئت‌مدیره. امروز KYC حقوقی فقط فیلد و ناظر دستی است.

## مجوز

ارث از CY-001. دادهٔ روزنامهٔ رسمی و امضاداران حساس است؛ ذخیرهٔ حداقل؛ اشتراک با شریک فقط با رضایت.

## نیازمندی‌ها و پیش‌نیازها

- CY-001-b (همان Port، عملیات جدا).
- شناسهٔ ۱۱ رقمی از قبل در KYC حقوقی validate می‌شود.
- تصمیم محصول: آیا `approved` خودکار حقوقی مجاز است یا استعلام فقط ضمیمهٔ صف ناظر است (پیشنهاد پایلوت: ضمیمه + ناظر، چون ترکیب امضا پیچیده‌تر از شاهکار است).

## سناریو (کاربر و پلتفرم)

کاربر حقوقی KYC می‌فرستد. سیستم شرکت را استعلام می‌کند. اگر یافت نشد → رد با کد. اگر یافت شد → خلاصه برای ناظر؛ در صورت پیکربندی سخت‌گیر، عدم تطبیق نام شرکت با فرم = رد.

## شرایط پذیرش

- [ ] مسیر حقوقی API حقیقیِ نام/تولد را صدا نمی‌زند.
- [ ] نبود شرکت در منبع → `approved` خودکار نیست.
- [ ] با فلگ `kyb_inquiry_live` خاموش، رفتار فعلی حقوقی حفظ می‌شود.

## User Story (برای start-prompt)

```text
Feature Scope: BACKEND-ONLY
Capability Types: API / SERVICE · DATA LAYER

User Story:
به عنوان ناظر
می‌خواهم برای کاربر حقوقی استعلام شرکت و امضاداران به درخواست KYC ضمیمه شود
تا تصمیم رد/تأیید بر دادهٔ ثبت باشد نه فقط خوداظهاری.

Additional Context:
- ریپو: بک‌اند doion
- ریل تسویه: n/a
- خارج از محدودهٔ این برش: بیومتریک مدیران، امضای دیجیتال اسناد
- اسناد والد: docs/capability-roadmap/capabilities/CY-001-live-kyc-sms-adapters/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
- انتخاب vendor: docs/capability-roadmap/vendor-landscape.md بخش ۲.۲ + پرامپت تحقیق همان فایل
- مرجع شکل API (نه قفل): وندار company-information / company-signature
```
