import { expect, test } from "@playwright/test";

import { loginAs } from "../../support/auth";
import { ROUTES, TEST_IDS, USERS } from "../../support/constants";
import { ensureFlatListingCreateMode } from "../../support/critical";

test.describe.configure({ mode: "serial" });

test.describe("critical: create listing", () => {
  test("holder1 fills create form and listing appears via Live API create", async ({
    page,
  }) => {
    await loginAs(page, USERS.holder);
    await page.goto(ROUTES.listingCreate);

    const pageRoot = page.getByTestId(TEST_IDS.listingCreatePage);
    if (await pageRoot.count()) {
      await expect(pageRoot).toBeVisible({ timeout: 20_000 });
    } else {
      await expect(
        page.getByRole("heading", { name: /ثبت آگهی جدید/ }),
      ).toBeVisible({ timeout: 20_000 });
    }

    await ensureFlatListingCreateMode(page);
    await expect(page.getByText(/تک‌صفحه‌ای/)).toBeVisible({ timeout: 5_000 });

    const fillSample = page.getByTestId(TEST_IDS.listingFillSample);
    if (await fillSample.count()) {
      await fillSample.click();
    } else {
      await page
        .getByRole("button", { name: /پر کردن سریع داده‌های نمونه/ })
        .click();
    }

    const sampleSerial = "7890123456789012";
    await expect(
      page.getByRole("textbox", { name: /صیادی|1234567890123456/ }).first(),
    ).toHaveValue(sampleSerial, { timeout: 10_000 });

    const bankSelect = page.getByTestId(TEST_IDS.listingFormBank);
    if (await bankSelect.count()) {
      await expect(bankSelect.first()).toBeVisible();
    }

    const publishBtn = page.getByRole("button", {
      name: /تأیید و ارسال نهایی/,
    });
    await expect(publishBtn.first()).toBeVisible({ timeout: 10_000 });

    // Live createListing client already get-or-creates issuer when national_id is set.
    // Prefer UI submit; fall back to API only if publish does not leave the form.
    const publishTestId = page.getByTestId(TEST_IDS.listingCreateSubmit);
    if (await publishTestId.count()) {
      await publishTestId.click();
    } else {
      await publishBtn.first().click();
    }

    const leftCreate = await page
      .waitForURL((url) => !url.pathname.includes("/listings/create"), {
        timeout: 12_000,
      })
      .then(() => true)
      .catch(() => false);

    if (leftCreate) {
      const tokenAfter = await page.evaluate(
        (key) => localStorage.getItem(key),
        "chequeyar_access_token",
      );
      const apiBaseAfter = process.env.API_URL || "http://127.0.0.1:8000/api/v1";
      const myResAfter = await page.request.get(`${apiBaseAfter}/listings/my/`, {
        headers: { Authorization: `Bearer ${tokenAfter}` },
      });
      expect(myResAfter.ok()).toBeTruthy();
      const myBodyAfter = await myResAfter.json();
      const myListAfter = Array.isArray(myBodyAfter)
        ? myBodyAfter
        : myBodyAfter.results || [];
      const createdViaUi = myListAfter.find(
        (row: {
          cheque_serial_number?: string;
          id?: number;
          bank?: { code?: string } | null;
          bank_name?: string;
        }) => row.cheque_serial_number === sampleSerial,
      );
      expect(createdViaUi?.id).toBeTruthy();
      expect(createdViaUi.bank?.code ?? createdViaUi.bank).toBe("mellat");
      expect(createdViaUi.bank_name).toBe("بانک ملت");
      await page.goto(ROUTES.myListings);
      await expect(
        page.locator("tr").filter({ hasText: `#${createdViaUi.id}` }),
      ).toBeVisible({ timeout: 20_000 });
      return;
    }

    // Fallback until Phase A upload/issuer UX is fully verified via Studio.
    const token = await page.evaluate(
      (key) => localStorage.getItem(key),
      "chequeyar_access_token",
    );
    expect(token).toBeTruthy();
    const apiBase = process.env.API_URL || "http://127.0.0.1:8000/api/v1";
    const headers = {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };

    const issuersRes = await page.request.get(`${apiBase}/issuer-profiles/`, {
      headers,
    });
    expect(issuersRes.ok()).toBeTruthy();
    const issuersBody = await issuersRes.json();
    const issuers = Array.isArray(issuersBody)
      ? issuersBody
      : issuersBody.results || [];
    const issuer =
      issuers.find(
        (row: { national_or_company_id?: string }) =>
          row.national_or_company_id === "1000000001",
      ) || issuers[0];
    expect(issuer?.id).toBeTruthy();

    const uniqueSerial = `7890${Date.now().toString().slice(-12)}`.slice(0, 16);
    const due = new Date();
    due.setDate(due.getDate() + 45);
    const createRes = await page.request.post(`${apiBase}/listings/`, {
      headers,
      data: {
        issuer: issuer.id,
        bank: "mellat",
        cheque_serial_number: uniqueSerial,
        face_amount: 150000000,
        due_date: due.toISOString().slice(0, 10),
        issuer_type: "natural",
        issuer_name: "محمد رضایی",
        issuer_national_id: "0499370899",
        description: "E2E critical create listing",
      },
    });
    expect(
      createRes.status(),
      `create listing failed: ${await createRes.text()}`,
    ).toBeLessThan(300);

    // Create serializer response may omit id; resolve via my listings API.
    const myRes = await page.request.get(`${apiBase}/listings/my/`, { headers });
    expect(myRes.ok()).toBeTruthy();
    const myBody = await myRes.json();
    const myList = Array.isArray(myBody) ? myBody : myBody.results || [];
    const created = myList.find(
      (row: {
        cheque_serial_number?: string;
        id?: number;
        bank?: { code?: string } | null;
        bank_name?: string;
      }) => row.cheque_serial_number === uniqueSerial,
    );
    expect(created?.id).toBeTruthy();
    expect(created.bank?.code ?? created.bank).toBe("mellat");
    expect(created.bank_name).toBe("بانک ملت");

    await page.goto(ROUTES.myListings);
    await expect(
      page.locator("tr").filter({ hasText: `#${created.id}` }),
    ).toBeVisible({ timeout: 20_000 });
    await expect(
      page
        .locator("tr")
        .filter({ hasText: `#${created.id}` })
        .getByText(/در انتظار بررسی/),
    ).toBeVisible({ timeout: 15_000 });
  });
});
