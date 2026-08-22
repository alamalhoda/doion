# Feature Specification — CI/CD بعدی (پس از محصول روی چابکان)

این پوشه **نسخهٔ بعدی** اتوماسیون است. نسخهٔ فعلی (`cicd-chabokan-prod`، گام‌های ۱–۱۳) کامل و روی زنده Verify شده است؛ آن پلن را دوباره باز نکنید.

مخاطب: مالک ریپو و Chat بعدی که این نقشه را اجرا می‌کند.  
تاریخ مبنا: ۲۲ اوت ۲۰۲۶.

- **Scope:** FULL-STACK (AUTOMATION؛ رفتار کسب‌وکار REST عوض نمی‌شود مگر قرارداد جدا)
- **Capability types:** AUTOMATION
- **ریپوی اجرا:** `doion` (GitFlow) + پرامپت Studio برای `checkyar-googleai` (Cursor به UI پوش نمی‌کند)

## 1. Baseline که نباید خراب شود

| قرارداد | وضعیت فعلی |
|---------|------------|
| PR به `develop` | CI Backend: Ruff + pytest روی Postgres؛ بدون fallback SQLite |
| لوکال | SQLite یا Postgres Compose؛ هیچ‌کدام تنها مسیر اجباری نیست |
| فرانت | Studio → `main`؛ تولید از شاخهٔ `product`؛ Cursor سورس UI را پوش نمی‌کند |
| دمو mock | `cd-demo.yml` و `chequeyar-front-demo` جدا از محصول |
| استقرار زنده | فقط `workflow_dispatch` مالک؛ بدون staging جدید در این نقشه مگر تصمیم صریح |
| SemVer | فقط workflow **Release** در doion؛ تگ روی ریپوی UI ممنوع |
| ایمیج | GHCR `doion-api` و `chequeyar-front` با همان تگ؛ **پنل هنوز سورس/Static CLI بیلد می‌کند** |
| E2E | بعد از push به `main` با `ui_sha`؛ gate ادغام PR بک‌اند نیست |
| REST | `/api/v1/` طبق `MASTER_API_CONTRACT.md` |

جزئیات انسانی مسیر فعلی: [`docs/development/DEVELOPMENT_TO_DEPLOY.md`](../../../docs/development/DEVELOPMENT_TO_DEPLOY.md).

## 2. هدف این نسخهٔ بعدی

سه چیز را بهتر کنید، بدون خودکار کردن استقرار روی هر merge:

1. **ایمنی merge و deploy** — چک اجباری واقعی روی `develop`؛ Environment گیت‌هاب برای CD.
2. **آرتیفکت = آنچه روی سرور می‌رود** — تگ GHCR همان بایتی باشد که چابکان اجرا می‌کند (نه بیلد دوباره از سورس روی PaaS).
3. **زنجیرهٔ تأمین و مشاهده‌پذیری** — اکشن‌های قابل‌اعتماد؛ در صورت نیاز changelog داخل اپ طبق [`PRODUCT_CHANGELOG.md`](../../../docs/development/PRODUCT_CHANGELOG.md).

## 3. قوانین قفل (نباید حدس زده شوند)

1. استقرار محصول بدون تأیید مالک (`workflow_dispatch` یا Environment approval) اضافه نشود.
2. `cd-demo.yml` و سرویس دمو را با CD محصول قاطی نکنید.
3. Cursor به `checkyar-googleai` commit/push نکند؛ تغییر workflow فرانت فقط پرامپت Studio.
4. تگ محصول روی feature branch یا ریپوی UI ساخته نشود.
5. محیط staging ساخته نشود مگر مالک در همان گام صریحاً بخواهد (پیش‌فرض این نقشه: نه).
6. `CHABOKAN_TOKEN` و PATها در git نروند.
7. نوع سرویس چابکان را بدون تأیید مالک عوض نکنید (الان فرانت **Static** است؛ کشیدن ایمیج SPA یعنی تصمیم پنل جدا).

## 4. خارج از این نقشه مگر تصمیم جدا

- deploy خودکار روی merge به `develop` یا `product`
- Git tag روی UI
- Playwright داخل ریپوی Vue
- Dependabot به‌عنوان پیش‌نیاز فاز آرتیفکت (می‌تواند موازی باشد، مسدودکننده نیست)
- صفحهٔ Versions داخل SPA قبل از قرارداد API changelog

## 5. تصمیم‌هایی که قبل از فاز آرتیفکت باید از مالک پرسیده شود

- آیا پنل چابکان برای `chequeyar-back` **کشیدن ایمیج از GHCR** را پشتیبانی می‌کند (رجیستری خصوصی + توکن)؟
- آیا محصول فرانت روی **Static** می‌ماند یا سرویس به **Docker image** برمی‌گردد؟
- آیا Environment `production` باید reviewer اجباری داشته باشد (علاوه بر کسی که Run workflow می‌زند)؟
