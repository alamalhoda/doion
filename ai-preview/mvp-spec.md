# مشخصات فنی MVP — چک‌بازار
## Frontend & UX Specification for Engineering Team

> **راهنمای استفاده:** این سند مرجع اجرایی تیم فنی است. هر بخش یک سؤال UX را از پیش پاسخ می‌دهد تا توسعه بدون ابهام آغاز شود. سند را همراه با `cheque-platform-low-level-design.md` و `cheque-marketplace-design-system.md` مطالعه کنید.

---

## ۱. State Machines — ماشین حالت موجودیت‌ها

### ۱.۱ User / کاربر

```
                    ┌─────────────────────────────┐
                    │         REGISTERED           │  ← ثبت‌نام با موبایل + OTP
                    └──────────────┬──────────────┘
                                   │ [submit_kyc_docs]
                                   ▼
                    ┌─────────────────────────────┐
                    │        KYC_PENDING           │  ← مدارک آپلود شده، منتظر بررسی
                    └───────────┬────────┬────────┘
                                │        │
              [moderator_approve]        [moderator_reject]
                                │        │
                    ┌───────────▼┐      ┌▼────────────────┐
                    │KYC_APPROVED│      │  KYC_REJECTED   │  ← با دلیل مشخص
                    └───────────┬┘      └┬────────────────┘
                                │        │ [resubmit_docs]
                [admin_suspend] │        └──────────────────→ KYC_PENDING
                                ▼
                    ┌─────────────────────────────┐
                    │         SUSPENDED            │  ← admin_reinstate → KYC_APPROVED
                    └─────────────────────────────┘
```

**جدول کامل transitions:**

| از وضعیت | رویداد | به وضعیت | actor | side-effects |
|---|---|---|---|---|
| `REGISTERED` | `submit_kyc_docs` | `KYC_PENDING` | کاربر | emit `VerificationSubmitted` |
| `KYC_PENDING` | `moderator_approve` | `KYC_APPROVED` | Moderator | emit `UserVerified`، ارسال SMS |
| `KYC_PENDING` | `moderator_reject` | `KYC_REJECTED` | Moderator | emit `VerificationRejected`، ارسال SMS با دلیل |
| `KYC_REJECTED` | `resubmit_docs` | `KYC_PENDING` | کاربر | emit `VerificationSubmitted` مجدد |
| `KYC_APPROVED` | `admin_suspend` | `SUSPENDED` | Admin | emit `UserSuspended`، revoke tokens |
| `SUSPENDED` | `admin_reinstate` | `KYC_APPROVED` | Admin | emit `UserReinstated` |

**قوانین دسترسی بر اساس وضعیت:**

| عملیات | REGISTERED | KYC_PENDING | KYC_APPROVED | KYC_REJECTED | SUSPENDED |
|---|---|---|---|---|---|
| مشاهده بازارچه | ✅ | ✅ | ✅ | ✅ | ❌ |
| ثبت آگهی | ❌ | ❌ | ✅ | ❌ | ❌ |
| ابراز تمایل | ❌ | ❌ | ✅ | ❌ | ❌ |
| آپلود مدارک KYC | ✅ | ❌ | ❌ | ✅ | ❌ |

---

### ۱.۲ ChequeListing / آگهی چک

```
         [submit]                [moderator_approve]
DRAFT ──────────────→ PENDING_MODERATION ──────────────→ PUBLISHED
                              │                               │
                    [moderator_reject]              [investor_interest +
                              │                      holder_accept]
                              ▼                               │
                        REJECTED ──[resubmit]──→ PENDING     ▼
                                                         MATCHED
                                                          │    │
                                             [both_confirm]    [cancel_match]
                                                  │                  │
                                                  ▼                  ▼
                                      SETTLED_OFF_PLATFORM       PUBLISHED
                                                  
         PUBLISHED ──[due_date_passed]──→ EXPIRED
         PUBLISHED ──[holder_withdraw]──→ WITHDRAWN
         MATCHED   ──[due_date_passed]──→ EXPIRED  (با ثبت در audit log)
```

**جدول کامل transitions:**

