# پرامپت A — اسکلت، مسیر، و گیت فلگ

خروجی Step 2 از [`implementation_plan.md`](../implementation_plan.md).

## قاعده اجرا

این متن **بدون هیچ تغییری** دو بار اجرا می‌شود: یک بار در Google AI Studio (کد رسمی محصول) و یک بار در sandbox مسیر `/Users/alamalhoda/Projects/checkyar-cursor-lab` روی شاخه `experiment/landing-cursor`. اگر پرامپت اصلاح شد، هر دو مسیر باید از نو با نسخه اصلاح‌شده اجرا شوند، وگرنه مقایسه بی‌اعتبار است.

فقط بلوک `text` پایین کپی می‌شود.

## پوشش قوانین spec

قوانین ۱، ۲، ۳، ۵، ۶، ۱۸، ۲۲، ۲۶، ۲۷، ۲۸ از [`feature_spec.md`](../feature_spec.md).

## تصمیم‌ها و فرض‌های این پرامپت

- **حالت مهمان در mock:** طبق تصمیم کاربر، گزینه «نشانگر صریح خروج» انتخاب شد. راحتی دموی فعلی حفظ می‌شود ولی logout در mock بین بارگذاری‌ها پایدار می‌ماند. بدون این تغییر، سناریو ۲۲ و همه سناریوهای مهمان در حالت mock قابل تأیید نبودند.
- **ترتیب بخش‌ها:** spec §۲.۳ فوتر را ردیف ۱۲ و «سرمایه‌گذاری روی چک‌یار» را ردیف ۱۳ فهرست کرده است. فوتر به‌طور طبیعی باید آخرین عنصر صفحه باشد، پس بخش سرمایه‌گذاری **قبل از** فوتر قرار می‌گیرد. اگر ترتیب عینی spec مقصود بوده، این مورد باید اصلاح و هر دو مسیر از نو اجرا شوند.
- **پوسته:** صفحه همیشه با پوسته برند `dark` رندر می‌شود، حتی اگر کاربر پوسته دیگری انتخاب کرده باشد (قانون ۲۳ و بخش Out of Scope). ترجیح ذخیره‌شده کاربر تغییر نمی‌کند.
- **عنوان مرورگر:** طبق spec §۶ عنوان و توضیح متای پایه در همین پرامپت تنظیم می‌شود؛ OG و آنالیتیکس خارج از محدوده است.

---

