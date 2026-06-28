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
- `role`: required, one of `check_holder` | `investor`
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
  "id": "uuid",
  "full_name": "رضا کریمی",
  "national_id": "0012345678",
  "company_name": "شرکتExample",
  "status": "pending",
  "documents": [
    { "id": "uuid", "document_type": "national_id_front", "file": "/media/documents/...", "file_size": 102400 }
  ]
}
```

**Errors:** `VALIDATION_ERROR` if fields missing or files invalid.

#### GET /api/v1/verifications/me/
Get current user's latest verification.

**Response 200:**
```json
{
  "id": "uuid",
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
      "id": "uuid",
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
  "id": "uuid",
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

## Role Values

| Value | Label (FA) | Label (EN) | Description |
|-------|------------|------------|-------------|
| `check_holder` | دارنده چک | Check Holder | Can create and list cheques |
| `investor` | سرمایه‌گذار | Investor | Can browse and express interest |
| `moderator` | مدیر | Moderator | Can moderate listings and KYC |
| `admin` | مدیر کل | Admin | Full platform access |

---

## Legacy Endpoints (Backward Compatibility)

The following endpoints remain available under `/api/` for backward compatibility:

- `POST /api/login/` - Same as `/api/v1/auth/login/`
- `GET /api/users/me/` - Same as `/api/v1/users/me/`
- `GET /api/schema/` - API schema
- `GET /api/docs/` - Swagger UI documentation
