# پرامپت A — دور اصلاح پس از بازبینی کامیت `85ec0be`

پیگیری اجرای [`01-skeleton.md`](01-skeleton.md) و [`01-skeleton-clarifications.md`](01-skeleton-clarifications.md) در Studio.

## چرا فایل جدا

مطابق همان استدلال فایل clarifications: ساختار پیام‌ها باید در هر دو مسیر یکسان بماند تا معیار «تعداد رفت‌وبرگشت» در Step 7 معتبر باقی بماند. در sandbox هم همین سه بلوک به همین ترتیب پیست می‌شود (پرامپت، پاسخ به سؤال، دور اصلاح)، حتی اگر عامل sandbox خودش این ایرادها را نداشته باشد — در آن حالت نتیجه‌اش «تغییری لازم نبود» ثبت می‌شود و این خودش یکی از داده‌های مقایسه است.

## چه چیزی درست بود (تأیید زنده، نه گزارش خودِ Studio)

اسکلت روی localhost با Playwright و Chrome بررسی شد:

- دوازده بخش با همان شناسه‌ها و همان ترتیب تأییدشده؛ فوتر آخرین عنصر.
- گیت fail-closed در همه حالت‌ها: با فلگ خاموش، هم `/` و هم `/landing` مهمان را به `/login` می‌رسانند، بدون حلقه ریدایرکت، و مقدار ذخیره‌شده فلگ در شبیه‌ساز هم بازنویسی نمی‌شود.
- کروم عمومی بدون سایدبار و هدر اپ (`<aside>` صفر).
- قفل پوسته dark بدون دست‌زدن به ترجیح کاربر: با `chequeyar_app_theme = 'light'`، ریشه صفحه `data-theme="dark"` و پس‌زمینه `rgb(2, 6, 23)` می‌ماند و مقدار ذخیره‌شده دست‌نخورده باقی می‌ماند.
- نشانگر `chequeyar_mock_signed_out`، لینک‌های placeholder فوتر با «به‌زودی» و بدون تغییر URL، و نبود اسکرول افقی در ۳۶۰px.
- `tsc --noEmit` تمیز و ۷۱ تست vitest پاس (هر دو محلی بازتولید شد).

## پنج ایراد

سه مورد blocking (نیم‌فاصله عنوان/متا، testid تکراری، حالت بارگذاری) و دو مورد مستندات و سال فوتر. جزئیات و شواهد اندازه‌گیری‌شده در بلوک زیر.

## نکته‌ای که در دور اصلاح فرستاده نمی‌شود

خلاصه‌ای که Studio برگرداند با کامیت خودش نمی‌خواند: بخش‌هایی نام برد که در کد نیستند (`social-proof`، `for-holders`، `for-investors`، `trust`، `comparison`، `final-cta`، `sticky-cta`)، از یک نوار CTA چسبان گفت که وجود ندارد، و برچسب CTA کاربر واردشده را «ورود به سامانه» گزارش کرد در حالی که کد درست «ورود به بازارچه» است. کد درست بود و گزارش غلط. برای Step 7 این ثبت می‌شود و از این پس diff مبنا است، نه خلاصه عامل.

---