| از | رویداد | به | actor | شرایط | side-effects |
|---|---|---|---|---|---|
| `DRAFT` | `submit` | `PENDING_MODERATION` | CheckHolder | KYC_APPROVED | emit `ListingSubmittedForModeration` |
| `PENDING_MODERATION` | `approve` | `PUBLISHED` | Moderator | — | emit `ChequeListingPublished` |
| `PENDING_MODERATION` | `reject` | `REJECTED` | Moderator | rejection_reason مشخص باشد | emit `ListingRejected` + SMS |
| `REJECTED` | `resubmit` | `PENDING_MODERATION` | CheckHolder | تغییر حداقل یک فیلد | emit `ListingSubmittedForModeration` |
| `PUBLISHED` | `match_accepted` | `MATCHED` | سیستم | Match در حالت ACCEPTED | emit `ListingMatched` |
| `PUBLISHED` | `expire` | `EXPIRED` | سیستم (Celery beat) | due_date < now | emit `ListingExpired` |
| `PUBLISHED` | `withdraw` | `WITHDRAWN` | CheckHolder | هیچ Match فعالی نباشد | emit `ListingWithdrawn` |
| `MATCHED` | `settle` | `SETTLED_OFF_PLATFORM` | CheckHolder | — | emit `SettlementRecorded` |
| `MATCHED` | `cancel_match` | `PUBLISHED` | هر دو طرف | — | emit `MatchCancelled` |

**نکات مهم:**
- `REJECTED` → `PENDING_MODERATION` حداکثر ۳ بار مجاز است؛ بعد از آن به Admin ارجاع می‌شود.
- آگهی در وضعیت `EXPIRED` قابل ویرایش یا ارسال مجدد نیست.
- هر تغییر وضعیت یک رکورد در `audit_events` ثبت می‌کند.

---

### ۱.۳ Match / تطابق

```
                         [holder_accept]
          PENDING ──────────────────────→ ACCEPTED
             │                               │
   [holder_decline]               [both_off_platform_confirm]
             │                               │
             ▼                               ▼
         DECLINED                OFF_PLATFORM_CONFIRMED
                                             │
                                   [admin_close / auto]
                                             │
                                             ▼
                                          SETTLED
                                             
          ACCEPTED ──[either_cancel]──→ CANCELLED
          PENDING  ──[listing_expired]──→ CANCELLED  (auto)
```

**جدول کامل transitions:**

| از | رویداد | به | actor | side-effects |
|---|---|---|---|---|
| `PENDING` | `holder_accept` | `ACCEPTED` | CheckHolder | emit `MatchAccepted` + اطلاع‌رسانی investor |
| `PENDING` | `holder_decline` | `DECLINED` | CheckHolder | emit `MatchDeclined` + اطلاع‌رسانی investor |
| `PENDING` | `listing_expired` | `CANCELLED` | سیستم | emit `MatchCancelled` (auto) |
| `ACCEPTED` | `both_confirm` | `OFF_PLATFORM_CONFIRMED` | هر دو طرف | emit `SettlementConfirmed` |
| `ACCEPTED` | `cancel` | `CANCELLED` | هر دو طرف | emit `MatchCancelled` + listing → PUBLISHED |
| `OFF_PLATFORM_CONFIRMED` | `close` | `SETTLED` | سیستم / Admin | emit `MatchSettled` |

**settlement_type:**
- لایه ۱: `off_platform` (پیش‌فرض) — فقط ثبت رکورد
- لایه ۲ (آینده): `escrow` — فعال‌سازی Settlement Port
- لایه ۳ (آینده): `principal_ledger`

---

## ۲. Error States — کاتالوگ خطا

### ۲.۱ خطاهای احراز هویت

| کد خطا | پیام نمایشی | راهنمای کاربر | HTTP |
|---|---|---|---|
| `AUTH_001` | کد تأیید نامعتبر است | کد جدید درخواست دهید | 400 |
| `AUTH_002` | کد تأیید منقضی شده | کد جدید درخواست دهید | 400 |
| `AUTH_003` | تعداد تلاش بیش از حد | ۱۵ دقیقه صبر کنید | 429 |
| `AUTH_004` | توکن منقضی شده | مجدداً وارد شوید | 401 |
| `AUTH_005` | حساب معلق است | با پشتیبانی تماس بگیرید | 403 |

