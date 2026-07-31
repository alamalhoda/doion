// ============================================================================
// CHEQUE YAR — MASTER API TYPES
// Target Stack: Django REST Framework 5.x <-> Vue 3 + Naive UI + Pinia (Strict TS)
// Source of Truth: docs/development/MASTER_API_CONTRACT.md
// Sync: Keep this file in sync with backend code changes.
// ============================================================================

// ============================================================================
// 1. GLOBAL ENUMS & LITERALS
// ============================================================================

/** User roles */
export type UserRole = 'check_holder' | 'investor' | 'moderator' | 'admin';

/** Verification status values */
export type VerificationStatus = 'pending' | 'approved' | 'rejected';

/** ChequeListing status values */
export type ListingStatus =
  | 'pending_moderation'
  | 'published'
  | 'rejected'
  | 'matched'
  | 'expired'
  | 'withdrawn'
  | 'settled_off_platform';

/** Match status values */
export type MatchStatus =
  | 'pending'
  | 'accepted'
  | 'declined'
  | 'cancelled'
  | 'off_platform_confirmed'
  | 'settled';

/** Match settlement type values */
export type SettlementType = 'off_platform' | 'escrow' | 'principal_ledger';

/** Issuer type values */
export type IssuerType = 'legal' | 'natural';

/** Document type values */
export type DocumentType =
  | 'national_id_front'
  | 'national_id_back'
  | 'selfie'
  | 'cheque_image'
  | 'id_document'
  | 'supplementary';

/** Notification type values */
export type NotificationType =
  | 'match_created'
  | 'match_accepted'
  | 'match_declined'
  | 'match_cancelled'
  | 'settlement_confirmed'
  | 'listing_published'
  | 'listing_rejected'
  | 'listing_expired'
  | 'kyc_approved'
  | 'kyc_rejected'
  | 'new_moderation_item';

/** Notification channel values */
export type NotificationChannel = 'in_app' | 'sms' | 'email';

/** Notification status values */
export type NotificationStatus = 'pending' | 'sent' | 'read' | 'failed';

/** Moderation decision values */
export type ModerationDecision = 'approved' | 'rejected';

/** Rejection code values */
export type RejectionCode =
  | 'MOD_101'
  | 'MOD_102'
  | 'MOD_103'
  | 'MOD_104'
  | 'MOD_105'
  | 'MOD_106';

// ============================================================================
// 2. ERROR TYPES
// ============================================================================

/** General error codes */
export type GeneralErrorCode =
  | 'VALIDATION_ERROR'
  | 'AUTHENTICATION_ERROR'
  | 'PERMISSION_ERROR'
  | 'NOT_FOUND_ERROR'
  | 'SERVER_ERROR';

/**
 * Listing validation historically labeled LST_* in specs.
 * Live backend emits VALIDATION_ERROR with field details — LST_* are not envelope codes.
 */
export type ListingSpecLabel = 'LST_201' | 'LST_202' | 'LST_203' | 'LST_204' | 'LST_205' | 'LST_206';

/** Envelope moderation code (resubmit limit). MOD_101–106 are rejection_code payload values. */
export type ModerationEnvelopeErrorCode = 'MOD_306';

/** All envelope error codes union (emitted by custom_exception_handler) */
export type ErrorCode = GeneralErrorCode | ModerationEnvelopeErrorCode;

/** Field-level validation error detail */
export interface ApiErrorDetail {
  field?: string;
  code: ErrorCode | string;
  message: string;
}

/** Standard error envelope returned by custom_exception_handler */
export interface ApiErrorEnvelope {
  error: {
    code: string;
    message: string;
    details?: Record<string, string[]> | ApiErrorDetail[];
  };
}

// ============================================================================
// 3. AUTH TYPES
// ============================================================================

/** Login request */
export interface LoginRequest {
  identifier: string;
  password: string;
}

/** Login response */
export interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    name: string;
    role: UserRole;
    phone?: string | null;
  };
}

/** Register request */
export interface RegisterRequest {
  username: string;
  email?: string;
  password: string;
  password_confirm: string;
  name?: string;
  phone?: string;
  role: 'check_holder' | 'investor';
}

/** Register response */
export interface RegisterResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    name: string;
    role: 'check_holder' | 'investor';
    phone?: string | null;
  };
}

/** Refresh token request */
export interface RefreshTokenRequest {
  refresh: string;
}

/** Refresh token response */
export interface RefreshTokenResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    name: string;
    role: UserRole;
    phone?: string | null;
  };
}

// ============================================================================
// 4. USER & IDENTITY TYPES
// ============================================================================

/** User object (GET /users/me/, identity/me) */
export interface User {
  id: number;
  username: string;
  email: string;
  name: string;
  phone?: string | null;
  role: UserRole;
  is_verified: boolean;
  url?: string;
}

