import { expect, test } from "@playwright/test";

import { expectMyListingsPage, loginAs } from "../../support/auth";
import { ROUTES, USERS } from "../../support/constants";

test.describe("smoke: holder my listings", () => {
  test("holder1 opens /listings/my without crash and sees listings", async ({
    page,
  }) => {
    const pageErrors: string[] = [];
    page.on("pageerror", (err) => pageErrors.push(String(err)));

    await loginAs(page, USERS.holder);
    await page.goto(ROUTES.myListings);
    await expectMyListingsPage(page);

    expect(
      pageErrors.some(
        (e) =>
          e.includes("filter is not a function") ||
          e.includes("Cannot read properties of null"),
      ),
    ).toBeFalsy();
  });
});
