# پرامپت B — بخش‌های محتوایی ثابت

خروجی Step 3 از [`implementation_plan.md`](../implementation_plan.md).

## قاعده اجرا

این متن **بدون هیچ تغییری** دو بار اجرا می‌شود: یک بار در Google AI Studio (کد رسمی محصول) و یک بار در sandbox مسیر `/Users/alamalhoda/Projects/checkyar-cursor-lab` روی شاخه `experiment/landing-cursor`. اگر پرامپت اصلاح شد، هر دو مسیر باید از نو با نسخه اصلاح‌شده اجرا شوند.

فقط بلوک `text` پایین کپی می‌شود.

## پیش‌نیاز

پرامپت ۰۱ (اسکلت) باید قبلاً اجرا و پذیرفته شده باشد. HEAD فعلی UI: `86ee6e3`. ساختار موجود:

- `src/features/landing/LandingView.vue` — ۱۲ بخش place-held + `LandingFooter`
- `src/features/landing/constants.ts` — `DOCUMENT_TITLE` و `META_DESCRIPTION` با ZWNJ
- testidهای بخش، هدر، فوتر — طبق پرامپت ۰۱
- testidهای موبایل هدر: `landing-nav-*-mobile`

## پوشش قوانین spec

قوانین ۱۵، ۱۹، ۲۰، ۲۱، ۲۳، ۲۴ از [`feature_spec.md`](../feature_spec.md).

## خارج از دامنه این پرامپت (پرامپت ۰۳)

این سه بخش **همچنان placeholder** بمانند — فقط عنوان کوتاه و یک جمله «در پرامپت بعدی»؛ بدون API، بدون فرم، بدون منطق:

- `landing-section-live-listings`
- `landing-section-contact-us`
- `landing-section-lead-capture-form`

## تصمیم‌های این پرامپت

- **SSOT متن:** همه متن‌های ثابت در `src/features/landing/content/landingContent.ts`؛ کامپوننت‌ها فقط import می‌کنند.
- **متن رگولاتوری قفل‌شده:** §۲.۵، §۲.۶، پرسش‌های §۲.۸، و پاسخ‌های FAQ — عیناً یا با escape `\u200c`؛ بدون بازنویسی خلاقانه.
- **فوتر:** توضیح برند و خط سلب مسئولیت پایین فوتر با زبان §۲.۵ هم‌راستا شود (جزئیات در بلوک پرامپت).
- **CTA هیرو:** اولین بار در این پرامپت ساخته می‌شوند.

---

```text
Goal: replace the place-held static content sections on the public landing page with real Persian copy. This prompt is content and layout for fixed sections only — no API calls, no forms, no live listings widget. Those arrive in the next prompt.

Before coding: list any ambiguities and ask me questions until the instructions are fully clear.

## Context

- Repo: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun only.
- All user-facing text is Persian, RTL only. No i18n, no English UI copy.
- Do NOT change backend code, routing guards, feature flags, auth logic, or `LoginView`.
- The landing page skeleton from the previous prompt is already merged (HEAD `86ee6e3`). Keep every existing section `id`, `data-testid`, and DOM order exactly as they are today.
- Brand theme: `dark`, semantic `--theme-*` tokens from `docs/design-system.md`. No one-off hex colors outside tokens.
- Tone guide (section ۸ of design-system): say «سکوی اتصال» / «Marketplace اطلاعاتی» / «نرخ پیشنهادی، غیرالزام‌آور» / «آماده پایلوت» / «تسویه بیرون از پلتفرم». Do NOT say «بانک»، «کیف پول»، «سود قطعی»، «لانچ شد»، or claim receivables management.
- Product messaging source: `docs/سند پایه پروژه (Core Brief).md` in the doion monorepo (referenced for intent only; do not edit that file).

## 1) Content SSOT — `src/features/landing/content/landingContent.ts`

Create this file as the single source of truth for all static landing copy in this prompt.

Export structured objects (not loose scattered strings). Suggested shape:

- `hero`
- `problemSolution`
- `howItWorks` (title + ordered steps array)
- `audiences` (title + two audience cards)
- `responsibilityBoundary` (LOCKED — see part 3)
- `productStatus` (LOCKED — see part 4)
- `pricing` (title + three revenue models + no-fee disclaimer)
- `faq` (array of `{ question, answer }` — LOCKED questions, LOCKED answers below)
- `investing` (title + short body + CTA label)

**ZWNJ rule:** every Persian string that contains «چک‌یار»، «چک‌های»، «مدت‌دار»، or similar must preserve U+200C. Prefer `\u200c` escapes in the TS source (same pattern as `src/features/landing/constants.ts`) so editors cannot silently flatten them.

Do NOT put static copy inline in Vue templates except trivial structural words like «بعدی» if needed.

## 2) Section components

Refactor `LandingView.vue` to compose one Vue component per content section under `src/features/landing/sections/`:

| Component | Replaces placeholder in `LandingView` |
|-----------|--------------------------------------|
| `HeroSection.vue` | section `#hero` |
| `ProblemSolutionSection.vue` | `#problem-and-solution` |
| `HowItWorksSection.vue` | `#how-it-works` |
| `AudiencesSection.vue` | `#audiences` |
| `ResponsibilityBoundarySection.vue` | `#responsibility-boundary` |
| `ProductStatusSection.vue` | `#product-status` |
| `PricingSection.vue` | `#pricing` |
| `FaqSection.vue` | `#faq` |
| `InvestingSection.vue` | `#investing-in-cheque-yar` |

