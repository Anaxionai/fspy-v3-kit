import { defineConfig, devices } from '@playwright/test'

// End-to-end tests for RailSeat web (task 15). Run them with:
//   npx playwright test
// Playwright starts the web app for you. Start PostgreSQL and the API first:
//   uv run fastapi dev app/main.py   (in railseat/api/)
// https://playwright.dev/docs/test-configuration
export default defineConfig({
  testDir: './tests/e2e',
  // One test at a time, so two tests never race for the same seat.
  workers: 1,
  // A line per test in the terminal (to paste into evidence.md), and an
  // HTML report in playwright-report/ that you open yourself.
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: 'http://localhost:5173',
    // Keep a trace of every failed test: npx playwright show-trace <file>
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: true,
  },
})
