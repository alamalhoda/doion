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
2. پرامپت آماده برای Google AI Studio می‌نویسد.
3. بعد از اینکه شما commit را از Studio آوردید: `git pull`، بررسی diff، و در صورت نیاز smoke/تست.

## چه کار نمی‌کند

- به AI Studio مستقیم وصل نمی‌شود؛ شما پرامپت را کپی می‌کنید.
- سورس UI را از لوکال به GitHub پوش نمی‌کند (قانون one-way).

## پیش‌نیاز لوکال

- کلون `checkyar-googleai` با `VITE_USE_MOCK=false`
- بک‌اند doion (ترجیحاً demo seed) روی `:8000`
- Bun برای UI

جزئیات: `docs/development/FRONTEND_DEVELOPMENT_STATUS.md` و `docs/development/E2E_LOCAL_RUNBOOK.md`.
