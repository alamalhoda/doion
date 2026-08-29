# GitFlow Workflow Skill — User Guide

این فایل برای **توسعه‌دهنده** نوشته شده است (نه برای Agent).

---

## این Skill چه کاری انجام می‌دهد؟

Skill `gitflow-workflow` کمک می‌کند جریان GitFlow پروژه را درست و امن اجرا کنید:

- سه نقطهٔ همگام‌سازی: شروع Task، قبل از PR، بعد از merge
- شروع branch جدید از `develop` به‌روز (`pull --ff-only`)
- نوشتن commit مطابق convention
- همگام‌سازی branch قبل از PR (پیش‌فرض: merge با `origin/develop`)
- push امن بعد از rebase (`--force-with-lease`)
- چک‌لیست آماده‌سازی PR
- ادغام به `develop` فقط از مسیر PR
- پاک‌سازی branch بعد از PR merge (`branch -d` محلی + `fetch --prune`)
- شاخهٔ کوتاه‌عمر با یک هدف (جلوگیری از شلوغی GitHub)

---

## شروع سریع (Quick Start)

در چت Cursor یکی از این درخواست‌ها را بنویس:

- `میخوام یک feature branch جدید شروع کنم`
- `قبل از PR برنچ من را با develop sync کن`
- `بعد از merge شاخه را پاک کن`
- `برای این تغییر commit message استاندارد پیشنهاد بده`
- `برای این فیچر تگ بزن`
- `Release روی develop اجرا کن`

---

## سه نقطهٔ Sync (حفظ کنید)

**نقطه ۱ — شروع Task**

```bash
git switch develop
git fetch origin
git pull --ff-only origin develop
git switch -c feature/<task-name>
```

روی `develop` محلی commit نکنید؛ فقط آینهٔ `origin/develop` است.

**نقطه ۲ — قبل از PR** (پیش‌فرض merge)

```bash
git fetch origin
git merge origin/develop
```

Rebase فقط اگر با آن راحت هستید؛ بعدش `--force-with-lease`.

**نقطه ۳ — بعد از Merge**

```bash
git switch develop
git pull --ff-only origin develop
git branch -d feature/<task-name>
git fetch --prune
```

اگر GitHub گزینهٔ **Automatically delete head branches** را روشن کرده باشد، حذف remote معمولاً لازم نیست.

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

### 5) پاک‌سازی بعد از merge

`PR مرج شد؛ develop محلی و شاخهٔ feature را طبق نقطه ۳ تمیز کن`

---

## رفتار مورد انتظار Skill

وقتی درست trigger شود، معمولا این کارها را انجام می‌دهد:

1. وضعیت فعلی git را بررسی می‌کند (`git status`, branch فعلی)
2. اگر روی `main` یا `develop` باشید هشدار می‌دهد
3. مسیر امن GitFlow را مرحله‌به‌مرحله پیشنهاد/اجرا می‌کند
4. نقطهٔ sync مناسب (۱ / ۲ / ۳) را اعمال می‌کند
5. قبل از PR، merge با `origin/develop` را پیش‌فرض می‌گذارد
6. به جای `--force` از `--force-with-lease` استفاده می‌کند
7. برای ادغام به `develop` مسیر PR را پیشنهاد می‌دهد (نه merge مستقیم محلی)

---

## خطاهای رایج که این Skill جلوگیری می‌کند

- commit مستقیم روی `main` یا `develop`
- ساخت branch بدون به‌روز کردن `develop` (نقطه ۱)
- PR بدون sync دوباره با `develop` (نقطه ۲) → conflict دیرهنگام
- ماندن شاخه بعد از merge (نقطه ۳) → شلوغی ریپو
- شاخهٔ همه‌کاره مثل `feature/ali-work`
- push اجباری ناامن (`--force`)
- تگ روی feature به‌جای workflow `Release`
- فراموش کردن تگ وقتی کاربر صریحاً می‌خواهد نسخهٔ قابل استقرار داشته باشد (یک یادآوری کافی است)

---

## نکته مهم

این Skill از Rule اصلی پروژه برای GitFlow استفاده می‌کند:

- `.cursor/rules/share/gitflow-branch-policy.mdc`
- `docs/development/ONBOARDING.md` برای همکار جدید (clone، دسترسی دو ریپو، UI یک‌طرفه)
- `.cursor/skills/semver-release/SKILL.md` برای تگ / GitHub Release / GHCR
- `docs/development/GIT_TAGS_AND_RELEASES.md` آموزش تگ و SemVer (برای انسان، نه فقط Agent)

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
