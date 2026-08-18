# پرامپت G — پذیرش estética پس‌زمینه/باکس sandbox + اصلاحات مقایسه

پیگیری [`06-product-led-ssot-safe.md`](06-product-led-ssot-safe.md) و [`comparison_notes.md`](../comparison_notes.md).

**HEAD UI مبنا:** **`56c9d49`**

**تصمیم کاربر:** پس از مقایسه زنده، estética **پس‌زمینه‌ها (backgrounds)** و **باکس‌ها (boxes/cards)** sandbox را ترجیح داده؛ می‌خواهد علاوه بر اصلاحات لازم، محصول Studio به همان حس بصری نزدیک شود.

**روش:** Studio → pull → (sandbox دیگر به‌روز نمی‌شود؛ فقط مرجع بصری بود)

**مهم:** این پرامپت **توصیف هدف بصری** است — نه دستور کپی فایل از `checkyar-cursor-lab`. معماری Studio (testidها، تست‌های mount، composableها) حفظ شود.

---

```text
You are continuing the Cheque Yar public landing page (Vue 3 + Pinia + Tailwind).

Base commit: 56c9d49 (prompts 01–06 complete).

## Goal

The product owner compared Route A (this repo) with a sandbox build and prefers the **background atmosphere** and **box/card surfaces** from the sandbox — while keeping this repo's behavior, SSOT copy, testids, and test coverage.

Apply a **visual-only** pass to match the sandbox feel described below. Do NOT copy files from another repo.

## Hard constraints (unchanged)

1. No locked copy changes (§2.5, §2.6, FAQ, pricing disclaimer, form success, CTA labels/routes).
2. No section reorder. No behavior/API/routing changes.
3. Keep ALL existing `data-testid` values exactly (including `landing-step-*`, `landing-listings-grid`, field testids on contact/lead inputs).
4. Dark emerald brand only — no blue/gold identity, no `animate-pulse`, no LTR arrows.
5. All existing vitest must pass; you may add tests only for new optional `landingContent` keys if needed.
6. No new npm dependencies.

## Part A — Background system (sandbox feel)

Update `src/features/landing/styles/landingDecor.css` and `LandingDecorLayer.vue`:

### A1. Neutral pattern tint (not emerald-green dots)

Sandbox uses **slate-neutral** grid/dots (readable depth, not “green wallpaper”):

- Dots: `radial-gradient` with slate ~`#94a3b8` at 1px, size ~22px
- Grid: slate 1px lines, size ~32px
- Stripes: subtle `-45deg` slate stripes at very low opacity

Keep mesh **emerald** but use **elliptical** radial gradients (3 blobs: top-right, bottom-left, center) with tunable opacity via CSS variables on `.landing-decor`:

```css
.landing-decor {
  --landing-dots-opacity: 0.06;
  --landing-grid-opacity: 0.04;
  --landing-stripes-opacity: 0.03;
  --landing-mesh-opacity: 0.22;
}
.landing-decor-intensity-low { /* lower values */ }
.landing-decor-intensity-medium { /* medium values */ }
```

Apply intensity class on the decor wrapper, not scattered Tailwind opacity on each section.

### A2. Pattern + overlay stacking

Extend `LandingDecorLayer` with optional **`overlay`** prop (`dots` | `grid` | `stripes` | `none`) in addition to `pattern`, so a section can render e.g. `mesh` + `dots` together (sandbox Hero and several sections use layered backgrounds).

Keep existing `vector` support; do not remove it.

### A3. Section decor tuning (match sandbox rhythm)

Re-tune per-section decor props for **more visible but still subtle** depth (medium intensity where sandbox used it):

| Section | Target |
|---------|--------|
| Hero | mesh + dots overlay, medium; corner stripe accent; keep static SVG vectors |
| Problem/Solution | mesh low + dots overlay |
| How it works | grid low |
| Audiences | stripes low + glass cards |
| Live listings | mesh bottom-left, medium-low |
| Responsibility | mesh medium + shield vector |
| Product status | glass + gradient border |
| Pricing | dots medium |
| FAQ | dots low |
| Contact / Lead | grid low behind form panel |
| Investing | mesh low + growth vector |

