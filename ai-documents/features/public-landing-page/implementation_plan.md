# Implementation Plan — صفحه معرفی عمومی (Public Landing Page)

## Architecture Summary

صفحه معرفی به‌صورت ماژول جدید `src/features/landing/` در ریپوی UI (`checkyar-googleai`) ساخته می‌شود: یک `LandingView` که سیزده بخش را می‌چیند، کروم معرفی مستقل از سایدبار اپ، و تنها یک بخش داده‌دار (آگهی‌های اخیر از endpoint عمومی موجود). دسترسی به صفحه پشت فلگ `show_landing_page` است که در گارد روتر به‌صورت async و fail-closed بررسی می‌شود. هیچ endpoint یا قرارداد API جدیدی ساخته نمی‌شود؛ تنها تغییر backend، seed همان فلگ در مونورپوی `doion` است.

- **Scope:** FRONTEND-ONLY (به‌همراه یک کار جانبی کوچک backend برای seed فلگ)
- **Spec مرجع:** [`feature_spec.md`](feature_spec.md)
- **قرارداد API (SSOT):** `docs/development/MASTER_API_CONTRACT.md` — بدون تغییر

## مدل تحویل (مهم؛ با ویژگی‌های معمولی فرق دارد)

کد UI محلی نوشته و پوش نمی‌شود. هر مرحله UI خروجی‌اش یک **پرامپت** است که در `prompts/` ذخیره می‌شود و **دو بار و بدون تغییر** اجرا می‌شود:

| مسیر | محل اجرا | سرنوشت خروجی |
|------|-----------|----------------|
| A — محصول | Google AI Studio → push به GitHub → `git pull` محلی | کد رسمی محصول |
| B — مقایسه | sandbox: `/Users/alamalhoda/Projects/checkyar-cursor-lab` روی شاخه `experiment/landing-cursor` | فقط مرجع مقایسه؛ هرگز پوش نمی‌شود (remote حذف شده) |

قاعده اعتبار مقایسه: متن پرامپت برای هر دو مسیر **کاملاً یکسان** باشد. اگر حین کار پرامپت اصلاح شد، هر دو مسیر باید با نسخه اصلاح‌شده از نو اجرا شوند، وگرنه نتیجه مقایسه بی‌اعتبار است.

### ترتیب اجرای توافق‌شده (جایگزین ترتیب اولیه Stepهای ۵ و ۶)

هر پرامپت بلافاصله پس از نوشتن در Studio اجرا و بازبینی می‌شود، و پرامپت بعدی با آگاهی از ساختار واقعی خروجی نوشته می‌شود:

```text
نوشتن ۰۱ → اجرا در Studio → بازبینی → نوشتن ۰۲ → اجرا در Studio → بازبینی → نوشتن ۰۳ → اجرا در Studio → بازبینی
سپس: اجرای هر سه پرامپت نهایی در sandbox (یکجا) → مقایسه
```

دلیل: ویرایش پرامپت اجرانشده مجانی است، ولی اصلاح پرامپت اجراشده هر دو مسیر را مجبور به اجرای مجدد می‌کند. پرخطرترین بخش هر پرامپت فرض‌هایش درباره کد موجود است و فقط اجرا آن‌ها را اعتبارسنجی می‌کند. اعتبار مقایسه حفظ می‌شود چون شرط آن یکسان‌بودن متن پرامپت در دو مسیر است، نه ترتیب اجرا.

صفحه در هر دو حالت کار می‌کند:

- **mock** (`VITE_USE_MOCK=true`): همه داده از شبیه‌ساز. برای ساخت و مقایسه روزمره کافی است و به بک‌اند نیاز ندارد.
- **Live** (`VITE_USE_MOCK=false` و `VITE_API_BASE_URL=http://localhost:8000/api/v1`): برای تأیید نهایی بخش آگهی‌ها، با بک‌اند محلی بالا و فلگ روشن در دیتابیس.

هر دو محیط A و B باید در لحظه مقایسه تنظیمات env یکسان داشته باشند.

## Implementation Steps

### - [x] Step 1: seed فلگ در backend (`doion`)

