# Share Rules Full Content

این فایل تجمیع کامل محتوای همه فایل‌های `.mdc` در پوشه `share/` است (بدون خلاصه‌سازی).

---

## `gitflow-branch-policy.mdc`

````mdc
---
description: Canonical Git Flow branch policy and guardrails for this project
alwaysApply: true
---

# GitFlow Branch Policy (OilChenger)

## هدف
- این قانون مرجع اصلی Git Flow برای پیشنهادهای AI در این پروژه است.
- AI باید توسعه را فقط روی branchهای کاری انجام دهد و از commit مستقیم روی `master`/`develop` جلوگیری کند.
- سه نقطهٔ همگام‌سازی اجباری است تا conflict و شلوغی ریپو کم شود؛ `develop` محلی فقط آینهٔ `origin/develop` است.

## مدل شاخه‌ها
در این ریپو (`doion`) شاخهٔ پایدار **`master` است، نه `main`**. `main` متعلق به ریپوی UI (`checkyar-googleai`) است و با GitFlow بک‌اند قاطی نشود.
- `master`: فقط نسخه پایدار production-ready
- `develop`: شاخه integration (فقط از طریق PR) — محل توسعه نیست
- `feature/*`: توسعه قابلیت جدید (از `develop`) — یک هدف، عمر کوتاه
- `bugfix/*`: رفع باگ محیط توسعه (از `develop`)
- `release/*`: آماده‌سازی نسخه (از `develop`)
- `hotfix/*`: رفع فوری production (از `master`)

## قوانین قطعی
1. هرگز commit مستقیم روی `master` یا `develop` پیشنهاد نده (نه remote، نه local).
2. همگام‌سازی در **سه نقطه** اجباری است: شروع Task، قبل از PR، بعد از merge.
3. branch جدید را صریحاً از `develop` به‌روز بساز (`git checkout -b ... develop`).
4. قبل از PR، پیش‌فرض همگام‌سازی با `origin/develop` **merge** است؛ rebase فقط اگر کاربر صریح بخواهد.
5. اگر rebase انجام شد، فقط `--force-with-lease` مجاز است (نه `--force`).
6. ادغام `feature/*` یا `bugfix/*` به `develop` فقط از طریق Pull Request مجاز است.
7. برای ادغام عادی به `develop` هرگز دستور merge مستقیم محلی (`git merge feature/...`) پیشنهاد نده.
8. شاخهٔ کاری یک هدف داشته باشد (نه `feature/ali-work` چندروزه با هر موضوع). بعد از merge از remote و local حذف شود.

## سه نقطهٔ همگام‌سازی (اجباری)

### نقطه ۱ — شروع Task
`develop` محلی را آینه کن، بعد branch بساز. روی `develop` از `pull --ff-only` استفاده کن تا merge تصادفی ساخته نشود.

```bash
git checkout develop
git fetch origin
git pull --ff-only origin develop
git checkout -b feature/<short-name> develop
```

اگر `--ff-only` شکست خورد: روی `develop` محلی commit نکن؛ وضعیت را بررسی کن. اگر commit محلی روی `develop` بی‌ارزش است، به `origin/develop` برگرد (`reset --hard` فقط با تأیید کاربر).

برای bugfix همان ترتیب با `bugfix/<short-name>`.

### نقطه ۲ — قبل از PR (پیش‌فرض: merge)
شروع از develop به‌روز کافی نیست اگر وسط کار `origin/develop` جلو رفته باشد.

```bash
git checkout feature/<name>
git fetch origin
git merge origin/develop
# فقط اگر کاربر صریح بخواهد:
# git rebase origin/develop
```

در صورت conflict: فایل‌ها را اصلاح کن، `git add`، سپس `git merge --continue` یا `git rebase --continue`.

### نقطه ۳ — بعد از merge شدن PR
شاخهٔ ادغام‌شده را پاک کن و `develop` محلی را دوباره آینه کن.

```bash
git checkout develop
git pull --ff-only origin develop
git branch -d feature/<name>
git fetch --prune
```

اگر GitHub هنوز head branch را دارد: `git push origin --delete feature/<name>`. اگر **Automatically delete head branches** روشن است، حذف remote را رد کن؛ `fetch --prune` کافی است.

## نام‌گذاری پیشنهادی
- خوب: `feature/add-user-profile`، `feature/124-login-with-google`، `bugfix/login-validation`
- بد: `feature/ali-work`، شاخهٔ همه‌کارهٔ طولانی
- `hotfix/security-patch-2026`

