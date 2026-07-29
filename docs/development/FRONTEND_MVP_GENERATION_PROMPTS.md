# Frontend MVP Generation Prompts — Cheque Yar

This file contains two LLM prompts in order:

1. First build the **Infrastructure Prompt** (Vite, router, axios client, simulator, auth, shared layout).
2. Then build each **Feature Prompt** for individual pages.

All prompts keep the error envelope and field names aligned with the actual backend contract.

---

# PART 1 — INFRASTRUCTURE PROMPT

```text
You are a senior frontend architect. Build the foundational infrastructure for a production-ready Vue 3 application named "Cheque Yar" — an Iranian financial receivables and cheque trading platform.

=== SOURCES OF TRUTH ===
Read and strictly follow:
- docs/development/MASTER_API_CONTRACT.md
- frontend/src/types/api.d.ts

=== TECH STACK ===
- Vue 3 (Composition API, `<script setup lang="ts">` exclusively)
- TypeScript (Strict Mode)
- Naive UI (`naive-ui`)
- Pinia for state management
- Vue Router 4
- Axios for HTTP client
- Vite for build tooling
- **Policy:** No CDN dependencies, no jQuery, no Options API, no `any` unless absolutely unavoidable.

=== DELIVERABLE ===
Provide the complete file contents for the scaffold below. Every file must be complete and compile-ready. Do not use placeholders or `// TODO` comments.

### 1. Package & Config
- package.json
- tsconfig.json
- vite.config.ts
- index.html

### 2. Entry & Shell
- src/main.ts
- src/App.vue
- src/vite-env.d.ts

### 3. Router
- src/router/index.ts with routes for:
  - `/login` — LoginView
  - `/register` — RegisterView
  - `/me` — ProfileView
  - `/account` — MyAccountView
  - `/listings/create` — ListingCreateView
  - `/listings/my` — MyListingsView
  - `/listings/:id` — ListingDetailView
  - `/listings/:id/edit` — ListingEditView
  - `/marketplace` — MarketplaceView
  - `/matches/express-interest/:listingId` — ExpressInterestView
  - `/matches` — MyMatchesView
  - `/matches/:id` — MatchDetailView (placeholder is fine)
  - `/notifications` — NotificationsView
  - `/notifications/preferences` — NotificationPreferencesView
  - `/moderation` — ModerationQueueView
  - `/moderation/kyc` — KycQueueView
  - `/admin/stats` — AdminStatsView
  - `/admin/feature-flags` — FeatureFlagsView
  - `/admin/audit` — AuditEventsView
- Include navigation guards using `authStore` and `canAccessModeration` / `canAccessAdmin` helpers.

### 4. API Client & Mock Adapter
- `src/api/client.ts`
  - Configure axios with `baseURL` from `import.meta.env.VITE_API_BASE_URL`.
  - Request interceptor: attach `Authorization: Bearer <access>`.
  - Response interceptor: if `import.meta.env.VITE_USE_MOCK === 'true'`, forward the resolved promise to `useBackendSimulatorStore` so the store returns data. If `VITE_USE_MOCK === 'false'`, pass through.
  - Expose `api` and `setMockMode(enabled: boolean)`.
- `src/api/index.ts`
  - Re-export axios instance and per-feature API modules (auth, identity, listings, marketplace, matches, notifications, moderation, compliance).

### 5. Types
- `src/types/api.d.ts` — Single source of truth. Implement exactly these interfaces/enums/exports (no additions, no removals, match current file verbatim except for any corrections noted below):

