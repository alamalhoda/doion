---
id: CY-020-a
parent: CY-020
status: draft
scope: FULL-STACK
capability_types:
  - UI FEATURE
  - API / SERVICE
  - DATA LAYER
blocked_by: []
impl_path: null
updated: 2026-08-30
---

# CY-020-a — پورت پیشنهاد فیلد چک از تصویر + stub و فلگ

## معرفی و هدف

یک Port داخلی که از تصویر چک (فایل یا `document_id` نوع `cheque_image`) فیلدهای پیشنهادی آگهی را برمی‌گرداند تا ویزارد ثبت آن‌ها را در فرم **قابل ویرایش** نشان دهد. آداپتر زنده در این برش stub است. استعلام صیاد و OCR مدارک هویتی خارج است.

## مجوز

ارث از CY-020. تصویر فقط با رضایت ضمنی آپلود دارنده و فلگ روشن به Port می‌رود.

## نیازمندی‌ها و پیش‌نیازها

- آپلود مدرک آگهی و فیلدهای `ChequeListing` موجود.
- الگوی `doion.integrations`؛ تست بدون شبکه.
- آستانهٔ اطمینان per-field از تنظیمات.
- کاندید واسط: [`vendor-landscape.md`](../../../vendor-landscape.md) بخش ۲.۹. این برش vendor را قفل نمی‌کند.
- UI فقط از مسیر Google AI Studio.

## سناریو (کاربر و پلتفرم)

دارنده تصویر را می‌فرستد. با فلگ روشن پاسخ پیشنهاد (یا خالی) می‌آید. فرم را ویرایش و submit می‌کند. Stub در تست فیلد ثابت یا خالی برمی‌گرداند؛ شبکه صدا زده نمی‌شود.

## شرایط پذیرش

- [ ] فلگ خاموش: بدون فراخوانی OCR؛ ایجاد آگهی دستی intact است.
- [ ] شکست/stub خالی مانع `POST` آگهی معتبر نیست.
- [ ] مقدار پیشنهادی نامعتبر (مثلاً شناسه غیر ۱۶ رقم) در submit همان خطای فعلی را می‌دهد.
- [ ] پاسخ Port شامل وضعیت صیاد یا نمرهٔ bureau نیست.
- [ ] دامنه به schema یک vendor وابسته نیست.
- [ ] تصویر کامل در لاگ نیست.

## User Story (برای start-prompt)

```text
Feature Scope: FULL-STACK
Capability Types: UI FEATURE · API / SERVICE · DATA LAYER

User Story:
به عنوان دارنده چک
می‌خواهم پس از آپلود تصویر چک، مشخصات خوانده‌شده به‌صورت پیشنهادی در فرم آگهی بیاید تا بتوانم آن‌ها را اصلاح و تأیید کنم
تا ورود شناسهٔ صیادی و مبلغ کمتر خطا داشته باشد بدون حذف ورود دستی.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio
- ریل تسویه: n/a
- خارج از محدودهٔ این برش: استعلام صیاد CY-002، اعتبار صادرکننده، OCR کارت ملی، آداپتر زنده vendor
- اسناد والد: docs/capability-roadmap/capabilities/CY-020-cheque-document-ocr-assist/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
- انتخاب vendor: docs/capability-roadmap/vendor-landscape.md بخش ۲.۹ + پرامپت تحقیق همان فایل؛ دامنه را قفل نکن
- منبع حقیقت فرم: مقادیر تأییدشدهٔ کاربر + اعتبارسنجی موجود listings
```
