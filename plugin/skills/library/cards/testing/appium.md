---
name: appium
title: Appium
area: testing
tags: [testing, mobile, e2e, android, ios, webdriver, automation]
detect: [dep:appium, dep:appium-uiautomator2-driver, dep:appium-xcuitest-driver, dep:wd, dep:webdriverio, dep:Appium.WebDriver, dep:io.appium*]
related: [e2e-strategy, flaky-tests, detox, maestro, xcuitest]
---
Appium: WebDriver-protocol mobile automation across Android and iOS, driven by capabilities and stable accessibility locators.

## Verify
- `appium driver list --installed`: the needed drivers (uiautomator2, xcuitest) are installed.
- `appium --log-level info`: the server starts and accepts sessions.
- `adb devices`: the Android device or emulator is attached and authorized.
- `xcrun simctl list devices booted`: an iOS simulator is booted (macOS).
- `npx wdio run wdio.conf.js`: the suite runs (WebdriverIO runner; use your project's runner otherwise).

## Test first
Locate by accessibility id and wait on a condition.
```js
describe('login', () => {
  it('shows an error for a wrong password', async () => {
    await $('~email').setValue('a@b.co');
    await $('~password').setValue('wrong');
    await $('~login-button').click();
    const err = await $('~login-error');
    await err.waitForDisplayed({ timeout: 5000 });
    expect(await err.getText()).toContain('Invalid');
  });
});
```

## Do
- Give elements `accessibilityLabel` / `contentDescription` (accessibility id) and locate with `~id`; they work on both platforms.
- Use explicit waits (`waitForDisplayed`, `waitUntil`) on state, never fixed sleeps.
- Set capabilities in one config: `platformName`, `appium:automationName`, `appium:app`, `appium:deviceName`.
- Reset app state per test (`noReset` false, or clear data / terminate and activate the app) so tests are independent.
- Use a page-object per screen; keep assertions in the test.
- Log in through an API or deep link in setup, not the UI, except in the login test.
- Capture a screenshot and page source on failure.
- Pin Appium and driver versions in `package.json`.

## Avoid
- `driver.pause(5000)` as synchronization: slow and still flaky. Wait for an element or condition.
- XPath on the whole hierarchy: brittle and slow on mobile. Use accessibility id or resource-id.
- Running tests that depend on prior test state: one failure cascades. Reset per test.
- Hard-coded device names or OS versions in test code: move them to config or CI matrix.
- Testing business logic through the UI: slow. Cover logic in unit tests and keep E2E for flows.
- Unpinned driver versions: a driver update breaks CI overnight. Pin and upgrade deliberately.

## Review
- [ ] Elements use accessibility ids; no long XPath.
- [ ] No fixed sleeps; waits are conditional.
- [ ] Each test sets up and tears down its own state.
- [ ] Capabilities live in config; versions are pinned.
- [ ] Failures leave a screenshot or log artifact.
