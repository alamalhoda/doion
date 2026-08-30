---
id: CY-001-b
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

# CY-001-b — پورت استعلام هویتی حقیقی + stub

## معرفی و هدف

یک Port داخلی برای استعلام هویت **حقیقی**: تطبیق موبایل–کدملی (شاهکار) و تطبیق نام/کدملی/تاریخ تولد (و در صورت وجود استعلام ثبت احوال). آداپتر واقعی قابل تعویض است (وندار، یوآیدی، فینوتک، بانک). این برش eKYC ویدئویی و KYB نیست.

## مجوز

ارث از CY-001. رضایت کاربر برای استعلام باید قبل از فراخوانی ثبت شود.

## نیازمندی‌ها و پیش‌نیازها

- مدل `Verification` امروز تاریخ تولد ندارد؛ این برش باید فیلد لازم برای استعلام را به فرآیند KYC حقیقی اضافه کند (API + مهاجرت) بدون طراحی UI در این scope — اگر UI بدون فیلد بماند، فلگ زنده روشن نمی‌شود.
- الگوی `doion.integrations`؛ تست‌ها با stub و بدون شبکه.
- آستانهٔ درصد تطبیق نام از تنظیمات (نه magic number در دامنه). مرجع بازار: وندار پیشنهاد ≥۸۰ می‌دهد؛ مقدار پایلوت با شریک تثبیت می‌شود.
- کاندید واسط: [`vendor-landscape.md`](../../../vendor-landscape.md) بخش ۲.۱. آداپتر زنده بعد از امتیازدهی؛ این برش می‌تواند فقط Port+stub باشد.

## سناریو (کاربر و پلتفرم)

ناظر/سیستم پس از submit KYC حقیقی استعلام را می‌زند. تطبیق → مسیر تأیید خودکار یا پیشنهاد به ناظر طبق فلگ. عدم تطبیق → `rejected` با کد. قطع تأمین‌کننده → `pending` + صف دستی.

## شرایط پذیرش

- [ ] دامنه به URL یا schema یک vendor وابسته نیست.
- [ ] با فلگ خاموش هیچ فراخوانی شبکه برای KYC نیست.
- [ ] شاهکار نامنطبق مانع `approved` خودکار است.
- [ ] پاسخ ۵۰۲/timeout تأمین‌کننده `approved` نمی‌سازد.
- [ ] تست‌ها بدون شبکه سبز می‌مانند.

## User Story (برای start-prompt)

```text
Feature Scope: BACKEND-ONLY
Capability Types: API / SERVICE · DATA LAYER

User Story:
به عنوان ناظر و پلتفرم
می‌خواهم احراز حقیقی از طریق پورت استعلام (شاهکار + تطبیق هویتی) با failover به صف دستی انجام شود
تا درخواست‌های سازگار بدون دستکاری DB به وضعیت نهایی برسند.

Additional Context:
- ریپو: بک‌اند doion؛ ویزارد UI در صورت نیاز به تاریخ تولد در برش جدا / Studio
- ریل تسویه: n/a
- خارج از محدودهٔ این برش: SMS، KYB، بیومتریک، اعتبار صادرکننده
- اسناد والد: docs/capability-roadmap/capabilities/CY-001-live-kyc-sms-adapters/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
- انتخاب vendor: docs/capability-roadmap/vendor-landscape.md بخش ۲.۱ + پرامپت تحقیق همان فایل
- مرجع شکل API (نه قفل): docs.vandar.io inquiry kyc / shahkar / nid
```
