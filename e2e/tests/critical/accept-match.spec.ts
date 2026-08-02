import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, SEED, TEST_IDS, USERS } from "../../support/constants";
import { clickConfirmDialog } from "../../support/critical";

test.describe.configure({ mode: "serial" });

test.describe("critical: accept match", () => {
  test("holder1 accepts seeded pending match", async ({ page }) => {
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

    // Prefer unique seed message; cards do not show cheque serial.
    const card = page.getByTestId(TEST_IDS.matchCard).filter({
      hasText: /Demo interest for accept-match E2E/,
    });
    await expect(card.first()).toBeVisible({ timeout: 20_000 });

    // If a prior mutating run already accepted, assert accepted state and exit.
    const alreadyAccepted = card.getByText(/پذیرفته شده|پیشنهاد پذیرفته شده/);
    if ((await alreadyAccepted.count()) > 0) {
      await expect(alreadyAccepted.first()).toBeVisible();
      return;
    }

    const acceptBtn = card.getByTestId(TEST_IDS.matchAcceptBtn);
    if (await acceptBtn.count()) {
      await acceptBtn.click();
    } else {
      await card
        .getByRole("button", { name: /پذیرش پیشنهاد خرید/ })
        .click();
    }

    await clickConfirmDialog(
      page,
      TEST_IDS.matchAcceptConfirm,
      /تأیید و ادامه|تایید و ادامه/,
    );

    const status = page.getByTestId(TEST_IDS.matchStatusAccepted);
    if (await status.count()) {
      await expect(status.first()).toBeVisible({ timeout: 20_000 });
    } else {
      await expect(
        page.getByText(/پذیرفته شده|پیشنهاد پذیرفته شده/).first(),
      ).toBeVisible({ timeout: 20_000 });
    }

    // Keep serial constant referenced for operators / Studio docs.
    expect(SEED.acceptMatchSerial).toMatch(/^2000/);
  });
});
