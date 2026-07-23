# API Contract Registry

This document tracks all API endpoints and error envelope format for the Cheque Marketplace backend.

## Error Envelope Format

All API errors follow a consistent envelope format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { /* optional, field-level errors */ }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Field validation failed |
| `AUTHENTICATION_ERROR` | 401 | Authentication credentials invalid or missing |
| `PERMISSION_ERROR` | 403 | User lacks required permissions |
| `NOT_FOUND_ERROR` | 404 | Requested resource not found |
| `SERVER_ERROR` | 500 | Unexpected server error |

### Listing-Specific Error Codes

| Code | HTTP Status | Field/Detail | Description |
|------|-------------|--------------|-------------|
| `LST_201` | 400 | `face_amount` | Face amount must be greater than zero |
| `LST_202` | 400 | `due_date` | Due date must be in the future |
| `LST_203` | 400 | `cheque_serial_number` | Sayad number must be exactly 16 digits |
| `LST_204` | 400 | `cheque_serial_number` | Duplicate cheque for this issuer/bank (unique constraint) |
| `LST_205` | 400 | `non_field_errors` | Daily limit of 10 listings reached |
| `LST_206` | 400 | `documents` | At least one cheque image is required |

### Moderation-Specific Error Codes

| Code | HTTP Status | Field/Detail | Description |
|------|-------------|--------------|-------------|
| `MOD_101` | — | `rejection_code` | Incomplete information |
| `MOD_102` | — | `rejection_code` | Poor quality image |
| `MOD_103` | — | `rejection_code` | Invalid cheque |
| `MOD_104` | — | `rejection_code` | Duplicate listing |
| `MOD_105` | — | `rejection_code` | Risk too high |
| `MOD_106` | — | `rejection_code` | Other |
| `MOD_306` | 400 | `non_field_errors` | Maximum resubmission limit exceeded (3 rejects) |

---

## Phase-0 Endpoints

### Authentication

#### POST /api/v1/auth/login/

Authenticate user and return JWT tokens.

**Request Body:**
```json
{
  "identifier": "username_or_email_or_phone",
  "password": "user_password"
}
```

**Response (200):**
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "phone": "09123456789",
    "role": "check_holder"
  }
}
```

#### POST /api/v1/auth/refresh/

Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh": "jwt_refresh_token"
}
```

**Response (200):**
```json
{
  "access": "new_jwt_access_token"
}
```

### Users

#### GET /api/v1/users/me/

Get current authenticated user's profile.

**Response (200):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "phone": "09123456789",
  "role": "check_holder",
  "is_verified": false
}
```

#### PATCH /api/v1/users/me/

Update current user's profile.

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "john.new@example.com",
  "phone": "09129876543"
}
```

**Response (200):** Same as GET /users/me/

---

## Phase-1 Endpoints

### Identity

#### POST /api/v1/identity/register/

Register a new user with role selection.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "phone": "09123456789",
  "role": "check_holder",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**Constraints:**
- `username`: required, unique, max 150 chars
- `email`: optional
- `phone`: optional, unique, max 20 chars
- `role`: required, one of `check_holder` | `investor` | `moderator` | `admin`
- `password`: required, min 8 chars
- `password_confirm`: must match `password`

**Response (201):**
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "role": "check_holder"
  }
}
```

**Error Response (400):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Registration failed",
    "details": {
      "username": ["This username is already taken."],
      "phone": ["This phone number is already registered."],
      "password_confirm": ["Passwords do not match."]
    }
  }
}
```

#### GET /api/v1/identity/me/

Get current user's profile (alias of /users/me/).

**Response (200):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "phone": "09123456789",
  "role": "check_holder",
  "is_verified": false
}
```

#### PATCH /api/v1/identity/me/

Update current user's profile.

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "john.new@example.com",
  "phone": "09129876543"
}
```

**Response (200):** Same as GET /identity/me/

#### GET /api/v1/identity/profile/

Get detailed profile with bio and verification status.

**Response (200):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "phone": "09123456789",
  "role": "check_holder",
  "bio": "",
  "is_verified": false,
  "created_at": "2026-06-24T14:30:00Z",
  "updated_at": "2026-06-24T14:30:00Z"
}
```

#### PATCH /api/v1/identity/profile/

Update detailed profile.

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "john.new@example.com",
  "phone": "09129876543",
  "bio": "Experienced investor"
}
```

