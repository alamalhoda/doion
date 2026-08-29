# پرامپت ۰۱ — کاتالوگ محلی و `BankBadge`

خروجی Step 4 از [`implementation_plan.md`](../implementation_plan.md). مرجع رفتار: [`feature_spec.md`](../feature_spec.md) §۲.۱ (حالت‌های نشان بانک)، §۳.۱ (۱۴ بانک)، قوانین ۸، ۱۲، ۱۶، ۱۸، ۲۶.

## قاعده اجرا

این متن **فقط در Google AI Studio** روی ریپوی فعال UI (`checkyar-googleai`) اجرا می‌شود. از Cursor یا کلون لوکال روی این ریپو commit/push نکنید.

فقط بلوک `text` پایین را در Studio بچسبانید.

## پوشش این پرامپت

- کاتالوگ محلی هم‌مجموعه ۱۴ بانک با `code`های قفل‌شده (SSOT کلاینت برای mock و fallback بعدی).
- کامپوننت `BankBadge` بدون اتصال به صفحات (YAGNI).
- Vitest برای lookup alias، unknown، و رنگ تم.
- Docs Architecture EN+FA.

اتصال به کارت‌ها، فیلترها، شبیه‌ساز، و `banksApi` در پرامپت‌های بعدی است.

## تصمیم‌های قفل‌شده

- `code`ها باید با بک‌اند یکی باشند (جدول داخل بلوک `text`).
- رنگ seed تقریبی `#RRGGBB` است؛ هویت بصری رسمی برند قفل نیست.
- تم پیش‌فرض محصول تیره است؛ بدون لوگو از `brand_color_dark` استفاده شود.
- لوگو فقط از `logo_url` خود محصول؛ CDN/دامنه بانک‌ها ممنوع.
- `BankSelect` و تعویض `NSelect`های فعلی در این قدم نیست.

---

