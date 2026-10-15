---
name: mobile-app-security
title: Mobile app security
area: security
tags: [security, mobile, ios, android, keychain, deep-links]
detect: []
related: [tls, oauth2-oidc, api-keys, open-redirect, secrets-management]
---
Mobile clients: secrets in Keychain or Keystore, TLS everywhere, validated deep links, PKCE sign-in, and no trust in the client for authorization.

## Verify
- `./gradlew lint`: Android lint reports exported components, cleartext traffic and insecure storage (Android projects).
- `git grep -nE "usesCleartextTraffic|NSAllowsArbitraryLoads|allowBackup" -- ':!*test*'`: transport and backup settings.
- `git grep -nE "exported=\"true\"|android:exported" -- '*AndroidManifest.xml'`: every exported component is intentional.
- `gitleaks detect --source . --no-banner --redact`: no embedded keys in the app source.

## Test first
Ship a repo-level check on the manifest, and a unit test for link handling.
```python
import re, pathlib

def test_android_blocks_cleartext_and_backup():
    m = pathlib.Path("app/src/main/AndroidManifest.xml").read_text()
    assert 'usesCleartextTraffic="true"' not in m
    assert 'allowBackup="false"' in m

def test_deep_link_rejects_foreign_redirect():
    assert resolve_deeplink("myapp://login?next=https://evil.example") == "myapp://home"
    assert resolve_deeplink("myapp://order/42") == "myapp://order/42"
```

## Do
- Store tokens in the iOS Keychain (with an appropriate accessibility class) or the Android Keystore with encrypted preferences. Never use plain preferences, files or logs.
- Use short-lived access tokens with refresh rotation. Sign in through the system browser with OAuth authorization code plus PKCE.
- Require TLS on every connection, with App Transport Security and a network security config that forbids cleartext. Consider certificate pinning with a backup pin and an update path.
- Verify universal links and app links (the domain association files), and validate the host and every parameter in custom schemes before acting.
- Set `android:exported` explicitly and protect exported components with permissions. Use `FLAG_IMMUTABLE` on PendingIntents.
- Enforce authorization on the server. Any check in the app is advisory only.
- Disable backups of sensitive data, mask screens in app switchers and avoid the clipboard for secrets.
- Use biometric prompts bound to a Keystore or Keychain key, rather than a boolean result.
- Strip debug logging and test endpoints from release builds, and enable code shrinking.

## Avoid
- API secrets or signing keys inside the app binary: they are extractable. Keep them on the server and use per-user tokens.
- `NSAllowsArbitraryLoads` or a trust-all `TrustManager` to get past a certificate error: fix the certificate.
- WebViews with `javaScriptInterface` and loose URL loading: allow-list origins and disable file access.
- Trusting a jailbreak or root check as a security boundary: treat it as a signal only.
- Handling a custom-scheme deep link as authenticated input: another app can send any link. Re-validate and re-authenticate.
- Logging tokens or request bodies with the system logger: other tools may read them.

## Review
- [ ] Tokens live only in Keychain or Keystore.
- [ ] Cleartext and trust-all settings are absent and tested.
- [ ] Deep links and exported components validate their inputs.
- [ ] Sign-in uses the system browser with PKCE.
- [ ] The server enforces every authorization decision.
