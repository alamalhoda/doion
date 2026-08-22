# Implementation Plan — CI/CD بعدی

Chat اجراکننده در هر نشست **یک گام** را پیاده می‌کند، Verify می‌نویسد، و منتظر تأیید می‌ماند. گام‌های این فایل همه `[ ]` هستند تا با پلن تمام‌شدهٔ `cicd-chabokan-prod` قاطی نشوند.

نقشهٔ فشرده برای انسان: [`docs/development/CICD_NEXT_ROADMAP.md`](../../../docs/development/CICD_NEXT_ROADMAP.md).  
مشخصات و قفل‌ها: [`feature_spec.md`](./feature_spec.md).

Scope: FULL-STACK (AUTOMATION)

## وضعیت مبدأ (۲۲ اوت ۲۰۲۶)

- پلن `cicd-chabokan-prod` گام ۱–۱۳ انجام شده.
- زنده: API `chequeyar-back`، SPA Static `royasoft.dev`، دمو `royasoftgroup.ir`.
- آخرین تگ آزمایشی مستند: `v0.1.0-test.2` (تگ ≠ CD).
- CD Backend: `chabok deploy` سورس Django. CD Product: باندل Static + بازنویسی `chabok.json` روی runner.

---

## فاز A — سخت‌کاری کم، ریسک کم (همین خط محصول)

هدف: پیش‌فرض‌ها و حفاظت merge با واقعیت زنده یکی شود. بدون تغییر مدل استقرار.

- [ ] **Step A1 — cicd-backend: CORS و دامنه در کد و سند**  
  ریپو: `doion`.  
  - پیش‌فرض `CORS_ALLOWED_ORIGINS` در settings تولید با origin واقعی (`https://royasoft.dev` و در صورت استفاده `www`) هم‌خوان شود؛ مقدار پنل را حدس نزن — با سند `PRODUCTION_CHABOKAN_DEPLOY.md` و مالک چک کن.  
  - اگر `*.chbkn.dev` فرانت بعد از دامنهٔ سفارشی timeout است، در همان سند بنویس کدام URL پشتیبانی می‌شود.  
  **Verify:** سند و پیش‌فرض کد با پنل یکی است؛ لاگین از royasoft.dev قطع CORS ندارد.  
  **خارج:** عوض کردن نوع سرویس چابکان.

- [ ] **Step A2 — cicd-backend: حفاظت شاخهٔ `develop`**  
  - Ruleset یا classic protection: Check **CI Backend** (Ruff + pytest) برای merge به `develop` required شود.  
  - E2E را در این گام required نکن.  
  - مستقیم روی `develop`/`main` هنوز commit نشود (GitFlow).  
  **Verify:** PR بدون CI سبز merge نمی‌شود (یا مالک صریحاً bypass را مستند کرده).  
  **نکته:** این تنظیم در GitHub است نه لزوماً فایل workflow.

- [ ] **Step A3 — هر دو ریپو: هشدار Node 20 اکشن‌ها**  
  - `actions/checkout` و `actions/setup-node` (و مشابه) را به نسخه‌ای ببر که runtime پشتیبانی‌شده GitHub باشد.  
  فرانت: پرامپت Studio؛ بک‌اند: PR به `develop`.  
  **Verify:** CI سبز؛ هشدار Node 20 روی jobهای اصلی نماند.  
  **خارج:** بازنویسی کل pipeline.

- [ ] **Step A4 — cicd-frontend: SSOT نام سرویس چابکان برای محصول**  
  - workaround فعلی (بازنویسی `chabok.json` روی runner چون CLI به `-s` بی‌اعتناست اگر فایل committed نام دمو باشد) را با یکی از این‌ها عوض کن، بعد از تأیید مالک: فایل جدا برای محصول، یا CLI اگر رفتارش عوض شده، یا مسیر documented پایدار.  
  **Verify:** CD Product روی `product` به `chequeyar-front` می‌رود نه دمو؛ `cd-demo.yml` دست‌نخورده.  
  پرامپت Studio؛ Cursor پوش UI نکند.

---

## فاز B — ایمنی استقرار (هنوز سورس/Static)

هدف: دکمهٔ CD سخت‌تر اشتباه بخورد؛ هنوز pull ایمیج لازم نیست.

- [ ] **Step B1 — cicd-backend: GitHub Environment برای CD Backend**  
  - Environment مثلاً `production-api`؛ secrets مربوط به چابکان روی Environment نه فقط repo اگر مالک بخواهد.  
  - Protection: reviewer اختیاری — از مالک بپرس (قانون spec).  
  **Verify:** CD Backend بدون عبور از Environment اجرا نمی‌شود؛ `workflow_dispatch` سر جایش است.

- [ ] **Step B2 — cicd-frontend: Environment برای CD Product**  
  - مشابه B1 روی ریپوی UI؛ شاخهٔ اجرا همچنان `product`.  
  **Verify:** Run از `main` به‌اشتباه محصول را عوض نمی‌کند (یا job صریحاً رد می‌کند).  
  پرامپت Studio.

---

