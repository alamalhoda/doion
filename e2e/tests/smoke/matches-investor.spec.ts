import { test } from "@playwright/test";

import { expectMatchesSentWithCard, loginAs } from "../../support/auth";
import { ROUTES, USERS } from "../../support/constants";

test.describe("smoke: investor matches", () => {
  test("investor1 opens /matches sent tab and sees a match card", async ({
    page,
  }) => {
    await loginAs(page, USERS.investor);
    await page.goto(ROUTES.matches);
    await expectMatchesSentWithCard(page);
  });
});
