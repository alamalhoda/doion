import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, TEST_IDS, USERS } from "../../support/constants";

test.describe.configure({ mode: "serial" });

async function fetchPendingKycId(
  page: import("@playwright/test").Page,
): Promise<number> {
  const token = await page.evaluate(
    (key) => localStorage.getItem(key),
    "chequeyar_access_token",
  );
  expect(token).toBeTruthy();
  const apiBase = process.env.API_URL || "http://localhost:8000/api/v1";
  const res = await page.request.get(`${apiBase}/moderation/kyc/`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  const results = Array.isArray(body) ? body : body.results || [];
  const pending = results.find(
    (row: { status?: string; id?: number }) => row.status === "pending",
  );
  if (!pending?.id) {
    throw new Error("No pending KYC verification in moderation queue");
  }
  return pending.id as number;
}

test.describe("critical: kyc approve", () => {
  test("moderator1 approves pending KYC for holderkyc1", async ({ page }) => {
    await loginAs(page, USERS.moderator);
    await page.goto(ROUTES.moderationKyc);

    const kycId = await fetchPendingKycId(page);
    await page.goto(ROUTES.kycReview(kycId));

    const approveBtn = page.getByTestId(TEST_IDS.kycApproveBtn);
    if (await approveBtn.count()) {
      await approveBtn.click();
    } else {
      await page
        .getByRole("button", { name: /تأیید احراز هویت|تأیید سطح/ })
        .first()
        .click();
    }

    await expect
      .poll(async () => {
        const token = await page.evaluate(
          (key) => localStorage.getItem(key),
          "chequeyar_access_token",
        );
        const apiBase = process.env.API_URL || "http://localhost:8000/api/v1";
        const res = await page.request.get(
          `${apiBase}/verifications/${kycId}/`,
          { headers: { Authorization: `Bearer ${token}` } },
        );
        if (!res.ok()) return "";
        const body = await res.json();
        return body.status || "";
      }, { timeout: 20_000 })
      .toBe("approved");
  });
});
