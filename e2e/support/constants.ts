/** Demo users from `manage.py seed_demo` (doion backend). */
export const DEMO_PASSWORD =
  process.env.DEMO_SEED_PASSWORD || "password123";

export const USERS = {
  holder: "holder1",
  investor: "investor1",
  moderator: "moderator1",
  admin: "admin1",
  holderKycPending: "holderkyc1",
} as const;

/** Stable cheque serials from enriched `seed_demo`. */
export const SEED = {
  acceptMatchSerial: "2000000000000001",
  declineMatchSerial: "2000000000000002",
  expressInterestSerial: "2000000000000022",
  approvePendingSerial: "3000000000000001",
  rejectPendingSerial: "3000000000000012",
  publishedCount: 22,
  pendingCount: 12,
  notificationCount: 12,
  marketplacePageSize: 20,
  notificationsPageSize: 10,
} as const;

export const ROUTES = {
  login: "/login",
  marketplace: "/marketplace",
  moderation: "/moderation",
  moderationKyc: "/moderation/kyc",
  matches: "/matches",
  myListings: "/listings/my",
  listingCreate: "/listings/create",
  notifications: "/notifications",
  adminStats: "/admin/stats",
  adminFeatureFlags: "/admin/feature-flags",
  adminAudit: "/admin/audit",
  profile: "/me",
  landing: "/landing",
  expressInterest: (listingId: number | string) =>
    `/matches/express-interest/${listingId}`,
  moderationReview: (listingId: number | string) =>
    `/moderation/review/${listingId}`,
  kycReview: (verificationId: number | string) =>
    `/moderation/kyc/${verificationId}`,
} as const;

/**
 * Prefer data-testid after AI Studio applies prep / critical-path prompts.
 * Fallbacks match current LoginView / Marketplace / ModerationQueue copy.
 */
export const TEST_IDS = {
  loginIdentifier: "login-identifier",
  loginPassword: "login-password",
  loginSubmit: "login-submit",
  mockModeSwitch: "mock-mode-switch",
  marketplacePage: "marketplace-page",
  marketplaceListingCard: "marketplace-listing-card",
  marketplacePagination: "marketplace-pagination",
  moderationQueuePage: "moderation-queue-page",
  moderationItem: "moderation-item",
  moderationApproveBtn: "moderation-approve-btn",
  moderationApproveConfirm: "moderation-approve-confirm",
  matchesPage: "matches-page",
  matchCard: "match-card",
  matchesTabReceived: "matches-tab-received",
  matchesTabSent: "matches-tab-sent",
  matchesPanelReceived: "matches-panel-received",
  matchesPanelSent: "matches-panel-sent",
  matchAcceptBtn: "match-accept-btn",
  matchAcceptConfirm: "match-accept-confirm",
  matchDeclineBtn: "match-decline-btn",
  matchDeclineConfirm: "match-decline-confirm",
  matchStatusAccepted: "match-status-accepted",
  matchStatusDeclined: "match-status-declined",
  expressInterestPage: "express-interest-page",
  expressInterestMessage: "express-interest-message",
  expressInterestSubmit: "express-interest-submit",
  expressInterestConfirm: "express-interest-confirm",
  listingCreatePage: "listing-create-page",
  listingFillSample: "listing-fill-sample",
  listingCreateSubmit: "listing-create-submit",
  moderationRejectBtn: "moderation-reject-btn",
  moderationRejectConfirm: "moderation-reject-confirm",
  kycApproveBtn: "kyc-approve-btn",
  kycRejectBtn: "kyc-reject-btn",
  kycSubmitBtn: "kyc-submit-btn",
  adminStatsPage: "admin-stats-page",
  adminFeatureFlagsPage: "admin-feature-flags-page",
  notificationsPage: "notifications-page",
  notificationItem: "notification-item",
  notificationMarkRead: "notification-mark-read",
  notificationsPagination: "notifications-pagination",
  landingPage: "landing-page",
  landingHeader: "landing-header",
  landingFooter: "landing-footer",
  landingTrustStrip: "landing-trust-strip",
  landingSectionHero: "landing-section-hero",
  landingSectionHowItWorks: "landing-section-how-it-works",
  landingSectionLiveListings: "landing-section-live-listings",
  landingSectionFaq: "landing-section-faq",
  landingListingsGrid: "landing-listings-grid",
  landingListingsLoading: "landing-listings-loading",
  landingListingsError: "landing-listings-error",
  landingHeroPrimaryCta: "landing-hero-primary-cta",
  landingNavLogin: "landing-nav-login",
} as const;