**رفتار UI برای AUTH_003 (rate limit):**
```
┌─────────────────────────────────────────┐
│  ⚠️  تعداد تلاش بیش از حد              │
│  لطفاً ۱۴:۳۲ دیگر صبر کنید.           │
│  [شمارش معکوس زنده]                    │
│                          [بستن]         │
└─────────────────────────────────────────┘
```

---

### ۲.۲ خطاهای KYC

| کد خطا | دلیل رد | پیام نمایشی | اقدام بعدی |
|---|---|---|---|
| `KYC_101` | تصویر مدرک ناخوانا | لطفاً تصویر با کیفیت‌تر آپلود کنید | رفتن به مرحله آپلود |
| `KYC_102` | اطلاعات مغایرت دارد | اطلاعات با مدارک مطابقت ندارد | ویرایش اطلاعات |
| `KYC_103` | مدارک ناقص | مدرک شناسه کامل نیست | آپلود مجدد |
| `KYC_104` | هویت قبلاً ثبت شده | این هویت در سیستم وجود دارد | تماس با پشتیبانی |

**State UI بعد از رد KYC:**
```
داشبورد کاربر:

  [!] KYC شما رد شد                              [×]
  ──────────────────────────────────────────────
  دلیل: تصویر کارت ملی ناخوانا است
  
  ← برای بارگذاری مجدد اینجا کلیک کنید
  
  راهنما: عکس واضح با نور کافی، بدون انعکاس
  ──────────────────────────────────────────────
  [اصلاح و ارسال مجدد]          [تماس پشتیبانی]
```

---

### ۲.۳ خطاهای ثبت آگهی

| کد خطا | فیلد | پیام | validation |
|---|---|---|---|
| `LST_201` | `face_amount` | مبلغ باید بیشتر از صفر باشد | `> 0` |
| `LST_202` | `due_date` | سررسید باید در آینده باشد | `> today + 7 days` |
| `LST_203` | `sayad_number` | کد صیاد باید ۱۶ رقم باشد | `len == 16, numeric` |
| `LST_204` | `sayad_number` | این چک قبلاً ثبت شده | unique check در DB |
| `LST_205` | — | سقف ثبت آگهی روزانه (۱۰ آگهی) | rate limit |
| `LST_206` | `documents` | حداقل یک تصویر از چک الزامی است | required |

**رفتار UI برای LST_204 (چک تکراری):**
```
┌──────────────────────────────────────────────┐
│  ⛔ این چک قبلاً در سیستم ثبت شده است       │
│                                              │
│  کد صیاد: ۱۴۰۲ ۱۰۳۵ ۶۸۷۱ ۲۳               │
│  تاریخ ثبت: ۱۴۰۴/۰۱/۱۲                     │
│  وضعیت: منتشرشده                            │
│                                              │
│  اگر این چک متعلق به شما نیست، گزارش دهید. │
│                                              │
│  [گزارش تخلف]              [بازگشت]         │
└──────────────────────────────────────────────┘
```

---

### ۲.۴ خطاهای Moderation (رد آگهی)

| کد خطا | دلیل رد | پیام به کاربر |
|---|---|---|
| `MOD_301` | اطلاعات چک ناقص | لطفاً تمام فیلدهای اجباری را تکمیل کنید |
| `MOD_302` | تصویر چک ناخوانا | تصویر واضح از جلو و پشت چک ارائه دهید |
| `MOD_303` | عدم تطابق اطلاعات | اطلاعات وارد‌شده با تصویر چک مطابقت ندارد |
| `MOD_304` | محتوای غیرمجاز | — (پیام عمومی، جزئیات در داشبورد Admin) |
| `MOD_305` | مدارک صادرکننده ناقص | مدارک هویتی صادرکننده را کامل ارائه دهید |

