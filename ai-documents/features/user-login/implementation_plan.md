# Implementation Plan — User Login

## Architecture Summary

Combined web + API login using Django custom User model, Simple JWT for token-based auth, and django-allauth for session-based auth. Users can authenticate with username, email, or phone. Phone field will be added to User model.

## Implementation Steps

- [ ] Step 1: Add phone field to User model and create migration
- [ ] Step 2: Add Simple JWT dependency and configure in settings
- [ ] Step 3: Create LoginSerializer for validation
- [ ] Step 4: Create LoginService with business logic
- [ ] Step 5: Create LoginView for API endpoint
- [ ] Step 6: Configure URL routing
- [ ] Step 7: Update allauth configuration to support phone login
- [ ] Step 8: Write tests

## Key Decisions & Assumptions

1. **Phone field**: Adding nullable phone field to User model - allows login-by-phone without requiring it for all users
2. **Simple JWT**: Using `djangorestframework-simplejwt` with 1-hour access token expiration
3. **Identifier flexibility**: Login accepts username OR email OR phone in a single `identifier` field
4. **Error message**: Generic "Invalid credentials" for all authentication failures (security best practice)
5. **UserSerializer update**: Will include email and name fields for response

## Open Questions

- Should phone be unique? (Assuming yes for identifier purposes)
- What format should phone be stored in? (Assuming E.164 format, no validation on input)