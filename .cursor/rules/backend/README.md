# Backend Rules — Django/DRF

قوانین backend برای پروژه Django (`backend/`).

**راهنما:** `BACKEND-RULES-GUIDE.md` — مستند دسته‌بندی‌شدهٔ تمام قوانین و نقشهٔ فایل‌های `.mdc` (فایل راهنما، نه قانون).
  
**نسخه تجمیعی کامل:** `BACKEND-RULES-FULL.md` — تجمیع کامل محتوای همه Ruleهای `.mdc` بدون خلاصه‌سازی.

## Shared Rules (سراسری)

قوانین مشترک پروژه در پوشه `../share/` قرار دارند و برای backend نیز اعمال می‌شوند:

- `share/gitflow-branch-policy.mdc`
- `share/engineering-principles.mdc`
- `share/code-quality-baseline.mdc`

## ساختار

```
backend/
├── README.md                    # این فایل
├── BACKEND-RULES-GUIDE.md       # راهنما و مستند (مرجع دسته‌بندی‌شده)
├── BACKEND-RULES-FULL.md        # محتوای کامل همه قوانین backend
│
├── core/                        # قوانین پایه
│   ├── ai-guardrails.mdc        # AI محدودیت‌ها (alwaysApply: true)
│   ├── design-principles.mdc    # SOLID، DRY، KISS، SSOT
│   ├── git-workflow.mdc         # Branch/commit (aligned with share/gitflow-branch-policy.mdc)
│   └── quick-reference.mdc      # AI Checklist (alwaysApply: true)
│
├── architecture/                # معماری Django
│   └── django-architecture.mdc  # View/Service/Serializer، business logic
│
├── api/                         # API و REST
│   └── rest.mdc                 # HTTP methods، status codes، response structure
│
├── python/                      # پایتون
│   └── best-practices.mdc       # Type hints، context manager، exception
│
├── database/                    # دیتابیس
│   └── models.mdc               # Migrations، ORM، transactions
│
├── security/                    # امنیت
│   └── security.mdc             # Permissions، secrets، password hashing
│
├── performance/                 # عملکرد
│   └── optimization.mdc         # N+1، select_related، caching
│
├── logging/                     # لاگ
│   └── monitoring.mdc           # سطوح logging، چه چیزی log شود
│
├── configuration/               # تنظیمات
│   └── settings.mdc             # settings، env، django-environ
│
├── testing/                     # تست
│   └── strategy.mdc             # APITestCase، AAA، coverage
│
├── patterns/                    # الگوها
│   ├── progressive-development.mdc  # Feature flags، deprecation
│   └── anti-patterns.mdc        # God class، magic numbers، ...
│
└── documentation/               # مستندسازی
    └── file-header.mdc          # Minimal و Full header
```

## Globs (محدوده اثر)

| فایل | Globs | alwaysApply |
|------|-------|-------------|
| ai-guardrails.mdc | `backend/**/*.py` | false |
| quick-reference.mdc | `backend/**/*.py` | false |
| design-principles.mdc | `backend/**/*.py` | false |
| git-workflow.mdc | `backend/**/*`, `.github/**/*` | false |
| django-architecture.mdc | `**/views.py`, `**/serializers.py`, `**/urls.py` | false |
| rest.mdc | `**/views.py`, `**/serializers.py`, `**/urls.py` | false |
| best-practices.mdc | `backend/**/*.py` | false |
| models.mdc | `**/models.py`, `**/migrations/*.py` | false |
| security.mdc | `**/views.py`, `**/serializers.py`, `**/settings*.py` | false |
| optimization.mdc | `**/views.py`, `**/models.py` | false |
| monitoring.mdc | `backend/**/*.py` | false |
| settings.mdc | `**/settings*.py`, `.env*` | false |
| strategy.mdc | `**/test*.py`, `**/tests/**/*.py` | false |
| progressive-development.mdc | `backend/**/*.py` | false |
| anti-patterns.mdc | `backend/**/*.py` | false |
| file-header.mdc | `backend/**/*.py` | false |

## نحوه کار

* هنگام ویرایش فایل در `backend/`، Cursor بر اساس globها، فایل‌های rule مربوط را بارگذاری می‌کند.
* همه قوانین backend با globهای مرتبط اعمال می‌شوند (file-scoped).
* baselineهای سراسری از پوشه `share/` مستقل از دامنه اعمال می‌شوند.
