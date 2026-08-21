# راهنمای کاربر — AI Studio UI Fix Loop

Skill پروژه: `.cursor/skills/ai-studio-ui-fix-loop/`

این Skill **فقط وقتی صریح نام ببرید** فعال می‌شود (auto-invoke ندارد).

## چگونه صدا بزنید

در چت Cursor یکی از این‌ها را بگویید:

- «Skill `ai-studio-ui-fix-loop` را اجرا کن»
- «حلقه اصلاح UI با AI Studio را برای این خطا اجرا کن»
- `@ai-studio-ui-fix-loop` (اگر UI شما skill را به‌صورت mention نشان دهد)

## چه کار می‌کند

1. خطای Live را تشخیص می‌دهد (UI vs backend vs استفاده اشتباه).
2. پرامپت آماده برای Google AI Studio می‌نویسد (کد + در صورت نیاز vitest و docs دوزبانه).
3. بعد از commit از Studio: `git pull`، بررسی diff (کد/تست UI/docs)، و در صورت نیاز E2E در `doion/e2e`.

## چه کار نمی‌کند

- به AI Studio مستقیم وصل نمی‌شود؛ شما پرامپت را کپی می‌کنید.
- سورس UI، vitest، یا docs UI را از لوکال به GitHub پوش نمی‌کند (قانون one-way).
- تست Playwright را داخل repo UI اضافه نمی‌کند؛ آن‌ها در `doion/e2e` می‌مانند.
- تگ گیت روی `checkyar-googleai` نمی‌زند. نسخهٔ محصول همان تگ doion **Release** است (API + SPA). بعد از تغییر قابل‌دیدن کاربر و رفتن به `product`، یک‌بار یادآوری تگ می‌کند.

## Changelog محصول (آینده)

متن کوتاه FA+EN از Studio جمع می‌شود. نمایش داخل اپ (نسخه + تاریخ + خلاصهٔ سرور و کلاینت) در `docs/development/PRODUCT_CHANGELOG.md` مشخص شده؛ در باگ‌فیکس معمولی صفحهٔ Versions ساخته نمی‌شود. آموزش تگ محصول: `docs/development/GIT_TAGS_AND_RELEASES.md`.

## Docs اول‌بار

اگر هنوز `docs/ARCHITECTURE*.md` / `docs/TESTING*.md` در UI نیست، یک‌بار پرامپت bootstrap را به Studio بدهید:

`docs/development/AI_STUDIO_DOCS_BOOTSTRAP_PROMPT.md`

## پیش‌نیاز لوکال

- کلون `checkyar-googleai` با `VITE_USE_MOCK=false`
- بک‌اند doion (ترجیحاً demo seed) روی `:8000`
- Bun برای UI

جزئیات: `docs/development/FRONTEND_DEVELOPMENT_STATUS.md` و `docs/development/E2E_LOCAL_RUNBOOK.md`.
