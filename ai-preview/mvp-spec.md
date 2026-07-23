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
| `registered` | `submit_kyc_docs` | `pending` | کاربر | ایجاد رکورد `Verification`، emit `VerificationSubmitted` |
| `pending` | `moderator_approve` | `approved` | Moderator | emit `VerificationApproved`، `profile.is_verified = True`، ارسال SMS |
| `pending` | `moderator_reject` | `rejected` | Moderator | emit `VerificationRejected`، ارسال SMS با دلیل |
| `rejected` | `resubmit_docs` | `pending` | کاربر | ایجاد/به‌روزرسانی `Verification` مجدد |
| `approved` | `admin_suspend` | — | Admin | `User.is_active = False`، revoke tokens |
| `approved` | `admin_reinstate` | — | Admin | `User.is_active = True` |

**قوانین دسترسی بر اساس وضعیت:**

| عملیات | registered | pending | approved | rejected | suspended |
|---|---|---|---|---|---|
| مشاهده بازارچه | ✅ | ✅ | ✅ | ✅ | ❌ |
| ثبت آگهی | ❌ | ❌ | ✅ | ❌ | ❌ |
| ابراز تمایل | ❌ | ❌ | ✅ | ❌ | ❌ |
| آپلود مدارک KYC | ✅ | ❌ | ❌ | ✅ | ❌ |

---

### ۱.۲ ChequeListing / آگهی چک

```
          [submit]                [moderator_approve]
pending_moderation ──────────────→ published
                               │               │
                     [moderator_reject]    [match_accepted]
                               │               │
                               ▼               ▼
                         rejected ──[resubmit]──→ pending_moderation
                                                          │    │
                                             [cancel_match]    [settle]
                                                   │                  │
                                                   ▼                  ▼
                                       published       settled_off_platform
                                                   
          published ──[due_date_passed]──→ expired
          published ──[holder_withdraw]──→ withdrawn
          matched   ──[due_date_passed]──→ expired  (با ثبت در audit log)
```

**جدول کامل transitions:**

| از | رویداد | به | actor | شرایط | side-effects |
|---|---|---|---|---|---|
| `pending_moderation` | `approve` | `published` | Moderator | — | emit `ChequeListingPublished` |
| `pending_moderation` | `reject` | `rejected` | Moderator | `rejection_reason` مشخص باشد | emit `ListingRejected` + SMS |
| `rejected` | `resubmit` | `pending_moderation` | CheckHolder | تغییر حداقل یک فیلد و `resubmit_count < 3` | emit `ListingSubmittedForModeration` |
| `published` | `match_accepted` | `matched` | سیستم | Match در حالت `accepted` | emit `ListingMatched` |
| `published` | `expire` | `expired` | سیستم (Celery beat) | `due_date < today` | emit `ListingExpired` |
| `published` | `withdraw` | `withdrawn` | CheckHolder | هیچ Match فعالی نباشد | emit `ListingWithdrawn` |
| `matched` | `settle` | `settled_off_platform` | CheckHolder | — | emit `SettlementRecorded` |
| `matched` | `cancel_match` | `published` | هر دو طرف | — | emit `MatchCancelled` |

**نکات مهم:**
- `rejected` → `pending_moderation` حداکثر ۳ بار مجاز است (`resubmit_count`).
- آگهی در وضعیت `expired` قابل ویرایش یا ارسال مجدد نیست.
- هر تغییر وضعیت یک رکورد در `AuditEvent` ثبت می‌کند.

---

### ۱.۳ Match / تطابق

```
                          [accept]
           pending ──────────────────────→ accepted
              │                               │
    [decline]               [confirm_off_platform]
              │                               │
              ▼                               ▼
          declined                off_platform_confirmed
                                              │
                                    [admin_close / auto]
                                              │
                                              ▼
                                           settled
                      
           accepted ──[cancel]──→ cancelled
           pending  ──[listing_expired]──→ cancelled  (auto)
```

**جدول کامل transitions:**

| از | رویداد | به | actor | side-effects |
|---|---|---|---|---|
| `pending` | `accept` | `accepted` | CheckHolder | emit `MatchAccepted` + اطلاع‌رسانی investor |
| `pending` | `decline` | `declined` | CheckHolder | emit `MatchDeclined` + اطلاع‌رسانی investor |
| `pending` | `listing_expired` | `cancelled` | سیستم | emit `MatchCancelled` (auto) |
| `accepted` | `confirm_off_platform` | `off_platform_confirmed` | هر دو طرف | ایجاد `OffPlatformSettlement`، emit `SettlementConfirmed` |
| `accepted` | `cancel` | `cancelled` | هر دو طرف | emit `MatchCancelled` + listing → `published` |
| `off_platform_confirmed` | `close` | `settled` | سیستم / Admin | emit `MatchSettled` |

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
| `MOD_101` | اطلاعات ناقص | لطفاً تمام فیلدهای اجباری را تکمیل کنید |
| `MOD_102` | تصویر ناخوانا | تصویر واضح از چک ارائه دهید |
| `MOD_103` | عدم تطابق | اطلاعات وارد‌شده با تصویر چک مطابقت ندارد |
| `MOD_104` | محتوای غیرمجاز | — (پیام عمومی، جزئیات در داشبورد Admin) |
| `MOD_105` | مدارک صادرکننده ناقص | مدارک هویتی صادرکننده را کامل ارائه دهید |
| `MOD_106` | سایر | توضیح در پیام رد |

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

