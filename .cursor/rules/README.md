# Cursor Rules — OilChenger Monorepo

قوانین توسعه در ریشه مونورپو اعمال می‌شوند. هر قانون با **globs** به مسیر مشخص (مثلاً `frontend/**` / `frontend-legacy/**` یا `backend/**`) محدود می‌شود.

> **UI فعال:** فعلاً خارج از این مونورپو است ([checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai)). درخت اپلیکیشن آرشیو: `frontend-legacy/`. جزئیات: `docs/development/FRONTEND_DEVELOPMENT_STATUS.md`. پوشه `.cursor/rules/frontend/` همچنان قوانین *مهندسی* UI است (نه مسیر اپ فعال).

## تفکیک فیزیکی

- **share/** — قوانین مشترک و جهان‌شمول (global baseline). راهنما: `share/README.md`.
- **frontend/** — همه قوانین مخصوص واسط کاربری (frontend: Vue 3، Vite، Pinia). راهنما: `frontend/FRONTEND-RULES-GUIDE.md`.
- **backend/** — قوانین backend (Django، DRF، API، دیتابیس، امنیت، تست و …).
- **\_archive/** — قوانین قدیمی فقط برای مرجع (مثلاً Svelte).

با این ساختار قوانین UI و backend قاطی نمی‌شوند.

## ساختار پوشه‌ها

```
.cursor/rules/
├── share/              # قوانین مشترک پروژه (global)
│   ├── README.md
│   ├── SHARE-RULES-GUIDE.md     # راهنمای دسته‌بندی‌شده قوانین share
│   ├── SHARE-RULES-FULL.md      # تجمیع کامل محتوای تمام قوانین share
│   ├── gitflow-branch-policy.mdc
│   ├── engineering-principles.mdc
│   ├── code-quality-baseline.mdc
│   ├── rule-precedence.mdc
│   ├── documentation-sync-policy.mdc
│   ├── rule-authoring-standard.mdc
│   └── rules-audit-checklist.mdc
├── frontend/           # همه قوانین واسط کاربری
│   ├── FRONTEND-RULES-GUIDE.md  # راهنما و مستند دسته‌بندی‌شده
│   ├── FRONTEND-RULES-FULL.md   # تجمیع کامل محتوای تمام قوانین frontend
│   ├── core/           # AI behavior، meta-principles، git، code quality
│   ├── architecture/   # ساختار پروژه، Atomic Design، SOLID، component design
│   ├── patterns/       # props-emits، reactivity، component-patterns، api، anti-patterns
│   ├── state/          # Pinia، local vs global
│   ├── performance/    # Bundle، Core Web Vitals، optimization، runtime، assets
│   ├── ui-ux/          # Accessibility، responsive، styling، user-feedback، interaction-patterns
│   ├── testing/        # Strategy، unit (Vitest + Vue)، e2e
│   └── tools/          # Vue 3، Vite
├── backend/            # قوانین backend (Django/DRF)
│   ├── README.md
│   ├── BACKEND-RULES-FULL.md    # تجمیع کامل محتوای تمام قوانین backend
│   ├── core/           # AI guardrails، design principles، git، quick-ref
│   ├── architecture/   # Django architecture
│   ├── api/            # REST rules
│   ├── python/         # Python best practices
│   ├── database/       # Models، migrations
│   ├── security/       # Permissions، secrets
│   ├── performance/    # N+1، caching
│   ├── logging/        # Monitoring
│   ├── configuration/  # Settings
│   ├── testing/        # APITestCase، coverage
│   ├── patterns/       # Progressive dev، anti-patterns
│   └── documentation/  # File header
├── _archive/           # قوانین قدیمی (مرجع)
│   └── svelte/
└── README.md
```

## Globها

- در **share/** برخی Ruleها baseline سراسری (`alwaysApply: true`) هستند و برخی Ruleها فقط هنگام تغییر خود قوانین (`.cursor/rules/**`) فعال می‌شوند.
- قوانین داخل **frontend/** از globهای `frontend/**` (یا الگوی دقیق‌تر مثل `frontend/src/**/*.vue`) استفاده می‌کنند.
- قوانین داخل **backend/** از globهای `backend/**/*.py` و الگوهای تخصصی‌تر (مثلاً `**/models.py`, `**/test*.py`) استفاده می‌کنند. جزئیات در `backend/README.md`.

## اولویت قواعد

1. `share/` (قواعد عمومی)
2. `frontend/` یا `backend/` (قواعد تخصصی دامنه)
3. هنگام تعارض، rule تخصصی دامنه اولویت دارد.

## AlwaysApply Budget

- بودجه هدف: حداکثر `5` Rule با `alwaysApply: true`
- وضعیت فعلی: `5/5` (فقط در `share/`؛ شامل `python-venv-policy.mdc`)
- Ruleهای domain باید file-scoped باشند (`alwaysApply: false` + `globs`)

## نحوه استفاده

1. workspace را روی ریشه مونورپو (OilChenger) باز کن.
2. هنگام کار روی فایل‌های داخل `frontend/`، Cursor قوانین داخل `frontend/` را بر اساس glob اعمال می‌کند.
3. هنگام کار روی `backend/`، قوانین داخل `backend/` بر اساس glob اعمال می‌شوند.
