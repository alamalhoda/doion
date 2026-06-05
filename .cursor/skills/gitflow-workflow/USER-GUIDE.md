# GitFlow Workflow Skill — User Guide

این فایل برای **توسعه‌دهنده** نوشته شده است (نه برای Agent).

---

## این Skill چه کاری انجام می‌دهد؟

Skill `gitflow-workflow` کمک می‌کند جریان GitFlow پروژه را درست و امن اجرا کنید:

- شروع branch جدید از `develop`
- نوشتن commit مطابق convention
- همگام‌سازی branch قبل از PR
- push امن بعد از rebase
- چک‌لیست آماده‌سازی PR
- ادغام به `develop` فقط از مسیر PR
- پاک‌سازی branch بعد از PR merge

---

## شروع سریع (Quick Start)

در چت Cursor یکی از این درخواست‌ها را بنویس:

- `میخوام یک feature branch جدید شروع کنم`
- `قبل از PR برنچ من را با develop sync کن`
- `برای این تغییر commit message استاندارد پیشنهاد بده`
- `rebase کردم، push امنش را بگو`

---

## مثال Promptهای آماده

### 1) شروع Feature

`برای قابلیت reminder یک feature branch استاندارد GitFlow بساز`

### 2) Sync قبل از PR

`لطفا branch فعلی را با develop همگام کن و اگر conflict بود مراحلش را بگو`

### 3) Commit Convention

`برای تغییرات staged یک commit message با فرمت type(scope): description بده`

### 4) Push بعد از Rebase

`من rebase کردم، دستور push ایمن را بده`

---

## رفتار مورد انتظار Skill

وقتی درست trigger شود، معمولا این کارها را انجام می‌دهد:

1. وضعیت فعلی git را بررسی می‌کند (`git status`, branch فعلی)
2. اگر روی `main` یا `develop` باشید هشدار می‌دهد
3. مسیر امن GitFlow را مرحله‌به‌مرحله پیشنهاد/اجرا می‌کند
4. قبل از PR، sync با `origin/develop` را یادآوری می‌کند
5. به جای `--force` از `--force-with-lease` استفاده می‌کند
6. برای ادغام به `develop` مسیر PR را پیشنهاد می‌دهد (نه merge مستقیم محلی)

---

## خطاهای رایج که این Skill جلوگیری می‌کند

- commit مستقیم روی `main` یا `develop`
- ساخت branch بدون مشخص‌کردن مبدا (`develop`)
- push اجباری ناامن (`--force`)
- PR بدون sync شدن با `develop`
- commit message غیر استاندارد

---

## نکته مهم

این Skill از Rule اصلی پروژه برای GitFlow استفاده می‌کند:

- `.cursor/rules/share/gitflow-branch-policy.mdc`

اگر policy پروژه تغییر کند، Skill هم باید به‌روزرسانی شود.

---

## Troubleshooting

### Skill فعال نمی‌شود

- درخواست را واضح‌تر بنویس و کلمات trigger مثل `gitflow`, `feature branch`, `sync develop`, `PR` را بیاور.
- مطمئن شو داخل همین repository هستی (Project Skill).

### دستور اشتباه به نظر می‌رسد

- وضعیت فعلی branch را اعلام کن.
- هدف را دقیق بگو (مثلا: PR می‌خواهی یا فقط sync/rebase؟).

---

## Scope

این Skill برای workflow گیت طراحی شده است، نه review کد یا تصمیم معماری.
