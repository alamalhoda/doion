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

## Phase 2 — KYC — Completed

- [x] Create `doion.identity` Verification model + state machine
- [x] Create `doion.documents` app with Document model
- [x] KYC upload endpoints
- [x] Moderation queue endpoints

## Phase 3 — Listings — Completed

- [x] Create `doion.checks` app with `IssuerProfile` and `ChequeListing` models
- [x] `TextChoices` enums for `Status` and `IssuerType`
- [x] `UniqueConstraint` on `(issuer, bank_name, cheque_serial_number)` at DB level
- [x] Serializers with validation rules LST_201–LST_205
- [x] `IntegrityError` → `VALIDATION_ERROR` with field-level detail for duplicate sayad
- [x] `ChequeListingViewSet` with create, list, retrieve, update, destroy, `my/`, `upload_document`
- [x] Create `doion.pricing` app with synchronous `calculate_suggested_rate` stub
- [x] Change `Document.related_object_id` from `UUIDField` to `CharField(max_length=255)` for integer PK compatibility
- [x] Migrations created and applied
