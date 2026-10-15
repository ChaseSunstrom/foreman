---
name: koa
title: Koa
area: node
tags: [koa, node, http, middleware, async, api]
detect: [dep:koa, dep:@koa/router, dep:koa-router]
related: [node, express, zod, jest]
---
Koa apps: async middleware cascade, `ctx` handling, centralized error middleware, testable app export.

## Verify
- `npx tsc --noEmit`: types (with `@types/koa`).
- `npx eslint .`: lint.
- `npm test`: the suite, using supertest against `app.callback()`.
- `npm ls koa @koa/router`: one copy of each, router matching the Koa major.

## Test first
Pass `app.callback()` to supertest; never bind a port.
```js
import request from 'supertest';
import { app } from '../src/app.js';

test('unknown route is a JSON 404', async () => {
  const res = await request(app.callback()).get('/nope');
  expect(res.status).toBe(404);
  expect(res.body).toEqual({ error: 'not_found' });
});
```

## Do
- Export the `Koa` instance; call `listen` only in the entry file.
- Put an error-handling middleware first: `try { await next() } catch (err) { ctx.status = err.status ?? 500; ctx.body = {...}; ctx.app.emit('error', err, ctx) }`.
- Attach a `app.on('error', ...)` listener for logging.
- Use `@koa/router` and mount with `app.use(router.routes()).use(router.allowedMethods())`.
- Parse bodies with `koa-bodyparser` or `@koa/bodyparser` with limits, before routes.
- Throw with `ctx.throw(400, 'msg')` for client errors.
- Set `app.proxy = true` only when behind a trusted proxy.
- Validate `ctx.request.body` with a schema in middleware.

## Avoid
- Forgetting `await next()` (or `return next()`): downstream middleware runs unawaited and responses race.
- Using `ctx.res.end` / `res.write` directly: bypasses Koa's response handling. Set `ctx.body`.
- Calling `next()` twice in one middleware: Koa throws.
- The old `koa-router` package for new code: use `@koa/router`.
- Generator-style middleware (`function*`, `koa-convert`): removed in Koa 3 and obsolete. Use `async`.
- Setting `ctx.body` after an error when the error middleware already responded: guard with `ctx.headerSent`.
- Reading the body before the body parser is registered: `ctx.request.body` is undefined.

## Review
- [ ] Error middleware is first and normalizes status and body shape.
- [ ] Every middleware awaits `next` exactly once.
- [ ] Body limits and proxy trust are explicit.
- [ ] `allowedMethods()` mounted so 405 and OPTIONS work.
- [ ] Tests use `app.callback()`.