```ts
export type UserRole = 'check_holder' | 'investor' | 'moderator' | 'admin';
export type VerificationStatus = 'pending' | 'approved' | 'rejected';
export type ListingStatus = 'pending_moderation' | 'published' | 'rejected' | 'matched' | 'expired' | 'withdrawn' | 'settled_off_platform';
export type MatchStatus = 'pending' | 'accepted' | 'declined' | 'cancelled' | 'off_platform_confirmed' | 'settled';
export type SettlementType = 'off_platform' | 'escrow' | 'principal_ledger';
export type IssuerType = 'legal' | 'natural';
export type DocumentType = 'national_id_front' | 'national_id_back' | 'selfie' | 'cheque_image' | 'id_document' | 'supplementary';
export type NotificationType = 'match_created' | 'match_accepted' | 'match_declined' | 'match_cancelled' | 'settlement_confirmed' | 'listing_published' | 'listing_rejected' | 'listing_expired' | 'kyc_approved' | 'kyc_rejected' | 'new_moderation_item';
export type NotificationChannel = 'in_app' | 'sms' | 'email';
export type NotificationStatus = 'pending' | 'sent' | 'read' | 'failed';
export type ModerationDecision = 'approved' | 'rejected';
export type RejectionCode = 'MOD_101' | 'MOD_102' | 'MOD_103' | 'MOD_104' | 'MOD_105' | 'MOD_106';

export type GeneralErrorCode = 'VALIDATION_ERROR' | 'AUTHENTICATION_ERROR' | 'PERMISSION_ERROR' | 'NOT_FOUND_ERROR' | 'SERVER_ERROR';
export type ListingErrorCode = 'LST_201' | 'LST_202' | 'LST_203' | 'LST_204' | 'LST_205' | 'LST_206';
export type ModerationErrorCode = 'MOD_101' | 'MOD_102' | 'MOD_103' | 'MOD_104' | 'MOD_105' | 'MOD_106' | 'MOD_306';
export type ErrorCode = GeneralErrorCode | ListingErrorCode | ModerationErrorCode;

export interface ApiErrorDetail { field?: string; code: ErrorCode | string; message: string; }
export interface ApiErrorEnvelope { error: { code: string; message: string; details?: Record<string, string[]> | ApiErrorDetail[]; }; }

export interface LoginRequest { identifier: string; password: string; }
export interface LoginResponse { access: string; refresh: string; user: { id: number; username: string; email: string; name: string; }; }
export interface RegisterRequest { username: string; email?: string; password: string; password_confirm: string; name?: string; phone?: string; role: 'check_holder' | 'investor'; }
export interface RegisterResponse { access: string; refresh: string; user: { id: number; username: string; email: string; name: string; role: 'check_holder' | 'investor'; }; }
export interface RefreshTokenRequest { refresh: string; }
export interface RefreshTokenResponse { access: string; refresh: string; user: { id: number; username: string; email: string; name: string; }; }

export interface User { id: number; username: string; email: string; name: string; phone?: string | null; role: UserRole; is_verified: boolean; }
export interface Profile { id: number; username: string; email: string; name: string; phone: string; role: UserRole; bio: string; is_verified: boolean; created_at: string; updated_at: string; }

export interface Document { id: number; document_type: DocumentType; file: string; file_size: number; }
export interface Verification { id: number; full_name: string; national_id: string; company_name: string; status: VerificationStatus; rejection_reason: string; rejection_code: string; documents: Document[]; }
export interface CreateVerificationRequest { full_name: string; national_id?: string; company_name?: string; national_id_front: File; national_id_back: File; selfie?: File; }

export interface IssuerProfile { id: number; national_or_company_id: string; name: string; credit_score: number | null; created_at: string; updated_at: string; }
export interface ChequeListing { id: number; owner_id: number; issuer_profile: IssuerProfile; bank_name: string; cheque_serial_number: string; face_amount: string; due_date: string; issuer_type: IssuerType; issuer_name: string; issuer_national_id: string; description: string; suggested_discount_rate: string | null; risk_tier: 'low' | 'medium' | 'high' | null; status: ListingStatus; rejection_reason: string; rejection_code: string | null; resubmit_count: number; created_at: string; updated_at: string; }
export interface CreateListingRequest { issuer: number; bank_name: string; cheque_serial_number: string; face_amount: number; due_date: string; issuer_type: IssuerType; issuer_name: string; issuer_national_id: string; description?: string; }
export type UpdateListingRequest = Partial<CreateListingRequest>;
export interface ListingFilters { risk_tier?: 'low' | 'medium' | 'high'; min_amount?: number; max_amount?: number; max_days_to_due?: number; issuer_type?: 'legal' | 'natural'; bank_name?: string; ordering?: string; page?: number; page_size?: number; }

export interface MarketplaceListing { id: number; owner_id: number; issuer_profile: IssuerProfile; bank_name: string; cheque_serial_number: string; face_amount: string; due_date: string; issuer_type: IssuerType; issuer_name: string; issuer_national_id: string; description: string; suggested_discount_rate: string | null; risk_tier: 'low' | 'medium' | 'high' | null; status: ListingStatus; days_to_due: number; interest_count: number; published_at: string | null; created_at: string; updated_at: string; }
export interface MarketplaceLatestListing { id: number; issuer_profile: IssuerProfile; bank_name: string; face_amount: string; due_date: string; issuer_type: IssuerType; suggested_discount_rate: string | null; risk_tier: 'low' | 'medium' | 'high' | null; status: ListingStatus; days_to_due: number; created_at: string; }

export interface UserSummary { id: number; username: string; name: string; }
export interface ListingSummary { id: number; bank_name: string; face_amount: string; due_date: string; status: ListingStatus; created_at: string; updated_at: string; }
export interface Match { id: number; listing: ListingSummary; investor: UserSummary; check_holder: UserSummary; status: MatchStatus; settlement_type: SettlementType; final_discount_rate: string | null; terms: string; message: string; created_at: string; updated_at: string; }
export interface CreateMatchRequest { listing_id: number; message?: string; }
export interface UpdateMatchStatusRequest { status: MatchStatus; final_discount_rate?: string | null; terms?: string; }

export interface ModerationQueueItem { id: number; owner_id: number; issuer_profile: IssuerProfile; bank_name: string; cheque_serial_number: string; face_amount: string; due_date: string; issuer_type: IssuerType; issuer_name: string; issuer_national_id: string; description: string; suggested_discount_rate: string | null; risk_tier: 'low' | 'medium' | 'high' | null; status: ListingStatus; rejection_reason: string; rejection_code: string | null; resubmit_count: number; created_at: string; updated_at: string; }
export interface ModerationDecisionRequest { decision: 'approve' | 'reject'; rejection_code?: RejectionCode; rejection_note?: string; }
export interface ModerationDecisionResponse { id: number; listing: number; moderator: number | null; decision: ModerationDecision; rejection_code: RejectionCode | null; rejection_code_display: string | null; rejection_note: string; created_at: string; }

export interface Notification { id: number; type: NotificationType; channel: NotificationChannel; status: NotificationStatus; title: string; message: string; related_object_type?: string; related_object_id?: string; read_at: string | null; sent_at: string | null; created_at: string; }
export interface NotificationPreferences { in_app_enabled: boolean; sms_enabled: boolean; email_enabled: boolean; }
export interface MarkNotificationReadRequest { is_read: boolean; }

export interface FeatureFlag { key: string; description: string; is_enabled: boolean; is_system: boolean; }
export interface AuditEvent { id: number; actor: number; actor_username: string; event_type: string; object_type: string; object_id: string; metadata: Record<string, any>; ip_address: string; created_at: string; }
export interface AdminDashboardStats { listings: { total: number; published: number; pending_moderation: number; rejected: number; expired: number; matched: number; }; users: { total: number; kyc_pending: number; kyc_approved: number; }; verifications: { pending: number; }; notifications: { unread: number; }; }

export interface PaginatedResponse<T> { count: number; next: string | null; previous: string | null; results: T[]; }
export interface ApiError { field?: string; code: string; message: string; }

export const NOTIFICATION_TYPE_LABELS: Record<NotificationType, string> = { match_created: 'ابراز تمایل جدید', match_accepted: 'تطابق پذیرفته شد', match_declined: 'تطابق رد شد', match_cancelled: 'تطابق لغو شده', settlement_confirmed: 'تسویه تأیید شد', listing_published: 'آگهی منتشر شد', listing_rejected: 'آگهی رد شد', listing_expired: 'آگهی منقضی شد', kyc_approved: 'احراز هویت تأیید شد', kyc_rejected: 'احراز هویت رد شده', new_moderation_item: 'آگهی/احراز هویت جدید', };
export const REJECTION_CODE_LABELS: Record<RejectionCode, string> = { MOD_101: 'اطلاعات ناقص', MOD_102: 'تصویر ناخوانا', MOD_103: 'عدم تطابق', MOD_104: 'محتوای غیرمجاز', MOD_105: 'مدارک صادرکننده ناقص', MOD_106: 'سایر', };
export const LISTING_STATUS_LABELS: Record<ListingStatus, string> = { pending_moderation: 'در انتظار بررسی', published: 'منتشر شده', rejected: 'رد شده', matched: 'تطابق داده شده', expired: 'منقضی شده', withdrawn: 'پس گرفته شده', settled_off_platform: 'تسویه شده', };
export const MATCH_STATUS_LABELS: Record<MatchStatus, string> = { pending: 'در انتظار', accepted: 'پذیرفته شده', declined: 'رد شده', cancelled: 'لغو شده', off_platform_confirmed: 'تأیید تسویه', settled: 'تسویه نهایی', };
```

