# پرامپت ۰۲ — `banksApi`، شبیه‌ساز، و `useBanksCatalog`

خروجی Step 5 از [`implementation_plan.md`](../implementation_plan.md). مرجع رفتار: [`feature_spec.md`](../feature_spec.md) قوانین ۲۱–۲۸ و سناریوهای ۴–۶، ۹–۱۰، ۱۳. قرارداد Live: `GET /api/v1/banks/` آرایهٔ بدون صفحه‌بندی؛ `POST`/`PATCH` آگهی فیلد `bank` (کد کاتالوگ)؛ ورودی `bank_name` رد می‌شود.

## قاعده اجرا

این متن **فقط در Google AI Studio** روی ریپوی فعال UI (`checkyar-googleai`) اجرا می‌شود. از Cursor یا کلون لوکال روی این ریپو commit/push نکنید.

فقط بلوک `text` پایین را در Studio بچسبانید.

## پیش‌نیاز

پرامپت ۰۱ باید قبلاً اجرا و پذیرفته شده باشد. HEAD مورد انتظار UI پس از ۰۱: `78cc10c`. موجود است:

- `src/shared/banks/catalog.ts` — `LOCAL_BANKS` (۱۴ ردیف، `logo_url: null`)
- `src/shared/banks/lookup.ts` — `findBankByCode`, `findBankByNameOrAlias`, `getBankBrandColor`
- `src/shared/components/BankBadge.vue` — هنوز به صفحات وصل نشده
- `src/types/api.ts` — `Bank` / `BankSummary`؛ listingها هنوز فقط `bank_name` دارند؛ `CreateListingRequest` هنوز `bank_name`

## پوشش این پرامپت

- کلاینت `banksApi.list()` و hydrate شبیه‌ساز با همان ۱۴ بانک.
- شیء تو‌در‌توی `bank` روی آگهی‌ها؛ write با کد؛ فیلتر بازارچه مثل Live.
- `useBanksCatalog` (mock بدون HTTP؛ Live با فال‌بک محلی).
- Vitest + docs EN/FA.

**وصل کردن `BankBadge` / `BankSelect` به کارت‌ها، فیلتر بازارچه، و جایگزینی `NSelect` نام بانک در پرامپت ۰۳ است.** در این قدم فقط قرارداد داده و payload ثبت/ویرایش را هم‌راستا کن تا mock نشکند.

## تصمیم‌های قفل‌شده

- منبع واحد ۱۴ بانک: `LOCAL_BANKS`. شبیه‌ساز همان آرایه را import می‌کند؛ فهرست ۱۴تایی دوم نساز.
- `GET /api/v1/banks/` در Live با `unwrapList` (اگر آرایه خام آمد همان؛ اگر `{ results }` آمد `results`).
- اگر هم `bank` و هم `bank_name` در فیلتر بازارچه باشند، **`bank` برنده است** (مثل بک‌اند).
- لوگو در seed شبیه‌ساز `null` می‌ماند مگر صریحاً در fixture تست غیر null شود.
- `package-lock.json` ممنوع؛ فقط Bun.

---

