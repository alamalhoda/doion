# AI Studio prompt: E2E prep (selectors + demo usernames)

Copy everything under **Prompt** into Google AI Studio so the active UI stays aligned with `doion` `seed_demo` and the Playwright harness in `doion/e2e/`.

Do **not** apply these edits from the local Cursor clone of `checkyar-googleai` (one-way sync). After Studio pushes to GitHub, run `git pull` on the local UI clone.

---

## Prompt

```text
We need small, targeted UI changes so local Playwright smoke tests (in the doion monorepo) can talk to the Live API reliably. Do NOT change product behavior beyond the items below. Keep Bun lockfile; no package-lock.json.

### 0) Critical: stop auto-login mock seed when Live API is on (blocks E2E)

In `src/stores/auth.ts`, `loadSavedUser()` currently invents a demo user + `mock-access-token-1` when `chequeyar_auth_user` is missing. That forces a logged-in marketplace even with `VITE_USE_MOCK=false`, so `/login` is unreachable and Live API calls fail with empty listings.

Required behavior:
- If `VITE_USE_MOCK === 'false'` (or runtime mock mode is off): when there is no saved user/token, leave `user`/`access`/`refresh` as null. Do **not** write mock tokens.
- Keep the demo fallback seed **only** when mock mode is active.
- `logout()` should remain a clean wipe with no re-seed until the next mock-mode init.

### 1) Align moderator demo username with backend seed_demo

In LoginView personas (and any mock user list that uses the same username):
- Change username `mod1` → `moderator1`
- Keep role `moderator` and targetRoute `/moderation`

Backend seed users are: holder1, investor1, moderator1, admin1 (password from seed / DEMO_SEED_PASSWORD; UI demo buttons may still show password123 for local).

### 2) Add stable data-testid attributes

Login (features/auth/LoginView.vue or equivalent):
- identifier NInput → data-testid="login-identifier" (on the input root or native input)
- password NInput → data-testid="login-password"
- submit button → data-testid="login-submit"
- mock mode NSwitch → data-testid="mock-mode-switch"

Marketplace page root (MarketplaceView used by /marketplace):
- outer wrapper → data-testid="marketplace-page"
- each ListingCard root (or list item) → data-testid="marketplace-listing-card"

Moderation queue page:
- outer wrapper → data-testid="moderation-queue-page"

Use the exact testid strings above (kebab-case). Prefer putting them on stable wrappers, not ephemeral toast nodes.

### 3) Live-mode quick-fill buttons

When mock is OFF, the login form already has quick-fill for holder1 and investor1. Also add:
- moderator1 (fills identifier + password123)
- admin1 (fills identifier + password123)

Do not require mock mode for these buttons.

### 4) Constraints

- VITE_USE_MOCK default in .env.example can stay false for real-backend testing docs.
- No unrelated refactors, no new dependencies.
- Commit/push from AI Studio to GitHub as usual.
```

---

## After Studio push

```bash
cd /path/to/checkyar-googleai
git pull
bun install   # if lockfile changed
bun run dev
```

Then re-run `./e2e/scripts/run-smoke.sh` from `doion`. Prefer `getByTestId` paths in `e2e/support/auth.ts` (already implemented with fallbacks).

## Related

- Runbook: [`E2E_LOCAL_RUNBOOK.md`](./E2E_LOCAL_RUNBOOK.md)
- Seed users: [`BACKEND_DEMO_SEED_AND_DATA.md`](./BACKEND_DEMO_SEED_AND_DATA.md)
