// Roles in the browser (P5 add-on, task 13, step 8).
// Run with the API and the seed users ready. The password comes from the
// environment, never from this file:  SEED_PASSWORD=... npx playwright test
import { test } from "@playwright/test";

test.skip("a passenger who opens /admin sees the forbidden page", async ({ page }) => {
  void page; // only quiets TypeScript until you use the name; delete this line
  // Log in on /login as asha@example.com with process.env.SEED_PASSWORD, using
  // getByLabel and getByRole. Then open /admin and expect the text
  // "You do not have access to this page". Delete `.skip` when it is written.
  throw new Error("TODO(task 13): write this test");
});
