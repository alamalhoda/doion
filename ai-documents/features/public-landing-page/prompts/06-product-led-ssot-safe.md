# پرامپت F — محصول‌محور در چارچوب SSOT (Hero داده‌ای، نوار اعتماد، timeline، کارت غنی‌تر)

پیگیری [`05-modern-decor-layer.md`](05-modern-decor-layer.md). HEAD UI مبنا: **`9c19d9e`**.

**هدف:** حس «محصول آماده با داده واقعی» بدون نقض `feature_spec.md` یا `docs/design-system.md`. این پرامپت فقط بخش **اجرایی و سازگار** پیشنهاد خارجی را پیاده می‌کند؛ بخش‌های نیازمند amendment spec عمداً **حذف** شده‌اند (فهرست Out of Scope پایین پرامپت).

**روش:** Studio → pull → sandbox (پس از ۰۱–۰۵).

---

```text
You are continuing the Cheque Yar public landing page (Vue 3 + Pinia + Tailwind).

Base commit: 9c19d9e (prompts 01–05 complete).

## Goal

Make the landing feel more **product-led** (trust + live data + action) while staying strictly inside:
- `feature_spec.md` (section order, locked copy, CTA routes, data-testid contract)
- `docs/design-system.md` (dark emerald brand — NOT blue primary, NOT gold/amber as identity, cards on dark surfaces, Vazirmatn)

This is presentation + light data UX only. No backend/API changes.

## Hard constraints (non-negotiable)

1. **Section order unchanged** (spec §2.3): Hero → Problem/Solution → How it works → Audiences → Live listings → Responsibility boundary → Product status → Pricing → FAQ → Contact → Lead capture → Investing → Footer. Do NOT reorder sections.

2. **Locked copy unchanged** in `landingContent.ts`: hero one-liner, pilot badge (§2.6), responsibility §2.5 statements + closing, FAQ Q&A, pricing disclaimer, form success messages, live-listings empty/error strings. Do NOT replace hero headline/one-liner with shorter marketing copy. Do NOT change CTA labels/routes (spec §2.4): guest primary → `/register`, secondary → `/login`, tertiary → `/login`; authenticated primary → `/marketplace`, secondary scroll → `#live-listings`.

3. **Design system palette:** `--theme-*` + emerald accent only for identity/CTA. No `#2E90FA` blue primary buttons. No gold/amber chips for rates (emerald for rate chip). No white `#F8FAFC` card surfaces on the dark landing. Keep `data-theme="dark"`.

4. **Regulatory visibility:** §2.5 full section stays on the page verbatim. A new trust strip is a **scannable summary**, not a replacement — link to `#responsibility-boundary`.

5. **No invented data or fake UI:** No “مبلغ دریافتی تقریبی” (not in API). No non-functional filter bars that look clickable (no fake marketplace filters). No bank logo CDN images. No stock photos. Hero preview uses **real** `marketplaceApi.getLatestListings()` data only (or empty/loading states — never fabricated listing rows).

6. **No misleading status claims:** For listing status chips use existing `LISTING_STATUS_LABELS` from `src/types/api.ts` (e.g. `published` → «منتشر شده»). Do NOT invent labels like «بررسی اولیه‌شده» unless that exact string already exists in SSOT.

7. **Keep all existing `data-testid` values.** Add new ones only where noted below.

8. No `animate-pulse`, no infinite animations, no LTR arrows (`←`, `&larr;`, external-link icons pointing wrong for RTL). Short transitions (≤300ms) on hover/accordion OK.

9. Do not touch backend, router guards, simulator seeds, or `package-lock.json` / lockfile unless `@vue/test-utils` already present — do not add new npm dependencies.

## What to build

### 1. Shared listings fetch (SSOT — single network call)

Create `src/features/landing/composables/useLandingLatestListings.ts`:

- Calls `marketplaceApi.getLatestListings()` once, slices to max 4.
- Exposes `{ listings, isLoading, hasError, refetch }` as shared reactive state (module-level singleton or pinia-less shared ref so Hero + LiveListingsSection share one fetch).
- Refactor `LiveListingsSection.vue` to use this composable instead of local fetch.

Add vitest for composable error/empty/slice behavior (mock `marketplaceApi`).

### 2. Hero — real marketplace preview (replace schematic mock)

Update `HeroSection.vue`:

- **Remove** the abstract schematic placeholder blocks (fake bars, `chequeyar.ir/preview` window chrome). Replace right column (left in RTL on lg) with **`LandingHeroListingsPreview.vue`** showing up to **2** real listing cards (compact layout) from `useLandingLatestListings`.
- Keep left column (right in RTL): existing brand mark, **locked** pilot badge text, **locked** headline/one-liner/description, existing CTAs unchanged.
- Preview states:
  - Loading: static skeleton (no pulse), same glass styling
  - Data: 1–2 compact cards (reuse formatting from `LandingListingCard` or extract shared subcomponent)
  - Empty: short message from new `landingContent.hero.previewEmpty` key (non-regulatory, e.g. «فعلاً آگهی منتشرشده‌ای برای پیش‌نمایش نیست») + text link/button «مشاهده بخش آگهی‌ها» scrolling to `#live-listings` — no fake listings
  - Error: do not show fake data; optional one-line + rely on full section below
