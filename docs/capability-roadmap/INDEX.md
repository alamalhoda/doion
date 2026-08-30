# ایندکس کاتالوگ قابلیت

تابلوی پیگیری. قوانین وضعیت و موج: [`taxonomy.md`](taxonomy.md). معرفی کاتالوگ: [`README.md`](README.md).  
**قبل از شروع هر برش:** [`usage-guide.md`](usage-guide.md).  
**قبل از Think/Build برای KYC، SMS، صیاد، اعتبار صادرکننده، امضا، یا OCR چک:** [`vendor-landscape.md`](vendor-landscape.md).

همهٔ کارت‌ها در ۱۴۰۵/۰۶/۰۸ (2026-08-30) با وضعیت اولیه ثبت شده‌اند. پس از مرور شریک/تیم، `draft` را به `clarified` یا `ready` ببرید.

## W0 — پیش‌نیاز لایه ۱

| ID | نام | ریل | مجوز | کانال | وضعیت | مسدودکننده | برش بعدی | impl |
|----|-----|-----|------|--------|--------|------------|----------|------|
| [CY-001](capabilities/CY-001-live-kyc-sms-adapters/capability.md) | اتصال زنده KYC و پیامک | n/a | none-layer1 | listing_only | draft | — | [CY-001-b](capabilities/CY-001-live-kyc-sms-adapters/slices/CY-001-b-identity-inquiry-port.md) | — |
| [CY-002](capabilities/CY-002-sayad-inquiry/capability.md) | استعلام وضعیت چک صیادی | n/a | none-layer1 | listing_only | draft | کانال استعلام | CY-002-a (فایل بعد از تثبیت فیلد) | — |
| [CY-019](capabilities/CY-019-issuer-credit-inquiry/capability.md) | استعلام اعتبار صادرکننده | n/a | partner-covers | listing_only | draft | کانال bureau | CY-019-a | — |
| [CY-020](capabilities/CY-020-cheque-document-ocr-assist/capability.md) | کمک OCR ورود مشخصات چک | n/a | none-layer1 | listing_only | draft | — | [CY-020-a](capabilities/CY-020-cheque-document-ocr-assist/slices/CY-020-a-cheque-ocr-suggest-port.md) | — |

## W1 — هم‌برند؛ فقط معامله با صندوق / امانی بانک

ثالث روی تابلو می‌ماند اما ریل پول او `off_platform` است.

| ID | نام | ریل | مجوز | کانال | وضعیت | مسدودکننده | برش بعدی | impl |
|----|-----|-----|------|--------|--------|------------|----------|------|
| [CY-003](capabilities/CY-003-cobrand-multi-institution/capability.md) | هم‌برند چندنهادی | n/a | partner-covers | mixed | draft | — | [CY-003-a](capabilities/CY-003-cobrand-multi-institution/slices/CY-003-a-institution-tenant-model.md) | — |
| [CY-004](capabilities/CY-004-partner-counterparty-gate/capability.md) | دروازهٔ طرف معامله | off_platform | partner-covers | partner_trade | draft | CY-003 | [CY-004-a](capabilities/CY-004-partner-counterparty-gate/slices/CY-004-a-restrict-match-counterparty.md) | — |
| [CY-005](capabilities/CY-005-escrow-bank-settlement/capability.md) | ریل امانی بانک | escrow | partner-covers | partner_trade | draft | CY-003، CY-004 | [CY-005-a](capabilities/CY-005-escrow-bank-settlement/slices/CY-005-a-escrow-settlement-port.md) | — |
| [CY-006](capabilities/CY-006-principal-fund-liquidity/capability.md) | نقدینگی صندوق (principal) | principal_ledger | partner-covers | partner_trade | draft | CY-003، CY-004 | [CY-006-a](capabilities/CY-006-principal-fund-liquidity/slices/CY-006-a-principal-ledger-fund-buyer.md) | — |
| [CY-007](capabilities/CY-007-deal-contract-sayad-sync/capability.md) | قرارداد و وضعیت صیاد | n/a | partner-covers | partner_trade | draft | CY-005، CY-006 | [CY-007-a](capabilities/CY-007-deal-contract-sayad-sync/slices/CY-007-a-deal-contract-record.md) | — |
| [CY-008](capabilities/CY-008-partner-integration-ports/capability.md) | درگاه یکپارچه‌سازی بانک/صندوق | n/a | partner-covers | partner_trade | draft | CY-003 | [CY-008-a](capabilities/CY-008-partner-integration-ports/slices/CY-008-a-bank-fund-adapter-stubs.md) | — |

ترتیب پیشنهادی اجرا: **CY-003-a → CY-008-a → CY-004-a → CY-005-a و CY-006-a (موازی پس از دروازه) → CY-007-a**. پوستهٔ UI: CY-003-b پس از CY-003-a.

## W2 — چتر ثالث، قیمت، نکول

| ID | نام | ریل | مجوز | کانال | وضعیت | مسدودکننده | برش بعدی | impl |
|----|-----|-----|------|--------|--------|------------|----------|------|
| [CY-009](capabilities/CY-009-third-party-legal-umbrella/capability.md) | چتر حقوقی سرمایه‌گذار ثالث | n/a | additional-permit | third_party_trade | blocked | نظر حقوقی شریک | — | — |
| [CY-010](capabilities/CY-010-third-party-escrow-trades/capability.md) | امانی برای ثالث | escrow | partner-covers | third_party_trade | blocked | CY-009، CY-005 | — | — |
| [CY-011](capabilities/CY-011-pricing-engine-auction/capability.md) | موتور قیمت و حراج | n/a | unknown | mixed | draft | CY-006 (داده) | CY-011-a | — |
| [CY-012](capabilities/CY-012-default-collection-guarantee/capability.md) | نکول، وصول، ضمانت | n/a | additional-permit | partner_trade | draft | CY-006 | CY-012-a | — |

## W3 — کلاس دارایی و عملیات بنگاه

| ID | نام | ریل | مجوز | کانال | وضعیت | مسدودکننده | برش بعدی | impl |
|----|-----|-----|------|--------|--------|------------|----------|------|
| [CY-013](capabilities/CY-013-invoice-scf-factoring/capability.md) | فاکتور و SCF | principal_ledger | partner-covers | partner_trade | draft | CY-006 | CY-013-a | — |
| [CY-014](capabilities/CY-014-secondary-market/capability.md) | بازار ثانویه | principal_ledger | additional-permit | mixed | draft | CY-006، CY-009* | CY-014-a | — |
| [CY-015](capabilities/CY-015-treasury-accounting-integrations/capability.md) | خزانه و حسابداری | n/a | none-layer1 | listing_only | draft | CY-006 | CY-015-a | — |

\* اگر پایلوت ثانویه فقط صندوق-به-صندوق باشد، `CY-009` ممکن است کنار برود (سؤال باز کارت).

## W4 — توزیع و داده

| ID | نام | ریل | مجوز | کانال | وضعیت | مسدودکننده | برش بعدی | impl |
|----|-----|-----|------|--------|--------|------------|----------|------|
| [CY-016](capabilities/CY-016-white-label/capability.md) | وایت‌لیبل | n/a | partner-covers | mixed | draft | CY-003 | CY-016-a | — |
| [CY-017](capabilities/CY-017-market-data-products/capability.md) | محصولات داده | n/a | unknown | listing_only | draft | CY-011 | CY-017-a | — |
| [CY-018](capabilities/CY-018-open-partner-api/capability.md) | API باز نهاد/فین‌تک | n/a | partner-covers | mixed | draft | CY-008 | CY-018-a | — |