## Commit Convention
فرمت:
```text
type(scope): description
```

نوع‌ها:
- `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

نمونه:
```bash
git commit -m "feat(auth): add Google OAuth login flow"
```

## Push و PR (اجباری برای ادغام به `develop`)
```bash
git push -u origin feature/<name>
# اگر rebase شده:
git push --force-with-lease origin feature/<name>

gh pr create --base develop --head feature/<name> --title "<title>" --body "<body>"
```

PR باید:
- From: `feature/*` یا `bugfix/*`
- To: `develop`
- شامل هدف تغییر، خلاصه تغییرات، وضعیت تست/build باشد

## چک‌لیست قبل از PR
- `git status` تمیز یا قابل‌انتظار است
- نقطه ۲ انجام شده (branch با `origin/develop` همگام)
- conflictها حل شده
- build موفق است
- تست‌های مرتبط پاس شده‌اند
- commit messageها استاندارد هستند

## قاعده ادغام به `develop` (خیلی مهم)
- مسیر مجاز ادغام: `feature/*` یا `bugfix/*` -> Pull Request -> `develop`
- merge مستقیم محلی روی `develop` برای جریان عادی مجاز نیست.
- اگر کاربر درخواست merge مستقیم داد، ابتدا مسیر PR را پیشنهاد بده و دلیل ایمنی را کوتاه توضیح بده.

## همکاری داخلی روی GitHub (doion)
- همکار داخلی: **clone** از `alamalhoda/doion` و Collaborator با **Write** (نه Admin، نه Fork پیش‌فرض).
- کار روی `feature/*` یا `bugfix/*` همان origin؛ ادغام فقط PR به `develop`.
- ریپوی خالی جدا در اکانت همکار جایگزین Fork نیست و معمولاً PR به این ریپو نمی‌سازد.
- Fork فقط وقتی که Write روی این ریپو نباید داده شود؛ آن‌گاه `upstream` = این ریپو و PR به `develop`.
- UI فعال (`checkyar-googleai`): از Cursor پوش نکن. همکار برای تست لوکال حداکثر **Read** کافی است. منبع تغییر UI فقط AI Studio است؛ در هر لحظه یک UI Editor. جزئیات انسانی: `docs/development/ONBOARDING.md` و `docs/development/FRONTEND_DEVELOPMENT_STATUS.md`.
- Release / CD / تگ محصول / secretها را برای همکار پیشنهاد نده مگر مالک صریح بخواهد.

## شلوغی GitHub
- بعد از merge، head branch نباید بماند. در Settings ریپو گزینهٔ **Automatically delete head branches** توصیه می‌شود.
- Protection روی `master`/`develop` جلوی push مستقیم را می‌گیرد؛ این جایگزین سه نقطهٔ sync نیست.
- Required status checks روی PR به `develop`: jobهای CI بک‌اند (Ruff و pytest). E2E را merge-gate نکن مگر سیاست عوض شود.

## رفتار اجباری AI در پیشنهاد دستورات
- قبل از دستورهای حساس، ابتدا `git status` پیشنهاد بده.
- شروع کار جدید = نقطه ۱ (نه ساخت branch از `master` یا develop کهنه).
- آماده‌سازی PR = نقطه ۲ با **merge** مگر کاربر rebase بخواهد.
- بعد از merge = نقطه ۳ (local delete + prune).
- در صورت مشاهده الگوی خطرناک (کار/commit روی `master`/`develop`)، هشدار صریح بده.
- در صورت ابهام در هدف کاربر، اول هدف را شفاف کن و سپس دستور بده.
- برای ادغام به `develop` ابتدا push branch و سپس PR را راهنمایی/اجرا کن.
- برای همکار داخلی Fork یا Write روی ریپوی UI پیشنهاد نده مگر کاربر صریح بخواهد.

## تگ SemVer و یادآوری انتشار
- مسیر انتشار محصول: workflow [`.github/workflows/release.yml`](../../../.github/workflows/release.yml) با `workflow_dispatch` (تگ + GitHub Release + ایمیج GHCR). روی `feature/*` با `git tag` نسخهٔ محصول نساز.
- تگ را بازنویسی/force نکن؛ نسخهٔ بعدی بزن. بدون تأیید صریح نسخه، `workflow_dispatch` نزن.
- **یادآوری (یک سؤال کوتاه، نه سخنرانی):** وقتی کاربر feat/fix را به `develop` ادغام کرده و از تمام‌شدن کار، ship، deploy، چابکان، یا نسخه حرف می‌زند؛ وقتی UI قابل‌دیدن کاربر به `product` رفته؛ یا Verify یک گام CI/CD به ایمیج تگ‌شده نیاز دارد. روی docs/chore/rule alone یا هر کامیت یادآوری نکن.
- جزئیات اجرا: Skill `.cursor/skills/semver-release/SKILL.md`. آموزش انسانی: `docs/development/GIT_TAGS_AND_RELEASES.md`.
````

---

## `engineering-principles.mdc`

````mdc
---
description: Universal engineering principles for maintainable code across the project
alwaysApply: true
---

# Engineering Principles (Shared)

این اصول برای همه بخش‌ها (backend/frontend/docs/scripts) معتبر هستند.

## Core Principles

- **SSOT:** هر منطق یا قانون باید یک منبع یکتا داشته باشد.
- **Separation of Concerns:** UI/transport, business logic, data access را جدا نگه دار.
- **DRY:** از تکرار منطق پرهیز کن؛ استخراج helper/service زمانی که تکرار دیده می‌شود.
- **KISS:** ساده‌ترین طراحی درست را انتخاب کن.
- **YAGNI:** قابلیت اضافی بدون نیاز فعلی اضافه نکن.
- **Minimize Change Impact:** تغییرات کوچک، قابل بازبینی، و با اثر جانبی محدود انجام بده.
- **Explicitness:** قراردادها (ورودی/خروجی/خطا) واضح باشند، نه ضمنی.

## Decision Rules

- اگر بین دو قاعده conflict دیدی، اولویت با rule تخصصی همان دامنه است.
- اگر rule مبهم بود، سؤال بپرس؛ حدس نزن.
````

---

## `code-quality-baseline.mdc`

````mdc
---
description: Universal code quality baseline for all code changes
alwaysApply: true
---

# Code Quality Baseline (Shared)

این baseline در کل پروژه اعمال می‌شود و قوانین تخصصی هر دامنه آن را تکمیل می‌کنند.

## Baseline Rules

- کد باید خوانا، قابل فهم و قابل نگهداری باشد.
- از نام‌های توصیفی برای فایل‌ها، متغیرها، توابع، و کلاس‌ها استفاده کن.
- از `magic numbers` و `magic strings` پرهیز کن؛ از constant یا config استفاده کن.
- از کامنت غیرضروری پرهیز کن؛ فقط منطق پیچیده را توضیح بده.
- side effect پنهان ایجاد نکن؛ رفتار مهم باید قابل پیش‌بینی باشد.
- secrets (token/password/api-key) نباید hard-code شوند؛ فقط env/config امن.
- برای تغییرات بحرانی یا رفتارهای حیاتی، تست یا plan تست ارائه بده.

## Scope Note

- قوانین naming/framework-specific را ruleهای همان دامنه تعیین می‌کنند.
````

---

## `rule-precedence.mdc`

````mdc
---
description: Rule precedence and conflict resolution policy for all Cursor rules
alwaysApply: true
---

# Rule Precedence

این فایل ترتیب اولویت Ruleها را مشخص می‌کند تا تضادها قابل حل باشند.

## Precedence Order

1. **System/Platform constraints**
2. **Repository global rules** (`share/*`)
3. **Domain rules** (`backend/*` یا `frontend/*`) بر اساس مسیر فایل
4. **File-specific rules** (glob محدودتر) نسبت به glob کلی‌تر
5. **Style preferences** (کم‌اولویت‌تر از correctness/security)

## Conflict Resolution

- در تعارض بین `share` و domain، اگر موضوع domain-specific است، rule دامنه ارجح است.
- در تعارض بین دو rule هم‌سطح:
  - rule با scope محدودتر ارجح است.
  - اگر scope برابر بود، rule جدیدتر/شفاف‌تر را مبنا بگیر.
- در تعارض امنیت/درستی با style/performance، اولویت با **security/correctness** است.

## Mandatory Behavior

- اگر conflict قابل حل نبود، AI باید:
  1. تعارض را صریح اعلام کند
  2. ریسک هر گزینه را کوتاه بگوید
  3. سؤال روشن برای تصمیم نهایی بپرسد

## Scope Mapping

- فایل‌های `backend/**` → rules در `backend/` + `share/`
- فایل‌های `frontend/**` → rules در `frontend/` + `share/`
- سایر فایل‌ها → فقط `share/` و ruleهای مرتبط با همان مسیر
````

---

## `rule-authoring-standard.mdc`

````mdc
---
description: Authoring standards for creating and maintaining Cursor rule files
globs:
  - ".cursor/rules/**/*.mdc"
  - ".cursor/rules/**/*.md"