Do not add new sections. Only adjust decor props and CSS — not copy.

### A4. Hero atmosphere

Hero should feel **deeper** than inner sections:

- Layered decor (mesh + dots + optional corner stripe block)
- Optional very faint noise (`feTurbulence` SVG filter at opacity ≤ 0.04) — static, no animation
- Keep real listings preview component; do not revert to schematic mock

## Part B — Box / card surfaces (sandbox feel)

Update `LandingSurfaceCard.vue` and listing/FAQ/form surfaces:

### B1. Glass recipe

Use `color-mix(in srgb, var(--theme-surface) 60%, transparent)` (or equivalent) for `.landing-glass-card` so glass feels **lighter and more layered** than flat `rgba(15,23,42,0.65)`.

Default border on glass: `border-white/5` or `/10` — subtle rim light.

### B2. Gradient border (sandbox style)

Replace or supplement current padding-box gradient borders with a **pseudo-element** approach:

- `.landing-gradient-border::after` — 1px emerald gradient edge (RTL-friendly: stronger on the right/start side in RTL)
- Optional `.landing-gradient-border-hover` — gradient edge fades in on hover (for listing cards)

Keep existing `gradientBorder` prop API; implementation may change internally.

### B3. Card structure

- `accentTop`: 3px bar `bg-gradient-to-l from-emerald-500 via-emerald-400/80 to-transparent` (RTL accent)
- Inner content padding in a nested wrapper so accent bar spans full width (sandbox pattern)
- Hover: keep `-translate-y-[3px]` + emerald border; add slightly stronger shadow on hover (`shadow-[0_16px_32px_-8px_rgba(0,0,0,0.35)]`)

### B4. Listing cards

Apply sandbox-like box treatment to `LandingListingCard.vue`:

- Glass base + optional gradient-border on hover
- Clear rim (`border-white/10`)
- Do NOT change click routing or card data fields

### B5. Trust strip + form panels

- Trust strip: glass band `bg-[var(--theme-surface)]/50` + `backdrop-blur-md` + `border-y border-white/5`
- Contact/Lead: glass `LandingSurfaceCard` with `accentTop` + grid decor behind section

## Part C — Fixes from comparison (required in same commit)

1. **Trust strip text color:** replace any `--theme-text` with `--theme-text-primary`.
2. **Hero preview strings:** move hardcoded «تابلوی زنده آگهی‌ها» / «مشاهده همه» / error line into `landingContent.hero` (or `landingContent.visual`) + SSOT tests. Keep locked strings untouched.
3. **How it works timeline:** on `lg+`, six steps in **one horizontal row** with dashed connector line (RTL 1→6). Below `lg`, vertical spine on the right. Keep `data-testid="landing-step-${n}"` (do NOT rename to `landing-how-it-works-step-*`).
4. **Step numbers:** keep `toPersianDigits()` on step badges (Studio strength — do not regress to Latin digits).

## Part D — Documentation

Update `docs/ARCHITECTURE.md` / `.fa.md` — note sandbox-aligned decor tuning (neutral patterns + layered overlay + pseudo gradient borders). Reference `docs/design-system.md`.

## Explicitly OUT OF SCOPE

- Copying sandbox file paths or repo structure (`landingVisualClasses.ts` rename is optional only if it reduces duplication without breaking imports)
- Changing testid contract
- Reordering sections
- New features or copy rewrites

## Verification

- `bun run lint` — 0 errors
- `bun run test` — all pass (≥145 tests)
- Visual: backgrounds feel deeper/neutral; cards feel glassy with subtle gradient edges; Hero + listing cards clearly improved vs 56c9d49
- 360px: no horizontal scroll

Reply with commit SHA and a short note: which CSS variables changed, and one before/after description of Hero + one listing card.
```
