# پرامپت C — پاسخ به سؤالات رفت‌وبرگشت اول

پاسخ به پرسش‌های Studio پیش از پیاده‌سازی [`03-live-data-and-forms.md`](03-live-data-and-forms.md).

## چرا فایل جدا

همان استدلال [`01-skeleton-clarifications.md`](01-skeleton-clarifications.md): ورودی دو مسیر یکسان بماند و رفت‌وبرگشت در Step 7 قابل شمارش باشد.

## یک اصلاح

testid نقش فرم لید نباید روی هر گزینه رادیو تکرار شود (درس پرامپت ۰۱: `landing-nav-login` دو بار Playwright را شکست).

---

```text
Confirmed. Proceed with implementation, with one correction.

## Confirmed as proposed

1) `formatJalaliDate`: `Intl.DateTimeFormat('fa-IR-u-ca-persian', { year: 'numeric', month: 'long', day: 'numeric' })`. Invalid / empty / unparseable input returns `''` and never throws.

2) Discount rate: if the string is non-null and non-empty after trim, show it with `toPersianDigits` and a trailing `٪` (example: `3.80` → `۳.۸۰٪`). Keep the ASCII decimal point; do not invent `/ماه` and do not invent a fallback when the field is missing. Omit the whole rate row when null, undefined, or `''`.

3) Success toast: the exact sentence from the prompt on both forms, then reset. Zero `axios` / `api.post` / `fetch(` in the new landing files.

4) Card navigation and `getLandingListingTarget(isAuthenticated, listingId)`: guest → `/login`, signed-in → `/listings/${id}`. Unit-test both.

## One correction — lead role testid

Do not put `data-testid="landing-lead-role"` on every radio button. That repeats the prompt-01 header bug (strict-mode locator resolves to 3 elements).

Prefer `NRadioGroup` / `NSelect` with **one** `landing-lead-role` on the group/select root. If you also want per-option hooks, they must be unique: `landing-lead-role-check-holder`, `landing-lead-role-investor`, `landing-lead-role-other`.

Internal values `check_holder` | `investor` | `other` are fine. UI labels stay the Persian strings in `landingContent.ts`. `validateLeadForm` accepts those three internal keys (missing/other values → role error). Never show `check_holder` / `user_type` to the guest.

## Still required (your summary omitted these)

- Slice to 4 after `marketplaceApi.getLatestListings()`; do not call `getListingDetail`.
- Do not import `LatestListingsWidget` or `ListingCard`.
- Four listings states with the specified testids; empty CTA is «ثبت‌نام» `/register` for guests and «ورود به بازارچه» `/marketplace` for signed-in users.
- `risk_tier` only when `showRiskTier` is true; badge testid `landing-listing-risk-tier`.
- Loading skeleton height close to 4 cards (no layout jump).
- Contact fields: name, email, message with the stated rules and `:input-props` testids.
- New static copy in `landingContent.ts` with `\u200c` where Persian typography needs it. No «مطالبات».
- Unique testids in any viewport (same rule as prompt 01).
- Docs + `bun run lint` + `bun run test` in the same commit.

Go ahead. In your reply: changed files as code / tests / docs, the new data-testid list, confirmation of zero form network calls, lint/test results, and the commit SHA.
```
