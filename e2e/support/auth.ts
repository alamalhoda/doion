import { expect, type Page } from "@playwright/test";

import { DEMO_PASSWORD, ROUTES, TEST_IDS } from "./constants";

const USER_KEY = "chequeyar_auth_user";
const TOKEN_KEY = "chequeyar_access_token";
const REFRESH_KEY = "chequeyar_refresh_token";

/**
 * Work around auth.ts loadSavedUser(): when USER_KEY is missing it invents a
 * mock holder1 + token even with VITE_USE_MOCK=false. Seed a guest user JSON
 * without tokens so isAuthenticated stays false and /login remains reachable.
 * Remove after AI Studio fixes loadSavedUser for Live API (see AI_STUDIO_E2E_PREP_PROMPT.md).
 */
export async function prepareGuestSession(page: Page): Promise<void> {
  await page.goto(ROUTES.login);
  await page.evaluate(
    ({ userKey, tokenKey, refreshKey }) => {
      localStorage.clear();
      sessionStorage.clear();
      localStorage.setItem(
        userKey,
        JSON.stringify({
          id: 0,
          username: "_e2e_guest",
          email: "e2e@local.test",
          name: "E2E Guest",
          role: "check_holder",
          is_verified: false,
        }),
      );
      localStorage.removeItem(tokenKey);
      localStorage.removeItem(refreshKey);
    },
    { userKey: USER_KEY, tokenKey: TOKEN_KEY, refreshKey: REFRESH_KEY },
  );
  await page.goto(ROUTES.login);
}

/**
 * Ensure Live API mode (mock off). Safe if switch is already off or missing.
 */
export async function ensureLiveApiMode(page: Page): Promise<void> {
  const byTestId = page.getByTestId(TEST_IDS.mockModeSwitch);
  if (await byTestId.count()) {
    const checked = await byTestId.getAttribute("aria-checked");
    if (checked === "true") {
      await byTestId.click();
    }
    return;
  }

  const switchEl = page.locator(".n-switch").first();
  if (!(await switchEl.count())) {
    return;
  }
  const checked = await switchEl.getAttribute("aria-checked");
  if (checked === "true") {
    await switchEl.click();
  }
}

async function fillIdentifier(page: Page, identifier: string): Promise<void> {
  const byTestId = page.getByTestId(TEST_IDS.loginIdentifier);
  if (await byTestId.count()) {
    await byTestId.fill(identifier);
    return;
  }
  const textbox = page.getByRole("textbox").first();
  await textbox.fill(identifier);
}

async function fillPassword(page: Page, password: string): Promise<void> {
  const byTestId = page.getByTestId(TEST_IDS.loginPassword);
  if (await byTestId.count()) {
    await byTestId.fill(password);
    return;
  }
  await page.locator('input[type="password"]').first().fill(password);
}

async function clickLoginSubmit(page: Page): Promise<void> {
  const byTestId = page.getByTestId(TEST_IDS.loginSubmit);
  if (await byTestId.count()) {
    await byTestId.click();
    return;
  }
  await page.getByRole("button", { name: /ورود به حساب کاربری/ }).click();
}

/**
 * Submit the login form (does not assert success).
 */
export async function submitLoginForm(
  page: Page,
  username: string,
  password: string = DEMO_PASSWORD,
): Promise<void> {
  await prepareGuestSession(page);
  await expect(page.getByText(/ورود به سامانه چک‌یار/)).toBeVisible({
    timeout: 20_000,
  });
  await ensureLiveApiMode(page);
  await fillIdentifier(page, username);
  await fillPassword(page, password);
  await clickLoginSubmit(page);
}

/**
 * Log in via the standard form (not mock persona cards).
 */
export async function loginAs(
  page: Page,
  username: string,
  password: string = DEMO_PASSWORD,
): Promise<void> {
  await submitLoginForm(page, username, password);
  // Wait until Live login finishes (token stored / leave /login).
  await expect
    .poll(async () => page.evaluate((key) => localStorage.getItem(key), TOKEN_KEY), {
      timeout: 20_000,
    })
    .not.toBeNull();
  await expect(page).not.toHaveURL(/\/login(?:\?|$)/, { timeout: 20_000 });
}

