---
name: pwa
title: Progressive Web Apps
area: frontend
tags: [pwa, service-worker, manifest, offline, workbox, push]
detect: [dep:workbox-window, dep:workbox-build, dep:vite-plugin-pwa, dep:next-pwa, dep:@serwist/next, file:manifest.webmanifest, file:manifest.json, file:sw.js, file:service-worker.js]
related: [web-performance, browser-storage, seo, accessibility]
---
Installable, offline-capable web apps: a valid manifest, a carefully scoped service worker and a safe update path.

## Verify
- `npx lighthouse http://localhost:4173 --only-categories=best-practices,performance --quiet`: HTTPS, manifest and perf signals (the PWA category was removed in recent Lighthouse; use devtools Application panel for installability).
- `npx playwright test offline`: toggles `context.setOffline(true)` and asserts the shell still loads.
- `node -e "JSON.parse(require('fs').readFileSync('public/manifest.webmanifest'))"`: manifest is valid JSON.
- Devtools Application, Service Workers: shows state, scope, and update on reload.

## Test first
Prove offline behavior against the built app with a registered worker.
```ts
import { test, expect } from '@playwright/test';

test('shell loads offline after first visit', async ({ page, context }) => {
  await page.goto('/');
  await page.evaluate(() => navigator.serviceWorker.ready);
  await context.setOffline(true);
  await page.reload();
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
});
```

## Do
- Serve over HTTPS (localhost is exempt); register the worker after load.
- Manifest: `name`, `short_name`, `start_url`, `display: standalone`, `icons` at 192 and 512 (one `purpose: "maskable"`), `theme_color`, `background_color`.
- Choose strategies per resource: precache the hashed shell, stale-while-revalidate for content, network-first for HTML and API, cache-first for immutable assets.
- Use Workbox or the framework plugin rather than hand-rolled fetch handlers.
- Version caches and delete old ones in `activate`; prompt the user to reload when a new worker is waiting (`skipWaiting` only via explicit message).
- Provide an offline fallback page for navigation requests.
- Serve `sw.js` with `Cache-Control: no-cache` so updates are found.
- Request notification permission only after a user gesture with a reason.

## Avoid
- Caching the service worker file itself with a long max-age: users stick on old code forever. Use `no-cache`.
- `skipWaiting()` plus `clients.claim()` unconditionally: swaps code under an open page and breaks it. Prompt, then reload.
- Cache-first for HTML: shipped bugs persist. Use network-first or revalidate.
- Caching POST or authenticated API responses: leaks data across users on shared devices. Exclude them and clear on logout.
- Unbounded runtime caches: fills storage quota. Set `maxEntries` and `maxAgeSeconds` with ExpirationPlugin.
- A worker scope broader than needed: set `scope` to the app path.
- Treating a failed install as optional: handle `install` rejections and log them.

## Review
- [ ] Manifest and icons valid; app installs and launches standalone.
- [ ] Update flow tested: old tab, new deploy, reload prompt.
- [ ] Authenticated data is never served from a shared cache.
- [ ] Offline fallback exists and runtime caches are bounded.
- [ ] Worker file headers prevent stale registration.
