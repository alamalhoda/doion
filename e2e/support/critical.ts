import { expect, type Page } from "@playwright/test";

import { ROUTES, TEST_IDS } from "./constants";

/** Click confirm in shared ConfirmDialog (testid or Persian confirm label). */
export async function clickConfirmDialog(
  page: Page,
  testId: string,
  confirmText: RegExp,
): Promise<void> {
  const byTestId = page.getByTestId(testId);
  if (await byTestId.count()) {
    await byTestId.click();
    return;
  }
  await page.getByRole("button", { name: confirmText }).click();
}

/**
 * Resolve marketplace listing id for a seeded serial via Live API.
 * Prefer this over scraping cards when pagination may hide the row.
 */
export async function fetchListingIdBySerial(
  page: Page,
  serial: string,
): Promise<number> {
  const token = await page.evaluate(
    (key) => localStorage.getItem(key),
    "chequeyar_access_token",
  );
  expect(token).toBeTruthy();

  const apiBase =
    process.env.API_URL || "http://localhost:8000/api/v1";

  // Marketplace page size is fixed at 20; walk pages until serial found.
  for (let pageNum = 1; pageNum <= 3; pageNum += 1) {
    const res = await page.request.get(
      `${apiBase}/marketplace/listings/?page=${pageNum}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    expect(res.ok()).toBeTruthy();
    const body = await res.json();
    const results = body.results || body;
    const hit = (Array.isArray(results) ? results : []).find(
      (row: { cheque_serial_number?: string; id?: number }) =>
        row.cheque_serial_number === serial,
    );
    if (hit?.id) {
      return hit.id as number;
    }
    if (!body.next) {
      break;
    }
  }
  throw new Error(`Listing with serial ${serial} not found in marketplace`);
}

export async function ensureFlatListingCreateMode(page: Page): Promise<void> {
  // Prefer flat mode so fill-sample + submit are on one screen.
  // Do NOT use the first .n-switch on the page (header mock switch).
  const modeRow = page.getByText(/حالت نمایش/).locator("..");
  const modeSwitch = modeRow.locator(".n-switch").first();
  if (!(await modeSwitch.count())) {
    // Fallback: switch adjacent to wizard labels.
    const labeled = page
      .locator("div")
      .filter({ hasText: /^حالت نمایش/ })
      .locator(".n-switch")
      .first();
    if (await labeled.count()) {
      const checked = await labeled.getAttribute("aria-checked");
      if (checked === "true") {
        await labeled.click();
      }
    }
    return;
  }
  const checked = await modeSwitch.getAttribute("aria-checked");
  if (checked === "true") {
    await modeSwitch.click();
  }
}

export async function expectMarketplaceHasPagination(page: Page): Promise<void> {
  await page.goto(ROUTES.marketplace);
  await expect(page.getByTestId(TEST_IDS.marketplacePage)).toBeVisible({
    timeout: 20_000,
  });

  const byTestId = page.getByTestId(TEST_IDS.marketplacePagination);
  if (await byTestId.count()) {
    await expect(byTestId).toBeVisible();
    return;
  }
  // Naive pagination / "صفحه" / next control when count > page size (20).
  await expect(
    page.locator(".n-pagination").first(),
  ).toBeVisible({ timeout: 20_000 });
}