- افزودن رکورد `show_landing_page` با `is_enabled=false` به `seed_default_feature_flags` در `backend/doion/compliance/signals.py`، دقیقاً هم‌الگوی seed موجود `show_risk_tier`.
- idempotent با `get_or_create` (رفتار موجود همان receiver روی `post_migrate`).
- تست: رکورد پس از مهاجرت وجود دارد و `GET /api/v1/compliance/feature-flags/show_landing_page/` برای مهمان `200` می‌دهد.
- GitFlow: شاخه `feature/landing-flag-seed` از `develop` → PR. مستقل از UI و قابل merge پیش از آن.
- به‌روزرسانی جدول تغییرات در `docs/development/MASTER_API_CONTRACT.md` (فقط ثبت seed؛ قرارداد تغییر نمی‌کند).

**REVIEW NOTE (اجراشده):** کامیت `c03af87` روی شاخه `feature/landing-flag-seed`؛ سه فایل: `signals.py`، `compliance/tests/test_views.py`، `MASTER_API_CONTRACT.md`. تست `test_show_landing_page_seed_present_and_readable_by_guest` مهمان بدون احراز هویت را می‌آزماید (`200`، `is_enabled=false`، `is_system=false`)؛ کل ۱۷۸ تست backend پاس. روی دیتابیس توسعه موجود هم تأیید شد که `migrate` بدون هیچ مهاجرت جدید، رکورد را می‌سازد (idempotent). هنوز push و PR انجام نشده. یافته مهم برای پرامپت‌های UI: پاسخ `GET /compliance/feature-flags/` صفحه‌بندی‌شده است (`{count, next, previous, results}`)، نه آرایه ساده.

### - [x] Step 2: پرامپت A — اسکلت، مسیر، و گیت فلگ

خروجی: `prompts/01-skeleton.md`

دامنه پرامپت:
- مسیر `/landing` با `meta: { publicChrome: true }`؛ نه `requiresAuth` نه `guestOnly`.
- `/` از ریدایرکت ثابت به ریدایرکت شرطی: فلگ روشن → `/landing`، وگرنه `/marketplace`.
- گارد async فقط برای `/` و `/landing`؛ سایر مسیرها دست‌نخورده.
- `useFeatureFlags`: افزودن computed `showLandingPage` هم‌الگوی `showRiskTier`.
- `useBackendSimulatorStore`: افزودن `show_landing_page` با `is_enabled=true` به `seedFeatureFlags` تا صفحه در حالت mock در دسترس باشد؛ منطق merge موجود، فلگ را به وضعیت ذخیره‌شده `localStorage` هم اضافه می‌کند.
- `App.vue`: حالت سوم کروم بر اساس `publicChrome` (بدون سایدبار/هدر اپ، صرف‌نظر از لاگین).
- `LandingView.vue` + `LandingHeader.vue` + `LandingFooter.vue` با بخش‌های خالی place-held.
- حالت در حال بارگذاری تا مشخص‌شدن وضعیت فلگ؛ بدون فلاش محتوای اشتباه.
- fail-closed در خطای دریافت فلگ.
- فهرست `data-testid`های موردنیاز E2E در همین پرامپت درخواست شود.

پوشش قوانین spec: ۱، ۲، ۳، ۵، ۶، ۱۸ (فوتر placeholder)، ۲۲، ۲۶، ۲۷، ۲۸.

**REVIEW NOTE (اجراشده):** پرامپت در [`prompts/01-skeleton.md`](prompts/01-skeleton.md). سه مورد بیش از دامنه اولیه Step 2 وارد پرامپت شد، هر سه با دلیل:

1. **حالت مهمان در mock (تصمیم کاربر).** `loadSavedUser()` در حالت mock خودکار `holder1` را لاگین می‌کند، پس بعد از logout اولین بارگذاری مجدد دوباره کاربر را وارد می‌کند و سناریو ۲۲ و همه سناریوهای مهمان در mock غیرقابل‌تأیید بودند. راه‌حل انتخاب‌شده: نشانگر صریح خروج در `localStorage`. راحتی دموی فعلی حفظ می‌شود و تصمیم قبلی ثبت‌شده در `docs/development/AI_STUDIO_E2E_PREP_PROMPT.md` («demo fallback seed فقط در mock») نقض نمی‌شود.
2. **قفل پوسته `dark`.** قانون ۲۳ و Out of Scope پوسته‌های دیگر را روی این صفحه رد می‌کنند، ولی `NConfigProvider` در `App.vue` پوسته Naive را از ترجیح کاربر می‌گیرد. پرامپت `data-theme="dark"` روی ریشه صفحه و پوسته dark برای مسیرهای `publicChrome` را می‌خواهد، بدون تغییر ترجیح ذخیره‌شده کاربر.
3. **حالت بارگذاری بوت سرد.** `#app` در `index.html` خالی است، پس قانون ۳ («فقط حالت بارگذاری دیده شود») روی بوت سرد نقض می‌شد. پرامپت یک placeholder کوچک RTL داخل `#app` می‌خواهد.

