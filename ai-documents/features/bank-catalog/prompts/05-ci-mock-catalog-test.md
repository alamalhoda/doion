# پرامپت ۰۵ — سبز کردن CI: تست mock کاتالوگ بدون HTTP

Follow-up بعد از پرامپت ۰۴. پرامپت ۰۴ برای اجرا رفته است؛ این متن را **بعد از commit شدن ۰۴** در Studio بچسبانید (نه هم‌زمان با ۰۴).

مرجع شکست: [CI روی `056722c`](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32267063505) و [CI روی `ebf75f1`](https://github.com/alamalhoda/checkyar-googleai/actions/runs/32262470474). هر دو: `src/api/banks.test.ts` → `banksApi.list returns mock catalog when mock mode is enabled` → `GET http://localhost:3000/api/v1/banks/` → `ECONNREFUSED`.

## قاعده اجرا

فقط در Google AI Studio روی `checkyar-googleai`. از Cursor روی آن ریپو commit/push نکنید.

فقط بلوک `text` پایین را بچسبانید.

## پیش‌نیاز

پرامپت ۰۴ باید commit شده باشد. اگر ۰۴ همین تست را درست کرده و CI سبز است، این پرامپت را اجرا نکنید.

---

```text
Goal: make GitHub Actions CI green by fixing unit tests that pretend to be in mock mode but still call the live HTTP client. Do not add features. Do not edit src/views/. Do not change Django.

Before coding: if banks.test.ts already stubs VITE_USE_MOCK='true' before setMockMode(true) and spies that api.get is not called, and bun run test would pass on a runner without .env, stop and say so.

## Why CI fails (and local may pass)

`setMockMode(true)` in `src/api/client.ts` is a no-op unless `String(import.meta.env.VITE_USE_MOCK) === 'true'`. GitHub Actions CI does not set that env. A local `.env` with VITE_USE_MOCK=true is gitignored, so `bun run test` can pass on a laptop and fail on Actions.

The failing assertion is in `src/api/banks.test.ts`:
`banksApi.list returns mock catalog when mock mode is enabled`
It currently only calls `setMockMode(true)`, then `banksApi.list()`, which hits `GET /api/v1/banks/` against localhost:3000.

Pattern that already works: `src/api/client.test.ts` (`vi.stubEnv('VITE_USE_MOCK', 'true')` then `setMockMode(true)`; `vi.unstubAllEnvs()` in beforeEach).

## Required changes

1. `src/api/banks.test.ts`
   - Mock-path test: `vi.stubEnv('VITE_USE_MOCK', 'true')` then `setMockMode(true)` then `banksApi.list()`. Spy `api.get` and expect it was **not** called. Result still includes `mellat`.
   - Live-path tests in the same file: `vi.stubEnv('VITE_USE_MOCK', 'false')` before `setMockMode(false)` and keep existing axios spies.
   - `afterEach` (or each `beforeEach`): `vi.unstubAllEnvs()` so env does not leak into other files (BankSelect `onMounted` → `fetchBanks` → `banksApi.list()`).

2. Search the repo for other tests added in prompt 04 that call `setMockMode(true)` or `banksApi.list()` / `fetchBanks()` without stubbing `VITE_USE_MOCK`. Apply the same stub. Do not “fix” tests that already spy axios for the live path.

3. Do not change production `client.ts` mock gating to make CI green (that gate is intentional).

## Do not

- New UI, new endpoints, package-lock.json, npm, src/views/, Django.
- Unrelated refactors.

## Acceptance

- `bun run lint` and `bun run test` pass.
- The mock catalog test does not perform HTTP.
- After this commit, GitHub Actions CI and CD Demo on `main` should pass (same jobs that failed on ebf75f1 / 056722c).

## After you finish

Commit: `test(banks): stub VITE_USE_MOCK so catalog mock tests skip HTTP`

Reply with SHA, files changed, lint/test results.
```