Each section component MUST:

- Keep the same outer `<section>` element with the same `id` and `data-testid` already on that section in `LandingView.vue` today. Move the attributes onto the component root (or pass them through) — do not rename or renumber.
- Import copy from `landingContent.ts` only.
- Use `--theme-*` tokens and spacing from design-system (cards on `--theme-surface`, borders `--theme-border`, `rounded-2xl`, responsive padding).
- Be responsive from 360px with no horizontal scroll.
- Keep keyboard focus visible on every interactive element (`focus-visible:ring-2 focus-visible:ring-emerald-500` or equivalent token-based ring).

Leave these three sections as minimal placeholders inside `LandingView.vue` (do not build components for them yet):

- `#live-listings` / `landing-section-live-listings`
- `#contact-us` / `landing-section-contact-us`
- `#lead-capture-form` / `landing-section-lead-capture-form`

## 3) LOCKED — Responsibility boundary (spec §2.5)

These strings are regulatory. Export them from `landingContent.ts` and render them verbatim in `ResponsibilityBoundarySection.vue`. No paraphrasing, no merging into one paragraph, no extra claims.

Four statements — each as its own visually distinct item (card, list item, or icon row):

1. پول را لمس نمی‌کند
2. چک را نگه نمی‌دارد
3. ضمانت وصول نمی‌دهد
4. نرخ پیشنهادی غیرالزام‌آور است

Closing sentence (separate, readable):

چک‌یار واسط فناورانه است، نه نهاد مالی.

Use ZWNJ in «چک‌یار» via `\u200c`.

## 4) LOCKED — Product status (spec §2.6)

Exact string (also used as the pilot badge in the hero):

v1 لایه ۱ آماده پایلوت — نه در حال ساخت MVP، نه لانچ‌شده

Render in:

- `HeroSection.vue` — visible pilot/status badge near the headline (`data-testid="landing-hero-pilot-badge"`).
- `ProductStatusSection.vue` — same exact sentence as the section body (can add a short neutral intro line above it, but the sentence itself must match character-for-character).

## 5) Hero section content and CTAs

Content:

- Headline: product name «چک‌یار» + the one-liner from spec §2.3: «سکوی دیجیتال کشف و اتصال در بازار نقدشوندگی چک‌های مدت‌دار»
- Supporting paragraph: 2–3 sentences describing the marketplace connector role (discovery + connection, not a bank, settlement outside platform). Derive from Core Brief §1–3; do not invent capabilities the product lacks.
- Pilot badge: exact §2.6 text (part 4).

CTAs (spec §2.4) — use `useAuthStore()`:

| Button | Guest | Signed in |
|--------|-------|-----------|
| Primary | «ثبت‌نام» → `/register` | «ورود به بازارچه» → `/marketplace` |
| Secondary | «ورود» → `/login` | «مشاهده آگهی‌ها» → `#live-listings` (smooth scroll, same pattern as header anchor links) |