## فاز C — آرتیفکت = runtime (بزرگ‌ترین جهش)

**توقف اجباری:** قبل از C1 از مالک جواب دو سؤال spec را بگیر (GHCR روی پنل بک‌اند؛ Static در برابر Docker برای فرانت). بدون آن حدس نزن.

- [ ] **Step C1 — تصمیم پنل + سند**  
  - در REVIEW NOTE بنویس: آیا `chequeyar-back` می‌تواند `ghcr.io/alamalhoda/doion-api:<tag>` را pull کند؟ آیا فرانت Static می‌ماند؟  
  - اگر پنل ایمیج خصوصی را نمی‌کشد، این فاز را متوقف کن و مسیر جایگزین (مثلاً رجیستری چابکان) را با مالک قفل کن.  
  **Verify:** تصمیم مکتوب است؛ هنوز deploy زنده عوض نشده مگر مالک در همین گام بخواهد.

- [ ] **Step C2 — cicd-backend: CD از ایمیج GHCR نه بیلد سورس PaaS**  
  - CD Backend تگ Release را به همان ایمیج موجود وصل کند (وجود ایمیج از قبل چک می‌شود).  
  - migrate/run مطابق entrypoint فعلی ایمیج؛ SQLite محصول ممنوع.  
  **Verify:** یک تگ آزمایشی (با تأیید مالک) روی زنده همان digest GHCR را اجرا می‌کند؛ لاگ پنل بیلد cookiecutter از سورس نیست.  
  **Rollback:** آخرین تگ موفق قبلی با همان دکمه.

- [ ] **Step C3 — فرانت: یا Static بماند یا ایمیج**  
  - اگر Static: C2 فقط بک‌اند است؛ ایمیج `chequeyar-front` همچنان آرتیفکت Release می‌ماند.  
  - اگر Docker: پرامپت Studio + تأیید پنل؛ `nginx.conf` و `VITE_*` بakeشده در ایمیج؛ دمو mock را به ایمیج محصول وصل نکن.  
  **Verify:** royasoft.dev باندل زنده است؛ دمو mock جدا.

---

## فاز D — کیفیت به‌عنوان gate (بعد از پایدار شدن CD)

E2E را required نکن تا flake و پین UI دردسر merge روزانه نشود.

- [ ] **Step D1 — cicd-backend: سیاست E2E required**  
  - گزینهٔ پیشنهادی: required فقط روی مسیر انتشار (مثلاً قبل از Release یا قبل از CD) نه روی هر PR کوچک به `develop`.  
  - اگر required روی PR `develop` خواسته شد: فقط smoke؛ critical جدا بماند. از مالک بپرس.  
  **Verify:** سیاست در `CHABOKAN_CD_AND_PRODUCT_BRANCH.md` و این پلن یکی است؛ GitFlow bump پین حفظ شود.

- [ ] **Step D2 — Release: پین UI با `product` هم‌تراز**  
  - قبل از بریدن تگ، job یا چک‌لیست: `e2e/ui-pin` = SHA شاخهٔ `product` (یا commit ادغام‌شدهٔ همان SPA).  
  **Verify:** ایمیج `chequeyar-front` تگ جدید همان UI محصول است نه SHA قدیمی.

---

## فاز E — زنجیرهٔ تأمین و مشاهده‌پذیری محصول

- [ ] **Step E1 — پین SHA اکشن‌های سوم‌شخص**  
  - checkout/setup را با SHA کامل پین کن یا Dependabot برای Actions.  
  هر دو ریپو؛ فرانت با Studio.  
  **Verify:** CI/CD سبز؛ tag شناور `@v4` تنها منبع نیست.

- [ ] **Step E2 — changelog داخل اپ**  
  - طبق [`PRODUCT_CHANGELOG.md`](../../../docs/development/PRODUCT_CHANGELOG.md)؛ اول قرارداد API در `MASTER_API_CONTRACT.md` با PR جدا، بعد UI Studio.  
  **Verify:** یک Release در اپ دیده می‌شود؛ اسرار در متن نیست.

- [ ] **Step E3 — HSTS تدریجی**  
  - `SECURE_HSTS_SECONDS` بعد از تثبیت HTTPS دامنهٔ سفارشی؛ مقدار را یک‌شبه سال نکن.  
  **Verify:** هدر روی royasoft.dev / API مطابق تصمیم مالک.

---

## صریحاً در این پلن نیست

| مورد | چرا |
|------|-----|
| staging جدید | مالک باید جدا تصمیم بگیرد |
| CD خودکار روی merge | خلاف قانون تأیید استقرار |
| تگ روی UI | SemVer فقط doion Release |
| Compose کامل Django+SPA به‌عنوان تنها مسیر لوکال | مسیر A/B فعلی معتبر بماند |

## ترتیب پیشنهادی اجرا

`A1 → A2 → A3 → A4 → B1 → B2 → (تصمیم C1) → C2 → C3 → D2 → D1 → E1 → E2 → E3`

اگر وقت کم است: **A2 سپس C1/C2**. بقیه را وقتی درد عملی دیدید.
