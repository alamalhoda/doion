# Feature Specification — CI/CD محصول روی چابکان

پوشهٔ این ویژگی در `doion` منبع مستند همهٔ گام‌هاست:

- `cicd-backend`: اجرا در ریپوی `doion` (GitFlow)
- `cicd-frontend`: فقط spec و پرامپت Google AI Studio (بدون commit/push از Cursor به `checkyar-googleai`)

## 1. Feature Overview

این ویژگی فرآیند یکپارچه‌سازی و تحویل محصول چک‌یار را روی PaaS چابکان به حالت قابل قبول می‌رساند. هر تغییر بک‌اند با Pull Request به `develop` توسط GitHub Checks رد یا قبول می‌شود. استقرار روی سرورهای **محصول** فقط پس از سبز بودن تست‌های اجباری همان انتشار و تأیید صریح مالک ریپو انجام می‌شود. محیط staging ساخته نمی‌شود. استقرار کاملاً خودکار بدون تأیید در این نسخه وجود ندارد.

فرانت همچنان از Google AI Studio روی GitHub پوش می‌شود و از Cursor به ریپوی UI commit/push نمی‌شود. چون Studio معمولاً PR نمی‌سازد، شاخهٔ `product` در کنار `main` مسیر تولید فرانت است: `main` محل ورود تغییرات Studio است؛ استقرار `chequeyar-front` فقط از `product` پس از PR و تأیید مالک انجام می‌شود.

مخاطبان انسانی مالک ریپو و همکاران توسعه‌اند. قرارداد REST محصول (`/api/v1/`) عوض نمی‌شود.

در توسعهٔ لوکال دو مسیر مجاز است: SQLite بدون Docker، یا Postgres داخل Docker. تست CI روی سرور و اجرای محصول فقط Postgres است؛ آنجا SQLite مجاز نیست.

- **Scope:** FULL-STACK
- **Capability types:** AUTOMATION
- **مخاطب انسانی:** مالک ریپوها و همکاران توسعه
- **مصرف‌کنندگان سیستمی:** GitHub Actions، استقرار چابکان، سرویس‌های `chequeyar-back` و `chequeyar-front`، GitHub Releases، ایمیج Docker، Compose اختیاری لوکال
- **ریپوی اجرا:** `doion` برای بک‌اند، E2E، Release/Docker بک‌اند، و این مستندات؛ `checkyar-googleai` فقط از مسیر AI Studio

## 2. Surfaces & Contract

### 2.1 UI (محصول چک‌یار)

این ویژگی صفحهٔ جدیدی در اپلیکیشن اضافه نمی‌کند. سطح قابل مشاهده برای انسان: وضعیت jobها در GitHub Actions / Checks.

### 2.2 cicd-backend (doion)

| رویداد | معنی |
|--------|------|
| باز شدن یا به‌روزرسانی PR به `develop` | اجرای تست اجباری: pytest و Ruff |
| توسعه / pytest لوکال مسیر SQLite | بدون Docker و بدون Postgres؛ انتخاب معتبر برای توسعه |
| توسعه / pytest لوکال مسیر Docker | Postgres داخل Docker؛ انتخاب معتبر برای همکار جدید |
| pytest در CI گیت‌هاب | فقط PostgreSQL؛ اگر Postgres آماده نباشد Check ناموفق است و به SQLite برنمی‌گردد |
| اجرای محصول `chequeyar-back` | فقط PostgreSQL |
| تأیید صریح مالک برای استقرار API | شروع deploy به `chequeyar-back` فقط اگر تست اجباری همان انتشار موفق باشد |
| شکست job استقرار API | Check ناموفق؛ محصول با deploy دستی نسخهٔ قبلی (آخرین انتشار موفق) برمی‌گردد — rollback خودکار پلتفرم الزامی نیست |

Playwright E2E در این نسخه **gate ادغام PR به `develop` نیست**.

پس از هر push به `main` در `checkyar-googleai`، یک اجرای E2E در `doion` علیه **همان commit فرانت** شروع می‌شود. نتیجه در GitHub Actions دیده می‌شود. شکست آن PR بک‌اند به `develop` را قرمز نمی‌کند.

### 2.3 cicd-frontend (checkyar-googleai، فقط Studio)

| رویداد | معنی |
|--------|------|
| push استودیو به `main` | CI فرانت: typecheck، unit tests، production build پیش‌فرض، و production build جدا با `VITE_USE_MOCK=false` |
| PR از `main` به `product` | همان تست‌های اجباری فرانت باید روی آن PR سبز باشند |
| تأیید مالک پس از PR سبز به `product` | deploy به `chequeyar-front` از باندل/ایمیج زنده (غیرmock) |
| سرویس `chequeyar-front-demo` | خارج از این ویژگی؛ CD فعلی mock دست‌نخورده می‌ماند |

