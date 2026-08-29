# پرامپت C — دور اصلاح پس از بازبینی کامیت `6fa040a`

پیگیری [`03-live-data-and-forms.md`](03-live-data-and-forms.md) و [`03-live-data-and-forms-clarifications.md`](03-live-data-and-forms-clarifications.md).

## چه چیزی درست بود (تأیید زنده)

- چهار کارت از شبیه‌ساز؛ slice به ۴؛ بدون `getListingDetail`.
- مهمان: کلیک کارت → `/login`، بدون درخواست احراز هویت.
- واردشده: کلیک کارت → `/listings/101`.
- `show_risk_tier` خاموش → صفر badge.
- `landing-lead-role` دقیقاً یک عنصر (select).
- موبایل نامعتبر → خطای فیلد، بدون toast؛ payload معتبر → جمله موفقیت قفل‌شده و ریست فرم؛ بدون `axios`/`fetch`.
- تماس خالی → خطای نام.
- ۳۶۰px بدون اسکرول افقی.
- `tsc` تمیز؛ ۱۱۵ تست vitest پاس.

سه ایراد کوچک باقی است. منطق آگهی و فرم را بازنویسی نکن.

---

```text
I reviewed commit 6fa040a live with Playwright. The listings and forms work. Do not rewrite them.

Confirmed: 4 simulator cards; guest card click → `/login` with no listing-detail request; signed-in → `/listings/101`; no risk badge while `show_risk_tier` is off; one `landing-lead-role` select; invalid mobile shows a field error and no success toast; valid lead submit shows the locked success sentence and resets the form; empty contact submit shows the name error; 360px has no horizontal scroll; 115 vitest tests pass.

Three small fixes in one commit:

## 1. Drop the LTR arrow on listing cards

`LandingListingCard.vue` still renders `&larr;` in the card footer. Prompt 02 already banned that arrow on the hero tertiary link. Remove it. The Persian hint text is enough.

Also replace the guest hint «ورود برای معامله» — the platform does not execute the trade. Use «ورود برای مشاهده» (and keep signed-in as «مشاهده جزئیات»). Put both hint strings in `landingContent.liveListings` so they are not hardcoded in the template.

## 2. `--theme-surface-hover` does not exist

The card uses `hover:bg-[var(--theme-surface-hover)]`. That custom property is not defined anywhere in this repo, so hover background is a no-op. Use an existing token, e.g. `hover:bg-[var(--theme-surface-muted)]`.

## 3. `animate-pulse` on the loading skeleton

Prompt 03 said no `animate-pulse` (same design-system rule as the hero badge). Keep the four static skeleton blocks and `min-h-[280px]`; just drop the `animate-pulse` class.

Do not change fetch logic, validators, routing, or locked form/empty-state copy. Run `bun run lint` and `bun run test`. Reply with the SHA.
```
