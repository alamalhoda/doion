# راهنمای قوانین Share (Global Rules)

> این سند **راهنما و مستند** قوانین `share` است، نه فایل قانون.  
> قوانین قابل اعمال در Cursor در فایل‌های `.mdc` قرار دارند.
>
> **English:** This document is a **guide and reference** for shared rules, not a rule file. Enforceable rules are in `.mdc` files.

---

## نقشهٔ فایل‌های قانون

هر بخش زیر به فایل `.mdc` مربوط اشاره می‌کند:

| بخش | فایل قانون | Scope | alwaysApply |
|-----|------------|-------|-------------|
| ۱. GitFlow Branch Policy | `gitflow-branch-policy.mdc` | کل پروژه | ✅ true |
| ۲. Engineering Principles | `engineering-principles.mdc` | کل پروژه | ✅ true |
| ۳. Code Quality Baseline | `code-quality-baseline.mdc` | کل پروژه | ✅ true |
| ۴. Rule Precedence | `rule-precedence.mdc` | کل پروژه | ✅ true |
| ۵. Rule Authoring Standard | `rule-authoring-standard.mdc` | `.cursor/rules/**/*.mdc`, `.cursor/rules/**/*.md` | false |
| ۶. Rules Audit Checklist | `rules-audit-checklist.mdc` | `.cursor/rules/**/*.mdc`, `.cursor/rules/**/*.md` | false |

---

## ۱. GitFlow Branch Policy — `gitflow-branch-policy.mdc`

**محتوا:** سیاست رسمی GitFlow برای branching، commit convention، sync قبل PR، و guardrailهای merge/push.

| موضوع | توضیح |
|-------|-------|
| Branch Model | `main`, `develop`, `feature/*`, `bugfix/*`, `release/*`, `hotfix/*` |
| Safety Rules | منع commit مستقیم روی `main/develop`، منع `--force` |
| PR Flow | sync با `origin/develop`، چک‌لیست قبل از PR |
| Merge Rule | شاخه فعلی = مقصد merge |

---

## ۲. Engineering Principles — `engineering-principles.mdc`

**محتوا:** اصول مهندسی عمومی و cross-domain برای کل پروژه.

| اصل | توضیح |
|-----|-------|
| SSOT | یک منبع حقیقت برای هر منطق |
| SoC | جداسازی UI/transport، business، data access |
| DRY/KISS/YAGNI | کاهش تکرار، سادگی، پرهیز از پیش‌پیچیدگی |
| Explicitness | قراردادهای صریح ورودی/خروجی/خطا |

---

## ۳. Code Quality Baseline — `code-quality-baseline.mdc`

**محتوا:** baseline کیفیت کد که همه دامنه‌ها باید رعایت کنند.

| موضوع | توضیح |
|-------|-------|
| Readability | کد خوانا و قابل نگهداری |
| Naming | نام‌گذاری توصیفی |
| Magic Values | پرهیز از magic numbers/strings |
| Security | منع hard-coded secrets |
| Testing | نیاز به تست یا plan تست برای تغییرات حیاتی |

---

## ۴. Rule Precedence — `rule-precedence.mdc`

**محتوا:** ترتیب اولویت Ruleها و روش حل تعارض بین Ruleهای global/domain/file-specific.

| موضوع | توضیح |
|-------|-------|
| Priority Chain | System → Share → Domain → File-specific → Style |
| Conflict Policy | scope محدودتر ارجح، security/correctness بالاتر از style |
| Mandatory Behavior | اعلام تعارض + ریسک + سؤال روشن در ابهام |

---

## ۵. Rule Authoring Standard — `rule-authoring-standard.mdc`

**محتوا:** استاندارد ساخت/نگهداری Ruleها، naming، placement، و بودجه `alwaysApply`.

| موضوع | توضیح |
|-------|-------|
| Placement | Global در `share`، domain-specific در `backend/frontend` |
| Naming | `kebab-case` و الگوهای policy/checklist/standards |
| AlwaysApply Budget | هدف حداکثر ۵ Rule سراسری |
| Content Quality | action-oriented، کم‌تکرار، دارای guardrail |

---

## ۶. Rules Audit Checklist — `rules-audit-checklist.mdc`

**محتوا:** چک‌لیست اجرایی برای PRهای تغییر Rule (scope، frontmatter، تعارض، مستندات، readiness).

| بخش | پوشش |
|-----|------|
| Scope/Placement | محل درست Rule و جلوگیری از overlap |
| Frontmatter | صحت `description`/`alwaysApply`/`globs` |
| Conflict/Precedence | همخوانی با `rule-precedence.mdc` |
| Docs Sync | بروزرسانی README/GUIDEها |

---

## نحوهٔ استفاده

- برای فهم سریع نقش Ruleها از همین فایل استفاده کن.
- برای مشاهده متن کامل Ruleها از `SHARE-RULES-FULL.md` استفاده کن.
- برای اعمال واقعی Ruleها، فقط فایل‌های `.mdc` ملاک هستند.
