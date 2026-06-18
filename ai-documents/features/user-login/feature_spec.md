# Feature Specification — User Login

## 1. Feature Overview

This feature enables users to authenticate into the system using username, email, or phone as identifiers with password verification. The service returns JWT tokens with expiration for API access and establishes Django session for web-based authentication. The service type is **DB-BACKED SERVICE**. Consumers include both web clients (session-based) and API clients (token-based).

## 2. Inputs & Outputs

### Inputs (Login Credentials)
| Name | Type | Required | Constraints |
|------|------|----------|-------------|
| identifier | string | Yes | Must match existing user's username, email, or phone |
| password | string | Yes | Minimum 8 characters |

### Outputs (Authentication Response)
| Field | Type | Description |
|-------|------|-------------|
| access_token | string | JWT token with 1-hour expiration |
| user | object | Serialized User object (id, username, email, name) |
| session_established | boolean | True when web session is active |

### Request/Response Contract (API)
```
POST /api/login/
{
  "identifier": "user_or_email_or_phone",
  "password": "user_password"
}

Response (200 OK):
{
  "access_token": "eyJ...<jwt_token>",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe"
  }
}

Response (401 Unauthorized):
{
  "detail": "Invalid credentials"
}
```

## 3. Business Rules

1. A user can login using username, email, or phone as identifier
2. Login is denied if user account is inactive (is_active=False)
3. Login is denied if user credentials are invalid
4. JWT access token is generated with 1-hour expiration
5. Django session is established for web-based access
6. Login failures are logged with identifier and timestamp (not password)
7. No rate limiting is applied at this stage (security will be added later)

## 4. Acceptance Scenarios

**Scenario 1: Successful login with username**
- Given: A user exists with username "johndoe" and valid password
- When: POST /api/login/ with identifier="johndoe" and password="validpass"
- Then: Returns 200 with access_token and user object

**Scenario 2: Successful login with email**
- Given: A user exists with email "john@example.com" and valid password
- When: POST /api/login/ with identifier="john@example.com" and password="validpass"
- Then: Returns 200 with access_token and user object

**Scenario 3: Successful login with phone**
- Given: A user exists with phone "09123456789" and valid password
- When: POST /api/login/ with identifier="09123456789" and password="validpass"
- Then: Returns 200 with access_token and user object

**Scenario 4: Login with inactive account**
- Given: A user exists with is_active=False
- When: POST /api/login/ with valid credentials
- Then: Returns 401 with "Invalid credentials" message

**Scenario 5: Login with invalid password**
- Given: A user exists with valid username
- When: POST /api/login/ with correct username but wrong password
- Then: Returns 401 with "Invalid credentials" message

**Scenario 6: Login with non-existent identifier**
- Given: No user exists with the provided identifier
- When: POST /api/login/ with any password
- Then: Returns 401 with "Invalid credentials" message

**Scenario 7: Login with missing fields**
- Given: Login endpoint is available
- When: POST /api/login/ with missing identifier or password
- Then: Returns 400 with validation error

## 5. Out of Scope

- Rate limiting and account lockout (future enhancement)
- Refresh token mechanism (future enhancement)
- Password reset functionality
- Social authentication
- Multi-factor authentication
- Token revocation/blacklist