- Guest only: optional tertiary text link «مشاهده بازارچه» → `/login` (not a second primary button).
- Signed-in: do NOT render login or register buttons in the hero.

`data-testid`:

- `landing-hero-primary-cta` on the primary button
- `landing-hero-secondary-cta` on the secondary button
- `landing-hero-pilot-badge` on the status badge

Use `<button type="button">` or router navigation consistent with `LandingHeader.vue`. Every CTA must have a meaningful Persian label and visible focus ring.

## 6) Problem / solution

Two-column or stacked layout on mobile:

- **مسئله:** opaque, fragmented cheque discount market; informal intermediaries; lack of price discovery transparency.
- **راه‌حل:** Cheque Yar as a digital discovery and connection platform — registered listings, Sayad-related validation in the product flow, marketplace browse, match expression; settlement stays outside.

Keep copy factual and aligned with Core Brief. No numbers, no guarantees.

## 7) How it works — six steps (spec §2.3)

Render as a numbered or stepped list (Naive `NSteps` or a simple ordered visual — your choice, but must work at 360px):

1. ثبت‌نام و تکمیل KYC
2. ثبت آگهی چک
3. بررسی و تأیید توسط ناظر
4. کشف در بازارچه
5. ابراز تمایل (Match)
6. تسویه بیرون از پلتفرم

Each step: short title + one-line description. Step 6 must explicitly say settlement is outside the platform.

## 8) Audiences — two columns (spec §2.3)

| Column | Title | Bullet points |
|--------|-------|---------------|
| Right (RTL first) | دارندگان چک | Why they use the platform: liquidity before maturity, transparent suggested rate, moderated listings |
| Left | سرمایه‌گذاران (حقیقی و حقوقی) | Browse/filter published listings, express interest; both natural and legal entities per `user_type` |

Stack vertically on mobile. No third column.

## 9) Pricing placeholder (spec rules 15 + 19)

Three revenue models — **no numbers, no percentages, no currency amounts**:

1. کارمزد ثبت آگهی
2. اشتراک
3. کارمزد موفقیت در ازای اتصال (lead/match fee)

Prominent disclaimer (exact intent, ZWNJ-safe Persian):

«در محصول فعلی کارمزدی دریافت نمی‌شود.»

Each model gets a card with title + one sentence explaining it is a future/planned model, not active billing.

## 10) FAQ — six Q&A pairs (spec §2.8)

Questions are LOCKED — use these exact strings:

1. آیا پول در پلتفرم جابه‌جا می‌شود؟
2. آیا نرخ پیشنهادی الزام‌آور است؟
3. تسویه و انتقال چک کجا انجام می‌شود؟
4. برای شروع چه چیزی لازم است (KYC)؟
5. آیا استفاده هزینه دارد؟
6. آیا چک‌یار وصول چک را ضمانت می‌کند؟

Answers are LOCKED for regulatory consistency — use these exact strings (with `\u200c` in «چک‌یار» where shown):

1. «خیر. چک‌یار هیچ وجهی را دریافت، نگه‌داری یا جابه‌جا نمی‌کند. تسویه مالی مستقیماً بین طرفین و بیرون از پلتفرم انجام می‌شود.»
2. «خیر. نرخ تنزیل نمایش‌داده‌شده در آگهی‌ها پیشنهادی و غیرالزام‌آور است. توافق نهایی بین دارنده چک و سرمایه‌گذار بیرون از پلتفرم صورت می‌گیرد.»
3. «انتقال مالکیت چک (از جمله در سامانه صیاد) و تسویه وجه مستقیماً بین طرفین و بیرون از پلتفرم انجام می‌شود. چک‌یار در این فرآیندها دخالت اجرایی ندارد.»
4. «ثبت‌نام، تکمیل احراز هویت (KYC)، و تأیید مدارک توسط ناظر. پس از تأیید، می‌توانید آگهی ثبت کنید یا در بازارچه فرصت‌ها را ببینید.»
5. «در محصول فعلی هیچ کارمزدی دریافت نمی‌شود. مدل‌های درآمدی آینده (بدون عدد) در بخش تعرفه همین صفحه توضیح داده شده‌اند.»
6. «خیر. چک‌یار هیچ ضمانتی برای وصول چک ارائه نمی‌دهد. ریسک اعتباری بر عهده طرفین معامله است.»

