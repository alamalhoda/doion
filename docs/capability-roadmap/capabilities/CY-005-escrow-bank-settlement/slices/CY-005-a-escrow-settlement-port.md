---
id: CY-005-a
parent: CY-005
status: draft
scope: BACKEND-ONLY
capability_types:
  - API / SERVICE
  - DATA LAYER
blocked_by: [CY-003-a, CY-004-a]
impl_path: null
updated: 2026-08-30
---

# CY-005-a — مدل وضعیت امانی و Port

## معرفی و هدف

ماشین‌حالت وضعیت امانی روی `SettlementPort` (قفل، آزاد، برگشت، نامشخص) با اتصال به `institution` بانک. آداپتر زنده در این برش stub است.

## مجوز

ارث از CY-005. طرف قرارداد: بانک. وجه واقعی در این برش جابه‌جا نمی‌شود.

## نیازمندی‌ها و پیش‌نیازها

- CY-004-a (نمی‌توان escrow بدون نهاد ساخت).
- مدل `SettlementPort` موجود.

## سناریو (کاربر و پلتفرم)

سیستم Match escrow می‌سازد؛ وضعیت از stub می‌گذرد؛ confirm-off-platform برای این Match مجاز نیست.

## شرایط پذیرش

- [ ] Match `escrow` بدون بانک `escrow_bank` ذخیره نمی‌شود.
- [ ] گذار وضعیت نامعتبر رد می‌شود.
- [ ] `confirm-off-platform` روی Match escrow خطای معنایی می‌دهد.
- [ ] تست‌ها با stub و بدون بانک واقعی سبزند.

## User Story (برای start-prompt)

```text
Feature Scope: BACKEND-ONLY
Capability Types: API / SERVICE · DATA LAYER

User Story:
به عنوان سیستم matching
می‌خواهم برای معاملهٔ امانی بانک یک SettlementPort با وضعیت‌های قفل/آزاد/برگشت داشته باشم
تا آزادسازی وجه به ماشین‌حالت وصل باشد نه به تأیید تهی لایه ۱.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio در صورت لمس UI — این برش UI ندارد
- ریل تسویه: escrow
- خارج از محدودهٔ این برش: وب‌هوک زنده بانک، UI وضعیت، گیت صیاد
- اسناد والد: docs/capability-roadmap/capabilities/CY-005-escrow-bank-settlement/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
```
