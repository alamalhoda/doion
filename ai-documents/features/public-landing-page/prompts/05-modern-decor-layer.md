# پرامپت E — لایه بصری مدرن (گرادیانت، الگو، شیشه، وکتور)

پیگیری [`04-visual-polish.md`](04-visual-polish.md). HEAD UI مبنا: **`a8250bd`**.

**بازخورد کاربر:** پس از پرامپت ۰۴ هنوز صفحه ساده به نظر می‌رسد؛ می‌خواهد المان‌های مدرن‌تر: گرادیانت، پس‌زمینه نقطه‌ای/راه‌راه، شفافیت (glass)، و وکتور.

**روش:** همان مسیر Studio → pull → sandbox (پس از ۰۱–۰۳ + ۰۴).

**تعادل با design-system §2:** «از گرادیان شلوغ، شیشهٔ افراطی پرهیز» — یعنی **لایه‌بندی ظریف و کنترل‌شده**، نه پس‌زمینه رنگین‌کمانی یا glass روی کل صفحه.

---

```text
You are continuing the Cheque Yar public landing page (Vue 3 + Pinia + Tailwind).

Base commit: a8250bd (prompt 04 visual polish is complete).

## Goal

The landing page still feels visually flat. Add a **modern, layered aesthetic** using controlled gradients, dot/grid/stripe patterns, glass surfaces, and inline SVG vector decor — while staying inside `docs/design-system.md` (dark emerald brand, trustworthy fintech-marketplace, NOT crypto/neon/bank luxury).

This is **presentation-only**. Do not rewrite business logic, copy locks, routing, forms, or API behavior.

## Hard constraints (unchanged from prompt 04)

1. **No changes** to locked regulatory strings in `landingContent.ts` (§2.5, §2.6, §2.8 FAQ verbatim, pricing disclaimer, form success messages, live-listings empty/error copy). You MAY extend `landingContent.visual` with new decorative-only keys if needed.

2. **No behavior changes:** routing, CTA handlers, validation, fetch, feature flags, auth, scroll targets, section order/IDs, and all existing `data-testid` values stay identical.

3. **Brand palette only:** `--theme-*` tokens + emerald accent family. No `amber-*`, `indigo-*` as section identity. `rose-*` only for form validation errors (already present). No `animate-pulse`, no infinite CSS animations, no LTR arrows.

4. **No stock photos, no bank/vault/currency icons, no 3D illustrations, no external image/CDN assets.** All decor must be CSS and inline SVG in the repo.

5. **Readability & performance:** text contrast must remain AA-friendly on dark surfaces. Decorative layers use `pointer-events-none`, `aria-hidden="true"`, and must not cause horizontal scroll at **360px**.

6. Do not touch `package-lock.json`, backend, router guards, or simulator seeds.

## Design direction (what “modern” means here)

Think: **depth through layers**, not clutter.

Allowed techniques (use several, not all at max intensity on every section):

| Technique | Rules |
|-----------|--------|
| **Mesh / radial gradients** | Emerald → transparent on `#020617`; opacity ≤ 0.25; max 2–3 blobs per section |
| **Dot pattern** | `radial-gradient` dots; opacity ≤ 0.06 |
| **Grid pattern** | 1px lines; opacity ≤ 0.04 |
| **Diagonal stripes** | Very subtle (`repeating-linear-gradient`); opacity ≤ 0.03; alternate sections only |
| **Glass surfaces** | `bg-[var(--theme-surface)]/60` + `backdrop-blur-md` + border `white/5` or `--theme-border`; use on cards/panels, NOT full-page overlay |
| **Inline SVG vectors** | Abstract geometric shapes (circles, arcs, connection lines, chevrons in RTL flow); stroke emerald at low opacity; no illustrative money/check art |
| **Gradient borders** | `border` + pseudo-element or `bg-gradient-to-r` on 1–2px accent edges |
| **Noise texture (optional)** | Tiny SVG feTurbulence or CSS noise at ≤ 0.03 opacity — hero only |

Forbidden: rainbow gradients, purple/pink neon, gold, heavy glass blur on entire viewport, parallax JS, animated particles, gradient text on body copy.

## What to build

### 1. Central decor system (SSOT for backgrounds)

Create `src/features/landing/styles/landingDecor.css` (import once from `LandingView.vue`):

Define reusable utility classes, e.g.:

- `.landing-bg-dots` — dot grid
- `.landing-bg-grid` — line grid
- `.landing-bg-stripes` — diagonal stripes
- `.landing-bg-mesh-emerald` — layered radial emerald glows (static)
- `.landing-glass-card` — glass surface recipe (background alpha + blur + border)
- `.landing-gradient-border` — subtle emerald gradient edge

