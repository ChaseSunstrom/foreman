---
name: playwright
title: Playwright
area: web
tags: [playwright, e2e, browser-testing, testing, typescript, ui]
detect: [dep:@playwright/test, dep:playwright, dep:playwright-core, file:playwright.config.*]
related: [testing-library, cypress, msw, nextjs]
---
Playwright Test: real-browser end-to-end tests with auto-waiting locators and web-first assertions.

## Verify
- `npx playwright test`: the suite across configured browsers.
- `npx playwright test --repeat-each=5 path/to.spec.ts`: a new test is not flaky.
- `npx playwright test --list`: specs are discovered and titles are unique.
- `npx playwright show-report`: failure traces, screenshots and videos (when a report exists).

## Test first
Write the user flow first, with role-based locators and web-first assertions.
```ts
import { test, expect } from "@playwright/test";

test("adding a todo shows it in the list", async ({ page }) => {
  await page.goto("/");
  await page.getByPlaceholder("What needs to be done?").fill("buy milk");
  await page.keyboard.press("Enter");
  await expect(page.getByRole("listitem")).toHaveText("buy milk");
});
```

## Do
- Locate by role, label, placeholder or text: `getByRole`, `getByLabel`, `getByText`; use `getByTestId` as a last resort.
- Assert with web-first matchers (`toBeVisible`, `toHaveText`, `toHaveURL`) that retry until the timeout.
- Configure `webServer` in `playwright.config.ts` so the app starts for the run, and `use.baseURL` for relative `goto`.
- Log in once in a setup project and reuse `storageState` instead of logging in per test.
- Isolate data per test (fresh user or database state) so tests run in parallel.
- Stub third-party and flaky calls with `page.route`; keep first-party flows real.
- Set `trace: "on-first-retry"` and `retries` only in CI.
- Use `test.step` and `expect.soft` to keep long flows readable.

## Avoid
- `page.waitForTimeout(…)`: slow and flaky. Wait on a locator condition or a response with `page.waitForResponse`.
- Non-retrying assertions on snapshots of state: `expect(await loc.textContent()).toBe(...)` checks once. Use `await expect(loc).toHaveText(...)`.
- Missing `await` on actions and assertions: the test passes before anything ran. Enable the `@typescript-eslint/no-floating-promises` rule.
- CSS and XPath chains (`.btn > div:nth-child(2)`): break on markup changes. Use role locators.
- Tests that depend on order or shared state: break under parallel workers. Make each test self-contained.
- `page.$` and `elementHandle` APIs: discouraged. Use `locator`.
- Committing `test.only`: skips the suite. Set `forbidOnly: !!process.env.CI`.

## Review
- [ ] Locators are role, label or text based and assertions auto-retry.
- [ ] No fixed sleeps and no floating promises.
- [ ] Tests are independent and parallel-safe.
- [ ] Auth state is reused through `storageState`.
- [ ] CI config has `forbidOnly`, retries and trace on retry.
