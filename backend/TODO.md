# Backend TODO

## Phase 1 — Completed

- [x] Create `doion.core` app with `TimeStampedModel`, `UUIDModel`, permission classes
- [x] Create `doion.identity` app with `Profile` model, register/me/profile endpoints
- [x] Add `role` field to `User` model (TextChoices: check_holder, investor, moderator, admin)
- [x] Create Django Groups on post_migrate (CheckHolder, Investor, Moderator, Admin)
- [x] Update `UserSerializer` to include `role` and `phone`
- [x] Update `LoginTokenSerializer` to include `role` and `phone`
- [x] Register API: `POST /api/v1/identity/register/` with role selection
- [x] Profile API: `GET/PATCH /api/v1/identity/me/` and `/api/v1/identity/profile/`
- [x] Run migrations

## Phase 1 — Remaining

- [ ] Add tests for identity endpoints (serializer + permission)
- [ ] Add rate limiting to register endpoint
- [ ] Add OpenAPI schema annotations (drf-spectacular)

## Phase 2 — KYC

- [ ] Create `doion.identity` Verification model + state machine
- [ ] Create `doion.documents` app with Document model
- [ ] KYC upload endpoints
- [ ] Moderation queue endpoints