- `src/stores/auth.ts` — Authentication store with `user`, `access`, `refresh`, `isMock`, `login`, `register`, `refreshToken`, `logout`, `loadUser`.

### 6. Backend Simulator Store
- `src/stores/useBackendSimulatorStore.ts` — Simulate full DRF backend behavior.
- **CRITICAL:** Error envelope MUST match API contract exactly.
  - Success: standard DRF response body.
  - Error: `{ error: { code: string, message: string, details?: Record<string, string[]> | ApiErrorDetail[] } }`
  - Do NOT use `{ status, error_code, message, details }` format.
- **CRITICAL:** At Match endpoints on the model, use field name `settlement_type` exactly as in the contract, with values `off_platform`, `escrow`, `principal_ledger`. Do NOT rename it to `settlement_port_type`.
- Support login/register with mocked JWT strings, permission checks, CRUD for all resources, pagination.
- Persist all state to `localStorage` when simulation is active.
- Seed with at least 3 users, 15 listings across Iranian banks, matches, notifications, verifications, feature flags, audit events.

### 7. Shared Layout Components
- `src/shared/components/AppSidebar.vue`
  - RTL sidebar using Naive UI `n-menu`.
  - Route items grouped by feature (Auth excluded).
  - Show unread notification count badge.
- `src/shared/components/AppHeader.vue`
  - Naive UI `n-page-header` or custom header.
  - Role switcher (dev only, injectable via prop).
  - Notification bell.
  - User avatar dropdown with logout.