**State UI آگهی رد شده در داشبورد:**
```
  ┌────────────────────────────────────────────┐
  │  ⚠️  چک بانک ملت — شرکت آسان‌پرداخت       │
  │  ────────────────────────────────────────  │
  │  وضعیت: رد شده                            │
  │  دلیل: تصویر چک ناخوانا است (MOD_302)     │
  │  تاریخ بررسی: ۱۴۰۴/۰۱/۱۵                 │
  │                                            │
  │  تلاش مجدد: ۱ از ۳                         │
  │                                            │
  │  [اصلاح و ارسال مجدد]    [حذف آگهی]       │
  └────────────────────────────────────────────┘
```

---

### ۲.۵ Empty States — وضعیت خالی

| صفحه / بخش | وضعیت | عنوان | توضیح | CTA |
|---|---|---|---|---|
| بازارچه | بدون نتیجه فیلتر | فرصتی یافت نشد | معیارهای جست‌وجو را تغییر دهید | بازنشانی فیلترها |
| داشبورد — آگهی‌های من | کاربر جدید | هنوز آگهی ثبت نکرده‌اید | اولین چک خود را در چند دقیقه ثبت کنید | ثبت آگهی |
| داشبورد — ابراز تمایل | کاربر جدید | هنوز ابراز تمایل نکرده‌اید | فرصت‌های سرمایه‌گذاری را بررسی کنید | مشاهده بازارچه |
| اعلان‌ها | بدون اعلان | همه چیز مرتب است | اعلان جدیدی ندارید | — |
| صف Moderation | صف خالی | صف خالی است | تمام آگهی‌ها بررسی شده‌اند | — |

---

### ۲.۶ خطاهای شبکه و سرور

| وضعیت | پیام نمایشی | رفتار UI |
|---|---|---|
| آفلاین (no connection) | اتصال اینترنت برقرار نیست | نوار هشدار بالای صفحه، غیرفعال کردن فرم‌ها |
| 500 Server Error | خطای موقت سرور — لطفاً مجدد تلاش کنید | دکمه Retry + timestamp |
| 503 Service Unavailable | سیستم در حال به‌روزرسانی است | صفحه maintenance با زمان تقریبی |
| Timeout | پاسخ سرور دیر کرد | Retry خودکار (۱ بار) + پیام به کاربر |

---

## ۳. API Specification — مشخصات کامل Endpoint‌ها

### پایه‌ها

```
Base URL:    https://api.cheque-bazaar.ir/api/v1
Auth:        Bearer JWT (djangorestframework-simplejwt)
Content-Type: application/json; charset=utf-8
Date format: ISO 8601 — "2025-04-05T10:30:00Z"
```

**فرمت یکنواخت خطا:**
```json
{
  "error": {
    "code": "LST_204",
    "message": "این چک قبلاً در سیستم ثبت شده است",
    "details": {
      "sayad_number": ["کد صیاد ۱۴۰۲۱۰۳۵۶۸۷۱۲۳ تکراری است"]
    },
    "request_id": "req_8f3a2c1d"
  }
}
```

---

### ۳.۱ Auth — احراز هویت

#### `POST /auth/otp/request/`
درخواست OTP برای شماره موبایل.

**Request:**
```json
{ "phone_number": "09121234567" }
```
**Response 200:**
```json
{
  "message": "کد تأیید ارسال شد",
  "expires_in_seconds": 120,
  "retry_after_seconds": 60
}
```
**Errors:** `AUTH_003` (rate limit)

---

#### `POST /auth/otp/verify/`
تأیید OTP و دریافت token.

**Request:**
```json
{
  "phone_number": "09121234567",
  "otp_code": "123456",
  "role": "check_holder"   // "check_holder" | "investor" | "institutional_investor"
}
```
**Response 200:**
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci...",
  "user": {
    "id": "uuid",
    "phone_number": "09121234567",
    "role": "check_holder",
    "kyc_status": "registered",
    "full_name": null
  }
}
```

---

#### `POST /auth/token/refresh/`
**Request:** `{ "refresh": "eyJhbGci..." }`
**Response 200:** `{ "access": "eyJhbGci..." }`

---

### ۳.۲ Users — کاربران

#### `GET /users/me/`
**Response 200:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "phone_number": "09121234567",
  "role": "check_holder",
  "kyc_status": "approved",
  "profile": {
    "full_name": "رضا کریمی",
    "company_name": null,
    "national_id": "0012345678",
    "kyc_level": "basic"
  },
  "created_at": "2025-01-15T08:30:00Z"
}
```