```text
I reviewed commit 85ec0be against the prompt and the spec, and verified the behavior live on localhost with Playwright rather than relying on the summary.

## Confirmed working, no change needed

All 12 section ids and testids match exactly and in the confirmed order, with the footer last. The fail-closed gate is correct in every flag state: with the flag disabled, both `/` and `/landing` take a guest to `/login`, with no redirect loop, and the stored simulator value is not overwritten. The public chrome renders with no app sidebar and no app header. The dark theme is forced without touching the saved preference: with `chequeyar_app_theme = 'light'`, the landing root still renders `data-theme="dark"` with background `rgb(2, 6, 23)` and the saved value stays `light`. The mock sign-out marker works. Footer placeholders show «به‌زودی» without changing the URL. There is no horizontal scroll at 360px. `tsc --noEmit` is clean and all 71 vitest tests pass.

Five things need fixing. Please do all of them in a single commit.

## 1. Blocking — the ZWNJ characters are missing from the title and meta description

In `LandingView.vue`, `DOCUMENT_TITLE` and `META_DESCRIPTION` lost every U+200C. `document.title.includes('\u200c')` returns false and the browser tab currently reads «چکیار ... چکهای مدتدار» instead of «چک‌یار ... چک‌های مدت‌دار». Only those two constants were flattened; the rest of the file is fine, for example the hero heading still has a correct «چک‌یار».

Restore them exactly, with the zero-width non-joiners intact:

Title: چک‌یار | سکوی دیجیتال کشف و اتصال در بازار نقدشوندگی چک‌های مدت‌دار
Meta description: چک‌یار سکوی دیجیتال کشف و اتصال در بازار نقدشوندگی چک‌های مدت‌دار است؛ واسط فناورانه، نه نهاد مالی.

Add a vitest assertion that both strings contain U+200C so this cannot silently regress. Also check the strings you added to `index.html` and the footer for the same problem.

## 2. Blocking — duplicate data-testid values in the header

`landing-nav-login`, `landing-nav-register` and `landing-nav-marketplace` each appear twice in `LandingHeader.vue`: once in the desktop container and once in the mobile dropdown. Measured at 360px: with the menu closed, the only match has a zero-size bounding box because its parent is `display: none`, so a test cannot click it; with the menu open, a Playwright locator for `[data-testid="landing-nav-login"]` resolves to 2 elements and fails with a strict mode violation.

Give the mobile dropdown copies distinct ids: `landing-nav-login-mobile`, `landing-nav-register-mobile`, `landing-nav-marketplace-mobile`. The rule for the rest of this feature: every data-testid on the page resolves to exactly one element in any single viewport and menu state.

## 3. Blocking — the loading state, which the clarification round asked for and the commit does not implement

`main.ts` calls `app.mount('#app')` without waiting for the router. Vue clears `#app` on mount, which removes the `landing-loading` placeholder, while the async `beforeEnter` is still awaiting the flag request. Measured on localhost in mock mode: the placeholder disappears, then the page content appears about 310 ms later, with nothing on screen in between. Against a real backend that gap grows with the flag request latency, so this is exactly the "neither loading state nor content" window the prompt ruled out.

Gate the first mount on the router, for example `router.isReady().then(() => app.mount('#app'))`, or an equivalent that keeps the boot placeholder on screen until the first navigation resolves. Verify there is no blank frame between the placeholder and the first rendered route, and confirm this does not delay or break any other route.

Then handle the in-app case too: navigating to `/` or `/landing` from inside the app currently awaits the flag with no indication at all. Either implement the full-screen loading state the prompt asked for, or, if you think keeping the previous page visible during the await is better, say so explicitly with your reasoning. Do not leave it out silently.

## 4. The documentation describes UI that does not exist

- `docs/TESTING.md` and `.fa.md` reference `landing-nav-register-btn`. The actual testid is `landing-nav-register`.
- Both TESTING files describe "Hero and sticky bar CTAs". There is no sticky bar, and the hero has no CTAs in your own code.
- `docs/ARCHITECTURE.md` and `.fa.md` claim "responsive action bars for guests and authenticated users". The only action buttons are in the header.

Correct all four files to describe exactly what exists, and after fixing item 2, list the mobile testids as well.

## 5. The footer copyright year is hardcoded

`LandingFooter.vue` has «© ۱۴۰۴». The current Jalali year is ۱۴۰۵, so it is already wrong, and a hardcoded year keeps drifting. Derive it at runtime from the existing helpers in `src/utils/persianUtils.ts` instead of embedding a literal.

## Two small ones

`handlePlaceholderClick(name: string)` in `LandingFooter.vue` never uses `name`. Either use it or drop the parameter.

The `/` route carries a `component` and no `meta: { publicChrome: true }`, while its guard always redirects away from it, so that component reference is dead configuration. Either remove it or add the meta so the two routes are consistent. Whichever you choose, keep the redirect behavior identical.

## Not a change request

The footer already contains regulatory-adjacent copy: «چک‌یار یک واسط فناورانه است و نهاد مالی یا بانکی نمی‌باشد» and «واسط فناورانه کشف و اتصال — فاقد کارکرد بانکی، اعتباری و تسهیلاتی». Prompt 01 was skeleton-only and the regulatory wording is locked in the spec, so leave both sentences exactly as they are for now. I will reconcile them against the locked text in prompt 02.

## One process note

Your reply summary did not match your commit. It listed sections that do not exist in the code (`landing-section-social-proof`, `-for-holders`, `-for-investors`, `-trust`, `-comparison`, `-final-cta`, `-sticky-cta`), described a sticky CTA bar that was never built, and reported the authenticated CTA label as «ورود به سامانه» when the code correctly says «ورود به بازارچه». The code was right and the report was wrong, which is the safer direction, but it cost a full review cycle. For the rest of this feature, generate the summary from the actual diff.

Report the changed files grouped as code / tests / docs, the lint and test results, and the commit SHA.
```