**Note:** `role` and `is_verified` are read-only via this endpoint.

**Response (200):** Same as GET /identity/profile/

---

## Phase-2 Endpoints

### KYC/Verifications

#### POST /api/v1/verifications/
Start KYC verification process.

**Request (multipart/form-data):**
```json
{
  "full_name": "رضا کریمی",
  "national_id": "0012345678",
  "company_name": "شرکتExample"
}
```
With files: `national_id_front`, `national_id_back` (required), `selfie` (optional).

**Response 201:**
```json
{
  "id": 1,
  "full_name": "رضا کریمی",
  "national_id": "0012345678",
  "company_name": "شرکتExample",
  "status": "pending",
  "documents": [
    { "id": 1, "document_type": "national_id_front", "file": "/media/documents/...", "file_size": 102400 }
  ]
}
```

**Errors:** `VALIDATION_ERROR` if fields missing or files invalid.

#### GET /api/v1/verifications/me/
Get current user's latest verification.

**Response 200:**
```json
{
  "id": 1,
  "full_name": "رضا کریمی",
  "national_id": "0012345678",
  "company_name": "شرکتExample",
  "status": "approved",
  "rejection_reason": null,
  "rejection_code": null,
  "documents": []
}
```

**Errors:** `404` if no verification exists.

### Moderation — KYC Queue

#### GET /api/v1/moderation/kyc/
List pending KYC verifications (Moderator/Admin only).

**Response 200:**
```json
{
  "results": [
    {
      "id": 1,
      "full_name": "رضا کریمی",
      "national_id": "0012345678",
      "company_name": "شرکتExample",
      "status": "pending",
      "documents": [...],
      "created_at": "2026-06-28T10:00:00Z"
    }
  ]
}
```

#### POST /api/v1/moderation/kyc/{id}/decision/
Approve or reject a KYC verification.

**Request:**
```json
{
  "decision": "approve"  // or "reject"
}
```

**Response 200 (approve):**
```json
{ "status": "approved" }
```

**Response 200 (reject):**
```json
{ "status": "rejected" }
```

**Error:** `400` if `decision` is missing or invalid. `403` if user is not moderator/admin.

---

## Phase-3 Endpoints

### Listings

#### POST /api/v1/listings/

Create a new cheque listing. Requires KYC_APPROVED status.

**Request Body:**
```json
{
  "issuer": 1,
  "bank_name": "بانک ملت",
  "cheque_serial_number": "1234567890123456",
  "face_amount": 500000000,
  "due_date": "2026-12-31",
  "issuer_type": "legal",
  "issuer_name": "شرکت فناوری نوین",
  "issuer_national_id": "1234567890",
  "description": "توضیحات تکمیلی"
}
```

**Response (201):**
```json
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
  "face_amount": 500000000,
  "due_date": "2026-12-31",
  "issuer_type": "legal",
  "issuer_name": "شرکت فناوری نوین",
  "issuer_national_id": "1234567890",
  "description": "توضیحات تکمیلی",
  "suggested_discount_rate": 6.0,
  "risk_tier": "medium",
  "status": "pending_moderation",
  "created_at": "2026-06-28T10:00:00Z",
  "updated_at": "2026-06-28T10:00:00Z"
}
```

**Validation Rules:**
- `face_amount`: required, must be > 0 (LST_201)
- `due_date`: required, must be in the future (LST_202)
- `cheque_serial_number`: required, exactly 16 digits, numeric (LST_203)
- `issuer`: required, must be a valid IssuerProfile ID
- `bank_name`: required, max 100 chars
- `issuer_type`: required, one of `legal` | `natural`
- `issuer_name`: required, max 255 chars
- `issuer_national_id`: required, max 20 chars
- Daily limit: max 10 listings per user per day (LST_205)

**Errors:**
- `VALIDATION_ERROR` with field-level details for LST_201–LST_205
- `VALIDATION_ERROR` with `cheque_serial_number` detail for duplicate (LST_204)

#### PATCH /api/v1/listings/{id}/

Update an existing listing. Only allowed when status is `pending_moderation` or `rejected`, and only by the listing owner.

**Request Body:** Same fields as POST (all optional for PATCH)

