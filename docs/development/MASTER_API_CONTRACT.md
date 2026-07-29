# Master API Contract — Cheque Yar

**Purpose:** Single source of truth for backend API contract. Every endpoint, request/response shape, enum, and error code documented here is derived directly from `backend/doion/*/serializers.py`, `backend/doion/*/views.py`, `backend/config/api_router.py`, and `backend/config/exception_handler.py`.

**Stack:** Django 5.x + DRF + SimpleJWT ↔ Vue 3 + Naive UI + Pinia (TypeScript Strict)

**Base URL:** `/api/v1/`

**Auth:** Bearer JWT (`djangorestframework-simplejwt`). Access token lifetime: 1 hour. Refresh token lifetime: 7 days.

**Date Format:** ISO 8601 (`"2025-04-25T09:00:00Z"`)

**IDs:** All primary keys are `number` (`BigAutoField`). There are no UUIDs in the current implementation.

---

## Table of Contents

1. [Error Envelope & Error Codes](#1-error-envelope--error-codes)
2. [Authentication](#2-authentication)
3. [Users & Identity](#3-users--identity)
4. [KYC / Verifications](#4-kyc--verifications)
5. [Documents](#5-documents)
6. [Cheque Listings](#6-cheque-listings)
7. [Issuer Profiles](#7-issuer-profiles)
8. [Marketplace & Search](#8-marketplace--search)
9. [Matches](#9-matches)
10. [Moderation](#10-moderation)
11. [Notifications](#11-notifications)
12. [Compliance & Admin](#12-compliance--admin)

---

## 1. Error Envelope & Error Codes

### 1.1 Error Envelope

All API errors follow this envelope format (implemented in `backend/config/exception_handler.py`):

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "face_amount": ["Must be greater than 0."]
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `code` | `string` | Machine-readable error code |
| `message` | `string` | Human-readable error message |
| `details` | `object \| undefined` | Optional field-level errors (only present for `VALIDATION_ERROR`) |

### 1.2 General Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `VALIDATION_ERROR` | 400 | Field validation failed |
| `AUTHENTICATION_ERROR` | 401 | Invalid or missing credentials |
| `PERMISSION_ERROR` | 403 | User lacks required permissions |
| `NOT_FOUND_ERROR` | 404 | Resource not found |
| `SERVER_ERROR` | 500 | Unexpected server error |

### 1.3 Listing Error Codes (`LST_*`)

| Code | Field | Description |
|------|-------|-------------|
| `LST_201` | `face_amount` | Must be greater than 0 |
| `LST_202` | `due_date` | Must be in the future |
| `LST_203` | `cheque_serial_number` | Must be exactly 16 digits |
| `LST_204` | `cheque_serial_number` | Duplicate cheque for this issuer/bank (unique constraint) |
| `LST_205` | — | Daily listing limit (10) reached |
| `LST_206` | — | At least one cheque image required (enforced at submission, not serializer) |

### 1.4 Moderation Error Codes (`MOD_*`)

| Code | Description |
|------|-------------|
| `MOD_101` | Incomplete information |
| `MOD_102` | Poor quality image |
| `MOD_103` | Invalid cheque |
| `MOD_104` | Duplicate listing |
| `MOD_105` | Risk too high |
| `MOD_106` | Other |
| `MOD_306` | Maximum resubmission limit exceeded (3 rejects) |

### 1.5 Notification Error Codes (`NOTIF_*`)

| Code | HTTP | Description |
|------|------|-------------|
| `NOTIF_401` | 401 | Authentication required |
| `NOTIF_403` | 403 | Permission denied |

---

## 2. Authentication

### 2.1 Login

**Endpoint:** `POST /api/v1/auth/login/`

**Permission:** AllowAny

**Request Body:**

```json
{
  "identifier": "09121234567",
  "password": "secure-pass"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `identifier` | `string` | Username, email, or phone number |
| `password` | `string` | User password |

**Response 200:**

```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci...",
  "user": {
    "id": 1,
    "username": "09121234567",
    "email": "user@example.com",
    "name": "رضا کریمی",
    "role": "check_holder",
    "phone": "+989123456789"
  }
}
```

**Errors:** `AUTHENTICATION_ERROR` (401)

---

### 2.2 Refresh Token

**Endpoint:** `POST /api/v1/auth/refresh/`

**Permission:** AllowAny

**Request Body:**

```json
{
  "refresh": "eyJhbGci..."
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
    "email": "user@example.com",
    "name": "رضا کریمی",
    "role": "check_holder",
    "phone": "+989123456789"
  }
}
```

**Errors:** `AUTHENTICATION_ERROR` (401)

---

### 2.3 Register

**Endpoint:** `POST /api/v1/identity/register/`

**Permission:** AllowAny

**Request Body:**

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

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | `string` | Yes | Unique username, max 150 chars |
| `email` | `string` | No | Valid email |
| `password` | `string` | Yes | Min 8 chars |
| `password_confirm` | `string` | Yes | Must match `password` |
| `name` | `string` | No | Full name |
| `phone` | `string` | No | Phone number |
| `role` | `"check_holder" \| "investor"` | Yes | User role |

**Response 201:**

```json
{
  "access": "eyJhbGci...",
  "refresh": "eyJhbGci...",
  "user": {
    "id": 1,
    "username": "09121234567",
    "email": "user@example.com",
    "name": "رضا کریمی",
    "role": "check_holder"
  }
}
```

**Errors:** `VALIDATION_ERROR` (400) — field-level details for duplicate username/phone, password mismatch

---

## 3. Users & Identity

### 3.1 Get / Update Current User

**Endpoint:** `GET /api/v1/users/me/`

**Permission:** IsAuthenticated

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

**Endpoint:** `PATCH /api/v1/users/me/`

**Request Body (partial):**

```json
{
  "name": "NAME_UPDATED",
  "email": "new@example.com",
  "phone": "+989198765432"
}
```

**Response 200:**

```json
{
  "id": 1,
  "username": "09121234567",
  "email": "new@example.com",
  "name": "NAME_UPDATED",
  "phone": "+989198765432",
  "role": "check_holder",
  "is_verified": false
}
```

---

### 3.2 Get / Update Profile

**Endpoint:** `GET /api/v1/identity/profile/`

**Permission:** IsAuthenticated

**Response 200:**

```json
{
  "id": 1,
  "username": "09121234567",
  "email": "user@example.com",
  "name": "رضا کریمی",
  "phone": "+989123456789",
  "role": "check_holder",
  "bio": "",
  "is_verified": false,
  "created_at": "2025-04-25T08:30:00Z",
  "updated_at": "2025-04-25T08:30:00Z"
}
```

| Field | Type | Read-Only | Description |
|-------|------|-----------|-------------|
| `id` | `number` | Yes | Profile ID |
| `username` | `string` | Yes | From `user.username` |
| `email` | `string` | No | Mapped to `user.email` |
| `name` | `string` | No | Mapped to `user.name` |
| `phone` | `string` | No | Mapped to `user.phone` |
| `role` | `string` | Yes | From `user.role` |
| `bio` | `string` | No | Profile bio |
| `is_verified` | `boolean` | Yes | KYC verification status |
| `created_at` | `string` (ISO 8601) | Yes | |
| `updated_at` | `string` (ISO 8601) | Yes | |

**Endpoint:** `PATCH /api/v1/identity/profile/`

**Request Body (partial):**

```json
{
  "bio": "Experienced investor",
  "role": "investor"
}
```

Note: `role` is writeable via ProfileSerializer (not read-only), but `is_verified` is read-only.

**Response 200:** Same shape as GET.

---

### 3.3 Get / Update Current User (Alt Endpoint)

**Endpoint:** `GET /api/v1/identity/me/`

**Permission:** IsAuthenticated

**Response 200:** Same shape as `GET /api/v1/users/me/` (returns `UserMeSerializer` data).

**Endpoint:** `PATCH /api/v1/identity/me/`

Updates `User` fields directly (not Profile fields). Response 200: same shape as GET.

---

## 4. KYC / Verifications

### 4.1 Create Verification

**Endpoint:** `POST /api/v1/verifications/`

**Permission:** IsAuthenticated

**Request Body (multipart/form-data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `full_name` | `string` | Yes | Full name |
| `national_id` | `string` | No | 10-digit national ID |
| `company_name` | `string` | No | Company name (optional) |
| `national_id_front` | `file` | Yes | Front of ID card |
| `national_id_back` | `file` | Yes | Back of ID card |
| `selfie` | `file` | No | Selfie image (optional) |

**Response 201:**

```json
{
  "id": 1,
  "full_name": "رضا کریمی",
  "national_id": "0012345678",
  "company_name": "شرکت آسان‌پرداخت",
  "status": "pending",
  "rejection_reason": "",
  "rejection_code": "",
  "documents": [
    {
      "id": 1,
      "document_type": "national_id_front",
      "file": "/media/documents/2025/04/25/abc.jpg",
      "file_size": 204800
    },
    {
      "id": 2,
      "document_type": "national_id_back",
      "file": "/media/documents/2025/04/25/def.jpg",
      "file_size": 192300
    }
  ]
}
```

---

### 4.2 List Verifications

**Endpoint:** `GET /api/v1/verifications/`

**Permission:** IsAuthenticated

**Behavior:** Returns all verifications for moderators/admins, or only the current user's verifications for regular users.

**Response 200:**

```json
[
  {
    "id": 1,
    "full_name": "رضا کریمی",
    "national_id": "0012345678",
    "company_name": "",
    "status": "pending",
    "rejection_reason": "",
    "rejection_code": "",
    "documents": []
  }
]
```

---

### 4.3 Retrieve Verification

**Endpoint:** `GET /api/v1/verifications/{id}/`

**Permission:** IsAuthenticated (owner or moderator/admin)

**Response 200:** Same shape as single verification object from list.

---

### 4.4 Update Verification

**Endpoint:** `PATCH /api/v1/verifications/{id}/`

**Permission:** IsAuthenticated (owner or moderator/admin)

**Request Body (partial):**

```json
{
  "full_name": "Name Updated",
  "national_id": "0012345678"
}
```

Note: Only `full_name`, `national_id`, and `company_name` are writable. `status`, `rejection_reason`, `rejection_code`, and `documents` are read-only.

**Response 200:** Updated verification object.

---

### 4.5 Get My Verification

**Endpoint:** `GET /api/v1/verifications/me/`

**Permission:** IsAuthenticated

**Behavior:** Returns the most recent verification for the current user, or 404 if none exists.

**Response 200:** Same shape as single verification object.

---

### 4.6 Moderation — KYC Queue

**Endpoint:** `GET /api/v1/moderation/kyc/`

**Permission:** IsModerator

**Query Parameters:** `ordering=-created_at`, `page`, `page_size`

**Response 200:**

```json
[
  {
    "id": 1,
    "full_name": "رضا کریمی",
    "national_id": "0012345678",
    "company_name": "شرکت آسان‌پرداخت",
    "status": "pending",
    "rejection_reason": "",
    "rejection_code": "",
    "documents": []
  }
]
```

---

### 4.7 Moderation — KYC Decision

**Endpoint:** `POST /api/v1/moderation/kyc/{id}/decision/`

**Permission:** IsModerator

**Request Body:**

```json
{
  "decision": "approve",
  "rejection_code": "KYC_101",
  "rejection_note": "تصویر کارت ملی ناخوانا است"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | `"approve" \| "reject"` | Yes | Decision |
| `rejection_code` | `string` | Conditional | Required if `decision === "reject"` |
| `rejection_note` | `string` | No | Explanation note |

**Response 200 (approve):**

```json
{ "status": "approved" }
```

**Response 200 (reject):**

```json
{ "status": "rejected" }
```

---

## 5. Documents

Documents are created as part of Verification creation or Listing document upload. There is no standalone Document CRUD API.

### 5.1 Upload Listing Document

**Endpoint:** `POST /api/v1/listings/{id}/documents/`

**Permission:** IsAuthenticated (listing owner only)

**Request Body (multipart/form-data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `document_type` | `string` | Yes | One of: `cheque_image`, `id_document`, `supplementary` |
| `file` | `file` | Yes | Binary file |

**Response 201:**

```json
{
  "id": 1,
  "document_type": "cheque_image",
  "file": "/media/documents/2025/04/25/cheque.jpg",
  "file_size": 204800
}
```

---

## 6. Cheque Listings

### 6.1 Create Listing

**Endpoint:** `POST /api/v1/listings/`

**Permission:** IsAuthenticated (check_holder with approved KYC)

**Request Body:**

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

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `issuer` | `number` | Yes | IssuerProfile ID |
| `bank_name` | `string` | Yes | Bank name, max 100 chars |
| `cheque_serial_number` | `string` | Yes | Exactly 16 digits |
| `face_amount` | `number` | Yes | Must be > 0 |
| `due_date` | `string` (date) | Yes | Must be in the future |
| `issuer_type` | `"legal" \| "natural"` | Yes | Issuer type |
| `issuer_name` | `string` | Yes | Issuer name, max 255 chars |
| `issuer_national_id` | `string` | Yes | Issuer national ID, max 20 chars |
| `description` | `string` | No | Optional description |

**Response 201:**

```json
{
  "id": 1,
  "owner_id": 1,
  "issuer_profile": {
    "id": 1,
    "national_or_company_id": "10100345678",
    "name": "شرکت آسان‌پرداخت",
    "credit_score": 78
  },
  "bank_name": "بانک ملت",
  "cheque_serial_number": "1402103568712345",
  "face_amount": "500000000",
  "due_date": "2025-06-10",
  "issuer_type": "legal",
  "issuer_name": "شرکت آسان‌پرداخت",
  "issuer_national_id": "10100345678",
  "description": "",
  "suggested_discount_rate": "3.80",
  "risk_tier": "low",
  "status": "pending_moderation",
  "rejection_reason": "",
  "rejection_code": "",
  "resubmit_count": 0,
  "created_at": "2025-04-25T09:00:00Z",
  "updated_at": "2025-04-25T09:00:00Z"
}
```

**Errors:** `LST_201`, `LST_202`, `LST_203`, `LST_204`, `LST_205`, `PERMISSION_ERROR`

---

### 6.2 List Listings

**Endpoint:** `GET /api/v1/listings/`

**Permission:** IsAuthenticated

**Behavior:**
- Moderators/admins: see all listings
- Check holders/investors: see only their own listings

**Response 200:** Array of `ChequeListing` objects (same shape as create response).

---

### 6.3 Get Listing Detail

**Endpoint:** `GET /api/v1/listings/{id}/`

**Permission:** IsAuthenticated

**Response 200:** Same shape as create response.

---

### 6.4 Update Listing

**Endpoint:** `PATCH /api/v1/listings/{id}/`

**Permission:** IsAuthenticated (owner only)

**Behavior:** Only allowed when status is `pending_moderation` or `rejected`.

**Request Body:** Any subset of create fields.

**Response 200:** Updated listing object.

---

### 6.5 My Listings

**Endpoint:** `GET /api/v1/listings/my/`

**Permission:** IsAuthenticated

**Behavior:** Returns all listings owned by the current user.

**Response 200:** Array of `ChequeListing` objects.

---

### 6.6 Upload Document

**Endpoint:** `POST /api/v1/listings/{id}/documents/`

**Permission:** IsAuthenticated (owner only)

**Request Body (multipart/form-data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `document_type` | `string` | Yes | One of: `cheque_image`, `id_document`, `supplementary` |
| `file` | `file` | Yes | Binary file |

**Response 201:**

```json
{
  "id": 1,
  "document_type": "cheque_image",
  "file": "/media/documents/2025/04/25/cheque.jpg",
  "file_size": 204800
}
```

---

### 6.7 Listing Status Values

| Value | Description |
|-------|-------------|
| `pending_moderation` | Awaiting moderator review |
| `published` | Active and visible in marketplace |
| `rejected` | Rejected by moderator |
| `matched` | Match accepted |
| `expired` | Past due date |
| `withdrawn` | Withdrawn by owner |
| `settled_off_platform` | Settlement confirmed off-platform |

---

## 7. Issuer Profiles

### 7.1 List Issuer Profiles

**Endpoint:** `GET /api/v1/issuer-profiles/`

**Permission:** IsAuthenticated

**Response 200:** Array of `IssuerProfile` objects.

---

### 7.2 Retrieve / Update Issuer Profile

**Endpoint:** `GET /api/v1/issuer-profiles/{id}/`

**Endpoint:** `PATCH /api/v1/issuer-profiles/{id}/`

**Permission:** IsAuthenticated (owner only for PATCH)

**Response 200:**

```json
{
  "id": 1,
  "national_or_company_id": "10100345678",
  "name": "شرکت آسان‌پرداخت",
  "credit_score": 78,
  "created_at": "2025-04-25T08:00:00Z",
  "updated_at": "2025-04-25T08:00:00Z"
}
```

| Field | Type | Read-Only | Description |
|-------|------|-----------|-------------|
| `id` | `number` | Yes | |
| `national_or_company_id` | `string` | No | National ID or company registration |
| `name` | `string` | No | Issuer name |
| `credit_score` | `number \| null` | Yes | Calculated credit score |
| `created_at` | `string` (ISO 8601) | Yes | |
| `updated_at` | `string` (ISO 8601) | Yes | |

---

## 8. Marketplace & Search

### 8.1 List Published Listings

**Endpoint:** `GET /api/v1/marketplace/listings/`

**Permission:** IsAuthenticated

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `risk_tier` | `string` | Filter by risk tier (`low`, `medium`, `high`) |
| `min_amount` | `number` | Minimum face amount (Rials) |
| `max_amount` | `number` | Maximum face amount (Rials) |
| `max_days_to_due` | `number` | Maximum days until due date |
| `issuer_type` | `string` | Filter by issuer type (`legal`, `natural`) |
| `bank_name` | `string` | Partial match on bank name (icontains) |
| `ordering` | `string` | Sort field: `created_at`, `-created_at`, `face_amount`, `-face_amount`, `suggested_discount_rate`, `-suggested_discount_rate`, `due_date`, `-due_date` |
| `page` | `number` | Page number (default: 1) |
| `page_size` | `number` | Results per page (default: 20, max: 50) |

**Response 200:**

```json
{
  "count": 142,
  "next": "/api/v1/marketplace/listings/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "owner_id": 1,
      "issuer_profile": {
        "id": 1,
        "national_or_company_id": "10100345678",
        "name": "شرکت آسان‌پرداخت",
        "credit_score": 78
      },
      "bank_name": "بانک ملت",
      "cheque_serial_number": "1402103568712345",
      "face_amount": "500000000",
      "due_date": "2025-06-10",
      "issuer_type": "legal",
      "issuer_name": "شرکت آسان‌پرداخت",
      "issuer_national_id": "10100345678",
      "description": "",
      "suggested_discount_rate": "3.80",
      "risk_tier": "low",
      "status": "published",
      "days_to_due": 45,
      "interest_count": 0,
      "published_at": "2025-04-25T09:00:00Z",
      "created_at": "2025-04-25T09:00:00Z",
      "updated_at": "2025-04-25T09:00:00Z"
    }
  ]
}
```

**Cache:** TTL 60s on list responses. Invalidated on status change.

---

### 8.2 Latest Listings (Public)

**Endpoint:** `GET /api/v1/marketplace/listings/latest/`

**Permission:** AllowAny

**Behavior:** Returns the 4 most recent published listings.

**Response 200:**

```json
[
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
    "created_at": "2025-04-25T09:00:00Z"
  }
]
```

---

## 9. Matches

### 9.1 Create Match (Express Interest)

**Endpoint:** `POST /api/v1/matches/`

**Permission:** IsAuthenticated (investor only)

**Request Body:**

```json
{
  "listing_id": 1,
  "message": "I am interested in this cheque"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `listing_id` | `number` | Yes | ChequeListing ID |
| `message` | `string` | No | Optional message to check holder |

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
  "message": "I am interested in this cheque",
  "created_at": "2025-04-25T10:00:00Z",
  "updated_at": "2025-04-25T10:00:00Z"
}
```

**Errors:** `MatchNotAllowed` (400) — if listing not found, user is not investor, or investor already expressed interest.

---

### 9.2 List Matches

**Endpoint:** `GET /api/v1/matches/`

**Permission:** IsAuthenticated

**Behavior:**
- Investors: see matches where they are the investor
- Check holders: see matches where they are the check holder

**Response 200:** Paginated array of `Match` objects (same shape as create response).

---

### 9.3 Accept Match

**Endpoint:** `POST /api/v1/matches/{id}/accept/`

**Permission:** IsAuthenticated (check_holder only)

**Response 200:** Updated `Match` object with `status: "accepted"`.

---

### 9.4 Decline Match

**Endpoint:** `POST /api/v1/matches/{id}/decline/`

**Permission:** IsAuthenticated (check_holder only)

**Request Body:**

```json
{
  "note": "The terms are not acceptable"
}
```

**Response 200:** Updated `Match` object with `status: "declined"`.

---

### 9.5 Cancel Match

**Endpoint:** `POST /api/v1/matches/{id}/cancel/`

**Permission:** IsAuthenticated

**Behavior:** Either party can cancel an accepted match.

**Response 200:** Updated `Match` object with `status: "cancelled"`.

---

### 9.6 Confirm Off-Platform Settlement

**Endpoint:** `POST /api/v1/matches/{id}/confirm-off-platform/`

**Permission:** IsAuthenticated (check_holder only)

**Response 200:** Updated `Match` object with `status: "off_platform_confirmed"`.

---

### 9.7 List My Matches

**Endpoint:** `GET /api/v1/matches/my/`

**Permission:** IsAuthenticated

**Behavior:**
- Investors: see matches where they are the investor
- Check holders: see matches where they are the check holder

**Response 200:** Paginated array of `Match` objects (same shape as create response).

---

### 9.8 Update Match Status

**Endpoint:** `PATCH /api/v1/matches/{id}/status/`

**Permission:** IsAuthenticated

**Request Body:**

```json
{
  "status": "accepted",
  "final_discount_rate": "2.7",
  "terms": "Updated terms"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | `MatchStatus` | Yes | New match status |
| `final_discount_rate` | `string \| null` | No | Final discount rate |
| `terms` | `string` | No | Updated terms |

**Response 200:** Updated `Match` object.

---

### 9.9 Match Status Values

| Value | Description |
|-------|-------------|
| `pending` | Interest expressed, awaiting holder response |
| `accepted` | Holder accepted the match |
| `declined` | Holder declined the match |
| `cancelled` | Match cancelled by either party |
| `off_platform_confirmed` | Settlement confirmed outside platform |
| `settled` | Match fully settled |

---

### 9.9 Match Status Values

| Value | Description |
|-------|-------------|
| `off_platform` | Default — settlement occurs outside the platform |
| `escrow` | Future: escrow-based settlement (Layer 2) |
| `principal_ledger` | Future: internal ledger settlement (Layer 3) |

---

## 10. Moderation

### 10.1 Moderation Queue (Listings)

**Endpoint:** `GET /api/v1/moderation/queue/`

**Permission:** IsAuthenticated (moderator/admin only)

**Query Parameters:** `ordering=-created_at`, `page`, `page_size`

**Response 200:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "owner_id": 1,
      "issuer_profile": {
        "id": 1,
        "national_or_company_id": "1234567890",
        "name": "شرکت فناوری نوین",
        "credit_score": 750
      },
      "bank_name": "بانک ملت",
      "cheque_serial_number": "1234567890123456",
      "face_amount": "500000000",
      "due_date": "2026-12-31",
      "issuer_type": "legal",
      "issuer_name": "شرکت فناوری نوین",
      "issuer_national_id": "1234567890",
      "description": "توضیحات تکمیلی",
      "suggested_discount_rate": "3.80",
      "risk_tier": "low",
      "status": "pending_moderation",
      "rejection_reason": "",
      "rejection_code": null,
      "resubmit_count": 0,
      "created_at": "2026-06-28T10:00:00Z",
      "updated_at": "2026-06-28T10:00:00Z"
    }
  ]
}
```

---

### 10.2 Moderation Decision (Listings)

**Endpoint:** `POST /api/v1/moderation/{id}/decision/`

**Permission:** IsAuthenticated (moderator/admin only)

**Request Body:**

```json
{
  "decision": "approve",
  "rejection_code": "MOD_102",
  "rejection_note": "تصویر چک ناخوانا است"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | `"approve" \| "reject"` | Yes | Decision |
| `rejection_code` | `string` | Conditional | Required if `decision === "reject"`. Must be one of `MOD_101`..`MOD_106`. |
| `rejection_note` | `string` | No | Explanation note |

**Response 201:**

```json
{
  "id": 1,
  "listing": 1,
  "moderator": 5,
  "decision": "approved",
  "rejection_code": null,
  "rejection_code_display": null,
  "rejection_note": "",
  "created_at": "2026-06-28T11:00:00Z"
}
```

**Response 201 (rejected):**

```json
{
  "id": 2,
  "listing": 1,
  "moderator": 5,
  "decision": "rejected",
  "rejection_code": "MOD_102",
  "rejection_code_display": "Poor quality image",
  "rejection_note": "تصویر چک ناخوانا است",
  "created_at": "2026-06-28T11:00:00Z"
}
```

---

### 10.3 Resubmit Rejected Listing

**Endpoint:** `POST /api/v1/moderation/{id}/resubmit/`

**Permission:** IsAuthenticated (owner only)

**Behavior:** Changes listing status from `rejected` back to `pending_moderation`. Only allowed if `resubmit_count < 3`.

**Response 200:** Updated listing object with `status: "pending_moderation"`.

**Errors:** `MOD_306` (400) — maximum resubmission limit exceeded.

---

## 11. Notifications

### 11.1 List Notifications

**Endpoint:** `GET /api/v1/notifications/`

**Permission:** IsAuthenticated

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `type` | `string` | Filter by notification type |
| `status` | `string` | Filter by status (`pending`, `sent`, `read`, `failed`) |
| `page` | `number` | Page number |
| `page_size` | `number` | Results per page |

**Response 200:**

```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "unread_count": 3,
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

---

### 11.2 Mark Notification as Read

**Endpoint:** `PATCH /api/v1/notifications/{id}/`

**Permission:** IsAuthenticated

**Request Body:**

```json
{
  "is_read": true
}
```

**Response 200:** Updated notification object (status changed to `read`, `read_at` set).

---

### 11.3 Mark All Notifications as Read

**Endpoint:** `POST /api/v1/notifications/mark-all-read/`

**Permission:** IsAuthenticated

**Response 200:**

```json
{
  "message": "3 notifications marked as read"
}
```

---

### 11.4 Get Notification Preferences

**Endpoint:** `GET /api/v1/notifications/preferences/`

**Permission:** IsAuthenticated

**Response 200:**

```json
{
  "in_app_enabled": true,
  "sms_enabled": false,
  "email_enabled": true
}
```

---

### 11.5 Update Notification Preferences

**Endpoint:** `PATCH /api/v1/notifications/preferences/`

**Permission:** IsAuthenticated

**Request Body (partial):**

```json
{
  "sms_enabled": true,
  "email_enabled": false
}
```

**Response 200:** Updated preferences object.

---

### 11.6 Notification Types

| Value | Description |
|-------|-------------|
| `match_created` | New match created |
| `match_accepted` | Match accepted |
| `match_declined` | Match declined |
| `match_cancelled` | Match cancelled |
| `settlement_confirmed` | Settlement confirmed |
| `listing_published` | Listing published |
| `listing_rejected` | Listing rejected |
| `listing_expired` | Listing expired |
| `kyc_approved` | KYC approved |
| `kyc_rejected` | KYC rejected |
| `new_moderation_item` | New moderation item |

---

## 12. Compliance & Admin

### 12.1 List Feature Flags

**Endpoint:** `GET /api/v1/compliance/feature-flags/`

**Permission:** IsAuthenticated (moderator/admin only)

**Response 200:**

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "key": "matching_enabled",
      "description": "Enable investor express-interest / matching flow",
      "is_enabled": true,
      "is_system": false
    }
  ]
}
```

---

### 12.2 Retrieve Feature Flag

**Endpoint:** `GET /api/v1/compliance/feature-flags/{key}/`

**Permission:** IsAuthenticated (moderator/admin only)

**Response 200:** Single `FeatureFlag` object.

---

### 12.3 Update Feature Flag

**Endpoint:** `PATCH /api/v1/compliance/feature-flags/{key}/`

**Permission:** IsAuthenticated (admin only)

**Request Body:**

```json
{
  "is_enabled": true
}
```

**Response 200:** Updated `FeatureFlag` object.

**Errors:** `PERMISSION_ERROR` (403) — system flags cannot be modified.

---

### 12.4 Toggle Feature Flag

**Endpoint:** `POST /api/v1/compliance/feature-flags/{key}/toggle/`

**Permission:** IsAuthenticated (moderator/admin only)

**Behavior:** Toggles `is_enabled` on the feature flag identified by `key`.

**Response 200:** Updated `FeatureFlag` object.

**Errors:** `PERMISSION_ERROR` (403) — system flags cannot be toggled.

---

### 12.5 Admin Stats

**Endpoint:** `GET /api/v1/compliance/stats/`

**Permission:** IsAuthenticated (moderator/admin only)

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

---

### 12.6 Audit Events

**Endpoint:** `GET /api/v1/compliance/audit/`

**Permission:** IsAuthenticated (moderator/admin only)

**Query Parameters:** `page`, `page_size`

**Response 200:**

```json
{
  "count": 10,
  "next": null,
  "previous": null,
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

## 13. Pagination

All list endpoints support DRF standard pagination:

```json
{
  "count": 142,
  "next": "/api/v1/marketplace/listings/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

**Default page size:** 20
**Max page size:** 50 (for marketplace), 100 (for compliance)

---

## 14. Rate Limiting

| Scope | Limit |
|-------|-------|
| Anonymous | 100 requests/minute |
| Authenticated | 1000 requests/minute |
| Listing creation | 10 requests/day per user |

---

## 15. Changelog

| Date | Change |
|------|--------|
| 2026-07-29 | Phase 1 backend connectivity: added role/phone to login/refresh responses; exposed identity/profile/ and identity/me/ without pk; fixed ProfileSerializer.update field separation; added matches/my/ and matches/{id}/status/ endpoints; added feature flag toggle endpoint |
| 2026-07-23 | Initial contract derived from actual backend code (Phases 0-8) |

---

## 16. Sync Policy

**This file must be updated whenever any of the following change:**
- `backend/doion/*/serializers.py` — fields, read-only fields, response shapes
- `backend/doion/*/views.py` — endpoints, permissions, actions
- `backend/doion/*/urls.py` — URL patterns
- `backend/config/api_router.py` — router registrations
- `backend/config/exception_handler.py` — error envelope format
- `backend/doion/*/models.py` — model fields, choices, constraints

**Do not update this file from memory or from design docs alone. Always sync from the actual backend code.**
