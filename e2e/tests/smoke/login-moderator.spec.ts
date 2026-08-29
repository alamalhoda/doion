import { test } from "@playwright/test";

import { expectModerationQueue, loginAs } from "../../support/auth";
import { USERS } from "../../support/constants";

test.describe("smoke: moderator login", () => {
  test("moderator1 reaches moderation queue after live login", async ({
    page,
  }) => {
    await loginAs(page, USERS.moderator);
    await expectModerationQueue(page);
  });
});
