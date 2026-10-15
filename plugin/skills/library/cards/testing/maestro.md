---
name: maestro
title: Maestro
area: testing
tags: [testing, mobile, e2e, yaml, android, ios, flows]
detect: [file:.maestro/*.yaml, file:.maestro/*.yml, file:.maestro/config.yaml]
related: [appium, detox, e2e-strategy, flaky-tests]
---
Maestro: declarative YAML UI flows for mobile apps and web, with built-in tolerance for timing and no code to maintain.

## Verify
- `maestro test .maestro/login.yaml`: one flow runs against the connected device or simulator.
- `maestro test .maestro/`: the whole flow directory runs.
- `maestro test --format junit --output report.xml .maestro/`: a JUnit report for CI.
- `maestro hierarchy`: prints the current view tree, so selectors can be checked against what is on screen.

## Test first
```yaml
appId: com.example.app
---
- clearState
- launchApp
- tapOn:
    id: "email"
- inputText: "a@b.co"
- tapOn:
    id: "password"
- inputText: "wrong"
- tapOn: "Log in"
- assertVisible: "Invalid credentials"
```
Run it before the error message exists; the red `assertVisible` is the failing test.

## Do
- Start flows with `clearState` and `launchApp` so each is independent.
- Select by `id` (accessibility id or resource-id) first; use text only for stable user-facing labels.
- Use `extendedWaitUntil` with a timeout for slow async screens instead of repeated taps.
- Split reusable steps into subflows and call them with `runFlow`.
- Use `env` variables (`${USERNAME}`) and pass them with `-e`; keep secrets out of the YAML.
- Tag flows (`tags: [smoke]`) and run subsets with `--include-tags`.
- Use `assertVisible` and `assertNotVisible` after every key action so failures point to the step.
- Use `takeScreenshot` at key points for review artifacts.

## Avoid
- Long chains of `tapOn` by coordinates (`point:`): they break on other screen sizes. Select by id or text.
- `waitForAnimationToEnd` or retries everywhere as a cure: slow and still racy. Wait on the specific element.
- Flows that assume the app is already logged in: order-dependent. Use `clearState` plus a login subflow.
- Giant single flows: a failure hides what broke. Keep flows short and focused.
- Hard-coded credentials in the YAML: use `env` vars.
- Covering logic that a unit test could check: keep Maestro for critical user journeys.

## Review
- [ ] Each flow starts clean and is independent.
- [ ] Selectors use ids; no coordinates.
- [ ] Assertions follow each key step.
- [ ] Shared steps are subflows; secrets come from `env`.
- [ ] Tagged smoke flows run in CI with a JUnit report.
