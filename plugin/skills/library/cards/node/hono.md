---
name: hono
title: Hono
area: node
tags: [hono, web-standards, edge, api, typescript, middleware]
detect: [dep:hono, dep:@hono/node-server, dep:@hono/zod-validator]
related: [zod, bun, deno, vitest, trpc]
---
Hono apps on Web-standard `Request`/`Response`: typed routes, validators, middleware, testable via `app.request`.

## Verify
- `npx tsc --noEmit`: types, including typed context variables and RPC client types.
- `npx vitest run`: the suite, calling `app.request()` with no server.
- `npx eslint .`: lint.
- `npx wrangler deploy --dry-run`: Cloudflare Workers bundle builds (only if deploying there).

## Test first
`app.request` takes a path or `Request` and returns a `Response`.
```ts
import { describe, it, expect } from 'vitest';
import { app } from '../src/app';

describe('POST /todos', () => {
  it('400s on empty title', async () => {
    const res = await app.request('/todos', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ title: '' }),
    });
    expect(res.status).toBe(400);
  });
});
```

## Do
- Export `app` from its own module; adapters (`serve` from `@hono/node-server`, `export default app` on Workers/Bun) live in the entry file.
- Validate with `zValidator('json', schema)` (or `validator`) so handlers read `c.req.valid('json')`.
- Chain routes and `export type AppType = typeof routes` to use the typed `hc` client.
- Type env and variables: `new Hono<{ Bindings: Env; Variables: { user: User } }>()`.
- Use built-in middleware: `cors`, `secureHeaders`, `logger`, `jwt`, `bearerAuth`; register before routes they guard.
- Handle errors with `app.onError` and unknown routes with `app.notFound`.
- Return via `c.json(data, status)`.

## Avoid
- Reading `c.req.json()` directly after a validator: the body is already consumed in some runtimes. Use `c.req.valid`.
- Not chaining routes then expecting `AppType` inference: separate `app.get(...)` statements lose the route types. Chain or compose with `app.route`.
- Node-only APIs (`fs`, `Buffer`-only code) in code meant for Workers or Deno: it breaks at deploy.
- `cors()` with `origin: '*'` on credentialed endpoints: allow-list origins.
- Middleware registered after the route: it does not run. Order matters.
- Forgetting `await next()` in custom middleware: later handlers and post-processing never run.
- `@hono/node-server` imported in a Workers bundle: wrong adapter.

## Review
- [ ] All inputs pass a validator.
- [ ] `onError` returns one error shape.
- [ ] Middleware order is deliberate; auth precedes routes.
- [ ] No runtime-specific imports in shared modules.
- [ ] Tests cover one validation failure and one auth failure.
