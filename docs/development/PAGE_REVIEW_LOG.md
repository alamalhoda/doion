# Page Review Log

**As of:** 2026-08-18  
**Scope:** Product UI flows in active repo [`checkyar-googleai`](https://github.com/alamalhoda/checkyar-googleai) (Google AI Studio → GitHub). Backend/API notes reference this monorepo.

## Status legend

| Status | Meaning |
|--------|---------|
| **Ready (pilot)** | Meets v1 Layer 1 spec; usable in controlled pilot with known non-blockers |
| **In progress** | Partially implemented or under active Studio prompts |
| **Blocked** | Missing backend contract, flag, or E2E contract |
| **Deferred** | Out of v1 Layer 1 scope |

## Summary

| Page / route | Feature module | Status | UI HEAD (Studio) | E2E | Notes |
|--------------|----------------|--------|------------------|-----|-------|
| Public landing | `src/features/landing/` | **Ready (pilot)** | `d518d20` | `e2e/tests/smoke/landing-guest.spec.ts` (4 tests, Live API) | Gated by `show_landing_page` (default **off** in backend seed) |
| Login / Register | `src/features/auth/` | Ready (pilot) | (prior Phase A) | smoke login specs | Unchanged by landing feature |
| Marketplace | `src/features/marketplace/` | Ready (pilot) | (prior Phase A) | smoke + critical | Guest redirect when landing flag off |
| Matches | `src/features/matches/` | Ready (pilot) | (prior Phase A) | smoke + critical | — |
| Moderation | `src/features/moderation/` | Ready (pilot) | (prior Phase A) | smoke + critical | — |
| Admin (stats / flags / audit) | `src/features/admin/` | Ready (pilot) | (prior Phase A) | `admin-surfaces.spec.ts` | Flag toggle for landing |
| Listings (create / my / detail) | `src/features/listings/` | Ready (pilot) | (prior Phase A) | smoke + critical | — |

Spec SSOT for landing: [`ai-documents/features/public-landing-page/feature_spec.md`](../../ai-documents/features/public-landing-page/feature_spec.md).

---

## Public landing page (`/`, `/landing`)

**Last reviewed:** 2026-08-18  
**Status:** **Ready (pilot)** — feature-complete per spec; production visibility controlled by feature flag.

### Routes & gating

| Route | When `show_landing_page` is **on** | When **off** (fail-closed) |
|-------|-----------------------------------|----------------------------|
| `/` | Redirect → `/landing` | Redirect → `/marketplace` → auth → `/login` (guest) |
| `/landing` | Public landing (guest + signed-in) | Redirect → `/marketplace` → `/login` (guest) |

- Flag key: `show_landing_page`
- Backend seed: `post_migrate` → `seed_default_feature_flags` (`is_enabled=false` by default) — PR #31, merged to `develop`
- Mock simulator: flag seeded **on** in `seedFeatureFlags` for demo convenience
- Toggle at runtime: `/admin/feature-flags` (admin/moderator) or `PATCH /api/v1/compliance/feature-flags/show_landing_page/`

### Content & sections (13 blocks)

Hero (+ trust strip), problem/solution, how it works, audiences, live listings (API), responsibility boundary, product status, pricing placeholder, FAQ, contact (UI-only), lead capture (UI-only), investing CTA, footer — order locked in spec §2.3.

### Data & API usage (no new endpoints)

| Need | Existing API |
|------|----------------|
| Feature flag | `GET /api/v1/compliance/feature-flags/` (AllowAny read) |
| Live listings (max 4) | `GET /api/v1/marketplace/listings/latest/` |
| Risk tier badge (optional) | Gated by `show_risk_tier` (unchanged) |

**Docs impact (API):** `MASTER_API_CONTRACT.md` updated only for **seed record** `show_landing_page` — no new endpoints, serializers, or permission changes.

### UI delivery (Studio chain)

| Prompt | Commit | Notes |
|--------|--------|-------|
| 01 skeleton | `86ee6e3` | Routing, flag gate, chrome, testids |
| 02 content | `746cea6` | SSOT copy, 12 sections |
| 03 live data/forms | `6358a0c` | Listings, contact/lead forms |
| 04 visual polish | `a8250bd` | Section shell, primitives |
| 05 modern decor | `9c19d9e` | Decor layer, glass, vectors |
| 06 product-led | `56c9d49` | Trust strip, hero preview, timeline |
| 07 sandbox visual | **`d518d20`** | Neutral backgrounds, card surfaces, SSOT fixes |

Architecture docs: updated in UI repo via Studio (`docs/ARCHITECTURE.md`, `.fa.md`) — not edited locally in `doion`.

### E2E (doion)

- Spec: `e2e/tests/smoke/landing-guest.spec.ts`
- Helpers: `e2e/support/landing.ts`
- Requires **Live API UI** (`VITE_USE_MOCK=false`); mock always enables landing flag
- CI UI pin: `d518d20` in `.github/workflows/ci-e2e.yml`

### Known non-blockers

- How-it-works timeline on desktop: 3×2 grid with chevron flow (sandbox used 1×6 row) — optional Studio follow-up
- One flaky unit test timeout in `LandingHeroListingsPreview.test.ts` (Studio vitest)

### PR checklist snippet

```text
Docs updated:
- docs/development/PAGE_REVIEW_LOG.md (this entry)
- docs/development/E2E_LOCAL_RUNBOOK.md (landing smoke row)
- ai-documents/features/public-landing-page/implementation_plan.md (Step 8–9)

Docs impact (API): none beyond existing show_landing_page seed row in MASTER_API_CONTRACT.md (PR #31).
```
