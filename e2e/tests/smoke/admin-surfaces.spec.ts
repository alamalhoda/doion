import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, TEST_IDS, USERS } from "../../support/constants";

test.describe("smoke: admin surfaces", () => {
  test("admin1 opens stats and feature-flags", async ({ page }) => {
    await loginAs(page, USERS.admin);

    await page.goto(ROUTES.adminStats);
    const statsRoot = page.getByTestId(TEST_IDS.adminStatsPage);
    if (await statsRoot.count()) {
      await expect(statsRoot).toBeVisible({ timeout: 20_000 });
    } else {
      await expect(
        page.getByText(/آمار|داشبورد|شاخص/).first(),
      ).toBeVisible({ timeout: 20_000 });
    }

    await page.goto(ROUTES.adminFeatureFlags);
    const flagsRoot = page.getByTestId(TEST_IDS.adminFeatureFlagsPage);
    if (await flagsRoot.count()) {
      await expect(flagsRoot).toBeVisible({ timeout: 20_000 });
    } else {
      await expect(
        page.getByText(/کلید|ویژگی|feature/i).first(),
      ).toBeVisible({ timeout: 20_000 });
    }

    await page.goto(ROUTES.adminAudit);
    await expect(
      page.getByText(/حسابرسی|رویداد|audit/i).first(),
    ).toBeVisible({ timeout: 20_000 });
  });
});
