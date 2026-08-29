# پرامپت D — ارتقای ظاهر حرفه‌ای (Visual Polish)

پیگیری پرامپت‌های ۰۱–۰۳. HEAD UI مبنا: **`6358a0c`**.

**هدف:** صفحه Landing از نظر بصری حرفه‌ای‌تر، عمیق‌تر و هم‌تراز با `docs/design-system.md` شود — **بدون** تغییر رفتار، routing، فرم‌ها، API، یا متن‌های رگولاتوری قفل‌شده.

این پرامپت **فقط** لایه بصری است. مقایسه پرامپت‌های ۰۱–۰۳ بین Studio و sandbox سالم می‌ماند.

---

```text
You are continuing the Cheque Yar public landing page in the Vue 3 + Pinia + Tailwind repo.

Base commit: 6358a0c (prompts 01–03 are complete and accepted).

## Goal

The landing page works but looks too plain — repetitive sections, flat cards, small body text, minimal hierarchy. Upgrade the **visual polish** to a professional fintech-marketplace feel aligned with `docs/design-system.md` (brand theme `dark`, emerald accent, RTL Persian).

This is a **presentation-only** pass. Do not rewrite business logic.

## Hard constraints (do not violate)

1. **No copy changes** to locked regulatory strings in `landingContent.ts` (§2.5 responsibility boundary statements + closing sentence, §2.6 product status sentence, §2.8 FAQ Q&A verbatim, pricing disclaimer, lead/contact success messages, live-listings empty/error copy). You MAY add new optional visual-only strings under `landingContent.visual` (section eyebrows, decorative labels) — never rewrite existing keys.

2. **No behavior changes:** routing, CTA handlers, form validation, fetch logic, feature flags, auth gating, scroll targets, `data-testid` values, section order, and section IDs stay identical.

3. **Design system only:** use `--theme-*` tokens + emerald accent (`#10b981`, `#34d399`, soft rgba borders). Do NOT use `amber-*`, `rose-*`, `indigo-*` as section identity colors. Do NOT use `animate-pulse` or looping decorative animations. Do NOT add LTR arrows (`←`, `&larr;`, `→`).

4. **No new product sections** and no invented capabilities in copy. No stock photos, bank icons, vault imagery, or crypto/neon aesthetics.

5. **Keep all existing `data-testid` attributes** unchanged (including `landing-section-*`, `landing-hero-*`, `landing-faq-item-*`, `landing-listing-card-*`, form testids, header/footer nav testids).

6. **Do not touch** `package-lock.json`, backend, router guard logic, or `useBackendSimulatorStore` seed values.

7. Primary buttons on emerald background should use dark text (`#020617` or `#022c22`) per design-system §4 contrast rules.

## What to build

### 1. Shared layout primitives (DRY visual shell)

Create reusable components under `src/features/landing/components/`:

**`LandingSectionShell.vue`**
- Props: `id`, `testId` (maps to `data-testid`), `title`, `subtitle`, optional `eyebrow`, optional `variant: 'default' | 'muted' | 'elevated'`, optional `narrow` (max-w-4xl for FAQ/forms).
- Consistent vertical rhythm: `py-20 sm:py-24`, `scroll-mt-16` where anchors exist today.
- Unified section header: eyebrow pill (if provided) → h2 → subtitle, centered unless a section needs left-aligned (none required now).
- Background variants using tokens only:
  - `default`: `--theme-bg`
  - `muted`: `--theme-surface`
  - `elevated`: `--theme-bg` with subtle top/bottom gradient separators instead of harsh `border-b` everywhere
- Replace duplicated header markup in section files with this shell (keep section-specific content inside the default slot).

**`LandingSurfaceCard.vue`**
- Props: `highlight?: boolean` (emerald border emphasis for “solution” cards), `hoverable?: boolean`.
- Base: `rounded-2xl border bg-[var(--theme-surface)] p-6 sm:p-8`.
- Default border: `--theme-border`. Highlight: `border-emerald-500/30` + soft shadow `shadow-[0_12px_28px_-6px_rgba(0,0,0,0.25)]`.
- If `hoverable`: `transition duration-[250ms] ease-[cubic-bezier(0.4,0,0.2,1)] hover:-translate-y-[3px] hover:border-emerald-500/40` (design-system §5 motion).

**`LandingIconBadge.vue`**
- Small outline-style SVG icon inside `h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400` — used for list bullets and step headers instead of raw `&bull;`, `&times;`, `&check;` characters.

Refactor existing sections to compose these primitives. Logic stays in section files; templates get cleaner.

### 2. Hero — stronger first impression

Upgrade `HeroSection.vue` per design-system brand mark + §7.4 accent bar:

- **Two-column layout on `lg+`:** text/CTA column (right in RTL) + decorative product preview panel (left in RTL).
- **Brand mark:** 48×48 (`w-12 h-12`), rounded-2xl, letter «چک» (not just «چ») above or beside headline per design-system §1.
- **RTL accent bar:** 3–4px vertical emerald bar on the **right** edge of the hero content block (not a full-width gradient wallpaper).
- **Background:** keep subtle emerald glow but add a very faint grid/dot pattern using CSS (opacity ≤ 0.04, no animation) — must not hurt readability or cause horizontal scroll at 360px.
- **Decorative preview panel (static, no real data):** a stacked/card mock showing abstract marketplace UI blocks built only from theme tokens (placeholder bars, fake amount line, fake date line). Label it visually as preview/decorative only — do NOT wire to API or simulator. No listing IDs, no clickable cards, no fake rates that look like live data. Optional small caption from `landingContent.visual.heroPreviewCaption` e.g. «نمای شماتیک رابط بازارچه».
- **Typography:** headline scales per design-system (up to ~44px on md). Body at least `text-base` with `leading-[1.7]`.
- CTAs unchanged functionally; restyle primary button with `shadow-[0_10px_24px_-8px_rgba(16,185,129,0.45)]` and dark text on emerald.

