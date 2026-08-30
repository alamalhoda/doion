---
id: CY-006-a
parent: CY-006
status: draft
scope: FULL-STACK
capability_types:
  - UI FEATURE
  - API / SERVICE
  - DATA LAYER
blocked_by: [CY-004-a]
impl_path: null
updated: 2026-08-30
---

# CY-006-a — Match از نوع principal با نهاد صندوق

## معرفی و هدف

ایجاد و نمایش Match با `principal_ledger` که خریدار آن نهاد `liquidity_fund` است. پرداخت زنده و آداپتر در این برش stub است.

## مجوز

ارث از CY-006. طرف قرارداد: صندوق. پلتفرم خریدار نیست.

## نیازمندی‌ها و پیش‌نیازها

- CY-004-a.
- صفحات Match موجود در UI.

## سناریو (کاربر و پلتفرم)

دارنده پیشنهاد صندوق را می‌بیند و می‌پذیرد. سرمایه‌گذار ثالث این مسیر را نمی‌بیند. API طرف غیرصندوق را برای این ریل رد می‌کند.

## شرایط پذیرش

- [ ] `principal_ledger` فقط با نهاد صندوق فعال ایجاد می‌شود.
- [ ] UI نام حقوقی صندوق را روی پیشنهاد نشان می‌دهد.
- [ ] ثالث نمی‌تواند این نوع Match بسازد.
- [ ] پرداخت واقعی در این برش رخ نمی‌دهد (وضعیت stub مستند است).

## User Story (برای start-prompt)

```text
Feature Scope: FULL-STACK
Capability Types: UI FEATURE · API / SERVICE · DATA LAYER

User Story:
به عنوان دارنده چک
می‌خواهم پیشنهاد خرید صندوق هم‌برند را جدا از ابراز تمایل سرمایه‌گذار ثالث ببینم و بپذیرم
تا طرف قرارداد من صندوق باشد نه پلتفرم.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio در صورت لمس UI
- ریل تسویه: principal_ledger
- خارج از محدودهٔ این برش: واریز واقعی، سقف ریسک پیشرفته، بازار ثانویه
- اسناد والد: docs/capability-roadmap/capabilities/CY-006-principal-fund-liquidity/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
```
