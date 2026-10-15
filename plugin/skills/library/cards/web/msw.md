---
name: msw
title: Mock Service Worker
area: web
tags: [msw, mocking, network, api, testing, service-worker]
detect: [dep:msw]
related: [testing-library, playwright, storybook, tanstack-query]
---
MSW: intercept requests at the network layer with handlers (`http`, `graphql`), shared by tests, Storybook and the browser.

## Verify
- `npx vitest run`: tests pass with `onUnhandledRequest: "error"` set, so unmocked calls fail loudly.
- `npx msw init public/ --save`: the service worker file exists for browser use (only needed for the browser).
- `npx tsc --noEmit`: typed handlers and responses.

## Test first
Define handlers, start the server for the test run, override per test.
```ts
// setup (vitest setupFiles)
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

export const server = setupServer(
  http.get("/api/user", () => HttpResponse.json({ name: "Ada" })),
);
beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// in a test: the failure path first
server.use(http.get("/api/user", () => new HttpResponse(null, { status: 500 })));
```

## Do
- Use `msw/node` (`setupServer`) in Node tests and `msw/browser` (`setupWorker`) in the browser and Storybook.
- Start the server in `beforeAll`, reset in `afterEach`, close in `afterAll`.
- Keep happy-path handlers in one shared file and override per test with `server.use(...)`.
- Use `onUnhandledRequest: "error"` in tests.
- Respond with `HttpResponse.json(body, { init })`, `HttpResponse.text`, `new HttpResponse(null, { status })` or `HttpResponse.error()` for network failure.
- Use absolute URLs in Node when the code under test uses absolute ones, since relative URLs need a base in Node.
- Read request data with `await request.json()` and params from `params`; assert on them to verify what the client sent.
- Use `delay()` for loading-state tests and `once: true`-style one-shot overrides via `http.get(url, resolver, { once: true })`.

## Avoid
- The v1 `rest` API (`rest.get`, `res(ctx.json())`, `ctx`): removed in v2. Use `http` and `HttpResponse`.
- Forgetting `server.resetHandlers()`: overrides leak between tests. Reset in `afterEach`.
- Mocking `fetch` or axios by hand alongside MSW: two mocking layers. Use MSW only.
- Handlers that always succeed: untested error paths. Add 4xx, 5xx and network-error overrides.
- Shipping `mockServiceWorker.js` or starting the worker in production builds: guard on dev or test.
- `onUnhandledRequest: "bypass"` in tests: real network calls sneak in. Use `"error"`.
- Returning a plain object from a resolver: not a response in v2. Return `HttpResponse`.

## Review
- [ ] Unhandled requests fail the test.
- [ ] Handlers reset between tests; per-test overrides cover error paths.
- [ ] Handlers assert on the request payload where it matters.
- [ ] The worker script is not loaded in production.
- [ ] No second mocking layer wraps `fetch` or axios.