```text
Goal: add a single local bank catalog module and a reusable BankBadge component in this UI repo. Do not wire the badge into pages, filters, forms, or the simulator in this prompt. That comes later.

Before coding: list any remaining ambiguities. If the instructions are already complete, proceed.

## Context

- This repo is the active Cheque Yar UI: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun lockfile only (`bun.lock`). Never create or commit `package-lock.json`. Never use npm as the package manager of record.
- All user-facing text is Persian and the app is RTL only. No i18n layer. No English UI copy.
- The backend is a separate Django monorepo (doion). Do NOT change, mock out, or invent backend code, endpoints, or Django files.
- Do not touch legacy unused duplicates under `src/views/`.
- Do not add new npm/bun dependencies.
- Current listing cards show a generic `BusinessOutline` building icon plus `bank_name` text. Leave those call sites unchanged in this prompt.
- Product default theme is dark (`data-theme="dark"`). Light theme colors exist for later use.

## 1) Local catalog SSOT

Create one catalog module, for example:

- `src/shared/banks/catalog.ts`
- `src/shared/banks/lookup.ts` (pure functions; easy to unit-test)

The catalog MUST contain exactly these 14 banks. Codes are locked and must match the backend:

| code | display_name | aliases (minimum) | brand_color_light | brand_color_dark |
|------|----------------|-------------------|-------------------|------------------|
| mellat | بانک ملت | بانک ملت | #E21836 | #C4112C |
| melli | بانک ملی ایران | بانک ملی ایران, بانک ملی | #0057A0 | #004080 |
| saderat | بانک صادرات ایران | بانک صادرات ایران, بانک صادرات | #1A7A3A | #14622E |
| pasargad | بانک پاسارگاد | بانک پاسارگاد | #F5A623 | #C48412 |
| tejarat | بانک تجارت | بانک تجارت | #003DA5 | #002D7A |
| saman | بانک سامان | بانک سامان | #00A0E3 | #007FB5 |
| parsian | بانک پارسیان | بانک پارسیان | #8B1E3F | #6E1832 |
| sepah | بانک سپه | بانک سپه | #1B4F72 | #153D59 |
| ayandeh | بانک آینده | بانک آینده | #E67E22 | #B85F14 |
| maskan | بانک مسکن | بانک مسکن | #27AE60 | #1E8449 |
| shahr | بانک شهر | بانک شهر | #8E44AD | #6C3483 |
| keshavarzi | بانک کشاورزی | بانک کشاورزی | #229954 | #1A7439 |
| refah | بانک رفاه کارگران | بانک رفاه کارگران | #16A085 | #117A65 |
| sina | بانک سینا | بانک سینا | #2C3E50 | #1A252F |

Each catalog row shape (TypeScript), aligned with `GET /api/v1/banks/` items:

```ts
export interface Bank {
  code: string;
  display_name: string;
  aliases: string[];
  logo_url: string | null;
  brand_color_light: string; // #RRGGBB
  brand_color_dark: string;  // #RRGGBB
}
```

Local seed: `logo_url` is `null` for every row. `aliases` must include `display_name`.

Export:

- `LOCAL_BANKS: readonly Bank[]` (stable order: `display_name` ascending, same as the API).
- `findBankByCode(code: string): Bank | undefined` (trim; exact code match).
- `findBankByNameOrAlias(name: string): Bank | undefined` (trim leading/trailing whitespace; exact match against `display_name` or any alias; do not use fuzzy/substring match).

Put `Bank` in `src/types/api.ts` (or re-export from the catalog) so later prompts can attach `bank: BankSummary | null` on listings. For this prompt, a summary type without `aliases` may also be added as `BankSummary`. Do NOT yet change `CreateListingRequest.bank_name` or listing interfaces to require nested `bank` — that is the next prompt.

Do not duplicate this 14-bank list in any form/filter in this prompt. Existing hardcoded `bankOptions` arrays stay as they are until a later prompt.

## 2) BankBadge

New shared component: `src/shared/components/BankBadge.vue`.

Props (keep them explicit and typed):

- `bank`: `BankSummary | Bank | null | undefined` — catalog object when known.
- `fallbackName`: optional string — stored `bank_name` when `bank` is null (unknown / unmapped listing).
- `theme`: `'dark' | 'light'`, default `'dark'`.
- `size`: `'default' | 'compact'`, default `'default'`.
- `showName`: boolean, default `true`.

Visual states (mandatory):

1. Catalog bank with non-null `logo_url`: render an `<img>` of that URL next to the display name. Never load logos from a third-party bank CDN or bank website. If `logo_url` is a relative media path, that is fine.
2. Catalog bank with `logo_url === null`: first character of `display_name` on a colored surface. Dark theme uses `brand_color_dark` as the surface; light theme uses `brand_color_light`. Text on the surface must stay readable (white or near-white is acceptable).
3. Unknown / no catalog match (`bank` is null/undefined): current building icon (`BusinessOutline` from `@vicons/ionicons5`, already used on listing cards) PLUS the first character of `fallbackName` (or a simple fallback character if the name is empty). Do NOT apply any catalog brand color.
4. Compact vs default: compact is a smaller mark suitable for table cells and select option rows; default matches the ~36px mark used on listing cards today.

Accessibility:

- The mark is decorative if the name is shown beside it (`aria-hidden` on the icon/img).
- If `showName` is false, give the root an accessible name from `display_name` or `fallbackName`.
- Keyboard: the badge is display-only (not a button) unless you wrap it later.

data-testid (kebab-case, same convention as `marketplace-listing-card`):

- `bank-badge` on the root
- `bank-badge-logo` when showing an image
- `bank-badge-initial` when showing the letter on brand color
- `bank-badge-unknown` when showing the unknown/building state

Do not invent BankSelect in this prompt.

## 3) Tests (Vitest only)

Add colocated tests, for example `src/shared/banks/lookup.test.ts` and a BankBadge test if you mount the component (optional if lookup + a small pure helper for “which visual state / which color” is easier).

Must cover:

- `findBankByCode('mellat')` -> بانک ملت
- `findBankByNameOrAlias('  بانک ملی  ')` -> melli / بانک ملی ایران
- unknown name -> undefined
- theme color helper: dark -> `brand_color_dark`, light -> `brand_color_light`
- unknown badge path does not use catalog brand colors

Run `bun run lint` (tsc) and `bun run test`. Report results in your reply. Do not add Playwright or doion e2e in this repo.

## 4) Documentation (this repo, same commit, bilingual EN + FA)

Update only what this change touches:

- `docs/ARCHITECTURE.md` and `docs/ARCHITECTURE.fa.md`: mention `src/shared/banks/` as the client SSOT catalog (mock + future live fallback), and `BankBadge` in `src/shared/components/`. State that page wiring is a follow-up.
- `docs/TESTING.md` and `docs/TESTING.fa.md`: list the new vitest files.

Do not document Django internals; the API contract lives in the doion monorepo.

## 5) Do not

- Commit `package-lock.json` or run npm as the source of truth.
- Add new dependencies.
- Touch `src/views/`.
- Call `GET /api/v1/banks/` yet, or add `banksApi`.
- Change `useBackendSimulatorStore` listing payloads.
- Replace `bankOptions` or `BusinessOutline` on ListingCard / landing / marketplace / forms.
- Load images from bank official websites or CDNs.
- Add English user-facing copy.
- Unrelated refactors.

## 6) Acceptance

- `LOCAL_BANKS` has 14 rows with the locked codes above; `logo_url` is null.
- Lookup by alias «بانک ملی» returns melli.
- BankBadge stories/states: logo (can be tested with a fake data-URL or by passing a non-null logo_url without networking), initial+dark color, unknown+building.
- No page in the running app looks different yet (no wiring).
- `bun run lint` and `bun run test` pass.
- Docs updated EN+FA.

## 7) After you finish

Commit in this GitHub-connected AI Studio project with a conventional message such as:

`feat(banks): add local catalog and BankBadge`

Reply with:

1. The commit SHA
2. Files added/changed
3. Lint and test command results
4. The exact data-testid strings
```