alwaysApply: false
---

# Rule Authoring Standard

استاندارد نگارش Ruleها برای یکدستی، نگهداری ساده، و کاهش تداخل.

## Structure

- هر Rule باید frontmatter معتبر داشته باشد:
  - `description`
  - `alwaysApply` یا `globs` (بر اساس نیاز)
- عنوان واضح و محتوای action-oriented داشته باشد.
- یک Rule = یک concern اصلی (از ruleهای God پرهیز کن).

## Placement Policy

- قوانین **عمومی/جهان‌شمول** → `share/`
- قوانین **تخصصی frontend** → `frontend/`
- قوانین **تخصصی backend** → `backend/`
- قوانین deprecated:
  - `alwaysApply: false`
  - در توضیح، `replaced by <path>` ذکر شود

## AlwaysApply Budget

- هدف پروژه: حداکثر **۵ Rule** با `alwaysApply: true`
- `alwaysApply: true` فقط برای قواعد global و کم‌حجم در `share/`
- Ruleهای domain-specific باید `alwaysApply: false` باشند و با `globs` دقیق فعال شوند
- اگر Rule جدید نیاز به `alwaysApply: true` داشت:
  1. دلیل صریح بنویس
  2. اثر آن بر context window را بررسی کن
  3. در صورت امکان یک Rule قدیمی را به حالت scoped تبدیل کن

