import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, SEED, TEST_IDS, USERS } from "../../support/constants";
import {
  clickConfirmDialog,
  expectMarketplaceHasPagination,
  fetchListingIdBySerial,
} from "../../support/critical";

test.describe.configure({ mode: "serial" });

test.describe("critical: express interest", () => {
  test("marketplace pagination is active with rich seed", async ({ page }) => {
    await loginAs(page, USERS.investor);
    await expectMarketplaceHasPagination(page);
  });

  test("investor1 expresses interest on seeded published listing without prior match", async ({
    page,
  }) => {
    await loginAs(page, USERS.investor);

    const listingId = await fetchListingIdBySerial(
      page,
      SEED.expressInterestSerial,
    );

    await page.goto(ROUTES.expressInterest(listingId));

    const pageRoot = page.getByTestId(TEST_IDS.expressInterestPage);
    if (await pageRoot.count()) {
      await expect(pageRoot).toBeVisible({ timeout: 20_000 });
    } else {
      await expect(
        page.getByRole("heading", { name: /ثبت ابراز تمایل/ }),
      ).toBeVisible({ timeout: 20_000 });
    }

    const messageField = page.getByTestId(TEST_IDS.expressInterestMessage);
    const e2eMessage = "E2E critical-path express interest message";
    if (await messageField.count()) {
      await messageField.fill(e2eMessage);
    } else {
      await page.locator("textarea").first().fill(e2eMessage);
    }

    const submit = page.getByTestId(TEST_IDS.expressInterestSubmit);
    if (await submit.count()) {
      await submit.click();
    } else {
      await page
        .getByRole("button", { name: /ارسال پیشنهاد خرید به دارنده چک/ })
        .click();
    }

    await clickConfirmDialog(
      page,
      TEST_IDS.expressInterestConfirm,
      /ارسال قطعی درخواست/,
    );

    await expect(page).toHaveURL(new RegExp(`${ROUTES.matches}`), {
      timeout: 20_000,
    });

    const sentTab = page.getByTestId(TEST_IDS.matchesTabSent);
    if (await sentTab.count()) {
      await sentTab.click();
    } else {
      await page.getByText(/پیشنهادهای ارسالی/).first().click();
    }

    // Cards show listing.id; assert by unique message we submitted.
    await expect(
      page.getByText(/E2E critical-path express interest message/),
    ).toBeVisible({ timeout: 20_000 });
    await expect(
      page.getByTestId(TEST_IDS.matchCard).filter({ hasText: `#${listingId}` }),
    ).toBeVisible({ timeout: 15_000 });
  });
});
