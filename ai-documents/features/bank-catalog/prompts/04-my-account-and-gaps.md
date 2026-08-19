# پرامپت ۰۴ — بانک مقصد واریز + بستن شکاف‌های پرامپت ۰۳

خروجی Step 7 از [`implementation_plan.md`](../implementation_plan.md). مرجع: [`feature_spec.md`](../feature_spec.md) قوانین ۱۶، ۲۹ و سناریوهای ۲، ۸، ۷، ۲۳. بدون REST پروفایل جدید (خارج از دامنه).

## قاعده اجرا

این متن **فقط در Google AI Studio** روی ریپوی فعال UI (`checkyar-googleai`) اجرا می‌شود. از Cursor یا کلون لوکال روی این ریپو commit/push نکنید.

فقط بلوک `text` پایین را در Studio بچسبانید.

## پیش‌نیاز

پرامپت‌های ۰۱–۰۳ پذیرفته شده‌اند. HEAD مورد انتظار: `056722c`.

شکاف‌های تأییدشده بعد از ۰۳ (باید در همین پرامپت بسته شوند):

1. هیرو لندینگ هنوز حرف اول سبز + `bank_name` است.
2. فیلتر بازارچه به `filters.bank_name` بایند شده و کد را به `bank` کپی می‌کند بدون حذف `bank_name`.
3. گزینهٔ «همه بانک‌ها» آیکون ساختمان ندارد.
4. testid استاندارد روی `BankSelect` ناقص است.
5. اگر کد بانک در فرم resolve نشود، `createListing` هنوز صدا می‌شود.
6. **CI GitHub Actions (CI + CD Demo) روی `ebf75f1` و `056722c` قرمز است:** تست `banksApi.list returns mock catalog when mock mode is enabled` بدون `VITE_USE_MOCK=true` به `http://localhost:3000/api/v1/banks/` می‌زند (`ECONNREFUSED`). لوکال ممکن است به‌خاطر `.env` سبز باشد؛ CI آن env را ندارد. این را در همین پرامپت درست کن.

## پوشش این پرامپت

- رفع همان پنج شکاف.
- بخش «بانک مقصد واریز» روی **مسیر فعال** `/account` → `src/features/profile/MyAccountView.vue` با `BankSelect` (کد کاتالوگ). mock در شبیه‌ساز؛ Live فقط state صفحه.
- Vitest + docs EN/FA.

صفحهٔ مرده `src/views/MyAccountView.vue` را کپی نکن و ویرایش نکن؛ الهام بصری آزاد است، مسیر فعال `features/profile` است.

---

```text
Goal: close the remaining bank-catalog UI gaps from the previous prompt, and add a catalog BankSelect for “destination payout bank” on the live My Account page. Do not add a Django/profile REST field. Do not edit unused files under src/views/.

Before coding: list remaining ambiguities. If the instructions are already complete, proceed.

## Context

- Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun only (`bun.lock`). Never create or commit `package-lock.json`. Never use npm as source of truth.
- User-facing text is Persian, RTL only. No i18n. No English UI copy.
- Do not change Django. Do not add dependencies.
- HEAD after prompt 03: `056722c`.
- Existing: `BankBadge`, `BankSelect` (`src/shared/components/BankSelect.vue`), `useBanksCatalog`, simulator catalog.
- Active account route: `/account` → `src/features/profile/MyAccountView.vue` (theme + name/email/phone). It currently has **no** IBAN/payout-bank section. The free-text “بانک مقصد واریز” lives only on unused `src/views/MyAccountView.vue` — do not edit that file; port the idea into the active page.
- Spec: no IBAN checksum / bank-prefix validation in this phase. No product-side bank CRUD in mock.

Keep these testids intact: `listing-create-page`, `listing-fill-sample`, `landing-listing-card-*`, `marketplace-listing-card`.

## A) Gaps from prompt 03 (mandatory)

### A1) Landing hero preview

File: `src/features/landing/components/LandingHeroListingsPreview.vue`

Replace the green first-letter chip + raw `listing.bank_name` with compact `BankBadge`:

```vue
<BankBadge
  :bank="listing.bank"
  :fallback-name="listing.bank_name"
  size="compact"
  theme="dark"
/>
```

Keep click → scroll to `#live-listings`, guest behavior, and existing tests that look for «بانک ملت» / listing fixtures. Update the hero test if it asserted the old chip markup.

No third-party bank CDN.

### A2) Marketplace filter uses `filters.bank` only

File: `src/features/marketplace/MarketplaceView.vue`

Today `BankSelect` is bound to `filters.bank_name` and `loadListings` copies that into `bank` without dropping `bank_name`.

Fix:

- `v-model` / `v-model:value` on `filters.bank` (catalog code). Keep `allow-all`.
- `data-testid="marketplace-bank-filter"` on that select (in addition to inherit).
- In `loadListings`:
  - if `filters.bank` is non-empty: send `bank` only; **delete `bank_name`** from the request object.
  - if empty / «همه بانک‌ها»: delete both `bank` and `bank_name`.
- Reset must clear `filters.bank` (and not leave a leftover `bank_name`).

Add or extend a vitest that `getListings` is called with `{ bank: 'mellat' }` and without `bank_name` when mellat is selected.

### A3) «همه بانک‌ها» building icon

File: `src/shared/components/BankSelect.vue`

For the `allowAll` option (`value === ''` or null): render Persian text «همه بانک‌ها» **plus** `BusinessOutline` (same icon as unknown BankBadge). Do **not** apply any catalog brand color or bank logo.