#### `PATCH /users/me/`
**Request (partial update):**
```json
{ "profile": { "full_name": "رضا کریمی" } }
```

---

### ۳.۳ Verifications — KYC

#### `POST /verifications/`
شروع فرایند KYC.

**Request (multipart/form-data):**
```
national_id_front:  [file]
national_id_back:   [file]
selfie:             [file] (optional, future)
full_name:          "رضا کریمی"
national_code:      "0012345678"
```
**Response 201:**
```json
{
  "id": "uuid",
  "status": "pending",
  "submitted_at": "2025-01-15T08:30:00Z",
  "estimated_review_hours": 24
}
```

#### `GET /verifications/status/`
**Response 200:**
```json
{
  "status": "rejected",
  "rejection_code": "KYC_101",
  "rejection_reason": "تصویر مدرک ناخوانا است",
  "reviewed_at": "2025-01-16T10:00:00Z",
  "can_resubmit": true
}
```

---

### ۳.۴ Listings — آگهی‌های چک

#### `GET /marketplace/listings/`
**Query params:**

| پارامتر | نوع | مثال | توضیح |
|---|---|---|---|
| `risk_tier` | string | `low,mid` | فیلتر ریسک (comma-separated) |
| `max_days_to_due` | int | `90` | حداکثر روز تا سررسید |
| `min_amount` | int | `100000000` | حداقل مبلغ (ریال) |
| `max_amount` | int | `1000000000` | حداکثر مبلغ |
| `issuer_type` | string | `legal` | `legal` / `natural` |
| `bank_name` | string | `ملت` | نام بانک |
| `ordering` | string | `-created_at` | فیلدهای مرتب‌سازی |
| `page` | int | `1` | صفحه‌بندی |
| `page_size` | int | `20` | تعداد در هر صفحه (max: 50) |

**Response 200:**
```json
{
  "count": 142,
  "next": "/api/v1/marketplace/listings/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "issuer_name": "شرکت آسان‌پرداخت",
      "issuer_type": "legal",
      "bank_name": "بانک ملت",
      "face_amount": "500000000",
      "due_date": "2025-06-10",
      "days_to_due": 45,
      "suggested_discount_rate": "3.80",
      "risk_tier": "low",
      "credit_score": 78,
      "status": "published",
      "published_at": "2025-04-25T09:00:00Z",
      "interest_count": 3
    }
  ]
}
```

---

#### `POST /listings/`
ثبت آگهی جدید (فقط `check_holder` با KYC تأییدشده).

**Request:**
```json
{
  "face_amount": 500000000,
  "due_date": "2025-06-10",
  "bank_name": "بانک ملت",
  "sayad_number": "1402103568712345",
  "issuer_type": "legal",
  "issuer_name": "شرکت آسان‌پرداخت",
  "issuer_national_id": "10100345678",
  "description": "توضیحات اختیاری"
}
```
**Response 201:**
```json
{
  "id": "uuid",
  "status": "pending_moderation",
  "created_at": "2025-04-25T09:00:00Z",
  "estimated_review_hours": 24
}
```
**Errors:** `LST_201`, `LST_202`, `LST_203`, `LST_204`, `LST_205`

---

#### `GET /listings/{id}/`
جزئیات کامل یک آگهی (برای صاحب آگهی، فیلدهای حساس‌تر نمایش داده می‌شوند).

#### `PATCH /listings/{id}/`
ویرایش آگهی (فقط مالک، فقط در وضعیت `draft` یا `rejected`).

**Request:** هر زیرمجموعه‌ای از فیلدهای `POST /listings/`

