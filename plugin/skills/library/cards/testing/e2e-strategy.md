---
name: e2e-strategy
title: End-to-end test strategy
area: testing
tags: [e2e, playwright, cypress, critical-paths, selectors, ci]
detect: [dep:@playwright/test, dep:playwright, dep:cypress, dep:selenium, dep:selenium-webdriver, file:playwright.config.*, file:cypress.config.*]
related: [test-pyramid, flaky-tests, visual-regression, accessibility-testing, test-sharding]
---
Keep a small set of end-to-end tests on the few journeys that earn money or break trust, and make each one hermetic, fast and stable.

## Verify
- `npx playwright test --reporter=line`: the browser suite passes headless.
- `npx playwright test --repeat-each=5 path/to/spec.ts`: a new spec passes five times in a row (flake probe).
- `npx cypress run --spec cypress/e2e/checkout.cy.ts`: one Cypress spec runs headless.
- `npx playwright test --trace on-first-retry`: a failing retry leaves a trace to inspect.

## Test first
Start from the user journey and assert on what the user sees.
```ts
import { test, expect } from "@playwright/test";

test("guest can check out", async ({ page }) => {
  await page.goto("/products/pen");
  await page.getByRole("button", { name: "Add to cart" }).click();
  await page.getByRole("link", { name: "Checkout" }).click();
  await expect(page.getByRole("heading", { name: "Order confirmed" })).toBeVisible();
});
```
Specs live in `e2e/` or `tests/e2e/`, with page helpers beside them.

## Do
- Cover critical journeys only (sign-up, login, purchase, core create flow); push edge cases down to unit and integration tests.
- Select by role, label or text (`getByRole`) or a dedicated `data-testid`, never CSS chains.
- Rely on auto-waiting and web-first assertions (`expect(locator).toBeVisible()`), not fixed timeouts.
- Seed state through the API or database in setup; log in once and reuse stored auth state.
- Give each test its own data and account so tests run in parallel.
- Stub third-party calls you do not own (payments, maps) at the network layer.
- Capture trace, video and screenshot on failure and upload as CI artifacts.

## Avoid
- `waitForTimeout(3000)` or `cy.wait(3000)`: slow and still flaky. Wait on a condition (element, response).
- Driving setup through the UI in every test: slow and fragile. Create data by API.
- Tests that depend on each other's order or leftover data: break under sharding. Make each self-contained.
- Selectors tied to layout (`div > div:nth-child(3)`): break on markup change. Use roles and test ids.
- Running against shared staging with real accounts: nondeterministic. Use an ephemeral environment.
- Retrying all failures forever: hides flaky bugs. Allow one retry and track retried tests.

## Review
- [ ] Each e2e test maps to a named critical journey.
- [ ] No fixed sleeps; assertions wait on conditions.
- [ ] Data is created per test and cleaned or isolated.
- [ ] Failures upload traces or screenshots.
- [ ] Logic that fits a lower tier is not tested here.