#### `POST /auth/login/`
دریافت JWT با نام کاربری، ایمیل یا شماره موبایل + رمز عبور.

**Request:**
```json
{
  "identifier": "09121234567",
  "password": "user-password"
}
```
**Response 200:**
```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci...",
  "user": {
    "id": 1,
    "username": "09121234567",
    "email": "",
    "name": "رضا کریمی",
    "phone": "+989123456789",
    "role": "check_holder"
  }
}
```
**Errors:** `AUTH_004` (اعتبار نامعتبر)، `AUTH_005` (حساب غیرفعال)

#### `POST /auth/refresh/`
تمدید access token.

**Request:** `{ "refresh": "eyJhbGci..." }`
**Response 200:** `{ "access": "eyJhbGci..." }`

---

#### `POST /identity/register/`
ثبت‌نام کاربر جدید.

**Request:**
```json
{
  "username": "09121234567",
  "email": "user@example.com",
  "password": "secure-pass",
  "password_confirm": "secure-pass",
  "name": "رضا کریمی",
  "phone": "+989123456789",
  "role": "check_holder"
}
```
**Response 201:** شیء کاربر ایجاد‌شده.

**Errors:** `AUTH_001` (رمزهای مطابقت ندارند)، `AUTH_003` (تعداد تلاش بیش از حد)

---

### ۳.۲ Users — کاربران

#### `GET /users/me/`
**Response 200:**
```json
{
  "id": 1,
  "username": "09121234567",
  "email": "user@example.com",
  "name": "رضا کریمی",
  "phone": "+989123456789",
  "role": "check_holder",
  "is_verified": false
}
```

#### `PATCH /users/me/`
**Request (partial update):**
```json
{ "name": "رضا کریمی", "email": "new@example.com" }
```
**Response 200:** شیء کاربر به‌روز شده.

---

#### `PATCH /identity/profile/`
بروزرسانی پروفایل (`bio`، `role`).

**Request:**
```json
{ "bio": "توضیحات اختیاری", "role": "investor" }
```
**Response 200:** شیء Profile به‌روز شده (شامل `user.username`, `user.email`, `user.name`, `user.phone`).

---

### ۳.۳ Verifications — KYC

#### `POST /verifications/`
شروع فرایند KYC.

**Request (multipart/form-data):**
```
national_id_front:  [file]
national_id_back:   [file]
selfie:             [file] (optional)
full_name:          "رضا کریمی"
national_id:        "0012345678"
company_name:       "شرکت آسان‌پرداخت"
```
**Response 201:**
```json
{
  "id": 1,
  "full_name": "رضا کریمی",
  "national_id": "0012345678",
  "company_name": "شرکت آسان‌پرداخت",
  "status": "pending",
  "rejection_reason": "",
  "documents": [
    { "id": 1, "document_type": "national_id_front", "file": "/media/documents/...", "file_size": 204800 }
  ]
}
```

#### `GET /verifications/me/`
آخرین درخواست KYC کاربر جاری.

**Response 200:** شیء `Verification` مشابه Response 201 بالا.

#### `GET /verifications/`
لیست درخواست‌های KYC کاربر جاری.

**Response 200:** آرایه‌ای از شیء `Verification`.

#### `GET /moderation/kyc/`
صف درخواست‌های KYC در انتظار بررسی (Moderator only).

#### `POST /moderation/kyc/{id}/decision/`
تأیید یا رد KYC.

**Request:**
```json
{
  "decision": "approve",
  "rejection_code": "KYC_101",
  "rejection_note": "تصویر کارت ملی ناخوانا است"
}
```
**Response 200:** `{ "id": 1, "status": "approved" }`

---

### ۳.۴ Listings — آگهی‌های چک

#### `POST /listings/`
ثبت آگهی جدید (فقط `check_holder` با KYC تأییدشده).

