# Shared Rules Index

این فایل مرجع رسمی قوانین مشترک (`global`) در پروژه است.

**راهنما:** `SHARE-RULES-GUIDE.md` — نقشه و توضیح دسته‌بندی‌شده قوانین `share`.
  
**نسخه تجمیعی کامل:** `SHARE-RULES-FULL.md` — تجمیع کامل محتوای همه Ruleهای `.mdc` بدون خلاصه‌سازی.

## هدف

- تعریف قوانین جهان‌شمول که باید در همه دامنه‌ها (backend/frontend/...) اعمال شوند.
- جلوگیری از تکرار قوانین یکسان در پوشه‌های تخصصی.
- شفاف‌سازی اولویت اعمال Ruleها.

## فایل‌های فعال در `share/`

| Rule | Role | Scope | alwaysApply |
|------|------|-------|-------------|
| `gitflow-branch-policy.mdc` | سیاست رسمی Git Flow، سه نقطهٔ sync، شاخهٔ کوتاه‌عمر | کل پروژه | ✅ true |
| `engineering-principles.mdc` | اصول مهندسی مشترک (SSOT/SoC/DRY/KISS/YAGNI/...) | کل پروژه | ✅ true |
| `code-quality-baseline.mdc` | baseline کیفیت کد (خوانایی، naming، magic values، secrets، test expectation) | کل پروژه | ✅ true |
| `rule-precedence.mdc` | سیاست رسمی اولویت و حل تعارض Ruleها | کل پروژه | ✅ true |
| `python-venv-policy.mdc` | قبل از اجرای دستور پایتون، محیط مجازی باید فعال شود (`source backend/.venv/bin/activate`) | کل پروژه | ✅ true |
| `semver-release-policy.mdc` | تگ SemVer فقط از workflow `Release`؛ نه `git tag` روی feature. آموزش: `docs/development/GIT_TAGS_AND_RELEASES.md` | workflow Release + مکالمات تگ | false |
| `active-frontend-toolchain.mdc` | UI فعال (`checkyar-googleai`): Bun SSOT، `bun.lock`، بدون `package-lock.json`، یادآوری one-way AI Studio | docs وضعیت فرانت | false |
| `documentation-sync-policy.mdc` | الزام همگام‌سازی TODO/README/PLAN و اسناد توسعه بعد از تغییرات مهم و قبل از PR | کد + مستندات پروژه | false |
| `rule-authoring-standard.mdc` | استاندارد نگارش/جایگذاری Ruleها | فقط تغییرات قوانین (`.cursor/rules/**`) | false |
| `rules-audit-checklist.mdc` | چک‌لیست قابل اجرا برای PRهای مربوط به Ruleها | فقط تغییرات قوانین (`.cursor/rules/**`) | false |

## Rule Priority (اولویت اعمال)

1. **Global rules** در `share/` به عنوان baseline مشترک
2. **Domain rules** در `backend/` و `frontend/` برای جزئیات تخصصی
3. در صورت تعارض، **rule تخصصی دامنه** نسبت به rule عمومی ارجح است
4. جزئیات precedence رسمی در `rule-precedence.mdc` تعریف شده است

## مرزبندی مسئولیت

- `share/`: فقط اصول عمومی، پایدار و cross-domain
- `backend/`: قواعد تخصصی Django/DRF و معماری backend
- `frontend/`: قواعد تخصصی Vue/UI/UX و الگوهای frontend

## Maintenance Policy

- قبل از افزودن Rule جدید، بررسی کن آیا موضوع واقعاً عمومی است یا تخصصی.
- اگر عمومی است، در `share/` اضافه کن و از تکرار در دامنه‌ها پرهیز کن.
- اگر تخصصی است، در پوشه دامنه نگه دار و فقط در صورت نیاز به Rule عمومی ارجاع بده.

## AlwaysApply Budget

- بودجه هدف: حداکثر `5` Rule با `alwaysApply: true` در کل پروژه
- `alwaysApply: true` فقط برای Ruleهای global کم‌حجم
- Ruleهای تخصصی دامنه باید با `globs` فعال شوند