### 3. Section rhythm across the page

Apply `LandingSectionShell` to all content sections. Alternate `variant` thoughtfully so the long scroll is not monotonous:

| Section | Suggested variant | Notes |
|---------|-------------------|-------|
| Hero | custom (not shell) | full-bleed |
| Problem/Solution | muted | two `LandingSurfaceCard`, solution `highlight` |
| How it works | default | 6 step cards, hoverable |
| Audiences | muted | two audience cards, hoverable |
| Live listings | default | polish grid spacing; do not break loading/empty/error states |
| Responsibility boundary | elevated | regulatory prominence — keep 4 statement texts verbatim |
| Product status | muted | status card with accent top bar |
| Pricing | default | placeholder cards |
| FAQ | narrow + muted | accordion polish |
| Contact + Lead | default/muted | form panels |
| Investing | muted | CTA block |

Replace most `border-b border-[var(--theme-border)]` section dividers with shell-managed spacing/gradients.

### 4. How it works — visual flow

- Wrap each step in `LandingSurfaceCard` hoverable.
- Step number in `LandingIconBadge` or enlarged pill.
- On `lg+` only: optional subtle dashed connector between steps in reading order (RTL: 1→2→3 top row, 4→5→6 bottom row). CSS/SVG only, no JS animation.
- Step 6 keeps `directSettlementTag` behavior and text.

### 5. Lists and cards

- Problem/Solution/Audiences bullet lists: replace character bullets with `LandingIconBadge` + small check/cross/minus SVG (semantic: problem=muted cross, solution=emerald check, audience=emerald dot/check).
- Listing cards (`LandingListingCard.vue`): add subtle card shadow, clearer typographic hierarchy for amount (larger tabular Persian digits), due date row, rate row — **no logic changes**.
- Responsibility boundary cards: keep verbatim text; improve icon badge consistency.

### 6. Header & footer polish

**`LandingHeader.vue`:**
- Brand lockup: 40×40 mark with «چک», tagline 11px muted per design-system §1.
- Sticky header: add subtle bottom shadow `shadow-[0_4px_24px_-4px_rgba(0,0,0,0.35)]` when scrolled OR always-on very subtle shadow — pick one, keep performant.
- Nav links: active-hover underline or bottom border on hover using emerald (no route change).

**`LandingFooter.vue`:**
- Improve column spacing and link hover states.
- Keep dynamic Jalali year and locked footer copy sources.

### 7. FAQ accordion polish

- Closed: neutral surface card.
- Open: `border-emerald-500/30`, answer area with slightly muted background `--theme-surface-muted`, smooth height transition OK (`transition-all` on max-height or grid — no pulse).
- Chevron rotation stays; ensure keyboard/a11y unchanged.

### 8. Form panels (Contact + Lead)

- Wrap forms in elevated `LandingSurfaceCard` with top emerald accent bar (3px).
- Inputs: consistent `min-h-[44px]`, `rounded-lg`, `bg-[var(--theme-input)]` if defined else `--theme-bg`, border `--theme-border`, focus `ring-2 ring-emerald-500/50`.
- Error text styling consistent; validation logic untouched.

### 9. Optional visual SSOT

Add to `landingContent.ts`:

```ts
visual: {
  heroPreviewCaption: '...', // schematic UI caption
  sectionEyebrows: {
    howItWorks: '...',
    audiences: '...',
    // only where it helps hierarchy; Persian, short, non-regulatory
  }
}
```

Add/adjust tests in `landingContent.test.ts` for new keys only. Locked string tests must still pass unchanged.

### 10. Documentation

Update `docs/ARCHITECTURE.md` and `docs/ARCHITECTURE.fa.md` with a short subsection: landing visual primitives (`LandingSectionShell`, cards, icon badge), note that prompt 04 is presentation-only.

Do NOT create parallel design docs — reference existing `docs/design-system.md`.

## Files likely touched

- `src/features/landing/components/*.vue` (new)
- `src/features/landing/sections/*.vue` (visual refactor)
- `src/features/landing/LandingHeader.vue`, `LandingFooter.vue`, `LandingView.vue` (minimal)
- `src/features/landing/content/landingContent.ts` + test
- `docs/ARCHITECTURE.md`, `docs/ARCHITECTURE.fa.md`

## Verification

- `bun run lint` (tsc --noEmit) — 0 errors
- `bun run test` — all existing tests pass; add tests only for new `landingContent.visual` keys if added
- Manual: 360px width — no horizontal scroll
- All prior Playwright-critical flows unchanged: guest hero CTAs, guest listing card → `/login`, signed-in listing → `/listings/:id`, FAQ accordion, form validation toasts, feature flag gates

Reply with commit SHA and a brief list of visual changes (not a feature list).
```
