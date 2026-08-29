# مقایسه مسیر A (Studio) و مسیر B (sandbox)

مقایسه خروجی **همان پرامپت‌ها** برای صفحه معرفی عمومی. اعتبار مقایسه: متن پرامپت‌ها یکسان است؛ ترتیب اجرا در Studio تدریجی بود و در sandbox یکجا، مطابق `implementation_plan.md`.

| | مسیر A — محصول | مسیر B — مقایسه |
|--|----------------|-----------------|
| Repo | `checkyar-googleai` | `checkyar-cursor-lab` |
| Branch | `main` | `experiment/landing-cursor` |
| HEAD | `56c9d49` | `b6843cf` |
| Baseline قبل از Landing | `c24fc46` (+ `1c36785` design-system docs) | `c24fc46` |
| Env | `VITE_USE_MOCK=true` | `VITE_USE_MOCK=true` |
| مشاهده زنده | `http://127.0.0.1:3000/landing` | `http://127.0.0.1:3001/landing` |

Sandbox هرگز پوش نشده است.

---

## زنجیره کامیت

### Studio (۹ کامیت؛ ۳ دور اصلاح جدا)

| پرامپت | اجرا | اصلاح | رفت‌وبرگشت |
|--------|------|-------|------------|
| ۰۱ اسکلت | `85ec0be` | `86ee6e3` | سؤال + اصلاح |
| ۰۲ محتوا | `568cf01` | `746cea6` | سؤال + اصلاح |
| ۰۳ داده/فرم | `6fa040a` | `6358a0c` | سؤال + اصلاح |
| ۰۴ polish | `a8250bd` | — | بدون اصلاح |
| ۰۵ decor | `9c19d9e` | — | بدون اصلاح |
| ۰۶ product-led | `56c9d49` | — | بدون اصلاح |

### Sandbox (۶ کامیت؛ clarifications/fixes در همان commit)

| پرامپت | SHA |
|--------|-----|
| ۰۱ | `96fa3d1` |
| ۰۲ | `36321e2` |
| ۰۳ | `fed5782` |
| ۰۴ | `8d9fb12` |
| ۰۵ | `41b941c` |
| ۰۶ | `b6843cf` |

**رفت‌وبرگشت:** Studio برای ۰۱–۰۳ شش پیام اضافه (۳ clarification + ۳ fix) لازم داشت. Sandbox همان متن‌ها را به‌عنوان پیام دوم/سوم گرفت و ایرادهای شناخته‌شده را در commit اول هر پرامپت اعمال کرد — طبق پروتکل مقایسه، این عدد «رفت‌وبرگشت خودعامل» صفر است، نه اینکه clarifications حذف شده باشند.

---

## پوشش spec و قرارداد تست

هر دو مسیر قوانین اصلی spec را پوشش می‌دهند:

- مسیر `/landing` + گارد fail-closed + `publicChrome`
- ترتیب بخش‌های §۲.۳ (Trust strip بین Hero و مسئله/راه‌حل، نه جابجایی آگهی‌ها)
- متن قفل §۲.۵ / §۲.۶ / FAQ / disclaimer
- CTA مهمان/واردشده طبق §۲.۴
- آگهی‌ها از `marketplaceApi.getLatestListings()` حداکثر ۴
- فرم‌ها UI-only
- پوسته `dark` بدون تغییر ترجیح کاربر
- نشانگر `chequeyar_mock_signed_out`

### تفاوت‌های قراردادی (testid / E2E)

| موضوع | Studio | Sandbox | اثر |
|--------|--------|---------|-----|
| CTA خالی آگهی | `landing-listings-empty-guest-cta` / `-auth-cta` | یک `landing-listings-empty-cta` | E2E باید شاخه جدا داشته باشد |
| گرید آگهی | `landing-listings-grid` | ندارد | locator Studio دقیق‌تر |
| گام نحوه کار | `landing-step-1`…`6` | `landing-how-it-works-step-1`…`6` | نام متفاوت |
| فیلد فرم تماس/لید | `data-testid` روی input | Naive `input-props` (مطابق پرامپت ۰۳) | هر دو قابل کلیک‌اند |
| Hero CTA | یک جفت دکمه با v-if متن | دو قالب جدا با همان testid | از نظر Playwright معادل است اگر همزمان mount نشوند |

**نتیجه:** برای E2E در `doion/e2e/` باید testidهای **Studio** مبنا باشد (کد محصول). Sandbox برای smoke محلی کافی است ولی قرارداد محصول نیست.

---

## معماری و خوانایی کد

### نقاط قوت Sandbox

1. **ماژول‌بندی تمیزتر:** `landingRedirect.ts` + `landingRouteGuards.ts`، `mapLandingListings.ts`، `landingVisualClasses.ts`، `landingForm.css`، `LandingLoadingOverlay.vue`، `LOCKED_*` export جدا در SSOT.
2. **Timeline واقعی:** در `lg+` شش گام در **یک ردیف افقی** با خط اتصال؛ موبایل spine راست — نزدیک‌تر به پرامپت ۰۶ از grid ۳×۲ Studio.
3. **توکن رنگ:** Trust strip از `--theme-text-primary` با fallback استفاده می‌کند (Studio `--theme-text` تعریف‌نشده دارد).
4. **رشته‌های preview در SSOT:** `hero.previewEmpty` / `previewError` / `previewListingsLink` — Studio «تابلوی زنده آگهی‌ها» و «مشاهده همه» را در تمپلیت hardcode کرده.
5. **بدون وابستگی جدید:** `@vue/test-utils` اضافه نشده (پرامپت ۰۵/۰۶ صریحاً dep جدید را منع کرده بودند؛ Studio برای تست کارت آن را اضافه کرد).

