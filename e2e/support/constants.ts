/** Demo users from `manage.py seed_demo` (doion backend). */
export const DEMO_PASSWORD =
  process.env.DEMO_SEED_PASSWORD || "password123";

export const USERS = {
  holder: "holder1",
  investor: "investor1",
  moderator: "moderator1",
  admin: "admin1",
} as const;

export const ROUTES = {
  login: "/login",
  marketplace: "/marketplace",
  moderation: "/moderation",
} as const;

/**
 * Prefer data-testid after AI Studio applies AI_STUDIO_E2E_PREP_PROMPT.md.
 * Fallbacks match current LoginView / Marketplace / ModerationQueue copy.
 */
export const TEST_IDS = {
  loginIdentifier: "login-identifier",
  loginPassword: "login-password",
  loginSubmit: "login-submit",
  mockModeSwitch: "mock-mode-switch",
  marketplacePage: "marketplace-page",
  marketplaceListingCard: "marketplace-listing-card",
  moderationQueuePage: "moderation-queue-page",
  matchesPage: "matches-page",
  matchCard: "match-card",
  matchesTabReceived: "matches-tab-received",
  matchesTabSent: "matches-tab-sent",
  matchesPanelReceived: "matches-panel-received",
  matchesPanelSent: "matches-panel-sent",
} as const;
