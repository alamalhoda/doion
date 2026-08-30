---
id: CY-003-b
parent: CY-003
status: draft
scope: FRONTEND-ONLY
capability_types:
  - UI FEATURE
blocked_by: [CY-003-a]
impl_path: null
updated: 2026-08-30
---

# CY-003-b — پوستهٔ هم‌برند در UI

## معرفی و هدف

نمایش نام و لوگوی چک‌یار همراه نهاد مرتبط در هدر/فوتر و روی صفحه‌ای که معامله به نهاد وصل است. چند نهاد فعال: زمینهٔ عمومی لندینگ طبق سیاست (سؤال باز CY-003) ؛ داخل معامله فقط نهاد همان معامله.

## مجوز

ارث از CY-003. متن دیسکلیمر باید نام حقوقی نهاد را نشان دهد.

## نیازمندی‌ها و پیش‌نیازها

- CY-003-a shipped (API فهرست نهاد).
- UI فقط AI Studio / `checkyar-googleai`.
- `design-system.md`.

## سناریو (کاربر و پلتفرم)

کاربر واردشده برند ترکیبی را می‌بیند. اگر لوگو نباشد نام حقوقی کافی است. مهمان: طبق سیاست لندینگ.

## شرایط پذیرش

- [ ] معاملهٔ وصل‌شده به نهاد نام آن نهاد را نشان می‌دهد.
- [ ] دادهٔ نهاد از API می‌آید نه hard-code.
- [ ] با فلگ خاموش، پوستهٔ فعلی لایه ۱ بدون نهاد است.

## User Story (برای start-prompt)

```text
Feature Scope: FRONTEND-ONLY
Capability Types: UI FEATURE

User Story:
به عنوان کاربر واردشده
می‌خواهم نام چک‌یار و نام نهاد هم‌برند مرتبط را روی صفحه ببینم
تا بدانم طرف حقوقی نمایش‌داده‌شده کیست.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio
- ریل تسویه: n/a
- خارج از محدودهٔ این برش: وایت‌لیبل، انتخاب نهاد توسط کاربر روی لندینگ اگر هنوز سیاست ندارد
- اسناد والد: docs/capability-roadmap/capabilities/CY-003-cobrand-multi-institution/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
```
