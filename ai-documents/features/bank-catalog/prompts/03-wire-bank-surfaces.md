# پرامپت ۰۳ — اتصال نشان و انتخاب بانک

خروجی Step 6 از [`implementation_plan.md`](../implementation_plan.md). مرجع: [`feature_spec.md`](../feature_spec.md) §۲.۱ سطوح UI، قوانین ۸، ۱۲، ۱۴، ۱۶، ۱۸، ۲۶، ۲۸ و سناریوهای ۲، ۳، ۷، ۸، ۱۲، ۱۳.

این **پرامپت ۰۳** است (نه گام ۳ بک‌اند). گام‌های بک‌اند ۱–۳ قبلاً در `doion` انجام شده‌اند.

## قاعده اجرا

این متن **فقط در Google AI Studio** روی ریپوی فعال UI (`checkyar-googleai`) اجرا می‌شود. از Cursor یا کلون لوکال روی این ریپو commit/push نکنید.

فقط بلوک `text` پایین را در Studio بچسبانید.

## پیش‌نیاز

پرامپت‌های ۰۱ و ۰۲ باید اجرا و پذیرفته شده باشند. HEAD مورد انتظار UI پس از ۰۲: `ebf75f1`. موجود است:

- `BankBadge`، `LOCAL_BANKS`، `useBanksCatalog` (`banks`, `loading`, `error`, `fetchBanks`)
- `banksApi.list()` و شبیه‌ساز با `bank` تو‌در‌تو
- فرم‌ها هنوز `NSelect` با **متن فارسی** دارند؛ فیلتر بازارچه هنوز `filters.bank_name` می‌فرستد
- حساب کاربری (`MyAccountView`) در این پرامپت **نیست** (پرامپت ۰۴)

## پوشش این پرامپت

- کامپوننت `BankSelect` (کاتالوگ + نشان داخل گزینه؛ مقدار = `code`)
- جایگزینی آیکون ساختمان / متن خام بانک با `BankBadge` در صفحات **فعال** `src/features/` و `src/shared/`
- فیلتر بازارچه و گزارش: `bank` (کد) یا «همه بانک‌ها»
- ثبت/ویرایش: بدون کد معتبر، API صدا نمی‌شود
- اسکن `bank_name` و گزارش باقی‌مانده‌ها
- Vitest + docs EN/FA

## تصمیم‌های قفل‌شده

- `NSelect` / `BankSelect` مقدار `code` می‌فرستد، نه نام آزاد.
- «همه بانک‌ها» = بدون قید بانک؛ متن «همه بانک‌ها» + آیکون ساختمان عمومی؛ بدون رنگ/لوگوی بانک.
- لوگو فقط از `logo_url` محصول؛ CDN بانک‌ها ممنوع.
- `src/views/` را دست نزن.
- testidهای موجود لندینگ/ثبت آگهی را نشکن (`landing-listing-card-*`, `listing-create-page`, `listing-fill-sample`, `marketplace-listing-card`).

---

