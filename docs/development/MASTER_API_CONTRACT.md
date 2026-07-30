# Master API Contract — Cheque Yar

**Purpose:** Single source of truth for backend API contract. Every endpoint, request/response shape, enum, and error code documented here is derived directly from `backend/doion/*/serializers.py`, `backend/doion/*/views.py`, `backend/config/api_router.py`, and `backend/config/exception_handler.py`.

**Stack:** Django 5.x + DRF + SimpleJWT ↔ Vue 3 + Naive UI + Pinia (TypeScript Strict)

**Base URL:** `/api/v1/`

**Auth:** Bearer JWT (`djangorestframework-simplejwt`). Access token lifetime: 1 hour. Refresh token lifetime: **1 day** (SimpleJWT default; `REFRESH_TOKEN_LIFETIME` is not overridden in settings).

**Date Format:** ISO 8601 (`"2025-04-25T09:00:00Z"`)

**IDs:** All primary keys are `number` (`BigAutoField`). There are no UUIDs in the current implementation.

**Legacy mount:** The same router is also mounted under `/api/` (alias of `/api/v1/`). Prefer `/api/v1/` for new clients.

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
13. [Pagination](#13-pagination)
14. [Rate Limiting](#14-rate-limiting)
15. [Operational Notes](#15-operational-notes)
16. [Legacy Endpoints](#16-legacy-endpoints)
17. [Role Values](#17-role-values)
18. [Changelog](#18-changelog)
19. [Sync Policy](#19-sync-policy)

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

### 1.2 Envelope Error Codes (emitted by `exception_handler`)

| Code | HTTP | When |
|------|------|------|
| `VALIDATION_ERROR` | 400 | DRF `ValidationError` (includes listing field validation) |
| `AUTHENTICATION_ERROR` | 401 | DRF `AuthenticationFailed` |
| `PERMISSION_ERROR` | 403 | DRF `PermissionDenied` (also returned manually by some views) |
| `NOT_FOUND_ERROR` | 404 | DRF `NotFound` |
| `SERVER_ERROR` | * | Fallback for other DRF `APIException` subclasses **including** match-domain exceptions |
| `MOD_306` | 400 | `ModerationResubmitLimitExceeded` |
| `MOD_500` | * | Base `ModerationError.default_code` (if raised without subclass) |

### 1.3 Listing validation (maps to `VALIDATION_ERROR`, not `LST_*`)

Listing create/update validators raise standard `ValidationError`. The API **does not** emit `LST_*` codes in the envelope `error.code`. Messages/fields in practice:

| Spec label (not emitted) | Field / detail | Actual message (approx.) |
|--------------------------|----------------|--------------------------|
| `LST_201` | `face_amount` | `face_amount must be greater than 0` |
| `LST_202` | `due_date` | `due_date must be in the future` |
| `LST_203` | `cheque_serial_number` | `sayad_number must be 16 digits` |
| `LST_204` | `cheque_serial_number` | Duplicate cheque for issuer/bank (IntegrityError → ValidationError) |
| `LST_205` | `non_field_errors` | `Daily limit of 10 listings reached` |
| `LST_206` | — | **spec-only / not implemented** — no cheque-image requirement enforced in serializer/views |

### 1.4 Moderation rejection codes (`MOD_101`–`MOD_106`)

These are **payload enum values** for `rejection_code` on listing moderation decisions — **not** envelope `error.code` values (except `MOD_306` above).

| Code | Meaning |
|------|---------|
| `MOD_101` | Incomplete information |
| `MOD_102` | Poor quality image |
| `MOD_103` | Invalid cheque |
| `MOD_104` | Duplicate listing |
| `MOD_105` | Risk too high |
| `MOD_106` | Other |

### 1.5 Match exception codes (declared but not emitted)

`MatchNotAllowed` (`MATCH_NOT_ALLOWED`) and `InvalidMatchStatus` (`INVALID_MATCH_STATUS`) exist on exceptions, but `custom_exception_handler` maps non-`ModerationError` `APIException`s to `SERVER_ERROR` with message `"An unexpected error occurred"`. Clients must treat match failures as `SERVER_ERROR` until the handler is fixed.

### 1.6 Spec-only codes (not in backend)

| Code family | Status |
|-------------|--------|
| `AUTH_001`–`AUTH_005` | **spec-only / not implemented** |
| `NOTIF_401`, `NOTIF_403` | **spec-only / not implemented** — notifications use standard envelope codes |
| `LST_*` as envelope codes | **spec-only / not implemented** — see §1.3 |

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

### 3.1 Get Current User

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
  "is_verified": false,
  "url": "http://example.com/api/v1/users/09121234567/"
}
```

Note: The `me` action is **GET-only**. Partial updates for the cookiecutter user route use `PATCH /api/v1/users/{username}/` (queryset is limited to the authenticated user). Prefer `PATCH /api/v1/identity/me/` for profile-style self-updates.

Also available: `GET /api/v1/users/` (list of self only), `GET|PUT|PATCH /api/v1/users/{username}/`.

---

### 3.2 Get / Update Profile

**Endpoint:** `GET /api/v1/identity/profile/`

**Endpoint:** `PUT|PATCH /api/v1/identity/profile/`

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
| `role` | `string` | Yes | Profile role (`read_only_fields`) |
| `bio` | `string` | No | Profile bio |
| `is_verified` | `boolean` | Yes | KYC verification status |
| `created_at` | `string` (ISO 8601) | Yes | |
| `updated_at` | `string` (ISO 8601) | Yes | |

**Request Body (partial):** `email`, `name`, `phone`, `bio` — **not** `role` / `is_verified`.

**Known runtime gap:** `ProfileViewSet.get_object` references `Profile` without importing it in `identity/api/views.py`, which can raise `NameError` on these routes until fixed.

Router also exposes detail stubs `GET|PUT|PATCH /api/v1/identity/profile/{pk}/` (same viewset).

---

### 3.3 Get / Update Current User (Identity)

**Endpoint:** `GET /api/v1/identity/me/`

**Endpoint:** `PUT|PATCH /api/v1/identity/me/`

**Permission:** IsAuthenticated

**Response 200:** `UserMeSerializer` — `{id, username, email, name, phone, role, is_verified}` (`role` / `is_verified` read-only). Writable: `email`, `name`, `phone`, `username` (model fields not marked read-only).

Router also exposes `GET|PUT|PATCH /api/v1/identity/me/{pk}/`.

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

**Permission:** `identity.IsModerator` — requires authenticated user whose **profile.role** is `moderator` or `admin`.

**Query Parameters:** Default list behavior (no custom pagination class on this view).

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
  "decision": "reject",
  "rejection_code": "KYC_101",
  "rejection_note": "تصویر کارت ملی ناخوانا است"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `decision` | `"approve" \| "reject"` | Yes | Decision |
| `rejection_code` | `string` | Conditional | Required if `decision === "reject"` (free-form string in current KYC view; not the listing `MOD_*` enum) |
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

**Permission:** IsAuthenticated (default). Scoped throttle `listing_create` = 10/day. Daily serializer cap of 10 listings/user/day also applies. `IsCheckHolder` is imported but **not** applied on this ViewSet; KYC-approved is **not** enforced in the view layer.

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

**Errors:** `VALIDATION_ERROR` (400) for face_amount / due_date / serial / daily limit / duplicate; `PERMISSION_ERROR` on illegal updates.

**Note:** Response create serializer returns create fields; list/retrieve use `ChequeListingSerializer` with nested field named `issuer_profile`. Model FK is `issuer` and the nested serializer currently has no `source="issuer"` — treat nested issuer as a known serialization gap until fixed.

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

Full CRUD via `IssuerProfileViewSet`. Permission: **IsAuthenticated** for all methods. There is **no ownership filter** — any authenticated user can list/create/update/delete any issuer profile.

### 7.1 List / Create Issuer Profiles

**Endpoint:** `GET /api/v1/issuer-profiles/`

**Endpoint:** `POST /api/v1/issuer-profiles/`

**Request Body (create):**

```json
{
  "national_or_company_id": "10100345678",
  "name": "شرکت آسان‌پرداخت"
}
```

**Response 200/201:**

```json
{
  "id": 1,
  "national_or_company_id": "10100345678",
  "name": "شرکت آسان‌پرداخت",
  "credit_score": null,
  "created_at": "2025-04-25T08:00:00Z",
  "updated_at": "2025-04-25T08:00:00Z"
}
```

---

### 7.2 Retrieve / Update / Delete Issuer Profile

**Endpoint:** `GET /api/v1/issuer-profiles/{id}/`

**Endpoint:** `PUT|PATCH /api/v1/issuer-profiles/{id}/`

**Endpoint:** `DELETE /api/v1/issuer-profiles/{id}/`

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

Note: Default DRF `PageNumberPagination` is used (page size fixed at **20**). Client `page_size` override is **not** enabled for marketplace. Cache key is `marketplace:listings:{page}` only (filter variance is not part of the cache key).

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

**Errors:** Match domain exceptions currently surface as envelope `SERVER_ERROR` (see §1.5), HTTP 400 from the exception `status_code` but with generic message.

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

### 9.10 Settlement Type Values

| Value | Description |
|-------|-------------|
| `off_platform` | Default — settlement occurs outside the platform |
| `escrow` | Future: escrow-based settlement (Layer 2) |
| `principal_ledger` | Future: internal ledger settlement (Layer 3) |

---

## 10. Moderation

### 10.1 Moderation Queue (Listings)

**Endpoint:** `GET /api/v1/moderation/queue/`

**Permission:** IsAuthenticated + `core.IsModerator` (`user.role == "moderator"` — note: does **not** treat `admin` the same way as compliance permissions).

**Query Parameters:** `page` (fixed page size 20; `page_size` query not enabled by default)

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
| `is_read` | `boolean` | Filter by read state (`true` / `false`) when supported by the view |
| `page` | `number` | Page number (fixed page size 20) |

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

**Permission:** IsModeratorOrAdmin (`user.role` in `moderator` \| `admin`)

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

Default list pagination uses DRF `PageNumberPagination` with fixed `PAGE_SIZE = 20`:

```json
{
  "count": 142,
  "next": "/api/v1/marketplace/listings/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

| Endpoint group | `page_size` query | Max |
|----------------|-------------------|-----|
| Most list endpoints | **Not supported** (fixed 20) | 20 |
| `GET /compliance/audit/` | Yes (`StandardResultPagination`) | 100 |

Exceptions (unpaginated array responses):
- `GET /listings/my/` — raw array
- `GET /marketplace/listings/latest/` — array of up to 4
- Some verification list views may return non-paginated arrays depending on queryset size / view config

Notifications list adds top-level `unread_count` alongside the pagination envelope.

---

## 14. Rate Limiting

Configured in `REST_FRAMEWORK["DEFAULT_THROTTLE_*"]`:

| Scope | Limit |
|-------|-------|
| Anonymous (`AnonRateThrottle`) | 100 requests/minute |
| Authenticated (`UserRateThrottle`) | 1000 requests/minute |
| Listing creation (`listing_create` scoped) | 10 requests/day per user |

Listing create also enforces a serializer-level daily cap of 10 listings per user (same calendar day).

---

## 15. Operational Notes

Behaviors that affect API responses or observed data without being separate endpoints:

| Behavior | Effect |
|----------|--------|
| **Marketplace list cache** | `GET /marketplace/listings/` cached 60s under key `marketplace:listings:{page}`. Invalidated when listing status changes to published/rejected/expired/withdrawn. |
| **Celery `expire_listings`** | Beat every 3600s. Sets `published` listings with `due_date < today` to `expired`. Clients may see status change without an API call. |
| **Correlation ID** | `CorrelationIDMiddleware` reads/sets `X-Correlation-ID` on every request/response (for logging). |
| **Feature flags (seeded)** | `matching_enabled`, `notifications_sms_enabled` (among others as seeded). |
| **Moderator permission inconsistency** | Listing moderation (`core.IsModerator`) checks `user.role == moderator`. KYC moderation (`identity.IsModerator`) checks profile role in `moderator` \| `admin`. Compliance uses `user.role` in `moderator` \| `admin`. |

---

## 16. Legacy Endpoints

| Path | Notes |
|------|-------|
| `/api/...` | Full alias of `/api/v1/...` (same `api_router`) |
| `POST /api/auth-token/` | DRF `obtain_auth_token` (non-JWT legacy token) |
| `/api/schema/`, `/api/docs/` | Legacy Spectacular schema/Swagger (also under `/api/v1/`) |
| Django template user pages (`/users/~redirect/`, etc.) | Not part of the REST JSON contract |

Prefer `/api/v1/` for all new client work.

---

## 17. Role Values

| Value | Description | Registerable via API? |
|-------|-------------|------------------------|
| `check_holder` | Can create and manage listings | Yes |
| `investor` | Can browse marketplace and create matches | Yes |
| `moderator` | Moderation queues | No — assign out-of-band |
| `admin` | Full platform access | No — assign out-of-band |

Model/profile store all four roles; `POST /identity/register/` only accepts `check_holder` \| `investor`.

---

## 18. Changelog

| Date | Change |
|------|--------|
| 2026-07-31 | Consolidated as sole API SSOT; aligned with live backend (error catalog, refresh TTL, pagination, issuer CRUD, permissions, operational notes, legacy mount); marked spec-only codes; deprecated `API_CONTRACT_REGISTRY.md` |
| 2026-07-29 | Phase 1 backend connectivity: role/phone on login/refresh; identity profile/me without pk; matches/my + status; feature-flag toggle |
| 2026-07-23 | Initial contract derived from backend code (Phases 0–8) |

---

## 19. Sync Policy

**This file (`docs/development/MASTER_API_CONTRACT.md`) is the only API contract SSOT.**

Any change to API-facing backend code **must** update this file in the **same PR**. Without documenting sync, the API change is incomplete.

Update when any of the following change:
- `backend/doion/*/serializers.py` — fields, read-only fields, response shapes
- `backend/doion/*/views.py` — endpoints, permissions, actions
- `backend/doion/*/urls.py` — URL patterns
- `backend/config/api_router.py` — router registrations
- `backend/config/exception_handler.py` — error envelope / code mapping
- `backend/doion/*/models.py` — model fields, choices, constraints that appear in the API
- JWT / pagination / throttling settings that affect clients

**Rules:**
1. Derive shapes and codes from code — never from memory, MVP specs, or the deprecated registry alone.
2. If a behavior is planned but not implemented, mark it **`spec-only / not implemented`** — do not document fictional runtime behavior.
3. Keep `frontend/src/types/api.d.ts` and clients aligned after contract edits.
4. Do not resurrect a parallel contract document; `API_CONTRACT_REGISTRY.md` is a deprecated stub only.

**PR checklist (API changes):**
- [ ] Endpoints / methods / permissions listed here match `show_urls` / router
- [ ] Request/response fields match serializers
- [ ] Error codes match `exception_handler` + raised exceptions
- [ ] Enums/choices match models
- [ ] Changelog row added with today's date
- [ ] Spec-only items explicitly labeled