- `src/shared/components/ConfirmDialog.vue`
  - Generic confirmation modal accepting title/confirmText/cancelText and emit confirm/cancel.
- `src/shared/components/ListingCard.vue`
  - Accept `MarketplaceListing` or `ChequeListing` props.
  - Mask phone/identity in public views.

### 8. Internationalization & RTL
- Set `dir="rtl"` on `<html>` in index.html.
- Use a naive custom locale provider or Naive UI built-in Persian font support.
- All user-facing text must be Persian.
```

---

# PART 2 — FEATURE PROMPTS

⚠️ **Execute the Part 1 prompt first and ensure it compiles before running these prompts.**

---

## PART 2-A: Auth, Identity & Listings

```text
You are continuing the Cheque Yar Vue 3 frontend project. The infrastructure from Part 1 is already built.

=== SOURCES OF TRUTH ===
- docs/development/MASTER_API_CONTRACT.md
- frontend/src/types/api.d.ts

=== POLICY ===
- Use only TypeScript (`<script setup lang="ts">`).
- Strict error envelope matching:
  { error: { code: string, message: string, details?: Record<string, string[]> | ApiErrorDetail[] } }
- RTL layout, Persian labels.
- All mutation pages must include loading, empty, and error states plus a ConfirmDialog for destructive actions.

=== FEATURES TO IMPLEMENT ===

### Auth
1. `src/features/auth/LoginView.vue`
   - Form: identifier + password.
   - On success, store tokens via authStore, redirect to `/marketplace`.
   - Display errors from `ApiErrorEnvelope`.

