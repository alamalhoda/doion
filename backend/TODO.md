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

## Phase 4 — Moderation — Completed

- [x] Create `doion.moderation` app with `ModerationDecision` model
- [x] `ModerationViewSet.queue` endpoint for Moderator/Admin only
- [x] `ModerationViewSet.decision` endpoint for approve/reject
- [x] `ModerationResubmitLimitExceeded` exception for MOD_306
- [x] Signal handlers for `ChequeListingPublished` and `ListingRejected`
- [x] Integration with Notification model (Phase 7)

## Phase 5 — Marketplace — Completed

- [x] Create `doion.marketplace` app
- [x] `MarketplaceViewSet` with caching (TTL 60s) and pagination (max 50/page)
- [x] `MarketplaceFilter` with risk_tier, amount range, days to due, issuer type, bank name filters

## Phase 6 — Matching — Completed

- [x] Match model created
- [x] Settlement Port stub implemented
- [x] Express interest endpoint

## Phase 7 — Notifications — Completed

- [x] Create `doion.notifications` app with `Notification` and `NotificationPreference` models
- [x] `NotificationViewSet` with list, retrieve, mark-read, mark-all-read, preferences actions
- [x] Index optimization on `(user, -created_at)` and `(user, status, -created_at)`
- [x] TextChoices for `NotificationType`, `NotificationChannel`, `NotificationStatus`
- [x] Create `doion.integrations` app with `SMSLog` model and `send_sms` stub service
- [x] Signal handlers for `ChequeListingPublished` and `ListingRejected`
- [x] Helper functions for Match events (created, accepted, declined, cancelled, settled)
- [x] Celery task `expire_listings` for expired listings (every 60 minutes)
- [x] Notification URLs registered in api_router
- [x] Tests: test_models.py, test_views.py, test_signals.py, test_services.py, test_celery_task.py

- [x] Create `doion.checks` app with `IssuerProfile` and `ChequeListing` models
- [x] `TextChoices` enums for `Status` and `IssuerType`
- [x] `UniqueConstraint` on `(issuer, bank_name, cheque_serial_number)` at DB level
- [x] Serializers with validation rules LST_201–LST_205
- [x] `IntegrityError` → `VALIDATION_ERROR` with field-level detail for duplicate sayad
- [x] `ChequeListingViewSet` with create, list, retrieve, update, destroy, `my/`, `upload_document`
- [x] Create `doion.pricing` app with synchronous `calculate_suggested_rate` stub
- [x] Change `Document.related_object_id` from `UUIDField` to `CharField(max_length=255)` for integer PK compatibility
- [x] Migrations created and applied
