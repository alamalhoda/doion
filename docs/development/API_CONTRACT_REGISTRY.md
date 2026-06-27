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