## Naming Convention

- نام فایل‌ها: `kebab-case.mdc`
- الگوی پیشنهادی:
  - `<topic>-policy.mdc`
  - `<topic>-checklist.mdc`
  - `<topic>-standards.mdc`

## Content Quality

- قوانین کوتاه، شفاف، و قابل اجرا باشند.
- از مثال‌های `Bad/Good` فقط وقتی کمک می‌کند استفاده کن.
- تکرار محتوای موجود را به ارجاع تبدیل کن، نه کپی.
- دستورات پرخطر باید صریحاً با guardrail همراه باشند.
````

---

## `rules-audit-checklist.mdc`

````mdc
---
description: PR-ready checklist for auditing rule changes before merge
globs:
  - ".cursor/rules/**/*.mdc"
  - ".cursor/rules/**/*.md"
alwaysApply: false
---

# Rules Audit Checklist (PR)

این چک‌لیست قبل از merge تغییرات Ruleها در PR اجرا شود.

## A) Scope and Placement

- [ ] Rule جدید واقعاً عمومی است؟ اگر بله در `share/` قرار گرفته.
- [ ] اگر domain-specific است، در `backend/` یا `frontend/` قرار گرفته.
- [ ] Rule با Rule موجود overlap غیرضروری ندارد.

## B) Frontmatter Validation

- [ ] `description` واضح و کوتاه است.
- [ ] `alwaysApply` فقط وقتی ضروری است `true` شده.
- [ ] برای ruleهای file-specific، `globs` دقیق و کم‌هزینه است.

## C) Conflict and Precedence

- [ ] با `share/rule-precedence.mdc` همخوان است.
- [ ] تعارض با ruleهای موجود بررسی شده و حل شده.
- [ ] اگر rule دیگری جایگزین شده، مسیر جایگزین ذکر شده.

## D) Content Quality

- [ ] Rule actionable است (فقط توضیح نظری نیست).
- [ ] متن تکراری به reference تبدیل شده.
- [ ] مثال‌ها (در صورت وجود) دقیق و به‌روز هستند.
- [ ] دستور ناایمن یا مبهم ندارد.

## E) Documentation Sync

- [ ] `share/README.md` در صورت نیاز به‌روزرسانی شده.
- [ ] `rules/README.md` در صورت تغییر ساختار به‌روزرسانی شده.
- [ ] راهنماهای دامنه (`BACKEND-RULES-GUIDE.md` / `FRONTEND-RULES-GUIDE.md`) در صورت تاثیر آپدیت شده‌اند.

## F) PR Readiness

- [ ] هدف تغییرات Ruleها در PR توضیح داده شده.
- [ ] موارد ریسک/تعارض احتمالی ذکر شده.
- [ ] plan بازگشت (revert) در صورت رفتار نامطلوب مشخص است.
````