**Response (200):** Updated listing object (same shape as POST response)

**Errors:**
- `PERMISSION_ERROR` if listing is not in editable status
- `PERMISSION_ERROR` if user is not the owner

#### GET /api/v1/listings/my/

List current user's listings.

**Response (200):**
```json
{
  "results": [
    {
      "id": 1,
      "owner_id": 1,
      "issuer_profile": { ... },
      "bank_name": "بانک ملت",
      "cheque_serial_number": "1234567890123456",
      "face_amount": 500000000,
      "due_date": "2026-12-31",
      "issuer_type": "legal",
      "issuer_name": "شرکت فناوری نوین",
      "issuer_national_id": "1234567890",
      "description": "توضیحات",
      "suggested_discount_rate": 6.0,
      "risk_tier": "medium",
      "status": "pending_moderation",
      "created_at": "2026-06-28T10:00:00Z",
      "updated_at": "2026-06-28T10:00:00Z"
    }
  ]
}
```

#### GET /api/v1/listings/{id}/

Get listing detail. Available to owner or public (depending on status).

**Response (200):** Same shape as POST response

**Errors:**
- `NOT_FOUND_ERROR` if listing does not exist
- `PERMISSION_ERROR` if user cannot access this listing

#### POST /api/v1/listings/{id}/documents/

Upload a document for a listing. Only the owner can upload.

**Request (multipart/form-data):**
- `file`: binary file (image/pdf)
- `document_type`: string (e.g. `cheque_image`, `id_document`, `supplementary`)

**Response (201):**
```json
{
  "id": 1,
  "document_type": "cheque_image",
  "file": "/media/documents/2026/06/28/cheque.jpg",
  "file_size": 102400
}
```

**Errors:**
- `PERMISSION_ERROR` if user is not the owner
- `LST_206` if no cheque image uploaded (validated at submission time)

---

## Phase-4 Endpoints

### Moderation — Listing Queue

#### GET /api/v1/moderation/queue/

List all listings with `pending_moderation` status (Moderator/Admin only). Supports pagination.

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
        "national_or_company_id": "1234767890",
        "name": "شرکت فناوری نوین",
        "credit_score": 750
      },
      "bank_name": "بانک ملت",
      "cheque_serial_number": "1234567890123456",
      "face_amount": 500000000,
      "due_date": "2026-12-31",
      "issuer_type": "legal",
      "issuer_name": "شرکت فناوری نوین",
      "issuer_national_id": "1234567890",
      "description": "توضیحات تکمیلی",
      "suggested_discount_rate": 6.0,
      "risk_tier": "medium",
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

**Errors:**
- `401` if not authenticated
- `403` if user is not moderator or admin

#### POST /api/v1/moderation/{id}/decision/

Approve or reject a listing (Moderator/Admin only).

**Request (approve):**
```json
{
  "decision": "approve"
}
```

**Request (reject):**
```json
{
  "decision": "reject",
  "rejection_code": "MOD_101",
  "rejection_note": "اطلاعات ناقص است"
}
```

**Response 201 (approve):**
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

**Response 201 (reject):**
```json
{
  "id": 2,
  "listing": 1,
  "moderator": 5,
  "decision": "rejected",
  "rejection_code": "MOD_101",
  "rejection_code_display": "Incomplete information",
  "rejection_note": "اطلاعات ناقص است",
  "created_at": "2026-06-28T11:00:00Z"
}
```

**Errors:**
- `401` if not authenticated
- `403` if user is not moderator or admin
- `400` `VALIDATION_ERROR` if `rejection_code` is missing on reject
- `400` `MOD_306` if listing has been rejected 3 times already (max resubmission limit exceeded)

---

## Phase-5 Endpoints

### Marketplace — Published Listings

#### GET /api/v1/marketplace/listings/

List all `published` cheque listings for investor browsing. Supports pagination (page_size=20, max=50), filtering, and ordering. Read-only.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `page` | int | Page number (default: 1) |
| `page_size` | int | Results per page (default: 20, max: 50) |
| `risk_tier` | string | Filter by risk tier: `low`, `medium`, `high` |
| `min_amount` | number | Minimum face amount (ریال) |
| `max_amount` | number | Maximum face amount (ریال) |
| `max_days_to_due` | number | Maximum days until due date |
| `issuer_type` | string | Filter by issuer type: `legal`, `natural` |
| `bank_name` | string | Partial match on bank name (icontains) |
| `search` | string | Search by bank name |
| `ordering` | string | Sort field: `created_at`, `-created_at`, `face_amount`, `-face_amount`, `suggested_discount_rate`, `-suggested_discount_rate`, `due_date`, `-due_date` |