```text
Goal: add the skeleton, routing, and feature-flag gate for a new public landing page in this UI repo. This prompt is structure only — the copy/content of the sections comes in a follow-up prompt, so leave the sections visually place-held.

Before coding: list any ambiguities and ask me questions until the instructions are fully clear.

## Context

- This repo is the active Cheque Yar UI: Vue 3 + TypeScript + Vite + Naive UI + Pinia. Bun lockfile only.
- All user-facing text is Persian and the app is RTL only. There is no i18n layer and no English UI copy.
- The backend is a separate Django monorepo (doion). Do NOT change, mock out, or invent backend code, endpoints, or contracts.
- The feature flag `show_landing_page` already exists in the backend seed with `is_enabled: false`. The flags endpoint `GET /api/v1/compliance/feature-flags/` is public (AllowAny) for read and is paginated; `adminApi.getFeatureFlags()` in `src/api/index.ts` already unwraps it with `unwrapList`. Do not change that call or the unwrapping.
- The brand theme for this page is `dark`, per `docs/design-system.md` (it has a section for the public marketing site). Use the semantic `--theme-*` tokens; do not invent one-off colors.
- `src/views/` contains legacy duplicates of views that the router no longer uses (the router imports from `src/features/**`). Do not touch `src/views/`.

## 1) Route

- Add `/landing`, name `landing`, component `src/features/landing/LandingView.vue`, with `meta: { publicChrome: true }`.
- `/landing` is NOT `requiresAuth` and NOT `guestOnly`. Guests and signed-in users both see it.
- `/` is currently `{ path: '/', redirect: '/marketplace' }`. Replace that static redirect with a conditional one that needs the flag: flag on -> `/landing`; flag off -> `/marketplace`.
- `/landing` while the flag is off -> redirect to `/marketplace`. The existing global guard then sends guests on to `/login`. Do not change that global behavior.
- Fail closed. All three of these mean "off": the flag is absent from the response, `is_enabled` is false, or the flags request failed.
- Resolve the flag in per-route async guards for `/` and `/landing` only (`beforeEnter`). Do NOT make the global `router.beforeEach` async, and do not change the behavior of any other route.
- Never auto-redirect a signed-in user away from `/landing`.
- Set the document title for this route to «چک‌یار | سکوی دیجیتال کشف و اتصال در بازار نقدشوندگی چک‌های مدت‌دار» and set a basic Persian meta description. No Open Graph, no sitemap, no analytics.

## 2) Feature-flag composable

In `src/shared/composables/useFeatureFlags.ts`:

- Add a `showLandingPage` computed that mirrors the existing `showRiskTier` exactly in shape and fail-closed behavior.
- Keep the existing auto-fetch and keep `fetchFlags()` swallowing errors as it does now.
- The route guards must await flag resolution before deciding, and must not spin in a retry loop when the request keeps failing.
- Do not change `showRiskTier`.

## 3) Loading state — no flash of the wrong page

Hard requirement: until the flag state is known, neither landing content nor marketplace content may be visible. Only a loading state.

- On a cold boot, `<div id="app">` in `index.html` is empty, so the user currently sees a bare dark screen. Add a minimal RTL loading placeholder inside `#app` that is replaced automatically once Vue mounts. Inline styles only, brand `dark` colors, no new dependency.
- For in-app navigation to `/` or `/landing`, show a full-screen loading state while the guard resolves.
- No layout jump and no flash of marketplace or landing content before the decision is made.

## 4) Landing chrome (third chrome state)

`src/App.vue` has two chrome states today: the app shell (`AppSidebar` + `AppHeader`, when authenticated and not on an auth page) and a full-screen state for auth pages. Add a third state for `route.meta.publicChrome`:

- No `AppSidebar`, no `AppHeader`. No theme switcher, no notification bell, no role switcher — regardless of whether the user is signed in.
- New `src/features/landing/LandingHeader.vue`: brand lockup «چک‌یار», in-page anchor links to «نحوه کار», «آگهی‌ها», «پرسش‌های متداول», «تماس با ما», plus auth CTAs.
  - Guest: «ورود» -> `/login` and «ثبت‌نام» -> `/register`.
  - Signed in: a single «ورود به بازارچه» -> `/marketplace`, and the login/register buttons are not rendered.
- New `src/features/landing/LandingFooter.vue`: placeholder links «قوانین», «حریم خصوصی», «درباره ما», «تماس با ما», and social placeholders. Clicking one must NOT navigate, must NOT produce a 404 or a broken route, and must show «به‌زودی» through the existing `message` util in `src/utils/discreteApi.ts`.
- The page must always render with the `dark` brand theme even when the user has selected another theme: put `data-theme="dark"` on the landing root (the tokens are declared under the `[data-theme="dark"]` selector) and pass the dark Naive theme + overrides for `publicChrome` routes. Do NOT modify the user's saved theme preference in `localStorage`.

## 5) Mock simulator seed

In `src/stores/useBackendSimulatorStore.ts`:

- Add to `seedFeatureFlags`: `{ key: 'show_landing_page', description: 'نمایش صفحه معرفی عمومی در مسیر /landing', is_enabled: true, is_system: false }`.
- This asymmetry is deliberate: on in the simulator (it is the demo environment), off in the real backend. Do not try to change the backend default.
- The existing merge inside `init()` already pushes missing seed flags into a stored state and persists. Confirm a returning user whose `chequeyar_simulator_v1` was saved before this change gets the new flag on the next load, with no simulator reset required.
- Turning the flag off from `/admin/feature-flags` in mock mode must make the page unavailable again, exactly like the flag being off.

## 6) Reachable guest state in mock mode

`loadSavedUser()` in `src/stores/auth.ts` seeds demo user `holder1` plus a mock token whenever mock mode is active and there is no saved user. Consequence: after logout, the next page reload silently signs the user back in, so the landing page can never be reviewed as a guest in mock mode.

Keep the instant-demo convenience, but make an explicit sign-out durable:

- `logout()` writes a marker, e.g. `localStorage['chequeyar_mock_signed_out'] = 'true'`.
- `loadSavedUser()` skips the mock demo seed while that marker is present.
- A successful login or register clears the marker.
- Live mode (`VITE_USE_MOCK=false`) behavior must not change: still no invented user and no invented tokens.

Do not otherwise change auth, roles, or permissions.

## 7) Place-held sections (no copy yet)

`LandingView.vue` renders these 12 section wrappers in this exact order, then `LandingFooter.vue` last. Each section is an empty, styled block with only a short placeholder heading — the real copy arrives in the next prompt.

1. hero
2. problem and solution
3. how it works
4. audiences
5. live listings
6. responsibility boundary
7. product status
8. pricing
9. FAQ
10. contact us
11. lead capture form
12. investing in Cheque Yar

Layout requirements that apply now: RTL, responsive from 360px with no horizontal scroll, tokens from `docs/design-system.md` (`dark`), and every interactive element reachable by keyboard with a visible focus ring.

## 8) data-testid

Follow the kebab-case convention already used in this repo (`marketplace-page`, `marketplace-listing-card`, `login-submit`). Playwright E2E lives in the doion monorepo and needs stable hooks, so add at least:

- `landing-page` on the page root
- `landing-loading` on the loading state
- `landing-header`, `landing-footer`
- `landing-nav-login`, `landing-nav-register`, `landing-nav-marketplace`
- one per section, named `landing-section-<name>` using the names in part 7 (for example `landing-section-hero`, `landing-section-live-listings`)
- one per placeholder footer link, named `landing-footer-link-<name>`

For Naive UI components, put the testid where Playwright can actually use it (for native inputs that means `:input-props`, not the component root). List the exact final testid strings in your reply.

## 9) Tests (this repo only)

Add or update vitest for the non-trivial logic:

- `showLandingPage`: flag on, flag off, flag absent, and failed request.
- The redirect decision for `/` and `/landing` in all four flag states. If the guard logic is hard to test directly, extract a small pure helper and test that.
- The simulator merge: an existing stored state without `show_landing_page` gains it without a reset.
- The three mock sign-out marker transitions: fresh visit auto-seeds, logout survives a reload, login clears the marker.

Run `bun run lint` (tsc) and `bun run test`, and report the results briefly in your reply. Do NOT add Playwright or doion e2e suites to this repo.

## 10) Documentation (this repo, same commit, bilingual EN + FA)

Update only the sections this change touches:

- `docs/ARCHITECTURE.md` + `docs/ARCHITECTURE.fa.md`: the new `src/features/landing/` module, the third chrome state driven by `meta.publicChrome`, the async fail-closed flag gate on `/` and `/landing`, and the mock sign-out marker.
- `docs/TESTING.md` + `docs/TESTING.fa.md`: the new vitest files, and how to review the page as a guest in mock mode (log out, then reload).
- Do not document Django internals here; point to the doion monorepo for the API contract.

## 11) Do not

- Commit `package-lock.json` or use npm as the package manager of record.
- Add new dependencies.
- Touch the legacy duplicates in `src/views/`.
- Write the real section copy — that is the next prompt.
- Call `axios` directly from the page; go through the `src/api/` layer only.
- Change `unwrapList`, the guards of any other route, or `LoginView`'s post-login redirect. Do not add a `?redirect=` deep-link return.
- Add any English user-facing copy.
- Change the theme behavior of any route other than the landing page.
- Do unrelated refactors.

## 12) Acceptance

Mock mode (`VITE_USE_MOCK=true`, no backend running):

- Guest opens `/` -> lands on `/landing`, sees the 12 place-held sections plus the footer, landing chrome only, no sidebar and no app header.
- Signed-in user opens `/landing` -> same page, «ورود به بازارچه» is shown, login/register are not, and there is no automatic redirect to the marketplace.
- Admin turns `show_landing_page` off at `/admin/feature-flags` -> `/` and `/landing` both go to `/marketplace`.
- A returning browser profile with an older simulator state gets the flag without resetting the simulator.

Live mode (`VITE_USE_MOCK=false`, `VITE_API_BASE_URL=http://localhost:8000/api/v1`), flag off in the database:

- `/landing` is not reachable and `/` behaves exactly as it does today.
- If the flags request fails, the result is the same as the flag being off, and nothing from the landing page flashes on screen.

Both modes:

- 360px width: no horizontal scroll, all header and footer CTAs clickable.
- Keyboard only: every header/footer CTA is reachable with a visible focus state.
- Tests: `bun run lint` and `bun run test` results reported.
- Docs: list the updated paths.
```
