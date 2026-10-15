---
name: visual-regression
title: Visual regression testing
area: testing
tags: [visual, screenshots, playwright, storybook, baselines, pixel-diff]
detect: [dep:@playwright/test, dep:backstopjs, dep:@storybook/test-runner, dep:chromatic, dep:percy, file:*-snapshots/*, file:backstop.json]
related: [snapshot-testing, e2e-strategy, accessibility-testing, flaky-tests]
---
Visual regression compares screenshots against committed baselines to catch unintended layout and style changes, with rendering pinned so diffs mean something.

## Verify
- `npx playwright test --grep @visual`: screenshot assertions run against baselines.
- `npx playwright test --update-snapshots`: regenerates baselines; then `git diff --stat` and view the images before committing.
- `npx backstop test`: BackstopJS compares against reference images.

## Test first
Screenshot a stable, isolated state and mask volatile regions.
```ts
import { test, expect } from "@playwright/test";

test("pricing card @visual", async ({ page }) => {
  await page.goto("/pricing");
  await expect(page.getByTestId("plans")).toHaveScreenshot("plans.png", {
    mask: [page.getByTestId("live-clock")],
    animations: "disabled",
  });
});
```
Baselines are stored beside specs in `*-snapshots/` and committed.

## Do
- Generate and compare baselines in one pinned environment (container image), so fonts and antialiasing match.
- Capture components or regions rather than whole pages; use a story per state.
- Disable animations, carets and transitions; wait for fonts and images to load.
- Freeze time and mock network data to fixed fixtures.
- Mask or hide volatile regions (ads, timestamps, avatars).
- Set a small `maxDiffPixelRatio` or threshold, not zero, only where antialiasing varies.
- Review image diffs in the PR and upload actual, expected and diff images as CI artifacts.

## Avoid
- Making baselines on a laptop and running in CI: font and renderer differences fail every run. Generate them in the CI container.
- Whole-page screenshots with live data: always different. Isolate regions and fixture data.
- Running `--update-snapshots` to turn a failure green: blesses regressions. Inspect each image first.
- Ignoring animations and lazy images: random diffs. Disable animations, wait for load.
- Loose thresholds to hide flake: real regressions slip through. Remove the nondeterminism instead.
- Huge numbers of full-viewport shots across many browsers: slow and noisy. Pick key components and one or two browsers.

## Review
- [ ] Baselines were produced in the pinned CI environment.
- [ ] Volatile content is masked or fixtured.
- [ ] Image diffs were viewed before baselines were updated.
- [ ] Thresholds are small and justified.
- [ ] Failure artifacts (expected, actual, diff) are uploaded.
