# V1 Phase A — AI Studio prompt (critical Live UI blockers)

Paste the fenced block below into Google AI Studio. After push, return to Cursor with: summary + **commit SHA** + docs note + any new `data-testid`s.

One-way rule: do **not** apply these edits from the local Cursor clone of `checkyar-googleai`.

---

## Prompt

```text
Context: Active UI repo checkyar-googleai (Bun lockfile only; no package-lock.json).
Live API against doion: VITE_USE_MOCK=false, VITE_API_BASE_URL=http://localhost:8000/api/v1.
Do NOT change backend. Targeted MVP v1 Live UI fixes only.
Before coding: list any ambiguities and ask me questions until the instructions are fully clear.

## Goal
Close critical Live gaps so holder/investor/moderator/admin flows work against real Django API (not placeholders/toasts-only). Mock UI remains available only when VITE_USE_MOCK=true (already env-gated).

## Symptom / root cause (current HEAD)
1) Routed `/me` (`src/features/profile/ProfileView.vue`) shows profile only — no KYC submit. Full submit lives in orphan `src/views/ProfileView.vue` (not routed).
2) `src/features/moderation/views/KYCReview.vue`: `handleDecision` only shows toast + navigates; never calls `moderationApi.submitKycDecision`. Placeholder name/images.
3) `src/features/moderation/stores/moderationStore.ts` `fetchReviewDetails`: hardcoded mock details; review UI not driven by Live listing/docs.
4) `listingsApi.uploadDocument` in `src/api/index.ts` builds FormData with `document_type` only — **no file bytes**. Call sites pass filename string. Wizard create may not upload after create. (createListing already has issuer get-or-create — keep/ harden that path.)
5) Admin reports may hit non-contract paths; compliance stats/feature-flags/audit are the real APIs.
6) Sayad inquiry is a stub — must be labeled as advisory/stub in UI, not as live inquiry.

## Required changes

### A1 — KYC submit on routed profile
- On active `/me` (or clearly linked child route), add KYC submit form calling `identityApi.createVerification` → `POST /verifications/`.
- Show current status via `GET /verifications/me/` (handle 404 = none).
- Prefer merging useful UX from orphan `src/views/ProfileView.vue` into the routed feature; do not leave submit only on unrouted orphan.
- data-testid (exact):
  - `kyc-submit-page` or section root on profile
  - `kyc-full-name`, `kyc-national-id` via NInput `:input-props`
  - `kyc-submit-btn`

### A2 — KYC moderator review Live
- `KYCReview.vue`: load verification by id from Live API (queue item / `GET` verification detail as available).
- `handleDecision` must call `moderationApi.submitKycDecision` with approve/reject (+ rejection_code/note when reject).
- Remove placeholder name/images when Live data exists; show real fields/docs if API returns them.
- data-testid: `kyc-approve-btn`, `kyc-reject-btn`

### A3 — Moderation listing review Live
- Replace mock `fetchReviewDetails` with Live listing retrieve + documents (use existing listings/moderation APIs; unwrap `{results}` lists correctly).
- Approve/reject already call `submitDecision` — keep; ensure UI uses Live-loaded fields.
- data-testid already may exist from critical prep; keep `moderation-approve-btn`, `moderation-reject-btn`, `moderation-approve-confirm`.

### A4 — Listing documents upload real files
- Change `uploadDocument` to accept a `File` (or Blob) and `formData.append('file', file)` (plus `document_type`) per contract multipart.
- Update wizard / `ListingDocumentUploadView` / any create flow to upload selected files after create.
- Ensure Live create still get-or-creates issuer and sends `issuer` id (`POST /issuer-profiles/` / list filter) — harden error handling if issuer missing (surface user-visible error; do not POST listing without issuer).
- data-testid: keep `listing-create-page`, `listing-fill-sample`, `listing-create-submit`; add `listing-doc-file-input`, `listing-doc-upload-btn` if upload UI is separate.

### A5 — Profile / account consistency
- Routed profile/account show KYC status; listing doc upload path works Live.
- Do not rely on orphan `src/views/*` for MVP routes.

### A6 — Admin reports
- Either wire admin reports only to real compliance endpoints, OR hide/disable `/admin/reports` in router/nav for v1 with a short note in Architecture docs that stats/feature-flags/audit are the supported admin surfaces.

### A7 — Sayad stub labeling
- Where sayad inquiry UI appears, label clearly as stub/advisory (not live bank inquiry).

## Same-class scan
Search for toast-only decisions, hardcoded placehold.co review data, FormData without file, and unrouted views that duplicate Live flows. Fix or route them. Report every extra site.

## Tests (UI repo only)
- Vitest for uploadDocument FormData includes file when Live; KYC decision helper if extracted.
- Run `bun run lint` / `bun run test`; report results.
- Do NOT add Playwright here.
- List every new/changed data-testid kebab-case string.

## Documentation (EN+FA with code)
Update docs/ARCHITECTURE.md + .fa.md and docs/TESTING.md + .fa.md for: KYC Live on /me, Live moderation/KYC review, real document upload, admin surfaces for v1, sayad stub labeling. Mock remains env-gated.

## Do not
- package-lock.json / npm as package manager of record
- Unrelated refactors or new dependencies
- Backend/Django edits
- Invent non-contract endpoints

## Acceptance (Live, VITE_USE_MOCK=false)
- holder1: submit KYC from /me (or see approved status if already verified); create listing with issuer + upload real file bytes
- moderator1: KYC review approve/reject hits API; listing moderation review shows Live data; approve/reject works
- investor1: express interest still works
- admin: stats / feature-flags / audit reachable; reports not lying about fake APIs
- Mock mode (VITE_USE_MOCK=true) still works for affected flows
```
