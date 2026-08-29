import { test } from "@playwright/test";

import {
  expectAtLeastOneListing,
  expectMarketplace,
  loginAs,
} from "../../support/auth";
import { USERS } from "../../support/constants";

test.describe("smoke: investor marketplace", () => {
  test("investor1 sees marketplace with seeded listings", async ({ page }) => {
    await loginAs(page, USERS.investor);
    await expectMarketplace(page);
    await expectAtLeastOneListing(page);
  });
});
