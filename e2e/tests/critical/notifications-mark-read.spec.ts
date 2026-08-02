import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, SEED, TEST_IDS, USERS } from "../../support/constants";

test.describe.configure({ mode: "serial" });

test.describe("critical: notifications mark-read", () => {
  test("holder1 marks a seeded unread notification as read", async ({
    page,
  }) => {
    await loginAs(page, USERS.holder);
    await page.goto(ROUTES.notifications);

    const pageRoot = page.getByTestId(TEST_IDS.notificationsPage);
    if (await pageRoot.count()) {
      await expect(pageRoot).toBeVisible({ timeout: 20_000 });
    } else {
      await expect(
        page.getByText(/اعلامیه|اعلان|نوتیف/i).first(),
      ).toBeVisible({ timeout: 20_000 });
    }

    // Rich seed: 12 notifications → UI pageSize 10 shows pagination.
    expect(SEED.notificationCount).toBeGreaterThan(SEED.notificationsPageSize);
    const pagination = page.getByTestId(TEST_IDS.notificationsPagination);
    if (await pagination.count()) {
      await expect(pagination).toBeVisible();
    } else {
      await expect(page.locator(".n-pagination").first()).toBeVisible({
        timeout: 15_000,
      });
    }

    const markByTestId = page.getByTestId(TEST_IDS.notificationMarkRead);
    const markByLabel = page.getByRole("button", {
      name: /علامت به عنوان خوانده‌شده/,
    });
    const markBtn =
      (await markByTestId.count()) > 0 ? markByTestId : markByLabel;

    const unreadBefore = await markBtn.count();
    expect(unreadBefore).toBeGreaterThan(0);
    await markBtn.first().click();

    await expect
      .poll(async () => markBtn.count(), { timeout: 15_000 })
      .toBeLessThan(unreadBefore);
  });
});
