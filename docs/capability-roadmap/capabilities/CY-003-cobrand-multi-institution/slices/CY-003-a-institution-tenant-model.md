---
id: CY-003-a
parent: CY-003
status: draft
scope: BACKEND-ONLY
capability_types:
  - API / SERVICE
  - DATA LAYER
blocked_by: []
impl_path: null
updated: 2026-08-30
---

# CY-003-a — مدل نهاد و نقش بانک/صندوق

## معرفی و هدف

ثبت نهاد هم‌برند با نقش `escrow_bank` و/یا `liquidity_fund`، فعال/غیرفعال‌سازی، و خواندن فهرست نهادهای فعال از API احرازشده (و در صورت نیاز ادمین). UI پوسته در این برش نیست.

## مجوز

ارث از CY-003. دادهٔ نهاد مجوز معامله نمی‌سازد.

## نیازمندی‌ها و پیش‌نیازها

- لایه ۱ و JWT موجود.
- UI این برش: فقط در صورت وجود ادمین جنگو؛ API برای برش بعد.

## سناریو (کاربر و پلتفرم)

ادمین نهاد بانک و صندوق می‌سازد. کلاینت احرازشده فهرست نهادهای فعال را می‌گیرد. نهاد غیرفعال در فهرست فعال نیست.

## شرایط پذیرش

- [ ] ایجاد دو نهاد همزمان با نقش‌های متفاوت ممکن است.
- [ ] نهاد غیرفعال در لیست فعال برنمی‌گردد.
- [ ] بدون نقش معتبر نهاد ذخیره نمی‌شود.
- [ ] تست permission: کاربر عادی write ندارد.

## User Story (برای start-prompt)

```text
Feature Scope: BACKEND-ONLY
Capability Types: API / SERVICE · DATA LAYER

User Story:
به عنوان ادمین پلتفرم
می‌خواهم بانک و صندوق هم‌برند را به‌صورت نهاد با نقش امانی یا نقدینگی ثبت و فعال/غیرفعال کنم
تا معامله‌های بعدی به شخص حقوقی مشخص وصل شوند نه به نام آزاد.

Additional Context:
- ریپو: بک‌اند doion؛ UI فقط از مسیر Google AI Studio در صورت لمس UI — این برش UI محصول ندارد
- ریل تسویه: n/a
- خارج از محدودهٔ این برش: تم، لوگو در SPA، ریل escrow/principal، دروازهٔ Match
- اسناد والد: docs/capability-roadmap/capabilities/CY-003-cobrand-multi-institution/capability.md
- فرآیند: docs/capability-roadmap/usage-guide.md
```
