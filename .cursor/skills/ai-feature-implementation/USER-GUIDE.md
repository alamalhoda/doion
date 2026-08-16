# AI Feature Implementation Skill — User Guide

این فایل برای **توسعه‌دهنده** است (نه برای Agent).

این مهارت **خودکار اجرا نمی‌شود**. فقط وقتی که آن را صریحاً صدا بزنید وارد چرخه Think/Build می‌شود. برای تغییر کوچک، باگ‌فیکس، یا سؤال معمولی از آن استفاده نکنید.

---

## چه زمانی استفاده شود؟

- ویژگی جدید با رفتار، قرارداد، یا سطح ابهام قابل توجه
- کار frontend-only، backend-only، یا full-stack
- وقتی می‌خواهید قبل از کد، spec و plan داشته باشید

## چه زمانی استفاده نشود؟

- اصلاح یک فایل، متن، استایل، یا باگ واضح
- ریفکتور کوچک
- سؤال درباره کد موجود

---

## نحوه فراخوانی

در چت Cursor یکی از این‌ها کافی است:

- `@ai-feature-implementation`
- `از skill ai-feature-implementation استفاده کن`
- پیست کردن قالب شروع در `start-prompt.md` یا `docs/ai_feature_implementation_start_generic.md`

بدون نام مهارت یا پرامپت شروع، Agent نباید این جریان را اجرا کند.

---

## جریان کوتاه

1. **Chat 1 — THINK:** سؤال‌های شفاف‌سازی → `feature_spec.md` → تأیید طراحی → `implementation_plan.md`
2. چت تازه باز کنید و spec + plan را بدهید.
3. **Chat 2 — BUILD:** پیاده‌سازی قدم‌به‌قدم → self-review → تست از روی spec → `integration_check.md`

---

## مثال پرامپت

```text
@ai-feature-implementation
لطفاً این ویژگی را مطابق skill پیش ببر. فعلاً کد ننویس.

Feature Scope: FRONTEND-ONLY
Capability Types: UI FEATURE

User Story:
[شرح ویژگی]

Additional Context:
[محدودیت‌ها]
```
