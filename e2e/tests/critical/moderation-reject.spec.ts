import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { DEMO_PASSWORD, ROUTES, SEED, TEST_IDS, USERS } from "../../support/constants";

test.describe.configure({ mode: "serial" });

async function fetchPendingListingIdBySerial(
  page: import("@playwright/test").Page,
  serial: string,
): Promise<number> {
  const token = await page.evaluate(
    (key) => localStorage.getItem(key),
    "chequeyar_access_token",
  );
  expect(token).toBeTruthy();
  const apiBase = process.env.API_URL || "http://localhost:8000/api/v1";
  const res = await page.request.get(`${apiBase}/moderation/queue/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  const results = Array.isArray(body) ? body : body.results || [];
  const hit = results.find(
    (row: { cheque_serial_number?: string; id?: number }) =>
      row.cheque_serial_number === serial,
  );
  if (!hit?.id) {
    throw new Error(`Pending listing ${serial} not found in moderation queue`);
  }
  return hit.id as number;
}

test.describe("critical: moderation reject", () => {
  test("moderator1 rejects seeded pending listing", async ({ page }) => {
    await loginAs(page, USERS.moderator);
    const listingId = await fetchPendingListingIdBySerial(
      page,
      SEED.rejectPendingSerial,
    );

    // Prefer queue reject modal (sends MOD_* codes). Review page options are
    // not contract-aligned and reject without rejection_code fails validation.
    await page.goto(ROUTES.moderation);
    await expect(page.getByTestId(TEST_IDS.moderationQueuePage)).toBeVisible({
      timeout: 20_000,
    });

    const row = page.locator("tr").filter({ hasText: `#${listingId}` });
    await expect(row).toBeVisible({ timeout: 20_000 });
    await row.getByRole("button", { name: /^رد آگهی$/ }).click();

    await page
      .getByPlaceholder(/علت دقیق رد|توضیح کامل|ناخوانا/)
      .fill("E2E reject: incomplete listing documents");
    await page.getByRole("button", { name: /ثبت رد آگهی/ }).click();

    await expect
      .poll(
        async () => {
          const token = await page.evaluate(
            (key) => localStorage.getItem(key),
            "chequeyar_access_token",
          );
          const apiBase = process.env.API_URL || "http://localhost:8000/api/v1";
          const res = await page.request.get(
            `${apiBase}/listings/${listingId}/`,
            {
              headers: { Authorization: `Bearer ${token}` },
            },
          );
          if (!res.ok()) return "";
          const body = await res.json();
          return body.status || "";
        },
        { timeout: 20_000 },
      )
      .toBe("rejected");

    void DEMO_PASSWORD;
  });
});
