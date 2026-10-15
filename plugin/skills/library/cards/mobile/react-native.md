---
name: react-native
title: React Native
area: mobile
tags: [react-native, javascript, typescript, mobile, ios, android]
detect: [dep:react-native, dep:@react-native-community/cli, dep:@testing-library/react-native, file:metro.config.js, file:ios/Podfile]
related: [expo, fastlane, xcodebuild, capacitor]
---
React Native apps: components over native views, Metro bundler, native modules, New Architecture and device testing.

## Verify
- `npx tsc --noEmit`: types check (TypeScript projects).
- `npx eslint .`: lint, including react-hooks rules.
- `npx jest`: unit and component tests.
- `npx react-native doctor`: toolchain and environment problems for the community CLI.
- `cd ios && pod install`: iOS native deps resolve after adding a native package.

## Test first
Use Jest with `@testing-library/react-native`; tests sit next to code or in `__tests__/`.
```tsx
import { render, screen, fireEvent } from '@testing-library/react-native';
import { Counter } from '../Counter';

test('pressing increment shows 1', () => {
  render(<Counter />);
  fireEvent.press(screen.getByText('Increment'));
  expect(screen.getByText('Count: 1')).toBeTruthy();
});
```
Mock native modules in `jest.setup.js` and register it via `setupFiles`.

## Do
- Use `FlatList` or `SectionList` (or FlashList) for long lists with a stable `keyExtractor`.
- Style with `StyleSheet.create`; use `Platform.select` and `useWindowDimensions` for differences.
- Wrap screens in `SafeAreaView` / safe-area context and `KeyboardAvoidingView` where inputs sit low.
- Keep expensive work off the JS thread: native driver animations (`useNativeDriver: true`) or Reanimated worklets.
- Request permissions at runtime and declare them in Info.plist and AndroidManifest.xml.
- Store secrets in the Keychain or Keystore (secure storage library), not AsyncStorage.
- After adding or upgrading a native dependency, reinstall pods and rebuild the app binary; Metro reload is not enough.

## Avoid
- `ScrollView` with hundreds of mapped children: renders all at once. Use `FlatList`.
- Inline arrow functions and objects as props in list items: re-render churn. Memoize with `useCallback` / `useMemo`, or `React.memo`.
- Missing dependencies in hooks arrays: stale closures. Satisfy the `exhaustive-deps` lint instead of disabling it.
- `console.log` in hot paths: slows the JS thread and ships to release. Strip or guard with `__DEV__`.
- Importing web-only packages (DOM, `window` APIs): crash at runtime. Check React Native support.
- `AsyncStorage` for tokens: unencrypted. Use secure storage.
- Updating state after unmount from async callbacks: leaks and warnings. Cancel with an `AbortController` or a flag in the effect cleanup.

## Review
- [ ] Types, lint and tests are clean; hooks deps satisfied.
- [ ] Lists are virtualized with stable keys.
- [ ] Native dependency changes include pod install and a native rebuild note.
- [ ] Permissions are declared per platform and requested at runtime.
- [ ] Tested on both iOS and Android paths for platform-specific code.
