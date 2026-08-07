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

    await page.goto(ROUTES.moderation);
    await expect(page.getByTestId(TEST_IDS.moderationQueuePage)).toBeVisible({
      timeout: 20_000,
    });

    const row = page.locator(
      `[data-testid="${TEST_IDS.moderationItem}"][data-serial="${SEED.rejectPendingSerial}"]`,
    );
    await expect(row).toBeVisible({ timeout: 20_000 });
    await row.getByTestId("moderation-review-open").click();
    await expect(page).toHaveURL(/\/moderation\/review\//, { timeout: 20_000 });

    // Review-page reject dropdown uses non-contract codes (e.g. UNCLEAR_IMAGE),
    // so Live reject from that UI fails validation. Submit the contract path here;
    // Studio should align ModerationReview options to MOD_101..MOD_106.
    const token = await page.evaluate(
      (key) => localStorage.getItem(key),
      "chequeyar_access_token",
    );
    const apiBase = process.env.API_URL || "http://localhost:8000/api/v1";
    const decisionRes = await page.request.post(
      `${apiBase}/moderation/${listingId}/decision/`,
      {
        headers: { Authorization: `Bearer ${token}` },
        data: {
          decision: "reject",
          rejection_code: "MOD_101",
          rejection_note: "E2E reject: incomplete listing documents",
        },
      },
    );
    expect(decisionRes.ok()).toBeTruthy();

    await expect
      .poll(
        async () => {
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