**Request:**
```json
{
  "issuer": 1,
  "bank_name": "بانک ملت",
  "cheque_serial_number": "1402103568712345",
  "face_amount": 500000000,
  "due_date": "2025-06-10",
  "issuer_type": "legal",
  "issuer_name": "شرکت آسان‌پرداخت",
  "issuer_national_id": "10100345678",
  "description": "توضیحات اختیاری"
}
```
**Response 201:**
```json
{
  "id": 1,
  "status": "pending_moderation",
  "created_at": "2025-04-25T09:00:00Z"
}
```
**Errors:** `LST_201`، `LST_202`، `LST_203`، `LST_204`، `LST_205`

---

#### `GET /marketplace/listings/`
لیست آگهی‌های `published` با فیلتر.

**Query params:**

| پارامتر | نوع | مثال | توضیح |
|---|---|---|---|
| `risk_tier` | string | `low,medium` | فیلتر ریسک (comma-separated) |
| `min_amount` | int | `100000000` | حداقل مبلغ (ریال) |
| `max_amount` | int | `1000000000` | حداکثر مبلغ |
| `issuer_type` | string | `legal` | `legal` / `natural` |
| `bank_name` | string | `ملت` | نام بانک |
| `ordering` | string | `-created_at` | فیلدهای مرتب‌سازی |
| `page` | int | `1` | صفحه‌بندی |
| `page_size` | int | `20` | تعداد در هر صفحه |

**Response 200:**
```json
{
  "count": 142,
  "next": "/api/v1/marketplace/listings/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "issuer_profile": {
        "id": 1,
        "national_or_company_id": "10100345678",
        "name": "شرکت آسان‌پرداخت",
        "credit_score": 78
      },
      "bank_name": "بانک ملت",
      "face_amount": "500000000",
      "due_date": "2025-06-10",
      "issuer_type": "legal",
      "suggested_discount_rate": "3.80",
      "risk_tier": "low",
      "status": "published",
      "days_to_due": 45,
      "interest_count": 3,
      "published_at": "2025-04-25T09:00:00Z",
      "created_at": "2025-04-25T09:00:00Z"
    }
  ]
}
```

---

#### `GET /listings/{id}/`
جزئیات کامل یک آگهی.

**Response 200:** شیء `ChequeListing` (شامل `issuer_profile`, `owner_id`, `description`, `rejection_code`, `resubmit_count`).

#### `PATCH /listings/{id}/`
ویرایش آگهی (فقط مالک، فقط در وضعیت `pending_moderation` یا `rejected`).

