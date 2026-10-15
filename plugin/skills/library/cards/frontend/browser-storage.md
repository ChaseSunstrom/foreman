---
name: browser-storage
title: Browser Storage
area: frontend
tags: [localstorage, indexeddb, cookies, session, cache-api, security]
detect: [dep:idb, dep:dexie, dep:localforage, dep:idb-keyval, dep:js-cookie, dep:zustand, dep:redux-persist]
related: [pwa, forms, web-performance, auth-providers]
---
Pick the right client store: cookies for server-read session, localStorage for tiny prefs, IndexedDB for data, Cache API for responses.

## Verify
- `npx playwright test storage`: checks values survive reload and clear on logout, using `context.storageState()`.
- `npx tsc --noEmit`: typed accessors and schema versions agree.
- Devtools Application panel: inspect cookies flags (HttpOnly, Secure, SameSite), IndexedDB contents and quota.
- `curl -sI https://example.com/login -c - -d 'u=a&p=b'`: `Set-Cookie` carries `HttpOnly; Secure; SameSite`.

## Test first
Wrap storage in one module, then test corruption and logout.
```ts
import { test, expect } from 'vitest';
import { loadPrefs, savePrefs } from './prefs';

test('corrupt or old data falls back to defaults', () => {
  localStorage.setItem('prefs', '{not json');
  expect(loadPrefs()).toEqual({ v: 2, theme: 'system' });
  savePrefs({ v: 2, theme: 'dark' });
  expect(loadPrefs().theme).toBe('dark');
});
```

## Do
- Session or auth tokens: `HttpOnly; Secure; SameSite=Lax` cookies set by the server.
- localStorage and sessionStorage: small strings only (about 5MB), synchronous, so never in hot paths; always `JSON.parse` inside try and catch.
- IndexedDB for structured or large data, through `idb` or Dexie; version the schema and write migrations in `onupgradeneeded`.
- Wrap every access in try/catch: private modes, blocked cookies and quota errors throw.
- Namespace and version keys (`app:v2:prefs`); validate with a schema on read.
- Request persistence with `navigator.storage.persist()` for data that must not be evicted; check `navigator.storage.estimate()`.
- Clear all stores on logout; sync cross-tab state with the `storage` event or `BroadcastChannel`.
- Store only what you can regenerate or what the user created.

## Avoid
- JWTs or secrets in localStorage: any XSS reads them. Use HttpOnly cookies.
- Trusting stored values (prices, roles, flags): users edit them. Re-check on the server.
- Reading localStorage during server rendering: it does not exist. Guard with `typeof window` and read in an effect to avoid hydration mismatch.
- Storing large blobs or JSON arrays in localStorage: blocks the main thread. Use IndexedDB.
- Cookies without `SameSite`: CSRF exposure. Set it, plus CSRF tokens for state changes.
- Assuming data persists: browsers evict under pressure and users clear it. Treat as cache with server truth.
- Unversioned schemas: old shapes crash new code. Add a version field and migrate.

## Review
- [ ] No credentials or PII in script-accessible storage.
- [ ] All reads tolerate absence, corruption and old versions.
- [ ] Access is wrapped for quota and disabled-storage errors.
- [ ] Logout and account switch clear every store, including caches.
- [ ] SSR paths never touch browser-only APIs at render time.
