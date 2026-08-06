import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, SEED, TEST_IDS, USERS } from "../../support/constants";
import { clickConfirmDialog } from "../../support/critical";

test.describe.configure({ mode: "serial" });

test.describe("critical: decline match", () => {
  test("holder1 declines seeded pending match", async ({ page }) => {
    await loginAs(page, USERS.holder);
    await page.goto(ROUTES.matches);

    await expect(page.getByTestId(TEST_IDS.matchesPage)).toBeVisible({
      timeout: 20_000,
    });

    const receivedTab = page.getByTestId(TEST_IDS.matchesTabReceived);
    if (await receivedTab.count()) {
      await receivedTab.click();
    } else {
      await page.getByText(/پیشنهادهای دریافتی/).first().click();
    }

    const card = page.getByTestId(TEST_IDS.matchCard).filter({
      hasText: /Demo interest for decline-match E2E/,
    });
    await expect(card.first()).toBeVisible({ timeout: 20_000 });

    const alreadyDeclined = card.getByText(/رد شده|پیشنهاد رد شده|declined/i);
    if ((await alreadyDeclined.count()) > 0) {
      await expect(alreadyDeclined.first()).toBeVisible();
      return;
    }

    const declineBtn = card.getByTestId(TEST_IDS.matchDeclineBtn);
    if (await declineBtn.count()) {
      await declineBtn.click();
    } else {
      await card.getByRole("button", { name: /رد پیشنهاد|decline/i }).click();
    }

    await clickConfirmDialog(
      page,
      TEST_IDS.matchDeclineConfirm,
      /تأیید|تایید|رد پیشنهاد/,
    );

    const status = page.getByTestId(TEST_IDS.matchStatusDeclined);
    if (await status.count()) {
      await expect(status.first()).toBeVisible({ timeout: 20_000 });
    } else {
      await expect(
        page.getByText(/رد شده|پیشنهاد رد شده/).first(),
      ).toBeVisible({ timeout: 20_000 });
    }

    expect(SEED.declineMatchSerial).toMatch(/^2000/);
  });
});