ترتیب بخش‌ها **تأییدشده**: فوتر آخرین عنصر صفحه است و بخش «سرمایه‌گذاری روی چک‌یار» قبل از آن می‌آید، برخلاف ترتیب عینی ردیف‌های ۱۲ و ۱۳ در spec §۲.۳. پرامپت از ابتدا همین را می‌گوید، پس نیازی به اصلاح و اجرای مجدد نیست.

تصحیح یک برداشت قبلی: قرارداد `data-testid` در ریپوی UI از قبل وجود دارد (`login-submit`، `mock-mode-switch`، `marketplace-listing-card`، ثبت‌شده در `AI_STUDIO_E2E_PREP_PROMPT.md`)، پس پرامپت testidهای landing را در ادامه همان قرارداد kebab-case می‌خواهد.

**اجرای Studio — کامیت `85ec0be`:** ۱۷ فایل، ۹۶۱ افزوده. دامنه فایل‌ها درست بود (بدون `package-lock.json`، بدون `src/views/`، بدون backend). بازبینی محلی با Playwright و Chrome روی `127.0.0.1:3100` انجام شد، نه بر پایه خلاصه خود Studio.

درست: دوازده بخش با شناسه و ترتیب تأییدشده و فوتر آخر؛ گیت fail-closed در همه حالت‌ها (با فلگ خاموش، `/` و `/landing` مهمان را به `/login` می‌رسانند، بدون حلقه، و مقدار ذخیره‌شده فلگ بازنویسی نمی‌شود)؛ کروم عمومی با `<aside>` صفر؛ قفل پوسته dark با ترجیح `light` کاربر و بدون تغییر آن؛ نشانگر خروج mock؛ لینک‌های فوتر با «به‌زودی» و بدون تغییر URL؛ نبود اسکرول افقی در ۳۶۰px؛ `tsc --noEmit` تمیز و ۷۱ تست پاس (بازتولید محلی).

پنج ایراد که در [`prompts/01-skeleton-fixes.md`](prompts/01-skeleton-fixes.md) به Studio برگشت: (۱) حذف کامل نیم‌فاصله از عنوان و توضیح متا، پس تب مرورگر «چکیار … چکهای مدتدار» نشان می‌داد؛ (۲) تکرار `landing-nav-login/register/marketplace` در نسخه دسکتاپ و منوی موبایل، که در ۳۶۰px با منوی بسته عنصر قابل‌کلیک نمی‌گذارد و با منوی باز locator را به دو عنصر می‌رساند و strict mode را می‌شکند؛ (۳) نبود حالت بارگذاری که در دور clarifications صریحاً خواسته شده بود — `main.ts` بدون انتظار برای `router.isReady()` مانت می‌کند، پس Vue محتوای `#app` و placeholder را پاک می‌کند در حالی که `beforeEnter` هنوز منتظر فلگ است و اندازه‌گیری روی localhost یک پنجره ~۳۱۰ms خالی نشان داد که با تأخیر backend واقعی بزرگ‌تر می‌شود؛ (۴) مستنداتی که UI ناموجود را توصیف می‌کند (`landing-nav-register-btn` به‌جای `landing-nav-register`، و نوار CTA چسبان و CTAهای هیرو که ساخته نشده‌اند)؛ (۵) سال کپی‌رایت فوتر به‌صورت ثابت «۱۴۰۴» که همین حالا هم غلط است.

متن سلب مسئولیت فوتر جلوتر از برنامه نوشته شده (پرامپت ۰۱ فقط اسکلت بود و متن رگولاتوری در spec قفل است)؛ فعلاً دست‌نخورده می‌ماند و در پرامپت ۰۲ با متن قفل‌شده تطبیق داده می‌شود.

**درس فرایندی:** خلاصه Studio با کامیت خودش نمی‌خواند — هفت بخش نام برد که در کد نیستند (`social-proof`، `for-holders`، `for-investors`، `trust`، `comparison`، `final-cta`، `sticky-cta`) و برچسب CTA را «ورود به سامانه» گفت در حالی که کد «ورود به بازارچه» است. کد درست بود و گزارش غلط. از این پس diff و بررسی زنده مبنای پذیرش است، نه خلاصه عامل. برای Step 7 هم ثبت می‌شود.

