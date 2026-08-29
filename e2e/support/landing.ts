import { expect, type APIRequestContext, type Page } from "@playwright/test";

import { prepareGuestSession } from "./auth";
import { DEMO_PASSWORD, ROUTES, TEST_IDS, USERS } from "./constants";

export const LANDING_FLAG_KEY = "show_landing_page";

export const LANDING_SECTIONS = [
  TEST_IDS.landingSectionHero,
  TEST_IDS.landingTrustStrip,
  TEST_IDS.landingSectionHowItWorks,
  TEST_IDS.landingSectionLiveListings,
  TEST_IDS.landingSectionFaq,
] as const;

function apiBase(): string {
  return process.env.API_URL || "http://127.0.0.1:8000/api/v1";
}

/**
 * Admin token for demo DB feature-flag toggles (Live API E2E only).
 */
export async function getAdminAccessToken(
  request: APIRequestContext,
): Promise<string> {
  const res = await request.post(`${apiBase()}/auth/login/`, {
    data: {
      identifier: USERS.admin,
      password: DEMO_PASSWORD,
    },
  });
  expect(res.ok(), `admin login failed: ${res.status()}`).toBeTruthy();
  const body = (await res.json()) as { access?: string };
  expect(body.access).toBeTruthy();
  return body.access as string;
}

export async function setLandingPageFlag(
  request: APIRequestContext,
  enabled: boolean,
): Promise<void> {
  const token = await getAdminAccessToken(request);
  const res = await request.patch(
    `${apiBase()}/compliance/feature-flags/${LANDING_FLAG_KEY}/`,
    {
      headers: { Authorization: `Bearer ${token}` },
      data: { is_enabled: enabled },
    },
  );
  expect(
    res.ok(),
    `PATCH ${LANDING_FLAG_KEY}=${enabled} failed: ${res.status()} ${await res.text()}`,
  ).toBeTruthy();
}

export async function prepareLandingGuest(page: Page): Promise<void> {
  await prepareGuestSession(page);
}

export async function expectLandingPageVisible(page: Page): Promise<void> {
  await expect(page).toHaveURL(/\/landing(?:\?|$|#)/, { timeout: 25_000 });
  await expect(page.getByTestId(TEST_IDS.landingPage)).toBeVisible({
    timeout: 25_000,
  });
}

export async function expectKeyLandingSections(page: Page): Promise<void> {
  for (const testId of LANDING_SECTIONS) {
    await expect(page.getByTestId(testId)).toBeVisible({ timeout: 20_000 });
  }
  await expect(page.getByTestId(TEST_IDS.landingFooter)).toBeVisible({
    timeout: 20_000,
  });
}

export async function expectLiveListingsReady(page: Page): Promise<void> {
  await expect(page.getByTestId(TEST_IDS.landingListingsGrid)).toBeVisible({
    timeout: 25_000,
  });
  await expect(page.getByTestId(TEST_IDS.landingListingsLoading)).toHaveCount(0);
  await expect(page.getByTestId(TEST_IDS.landingListingsError)).toHaveCount(0);
}

export async function clickFirstLandingListingCard(page: Page): Promise<void> {
  const card = page.locator('[data-testid^="landing-listing-card-"]').first();
  await expect(card).toBeVisible({ timeout: 25_000 });
  await card.click();
}

export async function expectGuestBlockedFromLanding(
  page: Page,
  path: string,
): Promise<void> {
  await prepareLandingGuest(page);
  await page.goto(path);
  await expect(page).not.toHaveURL(/\/landing(?:\?|$|#)/, { timeout: 25_000 });
  await expect(page.getByTestId(TEST_IDS.landingPage)).toHaveCount(0);
  await expect(page).toHaveURL(/\/(marketplace|login)(?:\?|$|#)/, {
    timeout: 25_000,
  });
}

export async function expectOnLogin(page: Page): Promise<void> {
  await expect(page).toHaveURL(new RegExp(`${ROUTES.login}(?:\\?|$|#)`), {
    timeout: 20_000,
  });
  await expect(page.getByText(/ورود به سامانه چک‌یار/)).toBeVisible({
    timeout: 20_000,
  });
}
