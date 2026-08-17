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

صفحه در هر دو حالت کار می‌کند:

- **mock** (`VITE_USE_MOCK=true`): همه داده از شبیه‌ساز. برای ساخت و مقایسه روزمره کافی است و به بک‌اند نیاز ندارد.
- **Live** (`VITE_USE_MOCK=false` و `VITE_API_BASE_URL=http://localhost:8000/api/v1`): برای تأیید نهایی بخش آگهی‌ها، با بک‌اند محلی بالا و فلگ روشن در دیتابیس.

هر دو محیط A و B باید در لحظه مقایسه تنظیمات env یکسان داشته باشند.

## Implementation Steps

### - [ ] Step 1: seed فلگ در backend (`doion`)

- افزودن رکورد `show_landing_page` با `is_enabled=false` به `seed_default_feature_flags` در `backend/doion/compliance/signals.py`، دقیقاً هم‌الگوی seed موجود `show_risk_tier`.
- idempotent با `get_or_create` (رفتار موجود همان receiver روی `post_migrate`).
- تست: رکورد پس از مهاجرت وجود دارد و `GET /api/v1/compliance/feature-flags/show_landing_page/` برای مهمان `200` می‌دهد.
- GitFlow: شاخه `feature/landing-flag-seed` از `develop` → PR. مستقل از UI و قابل merge پیش از آن.
- به‌روزرسانی جدول تغییرات در `docs/development/MASTER_API_CONTRACT.md` (فقط ثبت seed؛ قرارداد تغییر نمی‌کند).

### - [ ] Step 2: پرامپت A — اسکلت، مسیر، و گیت فلگ

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

### - [ ] Step 3: پرامپت B — بخش‌های محتوایی ثابت

خروجی: `prompts/02-content-sections.md`

دامنه پرامپت:
- `landing/content/landingContent.ts` به‌عنوان تنها محل متن‌های ثابت (آماده‌سازی چندزبانه فاز بعد).
- بخش‌های هیرو، مسئله/راه‌حل، نحوه کار، مخاطبان، مرز مسئولیت، وضعیت محصول، تعرفه placeholder، FAQ، سرمایه‌گذاری روی چک‌یار.
- متن مرز مسئولیت (spec §۲.۵) و جمله وضعیت محصول (spec §۲.۶) **عیناً** قفل شوند؛ اجازه بازنویسی خلاقانه داده نشود.
- شش پرسش FAQ دقیقاً مطابق spec §۲.۸.
- توکن‌های `docs/design-system.md` پوسته `dark`؛ بدون رنگ یک‌بارمصرف.
- ریسپانسیو از ۳۶۰px؛ بدون اسکرول افقی.

پوشش قوانین spec: ۱۵، ۱۹، ۲۰، ۲۱، ۲۳، ۲۴.

### - [ ] Step 4: پرامپت C — بخش داده‌دار و فرم‌ها

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