export async function expectStillOnLogin(page: Page): Promise<void> {
  await expect(page).toHaveURL(/\/login/, { timeout: 10_000 });
  await expect(page.getByText(/ورود به سامانه چک‌یار/)).toBeVisible();
}

export async function expectLoginErrorVisible(page: Page): Promise<void> {
  // Live API: "Invalid credentials"; UI may also show Persian fallback.
  await expect(
    page.getByText(/Invalid credentials|خطا در ورود|نامعتبر|credentials/i),
  ).toBeVisible({ timeout: 15_000 });
}

export async function expectMyListingsPage(page: Page): Promise<void> {
  await expect(page).toHaveURL(new RegExp(`${ROUTES.myListings}`), {
    timeout: 20_000,
  });
  await expect(page.getByRole("heading", { name: /آگهی‌های من/ })).toBeVisible({
    timeout: 20_000,
  });
  await expect(
    page.getByText(/هنوز هیچ آگهی چکی ثبت نکرده‌اید/),
  ).toHaveCount(0);
  // Seeded holder has listings; table rows render bank / id cells.
  await expect(page.locator(".n-data-table, table").first()).toBeVisible({
    timeout: 20_000,
  });
}

export async function expectMatchesSentWithCard(page: Page): Promise<void> {
  await expect(page).toHaveURL(new RegExp(`${ROUTES.matches}`), {
    timeout: 20_000,
  });
  await expect(page.getByTestId(TEST_IDS.matchesPage)).toBeVisible();

  // Investor defaults to "sent"; still click tab for explicit coverage.
  const sentTab = page.getByTestId(TEST_IDS.matchesTabSent);
  if (await sentTab.count()) {
    await sentTab.click();
  } else {
    await page.getByText(/پیشنهادهای ارسالی/).first().click();
  }

  const sentPanel = page.getByTestId(TEST_IDS.matchesPanelSent);
  if (await sentPanel.count()) {
    await expect(sentPanel).toBeVisible({ timeout: 15_000 });
  }
  await expect(page.getByTestId(TEST_IDS.matchCard).first()).toBeVisible({
    timeout: 20_000,
  });
}

export async function expectMarketplace(page: Page): Promise<void> {
  await expect(page).toHaveURL(new RegExp(`${ROUTES.marketplace}`), {
    timeout: 20_000,
  });
  const byTestId = page.getByTestId(TEST_IDS.marketplacePage);
  if (await byTestId.count()) {
    await expect(byTestId).toBeVisible();
    return;
  }
  await expect(page.getByText(/آگهی چک صیادی/)).toBeVisible({ timeout: 20_000 });
}

export async function expectAtLeastOneListing(page: Page): Promise<void> {
  const byTestId = page.getByTestId(TEST_IDS.marketplaceListingCard);
  if (await byTestId.count()) {
    await expect(byTestId.first()).toBeVisible({ timeout: 20_000 });
    return;
  }
  const empty = page.getByText(
    /هیچ آگهی چک صیادی با مشخصات انتخاب شده یافت نشد/,
  );
  await expect(empty).toHaveCount(0, { timeout: 20_000 });
  await expect(page.getByText(/نمایش\s+.+\s+از\s+.+\s+آگهی/)).toBeVisible();
}

export async function expectModerationQueue(page: Page): Promise<void> {
  await expect(page).toHaveURL(new RegExp(`${ROUTES.moderation}`), {
    timeout: 20_000,
  });
  const byTestId = page.getByTestId(TEST_IDS.moderationQueuePage);
  if (await byTestId.count()) {
    await expect(byTestId).toBeVisible();
    return;
  }
  await expect(page.getByText(/صف بررسی و نظارت آگهی/)).toBeVisible({
    timeout: 20_000,
  });
}
