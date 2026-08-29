# Onboarding همکار توسعه

**مخاطب:** مالک ریپو و همکار جدید.  
**جزئیات تکرار نمی‌شود؛** این صفحه فهرست تصمیم‌ها و لینک به SSOT است.

سیاست Git: [`.cursor/rules/share/gitflow-branch-policy.mdc`](../../.cursor/rules/share/gitflow-branch-policy.mdc) و Skill [`gitflow-workflow`](../../.cursor/skills/gitflow-workflow/USER-GUIDE.md).  
نقشهٔ محصول: [`DEVELOPMENT_TO_DEPLOY.md`](./DEVELOPMENT_TO_DEPLOY.md).  
UI یک‌طرفه: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md).

---

## مدل همکاری (doion)

| موضوع | تصمیم |
|--------|--------|
| Clone یا Fork؟ | **Clone** از `alamalhoda/doion` |
| نقش GitHub | Collaborator با **Write**، نه Admin |
| کار روزانه | `feature/*` یا `bugfix/*` روی همین origin |
| ادغام | فقط **PR به `develop`** |
| `develop` محلی | فقط آینه؛ commit ممنوع؛ `git pull --ff-only` |
| همگام‌سازی | سه نقطه: شروع Task، قبل از PR (پیش‌فرض **merge**)، بعد از merge |

Fork برای همکار داخلی لازم نیست. ریپوی خالی در اکانت همکار مسیر PR به این repo نیست.

Cursor: ریشهٔ **doion** را باز کن. Rules در `.cursor/rules/` و Skills در `.cursor/skills/` با clone می‌آیند. تنظیمات شخصی Cursor (`~/.cursor/skills/`، User Rules) را کپی نکن.

---

## مدل همکاری (checkyar-googleai)

| موضوع | تصمیم |
|--------|--------|
| نقش GitHub همکار | حداکثر **Read** (clone + `git pull`) |
| تغییر سورس UI | فقط **Google AI Studio** |
| Cursor / لپ‌تاپ | `bun install` و اجرا؛ **commit/push نکن** |
| ویرایش همزمان Studio | یک UI Editor در هر لحظه |

جزئیات اجرا و Vite: [`FRONTEND_DEVELOPMENT_STATUS.md`](./FRONTEND_DEVELOPMENT_STATUS.md). باگ UI: Skill `ai-studio-ui-fix-loop` (پرامپت برای Studio؛ پوش از لوکال نه).

---

## روز اول همکار

1. دعوت GitHub را قبول کن (`doion` = Write، UI = Read).
2. هر دو ریپو را clone کن. `origin` باید ریپوی `alamalhoda` باشد.
3. `doion`: `develop` را `pull --ff-only` کن؛ venv: `source backend/.venv/bin/activate`.
4. Cursor را روی ریشهٔ `doion` باز کن؛ `AGENTS.md` و [`MASTER_API_CONTRACT.md`](./MASTER_API_CONTRACT.md) را ببین.
5. UI: `git pull`، Bun، `.env` لوکال (`VITE_USE_MOCK=false`، API روی `http://localhost:8000/api/v1`) — فایل را commit نکن.
6. اولین کار: نقطهٔ ۱ GitFlow → `feature/<یک-هدف>`.

---

## چک‌لیست مالک (تنظیم GitHub؛ در git نیست)

این‌ها را در Settings ریپو بزن؛ فایل این سند جایگزین UI گیت‌هاب نمی‌شود.

- [ ] Collaborator `doion` = Write؛ Admin نده
- [ ] `checkyar-googleai` حداکثر Read
- [ ] Protection / ruleset روی `main` و `develop` (PR اجباری، بدون force-push، بدون حذف شاخه)
- [ ] Required checks روی PR به `develop`: **Ruff** و **pytest** (E2E merge-gate نیست)
- [ ] **Automatically delete head branches**
- [ ] Require review از CODEOWNERS برای `.github/` در صورت وجود plan مناسب
- [ ] Release / CD و secretهای چابکان فقط برای مالک
- [ ] مشخص کن چه کسی UI Editor استودیو است (رمز حساب شخصی را share نکن)

`CODEOWNERS` در [`.github/CODEOWNERS`](../../.github/CODEOWNERS) مسیرهای حساس را مشخص می‌کند؛ تا «Require review from code owners» روشن نشود فقط راهنماست.