Update `BankSelect.test.ts` to assert that all-banks option is not rendered via a catalog BankBadge brand surface.

### A4) BankSelect testids

On `BankSelect` root `NSelect`:

- default `data-testid="bank-select"`
- listing create/edit usages: `data-testid="listing-form-bank"` (pass through attrs or a `data-testid` prop)
- marketplace: `marketplace-bank-filter`
- account payout: `account-payout-bank`

Fallthrough of extra attrs onto `NSelect` is fine.

### A5) Do not call createListing without a catalog code

File: `src/features/listings/composables/useListingForm.ts` (`publishListing`)

After `findBankByCode` then `findBankByNameOrAlias`:

- if no match: show the existing Persian error (`message.error`) and **return false without** calling `listingsApi.createListing`.
- do not fall back to sending the raw unmatched string as `bank`.

`isFormValid` / step1 should treat empty bank as invalid (already requires non-empty trim; also require `findBankByCode` **or** alias match).

### A6) GitHub Actions: mock catalog test must not hit the network (CI is currently red)

File: `src/api/banks.test.ts` (and any other new test that calls `setMockMode(true)` then `banksApi.list()` / `fetchBanks()`).

`setMockMode(true)` is a **no-op** unless `import.meta.env.VITE_USE_MOCK === 'true'` (see `src/api/client.ts` and `src/api/client.test.ts`). GitHub Actions does not set that env, so the “mock catalog” test currently does `GET http://localhost:3000/api/v1/banks/` and fails with `ECONNREFUSED`.

Fix the failing test (and copy the same pattern wherever mock mode is required):

```ts
beforeEach(() => {
  vi.stubEnv('VITE_USE_MOCK', 'true'); // for mock-path tests
  setMockMode(true);
});
```

For the live-path tests in the same file, stub `VITE_USE_MOCK` to `'false'` and spy `api.get` / `api.post` as they already do.

Also spy `api.get` in the mock list test and assert it was **not** called.

Follow `src/api/client.test.ts`: `vi.unstubAllEnvs()` in `beforeEach`/`afterEach` so tests do not leak env into BankSelect/`fetchBanks` mounts.

Failed CI runs: [CI #33 on 056722c](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32267063505) and [CI #32 on ebf75f1](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32262470474). Same failure in CD Demo workflows.

## B) My Account — destination payout bank

File: `src/features/profile/MyAccountView.vue` only.

Add a card (Persian title e.g. «تنظیمات حساب بانکی و واریز») with:

1. `BankSelect` `allowAll=false`, label «بانک مقصد واریز», testid `account-payout-bank`. Value is catalog **code**.
2. Optional IBAN `NInput` for layout parity with the old unused page. Do **not** invent IBAN validation (out of scope). Placeholder/sample text may stay; saving IBAN may remain page-local even in mock.

Persistence:

- **Mock** (`isMock()` true): store the selected bank **code** on the simulator, keyed by current user id (e.g. `payoutBankCode` on the user record or a `Record<userId, code>` map). Persist with existing `persist()` / `chequeyar_simulator_v1`. Reload of `/account` in mock must restore the code. Expose small helpers e.g. `getPayoutBankCode(userId)` / `setPayoutBankCode(userId, code)` and call them from the account page save — **not** via `usersApi.updateMe` (do not put `bank` on the profile PATCH body).
- **Live** (`VITE_USE_MOCK=false`): keep the selection in component/`ref` (or a tiny session memory) for this page visit only. Do **not** PATCH `/users/me/` with a bank field. Do not invent a new live endpoint.

Saving the account profile (name/email/phone) must remain unchanged. Payout bank can save with the same confirm button **or** a second “ذخیره حساب بانکی” button on that card — either is fine if mock persist vs live page-state is clear.

Seed: optional default `pasargad` for holder1 in mock to match the old unused page; not required.

No free-text `NInput` for bank name.

## C) Tests

1. Hero preview uses BankBadge (mellat fixture still shows «بانک ملت»).
2. Marketplace filter request shape (`bank` code, no `bank_name`).
3. BankSelect all-banks option has building icon / no brand color.
4. `publishListing` does not call API when bank is empty or unknown (spy `listingsApi.createListing`).
5. Mock: set payout code on simulator, re-read same code. Live: do not assert a network profile bank field.
6. `banksApi.list` mock-path test: with `VITE_USE_MOCK=true`, returns catalog and `api.get` is not called. Without that stub, CI stays red.

Run `bun run lint` and `bun run test`. No Playwright / doion e2e.

## D) Docs

Update `docs/ARCHITECTURE.md` + `.fa.md`: hero uses BankBadge; marketplace filter sends `bank` code; MyAccount payout BankSelect (mock simulator vs Live page state; no profile API).

Update Testing EN/FA with new tests.

## E) Do not

- `src/views/`
- Django / new REST profile field
- IBAN validation
- Bank logo CDN
- `package-lock.json` / npm
- English UI copy
- Unrelated refactors
- Changing listing-create e2e-visible labels

## F) Acceptance

- Landing hero shows BankBadge (catalog color/letter or unknown), not the old emerald chip.
- Marketplace «ملت» filter → `getListings({ bank: 'mellat' })` without `bank_name`.
- «همه بانک‌ها» = text + generic building icon.
- Empty/invalid listing bank does not hit createListing.
- `/account` BankSelect stores code in simulator when mock; Live stays on the page only.
- Lint + tests pass.

## G) After you finish

Commit:

`feat(banks): add payout bank select and close catalog UI gaps`

Reply with SHA, files changed, lint/test results, and how mock vs Live payout persistence works.
```