```text
Goal: wire BankBadge into every active listing/match/moderation/landing/marketplace/report surface that currently shows a bank name, and add a reusable BankSelect so filters and listing forms send catalog codes. Do not change MyAccountView (destination payout bank) — that is the next prompt. Do not touch unused duplicates under src/views/.

Before coding: list remaining ambiguities. If the instructions are already complete, proceed.

## Context

- Active Cheque Yar UI: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun only (`bun.lock`). Never create or commit `package-lock.json`. Never use npm as the package manager of record.
- All user-facing text is Persian, RTL only. No i18n. No English UI copy.
- Backend is a separate Django monorepo. Do NOT change Django files.
- Do not add npm/bun dependencies.
- Product default theme is dark. Pass `theme="dark"` to BankBadge unless the page is explicitly light.
- HEAD after prompt 02: `ebf75f1`.

Already available:

- `src/shared/components/BankBadge.vue` — props: `bank`, `fallbackName`, `theme`, `size` (`default` | `compact`), `showName`. Unknown state = building icon + first letter of fallbackName, no catalog brand color.
- `src/shared/banks/lookup.ts` — `findBankByCode`, `findBankByNameOrAlias`, `toBankSummary`, `getBankBrandColor`
- `src/shared/banks/useBanksCatalog.ts` — `{ banks, loading, error, fetchBanks }`. Module-level cache. Live failure already falls back to `LOCAL_BANKS`. **You MUST call `fetchBanks()` from BankSelect (or a parent) so Live actually hits GET /banks/.**
- Listings already have `bank: BankSummary | null` plus `bank_name`.
- Create/update API already expects `bank` as a catalog code.

Router-active files (must update). Do not spend time on `src/views/*` clones:

Display (replace building icon +/or raw `bank_name` with BankBadge):

- `src/shared/components/ListingCard.vue` (`data-testid="marketplace-listing-card"`)
- `src/features/marketplace/LatestListingsWidget.vue`
- `src/features/marketplace/MarketplaceView.vue` (card grid already uses ListingCard; also the table column that currently renders `row.bank_name`)
- `src/features/landing/sections/LandingListingCard.vue` (`data-testid="landing-listing-card-${id}"` MUST stay)
- `src/features/landing/components/LandingHeroListingsPreview.vue` (today a green first-letter chip + name — replace with compact BankBadge; keep click/scroll behavior)
- `src/features/listings/ListingDetailView.vue`
- `src/features/listings/MyListingsView.vue` (table render)
- `src/features/matches/MyMatchesView.vue`
- `src/features/matches/ExpressInterestView.vue`
- `src/features/matches/views/TradeDetails.vue` (uses `matchesStore.currentMatch.listingBank` string — prefer nested `listing.bank` + `bank_name` via BankBadge)
- `src/features/moderation/views/ModerationQueue.vue` (active `/moderation` route)
- `src/features/moderation/views/ModerationReview.vue` (active review route; `currentReviewItem.bank` is currently a Persian string from the store mapper — show BankBadge from the underlying listing if available, otherwise fallbackName)

Select (replace hardcoded `bankOptions` arrays):

- `src/features/marketplace/MarketplaceView.vue` filter
- `src/features/listings/views/ListingCreateWizard.vue` (active create + used by ListingEdit.vue) — both wizard-step and flat-mode NSelects
- `src/features/listings/composables/useListingForm.ts`
- `src/features/reports/components/GlobalFiltersPanel.vue`

Optional if still imported by a live route: `src/features/listings/ListingCreateView.vue`, `ListingEditView.vue`, `src/features/moderation/ModerationQueueView.vue`. Prefer not duplicating work on unused files; list them in the remaining-scan report instead.

## 1) BankSelect

New component e.g. `src/shared/components/BankSelect.vue`.

Behavior:

- Wraps Naive UI `NSelect` (keep existing form/filter look: size, clearable where the current control is clearable).
- Options come from `useBanksCatalog().banks` after `fetchBanks()` on mount (do not duplicate the 14-bank table in the component).
- `v-model` is `string | null` = catalog **code** (e.g. `mellat`). Never a free-text name.
- Each bank option: `renderLabel` (and selected display) uses `BankBadge` with `size="compact"` and the catalog row (`toBankSummary` if needed).
- Prop `allowAll` (boolean, default false):
  - true (filters): first option value `null` or `''` labeled exactly «همه بانک‌ها» with the generic `BusinessOutline` building icon and **no** catalog brand color or logo. Clearing the select means the same (no bank constraint).
  - false (listing create/edit): no “all banks” option; placeholder e.g. «انتخاب بانک» (Persian). Empty is invalid.
- While `loading` is true: the select is disabled and shows Naive loading (spec: catalog loading disables the control). Cards that already have nested `bank` must NOT wait on this.
- If after fetch `banks` is empty: keep disabled; listing submit must not fire (parent responsibility + form validation).
- API catalog failure already falls back to `LOCAL_BANKS` inside `useBanksCatalog` — do not show a full-page error.
- data-testid: `bank-select` on the root/select. Marketplace filter wrapper may add `marketplace-bank-filter`. Listing form control: `listing-form-bank`.

Do not load images from bank websites or CDNs.

## 2) Display wiring

Everywhere a bank is shown on the surfaces above:

```vue
<BankBadge
  :bank="listing.bank"
  :fallback-name="listing.bank_name"
  size="default"  <!-- compact in tables, widgets, hero chips, select rows -->
/>
```

- If nested `bank` is present, BankBadge uses catalog logo/initial+brand color.
- If `bank` is null (seed listing id 114 is the unknown sample), unknown state must appear (building + first letter of `bank_name`).
- Remove the old `BusinessOutline` + heading pair on ListingCard (the badge replaces both mark and name when `showName` is true). Keep serial number and other listing fields.
- Landing: no third-party bank CDN. Keep existing landing testids and navigation/guest behavior.
- In `h()` table renders (MarketplaceView, MyListingsView), use `h(BankBadge, { bank: row.bank, fallbackName: row.bank_name, size: 'compact' })` (Vue 3 prop casing as required by your setup).

Smart pricing (`SmartPricingCalculator` / `useSmartPricing`): it currently displays `bankId` as the form string. After the form stores a **code**, show the Persian `display_name` (lookup) in the sentence; the pricing function may keep using the code as the bank key (more stable). Do not break existing smart-pricing unit tests — update fixtures if they assumed a Persian `bankId`.

## 3) Marketplace filter

In `MarketplaceView.vue`:

- Replace hardcoded `bankOptions` + `filters.bank_name` with `BankSelect allowAll`.
- Bind `filters.bank` (code). When «همه بانک‌ها» / empty, omit both `bank` and `bank_name` from the request.
- In `loadListings` / `cleanFilters`: if `filters.bank` is set, send `bank` and do **not** send `bank_name`. Reset must clear `bank`.
- Table bank column uses BankBadge (see §2).

Reports `GlobalFiltersPanel.vue`: same BankSelect `allowAll`. `store.filters.bank` should become a catalog code (or empty). Client-side mock report rows still have Persian `bankName` — match by `findBankByNameOrAlias(row.bankName)?.code === selectedCode` (or add codes to mock rows). Do not invent a new reports API.

## 4) Listing create / edit

Active path: `ListingCreateWizard.vue` + `useListingForm.ts` (edit route reuses the wizard).

- Replace both NSelects that use `bankOptions` with `BankSelect` (`allowAll=false`, testid `listing-form-bank`).
- Store **code** in `formData.bank` (not «بانک ملت»).
- `fillSampleData` (`data-testid="listing-fill-sample"`): set `formData.bank = 'mellat'` (not the Persian label). Keep the button and testid.
- Review/summary step that prints `form.formData.bank` must show BankBadge or display_name, never the raw code as the only user-visible label.
- `publishListing` / submit:
  - Resolve with `findBankByCode` first, then `findBankByNameOrAlias` as a last resort.
  - If still unresolved or empty: show the existing Persian form error and **do not** call `listingsApi.createListing`.
  - Payload remains `{ bank: code, ... }` with no `bank_name`.
- `isFormValid` must require a catalog code (or a name that lookup maps to a code).
- Do not change `data-testid="listing-create-page"` or the publish button labels that e2e uses (`تأیید و ارسال نهایی`).

## 5) Matches / moderation mappers

If a store copies only `bank_name` into a display string (`matchesStore.listingBank`, `moderationStore` `bank: listing.bank_name`):

- Prefer passing through `listing.bank` (summary) plus `bank_name`.
- UI uses BankBadge. Do not leave a bare Persian string as the only bank UI on those pages.

## 6) Tests (Vitest)

Add/adjust tests:

1. BankSelect: `allowAll` option shows «همه بانک‌ها» without catalog brand color; a bank option renders BankBadge / display_name; v-model emits a code like `mellat`.
2. ListingCard: with `bank` mellat and `logo_url` null, shows BankBadge initial (not a lone BusinessOutline heading). With `bank: null`, unknown testid appears.
3. Marketplace loadListings (mock the API): selecting mellat calls `getListings` with `bank: 'mellat'` and without `bank_name`.
4. useListingForm / wizard: empty bank does not call createListing; fill-sample sets `mellat`.
5. Existing landing tests still find `landing-listing-card-*`. Update fixtures with `bank: null` or a BankSummary as already done in prompt 02.

Run `bun run lint` and `bun run test`. No Playwright / doion e2e in this repo.

## 7) Remaining-scan report (mandatory in your reply)

Search `src/` (especially `src/features` and `src/shared`) for `bank_name`, `bankOptions`, and `BusinessOutline` next to bank UI. In the commit reply, list leftover call sites and classify:

- unused `src/views/` (ignore)
- MyAccount / payout bank (defer to prompt 04)
- intentional API field `bank_name` on types/simulator
- anything still user-visible that this prompt should have fixed (then fix it)

## 8) Docs (this repo, EN + FA)

Update Architecture: BankBadge/BankSelect are wired on marketplace, landing, listings, matches, moderation, reports filters; values are codes; MyAccount still pending.

Update Testing: new vitest files.

## 9) Do not

- Commit `package-lock.json` or use npm as source of truth.
- Add dependencies.
- Edit `src/views/`.
- Change MyAccountView / payout destination bank.
- Break landing or listing-create testids / e2e-visible button copy.
- Load bank logos from third-party CDNs.
- English user-facing copy.
- Unrelated refactors.
- Django / doion e2e.

## 10) Acceptance

- Marketplace/listing cards, landing hero + live cards, detail, my listings, matches, moderation queue/review, reports bank filter all show BankBadge (or BankSelect options with badges).
- Filter «همه بانک‌ها» sends no bank constraint; a bank option sends `bank=<code>`.
- Create listing cannot submit without a catalog bank; fill-sample still works and sends `mellat`.
- Unknown seeded listing still looks unknown (no catalog brand color).
- `bun run lint` and `bun run test` pass.
- Remaining-scan list is in the reply.

## 11) After you finish

Commit in this GitHub-connected AI Studio project:

`feat(banks): wire BankBadge and BankSelect across listing surfaces`

Reply with:

1. The commit SHA
2. Files added/changed
3. Lint and test results
4. The remaining-scan list (section 7)
5. Any testid you added
```
