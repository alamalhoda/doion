---
id: CY-007-a
parent: CY-007
status: draft
scope: BACKEND-ONLY
capability_types:
  - API / SERVICE
  - DATA LAYER
blocked_by: [CY-003-a]
impl_path: null
updated: 2026-08-30
---

# CY-007-a — رکورد قرارداد و پذیرش

## معرفی و هدف

ذخیرهٔ نسخهٔ قالب قرارداد نهاد و ثبت پذیرش دارنده (و در صورت نیاز نهاد) روی Match ریل شریک. فایل PDF اختیاری است؛ حداقل متن نسخه‌بندی‌شده و timestamp.

## مجوز

ارث از CY-007. شخص حقوقی روی رکورد باید نهاد ریل باشد نه چک‌یار به‌عنوان طرف معامله.

## نیازمندی‌ها و پیش‌نیازها

- CY-003-a.
- Match ریل شریک ممکن است هنوز stub باشد؛ پذیرش به `match_id` وصل می‌شود.

## سناریو (کاربر و پلتفرم)

کاربر قرارداد را می‌پذیرد؛ سیستم نسخه را قفل می‌کند. درخواست پذیرش دوباره همان نسخه را تکرار می‌کند نه متن جدید خاموش.

## شرایط پذیرش

- [ ] پس از پذیرش، `template_version` روی Match تغییرپذیر نیست.
- [ ] audit شامل نهاد، نسخه، کاربر، زمان است.
- [ ] Match با `off_platform` مجبور به این پذیرش نیست.

## User Story (برای start-prompt)

```text
Feature Scope: BACKEND-ONLY
Capability Types: API / SERVICE · DATA LAYER

User Story:
به عنوان طرف معامله ریل شریک
می‌خواهم نسخهٔ مشخص قرارداد نهاد را بپذیرم و سیستم همان نسخه را قفل کند
تا متن حقوقی معامله قابل استناد باشد.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio در صورت لمس UI — این برش می‌تواند API-only باشد
- ریل تسویه: escrow یا principal_ledger (نه اجباری روی off_platform)
- خارج از محدودهٔ این برش: امضای PKI، چک‌لیست صیاد، آزادسازی وجه
- اسناد والد: docs/capability-roadmap/capabilities/CY-007-deal-contract-sayad-sync/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
```
