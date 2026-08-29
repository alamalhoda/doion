import { expect, test } from "@playwright/test";

import {
  expectLoginErrorVisible,
  expectStillOnLogin,
  submitLoginForm,
} from "../../support/auth";
import { USERS } from "../../support/constants";

test.describe("smoke: failed login", () => {
  test("wrong password stays on /login and shows an error", async ({
    page,
  }) => {
    await submitLoginForm(page, USERS.holder, "definitely-wrong-password");
    await expectStillOnLogin(page);
    await expectLoginErrorVisible(page);
    await expect(page).not.toHaveURL(/marketplace|matches|moderation/);
  });
});
