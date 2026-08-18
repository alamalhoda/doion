# پرامپت C — بخش داده‌دار و فرم‌ها

خروجی Step 4 از [`implementation_plan.md`](../implementation_plan.md).

## قاعده اجرا

این متن **بدون هیچ تغییری** دو بار اجرا می‌شود: یک بار در Google AI Studio (کد رسمی محصول) و یک بار در sandbox مسیر `/Users/alamalhoda/Projects/checkyar-cursor-lab` روی شاخه `experiment/landing-cursor`. اگر پرامپت اصلاح شد، هر دو مسیر باید از نو با نسخه اصلاح‌شده اجرا شوند.

فقط بلوک `text` پایین کپی می‌شود.

## پیش‌نیاز

پرامپت‌های ۰۱ و ۰۲ باید قبلاً اجرا و پذیرفته شده باشند. HEAD فعلی UI: `746cea6`.

سه placeholder در `LandingView.vue`:

- `#live-listings` / `landing-section-live-listings`
- `#contact-us` / `landing-section-contact-us`
- `#lead-capture-form` / `landing-section-lead-capture-form`

`id` و `data-testid` این سه بخش را تغییر نده.

## پوشش قوانین spec

قوانین ۴، ۷–۱۴، ۱۶، ۱۷، ۲۵، ۲۹ از [`feature_spec.md`](../feature_spec.md).

## تصمیم‌های این پرامپت

- **کارت مخصوص landing** — `LatestListingsWidget` و `ListingCard` را import یا کپی نکن (رنگ off-token، نرخ ساختگی `۲.۵`، مقصد کلیک همیشه جزئیات آگهی). فرمت مبلغ/تاریخ از `persianUtils`.
- **یک مسیر API موجود** — فقط `marketplaceApi.getLatestListings()`. صدا زدن `axios` یا ساخت endpoint جدید ممنوع.
- **فرم‌ها UI-only** — هیچ `fetch` / `axios` / `api.*` روی submit.

---

```text
Goal: fill the three remaining landing placeholders: live listings (public API), contact form, and lead-capture form. Content sections from the previous prompt stay as they are.

Before coding: list any ambiguities and ask me questions until the instructions are fully clear.

## Context

- Repo: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun only.
- All user-facing text is Persian, RTL only. No English UI copy except tokens already on the page (KYC, Match, MVP, Marketplace, lead/match fee).
- Do NOT change backend code, routing guards, feature-flag seed, auth, `LoginView`, `unwrapList`, `marketplaceApi`, `LatestListingsWidget.vue`, or `ListingCard.vue`.
- HEAD is `746cea6`. Keep every existing section `id` and `data-testid`.
- Brand theme: `dark`, `--theme-*` tokens, emerald accent only. No amber / rose / indigo / one-off hex. No `animate-pulse`.
- Do not use «مطالبات», «پذیرش شرکای پایلوت», or `user_type` in user-facing copy.
- Live listings endpoint (already wrapped): `marketplaceApi.getLatestListings()` in `src/api/index.ts`.
  - Live: `GET /api/v1/marketplace/listings/latest/` — AllowAny, a plain array of up to 4 published listings (the helper already calls `unwrapList`).
  - Mock: the same function reads published simulator listings. No extra mock/Live branching in the landing module.
- Fields the card may read: `id`, `bank_name`, `face_amount`, `due_date`, `days_to_due`, `suggested_discount_rate`, `risk_tier`, `issuer_profile.name`.
- `face_amount` is rials. Display tomans = floor(rials / 10) with Persian digits and the word «تومان».
- `due_date` is ISO `YYYY-MM-DD`. Display Jalali via `Intl.DateTimeFormat('fa-IR-u-ca-persian', …)` — same calendar approach as `getCurrentJalaliYear` in `src/utils/persianUtils.ts`.

## 1) Shared formatters in `persianUtils.ts`

Add two small pure helpers (and vitest) so the landing card does not invent a third `formatTomans`:

- `formatTomanFromRial(amount: string | number): string` — floor divide by 10, `toLocaleString('fa-IR')`, no currency word (the template adds «تومان»).
- `formatJalaliDate(isoDate: string): string` — Jalali display for an ISO date; on invalid input return an empty string, never throw.

Do not change existing persianUtils functions.

## 2) Live listings section

Replace the `#live-listings` placeholder with `src/features/landing/sections/LiveListingsSection.vue` (keep `id="live-listings"` and `data-testid="landing-section-live-listings"` on the section root). Optional child `LandingListingCard.vue` in the same folder.

