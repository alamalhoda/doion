# Implementation Plan — کاتالوگ بانک و نشان بانک

## Architecture Summary

بانک به‌صورت اپ دامنهٔ جدا `doion.banks` در بک‌اند تعریف می‌شود: مدل کاتالوگ، seed ۱۴ بانک، ادمین جنگو، و `GET /api/v1/banks/` عمومی. `ChequeListing` با FK اختیاری `bank` به کاتالوگ وصل می‌شود؛ `bank_name` به‌عنوان نام نمایشی باقی می‌ماند. ایجاد/ویرایش آگهی فیلد `bank` (code) می‌گیرد و متن آزاد را رد می‌کند. UI در `checkyar-googleai` یک کاتالوگ واحد و کامپوننت `BankBadge` / `BankSelect` می‌سازد و همه‌جا نام بانک را با نشان جایگزین می‌کند. Mock همان قرارداد را از شبیه‌ساز برمی‌گرداند؛ Live از API می‌خواند و هنگام شکست به کاتالوگ محلی همان مجموعه برمی‌گردد. کد UI از Cursor پوش نمی‌شود — فقط پرامپت AI Studio.

- **Scope:** FULL-STACK
- **Spec مرجع:** [`feature_spec.md`](feature_spec.md)
- **قرارداد API (SSOT):** `docs/development/MASTER_API_CONTRACT.md` — در همان PR بک‌اند به‌روز می‌شود
- **GitFlow بک‌اند:** `feature/bank-catalog` از `develop`؛ ادغام فقط با PR
- **تحویل UI:** حلقه AI Studio (پرامپت در `prompts/` → Studio → GitHub → `git pull` محلی)

## Implementation Steps

قدم‌های بک‌اند در `doion` با GitFlow؛ قدم‌های UI فقط پرامپت Studio. UI و backend در یک قدم مخلوط نمی‌شوند.

### - [ ] Step 1: Data / schema + seed کاتالوگ (`doion`)

- اپ جدید `doion.banks` و ثبت در `LOCAL_APPS`.
- مدل `Bank` (از `TimeStampedModel`):
  - `code` (`SlugField`/`CharField`، یکتا، غیرقابل‌تغییر پس از ایجاد)
  - `display_name`
  - `aliases` (`JSONField`، لیست رشته؛ شامل `display_name`)
  - `logo` (`ImageField`، `null`/`blank`، آپلود از ادمین)
  - `brand_color_light` / `brand_color_dark` (رشته `#RRGGBB`)
  - `is_active` (default True)
- `ChequeListing.bank` → `ForeignKey(Bank, null=True, blank=True, on_delete=PROTECT)`
- `bank_name` حذف نمی‌شود.
- constraint فعلی `unique_cheque_per_issuer_per_bank` روی `(issuer, bank_name, serial)` حفظ می‌شود (پس از create، `bank_name` برابر `display_name` است).
- ایندکس روی `ChequeListing.bank`.
- ادمین جنگو: `BankAdmin` با لیست، جستجو، فیلتر فعال، آپلود لوگو، ویرایش رنگ و aliases؛ `code` در edit قفل.
- Seed idempotent ۱۴ بانک spec §۳.۱ با `code`های جدول پایین؛ رنگ‌ها `#RRGGBB` تقریبی متمایز؛ `logo` خالی.
- Factory: `BankFactory` در `doion/banks/factories.py`.
- تست مدل: یکتایی `code`، یکتایی alias در `clean`/`service`، seed حداقل ۱۴ بانک، FK nullable.
- مهاجرت برگشت‌پذیر؛ ستون غیر null بدون default اضافه نشود.

**خروجی قابل‌بازبینی:** migrate سبز؛ ادمین بانک را می‌سازد/ویرایش می‌کند؛ seed ۱۴ ردیف.

### - [ ] Step 2: Domain / backfill / write-path آگهی (`doion`)

- Service در `doion.banks` (نه در serializer/view):
  - `get_active_by_code(code) -> Bank`
  - `resolve_legacy_name(name) -> Bank | None` (trim؛ match روی `display_name` و aliases)
  - `apply_bank_to_listing(listing, bank)`: FK + `bank_name = display_name`
- Backfill یک‌بار روی آگهی‌های موجود: اگر نام با کاتالوگ بخواند FK پر شود؛ وگرنه `bank=null` و `bank_name` دست‌نخورده (مهاجرت fail نشود).
- `ChequeListingCreateSerializer` / update: فیلد write-only `bank` (code) اجباری در create؛ `bank_name` ورودی رد شود (400 VALIDATION_ERROR). `create()` فقط service را صدا بزند.
- یکتایی سریال همچنان روی `(issuer, bank_name, serial)` پس از نرمال‌سازی نام.
- `ChequeListingFactory` و `seed_demo` از بانک کاتالوگ (نه رشتهٔ آزاد بدون FK).
- تست: create با `mellat`؛ create با فقط `bank_name` → 400؛ کد نامعتبر → 400؛ backfill «بانک ملی» → بانک ملی ایران؛ نام ناشناس → `bank=null`.