**Response 200:**
```json
{
  "count": 24,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "owner_id": 1,
      "issuer_profile": {
        "id": 1,
        "national_or_company_id": "1234767890",
        "name": "شرکت فناوری نوین",
        "credit_score": 750
      },
      "bank_name": "بانک ملت",
      "cheque_serial_number": "1111222233334444",
      "face_amount": 500000000,
      "due_date": "2026-12-31",
      "issuer_type": "legal",
      "issuer_name": "شرکت فناوری نوین",
      "issuer_national_id": "1234567890",
      "description": "",
      "suggested_discount_rate": 3.5,
      "risk_tier": "low",
      "status": "published",
      "days_to_due": 60,
      "interest_count": 0,
      "published_at": "2026-06-28T10:00:00Z",
      "created_at": "2026-06-28T10:00:00Z",
      "updated_at": "2026-06-28T10:00:00Z"
    }
  ]
}
```

**Errors:**
- `401` if not authenticated
- `404` if endpoint does not exist (mounted under `/api/v1/marketplace/`)

**Cache:**
- TTL 60s on list responses
- Invalidated on `ChequeListing` status change to `published`, `rejected`, `expired`, or `withdrawn`

---

## Phase-7 Endpoints

### Notifications

#### `GET /api/v1/notifications/`