تغییر فایل‌های workflow و Docker فرانت فقط با پرامپت AI Studio اعمال می‌شود.

### 2.4 Inputs & outputs

**ورودی‌ها**

| نام | نوع | الزام | محدودیت |
|-----|-----|--------|----------|
| PR به `develop` در doion | رویداد GitHub | بله برای CI بک‌اند | تست اجباری همین PR |
| push به `main` در checkyar-googleai | رویداد GitHub | بله برای CI فرانت و تریگر E2E غیرمسدودکننده | Studio PR نمی‌سازد |
| PR از `main` به `product` | رویداد GitHub | بله برای مسیر تولید فرانت | مالک این PR را باز و تأیید می‌کند |
| تأیید استقرار مالک | اقدام عمدی روی GitHub | بله برای هر deploy محصول | بدون آن محصول عوض نمی‌شود |
| `CHABOKAN_TOKEN` | راز GitHub | بله برای deploy | از قبل در Actions موجود است |
| متغیرهای محیط محصول | پنل چابکان | بله در runtime | از قبل روی سرویس‌ها هستند |
| `VITE_API_BASE_URL` برای build زنده | URL | بله در CI/build فرانت | `https://chequeyar-back.chbkn.dev/api/v1` |
| `VITE_USE_MOCK` برای build زنده | بولین | بله | باید `false` باشد |
| تگ SemVer | رشته SemVer | بله برای هر انتشار محصول | با GitHub Release همان commit |
| ایمیج Docker بک‌اند و فرانت | آرتیفکت | بله برای محصول | همان تگ SemVer |
| انتخاب موتور دادهٔ لوکال | SQLite یا Postgres در Docker | بله یکی از دو مسیر | هیچ‌کدام در لوکال اجباریِ تنها نیست |

**خروجی‌ها**

| خروجی | معنی |
|--------|------|
| GitHub Check موفق/ناموفق | تنها کانال گزارش به انسان |
| `chequeyar-back` | API محصول پس از deploy تأییدشده |
| `chequeyar-front` | SPA زنده روی PaaS Static پس از deploy تأییدشده (ایمیج GHCR آرتیفکت نسخه است، نه pull فعلی پنل) |
| GitHub Release + تگ SemVer | ردیابی commit مستقرشده |
| ایمیج Docker با همان تگ برای API و SPA | آرتیفکت استقرار و تکرار deploy دستی قبلی |
| اجرای E2E پس از push فرانت | نتیجه در Actions؛ غیرمسدودکننده برای PR بک‌اند |
| `chequeyar-front-demo` | بدون تغییر توسط این ویژگی |
| Compose/اسناد onboarding لوکال | مسیر اختیاری Postgres در Docker برای همکار؛ مسیر SQLite همچنان مستند و کار می‌کند |

## 3. Business Rules

