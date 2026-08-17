# پرامپت A — پاسخ به سؤالات رفت‌وبرگشت اول

پاسخ به پرسش‌های Studio پیش از شروع پیاده‌سازی پرامپت [`01-skeleton.md`](01-skeleton.md).

## چرا فایل جدا و نه ادغام در پرامپت ۰۱

اگر این تصمیم‌ها را داخل بلوک پرامپت ۰۱ ادغام می‌کردیم، sandbox آن‌ها را از ابتدا و یکجا می‌گرفت، در حالی که Studio آن‌ها را بعد از پرسیدن سؤال گرفت. یکی از معیارهای مقایسه در Step 7 «تعداد رفت‌وبرگشت لازم» است و آن ادغام این معیار را برای پرامپت ۰۱ بی‌معنا می‌کرد.

پس ساختار دو پیامی حفظ می‌شود: در هر دو مسیر ابتدا بلوک `01-skeleton.md` پیست می‌شود و اگر عامل سؤال پرسید (هر سؤالی، حتی متفاوت از سؤال‌های Studio) این بلوک به‌عنوان پاسخ پیست می‌شود. اطلاعات ورودی دو مسیر یکسان می‌ماند و رفت‌وبرگشت هر مسیر قابل شمارش باقی می‌ماند.

## تصمیم‌های کاربر در این دور

- **شبکه‌های اجتماعی فوتر:** همان سه مورد پیشنهادی Studio (تلگرام، لینکدین، بله) تأیید شد.
- **توضیح متا:** پیشنهاد Studio رد شد چون عبارت «مدیریت مطالبات» قابلیتی را ادعا می‌کرد که محصول ندارد؛ متن فقط با زبان spec بازنویسی شد.

---

```text
Confirmed. Proceed with implementation, with one correction and a few explicit reminders.

## Confirmed as proposed

1) Section ids and data-testid slugs: exactly as you listed, all 12, with the anchors as listed. The header anchors point to #how-it-works, #live-listings, #faq and #contact-us.

2) Footer links: exactly as you listed — landing-footer-link-terms, -privacy, -about, -contact, plus landing-footer-link-telegram, -linkedin, -bale. All of them are placeholders: no navigation, no 404, no broken route, and «به‌زودی» through the existing message util.

3) Route guard and pure helper: yes, export a pure helper such as `getLandingRedirect(flagEnabled, targetPath)` that returns the redirect target or null to proceed. Put it inside `src/features/landing/` so the landing module owns it. Three extra constraints:
   - Collapse "flag absent", "is_enabled false" and "request failed" into a single false input. Fail closed.
   - Exactly one flag request per navigation attempt, and no retry loop inside a navigation.
   - Verify there is no redirect loop between `/`, `/landing` and `/marketplace` in any flag state.

5) Theme and state handling: yes, exactly as you described, including not touching the user's saved theme preference. Two clarifications:
   - The `chequeyar_mock_signed_out` marker must affect mock mode only. Live mode behavior stays exactly as it is today: no invented user and no invented tokens.
   - Keep the instant-demo seed for a first-time visitor in mock mode, meaning when the marker is absent.

## One correction

4) The document title is confirmed as you wrote it. Change the meta description: do not mention «مدیریت مطالبات» or receivables management. The product does not do that, and the whole purpose of this page is precise scope communication. Use exactly this text:

چک‌یار سکوی دیجیتال کشف و اتصال در بازار نقدشوندگی چک‌های مدت‌دار است؛ واسط فناورانه، نه نهاد مالی.

## Still required from the original prompt

Your summary did not mention the following. They are still in scope and must not be dropped:

- Part 3, loading state: the minimal RTL loading placeholder inside `<div id="app">` in `index.html` for cold boot, plus a full-screen loading state during in-app navigation to `/` or `/landing`. Until the flag state is known, neither landing content nor marketplace content may be visible, and there must be no flash of the wrong page and no layout jump.
- Part 5, simulator: confirm that a browser profile whose `chequeyar_simulator_v1` was saved before this change gains `show_landing_page` on the next load, with no simulator reset required.
- Part 9, tests: vitest for `showLandingPage` in all four flag states, the redirect decision for `/` and `/landing` in all four flag states, the simulator merge into an existing stored state, and the three sign-out marker transitions. Run `bun run lint` and `bun run test` and report the results.
- Part 10, docs: `docs/ARCHITECTURE.md` + `.fa.md` and `docs/TESTING.md` + `.fa.md`, in the same commit.
- Part 11, do-nots: Bun only and no `package-lock.json`, no new dependencies, do not touch `src/views/`, no section copy yet, no direct `axios` calls, no changes to other routes' guards or to `LoginView`'s post-login redirect, Persian only.

Go ahead and implement. In your reply include the changed files grouped as code / tests / docs, the exact final data-testid list, the lint and test results, and the commit SHA.
```
