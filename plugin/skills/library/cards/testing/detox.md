---
name: detox
title: Detox
area: testing
tags: [testing, mobile, e2e, react-native, gray-box, jest, ios, android]
detect: [dep:detox, file:.detoxrc.js, file:.detoxrc.json, file:e2e/jest.config.js]
related: [appium, maestro, e2e-strategy, flaky-tests]
---
Detox: gray-box React Native end-to-end tests that auto-synchronize with the app, run under Jest on simulators or emulators.

## Verify
- `npx detox build --configuration ios.sim.debug`: the app builds for the named configuration in `.detoxrc`.
- `npx detox test --configuration ios.sim.debug`: the E2E suite runs against the simulator.
- `npx detox test --configuration android.emu.debug --loglevel verbose`: the same on Android with verbose logs.
- `npx detox test --configuration ios.sim.release --record-logs failing`: keeps logs only for failing tests.

## Test first
```js
describe('checkout', () => {
  beforeAll(async () => { await device.launchApp({ newInstance: true }); });
  beforeEach(async () => { await device.reloadReactNative(); });

  it('shows the total after adding an item', async () => {
    await element(by.id('add-item-1')).tap();
    await element(by.id('cart-tab')).tap();
    await expect(element(by.id('cart-total'))).toHaveText('$9.99');
  });
});
```

## Do
- Add `testID` to every element you interact with and use `by.id`.
- Rely on Detox auto-sync; use `waitFor(element(...)).toBeVisible().withTimeout(ms)` only for async work it cannot see.
- Reset between tests with `device.reloadReactNative()` or `launchApp({ newInstance: true, delete: true })` for a clean install.
- Mock the backend at the network edge (local mock server or mock mode) so tests are deterministic.
- Skip the UI for setup: launch with `launchArgs` or deep link into the state under test.
- Turn off animations in the test build or via `device.disableSynchronization()` only around a known-endless animation, then re-enable.
- Run release-like builds in CI for realistic timing; debug builds for local iteration.

## Avoid
- `await new Promise(r => setTimeout(r, 3000))`: race masking. Use `waitFor` or fix what blocks synchronization.
- Matching by visible text: it breaks with copy or locale changes. Use `testID`.
- Leaving `disableSynchronization()` on: the safety net is gone. Wrap and restore it.
- Tests that rely on order or shared app state: reload or reinstall per test.
- Hitting real backends: flakiness and data pollution. Mock the network.
- Endless timers or polling in the app: Detox waits forever. Fake or stop them in test mode.

## Review
- [ ] Interactive elements have stable `testID`s.
- [ ] No arbitrary sleeps; `waitFor` has an explicit timeout.
- [ ] State is reset per test, and the backend is mocked.
- [ ] Synchronization is never left disabled.
- [ ] CI builds the exact configuration the tests run.