**دور اصلاح Studio — کامیت `86ee6e3` (پذیرفته):** ۱۳ فایل، ۸۴ افزوده / ۲۴ حذف. همه پنج ایراد blocking/non-blocking برطرف شد:

1. **ZWNJ:** `constants.ts` با `\u200c` escape + `landingConstants.test.ts` (≥۳ نیم‌فاصله + تطابق عین متن). بازبینی زنده: `document.title.includes('\u200c') === true`.
2. **testid تکراری:** پسوند `-mobile` برای سه دکمه منوی موبایل. در ۳۶۰px `[data-testid="landing-nav-login"]` دقیقاً یک عنصر؛ کلیک `landing-nav-login-mobile` پس از باز کردن همبرگر OK.
3. **بارگذاری بوت سرد:** `router.isReady().then(() => app.mount('#app'))` — placeholder تا لحظه ظاهر شدن landing-page باقی می‌ماند؛ بدون فریم خالی بین رفتن loader و آمدن محتوا. برای ناوبری درون‌برنامه‌ای، Studio الگوی SPA (صفحه قبلی visible) را صریح انتخاب و توضیح داد — قابل قبول طبق پرامپت اصلاح.
4. **مستندات:** action bar/sticky/hero CTA حذف؛ testidهای موبایل اضافه؛ `landingConstants.test.ts` در ماتریس تست.
5. **سال فوتر:** `getCurrentJalaliYear()` در `persianUtils.ts` + تست؛ فوتر «۱۴۰۵» نشان می‌دهد.

موارد کوچک هم انجام شد: حذف پارامتر بلااستفاده `handlePlaceholderClick`، `meta: { publicChrome: true }` روی `/`.

بازتولید محلی: `tsc --noEmit` تمیز، ۷۵ تست (۱۴ فایل) پاس. خلاصه Studio این بار با diff هم‌خوان بود.

**پرامپت ۰۱ (اسکلت) بسته شد.** HEAD UI: `86ee6e3`. قدم بعد: نوشتن [`prompts/02-content-sections.md`](prompts/02-content-sections.md).

**رفت‌وبرگشت اول (Studio):** Studio پیش از پیاده‌سازی سؤال پرسید و پیشنهاد مشخص برای شناسه بخش‌ها، لینک‌های فوتر، معماری گارد، عنوان/متا، و مدیریت پوسته و نشانگر خروج داد. پاسخ در [`prompts/01-skeleton-clarifications.md`](prompts/01-skeleton-clarifications.md) ثبت شد و در sandbox هم به‌عنوان پیام دوم استفاده می‌شود تا ورودی دو مسیر یکسان و شمارش رفت‌وبرگشت معتبر بماند. دو اصلاح در آن دور: توضیح متا از «مدیریت مطالبات» (ادعای قابلیتی که محصول ندارد) به زبان spec برگشت، و پنج مورد غایب از خلاصه Studio (حالت بارگذاری، تأیید merge شبیه‌ساز، فهرست vitest، مستندات دوزبانه، فهرست do-not) صریحاً یادآوری شد.

### - [x] Step 3: پرامپت B — بخش‌های محتوایی ثابت

خروجی: `prompts/02-content-sections.md`

دامنه پرامپت:
- `landing/content/landingContent.ts` به‌عنوان تنها محل متن‌های ثابت (آماده‌سازی چندزبانه فاز بعد).
- بخش‌های هیرو، مسئله/راه‌حل، نحوه کار، مخاطبان، مرز مسئولیت، وضعیت محصول، تعرفه placeholder، FAQ، سرمایه‌گذاری روی چک‌یار.
- متن مرز مسئولیت (spec §۲.۵) و جمله وضعیت محصول (spec §۲.۶) **عیناً** قفل شوند؛ اجازه بازنویسی خلاقانه داده نشود.
- شش پرسش FAQ دقیقاً مطابق spec §۲.۸.
- توکن‌های `docs/design-system.md` پوسته `dark`؛ بدون رنگ یک‌بارمصرف.
- ریسپانسیو از ۳۶۰px؛ بدون اسکرول افقی.

پوشش قوانین spec: ۱۵، ۱۹، ۲۰، ۲۱، ۲۳، ۲۴.

