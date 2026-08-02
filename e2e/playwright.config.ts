import { defineConfig, devices } from "@playwright/test";

/**
 * Servers are started outside Playwright (see scripts/ and E2E_LOCAL_RUNBOOK.md).
 * baseURL points at the active UI (checkyar-googleai) with VITE_USE_MOCK=false.
 */
const frontendUrl = process.env.FRONTEND_URL || "http://localhost:3000";

export default defineConfig({
  testDir: "./tests",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [["list"], ["html", { open: "never" }]],
  timeout: 60_000,
  expect: { timeout: 15_000 },
  use: {
    baseURL: frontendUrl,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "off",
    locale: "fa-IR",
  },
  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        // Bundled Chromium is unsupported on macOS 13; use system Google Chrome.
        // CI (newer hosts) can override with PLAYWRIGHT_CHANNEL=chromium or unset.
        channel: process.env.PLAYWRIGHT_CHANNEL || "chrome",
      },
    },
  ],
});
