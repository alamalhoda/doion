# سند معماری فنی ماژولار — نسخه نهایی (ترکیبی)
## چک‌یار (Cheque Yar) — لایه ۱ Marketplace

**به‌روزرسانی:** ۱۴۰۵/۰۵/۲۳ (2026-08-14)

| موضوع | وضعیت واقعی |
|--------|-------------|
| سبک معماری | Modular Monolith + Django signals (event-driven داخلی) — پیاده‌سازی‌شده |
| محل کد دامنه | `backend/doion/<app>/` نه `backend/apps/` |
| Presentation | Vue 3 + Naive UI + Pinia در [checkyar-googleai](https://github.com/alamalhoda/checkyar-googleai)؛ نه داخل `frontend/` این مونورپو |
| API | `/api/v1/` — SSOT: [`MASTER_API_CONTRACT.md`](development/MASTER_API_CONTRACT.md) |
| PK | `BigAutoField` |
| Schema DB | یک schema عمومی Django؛ schema جدا per bounded context ساخته نشده |
| Settlement | `off_platform` در `doion.matching` |
| قیمت | stub پیشنهادی؛ غیرالزام‌آور |
| لایه ۲/۳ | پیاده‌سازی نشده؛ `settlement_type` رزرو شده |

مرجع محصول: [`سند پایه پروژه (Core Brief).md`](سند%20پایه%20پروژه%20(Core%20Brief).md). جزئیات مدل/API: [`cheque-platform-low-level-design.md`](cheque-platform-low-level-design.md).

---

## ۱. هدف معماری

پیاده‌سازی یک **Marketplace / Information Board** که در فاز فعلی فقط نقش ثبت، نمایش، جست‌وجو، اعتبارسنجی اولیه، و ارتباط‌دهی بین دارندگان چک و سرمایه‌گذاران را ایفا می‌کند؛ بدون لمس وجه، نگهداری چک، تسویه، یا ضمانت وصول. معماری از ابتدا طوری طراحی می‌شود که افزودن لایه‌های Escrow/Guarantee (لایه ۲) و Principal (لایه ۳) در آینده بدون بازطراحی بنیادین ممکن باشد.

---

## ۲. اصول طراحی

- **Separation of Concerns** — هر قابلیت در مرز دامنه‌ی خودش.
- **Compliance by Design** — محدودیت‌های حقوقی در خود معماری enforce می‌شوند، نه فقط در سند.
- **Modularity via Events** — ماژول‌ها از طریق رویدادهای دامنه (نه فراخوانی مستقیم) با هم ارتباط برقرار می‌کنند؛ این دقیقاً مکانیزمی است که Extensibility را عملیاتی می‌کند.
- **Extensibility via Ports** — نقاطی که در آینده رفتارشان عوض می‌شود (مثل تسویه)، از همین حالا پشت یک رابط انتزاعی (port) قرار می‌گیرند.
- **Auditability** — تمام رخدادهای حساس ثبت و قابل پیگیری‌اند.
- **Feature Flag Control** — قابلیت‌های پرریسک فقط با کنترل صریح فعال می‌شوند.

---

## ۳. انتخاب معماری

**Modular Monolith با طراحی Event-Driven داخلی.** ساده‌تر، سریع‌تر، و کم‌هزینه‌تر از Microservices کامل است، در حالی‌که مرزهای دامنه را از طریق ماژول‌بندی و گذرگاه رویداد داخلی حفظ می‌کند. وقتی زمان استخراج یک ماژول به سرویس مستقل برسد (مثلاً هنگام ساخت لایه ۲)، چون ارتباط از ابتدا از طریق رویداد بوده، این استخراج به تغییر مرز فیزیکی محدود می‌شود، نه بازنویسی منطق.

---

## ۴. لایه‌های سیستم

### 4.1 Presentation Layer
Web App فعلی: Vue 3 (Composition API) + TypeScript + Naive UI + Tailwind + Pinia، ریپوی `checkyar-googleai`. مسیرهای اصلی: بازارچه، ثبت/ویرایش آگهی، Match، اعلان، صف moderation/KYC، آمار ادمین. در MVP **نباید** مذاکره‌ی مالی کامل، پرداخت، یا انتقال مالکیت در این لایه طراحی شود. Mobile App در دامنه فعلی نیست.

گزارش‌های `/reports` در UI لایه نمایشی/mock هستند و API گزارش جدا در بک‌اند ندارند.

### 4.2 API / BFF Layer
`API Gateway` مرکزی (و BFF در صورت نیاز هر کلاینت). وظایف: `Authentication`، `Authorization`، `Rate Limiting`، `Audit Logging`، `Feature Flags`، `Policy Enforcement`. این لایه نقطه‌ی اجرای مرزهای حقوقی بخش ۱۰ است — نه فقط جایی برای توضیح آن‌ها.

### 4.3 Core Domain Layer (به‌اندازه‌شده برای MVP)

پنج ماژول کسب‌وکاری به‌جای ده ماژول ریز، به‌علاوه یک مفهوم عرضی (cross-cutting) که مصرف‌کننده‌ی رویدادهای همه‌ی ماژول‌های دیگر است:

| ماژول مفهومی | Django app واقعی | موجودیت‌های اصلی |
|---|---|---|
| Identity & KYC | `doion.users` + `doion.identity` | `User`, `Profile`, `Verification` |
| Check Registry & Pricing | `doion.checks` + `doion.pricing` | `ChequeListing`, `IssuerProfile` |
| Listing & Search | `doion.marketplace` | فیلتر روی `ChequeListing` با `status=published` |
| Matching & Notification | `doion.matching` + `doion.notifications` | `Match`, `Notification` |
| Moderation & Admin | `doion.moderation` + `doion.compliance` | `ModerationDecision`؛ آمار/فلگ در compliance |
| مدارک (سرویس مشترک) | `doion.documents` | `Document` |
| Integrations | `doion.integrations` | SMS stub (`SMSLog`) |
| *عرضی:* Audit & Compliance | `doion.compliance` | `AuditEvent`, `FeatureFlag` |

**تغییر نسبت به نسخه‌ی اولیه:** `Search & Ranking` به‌عنوان تابعی از ماژول Listing ادغام شد (نیازی به ماژول مستقل در MVP نیست). `Document Management` ماژول مستقل نیست؛ یک سرویس مشترک ذخیره‌سازی است که Identity&KYC و Check Registry از آن استفاده می‌کنند. `Analytics` در این فاز حذف شد چون قابل بازسازی از `AuditEvent` در آینده است و ساخت ماژول جدا برایش الان زودهنگام است.

### 4.4 Integration Layer
اتصال بیرونی از طریق adapter: KYC/Identity و SMS فعلاً **stub** هستند. Credit Check، e-Signature، و Bank/PSP/Escrow در MVP نیستند.

### 4.5 Event Bus (مکانیزم عملیاتی Modularity)
ماژول‌های بخش ۴.۳ به‌جای فراخوانی مستقیم یکدیگر، رویداد منتشر می‌کنند و گوش می‌دهند. نمونه رویدادها: `UserVerified`، `ChequeListingPublished` (پس از تأیید Moderation)، `MatchCreated`، `ListingFlagged`، `FeatureFlagChanged`. این گذرگاه همان نقطه‌ای است که در لایه ۲ و ۳، ماژول‌های جدید بدون دست‌زدن به کد لایه ۱ به آن مشترک می‌شوند (بخش ۸ و ۹).

---

## ۵. مدل دامنه

### 5.1 موجودیت‌های اصلی (پیاده‌سازی واقعی در MVP)
`User`, `Profile`, `ChequeListing`, `IssuerProfile`, `Match`, `Verification`, `Document`, `AuditEvent`, `Notification`

### 5.2 رابط انتزاعی تسویه (Settlement Port)
نقطه‌ای از Core Domain که در آینده رفتارش عوض می‌شود، نه جزئیات پیاده‌سازی‌اش، باید همین حالا پشت یک port قرار بگیرد:
- در **لایه ۱**: پیاده‌سازی NoOp — فقط رکورد می‌کند که توافق نهایی و تسویه «بیرون از پلتفرم» انجام شده.
- در **لایه ۲**: پیاده‌سازی با ترکیب یک adapter جدید در Integration Layer برای Escrow Provider واقعی می‌شود.
- در **لایه ۳**: پیاده‌سازی کاملاً داخلی می‌شود (Ledger/Treasury داخل پلتفرم).

چون `Match` و `Listing` فقط با این port کار می‌کنند نه با جزئیاتش، تغییر لایه‌ی تسویه هیچ‌وقت ماژول‌های دیگر را نمی‌شکند.

### 5.3 موجودیت‌های آینده (واژه‌نامه‌ی مفهومی، نه جدول واقعی)
`EscrowContract`, `GuaranteePolicy`, `SettlementInstruction`, `PrincipalPosition`, `Portfolio`, `LedgerEntry`

**تغییر نسبت به نسخه‌ی اولیه:** این موجودیت‌ها در سند مدل دامنه (برای ارتباط با تیم حقوقی/رگولاتوری) ذکر می‌شوند، اما **migration واقعی برایشان در MVP ساخته نمی‌شود.** جزئیات دقیق این موجودیت‌ها (مثلاً ساختار دقیق `EscrowContract`) به نتیجه‌ی تحلیل حقوقی-رگولاتوری بستگی دارد که هنوز نهایی نشده؛ ساختن schema زودهنگام، ریسک طراحی روی فرضیات غلط را بالا می‌برد.

---

## ۶. جریان عملیاتی MVP

**سمت عرضه:** ثبت‌نام → KYC پایه → ثبت اطلاعات چک و مدارک → بررسی فرمت/تکراری‌نبودن → انتشار پس از Moderation (رویداد `ChequeListingPublished`).

**سمت تقاضا:** ورود سرمایه‌گذار → KYC → جست‌وجو و فیلتر → مشاهده‌ی آگهی → ابراز تمایل (`MatchCreated`) → پذیرش دارنده → تأیید تسویه بیرون از پلتفرم.

پلتفرم صحت حقوقی معامله را تضمین نمی‌کند و قیمت‌گذاری الزام‌آور انجام نمی‌دهد. پیام‌رسان کامل داخل پلتفرم در MVP وجود ندارد.

---

## ۷. لایه داده

یک پایگاه‌داده (Postgres در تولید؛ SQLite در توسعه/دمو). **schema فیزیکی جدا per bounded context پیاده نشده**؛ مرز دامنه از طریق Django app حفظ می‌شود.

**جداول پایه (نام Django):** `users_user`, `identity_profile`, `identity_verification`, `checks_chequelisting`, `checks_issuerprofile`, `documents_document`, `matching_match`, `notifications_notification`, `compliance_auditevent`, `compliance_featureflag`, …  
**فیلد توسعه‌پذیری:** `matching_match.settlement_type` با مقدار اولیه‌ی `off_platform`.
**جداول آینده** (`escrow_contracts`, `settlement_instructions`, `guarantee_policies`, `principal_positions`, `portfolios`, `ledger_entries`): فقط در سند، نه در migration فعلی (طبق بخش ۵.۳).

---

## ۸. الگوی رشد به لایه ۲ (Escrow/Guarantee)

ماژول‌های `Escrow`, `Settlement`, `Dispute`, `Guarantee` به‌عنوان مشترکین جدید روی رویداد `MatchCreated` اضافه می‌شوند. `Settlement Port` (بخش ۵.۲) از NoOp به پیاده‌سازی واقعی عوض می‌شود. `Listing` و `Match` دست‌نخورده می‌مانند؛ فقط state machine معامله گسترش پیدا می‌کند.

## ۹. الگوی رشد به لایه ۳ (Principal Marketplace)

`PrincipalInventory`, `Pricing Engine` (که از همان موتور بخش ۴.۳ توسعه می‌یابد), `Risk Engine`, `Treasury`, `Portfolio Management`, `Ledger` اضافه می‌شوند. `Settlement Port` به پیاده‌سازی کاملاً داخلی (Ledger) تغییر می‌کند. تفکیک کامل بین دارایی‌های پلتفرم، آگهی‌های کاربران، و جریان‌های مالی باید حفظ شود.

---

## ۱۰. مرزهای حیاتی MVP

پلتفرم در فاز ۱ **نباید**: پول را لمس کند؛ چک را نگهداری کند؛ ضمانت وصول بدهد؛ قیمت الزام‌آور ایجاد کند؛ یا نقش خریدار/فروشنده بگیرد.

کنترل این مرزها از طریق `Policy Engine`، `Feature Flags`، `Permission Model`، و `Audit Trail` در لایه‌ی API/BFF (بخش ۴.۲) اجرا می‌شود — نه فقط در سند توضیح داده می‌شود.

---

## ۱۱. جمع‌بندی

معماری نهایی یک **Modular Monolith با Event-Driven داخلی (Django signals + Celery برای کار async)** است که ماژول‌های کسب‌وکاری در `backend/doion/` پیاده شده‌اند، توسعه‌پذیری لایه ۲/۳ از طریق Settlement Port و `settlement_type` رزرو شده، و قرارداد API زنده جدا از این سند در MASTER_API_CONTRACT نگهداری می‌شود.