**REVIEW NOTE (نوشته‌شده):** پرامپت در [`prompts/02-content-sections.md`](prompts/02-content-sections.md). نسبت به طرح اولیه Step 3، سه تصمیم صریح اضافه شد:

1. **پاسخ‌های FAQ هم قفل شدند** — spec فقط پرسش‌ها را فهرست کرده؛ برای جلوگیری از ادعای قابلیت نادرست (مثل دور اول متا)، پاسخ‌های رگولاتوری در پرامپت verbatim نوشته شد.
2. **CTAهای هیرو** — اولین بار در این پرامپت ساخته می‌شوند (`landing-hero-primary-cta`، `-secondary-cta`، `-pilot-badge`)؛ مطابق §۲.۴.
3. **هم‌راستاسازی فوتر** — توضیح برند و خط پایین فوتر با §۲.۵ هم‌راستا می‌شود؛ import از `landingContent.ts` برای جلوگیری از drift.
4. **سه بخش placeholder** — live-listings، contact-us، lead-capture-form عمداً برای پرامپت ۰۳ باقی می‌مانند.

کامپوننت‌ها در `src/features/landing/sections/`؛ `LandingView.vue` فقط compose می‌کند. HEAD UI مبنا: `86ee6e3`.

**رفت‌وبرگشت اول (Studio):** Studio پیش از پیاده‌سازی سؤال ZWNJ canonical، FAQ testid/accordion، و رفتار scroll CTA پرسید. پاسخ در [`prompts/02-content-sections-clarifications.md`](prompts/02-content-sections-clarifications.md). یک اصلاح: A1 باید «نگه\u200cداری» باشد نه «نگهداری». بقیه تأیید شد.

**اجرای Studio — کامیت `568cf01`:** ۱۷ فایل، ۹۲۶ افزوده / ۱۶۲ حذف. دامنه درست (بدون routing/auth/API، سه placeholder باقی). بازبینی زنده با Playwright روی `127.0.0.1:3100`.

درست: متن قفل‌شده §۲.۵/۲.۶/FAQ/disclaimer روی صفحه؛ A1 شامل «نگه‌داری»؛ CTA هیرو مهمان/واردشده + tertiary؛ اسکرول سرمایه‌گذاری به `#contact-us`؛ FAQ شش آیتم پیش‌فرض بسته؛ فوتر از SSOT؛ ۳۶۰px بدون اسکرول افقی؛ `tsc` تمیز، ۸۶ تست پاس.

چهار ایراد در [`prompts/02-content-sections-fixes.md`](prompts/02-content-sections-fixes.md): (۱) ادعای «پذیرش شرکای پایلوت»، سه بار «مطالبات»، و `(user_type)` انگلیسی در UI مهمان؛ (۲) رنگ‌های amber/rose/indigo خارج از توکن + `animate-pulse` خلاف دیزاین‌سیستم؛ (۳) متن‌های «مرز مسئولیت رگولاتوری»، «تسویه مستقیم»، «مدل آتی» خارج از SSOT؛ (۴) فلش LTR بعد از لینک tertiary.

**دور اصلاح Studio — کامیت `746cea6` (پذیرفته):** ۹ فایل. همه چهار ایراد برطرف شد. زنده: صفحه مهمان بدون «مطالبات» / «پذیرش شرکای پایلوت» / `user_type`؛ بدون amber/rose/indigo و `animate-pulse`؛ tertiary بدون فلش؛ توضیح وضعیت محصول مطابق رشته جایگزین. `tsc` تمیز، ۹۰ تست پاس.

**پرامپت ۰۲ (محتوا) بسته شد.** HEAD UI: `746cea6`. قدم بعد: نوشتن [`prompts/03-live-data-and-forms.md`](prompts/03-live-data-and-forms.md).

### - [x] Step 4: پرامپت C — بخش داده‌دار و فرم‌ها

خروجی: `prompts/03-live-data-and-forms.md`