Static chrome (title, empty copy, error copy, retry label, empty CTA labels) lives in `landingContent.ts` under a `liveListings` object. Templates only import from there. Suggested title: «تابلوی آگهی‌های زنده». Do not mention «مطالبات».

Fetch: on mount, `await marketplaceApi.getLatestListings()`. Then `slice(0, 4)` in the same order the API returned. Never call `marketplaceApi.getListingDetail` from this page (that endpoint is not public).

Four states — only this section changes; the rest of the landing page stays visible:

| State | UI | testid |
|-------|----|--------|
| Loading | skeleton / spinner occupying similar height to 4 cards so the page does not jump when data arrives | `landing-listings-loading` |
| Data | 1–4 cards | each card `landing-listing-card-{id}` |
| Empty | exact message «هنوز آگهی منتشرشده‌ای وجود ندارد» + CTA | `landing-listings-empty`, CTA `landing-listings-empty-cta` |
| Error | message + «تلاش مجدد» that calls the same fetch again | `landing-listings-error`, button `landing-listings-retry` |

Empty CTA: guest → «ثبت‌نام» `/register`; signed-in → «ورود به بازارچه» `/marketplace`.

Card click / activation (spec §2.4 and rules 13–14):

- Guest → `/login`. No authenticated request.
- Signed-in → `/listings/{id}`.
- Extract a pure helper, e.g. `getLandingListingTarget(isAuthenticated: boolean, listingId: number): string`, and unit-test it.

Card content (Persian digits throughout):

- `bank_name`
- toman amount + «تومان»
- Jalali `due_date`
- `days_to_due` as «N روز تا سررسید» when the number is finite
- `suggested_discount_rate` only when it is a non-null non-empty string; never invent a fallback like «۲.۵»
- `issuer_profile.name` when present
- `risk_tier` **only** when `useFeatureFlags().showRiskTier` is true. Labels: `low` → «کم‌ریسک», `medium` → «متوسط», `high` → «پرریسک». If the flag is off, no risk word, badge, or testid on the card. Put `data-testid="landing-listing-risk-tier"` on the badge when it is rendered (one per card is fine because each card is a separate root).

Layout: 1 column at 360px, up to 4 columns on large screens. Cards are keyboard-activatable (`<a>` or `<button>`, visible focus ring). Use `--theme-*` + emerald; no indigo/amber.

## 3) Iranian mobile validator

Pure helper in the landing module (e.g. `src/features/landing/forms/iranianMobile.ts`):

- Run `toEnglishDigits` first.
- Valid iff `/^09\d{9}$/`.
- Export `isValidIranianMobile(raw: string): boolean`.
- Vitest: valid `09123456789`, valid Persian digits `۰۹۱۲۳۴۵۶۷۸۹`, invalid `12345`, invalid empty, invalid `0901234567` (too short).

## 4) Lead capture form (spec §2.7)

Replace `#lead-capture-form` with `LeadCaptureSection.vue`. Keep `id` and `data-testid="landing-section-lead-capture-form"`.

Fields (all labels and errors in `landingContent.ts`):

| Field | Required | Rule | testid on the native input |
|-------|----------|------|----------------------------|
| نام | yes | 2–60 chars after trim | `landing-lead-name` |
| موبایل | yes | `isValidIranianMobile` | `landing-lead-mobile` |
| نقش | yes | exactly one of «دارنده چک» \| «سرمایه‌گذار» \| «سایر» | `landing-lead-role` |
| توضیح | no | max 500 chars | `landing-lead-note` |

Submit button: `landing-lead-submit`. Form root: `landing-lead-form`.

Validation: show the field error, do not show success, do not fire any network request. Extract a pure `validateLeadForm(input): { ok: boolean; errors: Record<string, string> }` and unit-test empty name, short name, invalid mobile, missing role, note > 500, and a valid payload.

Success (only when `ok`): `message.success` via the existing `src/utils/discreteApi.ts` `message` helper, with this exact copy:

