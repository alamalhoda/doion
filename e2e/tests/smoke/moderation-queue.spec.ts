import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { TEST_IDS, USERS } from "../../support/constants";

test.describe("smoke: moderation queue live", () => {
  test("moderator1 opens /moderation without pagination/filter errors", async ({
    page,
  }) => {
    const pageErrors: string[] = [];
    page.on("pageerror", (err) => pageErrors.push(String(err)));

    await loginAs(page, USERS.moderator);
    await page.goto("/moderation");
    await expect(page.getByTestId(TEST_IDS.moderationQueuePage)).toBeVisible({
      timeout: 20_000,
    });

    // Risk filter change previously threw: store.moderationQueue.filter is not a function
    const riskSelect = page.locator(".n-select").first();
    if (await riskSelect.count()) {
      await riskSelect.click();
      const option = page.getByText(/ریسک بالا|پرریسک|high/i).first();
      if (await option.count()) {
        await option.click();
      } else {
        await page.keyboard.press("Escape");
      }
    }

    expect(
      pageErrors.some(
        (e) =>
          e.includes("filter is not a function") ||
          e.includes("Cannot read properties of null"),
      ),
    ).toBeFalsy();
  });
});
