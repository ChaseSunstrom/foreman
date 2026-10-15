---
name: nextjs-middleware
title: Next.js middleware
area: web
tags: [nextjs, middleware, edge, auth, redirects, matcher]
detect: [file:middleware.ts, file:middleware.js, file:src/middleware.ts]
related: [nextjs-app-router, nextjs-caching, nextjs]
---
Next.js middleware: a request-time function at the edge for redirects, rewrites, headers and coarse auth gating.

## Verify
- `npx tsc --noEmit`: `NextRequest` and `NextResponse` usage type-checks.
- `npx next build`: build fails on APIs unsupported in the edge runtime and prints the middleware size.
- `npx vitest run`: unit tests for the middleware function.
- `curl -si http://localhost:3000/PATH`: check status, `location` and added headers on a running server.

## Test first
Call the exported function with a `NextRequest` and assert on the response.
```ts
// middleware.test.ts
import { NextRequest } from "next/server";
import { middleware } from "./middleware";

test("redirects anonymous users from /dashboard", () => {
  const res = middleware(new NextRequest("http://t/dashboard"));
  expect(res.status).toBe(307);
  expect(res.headers.get("location")).toBe("http://t/login");
});
```

## Do
- Export `config = { matcher: [...] }` to limit paths; exclude `_next/static`, `_next/image` and the favicon.
- Keep it fast and small: read a cookie, verify a signed token with an edge-safe library (such as `jose`), redirect or continue.
- Return `NextResponse.next()` and set headers on that response, or `NextResponse.redirect(new URL("/login", req.url))`.
- Treat middleware as a first gate only: re-check authorization in the page, action and route handler that touch data.
- Forward request data downstream with `NextResponse.next({ request: { headers } })`.
- Check the installed version's docs for the file name and runtime: newer releases may rename or move it.

## Avoid
- Node-only APIs (`fs`, native modules, most ORMs and DB drivers) in edge middleware: they fail at build or runtime. Verify tokens only, query data elsewhere.
- Middleware as the only auth check: it can be bypassed by misconfigured matchers and does not protect server actions directly. Re-check in the data layer.
- A matcher that also catches static assets and API calls: extra latency and redirect loops. Anchor the matcher.
- Redirecting `/login` for unauthenticated users without excluding `/login`: infinite redirect loop.
- Heavy work (network calls to a database) per request: it runs on every matched path. Cache or move it.
- Relative redirect targets: use `new URL(path, req.url)`.

## Review
- [ ] The matcher is explicit and excludes assets and the login route.
- [ ] No Node-only imports; the build passes.
- [ ] Auth is enforced again in handlers and actions.
- [ ] No redirect loop for any logged-in or logged-out path.
- [ ] Tests cover allow, redirect and header cases.