«درخواست شما روی همین صفحه ثبت شد؛ در محصول فعلی به سرور ارسال نمی‌شود.»

Then reset the form. Still zero network calls — grep of the new files must not contain `axios`, `api.post`, or `fetch(`.

Naive `NInput`: put testids on `:input-props="{ 'data-testid': 'landing-lead-name' }"` (and the same for other native fields), not only on the wrapper. `NSelect` / radio group: put the testid where Playwright can target the control.

## 5) Contact form

Replace `#contact-us` with `ContactSection.vue`. Keep `id="contact-us"` and `data-testid="landing-section-contact-us"`.

This is a different form from lead capture (investing CTA already scrolls here). Fields:

| Field | Required | Rule | testid |
|-------|----------|------|--------|
| نام | yes | 2–60 chars | `landing-contact-name` |
| ایمیل | yes | `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` after trim | `landing-contact-email` |
| پیام | yes | 10–500 chars | `landing-contact-message` |

Submit: `landing-contact-submit`. Form root: `landing-contact-form`. Same UI-only success helper and same success sentence as the lead form (or a sibling sentence in `landingContent.ts` that still says the form is not sent). Same field-error / no-success-on-invalid behavior. Optional small pure validator + vitest.

Optional static line under the title: a placeholder email such as `info@chequeyar.ir` is fine if it is not a `mailto:` that claims a staffed inbox; do not add live social URLs.

## 6) Tests

Add or extend vitest (this repo only, no Playwright here):

- `getLandingListingTarget` for guest vs signed-in.
- `isValidIranianMobile` cases above.
- `validateLeadForm` cases above.
- `formatTomanFromRial` (e.g. `'500000000'` → `'۵۰٬۰۰۰٬۰۰۰'` or whatever `toLocaleString('fa-IR')` produces for 50000000) and `formatJalaliDate` (valid ISO in, empty on garbage).
- Do not mock axios. You may unit-test a thin mapper that slices to 4 and maps fields, without mounting Naive.

Run `bun run lint` and `bun run test`. Report results.

## 7) Docs (same commit, EN + FA)

Update touched sections only:

- `docs/ARCHITECTURE.md` + `.fa.md`: live listings consume `marketplaceApi.getLatestListings()`; guest card goes to `/login`; forms are UI-only.
- `docs/TESTING.md` + `.fa.md`: the new vitest files; how to review listings as a guest in mock (sign out, reload `/landing`); how to toggle `show_risk_tier` and confirm the badge appears/disappears.

## 8) Do not

- Import or restyle `LatestListingsWidget` / `ListingCard`.
- Call `axios` or any `*Api` other than `marketplaceApi.getLatestListings` from landing.
- Call `getListingDetail` or any matches/KYC endpoint from this page.
- Change `unwrapList`, simulator listing seed shape, or marketplace routes.
- Add dependencies or `package-lock.json`.
- Touch `src/views/`.
- Paraphrase locked §2.5 / §2.6 / FAQ strings.
- Show risk when `show_risk_tier` is off.
- Invent a discount rate when the field is null.
- Deep-link `?redirect=` after login.

## 9) Acceptance (mock, `VITE_USE_MOCK=true`)

Guest (`chequeyar_mock_signed_out` after logout):

- `/landing` shows up to 4 published simulator listings in the live section; toman + Jalali + bank visible.
- Clicking a card goes to `/login` and the network panel has no authenticated listing-detail request.
- Empty/error/loading can be reasoned about from the four-state code; retry exists.
- `show_risk_tier` off (simulator default) → no risk badge. Turning it on at `/admin/feature-flags` and reloading landing shows the badge.
- Lead form: `12345` as mobile → field error, no success toast. Valid payload → success toast, no POST.
- Contact form: empty submit → field errors. Valid payload → success toast, no POST.
- 360px: no horizontal scroll; cards stack; both submit buttons clickable.

Signed-in: card goes to `/listings/{id}`. Empty CTA is «ورود به بازارچه».

Live mode (`VITE_USE_MOCK=false`) uses the same component code path. Do not add a second implementation.

In your reply: changed files grouped as code / tests / docs, the new data-testid list, confirmation of zero form network calls, lint/test results, and the commit SHA.
```