**خروجی قابل‌بازبینی:** تست‌های service + create listing بدون هنوز expose کردن `GET /banks/` اگر در همین PR بعدی بیاید — ترجیح: Step 2 و 3 در یک شاخه ولی دو commit/بازبینی جدا.

### - [ ] Step 3: API خواندن + فیلتر + contract (`doion`)

- `BankViewSet` از نوع `ReadOnlyModelViewSet` (فقط list): `permission_classes = [AllowAny]`، بدون pagination (آرایهٔ ساده مطابق spec)، فقط `is_active=True`، ترتیب `display_name`.
- مسیر: `GET /api/v1/banks/` (ثبت در `config/api_router.py`).
- Serializer بانک: `code`, `display_name`, `aliases`, `logo_url`, `brand_color_light`, `brand_color_dark`. Mutation از API وجود ندارد (405/عدم ثبت).
- Serializer تو در توی `BankSummarySerializer` (بدون aliases) روی همهٔ پاسخ‌های آگهی که امروز `bank_name` دارند:
  - `ChequeListingSerializer` / create response
  - marketplace list + latest
  - `ChequeListingMinimalSerializer` (matches)
  - `QueueListingSerializer` (moderation)
- اگر `bank` null باشد فیلد JSON `bank` برابر `null` است؛ `bank_name` متن ذخیره‌شده می‌ماند.
- querysetهای list/retrieve: `select_related("bank")`.
- فیلتر بازارچه: `bank` دقیق روی `bank__code`؛ `bank_name` موجود روی `display_name`/aliases (یا `bank_name` + نام بانک وصل‌شده). اگر هر دو آمده باشند `bank` مقدم است.
- به‌روزرسانی `docs/development/MASTER_API_CONTRACT.md` در **همین PR** (الزام documentation-sync).
- تست API: مهمان 200 و ۱۴ بانک؛ nested `bank` روی latest/list/retrieve؛ فیلتر `?bank=mellat`؛ فیلتر `?bank_name=ملی`؛ POST بدون `bank` → 400.

**خروجی قابل‌بازبینی:** PR بک‌اند آمادهٔ merge به `develop` (schema + service + API + admin + contract + tests).

### - [ ] Step 4: UI — کاتالوگ واحد + `BankBadge` (AI Studio)

پرامپت: `prompts/01-bank-badge.md`  
اجرا فقط در Google AI Studio. Cursor UI را پوش نمی‌کند.

- ماژول کاتالوگ محلی هم‌مجموعه spec §۳.۱ با همان `code`های جدول پایین (SSOT کلاینت برای mock و fallback).
- `BankBadge`: لوگو / حرف‌اول+رنگ تم / ناشناس (ساختمان+حرف اول) / سایز compact و default.
- Vitest برای lookup alias، unknown، و انتخاب رنگ تم.
- بدون اتصال به صفحات در این قدم (YAGNI برای اسکن گسترده).
- Docs UI: Architecture EN+FA — ذکر `BankBadge` و کاتالوگ محلی.
- Bun؛ بدون `package-lock.json`؛ بدون backend.

**خروجی:** commit SHA از Studio + `git pull` + verify.

### - [ ] Step 5: UI — API client + شبیه‌ساز (AI Studio)

پرامپت: `prompts/02-banks-api-and-mock.md`

- `banksApi.list()` در `src/api/index.ts`: mock → simulator؛ Live → `GET /banks/` با `unwrapList`.
- شبیه‌ساز: seed ۱۴ بانک؛ listingهای seedشده `bank` تو در تو (یا `null` برای یک نمونه ناشناس)؛ `createListing`/`updateListing` فیلد `bank` اجباری؛ فیلتر `bank` و `bank_name`.
- `useBanksCatalog`: Live از API، شکست → کاتالوگ محلی؛ mock بدون HTTP.
- تایپ‌های `src/types/api.ts`: `Bank`, `bank` روی listingها؛ `CreateListingRequest.bank`.
- Vitest: mock بدون HTTP؛ Live fail → fallback؛ create mock با code.
- به‌روزرسانی Architecture + Testing EN/FA (mock در برابر Live).

**خروجی:** SHA + pull + verify simulator و client.

### - [ ] Step 6: UI — اتصال نشان و انتخاب بانک (AI Studio)

پرامپت: `prompts/03-wire-bank-surfaces.md`

جایگزینی نام بانک و آیکون ساختمان با `BankBadge` / `BankSelect` در:

