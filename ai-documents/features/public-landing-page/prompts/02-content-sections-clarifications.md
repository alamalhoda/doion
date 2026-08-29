# پرامپت B — پاسخ به سؤالات رفت‌وبرگشت اول

پاسخ به پرسش‌های Studio پیش از پیاده‌سازی [`02-content-sections.md`](02-content-sections.md).

## چرا فایل جدا

همان استدلال [`01-skeleton-clarifications.md`](01-skeleton-clarifications.md): ورودی دو مسیر (Studio + sandbox) یکسان بماند و «تعداد رفت‌وبرگشت» در Step 7 قابل شمارش باشد.

---

```text
Confirmed. Proceed with implementation, with one correction and a few explicit reminders.

## 1) ZWNJ canonical form — confirmed with one correction

Your proposed `\u200c` placement for §2.5, §2.6, the pricing disclaimer, and the FAQ Q&A is correct and matches the spec's visual typography (the spec source already contains U+200C in strings like «نمی‌کند», «جابه‌جا», «لانچ‌شده»).

Store every locked string in `landingContent.ts` using `\u200c` escapes exactly as you listed, EXCEPT this one fix in FAQ answer 1:

- Wrong: «نگهداری» (no ZWNJ)
- Correct: «نگه\u200cداری» (half-space between «نگه» and «داری»)

The locked answer 1 must read:

«خیر. چک\u200cیار هیچ وجهی را دریافت، نگه\u200cداری یا جابه\u200cجا نمی\u200cکند. تسویه مالی مستقیماً بین طرفین و بیرون از پلتفرم انجام می\u200cشود.»

For vitest: export the locked strings from `landingContent.ts` and assert against those exports (same pattern as `landingConstants.test.ts`). Do not duplicate string literals in the test file — single source of truth only.

Apply the same ZWNJ discipline to non-locked copy where standard Persian typography expects it (e.g. «چک\u200cهای»، «مدت\u200cدار»، «ثبت\u200cنام» in hero and how-it-works), but only the locked blocks need exact-match vitest assertions.

## 2) FAQ testids and accordion — confirmed

- `landing-faq-item-1` through `landing-faq-item-6`, 1-indexed in question order.
- All collapsed by default.
- Keyboard accessible: focusable headers, Enter/Space toggles, visible focus ring.
- Multiple items may be open at once (no forced accordion single-open unless Naive defaults require it — either is fine).

## 3) CTA anchor scrolling — confirmed

- Signed-in hero secondary CTA (`landing-hero-secondary-cta`, label «مشاهده آگهی‌ها»): smooth scroll to `#live-listings`, same `scrollIntoView({ behavior: 'smooth' })` pattern as `LandingHeader.vue`.
- Investing CTA (`landing-investing-cta`, label «تماس با ما»): smooth scroll to `#contact-us`.

Both targets are still placeholders in this prompt — scrolling to them is correct even before prompt 03 fills them in.

## Still required from the original prompt (not repeated in your summary)

- Guest-only tertiary text link «مشاهده بازارچه» → `/login` in the hero (not a third primary button).
- `#live-listings`, `#contact-us`, and `#lead-capture-form` remain minimal placeholders — do not build API or forms yet.
- Footer reconciliation (part 12): import §2.5 closing sentence from `landingContent.ts`; update bottom disclaimer line as specified.
- `landingContent.test.ts`: locked §2.5, §2.6, all 6 FAQ questions, all 6 FAQ answers (with the A1 fix above).
- Docs: `ARCHITECTURE*.md` and `TESTING*.md` in the same commit.
- Do-not list unchanged: no routing/auth/guard changes, no `axios`, no new deps, no English UI copy, no paraphrasing locked regulatory text.

Go ahead and implement. In your reply include changed files grouped as code / tests / docs, the list of new data-testid values, confirmation that locked strings were not paraphrased, lint/test results, and the commit SHA.
```