- Compact cards in hero: **display-only** (not separate click targets) OR single wrapped link to `#live-listings` — must NOT call `getListingDetail` or route to `/listings/:id` from hero preview (guest safety unchanged in main section cards).
- Add `data-testid="landing-hero-listings-preview"` on preview root.
- Optional caption from `landingContent.visual.heroPreviewCaption` → change to «پیش‌نمایش آگهی‌های منتشرشده» (update test in `landingContent.test.ts`).

Keep existing decor layers (mesh/dots/grid/SVG) unless they clutter the preview; reduce if needed.

### 3. Trust strip (new band — between Hero and Problem/Solution)

Create `LandingTrustStrip.vue` and mount it in `LandingView.vue` **immediately after** `<HeroSection />`, before `<ProblemSolutionSection />`.

- Full-width subtle band (`bg-[var(--theme-surface)]/50`, glass, border-y) with 4 scannable items.
- Copy in `landingContent.trustStrip.items` — **short paraphrases aligned with §2.5**, e.g.:
  - «بدون جابه‌جایی وجه»
  - «بدون نگهداری چک»
  - «بدون ضمانت وصول»
  - «نرخ پیشنهادی غیرالزام‌آور»
- Each item: small emerald outline icon + label (use `LandingIconBadge` or inline SVG).
- End of strip: link «جزئیات مسئولیت‌ها» → smooth scroll `#responsibility-boundary` (not tooltip-only).
- `data-testid="landing-trust-strip"`; items `landing-trust-item-1` … `landing-trust-item-4`; link `landing-trust-details-link`.
- Vitest for trust strip copy keys.

This does NOT remove or shorten `ResponsibilityBoundarySection`.

### 4. How it works — timeline layout

Refactor `HowItWorksSection.vue` presentation:

- **Desktop (lg+):** horizontal timeline — 6 steps in one row with connecting line (CSS/SVG, dashed emerald, RTL flow 1→6).
- **Mobile:** vertical timeline with line on the right (RTL).
- Same step titles/descriptions from `landingContent.howItWorks.steps`; step 6 keeps `directSettlementTag` and stronger visual emphasis (`highlight` + glass) — **no** “external link” icon.
- Remove the weak inline dashed span hack from prompt 05 if timeline replaces it.
- `data-testid` on section unchanged; optional `landing-how-it-works-step-${n}` on each step node (additive only).

### 5. Richer listing cards (Live Listings section)

Enhance `LandingListingCard.vue` (main section cards — keep click behavior):

- **Rate chip:** prominent pill when `suggested_discount_rate` present (emerald soft bg, tabular nums + `%`).
- **Days to due:** compact badge (static text, e.g. «۱۵ روز تا سررسید») — no animated progress ring.
- **Issuer masking:** pure helper `maskDisplayName(name: string): string` in `src/features/landing/utils/maskDisplayName.ts` — show first word + «…» or «شرکت …» pattern for long names; vitest edge cases (empty, short, single word).
- **Status chip:** when `listing.status === 'published'`, show `LISTING_STATUS_LABELS.published` (import from types); hide chip for other statuses if they ever appear.
- **Typography:** `tabular-nums` on amount and rate; amount remains **face amount in Toman** (label «مبلغ اسمی چک» — do NOT add received/net amount).
- **Bank row:** optional simple typographic “icon” (first letter in rounded square using theme tokens — not a real bank logo).

Guest click → `/login`; auth → `/listings/:id` unchanged.

### 6. Problem / Solution — light visual contrast (optional but requested)

In `ProblemSolutionSection.vue`, add static line-based SVG decor per column (muted friction lines vs emerald connection nodes) — `aria-hidden`, no copy changes. Keeps two `LandingSurfaceCard` columns.

### 7. Documentation

Update `docs/ARCHITECTURE.md` / `.fa.md`: composable `useLandingLatestListings`, trust strip, hero preview, timeline, `maskDisplayName`.

## Explicitly OUT OF SCOPE (do not implement)

- Reordering sections (e.g. moving live listings above problem/solution)
- New hero marketing headline or CTA labels («درخواست ورود به پایلوت», etc.)
- Blue/cyan primary palette or light/white card theme
- Hiding §2.5 behind tooltip only
- Fake marketplace filter UI
- «مبلغ دریافتی تقریبی» or new financial calculations
- Mobile sticky bottom CTA bar
- Changing locked pilot badge to «پذیرش محدود…» only (full §2.6 sentence stays on badge)
- Bank logo assets / CDN images

## Verification

- `bun run lint` — 0 errors
- `bun run test` — all pass + new tests for composable, maskDisplayName, trustStrip keys
- Manual: guest hero CTAs unchanged; guest listing card in **#live-listings** still → `/login`; only one `getLatestListings` network call on page load (verify in Network tab or mock spy in test)
- 360px: no horizontal scroll
- Locked string vitests in `landingContent.test.ts` still pass unchanged

Reply with commit SHA and note: hero preview data source, trust strip placement, timeline breakpoint.
```
