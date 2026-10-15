---
name: deep-links
title: Deep Links
area: mobile
tags: [deep-links, universal-links, app-links, ios, android, routing]
detect: [file:apple-app-site-association, file:assetlinks.json, file:*.entitlements]
related: [expo-router, swiftui-navigation, push-notifications, app-store-release]
---
Deep links: verified universal links (iOS) and app links (Android) mapped to routes, with server association files and strict parameter validation.

## Verify
- `curl -sI https://example.com/.well-known/apple-app-site-association`: returns 200 with no redirect and a JSON content type.
- `curl -s https://example.com/.well-known/assetlinks.json`: lists the package name and release signing certificate fingerprint.
- `adb shell am start -W -a android.intent.action.VIEW -d "https://example.com/orders/7" com.example.app`: opens the link in the app on a device.
- `xcrun simctl openurl booted "https://example.com/orders/7"`: opens the link in the booted simulator.
- `adb shell pm get-app-links com.example.app`: shows the verification state of each domain.

## Test first
The routing function is pure, so the failing test is for URL to route mapping, including hostile input.
```ts
import { parseLink } from './links';

test('maps order links and rejects junk', () => {
  expect(parseLink('https://example.com/orders/7')).toEqual({ route: 'order', id: 7 });
  expect(parseLink('https://example.com/orders/../admin')).toBeNull();
  expect(parseLink('https://evil.test/orders/7')).toBeNull();
});
```

## Do
- Host the association files at `/.well-known/` over HTTPS with no redirects, and serve them as `application/json`.
- On iOS add the `applinks:example.com` associated domain, and list paths in the `applinks` section of the `apple-app-site-association` file.
- On Android add an `<intent-filter android:autoVerify="true">` with `VIEW`, `DEFAULT`, `BROWSABLE` and the `https` scheme and host, and put each release and Play App Signing certificate SHA-256 in `assetlinks.json`.
- Convert every incoming URL to a typed route in one function, and use it for notifications, universal links and in-app taps.
- Handle cold start and warm start separately (iOS `onOpenURL` or scene delegate, Android `onNewIntent`).
- Require login by routing to sign-in and then to the stored target, and keep a sensible back stack.
- Provide a web fallback page on the same URLs for users without the app.
- Use deferred deep linking through a service only when installs must carry context.

## Avoid
- Custom URL schemes for sensitive flows: any app can claim them. Use verified https links.
- Trusting query parameters: they are attacker controlled. Validate hosts, paths and ids, and ignore unknown routes.
- Serving the association file behind a redirect or auth: verification fails silently. Serve it directly.
- Using only the debug certificate fingerprint in `assetlinks.json`: release builds are never verified. Add the Play signing key fingerprint.
- Acting on a link such as a payment or a logout without confirmation: links can be crafted. Show a confirmation.
- Caching the iOS association file expectation: Apple fetches through its CDN, so changes can lag. Test on a fresh install.

## Review
- [ ] Association files are valid, un-redirected and contain the release fingerprints and team and bundle ids.
- [ ] One parser maps URLs to routes and rejects unknown hosts and paths.
- [ ] Cold and warm start both open the right screen.
- [ ] Auth gating preserves the target, and sensitive actions confirm.
- [ ] A web fallback exists for each linkable path.