2. `src/features/auth/RegisterView.vue`
   - Form: username, email, password, password_confirm, name, phone, role (select: check_holder / investor).
   - Validate password match client-side before submit.
   - On success, store tokens, redirect to `/marketplace`.

### Identity
3. `src/features/profile/ProfileView.vue`
   - GET `/api/v1/identity/profile/`.
   - PATCH partial (bio, role).
   - Show read-only fields: id, username, email, name, phone, role, is_verified, created_at, updated_at.

4. `src/features/profile/MyAccountView.vue`
   - GET/PATCH `/api/v1/users/me/`.
   - Show all fields from User interface.

### Listings (Owner Workbench)
5. `src/features/listings/ListingCreateView.vue`
   - 3-step naives-ui Steps wizard:
     1. انتخاب/ایجاد Issuer Profile (form: issuer_type, issuer_name, issuer_national_id).
     2. مشخصات تسهیلات (bank_name, cheque_serial_number, face_amount, due_date).
     3. آپلود مدارک (national_id + supplementary).
   - Validate: cheque_serial_number exactly 16 digits, due_date in future, face_amount > 0.
   - Submit to POST `/api/v1/listings/`.
   - On success, show n-message and redirect to `/listings/:id`.

6. `src/features/listings/MyListingsView.vue`
   - GET `/api/v1/listings/my/` with pagination.
   - n-data-table with actions: view detail, edit (if pending_moderation or rejected), upload document, resubmit (if rejected).
   - Status chips using LISTING_STATUS_LABELS.

7. `src/features/listings/ListingDetailView.vue`
   - GET `/api/v1/listings/{id}/`.
   - Show all listing fields plus documents list.
   - Action buttons based on current user role and listing status.

8. `src/features/listings/ListingEditView.vue`
   - PATCH `/api/v1/listings/{id}/`.
   - Only allow update when status is pending_moderation or rejected.
   - Pre-fill existing data.

9. `src/features/listings/ListingDocumentUploadView.vue`
   - POST `/api/v1/listings/{id}/documents/` multipart/form-data.
   - Accepted document_types: cheque_image, id_document, supplementary.

10. Resubmit Logic (inline in MyListingsView or modal)
    - ConfirmDialog.
    - On confirm, POST `/api/v1/moderation/{id}/resubmit/`.
    - Handle MOD_306 if limit exceeded.
```

---

## PART 2-B: Marketplace & Matches

```text
You are continuing the Cheque Yar Vue 3 frontend project. The infrastructure from Part 1 and Auth/Identity/Listings views are already built.

=== SOURCES OF TRUTH ===
- docs/development/MASTER_API_CONTRACT.md
- frontend/src/types/api.d.ts

=== POLICY ===
- Error envelope: { error: { code, message, details? } }
- Privacy Shielding: mask phone/identity in marketplace public cards (e.g., ۰۹۱۲***۶۷۸۹). Unmask only in MatchesView when status === 'accepted'.
- Off-Platform Settlement only. No digital wallets or payment gateways.

=== FEATURES TO IMPLEMENT ===

### Marketplace
11. `src/features/marketplace/MarketplaceView.vue`
    - GET `/api/v1/marketplace/listings/` with query params from `ListingFilters`.
    - Naive UI `n-data-table` with sorting on ordering param.
    - Sidebar filters: bank_name (autocomplete/text model), min_amount (number), max_amount (number), max_days_to_due (number), risk_tier (select), issuer_type (select).
    - Pagination with page_size 20 max 50 per API contract.
    - n-empty for no results.

12. Latest Listings Widget
    - GET `/api/v1/marketplace/listings/latest/` (AllowAny).
    - Show 4 latest published listings in a horizontal n-card stack.

### Matches
13. `src/features/matches/MyMatchesView.vue`
    - GET `/api/v1/matches/`.
    - Investors see matches where they are investor; check holders see matches where they are check holder.
    - Two tabs: Received (check_holder) / Sent (investor).
    - Status chips with MATCH_STATUS_LABELS.

14. `src/features/matches/ExpressInterestView.vue`
    - GET listing detail first, then POST `/api/v1/matches/` with listing_id + optional message.
    - Only for investor role.
    - ConfirmDialog before express.