Use CSS variables for opacity so tuning is one place. **No magic inline styles duplicated across 12 sections.**

Optional helper component `LandingDecorLayer.vue`:
- Props: `pattern: 'dots' | 'grid' | 'stripes' | 'mesh' | 'none'`, `intensity: 'low' | 'medium'` (maps to opacity presets), `position: 'top-right' | 'bottom-left' | 'center' | 'full'`.
- Renders absolutely positioned, `pointer-events-none`, `aria-hidden="true"`.
- May include 1–2 inline SVG vector shapes per instance (simple paths only).

### 2. Hero — flagship modern layer

Upgrade `HeroSection.vue`:

- Stack: base `--theme-bg` → mesh gradient layer → dot OR grid pattern → optional subtle stripe accent in one corner → content.
- Add **2–3 inline SVG vector elements** (e.g. floating ring, dashed arc, small node graph suggesting “connection marketplace”) positioned behind text; stroke `#10b981` / `#34d399` at 0.15–0.35 opacity; no animation.
- Apply **glass** to the schematic preview panel: semi-transparent surface + backdrop-blur + gradient top edge (already has accent line — enhance, don’t replace caption).
- Optional: very soft **gradient mesh** behind headline (RTL accent bar stays; do not remove brand mark).

### 3. Section-specific ambient backgrounds

Assign patterns via `LandingSectionShell` or `LandingDecorLayer` inside each section — **alternate** so the scroll feels designed, not repetitive:

| Section | Suggested decor |
|---------|-----------------|
| Problem/Solution | muted mesh + dots low |
| How it works | grid low + SVG connector dots at lg (static dashed lines between step cards — finally implement the optional flow from prompt 04) |
| Audiences | glass cards on striped-bg section (stripes very faint) |
| Live listings | mesh bottom-left; listing cards get glass + subtle gradient border on hover |
| Responsibility boundary | elevated: stronger mesh + 1 SVG shield-outline vector (abstract, not a bank badge) behind header |
| Product status | glass status panel with gradient border |
| Pricing | dots medium |
| FAQ | minimal dots; open accordion item gets glass highlight |
| Contact / Lead | glass form panel + grid pattern behind |
| Investing | mesh + single SVG upward curve (abstract growth, not stock chart) |

Extend `LandingSectionShell.vue` with optional prop `decorPattern?: 'dots' | 'grid' | 'stripes' | 'mesh' | 'none'` that renders `LandingDecorLayer` behind the slot content.

### 4. Upgrade shared primitives

**`LandingSurfaceCard.vue`:**
- Add prop `glass?: boolean` — when true, apply `.landing-glass-card`.
- Add prop `gradientBorder?: boolean` — subtle emerald gradient border (1px).
- Keep existing `highlight`, `hoverable`, `accentTop`.

**`LandingListingCard.vue`:**
- Glass-style surface on resting state; on hover keep translate + emerald border (no logic change).
- Amount row: optional subtle gradient underline or glow behind number (text stays `--theme-text-primary`).

**`LandingHeader.vue`:**
- Strengthen glass sticky bar: `bg-[var(--theme-surface)]/70 backdrop-blur-lg border-b border-white/5`.
- Optional 1px gradient line at bottom edge (emerald fade).

### 5. SVG vector library (inline, small)

Create `src/features/landing/components/landingVectors.ts` exporting simple SVG path strings or small functional components:

- `VectorConnectionNodes` — 3–4 circles + lines (marketplace connection metaphor)
- `VectorArcRing` — decorative ring
- `VectorGridWave` — soft wave line

Use only inside decor layers; never replace readable content. All SVGs: `currentColor` or emerald stroke, no fills that obscure text.

### 6. FAQ & forms polish

- FAQ closed: glass-light border; open: `gradientBorder` + `--theme-surface-muted`/50 answer panel with blur.
- Form inputs: optional inner shadow; focus ring unchanged functionally.

### 7. Tests & docs

- Existing vitest must pass; add tests only if new `landingContent.visual` keys added.
- Update `docs/ARCHITECTURE.md` / `.fa.md` — subsection “Landing decor system” referencing `landingDecor.css` and `LandingDecorLayer`.
- Reference `docs/design-system.md`; do not duplicate it.

## Do NOT

- Change section titles/subtitles/regulatory body copy.
- Add new sections or CTAs.
- Add `framer-motion`, new npm deps, or Lottie.
- Use `background-attachment: fixed` (mobile jank).
- Exceed 360px horizontal overflow.

## Verification

- `bun run lint` — 0 errors
- `bun run test` — all pass
- Visual check: hero + responsibility boundary + one form section clearly show gradient/pattern/glass/vector layering
- 360px: no horizontal scroll; text still readable

Reply with commit SHA and a short note on which decor patterns were applied per major section.
```