1. هیچ محیط staging جدیدی در این ویژگی ایجاد یا الزامی نمی‌شود.
2. تست اجباری بک‌اند روی هر PR به `develop` در `doion` اجرا می‌شود و فقط وقتی Check سبز است که **pytest و Ruff** هر دو موفق باشند.
3. بدهی lint موجود باید در همین ویژگی پاک شود طوری که `ruff check` روی درخت بک‌اند در CI بدون چشم‌پوشی سراسری جدید قرمز نشود.
4. Playwright E2E gate ادغام PR بک‌اند نیست؛ افزودن آن به‌عنوان چک اجباری خارج از این نسخه است.
5. در توسعهٔ لوکال حق انتخاب وجود دارد: مسیر SQLite (بدون الزام Docker/Postgres) و مسیر Postgres داخل Docker هر دو پشتیبانی و مستند می‌شوند. هیچ‌کدام تنها مسیر اجباری توسعه نیست.
6. pytest در CI گیت‌هاب فقط با PostgreSQL اجرا می‌شود؛ آماده نبودن Postgres یعنی Check ناموفق است و CI به SQLite برنمی‌گردد.
6b. محصول (`chequeyar-back`) فقط PostgreSQL است؛ SQLite در محصول و در CI مجاز نیست.
7. تست اجباری فرانت شامل typecheck، unit tests، یک production build، و یک production build جدا با `VITE_USE_MOCK=false` است.
8. AI Studio به `main` پوش می‌کند و ملزم به ساخت PR برای هر تغییر روزمره نیست.
9. شاخهٔ `product` در `checkyar-googleai` شاخهٔ تولید فرانت است. استقرار `chequeyar-front` از `main` خام انجام نمی‌شود.
10. برای استقرار فرانت محصول، یک PR از `main` به `product` باز می‌شود؛ تست اجباری آن PR باید سبز باشد؛ سپس تأیید مالک لازم است.
11. استقرار `chequeyar-back` یا `chequeyar-front` بدون تأیید صریح مالک شروع نمی‌شود.
12. استقرار محصول فقط وقتی شروع می‌شود که تست‌های اجباری همان انتشار موفق بوده باشند.
13. استقرار کاملاً خودکار بدون تأیید در این نسخه وجود ندارد.
14. گزارش موفقیت یا شکست فقط در GitHub Actions/Checks است.
15. اگر job استقرار شکست بخورد، Check ناموفق است. بازیابی نسخهٔ قبلی با **تکرار deploy دستی/تأییدشدهٔ آخرین انتشار موفق** انجام می‌شود؛ rollback خودکار چابکان در این نسخه الزامی نیست.
16. هر انتشار محصول با GitHub Release و تگ SemVer روی همان commit قابل ردیابی است.
17. آرتیفکت انتشار شامل ایمیج Docker بک‌اند و ایمیج Docker فرانت با همان تگ SemVer است.
18. سورس UI و workflowهای `checkyar-googleai` از Cursor commit یا push نمی‌شوند.
19. قرارداد REST محصول در این ویژگی عوض نمی‌شود.
20. Dependabot، پین SHA اکشن‌های شخص ثالث، و GitHub Environments در این ویژگی الزامی نیستند.
21. CodeQL، coverage به‌عنوان gate، و Sentry در این ویژگی الزامی نیستند.
22. مخاطب pipeline مالک ریپو و همکاران توسعه است؛ تأیید استقرار محصول در این نسخه همچنان فقط با مالک است.
23. این ویژگی به سرویس `chequeyar-front-demo` و workflow CD دموی mock دست نمی‌زند.
24. پس از هر push به `main` فرانت، E2E دویون علیه همان commit فرانت اجرا می‌شود. شکست آن PR بک‌اند به `develop` را ناموفق نمی‌کند. پین commit UI در تنظیمات E2E دویون باید با همان commit هم‌تراز شود تا اجرای بعدی E2E روی همان نسخه باشد.
25. پیاده‌سازی در چند گام است: گام اجرایی اول فقط CI تست PR (و پاک‌سازی Ruff) است؛ CD محصول، Docker، SemVer/Release، شاخهٔ `product`، و همگام E2E در گام‌های بعدی plan می‌آیند — همه جزء تعریف کامل این ویژگی هستند.

## 4. Acceptance Scenarios

**Scenario 1: PR بک‌اند سبز**  
- Given: PR به `develop` در `doion`  
- When: Checks اجباری اجرا می‌شوند  
- Then: pytest روی PostgreSQL و Ruff هر دو موفق‌اند و Check سبز است  

**Scenario 2: شکست pytest یا Ruff**  
- Given: همان PR با خطای تست یا lint  
- When: CI تمام می‌شود  
- Then: Check ناموفق است؛ سرویس‌های محصول تغییر نمی‌کنند  

**Scenario 3: توسعه لوکال با SQLite**  
- Given: توسعه‌دهنده Docker/Postgres را برای داده انتخاب نکرده  
- When: سرور توسعه یا pytest لوکال اجرا می‌شود  
- Then: داده روی SQLite است و بدون کانتینر Postgres کار می‌کند  

**Scenario 3b: توسعه لوکال با Postgres در Docker**  
- Given: همکار مسیر Docker را طبق سند onboarding انتخاب کرده  
- When: سرویس Postgres در Docker بالا است و اپ/تست لوکال به آن وصل است  
- Then: توسعه و pytest لوکال روی PostgreSQL اجرا می‌شوند؛ مسیر SQLite برای دیگران حذف یا خراب نشده است  

**Scenario 3c: CI هرگز SQLite نیست**  
- Given: PR به `develop`  
- When: pytest در GitHub Actions اجرا می‌شود  
- Then: موتور داده PostgreSQL است؛ شکست Postgres باعث سبز شدن با SQLite نمی‌شود  

**Scenario 4: بدهی Ruff پاک شده**  
- Given: درخت بک‌اند پس از گام پاک‌سازی lint  
- When: `ruff check` معادل CI اجرا می‌شود  
- Then: بدون خطای باقی‌ماندهٔ قبلی که Check را قرمز کند  

**Scenario 5: E2E روی PR بک‌اند gate نیست**  
- Given: PR به `develop` و در صورت وجود job E2E  
- When: E2E شکست بخورد یا اجرا نشود  
- Then: شکست E2E به‌تنهایی Check اجباری ادغام را قرمز نمی‌کند (pytest+Ruff جدا هستند)  