```text
Goal: wire the bank catalog into the API client and the in-memory backend simulator so mock and Live share the same listing/bank JSON shape as Django. Do not replace listing-card building icons with BankBadge, do not invent BankSelect, and do not restyle marketplace/filter/landing in this prompt.

Before coding: list remaining ambiguities. If the instructions are already complete, proceed.

## Context

- Active Cheque Yar UI: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun only (`bun.lock`). Never create or commit `package-lock.json`. Never use npm as the package manager of record.
- All user-facing text is Persian, RTL only. No i18n. No English UI copy.
- Backend lives in a separate Django monorepo. Do NOT change, invent, or mock Django files.
- Do not edit unused duplicates under `src/views/`.
- Do not add npm/bun dependencies.
- Prerequisite (prompt 01): `LOCAL_BANKS`, lookup helpers, `BankBadge` exist and are not wired into pages. Keep pages visually as they are except where TypeScript forces a payload field rename on create/update.

Live contract to match:

- `GET /api/v1/banks/` — AllowAny, unpaginated JSON array of active banks ordered by `display_name`. Shape: `{ code, display_name, aliases, logo_url, brand_color_light, brand_color_dark }`.
- Nested listing `bank` is `BankSummary` (same fields minus `aliases`) or `null`. Display `bank_name` remains.
- `POST /api/v1/listings/` and `PATCH /api/v1/listings/{id}/` write `bank` as catalog **code** string. Sending `bank_name` instead of `bank` is `400 VALIDATION_ERROR`. Invalid code is also validation error.
- Marketplace: `?bank=` exact `bank.code`; `?bank_name=` partial match on stored name / catalog display_name / aliases. If both query params are present, `bank` wins.

## 0) Small BankBadge carry-over (spec gap)

Unknown state in `BankBadge.vue` currently shows only `BusinessOutline`. Spec requires building icon **plus** the first character of `fallbackName` (or a simple placeholder character if empty), still with **no** catalog brand color. Fix that in this prompt and extend `BankBadge.test.ts`. Do not wire the badge into pages.

## 1) Types (`src/types/api.ts`)

Add nested `bank: BankSummary | null` to:

- `ChequeListing`
- `MarketplaceListing`
- `MarketplaceLatestListing`
- `ModerationQueueItem`
- `ListingSummary` (matches)

Keep `bank_name: string` on those types.

Change write types:

```ts
export interface CreateListingRequest {
  issuer?: number;
  bank: string; // catalog code, e.g. "mellat"
  cheque_serial_number: string;
  face_amount: number | string;
  due_date: string;
  issuer_type: IssuerType;
  issuer_name: string;
  issuer_national_id: string;
  description?: string;
  suggested_discount_rate?: string | null;
}
```

Do **not** keep `bank_name` on `CreateListingRequest` / `UpdateListingRequest`. Call sites must send `bank`.

`ListingFilters`: add optional `bank?: string` (exact code). Keep optional `bank_name?: string`.

Add a tiny helper (e.g. in `src/shared/banks/lookup.ts`) `toBankSummary(bank: Bank): BankSummary` that omits `aliases`.

## 2) `banksApi` (`src/api/index.ts`)

```ts
export const banksApi = {
  list: async (): Promise<Bank[]> => {
    if (isMock()) return useBackendSimulatorStore().listBanks();
    const res = await api.get('/banks/');
    return unwrapList<Bank>(res.data);
  },
};
```

Export `Bank` / `BankSummary` from `src/api/index.ts` if other modules import types from there.

`listingsApi.createListing` / `updateListing` (Live branch): send `bank` (code). Never send `bank_name` on the JSON body. Keep existing issuer-profile get-or-create logic.

If a Live payload still has leftover `bank_name` from older callers, strip it before `api.post` / `api.patch`.

## 3) Simulator (`src/stores/useBackendSimulatorStore.ts`)

Import `LOCAL_BANKS` and lookup helpers. Do not duplicate the 14-bank table.

### 3.1 Catalog

- Keep an in-memory list seeded from `LOCAL_BANKS` (`logo_url: null`).
- Expose `listBanks(): Bank[]` returning that list (same order as `LOCAL_BANKS` / API: `display_name` ascending).
- Mock admin cannot create banks or upload logos.

### 3.2 Seed listings / matches / moderation

Every seeded listing (and nested match `listing` summaries) MUST include:

- `bank: BankSummary | null`
- `bank_name` equal to that bank's `display_name` when mapped

Resolve via `findBankByNameOrAlias` of the current seed `bank_name` strings (ملت، پاسارگاد، ملی ایران، …).

**Unknown sample (mandatory):** exactly one seeded published listing has `bank: null` and a `bank_name` that is **not** a catalog display_name/alias (e.g. a made-up unmapped name). Other seeds stay mapped.

### 3.3 Persist hydration

`localStorage` key `chequeyar_simulator_v1` may contain old listings without `bank`. On `init`, if a listing lacks `bank` (undefined), hydrate: lookup by `bank_name`; if found set nested summary + canonical `display_name`; else `bank: null`. Do not wipe user simulator data unless you already have a reset path.

### 3.4 createListing / updateListing

Require `req.bank` (trimmed catalog code of an **active** seeded bank).

- Missing `bank`, or `bank_name` present without `bank`: throw the existing `createErrorEnvelope('VALIDATION_ERROR', …)` with field details on `bank` (Persian message is fine).
- Unknown code: same `VALIDATION_ERROR`.
- On success: set nested `bank` via `toBankSummary`, set `bank_name` to `display_name`. Do not store the raw code in `bank_name`.

Follow the existing throw style (`throw createErrorEnvelope(...)`).

### 3.5 Marketplace filters

In `getMarketplaceListings`:

- If `filters.bank` is non-empty: keep results whose `bank?.code === filters.bank` (exact). Ignore `bank_name` when `bank` is set.
- Else if `filters.bank_name` is non-empty: keep results where the query is a case-sensitive substring of `bank_name` **or** nested `bank.display_name` **or** any alias of that catalog bank (use `LOCAL_BANKS` / the seeded bank’s aliases). Unmapped listings (`bank === null`) only match against their stored `bank_name`.

Replace the current `r.bank_name.includes(filters.bank_name)` as the sole rule.

### 3.6 Axios mock interceptor (`src/api/client.ts`)

Route `GET` URLs containing `/banks` (and not some other resource) to `simulator.listBanks()`. Place it so it does not steal `/marketplace/...` routes.

## 4) `useBanksCatalog`

New composable, e.g. `src/shared/banks/useBanksCatalog.ts` (or `src/shared/composables/`).

Behavior:

- Mock (`isMock()` true): set banks from `banksApi.list()` / simulator / `LOCAL_BANKS` — **no HTTP**. Prefer going through `banksApi.list()` so the mock branch is the real path.
- Live: call `banksApi.list()`. On any failure (network, 404, 500): use `LOCAL_BANKS` as fallback. Do **not** set a full-page error; expose `hasError` optionally but keep `banks` populated from local catalog (spec rule 28 / scenario 13).
- Return at least `{ banks, isLoading, hasError, refetch }`.
- Deduplicate in-flight fetches similarly to `useLandingLatestListings` if easy; do not over-engineer.

Do **not** switch marketplace `NSelect` or listing forms to this composable for option lists in this prompt (that is prompt 03). You MAY use a small mapper on **submit** only (next section).

## 5) Create/update payload mapping (minimal, so mock create still works)

Active create/edit currently send `bank_name: formData.bank` (a Persian label). After types change they must send `bank: <code>`.

In `src/features/listings/` only (not `src/views/`):

- `useListingForm.ts`
- `ListingEditView.vue`
- `ListingCreateView.vue` if it is the active route

On submit: resolve the current form string with `findBankByCode` first, then `findBankByNameOrAlias`. If resolved, send `{ bank: code, ... }` and omit `bank_name`. If not resolved, do not call the API; show the existing form error pattern (Persian).

Do **not** replace the form `NSelect` with BankSelect/BankBadge. Keep current options arrays.

Leave marketplace filters sending `bank_name` as they do today (simulator still supports it). Prompt 03 will switch the filter to `bank` codes.

## 6) Tests (Vitest)

Add focused tests (colocate or under `src/api/` / `src/stores/` / `src/shared/banks/`). Must cover:

1. Mock mode: `banksApi.list()` returns 14 banks and does **not** call `api.get` / axios. Use `VITE_USE_MOCK=true`, `setMockMode(true)`, and spy/mock axios.
2. Live fail: with `VITE_USE_MOCK=false`, if `banksApi.list` / the composable’s fetch rejects, `useBanksCatalog` still exposes the 14 local banks (no empty catalog).
3. Simulator `createListing` with `bank: 'mellat'` returns nested `bank.code === 'mellat'` and `bank_name === 'بانک ملت'`.
4. Simulator `createListing` with only `bank_name` (cast if needed) throws/rejects `VALIDATION_ERROR`.
5. Simulator marketplace `bank: 'mellat'` does not include a تجارت listing; `bank_name: 'ملی'` still matches بانک ملی ایران (alias/partial).
6. BankBadge unknown state includes first letter of `fallbackName`.

Update listing fixtures in existing tests (`LiveListingsSection.test.ts`, `LandingHeroListingsPreview.test.ts`, feature-flag tests, etc.) so they satisfy `bank: BankSummary | null` (can be `null` plus `bank_name`).

Run `bun run lint` and `bun run test`. Do not add Playwright or doion e2e here.

## 7) Docs (this repo, same commit, EN + FA)

Update `docs/ARCHITECTURE.md` + `docs/ARCHITECTURE.fa.md`:

- `banksApi.list()` mock vs Live (`GET /banks/` + `unwrapList`).
- Simulator seeds the same 14 banks; listings carry nested `bank`.
- `useBanksCatalog`: Live success = API; Live failure = `LOCAL_BANKS`; mock = no HTTP.
- Page wiring of BankBadge is still a follow-up.

Update `docs/TESTING.md` + `docs/TESTING.fa.md` with the new vitest files and a short mock-vs-Live catalog note.

Do not document Django internals.

## 8) Do not

- Commit `package-lock.json` or use npm as source of truth.
- Add dependencies.
- Touch `src/views/`.
- Wire `BankBadge` into ListingCard, landing cards, marketplace table, matches, moderation, or filters.
- Add BankSelect or change marketplace filter to send `bank` codes (keep `bank_name` query from the current NSelect).
- Load logos from bank websites/CDNs.
- English user-facing copy.
- Unrelated refactors.
- My Account destination-bank field (later prompt).

## 9) Acceptance

- `banksApi.list()` in mock returns 14 banks with zero HTTP.
- Live catalog composable falls back to `LOCAL_BANKS` on failure without blocking the page.
- Seeded listings (except the one unknown sample) have nested `bank`.
- Mock create with `mellat` matches Live shape; `bank_name`-only create is rejected.
- Marketplace simulator filters match the Live precedence rules.
- `bun run lint` and `bun run test` pass.
- Docs EN+FA updated.

## 10) After you finish

Commit in this GitHub-connected AI Studio project:

`feat(banks): add catalog API client and simulator seed`

Reply with:

1. The commit SHA
2. Files added/changed
3. Lint and test command results
4. How mock `GET /banks/` is routed (banksApi vs interceptor)
```
