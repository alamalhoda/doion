# API Contract Registry

This document tracks Phase-0 API endpoints and error envelope format for the Cheque Marketplace backend.

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
    "name": "John Doe"
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
  "access": "new_jwt_access_token",
  "refresh": "new_jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe"
  }
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
  "url": "http://api.example.com/api/v1/users/johndoe/"
}
```

---

## Legacy Endpoints (Backward Compatibility)

The following endpoints remain available under `/api/` for backward compatibility:

- `POST /api/login/` - Same as `/api/v1/auth/login/`
- `GET /api/users/me/` - Same as `/api/v1/users/me/`
- `GET /api/schema/` - API schema
- `GET /api/docs/` - Swagger UI documentation