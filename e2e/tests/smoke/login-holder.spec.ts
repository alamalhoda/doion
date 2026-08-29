import { test } from "@playwright/test";

import { expectMarketplace, loginAs } from "../../support/auth";
import { USERS } from "../../support/constants";

test.describe("smoke: holder login", () => {
  test("holder1 reaches marketplace after live login", async ({ page }) => {
    await loginAs(page, USERS.holder);
    await expectMarketplace(page);
  });
});