List user's notifications with pagination and filtering.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `type` | string | Filter by notification type: `match_created`, `match_accepted`, `match_declined`, `match_cancelled`, `settlement_confirmed`, `listing_published`, `listing_rejected`, `listing_expired`, `kyc_approved`, `kyc_rejected`, `new_moderation_item` |
| `is_read` | boolean | Filter by read status: `true` or `false` |
| `page` | int | Page number (default: 1) |
| `page_size` | int | Results per page (default: 20) |

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
      "status": "pending",
      "title": "درخواست خرید جدید",
      "message": "یک سرمایه‌گذار به آگهی چک شما علاقه‌مند شده است",
      "related_object_type": "cheque_listing",
      "related_object_id": "1",
      "read_at": null,
      "sent_at": "2025-04-25T14:00:00Z",
      "created_at": "2025-04-25T14:00:00Z"
    }
  ]
}
```

**Errors:**
- `NOTIF_401` - Authentication required (401)
- `NOTIF_403` - Permission denied (403)

---

#### `PATCH /api/v1/notifications/{id}/`

Mark a notification as read.

**Request Body:**
```json
{
  "is_read": true
}
```

**Response 200:**
```json
{
  "id": 1,
  "type": "match_created",
  "channel": "in_app",
  "status": "read",
  "title": "...",
  "message": "...",
  "related_object_type": "cheque_listing",
  "related_object_id": "1",
  "read_at": "2025-04-25T15:00:00Z",
  "sent_at": "2025-04-25T14:00:00Z",
  "created_at": "2025-04-25T14:00:00Z"
}
```

---

#### `POST /api/v1/notifications/mark-all-read/`

Mark all user notifications as read.

**Response 200:**
```json
{
  "message": "3 notifications marked as read"
}
```

---

#### `GET /api/v1/notifications/preferences/`

Get user notification preferences.

**Response 200:**
```json
{
  "in_app_enabled": true,
  "sms_enabled": false,
  "email_enabled": true
}
```

---

#### `PATCH /api/v1/notifications/preferences/`

Update user notification preferences.

**Request Body:**
```json
{
  "in_app_enabled": true,
  "sms_enabled": true,
  "email_enabled": true
}
```

**Response 200:**
```json
{
  "in_app_enabled": true,
  "sms_enabled": true,
  "email_enabled": true
}
```

**Errors:**
- `NOTIF_403` - Preference mismatch or invalid field

---

## Role Values

| Value | Label (FA) | Label (EN) | Description |
|-------|------------|------------|-------------|
| `check_holder` | دارنده چک | Check Holder | Can create and list cheques |
| `investor` | سرمایه‌گذار | Investor | Can browse and express interest |
| `moderator` | مدیر | Moderator | Can moderate listings and KYC |
| `admin` | مدیر کل | Admin | Full platform access |

---

## Phase 8 — Compliance, Jobs & Hardening

All compliance endpoints require `Moderator` or `Admin` role (permission `IsModeratorOrAdmin`).

### Feature Flags

**List feature flags**
`GET /api/v1/compliance/feature-flags/`

**Response 200:**
```json
{
  "count": 2,
  "results": [
    { "key": "matching_enabled", "description": "Enable investor express-interest / matching flow", "is_enabled": true, "is_system": false }
  ]
}
```

**Retrieve a flag**
`GET /api/v1/compliance/feature-flags/{key}/`

**Update a flag**
`PATCH /api/v1/compliance/feature-flags/{key}/`
```json
{ "is_enabled": true }
```

**Errors:**
- `PERMISSION_ERROR` (403) — Normal users cannot read/modify flags.
- `PERMISSION_ERROR` (403) — System flags (`is_system: true`) cannot be modified via API.

### Admin Stats

**Get aggregate dashboard stats**
`GET /api/v1/compliance/stats/`

**Response 200:**
```json
{
  "listings": {
    "total": 0, "published": 0, "pending_moderation": 0,
    "rejected": 0, "expired": 0, "matched": 0
  },
  "users": { "total": 0, "kyc_pending": 0, "kyc_approved": 0 },
  "verifications": { "pending": 0 },
  "notifications": { "unread": 0 }
}
```

### Audit Events

**List recent audit events (paginated)**
`GET /api/v1/compliance/audit/`

### Celery Jobs

- `expire_listings` (registered `shared_task`) — runs every 60 minutes via Celery Beat
  (`CELERY_BEAT_SCHEDULE["expire-listings-every-hour"]`). Marks `PUBLISHED` listings whose
  `due_date` is in the past as `EXPIRED`.
- Correlation ID middleware (`X-Correlation-ID`) attaches a per-request correlation id used in
  structured logging (structlog, when installed).

### Rate Limiting

DRF throttling is enabled globally:
- Anon: `100/minute`
- Authenticated user: `1000/minute`
- Listing creation (`listing_create` scope): `10/day` per user

### Error Code Catalog (from `mvp-spec.md` §2)

| Code | HTTP | Category | Description |
|------|------|----------|-------------|
| `AUTH_001` | 400 | Auth | Invalid verification code |
| `AUTH_002` | 400 | Auth | Verification code expired |
| `AUTH_003` | 429 | Auth | Too many attempts |
| `AUTH_004` | 401 | Auth | Token expired |
| `AUTH_005` | 403 | Auth | Account suspended |
| `LST_201` | 400 | Listing | Face amount must be greater than zero |
| `LST_202` | 400 | Listing | Due date must be in the future |
| `LST_203` | 400 | Listing | Sayad number must be 16 digits |
| `LST_204` | 400 | Listing | Cheque already registered (duplicate) |
| `LST_205` | 400 | Listing | Daily listing limit (10) reached |
| `LST_206` | 400 | Listing | At least one cheque image required |
| `MOD_101` | 400 | Moderation | Incomplete information |
| `MOD_102` | 400 | Moderation | Poor quality image |
| `MOD_103` | 400 | Moderation | Invalid cheque |
| `MOD_104` | 400 | Moderation | Duplicate listing |
| `MOD_105` | 400 | Moderation | Risk too high |
| `MOD_106` | 400 | Moderation | Other |
| `MOD_306` | 400 | Moderation | Maximum resubmission limit exceeded (3 rejects) |

> Note: The spec defines listing errors as `LST_*` (not `LISTING_*`); there are no `MATCH_*`
> codes defined in the spec yet (the matching flow is implemented per Phase 6).

---

## Legacy Endpoints (Backward Compatibility)

The following endpoints remain available under `/api/` for backward compatibility:

- `POST /api/login/` - Same as `/api/v1/auth/login/`
- `GET /api/users/me/` - Same as `/api/v1/users/me/`
- `GET /api/schema/` - API schema
- `GET /api/docs/` - Swagger UI documentation
