---
name: capacitor
title: Capacitor
area: mobile
tags: [capacitor, ionic, web, mobile, ios, android, hybrid]
detect: [dep:@capacitor/core, dep:@capacitor/cli, dep:@capacitor/ios, dep:@capacitor/android, file:capacitor.config.ts, file:capacitor.config.json]
related: [react-native, expo, fastlane, xcodebuild]
---
Capacitor: a web app in a native WebView with plugins, native iOS and Android projects, and `cap sync`.

## Verify
- `npx cap doctor`: Capacitor packages and native toolchain are healthy.
- `npm run build && npx cap sync`: web build is copied into native projects and plugins are updated.
- `npx tsc --noEmit`: types for the web layer.
- `npm test`: web unit tests (the repo's runner).
- `npx cap build android`: Android release build via Gradle, when the CLI supports it for your version (otherwise `cd android && ./gradlew assembleDebug`).

## Test first
Plugin calls hide behind a thin wrapper, so tests mock the plugin and check behavior.
```ts
import { vi, test, expect } from 'vitest';
vi.mock('@capacitor/preferences', () => ({
  Preferences: { get: vi.fn().mockResolvedValue({ value: null }) },
}));
import { loadTheme } from './theme';

test('defaults to light when nothing stored', async () => {
  expect(await loadTheme()).toBe('light');
});
```

## Do
- Set `appId`, `appName` and `webDir` in `capacitor.config.ts`; `webDir` must be the web build output folder.
- Run `npx cap sync` after every web build and after installing or removing plugins.
- Guard native-only code with `Capacitor.isNativePlatform()` and fall back on web.
- Use official plugin packages (`@capacitor/preferences`, `@capacitor/filesystem`, `@capacitor/camera`) and declare permissions in Info.plist and AndroidManifest.xml.
- Store tokens with a secure-storage plugin backed by Keychain and Keystore.
- Use `server.url` live reload only in development and remove it from production config.
- Commit the native `ios/` and `android/` folders, since they hold your native changes.

## Avoid
- Forgetting `cap sync`: the app runs stale web assets or missing plugins. Sync after each build.
- Leaving `server.url` pointed at a dev server in release builds: the app loads remote content. Gate it by environment.
- `Preferences` or `localStorage` for secrets: unencrypted on device. Use secure storage.
- `allowNavigation` with broad wildcards or cleartext HTTP enabled: widens attack surface. List exact hosts and use HTTPS.
- Calling plugin APIs on web without a web implementation: they reject or throw. Check platform or provide a fallback.
- Relying on browser-only features (service worker caching assumptions, third-party cookies) inside the WebView: behavior differs per platform. Test on devices.
- Mixing plugin major versions with the core: native builds break. Keep `@capacitor/*` majors aligned.

## Review
- [ ] Web build and `cap sync` run before native builds; `webDir` is correct.
- [ ] Production config has no dev `server.url` or cleartext allowances.
- [ ] Permissions declared natively and requested at runtime.
- [ ] Secrets in secure storage, not Preferences.
- [ ] Capacitor packages share one major version.
