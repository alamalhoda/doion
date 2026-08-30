---
id: CY-004-a
parent: CY-004
status: draft
scope: FULL-STACK
capability_types:
  - UI FEATURE
  - API / SERVICE
  - DATA LAYER
blocked_by: [CY-003-a]
impl_path: null
updated: 2026-08-30
---

# CY-004-a — محدودیت API و UI طرف معامله

## معرفی و هدف

اعمال قانون W1: `escrow` و `principal_ledger` فقط برای نهاد مجاز؛ سرمایه‌گذار غیرنهاد فقط `off_platform`.

## مجوز

ارث از CY-004. این برش پوشش حقوقی ثالث را گسترش نمی‌دهد.

## نیازمندی‌ها و پیش‌نیازها

- CY-003-a (نهاد و نقش).
- `POST /api/v1/matches/` موجود.

## سناریو (کاربر و پلتفرم)

سرمایه‌گذار ثالث ابراز تمایل می‌کند → `off_platform`. درخواست escrow از همان کاربر → خطای قرارداد. نهاد صندوق مسیر principal را می‌بیند.

## شرایط پذیرش

- [ ] API ریل شریک را برای غیرنهاد رد می‌کند با کد پایدار.
- [ ] UI دکمهٔ ریل شریک را برای غیرنهاد نشان نمی‌دهد.
- [ ] Match ثالث `off_platform` همچنان ساخته می‌شود.
- [ ] audit برای رد ریل ثبت می‌شود.

## User Story (برای start-prompt)

```text
Feature Scope: FULL-STACK
Capability Types: UI FEATURE · API / SERVICE · DATA LAYER

User Story:
به عنوان پلتفرم
می‌خواهم در موج اول فقط صندوق یا مسیر امانی بانک وارد ریل‌های غیر off_platform شوند
تا سرمایه‌گذار ثالث تا تعیین چتر حقوقی همان تسویهٔ بیرون از پلتفرم را داشته باشد.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio در صورت لمس UI
- ریل تسویه: off_platform پیش‌فرض؛ escrow و principal_ledger فقط نهاد
- خارج از محدودهٔ این برش: پیاده‌سازی آزادسازی وجه، آداپتر بانک، قرارداد PDF
- اسناد والد: docs/capability-roadmap/capabilities/CY-004-partner-counterparty-gate/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
```
