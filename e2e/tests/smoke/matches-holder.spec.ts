import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { TEST_IDS, USERS } from "../../support/constants";

test.describe("smoke: matches page", () => {
  test("holder1 opens /matches without filter error and sees match cards", async ({
    page,
  }) => {
    const pageErrors: string[] = [];
    page.on("pageerror", (err) => pageErrors.push(String(err)));

    await loginAs(page, USERS.holder);
    await page.goto("/matches");
    await expect(page.getByTestId(TEST_IDS.matchesPage)).toBeVisible({
      timeout: 20_000,
    });
    await expect(page.getByTestId(TEST_IDS.matchCard).first()).toBeVisible({
      timeout: 20_000,
    });
    expect(
      pageErrors.some((e) => e.includes("filter is not a function")),
    ).toBeFalsy();
  });
});
