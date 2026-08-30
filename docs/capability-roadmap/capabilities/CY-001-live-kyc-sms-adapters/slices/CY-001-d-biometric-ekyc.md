---
id: CY-001-d
parent: CY-001
status: draft
scope: FULL-STACK
capability_types:
  - UI FEATURE
  - API / SERVICE
blocked_by: [CY-001-b]
impl_path: null
updated: 2026-08-30
---

# CY-001-d — eKYC بیومتریک (SDK / Webview)

## معرفی و هدف

اگر نهاد هم‌برند مشتری‌پذیری غیرحضوری بانکی بخواهد: هدایت کاربر به SDK یا Webview ارائه‌دهنده (فراشناسا یا یوآیدی)، دریافت نتیجهٔ verification + liveness، نگاشت به `Verification`. بدون این الزام، برش `blocked` می‌ماند.

## مجوز

ارث از CY-001. نگهداری ویدئو/چهره حداقل و مطابق قرارداد ارائه‌دهنده؛ پلتفرم انبار بیومتریک ملی نیست.

## نیازمندی‌ها و پیش‌نیازها

- CY-001-b برای دادهٔ هویتی پایه قبل از جلسهٔ بیومتریک.
- قرارداد و کلید sandbox ارائه‌دهنده.
- UI فقط از مسیر Google AI Studio.
- تصمیم نهاد: فراشناسا در برابر یوآیدی در برابر جیبیت — امتیازدهی در [`vendor-landscape.md`](../../../vendor-landscape.md) بخش ۲.۳.

## سناریو (کاربر و پلتفرم)

کاربر پس از استعلام موفق به جلسهٔ بیومتریک می‌رود. موفقیت → `approved`. شکست liveness یا عدم تطبیق چهره → `rejected`. انصراف/timeout → `pending` و صف ناظر.

## شرایط پذیرش

- [ ] فلگ `kyc_biometric_live` خاموش مسیر استعلام‌only را نگه می‌دارد.
- [ ] نتیجه فقط از callback/استعلام وضعیت ارائه‌دهنده با همبستگی `verification_id` پذیرفته می‌شود.
- [ ] فایل بیومتریک در لاگ یا قرارداد API عمومی چک‌یار برنمی‌گردد.

## User Story (برای start-prompt)

```text
Feature Scope: FULL-STACK
Capability Types: UI FEATURE · API / SERVICE

User Story:
به عنوان کاربر حقیقی
می‌خواهم احراز غیرحضوری بیومتریک نهاد را کامل کنم
تا بانک/صندوق هم‌برند هویت مرا بدون مراجعهٔ حضوری بپذیرد.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط AI Studio
- ریل تسویه: n/a
- خارج از محدودهٔ این برش: امضای دیجیتال اسناد معامله، SMS
- اسناد والد: docs/capability-roadmap/capabilities/CY-001-live-kyc-sms-adapters/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
- انتخاب vendor: docs/capability-roadmap/vendor-landscape.md بخش ۲.۳ + پرامپت تحقیق همان فایل
- مرجع شکل (نه قفل): فراشناسا احراز غیرحضوری؛ یوآیدی eKYC؛ جیبیت SDK/API/Gateway
```
