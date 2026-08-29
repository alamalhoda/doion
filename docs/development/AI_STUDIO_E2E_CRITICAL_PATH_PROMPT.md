# AI Studio prompt: E2E critical-path selectors

Copy everything under **Prompt** into Google AI Studio so Playwright critical-path specs in `doion/e2e/tests/critical/` can target Live UI reliably.

Do **not** apply these edits from the local Cursor clone of `checkyar-googleai` (one-way sync). After Studio pushes to GitHub, run `git pull` on the local UI clone.

Prerequisite smoke selectors may already exist from [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md). This prompt adds **mutating critical-path** testids only.

---

## Prompt

```text
Context: Active UI repo checkyar-googleai (Bun lockfile only; no package-lock.json).
Live API against doion: VITE_USE_MOCK=false, VITE_API_BASE_URL=http://localhost:8000/api/v1.
Do NOT change backend. Small targeted UI changes only — stable data-testid hooks for Playwright critical-path E2E.
Before coding: list any ambiguities and ask me questions until the instructions are fully clear.

## Symptom
doion Playwright critical specs need stable selectors for:
- express interest form
- accept match confirm
- moderation approve confirm
- listing create (sample fill + submit)
- notifications mark-read
- marketplace / notifications pagination (when total > page size)

## Root cause
Critical flows currently lack dedicated data-testid attributes (or Naive UI NInput puts testid on the wrapper instead of the native input). Smoke login/marketplace testids may already exist; do not remove them.

## Required changes
Use exact kebab-case strings below. Prefer stable wrappers / buttons, not toast nodes.
For Naive NInput: put data-testid via `:input-props="{ 'data-testid': '...' }"` on the native input.

1) Express interest (`src/features/matches/ExpressInterestView.vue` or equivalent route `/matches/express-interest/:listingId`):
- page root → data-testid="express-interest-page"
- message textarea/input → data-testid="express-interest-message" (via input-props if NInput)
- primary submit that opens confirm → data-testid="express-interest-submit"
- ConfirmDialog confirm button → data-testid="express-interest-confirm" (or add prop/slot on shared ConfirmDialog so callers can set it; also support match/moderation confirms below)

2) Matches accept (`src/features/matches/MyMatchesView.vue`):
- Accept button on a pending received card → data-testid="match-accept-btn"
- ConfirmDialog confirm for accept → data-testid="match-accept-confirm"
- When status is accepted, badge/status area on that card → data-testid="match-status-accepted"

3) Moderation queue + review (active routes):
- Queue page: `src/features/moderation/views/ModerationQueue.vue` (`/moderation`)
  - page root already may have data-testid="moderation-queue-page"
  - each queue row → data-testid="moderation-item" (optional data-serial=cheque_serial_number)
  - «بررسی و تصمیم‌گیری» button → data-testid="moderation-review-open"
- Review page: `src/features/moderation/views/ModerationReview.vue` (`/moderation/review/:id`)
  - Approve / «تأیید و انتشار آگهی» → data-testid="moderation-approve-btn"
  - Reject button → data-testid="moderation-reject-btn" (optional)
  - If a ConfirmDialog is used on approve → confirm → data-testid="moderation-approve-confirm"
  - If approve is immediate (no dialog), still add the approve testid on the primary button.

4) Listing create (`src/features/listings/views/ListingCreateWizard.vue` + `src/api/index.ts` / `useListingForm.ts`):
- page root → data-testid="listing-create-page"
- «پر کردن سریع داده‌های نمونه» button → data-testid="listing-fill-sample"
- Final publish / «تأیید و ارسال نهایی» button(s) (wizard step 4 and flat mode) → data-testid="listing-create-submit"
- **Live API gap (required):** `POST /api/v1/listings/` requires `issuer` (IssuerProfile id). Current Live create payload omits it. Before submit: get-or-create IssuerProfile via `/api/v1/issuer-profiles/` from issuer_national_id/name and include `issuer` in createListing body. Do not invent a non-contract field.

5) Notifications (`src/features/notifications/NotificationsView.vue` + NotificationItem):
- page root → data-testid="notifications-page"
- each notification card root → data-testid="notification-item"
- «علامت به عنوان خوانده‌شده» button → data-testid="notification-mark-read"

6) Pagination hooks (when controls render):
- Marketplace pagination wrapper / NPagination root → data-testid="marketplace-pagination"
- Notifications pagination wrapper → data-testid="notifications-pagination"

## Same-class scan
If ConfirmDialog is shared, add an optional `confirmTestId` prop rather than hard-coding one testid for all dialogs. Apply the prop from express / accept / moderation callers.

## Do not
- Commit package-lock.json / use npm as package manager of record
- Unrelated refactors or new dependencies
- Change backend / API contracts
- Invent non-paginated backend APIs
- Push assumptions without asking when contract is unclear

## Acceptance (Live API)
- VITE_USE_MOCK=false; login as holder1 / investor1 / moderator1 (seed_demo users)
- /matches/express-interest/:id shows express-interest-* testids
- /matches pending card: match-accept-btn → confirm → match-status-accepted
- /moderation: open pending row → review → moderation-approve-btn succeeds
- /listings/create: listing-fill-sample then listing-create-submit
- /notifications: notification-mark-read hides unread affordance
- With rich seed_demo (22 published / 12 notifications): marketplace-pagination and notifications-pagination visible; moderation queue lists 12 pending rows
- Mock mode still works for affected flows
- tsc / vitest relevant checks pass
```

---

## After Studio push

```bash
cd /path/to/checkyar-googleai
git fetch origin
git pull origin main
git show --stat <commit-sha>
```

Then from `doion`:

```bash
./e2e/scripts/prepare-backend.sh
# backend runserver with DJANGO_DEMO_DATABASE=1 + UI bun run dev
cd e2e && npm run test:critical
```

## Related

- Runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)
- Seed SSOT: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
- Prior smoke prep: [`AI_STUDIO_E2E_PREP_PROMPT.md`](./AI_STUDIO_E2E_PREP_PROMPT.md)
