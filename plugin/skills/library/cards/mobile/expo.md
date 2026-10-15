---
name: expo
title: Expo
area: mobile
tags: [expo, react-native, typescript, eas, mobile, expo-router]
detect: [dep:expo, dep:expo-router, dep:expo-modules-core, file:app.json, file:app.config.js, file:app.config.ts, file:eas.json]
related: [react-native, fastlane, capacitor]
---
Expo: managed React Native workflow with SDK modules, Expo Router, config plugins, prebuild and EAS Build/Update.

## Verify
- `npx expo-doctor`: project config and dependency compatibility checks.
- `npx expo install --check`: installed packages match the SDK's expected versions.
- `npx tsc --noEmit`: types.
- `npx jest`: tests via `jest-expo` preset.
- `npx expo export --platform ios`: the JS bundle builds for a platform.

## Test first
Configure Jest with the `jest-expo` preset and test components with `@testing-library/react-native`.
```tsx
// package.json: "jest": { "preset": "jest-expo" }
import { render, screen } from '@testing-library/react-native';
import Home from '../app/index';

test('home shows the welcome title', () => {
  render(<Home />);
  expect(screen.getByText('Welcome')).toBeTruthy();
});
```

## Do
- Install Expo-aware packages with `npx expo install <pkg>` so versions match the SDK.
- Put routes in `app/` for Expo Router (file-based); use `_layout.tsx` for stacks and tabs and `Link` / `useRouter` for navigation.
- Read public config from `process.env.EXPO_PUBLIC_*` variables, and `expo-constants` for app config; dynamic config goes in `app.config.ts`.
- Use config plugins in `app.json` plugins for native settings, then run `npx expo prebuild` only to generate native folders.
- Use EAS profiles in `eas.json` (`development`, `preview`, `production`) and `eas build --profile <name>`.
- Build a development client (`expo-dev-client`) when using native modules that Expo Go lacks.
- Store secrets in EAS secrets or `expo-secure-store`, never in `EXPO_PUBLIC_` variables.

## Avoid
- Anything prefixed `EXPO_PUBLIC_` holding secrets: those are inlined into the shipped bundle. Keep secrets on a server.
- `npm install` of a native module when a matching Expo SDK version exists: version mismatch crashes. Use `npx expo install`.
- Hand-editing `ios/` and `android/` in a project that regenerates them with prebuild: edits get wiped. Use config plugins.
- Testing a custom native module in Expo Go: not available. Use a development build.
- Mixing React Navigation setup code with Expo Router in the same tree without need: duplicated navigators. Pick Expo Router.
- Forgetting to bump `version` and platform build numbers (or setting `autoIncrement` in eas.json): store rejects the upload.
- Assuming OTA updates can change native code: `eas update` ships JS and assets only. Native changes need a new build.

## Review
- [ ] `expo-doctor` and `expo install --check` are clean.
- [ ] No secrets in `EXPO_PUBLIC_` vars or app.json.
- [ ] Native changes go through config plugins, with a note when a rebuild is required.
- [ ] EAS profile and channel are correct for the target.
- [ ] Tests run under `jest-expo`.
