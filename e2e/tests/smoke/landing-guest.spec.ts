import { test } from "@playwright/test";

import {
  clickFirstLandingListingCard,
  expectGuestBlockedFromLanding,
  expectKeyLandingSections,
  expectLandingPageVisible,
  expectLiveListingsReady,
  expectOnLogin,
  prepareLandingGuest,
  setLandingPageFlag,
} from "../../support/landing";

test.describe.configure({ mode: "serial" });

test.describe("smoke: landing guest (Live API)", () => {
  test.beforeAll(async ({ request }) => {
    await setLandingPageFlag(request, false);
  });

  test("fail-closed when show_landing_page is off", async ({ page }) => {
    await expectGuestBlockedFromLanding(page, "/");
    await expectGuestBlockedFromLanding(page, "/landing");
  });

  test("guest / redirects to /landing when flag is on", async ({
    page,
    request,
  }) => {
    await setLandingPageFlag(request, true);
    await prepareLandingGuest(page);
    await page.goto("/");
    await expectLandingPageVisible(page);
  });

  test("key landing sections are visible", async ({ page, request }) => {
    await setLandingPageFlag(request, true);
    await prepareLandingGuest(page);
    await page.goto("/landing");
    await expectLandingPageVisible(page);
    await expectKeyLandingSections(page);
  });

  test("guest listing card click navigates to /login", async ({
    page,
    request,
  }) => {
    await setLandingPageFlag(request, true);
    await prepareLandingGuest(page);
    await page.goto("/landing#live-listings");
    await expectLandingPageVisible(page);
    await expectLiveListingsReady(page);
    await clickFirstLandingListingCard(page);
    await expectOnLogin(page);
  });

  test.afterAll(async ({ request }) => {
    await setLandingPageFlag(request, false);
  });
});