UI: accordion/collapse (Naive `NCollapse` is fine). Every answer visible when expanded. Add `data-testid="landing-faq-item-<n>"` on each item root (n = 1..6). Section must remain keyboard-accessible.

## 11) Investing in Cheque Yar (spec §2.3 row 13)

One short block (max one card): invite strategic investors/partners interested in platform development. CTA button «تماس با ما» scrolls to `#contact-us` (placeholder section for now). `data-testid="landing-investing-cta"`.

No financial projections, no equity terms, no English pitch deck language.

## 12) Footer copy reconciliation

Update `LandingFooter.vue` brand description and bottom disclaimer line so they align with §2.5 language and do not contradict locked copy:

- Brand blurb: keep «سکوی دیجیتال کشف و اتصال در بازار نقدشوندگی چک‌های مدت‌دار» and the sentence «چک‌یار واسط فناورانه است، نه نهاد مالی.» (same as §2.5 closing — import from `landingContent.ts` if possible to avoid drift).
- Replace the bottom line «واسط فناورانه کشف و اتصال — فاقد کارکرد بانکی، اعتباری و تسهیلاتی» with a shorter line that does not duplicate the four statements but stays consistent, e.g. «تسویه و انتقال چک بیرون از پلتفرم انجام می‌شود.»

Do NOT remove placeholder footer links or social buttons. Do NOT change `getCurrentJalaliYear()` behavior.

## 13) Tests (vitest)

Add `src/features/landing/content/landingContent.test.ts`:

- Assert §2.5 four statements and closing sentence match exactly (export and compare).
- Assert §2.6 product status string matches exactly.
- Assert FAQ array length === 6 and each question matches §2.8 exactly.
- Assert each FAQ answer matches the locked strings in part 10.
- Assert key strings contain `\u200c` where required (at least «چک‌یار» in hero headline export).

Run `bun run lint` and `bun run test`. Report results in your reply.

Do NOT add Playwright to this repo.

## 14) Documentation (same commit, bilingual EN + FA)

Update touched sections only:

- `docs/ARCHITECTURE.md` + `.fa.md`: document `landingContent.ts`, the `sections/` components, and which sections are content-complete vs still placeholder.
- `docs/TESTING.md` + `.fa.md`: document `landingContent.test.ts` and how to spot-check locked regulatory strings in the browser.

## 15) Do not

- Implement live listings API, listing cards, contact form, or lead capture form (next prompt).
- Call `axios` or `marketplaceApi` from these sections.
- Change routing, guards, `useFeatureFlags`, simulator seed, mock sign-out marker, or `App.vue` chrome logic.
- Touch `src/views/`, add dependencies, or commit `package-lock.json`.
- Rename, remove, or reorder existing `data-testid` values from prompt 01.
- Add duplicate `data-testid` values (same rule as prompt 01: one element per testid per viewport/menu state).
- Paraphrase locked regulatory text.
- Add English user-facing copy.
- Unrelated refactors.

## 16) Acceptance (mock mode, guest)

With `VITE_USE_MOCK=true` and guest state (`chequeyar_mock_signed_out` after logout):

- `/landing` shows real content in sections 1–4 and 6–9 and 12 (hero through investing); sections 5 (live listings), 10 (contact), 11 (lead form) remain placeholders.
- Hero shows pilot badge with exact §2.6 text; guest sees register + login CTAs with correct testids.
- Responsibility section shows four separate statements + closing sentence exactly.
- FAQ shows all six locked questions; expanding reveals locked answers.
- Pricing shows three models with no numbers and the no-fee disclaimer.
- Footer blurb matches §2.5 closing sentence; no horizontal scroll at 360px.
- `bun run lint` and `bun run test` pass.

In your reply: group changed files as code / tests / docs, list any new `data-testid` values, confirm locked strings were not paraphrased, and give the commit SHA.
```