دامنه پرامپت:
- `LiveListingsSection` با `marketplaceApi.getLatestListings()`؛ حداکثر ۴ آیتم. همین تابع در حالت mock داده شبیه‌ساز می‌دهد، پس شاخه‌بندی جدید mock/Live لازم نیست و صدا زدن مستقیم `axios` مجاز نیست.
- کارت مخصوص landing (بازاستفاده از `LatestListingsWidget` انجام نمی‌شود)، ولی فرمت مبلغ/تاریخ از `utils/persianUtils.ts`.
- چهار حالت: بارگذاری، داده، خالی، خطا با «تلاش مجدد»؛ خطا فقط همان بخش را تحت تأثیر بگذارد.
- گیت `show_risk_tier` روی نمایش سطح ریسک.
- مقصد کلیک: مهمان → `/login`، واردشده → `/listings/{id}`؛ بدون درخواست احراز هویتی از مهمان.
- فرم لید و فرم تماس، UI-only با اعتبارسنجی سمت کلاینت؛ بدون هیچ درخواست شبکه‌ای.
- درخواست vitest برای منطق غیربدیهی (اعتبارسنجی موبایل، انتخاب مقصد کارت بر اساس وضعیت ورود).
- درخواست به‌روزرسانی مستندات UI (`docs/ARCHITECTURE*.md`، `docs/TESTING*.md`) در همان commit.

پوشش قوانین spec: ۴، ۷–۱۴، ۱۶، ۱۷، ۲۵، ۲۹.

**REVIEW NOTE (نوشته‌شده):** پرامپت در [`prompts/03-live-data-and-forms.md`](prompts/03-live-data-and-forms.md). نسبت به طرح اولیه Step 4:

1. **ویجت بازارچه ممنوع است** — `LatestListingsWidget` نرخ ساختگی «۲.۵»، رنگ indigo/amber، و کلیک همیشه به جزئیات آگهی دارد؛ برای مهمان خلاف قانون ۱۳ است.
2. **فرمت‌کننده‌ها در `persianUtils`** — `formatTomanFromRial` و `formatJalaliDate` تا سومین کپی `formatTomans` ساخته نشود.
3. **پیام موفقیت فرم قفل شد** تا Studio ارسال واقعی ادعا نکند.
4. **فرم تماس** فیلدهای نام/ایمیل/پیام مشخص شد (spec فقط «ایمیل/فرم» گفته بود).
5. **CTA حالت خالی برای کاربر واردشده** → بازارچه، نه ثبت‌نام.

HEAD UI مبنا: `746cea6`.

**رفت‌وبرگشت اول (Studio):** Studio پیش از پیاده‌سازی قالب تاریخ شمسی، نمایش نرخ، UI نقش لید، toast موفقیت، و ناوبری کارت را پیشنهاد کرد. پاسخ در [`prompts/03-live-data-and-forms-clarifications.md`](prompts/03-live-data-and-forms-clarifications.md). یک اصلاح: `landing-lead-role` فقط یک عنصر (گروه/سلکت)، نه روی هر رادیو.

**اجرای Studio — کامیت `6fa040a`:** ۲۱ فایل، ۹۹۲ افزوده. بازبینی زنده: چهار کارت شبیه‌ساز؛ مهمان → `/login` بدون درخواست جزئیات؛ واردشده → `/listings/101`؛ ریسک خاموش؛ نقش لید یک select؛ اعتبارسنجی و toast قفل‌شده؛ بدون `axios`/`fetch`؛ ۳۶۰px سالم؛ ۱۱۵ تست پاس.

سه ایراد کوچک در [`prompts/03-live-data-and-forms-fixes.md`](prompts/03-live-data-and-forms-fixes.md): `&larr;` روی کارت + «ورود برای معامله»؛ توکن ناموجود `--theme-surface-hover`؛ `animate-pulse` روی اسکلت بارگذاری.

### - [ ] Step 5: اجرای مسیر A و pull

- کاربر پرامپت‌ها را به‌ترتیب در AI Studio اجرا می‌کند و بعد از هر کدام commit SHA برمی‌گرداند.
- `git pull origin main` در کلون محصول؛ تأیید اینکه HEAD شامل commitهای گزارش‌شده است.
- بازبینی diff در برابر متن پرامپت: فایل‌های خواسته‌شده، بدون ریفکتور بی‌ربط، بدون `package-lock.json`، بدون تغییر backend.
- ثبت شکاف‌ها؛ در صورت نیاز پرامپت پیگیری (نه اصلاح محلی UI).

### - [ ] Step 6: اجرای مسیر B در sandbox

- همان سه پرامپت، بدون تغییر، در `/Users/alamalhoda/Projects/checkyar-cursor-lab` روی شاخه `experiment/landing-cursor`.
- اجرا روی پورت ۳۰۰۱: `bun run dev -- --host 127.0.0.1 --port 3001`.
- commit پس از هر پرامپت تا diff هر مرحله قابل تفکیک بماند.

