---
name: browser-extension-security
title: Browser extension security
area: security
tags: [security, browser-extension, manifest, permissions, csp, webextension]
detect: []
related: [xss, security-headers, supply-chain-pinning, input-validation]
---
Extensions: minimal permissions, strict extension CSP, validated messages between worlds, no remote code, no secrets in storage that pages can reach.

## Verify
- `web-ext lint`: Mozilla's linter flags permission, CSP and manifest problems (when `web-ext` is installed).
- `git grep -nE "eval\(|new Function|innerHTML|document\.write|insertAdjacentHTML" -- 'src' ':!*test*'`: dynamic code and HTML sinks.
- `grep -nE '"(host_permissions|permissions|externally_connectable|content_security_policy)"' manifest.json`: review every grant and exposure.
- `npm audit --omit=dev`: bundled dependencies are checked.

## Test first
Messages from web pages must be validated before they trigger privileged actions.
```js
test("background ignores messages from untrusted senders", async () => {
  const sender = { url: "https://evil.example/", id: "other" };
  const res = await handleMessage({ type: "FETCH_TOKEN" }, sender);
  expect(res).toEqual({ error: "forbidden" });
});

test("content script renders page text as text", () => {
  render({ title: "<img src=x onerror=alert(1)>" });
  expect(document.querySelector("#panel img")).toBeNull();
});
```

## Do
- Request the narrowest `host_permissions`, and use `activeTab` or optional permissions requested at runtime instead of `<all_urls>`.
- Keep the extension-pages CSP strict: `script-src 'self'; object-src 'self'`. Bundle every script locally.
- In `onMessage` handlers, check `sender.id`, `sender.url` and `sender.origin`, then validate the message schema. Treat content-script messages as untrusted, since a compromised page can influence them.
- Limit `externally_connectable` and `web_accessible_resources` to named origins, and expose as little as possible.
- Use `textContent` or a templating framework that escapes. Sanitise any HTML from pages before inserting it.
- Keep tokens in `storage.session` or the background context, and out of content scripts and the page's DOM or `localStorage`.
- Make network calls from the background with fixed endpoints over HTTPS, and validate the responses.
- Ship with locked dependencies, minimal bundles and signed releases. Protect the publisher account with MFA.

## Avoid
- `<all_urls>` and `tabs` permissions for convenience: request per-site access when needed.
- `eval`, remote scripts or loaded CDN code: store policy bans them and they widen attack surface. Bundle code.
- `window.postMessage` with `"*"` as target or no origin check on receive: check `event.origin` and `event.source`.
- Passing page-controlled strings to `innerHTML` in injected UI: use `textContent`.
- Exposing privileged APIs to any page through web-accessible resources: restrict `matches`.
- Storing API keys in the bundle: users can read them. Use a backend with per-user auth.

## Review
- [ ] Permissions and host access are minimal and justified.
- [ ] CSP is strict and nothing loads remotely.
- [ ] Every message handler checks the sender and the schema.
- [ ] No HTML sinks take untrusted data.
- [ ] Secrets are not in the bundle or content-script reach.
