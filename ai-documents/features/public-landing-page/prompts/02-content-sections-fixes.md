# پرامپت B — دور اصلاح پس از بازبینی کامیت `568cf01`

پیگیری اجرای [`02-content-sections.md`](02-content-sections.md) و [`02-content-sections-clarifications.md`](02-content-sections-clarifications.md).

## چرا فایل جدا

همان استدلال فایل‌های clarifications قبلی: سه بلوک (پرامپت، clarifications، دور اصلاح) در sandbox هم به همین ترتیب پیست می‌شود تا شمارش رفت‌وبرگشت معتبر بماند.

## چه چیزی درست بود (تأیید زنده)

- ۹ بخش محتوایی با همان `id` / `data-testid` و ترتیب تأییدشده؛ سه placeholder باقی ماند.
- متن‌های قفل‌شده §۲.۵، §۲.۶، disclaimer تعرفه، و ۶ پرسش/پاسخ FAQ عیناً روی صفحه؛ A1 شامل «نگه‌داری».
- CTA هیرو مهمان/واردشده، لینک tertiary، اسکرول سرمایه‌گذاری به `#contact-us`.
- FAQ شش آیتم، پیش‌فرض بسته، `aria-expanded`.
- فوتر از `landingContent` جمله پایانی §۲.۵ را می‌گیرد.
- ۳۶۰px بدون اسکرول افقی.
- `tsc --noEmit` تمیز؛ ۸۶ تست vitest پاس.

## چهار ایراد

ادعای عملیاتی اختراع‌شده، زبان «مطالبات»، رنگ خارج از توکن، و متن inline خارج از SSOT. جزئیات در بلوک زیر.

---

```text
I reviewed commit 568cf01 against the prompt and verified the page live with Playwright.

## Confirmed working, no change needed

Locked strings are intact: §2.5 four statements + closing sentence, §2.6 badge and product-status body, pricing no-fee disclaimer, all 6 FAQ Q&As including «نگه\u200cداری» in A1. Guest hero CTAs are ثبت‌نام / ورود plus the tertiary «مشاهده بازارچه» link; signed-in hero is ورود به بازارچه / مشاهده آگهی‌ها with no tertiary. Investing CTA scrolls to #contact-us. FAQ items 1–6 start collapsed. Placeholders for live-listings, contact-us, and lead-capture-form remain. Footer imports the §2.5 closing sentence. No horizontal scroll at 360px. `tsc --noEmit` is clean and 86 vitest tests pass.

Four things need fixing in a single commit. Do not paraphrase the locked blocks while doing this.

## 1. Blocking — copy invents capabilities and uses rejected language

The locked regulatory strings are correct. The surrounding marketing copy is not.

Replace these four strings in `landingContent.ts` exactly:

a) `productStatus.description` currently claims the product is already accepting pilot partners («هم‌اکنون در حال پذیرش شرکای پایلوت می‌باشد»). The Core Brief says the product is ready for a controlled pilot, not that partners are being onboarded. Use:

«چک\u200cیار در لایه ۱ آماده پایلوت کنترل\u200cشده است؛ نه در حال ساخت MVP، و نه عرضه عمومی. مسیر کشف و اتصال پیاده\u200cسازی شده است.»

b) Remove «مطالبات» from user-facing copy. The product is cheque liquidity, not receivables management — the same reason the prompt-01 meta description was corrected. Replace:

- `problemSolution.subtitle` → «شفاف\u200cسازی بازار غیررسمی نقدشوندگی چک\u200cهای مدت\u200cدار»
- `audiences.investors.description` → «سرمایه\u200cگذاران و شرکت\u200cهایی که به دنبال فرصت\u200cهای شفاف خرید چک مدت\u200cدار هستند.»
- `investing.description` → «چک\u200cیار از همکاری راهبردی و جذب سرمایه\u200cگذاران تخصصی برای توسعه زیرساخت فناورانه و گسترش پایلوت استقبال می\u200cکند.»

After the change, `document.body.innerText` on `/landing` must not contain «مطالبات» and must not contain «پذیرش شرکای پایلوت».

c) `audiences.investors.points[2]` currently shows the English identifier `(user_type)` to guests. Replace with:

«پشتیبانی یکپارچه از اشخاص حقیقی و حقوقی»

No other English user-facing tokens except those already locked or specified (KYC, Match, MVP, Marketplace اطلاعاتی in the hero, lead/match fee in the pricing title).

## 2. Blocking — colors outside the design-system tokens (spec rule 23)

`docs/design-system.md` for this page is the `dark` brand palette (`--theme-*`, emerald primary). The commit introduces one-off palettes:

- `amber-*` in `ResponsibilityBoundarySection.vue` and the step-6 chip in `HowItWorksSection.vue`
- `rose-*` in `ProblemSolutionSection.vue`
- `indigo-*` in `AudiencesSection.vue`

Replace all of them with `--theme-*` tokens and the existing emerald accent (`emerald-400` / `emerald-500` already used as `--theme-primary` / `--theme-primary-soft`). Problem vs solution can still be visually distinct using border weight, surface vs bg, or an icon — not a third hue.

Also remove `animate-pulse` from the hero badge and the product-status badge. Design-system §5: no looping decorative animation on the marketing site.

## 3. Static copy still lives outside `landingContent.ts`

These user-visible strings are hardcoded in templates. Move them into `landingContent.ts` (or delete the decorative chip if it adds no information):

- `ResponsibilityBoundarySection.vue`: «مرز مسئولیت رگولاتوری»
- `HowItWorksSection.vue`: «تسویه مستقیم»
- `PricingSection.vue`: «مدل آتی»

Templates must keep rendering from the SSOT. Do not leave a second copy in the Vue file.

## 4. Small

The guest tertiary hero control appends `&larr;` (LTR arrow) after «مشاهده بازارچه». Drop the arrow; the Persian label is enough.

Do not change routing, guards, auth, API, or the three placeholder sections. Do not paraphrase locked §2.5 / §2.6 / FAQ strings.

Run `bun run lint` and `bun run test`. Reply with changed files (code / tests / docs), confirmation that `/landing` as a guest no longer contains «مطالبات», «پذیرش شرکای پایلوت», or `user_type`, and the commit SHA.
```