### - [ ] Step 7: مقایسه دو خروجی

خروجی: `comparison_notes.md`

- مقایسه diff در برابر diff: خروجی Studio (روی `main`) و خروجی sandbox (`git diff main...experiment/landing-cursor`).
- معیارها: پوشش قوانین spec، وفاداری به دیزاین سیستم، صحت متن رگولاتوری، رفتار حالت‌های خطا/خالی، کیفیت ریسپانسیو، خوانایی کد، تعداد رفت‌وبرگشت لازم.
- مشاهده هم‌زمان: نسخه محصول روی ۳۰۰۰، نسخه sandbox روی ۳۰۰۱، هر دو روی همان بک‌اند.
- خروجی تصمیم‌محور: چه چیزهایی از نسخه بازنده باید به‌صورت پرامپت پیگیری به Studio تزریق شود.

### - [ ] Step 8: E2E در `doion` (در صورت نیاز)

- یک spec سبک smoke در `doion/e2e/` برای مهمان: با فلگ روشن `/` به `/landing` می‌رسد، بخش‌های کلیدی دیده می‌شوند، کلیک کارت به `/login` می‌رود.
- اگر `data-testid` لازم موجود نبود، پرامپت پیگیری Studio (بدون ویرایش محلی UI).
- GitFlow در `doion`.

### - [ ] Step 9: sync مستندات

- `doion`: ثبت وضعیت صفحه در `docs/development/PAGE_REVIEW_LOG.md`؛ در PR ذکر شود که قرارداد API تغییر نکرده (`Docs impact: none` برای MASTER_API_CONTRACT به‌جز ثبت seed فلگ).
- ریپوی UI: مستندات Architecture/Testing از طریق Studio آمده باشند (نه ویرایش محلی).

## Key Decisions & Assumptions

1. **کارت آگهی مخصوص landing** به‌جای بازاستفاده از `LatestListingsWidget`. آگاهانه خلاف DRY، برای اجتناب از ریسک رگرسیون روی مسیر اصلی بازارچه. فرمت‌کردن مبلغ/تاریخ همچنان مشترک می‌ماند.
2. **گارد async فقط روی `/` و `/landing`**، نه resolve فلگ‌ها پیش از `app.mount()`؛ تا بوت بقیه اپ به یک درخواست شبکه گره نخورد.
3. **کروم معرفی** با `meta.publicChrome`، نه شرط سخت‌کدشده روی مسیر در `App.vue`.
4. **سه پرامپت جدا** به‌جای یک پرامپت غول‌پیکر، برای کاهش ریسک خروجی سطحی.
5. **متن‌های ثابت در یک ماژول داده** برای کم‌هزینه‌کردن چندزبانه‌سازی فاز بعد.
6. فرض: کلید فلگ `show_landing_page` است. اگر Step 1 نام دیگری تثبیت کرد، همه پرامپت‌ها باید هم‌زمان اصلاح و هر دو مسیر از نو اجرا شوند.
7. بازگشت عمیق پس از ورود پیاده نمی‌شود؛ `LoginView` دست‌نخورده می‌ماند.
8. **عدم تقارن آگاهانه پیش‌فرض فلگ:** در شبیه‌ساز روشن، در backend خاموش. دلیل: شبیه‌ساز محیط دمو است و صفحه باید بدون تنظیم دستی دیده شود، ولی محصول واقعی نباید صفحه ناتمام را به مهمان نشان دهد.
9. **مکانیزم seed فلگ:** طرح اولیه «مهاجرت data» فرض کرده بود، اما seed فلگ‌ها در این ریپو با receiver `post_migrate` (`seed_default_feature_flags`) انجام می‌شود، نه با مهاجرت data. برای حفظ SSOT سیدِ فلگ در یک نقطه، Step 1 همان receiver را گسترش می‌دهد.

## Open Questions

هیچ ⚠️ OPEN QUESTION بازی در `feature_spec.md` باقی نمانده است.

ریسک‌های عملیاتی که باید حین اجرا پایش شوند:

- اگر Studio بخواهد قرارداد API را «حدس» بزند یا endpoint غیرصفحه‌بندی‌شده جدید بسازد، در بازبینی diff رد شود.
- اگر sandbox و محصول با تنظیمات env متفاوت اجرا شوند، نتیجه مقایسه بی‌اعتبار است.