**Scenario 6: push فرانت به main**  
- Given: Studio به `main` پوش کرده  
- When: CI فرانت اجرا می‌شود  
- Then: typecheck، unit، build پیش‌فرض، و build با `VITE_USE_MOCK=false` و `VITE_API_BASE_URL=https://chequeyar-back.chbkn.dev/api/v1` همه باید موفق باشند تا Check سبز شود  

**Scenario 7: تریگر E2E بعد از push فرانت**  
- Given: commit جدید روی `main` فرانت  
- When: اتوماسیون E2E دویون اجرا می‌شود  
- Then: E2E همان commit را هدف می‌گیرد؛ پین UI در دویون با آن commit هم‌تراز است؛ نتیجه در Actions دیده می‌شود؛ PRهای بک‌اند به `develop` به‌خاطر این شکست merge-block نمی‌شوند  

**Scenario 8: PR فرانت به product**  
- Given: مالک PR از `main` به `product` باز کرده  
- When: Checks اجباری فرانت روی آن PR اجرا می‌شوند  
- Then: همان مجموعهٔ سناریو ۶ باید سبز باشد تا PR از نظر این ویژگی قابل ادغام باشد  

**Scenario 9: بدون تأیید، بدون deploy محصول**  
- Given: تست‌ها سبزند  
- When: مالک تأیید استقرار نمی‌دهد  
- Then: `chequeyar-back` و `chequeyar-front` نسخهٔ قبلی را سرو می‌کنند  

**Scenario 10: deploy تأییدشدهٔ API**  
- Given: انتشار بک‌اند با pytest+Ruff سبز و تأیید مالک  
- When: استقرار اجرا می‌شود  
- Then: `chequeyar-back` آن انتشار را روی PostgreSQL سرو می‌کند (نه SQLite) و Check استقرار موفق است  

**Scenario 11: deploy تأییدشدهٔ SPA**  
- Given: `product` با تست سبز و تأیید مالک  
- When: استقرار اجرا می‌شود  
- Then: `chequeyar-front` ایمیج زندهٔ غیرmock را سرو می‌کند  

**Scenario 12: شکست deploy**  
- Given: نسخهٔ N روی محصول است و استقرار N+1 شکست می‌خورد  
- When: job استقرار تمام می‌شود  
- Then: Check ناموفق است؛ بازیابی با deploy دستی/تأییدشدهٔ انتشار N است نه rollback خودکار پلتفرم  

**Scenario 13: SemVer و Docker**  
- Given: مالک یک انتشار محصول را تأیید می‌کند  
- When: فرآیند انتشار تمام می‌شود  
- Then: GitHub Release با تگ SemVer وجود دارد و ایمیج Docker بک‌اند و فرانت با همان تگ وجود دارند  

**Scenario 14: دمو mock**  
- Given: `chequeyar-front-demo` و CD فعلی mock  
- When: این ویژگی پیاده می‌شود  
- Then: رفتار دمو نسبت به قبل تغییر نکرده است  

**Scenario 15: مسیر Studio**  
- Given: سیاست یک‌طرفه UI  
- When: فایل‌های فرانت تغییر می‌کنند  
- Then: از Cursor به `checkyar-googleai` push نمی‌شود؛ پرامپت‌ها در همین پوشه مستند می‌شوند  

**Scenario 16: عدم staging**  
- Given: ویژگی کامل شده  
- When: استقرار بررسی می‌شود  
- Then: محیط staging جدیدی برای این کار وجود ندارد  

**Scenario 17: میانهٔ کار CI**  
- Given: نصب وابستگی یا runner در میانه fail می‌شود  
- When: job تمام می‌شود  
- Then: Check ناموفق است؛ retry خودکار الزامی نیست؛ محصول تغییر نمی‌کند  

## 5. Out of Scope

- ساخت یا الزام محیط staging
- استقرار خودکار محصول بدون تأیید مالک (این نسخه)
- Dependabot / Renovate، پین SHA اکشن‌ها، GitHub Environments
- CodeQL، coverage gate، Sentry
- Kubernetes
- Playwright به‌عنوان چک اجباری PR بک‌اند (نسخهٔ بعد)
- rollback خودکار داخلی چابکان
- تغییر `chequeyar-front-demo` و `.github/workflows/cd-demo.yml`
- تغییر قرارداد API محصول و صفحات اپ
- commit/push از Cursor به ریپوی UI فعال
- اعلان خارج از GitHub Actions UI
- اجبار همهٔ توسعه‌دهنده‌ها به Postgres یا Docker برای کار لوکال (مسیر SQLite باید بماند)
- استفاده از SQLite در CI یا در محصول