**Request:** هر زیرمجموعه‌ای از فیلدهای `POST /listings/`
**Response 200:** شیء به‌روز شده.

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
  "id": 1,
  "document_type": "cheque_image",
  "file": "/media/documents/...",
  "file_size": 204800
}
```
**Errors:** `LST_206` (فایل از 5MB بیشتر باشد)

---

#### `GET /issuer-profiles/`
لیست پروفایل‌های صادرکننده.

#### `GET /issuer-profiles/{id}/`
جزئیات پروفایل صادرکننده.

---

### ۳.۵ Matches — تطابق

#### `POST /matches/`
ابراز تمایل توسط سرمایه‌گذار.

**Request:**
```json
{ "listing_id": 1 }
```
**Response 201:**
```json
{
  "id": 1,
  "listing": {
    "id": 1,
    "bank_name": "بانک ملت",
    "face_amount": "500000000",
    "due_date": "2025-06-10",
    "status": "published",
    "created_at": "2025-04-25T09:00:00Z",
    "updated_at": "2025-04-25T09:00:00Z"
  },
  "investor": {
    "id": 2,
    "username": "investor_user",
    "name": "علی محمدی"
  },
  "check_holder": {
    "id": 1,
    "username": "holder_user",
    "name": "رضا کریمی"
  },
  "status": "pending",
  "settlement_type": "off_platform",
  "final_discount_rate": null,
  "terms": "",
  "message": "",
  "created_at": "2025-04-25T10:00:00Z",
  "updated_at": "2025-04-25T10:00:00Z"
}
```
**Errors:** 409 Conflict (اگر کاربر قبلاً برای همین آگهی Match داشته باشد)

#### `PATCH /matches/{id}/status/`
بروزرسانی وضعیت Match.

**Request:**
```json
{
  "status": "accepted",
  "final_discount_rate": "3.50",
  "terms": "توضیحات اختیاری"
}
```
**Response 200:**
```json
{
  "id": 1,
  "status": "accepted",
  "updated_at": "2025-04-25T11:00:00Z"
}
```

#### `POST /matches/{id}/confirm-off-platform/`
تأیید تسویه بیرون از پلتفرم.

**Response 200:** `{ "id": 1, "status": "off_platform_confirmed" }`

---

### ۳.۶ Moderation — پنل ناظر

#### `GET /moderation/queue/`
صف آگهی‌های در انتظار بررسی (Moderator only).

**Query params:** `ordering=-created_at`, `page`, `page_size`
**Response:** مشابه `GET /marketplace/listings/` با فیلدهای اضافه:
```json
{
  "results": [
    {
      "id": 1,
      "owner_id": 1,
      "issuer_profile": { "id": 1, "national_or_company_id": "...", "name": "...", "credit_score": 78 },
      "bank_name": "بانک ملت",
      "cheque_serial_number": "1402103568712345",
      "face_amount": "500000000",
      "due_date": "2025-06-10",
      "issuer_type": "legal",
      "issuer_name": "شرکت آسان‌پرداخت",
      "issuer_national_id": "10100345678",
      "description": "...",
      "suggested_discount_rate": "3.80",
      "risk_tier": "low",
      "status": "pending_moderation",
      "rejection_reason": "",
      "rejection_code": null,
      "resubmit_count": 0,
      "created_at": "2025-04-25T09:00:00Z"
    }
  ]
}
```

#### `POST /moderation/{id}/decision/`
تأیید یا رد آگهی.

**Request:**
```json
{
  "decision": "approve",   // "approve" | "reject"
  "rejection_code": "MOD_102",   // اگر decision == "reject"
  "rejection_note": "تصویر چک ناخوانا است"
}
```
**Response 200:** `{ "listing_id": 1, "new_status": "published" }`

---

#### `GET /moderation/kyc/`
صف درخواست‌های KYC در انتظار (Moderator only).

#### `POST /moderation/kyc/{id}/decision/`
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
**Query params:** `type` (match/kyc/system)، `status` (pending/sent/read/failed)، `page`

**Response 200:**
```json
{
  "unread_count": 0,
  "results": [
    {
      "id": 1,
      "type": "match_created",
      "channel": "in_app",
      "status": "sent",
      "title": "ابراز تمایل جدید دریافت شد",
      "message": "یک سرمایه‌گذار به آگهی چک ۵۰۰ میلیونی شما ابراز تمایل کرد",
      "related_object_type": "match",
      "related_object_id": "1",
      "read_at": null,
      "sent_at": "2025-04-25T14:00:00Z",
      "created_at": "2025-04-25T14:00:00Z"
    }
  ]
}
```

#### `PATCH /notifications/{id}/`
علامت‌گذاری به‌عنوان خوانده‌شده.

**Request:** `{ "is_read": true }` (ولی backend فعلی فقط `read_at` را در serializer برمی‌گرداند و `is_read` در `NotificationMarkReadSerializer` وجود دارد.)
**Response 200:** شیء Notification به‌روز شده.

#### `POST /notifications/mark-all-read/`
علامت‌گذاری همه به‌عنوان خوانده‌شده.

**Response 200:** `{ "marked_count": 3 }`

---

#### `GET /notifications/preferences/`
**Response 200:**
```json
{
  "in_app_enabled": true,
  "sms_enabled": false,
  "email_enabled": true
}
```

#### `PATCH /notifications/preferences/`
**Request:** هر زیرمجموعه‌ای از `{ "in_app_enabled": true, "sms_enabled": true, "email_enabled": false }`
**Response 200:** شیء به‌روز شده.

---

### ۳.۸ Compliance & Feature Flags

#### `GET /compliance/feature-flags/`
لیست Feature Flags.

**Response 200:**
```json
{
  "results": [
    { "key": "escrow_enabled", "description": "فعال‌سازی لایه ۲", "is_enabled": false, "is_system": false },
    { "key": "institutional_investor_api", "description": "فعال‌سازی API سرمایه‌گذار institutions", "is_enabled": false, "is_system": false }
  ]
}
```

#### `GET /compliance/feature-flags/{key}/`
**Response 200:** شیء `FeatureFlag`.

#### `PATCH /compliance/feature-flags/{key}/` (Admin only)
```json
{ "is_enabled": true }
```
**Response 200:** شیء `FeatureFlag` به‌روز شده.

---

#### `GET /compliance/stats/`
آمار داشبورد مدیریت.

**Response 200:**
```json
{
  "listings": {
    "total": 120,
    "published": 45,
    "pending_moderation": 8,
    "rejected": 20,
    "expired": 28,
    "matched": 19
  },
  "users": {
    "total": 150,
    "kyc_pending": 12,
    "kyc_approved": 80
  },
  "verifications": {
    "pending": 5
  },
  "notifications": {
    "unread": 20
  }
}
```

#### `GET /compliance/audit/`
لیست رویدادهای审计.

**Response 200:**
```json
{
  "results": [
    {
      "id": 1,
      "actor": 1,
      "actor_username": "admin",
      "event_type": "listing_published",
      "object_type": "cheque_listing",
      "object_id": "1",
      "metadata": {},
      "ip_address": "127.0.0.1",
      "created_at": "2025-04-25T09:00:00Z"
    }
  ]
}
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
| `match_created` | ابراز تمایل سرمایه‌گذار | CheckHolder | SMS + in-app |
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