### نقاط قوت Studio

1. **پوشش تست بالاتر:** ۲۶ فایل / **۱۴۵** تست در برابر ۲۲ فایل / **۱۰۹** تست. شامل mount کامپوننت (`LandingSurfaceCard`, `LandingHeroListingsPreview`, `LiveListingsSection`, `HowItWorksSection`, `LandingTrustStrip`).
2. **کارت آگهی غنی‌تر در بخش اصلی:** chip وضعیت از `LISTING_STATUS_LABELS`، حرف اول بانک، `tabular-nums` روی مبلغ.
3. **اعداد فارسی در نحوه کار:** `toPersianDigits(step.number)` — Sandbox عدد لاتین `index + 1` نشان می‌دهد (خلاف RTL/fa-IR).
4. **Hero preview با mask صادرکننده و chip نرخ** روی کارت فشرده؛ هر دو از composable مشترک استفاده می‌کنند و fetch را dedupe می‌کنند.

### بدهی مشترک / جزئی

- Studio: `--theme-text` ناموجود در Trust strip؛ timeline دسکتاپ ۳×۲ نه ۱×۶.
- Sandbox: اعداد گام لاتین؛ ساختار مسئله/راه‌حل بیشتر «دو پاراگراف» است تا لیست نقاط (پرامپت ۰۲ هر دو را مجاز می‌دانست ولی Studio کارت‌های نقطه‌ای غنی‌تری دارد).

---

## وفاداری به design system

هر دو مسیر:

- پوسته `dark` + emerald
- بدون `animate-pulse` / `indigo` / `amber` به‌عنوان هویت
- بدون فلش LTR
- glass / mesh / dots در پرامپت ۰۵

Sandbox لایه decor را کمی **سیستماتیک‌تر** کرده (`landingVisualClasses` + CSS variables با fallback hex). Studio لایه decor را **غلیظ‌تر روی Hero** پیاده کرده (چند `LandingDecorLayer` + SVG inline). از نظر برند هر دو داخل محدوده §2 design-system هستند؛ هیچ‌کدام پالت آبی/طلایی پیشنهاد خارجی را نیاوردند.

---

## تست و کیفیت ساخت

| | Studio | Sandbox |
|--|--------|---------|
| `tsc --noEmit` | پاک (پس از `bun install` به‌خاطر test-utils) | پاک بدون dep جدید |
| Vitest | 145 | 109 |
| کامیت lockfile | `bun.lock` + `@vue/test-utils` در ۰۵ | بدون تغییر lockfile |

هر دو پس از پرامپت ۰۶ lint/test سبز گزارش شدند.

---

## تصمیم محصول (چه چیز از sandbox به Studio تزریق شود)

کد رسمی همان مسیر A است. موارد زیر ارزش **پرامپت پیگیری کوتاه Studio** دارند — نه کپی فایل از sandbox:

1. **Timeline یک‌ردیفه در `lg+`** (الگوی `HowItWorksSection` sandbox) به‌جای grid ۳×۲.
2. **جایگزینی `--theme-text` با `--theme-text-primary`** در Trust strip.
3. **انتقال رشته‌های Hero preview به `landingContent`** (`previewError`, لینک «مشاهده همه» / «تابلوی زنده»).
4. **اعداد فارسی روی شماره گام‌ها** را نگه دارید (این را از Studio حذف نکنید؛ sandbox باید اصلاح شود اگر دوباره اجرا شود).

مواردی که **نباید** از sandbox به محصول بیاید:

- تغییر نام testid (`landing-how-it-works-step-*` به‌جای قرارداد فعلی Studio)
- ادغام CTA خالی به یک testid
- حذف تست‌های mount Studio

مواردی که **نباید** از Studio به sandbox برگردد (sandbox مرجع مقایسه است، نه محصول): هیچ — remote sandbox حذف شده و پوش نمی‌شود.

---

## جمع‌بندی یک‌صفحه‌ای

| معیار | برنده نسبی | توضیح |
|--------|-------------|--------|
| پوشش spec | مساوی | هر دو قفل‌ها و گارد را رعایت کردند |
| رفت‌وبرگشت | Sandbox | ایرادهای ۰۱–۰۳ را با متن fix از قبل جذب کرد |
| وفاداری visual prompt ۰۶ (timeline) | **Sandbox** | یک ردیف افقی واقعی |
| پوشش تست / E2E-ready testids | **Studio** | ۱۴۵ تست + testidهای فیلد/گرید |
| SSOT رشته‌ها و توکن CSS | **Sandbox** (جزئی) | بدون توکن مرده؛ preview در content |
| اعداد فارسی UI | **Studio** | |
| کد محصول نهایی | **Studio** | سیاست یک‌طرفه AI Studio |

**حکم:** هر دو مسیر به صفحه قابل‌استفاده رسیدند. محصول روی Studio می‌ماند. ارزش مقایسه این است که پرامپت ۰۶ در sandbox timeline را بهتر فهمید و Studio در تست و قرارداد testid سخت‌گیرانه‌تر بود. چهار مورد بالا تنها کاندیدهای پیگیری Studio هستند؛ بقیه تفاوت‌ها سبک پیاده‌سازی است نه شکاف spec.
