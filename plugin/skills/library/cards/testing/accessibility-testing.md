---
name: accessibility-testing
title: Accessibility testing
area: testing
tags: [a11y, axe, wcag, keyboard, aria, screen-reader]
detect: [dep:axe-core, dep:@axe-core/playwright, dep:jest-axe, dep:cypress-axe, dep:pa11y, dep:lighthouse, dep:@axe-core/react]
related: [e2e-strategy, visual-regression, unit-test-design]
---
Automated axe checks plus keyboard and semantic assertions catch common WCAG failures early; they cover only part of accessibility, so add manual checks.

## Verify
- `npx playwright test a11y.spec.ts`: axe scans of key pages report no violations.
- `npx pa11y http://localhost:3000`: Pa11y scans a running page.
- `npx lighthouse http://localhost:3000 --only-categories=accessibility --output=json --output-path=a11y.json`: Lighthouse accessibility audit saved as JSON.
- `npx jest --testPathPattern a11y`: component-level jest-axe tests pass.

## Test first
Assert zero violations on the rendered state, then add an interaction check.
```ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("login page has no detectable a11y violations", async ({ page }) => {
  await page.goto("/login");
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze();
  expect(results.violations).toEqual([]);
});
```
Keep these beside e2e specs or component tests.

## Do
- Scan every key page and each important state (open modal, error form, expanded menu), not only the initial load.
- Query by role and accessible name in tests (`getByRole`, `getByLabel`); failing lookups reveal missing semantics.
- Test keyboard flow: Tab order, Enter and Space activate, Escape closes dialogs, focus returns to the trigger.
- Assert focus moves to new content or an error summary after navigation or submit.
- Run scans in CI on every PR and fail on serious and critical impacts.
- Use native elements (`button`, `a`, `label`, `dialog`) before ARIA; add ARIA only to fill gaps.
- Add a manual pass with a screen reader and zoom to 200 percent before release.

## Avoid
- Treating a clean axe report as full compliance: automation finds only a portion of issues. Add manual checks.
- Disabling rules to get green: hides real failures. Fix the markup or document one narrow exclusion.
- `div` with `onClick` and no role, tabindex or key handler: unreachable by keyboard. Use a `button`.
- Placeholder as the only label, or `aria-label` duplicating visible text differently: fails name checks. Use a real `label`.
- Scanning before the page finishes rendering: false passes. Wait for the target content first.
- Color contrast verified only in light theme: check each theme.

## Review
- [ ] Key pages and states have axe scans in CI.
- [ ] Keyboard-only flow works and focus is managed.
- [ ] Controls have accessible names via native semantics.
- [ ] No axe rule is disabled without a written reason.
- [ ] A manual screen reader pass is scheduled for major changes.
