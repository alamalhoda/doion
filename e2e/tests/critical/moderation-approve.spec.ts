import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, SEED, TEST_IDS, USERS } from "../../support/constants";

test.describe.configure({ mode: "serial" });

test.describe("critical: moderation approve", () => {
  test("moderator1 approves a seeded pending listing", async ({ page }) => {
    await loginAs(page, USERS.moderator);
    await page.goto(ROUTES.moderation);

    await expect(page.getByTestId(TEST_IDS.moderationQueuePage)).toBeVisible({
      timeout: 20_000,
    });

    const reviewOpen = page.getByRole("button", { name: /بررسی و تصمیم‌گیری/ });
    await expect(reviewOpen.first()).toBeVisible({ timeout: 20_000 });

    const rowCount = await page.getByRole("row").count();
    expect(rowCount).toBeGreaterThan(10);

    const firstRow = page.locator("tbody tr").first();
    const idCell = ((await firstRow.locator("td").first().innerText()) || "").trim();
    const listingId = idCell.replace("#", "").trim();
    expect(listingId).toMatch(/^\d+$/);

    await firstRow.getByRole("button", { name: /بررسی و تصمیم‌گیری/ }).click();
    await expect(page).toHaveURL(/\/moderation\/review\//, { timeout: 20_000 });

    const approveBtn = page.getByTestId(TEST_IDS.moderationApproveBtn);
    if (await approveBtn.count()) {
      await approveBtn.click();
    } else {
      await page
        .getByRole("button", {
          name: /تأیید و انتشار آگهی|تأیید نهایی آگهی/,
        })
        .first()
        .click();
    }

    const confirm = page.getByTestId(TEST_IDS.moderationApproveConfirm);
    if (await confirm.count()) {
      await confirm.click();
    }

    await expect(page).toHaveURL(/\/moderation\/?$/, { timeout: 20_000 });
    // Approved row should leave the pending queue.
    await expect(
      page.locator("tbody tr").filter({ hasText: `#${listingId}` }),
    ).toHaveCount(0, { timeout: 15_000 });

    // My listings shows id + status, not cheque serial.
    await loginAs(page, USERS.holder);
    await page.goto(ROUTES.myListings);
    const listingRow = page.locator("tr").filter({ hasText: `#${listingId}` });
    await expect(listingRow).toBeVisible({ timeout: 20_000 });
    await expect(listingRow.getByText(/منتشر شده/)).toBeVisible({
      timeout: 15_000,
    });

    expect(SEED.pendingCount).toBeGreaterThan(10);
  });
});