#### `POST /listings/{id}/withdraw/`
پس‌گرفتن آگهی (فقط مالک، فقط در وضعیت `published` بدون Match فعال).
**Response 200:** `{ "status": "withdrawn" }`

---

#### `POST /listings/{id}/documents/`
آپلود مدارک برای آگهی.

**Request (multipart/form-data):**
```
document_type:  "cheque_image" | "id_document" | "supplementary"
file:           [file]
```
**Response 201:**
```json
{
  "id": "uuid",
  "document_type": "cheque_image",
  "uploaded_at": "2025-04-25T09:05:00Z"
}
```
**Errors:** `LST_206` (فایل از 5MB بیشتر باشد)

---

### ۳.۵ Matches — تطابق

#### `POST /matches/`
ابراز تمایل توسط سرمایه‌گذار.

**Request:**
```json
{ "listing_id": "uuid" }
```
**Response 201:**
```json
{
  "id": "uuid",
  "listing_id": "uuid",
  "investor_id": "uuid",
  "status": "pending",
  "settlement_type": "off_platform",
  "created_at": "2025-04-25T10:00:00Z"
}
```
**Errors:** اگر کاربر قبلاً برای همین آگهی Match داشته باشد → 409 Conflict

---

#### `PATCH /matches/{id}/status/`
بروزرسانی وضعیت Match.

**Request:**
```json
{
  "action": "accept",       // "accept" | "decline" | "confirm_off_platform" | "cancel"
  "note": "توضیح اختیاری"   // برای decline الزامی است
}
```
**Response 200:**
```json
{
  "id": "uuid",
  "status": "accepted",
  "updated_at": "2025-04-25T11:00:00Z"
}
```

---

### ۳.۶ Moderation — پنل ناظر

#### `GET /moderation/queue/`
صف آگهی‌های در انتظار بررسی.

**Query params:** `ordering=-created_at`, `page`, `page_size`
**Response:** مشابه `GET /marketplace/listings/` با فیلدهای اضافه:
```json
{
  "results": [
    {
      "id": "uuid",
      "issuer_name": "...",
      "submitted_at": "...",
      "resubmit_count": 0,
      "documents": [
        { "id": "uuid", "document_type": "cheque_image", "url": "https://..." }
      ]
    }
  ]
}
```

#### `POST /moderation/listings/{id}/decision/`
تأیید یا رد آگهی.

**Request:**
```json
{
  "decision": "approve",   // "approve" | "reject"
  "rejection_code": "MOD_302",   // اگر decision == "reject"
  "rejection_note": "تصویر چک ناخوانا است"
}
```
**Response 200:** `{ "listing_id": "uuid", "new_status": "published" }`

---

#### `GET /moderation/kyc-queue/`
صف درخواست‌های KYC در انتظار.

#### `POST /moderation/verifications/{id}/decision/`
تأیید یا رد KYC.

```json
{
  "decision": "approve",   // "approve" | "reject"
  "rejection_code": "KYC_101",
  "rejection_note": "تصویر کارت ملی ناخوانا است"
}
```

---

### ۳.۷ Notifications — اعلان‌ها

#### `GET /notifications/`
**Query params:** `type` (match/kyc/system), `is_read` (true/false), `page`

**Response 200:**
```json
{
  "unread_count": 3,
  "results": [
    {
      "id": "uuid",
      "type": "match_received",
      "title": "ابراز تمایل جدید دریافت شد",
      "body": "یک سرمایه‌گذار به آگهی چک ۵۰۰ میلیونی شما ابراز تمایل کرد",
      "related_object_type": "listing",
      "related_object_id": "uuid",
      "is_read": false,
      "created_at": "2025-04-25T14:00:00Z"
    }
  ]
}
```

#### `POST /notifications/{id}/read/`
علامت‌گذاری به‌عنوان خوانده‌شده.

#### `POST /notifications/read-all/`
علامت‌گذاری همه به‌عنوان خوانده‌شده.

---

### ۳.۸ Feature Flags

#### `GET /feature-flags/`
**Response:**
```json
{
  "results": [
    { "key": "escrow_enabled", "is_enabled": false, "description": "فعال‌سازی لایه ۲" },
    { "key": "institutional_investor_api", "is_enabled": false }
  ]
}
```

