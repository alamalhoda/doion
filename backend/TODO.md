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

- [x] Add tests for identity endpoints (serializer + permission)
- [x] Add rate limiting to register endpoint
- [x] Enforce KYC_APPROVED before listing create / express interest
- [x] Scope IssuerProfile update/delete to creator or staff (`created_by`)
- [x] Default `ordering` on FeatureFlag / Verification / Match / ChequeListing / IssuerProfile
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

## Phase 6 — Matching — Completed (backend), frontend wiring in progress

> Backend was implemented and merged via PR #6. The matching app exists, is in
> `INSTALLED_APPS`, and has models/views/serializers/services/urls/tests. Remaining
> work: frontend wiring to consume the API (`features/matches/`).

- [x] Match model + state machine
- [x] Settlement Port implementation
- [x] Express interest endpoint (`POST /api/v1/matches/`)
- [x] Match status transitions + listing `MATCHED` side-effect
- [x] Notification match-event handlers wired
- [ ] Frontend `matchService.ts` / `matchStore.ts` / views fully validated end-to-end

## Phase 8 — Compliance, Jobs & Hardening — Completed

- [x] Create `doion.compliance` app with `AuditEvent` and `FeatureFlag` models
- [x] `AuditEvent` indexes on `(event_type, -created_at)` and `actor`
- [x] `FeatureFlag.is_enabled(key, default)` classmethod
- [x] Seed `matching_enabled`, `notifications_sms_enabled`, and `show_risk_tier` flags on `post_migrate`
- [x] `FeatureFlagViewSet`: `GET` public; `PATCH`/`toggle` Moderator/Admin; system flags protected
- [x] `ComplianceStatsView`: `GET /api/v1/compliance/stats/` aggregate admin stats
- [x] `AuditEventViewSet`: `GET /api/v1/compliance/audit/` (paginated)
- [x] Compliance URLs wired into `config/api_router.py`; app added to `LOCAL_APPS`
- [x] Audit hooks on `ChequeListingPublished`, `ListingRejected`, KYC approved/rejected, and `FeatureFlag` changes
- [x] Celery app instance (`config/celery.py`) + guarded `shared_task` `expire_listings`; Beat schedule already in settings
- [x] DRF throttling: anon 100/min, user 1000/min, `listing_create` scope 10/day (ChequeListing create)
- [x] `CorrelationIDMiddleware` (`X-Correlation-ID`) + structlog JSON logging config (guarded imports so app boots without the packages)
- [x] Resolved `urls.W005` namespace warning in `config/urls.py`
- [x] Tests: `test_models.py`, `test_views.py`, `test_celery.py` (expire_listings → EXPIRED), `test_audit.py`
- [x] API contract consolidated into `docs/development/MASTER_API_CONTRACT.md` (SSOT); `API_CONTRACT_REGISTRY.md` deprecated stub

## Domain factories (prep for demo seed + broader tests)

- [x] App-level factories (outside `tests/`) for User, IssuerProfile, ChequeListing, Profile, Verification, Notification, Match, ModerationDecision
- [x] Refactor existing tests to use shared factories (DRY/SSOT)
- [x] `seed_demo` management command using the same factories
- [x] Local demo SQLite switch: `DJANGO_DEMO_DATABASE=1` → `db.demo.sqlite3` (see `docs/development/BACKEND_DEMO_SEED_AND_DATA.md`)

## Follow-ups (after `feature/backend-critical-path-test-hardening`)

کارهای توصیه‌شده برای بعد از merge این branch — عمداً اینجا انجام نشد تا PR کوچک و قابل‌بازبینی بماند.
جزئیات دمو/چابکان: [`docs/development/BACKEND_DEMO_SEED_AND_DATA.md`](../docs/development/BACKEND_DEMO_SEED_AND_DATA.md) (بخش Follow-ups).

### Wave 2 — Automation & quality
- [x] GitHub Actions: `pytest` روی PR/push به `develop` (`.github/workflows/ci-backend.yml`); `ruff` فعلاً فقط لوکال — gate اجباری بعد از پاک‌سازی lint
- [ ] رفع `UnorderedObjectListWarning` با `ordering` / `order_by` روی querysetهای FeatureFlag / Verification / Match / ChequeListing / IssuerProfile
- [ ] پوشش بیشتر matching API (شاخه‌های باقی‌مانده در `matching/views.py`) و edgeهای upload سند

### Demo / staging (ops)
- [ ] محیط staging یا demo جدا روی چابکان با **Postgres** + `migrate` + `seed_demo` (نه SQLite روی production)
- [ ] راهنمای کوتاه در پنل/runbook: رمز دمو فقط از `DEMO_SEED_PASSWORD` / خروجی seed؛ هرگز در production واقعی seed با `--reset` بدون آگاهی

### Cross-cutting (خارج از این مونورپو یا موج جدا)
- [x] E2E smoke harness در `e2e/` (Playwright) با `VITE_USE_MOCK=false` + `seed_demo` / demo DB — see [`docs/development/E2E_LOCAL_RUNBOOK.md`](../docs/development/E2E_LOCAL_RUNBOOK.md)
- [x] E2E critical-path specs + rich `seed_demo` (express interest / accept / moderation approve / create listing / notifications mark-read) — runbook + [`AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md`](../docs/development/AI_STUDIO_E2E_CRITICAL_PATH_PROMPT.md); needs Studio testids then `npm run test:critical`
- [x] CI Playwright (smoke + critical) — `.github/workflows/ci-e2e.yml`
- [ ] ادامه تست‌های UI در `checkyar-googleai` (store/API-client با mock کنترل‌شده) فقط از طریق AI Studio — selector prep: [`docs/development/AI_STUDIO_E2E_PREP_PROMPT.md`](../docs/development/AI_STUDIO_E2E_PREP_PROMPT.md) + Phase A: [`V1_PHASE_A_STUDIO_PROMPT.md`](../docs/development/V1_PHASE_A_STUDIO_PROMPT.md)

### Phase 8 — Remaining (requires shell, blocked in this environment)
- [ ] `python manage.py makemigrations` + `migrate` (generates compliance 0001 and the pending integrations/moderation/notifications migrations)
- [ ] `pip install celery structlog` (deps already declared in pyproject.toml)
- [ ] Run `python manage.py test doion.compliance` to confirm green