/** Profile object */
export interface Profile {
  id: number;
  username: string;
  email: string;
  name: string;
  phone: string;
  role: UserRole;
  bio: string;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

// ============================================================================
// 5. KYC / VERIFICATION TYPES
// ============================================================================

/** Document object */
export interface Document {
  id: number;
  document_type: DocumentType;
  file: string;
  file_size: number;
}

/** Verification object */
export interface Verification {
  id: number;
  full_name: string;
  national_id: string;
  company_name: string;
  status: VerificationStatus;
  rejection_reason: string;
  rejection_code: string;
  documents: Document[];
}

/** Create verification request (multipart/form-data) */
export interface CreateVerificationRequest {
  full_name: string;
  national_id?: string;
  company_name?: string;
  national_id_front: File;
  national_id_back: File;
  selfie?: File;
}

// ============================================================================
// 6. CHEQUE LISTING TYPES
// ============================================================================

/** Issuer profile object */
export interface IssuerProfile {
  id: number;
  national_or_company_id: string;
  name: string;
  credit_score: number | null;
  created_at: string;
  updated_at: string;
}

/** Cheque listing object */
export interface ChequeListing {
  id: number;
  owner_id: number;
  issuer_profile: IssuerProfile;
  bank_name: string;
  cheque_serial_number: string;
  face_amount: string; // DecimalField returns string in DRF
  due_date: string; // ISO date
  issuer_type: IssuerType;
  issuer_name: string;
  issuer_national_id: string;
  description: string;
  suggested_discount_rate: string | null;
  risk_tier: 'low' | 'medium' | 'high' | null;
  status: ListingStatus;
  rejection_reason: string;
  rejection_code: string | null;
  resubmit_count: number;
  created_at: string;
  updated_at: string;
}

/** Create listing request */
export interface CreateListingRequest {
  issuer: number;
  bank_name: string;
  cheque_serial_number: string;
  face_amount: number;
  due_date: string;
  issuer_type: IssuerType;
  issuer_name: string;
  issuer_national_id: string;
  description?: string;
}

/** Update listing request (same fields as create, all optional) */
export type UpdateListingRequest = Partial<CreateListingRequest>;

/** Listing filters for marketplace (page_size is not supported; fixed PAGE_SIZE=20) */
export interface ListingFilters {
  risk_tier?: 'low' | 'medium' | 'high';
  min_amount?: number;
  max_amount?: number;
  max_days_to_due?: number;
  issuer_type?: 'legal' | 'natural';
  bank_name?: string;
  ordering?: string;
  page?: number;
}

// ============================================================================
// 7. MARKETPLACE TYPES
// ============================================================================

/** Marketplace listing (lightweight for list views) */
export interface MarketplaceListing {
  id: number;
  owner_id: number;
  issuer_profile: IssuerProfile;
  bank_name: string;
  cheque_serial_number: string;
  face_amount: string;
  due_date: string;
  issuer_type: IssuerType;
  issuer_name: string;
  issuer_national_id: string;
  description: string;
  suggested_discount_rate: string | null;
  risk_tier: 'low' | 'medium' | 'high' | null;
  status: ListingStatus;
  days_to_due: number;
  interest_count: number;
  published_at: string | null;
  created_at: string;
  updated_at: string;
}

/** Latest marketplace listing (even more lightweight) */
export interface MarketplaceLatestListing {
  id: number;
  issuer_profile: IssuerProfile;
  bank_name: string;
  face_amount: string;
  due_date: string;
  issuer_type: IssuerType;
  suggested_discount_rate: string | null;
  risk_tier: 'low' | 'medium' | 'high' | null;
  status: ListingStatus;
  days_to_due: number;
  created_at: string;
}

// ============================================================================
// 8. MATCH TYPES
// ============================================================================

/** User summary (minimal user info in match context) */
export interface UserSummary {
  id: number;
  username: string;
  name: string;
}

/** Minimal listing summary in match context */
export interface ListingSummary {
  id: number;
  bank_name: string;
  face_amount: string;
  due_date: string;
  status: ListingStatus;
  created_at: string;
  updated_at: string;
}

/** Match object */
export interface Match {
  id: number;
  listing: ListingSummary;
  investor: UserSummary;
  check_holder: UserSummary;
  status: MatchStatus;
  settlement_type: SettlementType;
  final_discount_rate: string | null;
  terms: string;
  message: string;
  created_at: string;
  updated_at: string;
}

/** Create match request */
export interface CreateMatchRequest {
  listing_id: number;
  message?: string;
}

/** Update match status request */
export interface UpdateMatchStatusRequest {
  status: MatchStatus;
  final_discount_rate?: string | null;
  terms?: string;
}

// ============================================================================
// 9. MODERATION TYPES
// ============================================================================

/** Moderation queue listing item */
export interface ModerationQueueItem {
  id: number;
  owner_id: number;
  issuer_profile: IssuerProfile;
  bank_name: string;
  cheque_serial_number: string;
  face_amount: string;
  due_date: string;
  issuer_type: IssuerType;
  issuer_name: string;
  issuer_national_id: string;
  description: string;
  suggested_discount_rate: string | null;
  risk_tier: 'low' | 'medium' | 'high' | null;
  status: ListingStatus;
  rejection_reason: string;
  rejection_code: string | null;
  resubmit_count: number;
  created_at: string;
  updated_at: string;
}

/** Moderation decision request payload */
export interface ModerationDecisionRequest {
  decision: 'approve' | 'reject';
  rejection_code?: RejectionCode;
  rejection_note?: string;
}

/** Moderation decision response */
export interface ModerationDecisionResponse {
  id: number;
  listing: number;
  moderator: number | null;
  decision: ModerationDecision;
  rejection_code: RejectionCode | null;
  rejection_code_display: string | null;
  rejection_note: string;
  created_at: string;
}

// ============================================================================
// 10. NOTIFICATION TYPES
// ============================================================================

/** Notification object */
export interface Notification {
  id: number;
  type: NotificationType;
  channel: NotificationChannel;
  status: NotificationStatus;
  title: string;
  message: string;
  related_object_type?: string;
  related_object_id?: string;
  read_at: string | null;
  sent_at: string | null;
  created_at: string;
}

/** Notification preferences */
export interface NotificationPreferences {
  in_app_enabled: boolean;
  sms_enabled: boolean;
  email_enabled: boolean;
}

/** Mark notification as read request */
export interface MarkNotificationReadRequest {
  is_read: boolean;
}

// ============================================================================
// 11. COMPLIANCE & ADMIN TYPES
// ============================================================================

/** Feature flag object */
export interface FeatureFlag {
  key: string;
  description: string;
  is_enabled: boolean;
  is_system: boolean;
}

/** Audit event object */
export interface AuditEvent {
  id: number;
  actor: number;
  actor_username: string;
  event_type: string;
  object_type: string;
  object_id: string;
  metadata: Record<string, any>;
  ip_address: string;
  created_at: string;
}

/** Admin dashboard stats */
export interface AdminDashboardStats {
  listings: {
    total: number;
    published: number;
    pending_moderation: number;
    rejected: number;
    expired: number;
    matched: number;
  };
  users: {
    total: number;
    kyc_pending: number;
    kyc_approved: number;
  };
  verifications: {
    pending: number;
  };
  notifications: {
    unread: number;
  };
}

// ============================================================================
// 12. COMMON / PAGINATION TYPES
// ============================================================================

/** Standard DRF paginated response */
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

/** API error detail (field-level) */
export interface ApiError {
  field?: string;
  code: string;
  message: string;
}

// ============================================================================
// 13. CONSTANTS & LABELS
// ============================================================================

export const NOTIFICATION_TYPE_LABELS: Record<NotificationType, string> = {
  match_created: 'ابراز تمایل جدید',
  match_accepted: 'تطابق پذیرفته شد',
  match_declined: 'تطابق رد شد',
  match_cancelled: 'تطابق لغو شد',
  settlement_confirmed: 'تسویه تأیید شد',
  listing_published: 'آگهی منتشر شد',
  listing_rejected: 'آگهی رد شد',
  listing_expired: 'آگهی منقضی شد',
  kyc_approved: 'احراز هویت تأیید شد',
  kyc_rejected: 'احراز هویت رد شد',
  new_moderation_item: 'آگهی/احراز هویت جدید',
};

export const REJECTION_CODE_LABELS: Record<RejectionCode, string> = {
  MOD_101: 'اطلاعات ناقص',
  MOD_102: 'تصویر با کیفیت پایین',
  MOD_103: 'چک نامعتبر',
  MOD_104: 'آگهی تکراری',
  MOD_105: 'ریسک بیش از حد',
  MOD_106: 'سایر',
};

export const LISTING_STATUS_LABELS: Record<ListingStatus, string> = {
  pending_moderation: 'در انتظار بررسی',
  published: 'منتشر شده',
  rejected: 'رد شده',
  matched: 'تطابق داده شده',
  expired: 'منقضی شده',
  withdrawn: 'پس گرفته شده',
  settled_off_platform: 'تسویه شده',
};

export const MATCH_STATUS_LABELS: Record<MatchStatus, string> = {
  pending: 'در انتظار',
  accepted: 'پذیرفته شده',
  declined: 'رد شده',
  cancelled: 'لغو شده',
  off_platform_confirmed: 'تأیید تسویه',
  settled: 'تسویه نهایی',
};