#### `PATCH /feature-flags/{key}/`  (Admin only)
```json
{ "is_enabled": true }
```

---

## ۴. Notification Types — انواع اعلان

| نوع | تریگر | گیرنده | کانال |
|---|---|---|---|
| `kyc_approved` | تأیید KYC | کاربر | SMS + in-app |
| `kyc_rejected` | رد KYC | کاربر | SMS + in-app |
| `listing_published` | انتشار آگهی | CheckHolder | SMS + in-app |
| `listing_rejected` | رد آگهی | CheckHolder | SMS + in-app |
| `listing_expired` | انقضای آگهی | CheckHolder | in-app |
| `match_received` | ابراز تمایل سرمایه‌گذار | CheckHolder | SMS + in-app |
| `match_accepted` | پذیرش توسط دارنده | Investor | in-app |
| `match_declined` | رد توسط دارنده | Investor | in-app |
| `match_cancelled` | لغو Match | هر دو طرف | in-app |
| `settlement_confirmed` | تأیید تسویه | هر دو طرف | in-app |
| `new_moderation_item` | آگهی/KYC جدید | Moderator | in-app |

---

## ۵. UI Behavior Spec — رفتار UI در موقعیت‌های خاص

### ۵.۱ Loading States
- دکمه‌های submit در حین ارسال: `disabled` + spinner + متن «در حال ارسال...»
- لیست‌ها در حین بارگذاری: skeleton cards (نه spinner خالی)
- Modal در حین بارگذاری داده: spinner مرکزی

### ۵.۲ Optimistic Updates
- علامت‌گذاری اعلان به‌عنوان خوانده‌شده: فوری در UI، rollback در صورت خطا
- Bookmark آگهی: فوری در UI، rollback در صورت خطا

### ۵.۳ Confirmation Dialogs (قبل از عملیات برگشت‌ناپذیر)

| عملیات | متن تأییدیه |
|---|---|
| حذف آگهی | «آگهی شما حذف خواهد شد و قابل بازیابی نیست. ادامه می‌دهید؟» |
| پس‌گرفتن آگهی | «آگهی از بازارچه حذف می‌شود. ادامه می‌دهید؟» |
| لغو Match | «این تطابق لغو و آگهی مجدداً منتشر می‌شود. ادامه می‌دهید؟» |
| تعلیق کاربر | «حساب کاربری معلق می‌شود. ادامه می‌دهید؟» |

### ۵.۴ Accessibility
- تمام دکمه‌های icon-only باید `aria-label` داشته باشند
- رنگ ریسک نباید تنها نشانه باشد — متن کنار آن اجباری است
- فرم‌ها باید keyboard-navigable باشند

---

## ۶. Onboarding Checklist

برای کاربر تازه‌وارد در داشبورد:

```
آماده شروع هستید؟

✅ ثبت‌نام با موبایل — انجام شد
○  احراز هویت (KYC) — [شروع احراز هویت ←]
○  ثبت اولین آگهی — (پس از تأیید KYC)
○  اتصال به سرمایه‌گذار
```

---

## ۷. Glossary — واژه‌نامه UI

| اصطلاح فارسی | معادل انگلیسی | توضیح |
|---|---|---|
| آگهی چک | ChequeListing | یک آگهی برای فروش/تنزیل یک چک |
| دارنده چک | CheckHolder | کسی که چک دارد و می‌خواهد نقد کند |
| سرمایه‌گذار | Investor | خریدار بالقوه چک |
| ابراز تمایل | Match / Interest | اعلام علاقه سرمایه‌گذار به یک آگهی |
| نرخ تنزیل | Discount Rate | درصد کسر از مبلغ اسمی چک |
| سررسید | Due Date | تاریخ وصول چک |
| کد صیاد | Sayad Number | شناسه ۱۶ رقمی چک در سامانه بانک مرکزی |
| بررسی ناظر | Moderation | تأیید دستی آگهی قبل از انتشار |
| تسویه | Settlement | نهایی شدن معامله بیرون از پلتفرم |