- `ListingCard`، `LatestListingsWidget`، جدول بازارچه
- لندینگ: هیرو و کارت آگهی زنده (بدون CDN بانک)
- جزئیات آگهی، ثبت/ویرایش، wizard
- مچ‌ها، moderation، گزارش‌ها
- فیلتر بازارچه: گزینهٔ «همه بانک‌ها» = متن + آیکون ساختمان عمومی؛ بقیه نشان بانک + `renderLabel`

`NSelect` مقدار `code` می‌فرستد نه متن آزاد. اسکن `bank_name` در `src/` و گزارش محل‌های باقی‌مانده.

**خروجی:** SHA + pull + verify Live (در صورت آماده بودن Step 3) و mock.

### - [ ] Step 7: UI — حساب بانکی + بستن شکاف‌ها (AI Studio)

پرامپت: `prompts/04-my-account-and-gaps.md`

- `MyAccountView`: بانک مقصد واریز از کاتالوگ (`BankSelect`)؛ در mock ذخیره در simulator؛ Live فقط state صفحه.
- رفع جاهای باقی‌مانده از اسکن Step 6.
- Docs UI در صورت تغییر سطح جدید.

**خروجی:** SHA + pull + verify.

### - [ ] Step 8: E2E doion (در صورت تغییر selector/قرارداد)

- اگر `data-testid` یا payload ایجاد آگهی عوض شد: به‌روزرسانی `doion/e2e` روی شاخهٔ جدا (`bugfix/` یا ادامهٔ `feature/bank-catalog` فقط برای e2e، نه UI).
- اگر Studio testid نداد: follow-up prompt؛ UI را محلی دست نزن.
- اگر فقط نمایش بود و critical path نشکست: `skipped-cosmetic` در وضعیت تست.

## Key Decisions & Assumptions

1. اپ جدا `doion.banks` (نه مدل داخل `checks`) — تأییدشده در design brief.
2. FK آگهی nullable است؛ نگاشت‌نشده `bank: null` + UI ناشناس — تأییدشده.
3. `code`های پایدار کلاینت/سرور (باید یکسان باشند):

   | code | display_name |
   |------|----------------|
   | `mellat` | بانک ملت |
   | `melli` | بانک ملی ایران |
   | `saderat` | بانک صادرات ایران |
   | `pasargad` | بانک پاسارگاد |
   | `tejarat` | بانک تجارت |
   | `saman` | بانک سامان |
   | `parsian` | بانک پارسیان |
   | `sepah` | بانک سپه |
   | `ayandeh` | بانک آینده |
   | `maskan` | بانک مسکن |
   | `shahr` | بانک شهر |
   | `keshavarzi` | بانک کشاورزی |
   | `refah` | بانک رفاه کارگران |
   | `sina` | بانک سینا |

4. ایجاد آگهی breaking است (`bank` به‌جای `bank_name`)؛ خواندن additive است.
5. constraint یکتا روی `bank_name` متنی می‌ماند؛ پس از write، نام همیشه `display_name` است.
6. رنگ seed تقریبی است؛ تست فرمت `#RRGGBB` نه هویت برند.
7. لوگو تا آپلود ادمین `null` است؛ UI حرف اول + رنگ.
8. MyAccount در این فاز API پروفایل ندارد.
9. Mock ادمین جنگو ندارد؛ آپلود لوگو فقط Live.
10. پرامپت‌های UI بعد از (یا حداکثر موازی با) قفل شدن جدول `code` نوشته می‌شوند تا کاتالوگ محلی با سرور یکی باشد.
11. `GET /api/v1/banks/` آرایه است نه صفحهٔ DRF — با `unwrapList` در UI سازگار بماند اگر بعداً صفحه شد.
12. کتابخانهٔ npm/pip جدید اضافه نمی‌شود.

## Open Questions

هیچ `⚠️ OPEN QUESTION` باز در spec باقی نمانده.

## Handoff to Chat 2

قبل از چت ساخت:

1. `feature_spec.md` و `implementation_plan.md` را commit کنید (در `doion`، روی `feature/bank-catalog` از `develop` یا حداقل روی شاخهٔ کاری — نه مستقیم روی `develop`/`main`).
2. چت تازه باز کنید و هر دو فایل را بدهید.
3. بگویید **begin**. Chat 2 فقط Step 1 را پیاده می‌کند و منتظر بازبینی می‌ماند.

قالب شروع Chat 2:

```text
I am implementing a new feature. The thinking and design phase is complete.
Here are the reference files you must read before we start:

- ai-documents/features/bank-catalog/feature_spec.md
- ai-documents/features/bank-catalog/implementation_plan.md

Rules:
- Treat these files as the source of truth, not our conversation
- If anything in the codebase contradicts the spec, flag it, don't silently decide
- Follow implementation_plan.md one step at a time
- Backend in doion (GitFlow). UI only via AI Studio prompts — never commit/push checkyar-googleai from Cursor

Start by reading both files and confirming you understand the feature
and the plan. Then wait for me to say "begin".
```