15. Match Actions
    - POST `/api/v1/matches/{id}/accept/` — check_holder only.
    - POST `/api/v1/matches/{id}/decline/` — check_holder only, body { note }.
    - POST `/api/v1/matches/{id}/cancel/` — either party.
    - POST `/api/v1/matches/{id}/confirm-off-platform/` — check_holder only.
    - All actions via n-message feedback + optimistic UI refresh of match list.
    - In accepted matches, show unmasked check_holder/investor contact information.
    - Settlement must show banner: "تسویه با تأیید خارج از پلتفرم"
```

---

## PART 2-C: Notifications & Moderation

```text
You are continuing the Cheque Yar Vue 3 frontend project. The infrastructure and core business features are already built.

=== SOURCES OF TRUTH ===
MASTER_API_CONTRACT.md
api.d.ts

=== POLICY ===
- Error envelope: { error: { code, message, details? } }
- All lists support pagination.

=== FEATURES TO IMPLEMENT ===

### Notifications
16. `src/features/notifications/NotificationsView.vue`
    - GET `/api/v1/notifications/` with filters (type, status, page, page_size).
    - Show unread count in AppHeader bell and page header.
    - Actions:
      - PATCH `/api/v1/notifications/{id}/` { is_read: true } (mark single read).
      - POST `/api/v1/notifications/mark-all-read/` (mark all read).
    - Use NotificationItem component for each row.

17. `src/features/notifications/NotificationPreferencesView.vue`
    - GET `/api/v1/notifications/preferences/`.
    - PATCH partial (in_app_enabled, sms_enabled, email_enabled).

### Moderation
18. `src/features/moderation/ModerationQueueView.vue`
    - GET `/api/v1/moderation/queue/` (moderator/admin only).
    - n-data-table with voting columns.
    - Approve/Reject modals:
      - Approve: POST `/api/v1/moderation/{id}/decision/` { decision: 'approve' }.
      - Reject: require rejection_code (RejectionCode enum select) + rejection_note (text).
    - Redirect refetch after each decision.

19. `src/features/moderation/KycQueueView.vue`
    - GET `/api/v1/moderation/kyc/`.
    - Same approve/reject flow but to `/api/v1/moderation/kyc/{id}/decision/`.
    - Show documents preview links.
```

---

## PART 2-D: Admin & Compliance

```text
You are continuing the Cheque Yar Vue 3 frontend project. All previous features are already built.

=== SOURCES OF TRUTH ===
MASTER_API_CONTRACT.md
api.d.ts

=== POLICY ===
- Admin/Moderation guards must route unauthorized users to /marketplace with n-message warning.

=== FEATURES TO IMPLEMENT ===

### Admin
20. `src/features/admin/AdminStatsView.vue`
    - GET `/api/v1/compliance/stats/`.
    - Render four n-statistic groups (listings, users, verifications, notifications) inside n-card layout.

21. `src/features/admin/FeatureFlagsView.vue`
    - GET `/api/v1/compliance/feature-flags/`.
    - PATCH `/api/v1/compliance/feature-flags/{key}/` { is_enabled: true/false }.
    - Admin-only toggles; disable n-switch if `is_system === true`.

22. `src/features/admin/AuditEventsView.vue`
    - GET `/api/v1/compliance/audit/` with pagination.
    - n-data-table columns: id, actor_username, event_type, object_type, object_id, ip_address, created_at.

### Error Boundary & Dev Tools
- Add a global error handler in `src/main.ts` to catch unhandled Promise rejections and show n-message.
- Ensure simulator mode toggle is accessible from AppHeader or Dev Toolbar.
```

---

# USAGE NOTES

1. Paste each block above into an LLM interface.
2. Run Part 1 first. Verify `npm install && npm run dev` succeeds.
3. Run Part 2-A, then 2-B, then 2-C, then 2-D sequentially.
4. After all parts are generated, run the linter (`npm run lint`) and fix any remaining TS issues.
5. Verify the mock mode flag in `.env` shows `VITE_USE_MOCK=true` and `VITE_API_BASE_URL=http://localhost:8000` for real API switch later.
