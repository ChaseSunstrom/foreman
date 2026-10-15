---
name: express
title: Express
area: node
tags: [express, node, http, api, middleware, rest]
detect: [dep:express]
related: [node, zod, jest, vitest, fastify]
---
Express apps: middleware order, async error handling, validation at the edge, testable app factory.

## Verify
- `npx tsc --noEmit`: types (TypeScript projects).
- `npx eslint .`: lint, including no-floating-promises when configured.
- `npm test`: the suite, driving the app through supertest with no listening port.
- `npm audit --omit=dev`: advisories in runtime deps.

## Test first
Export the app without calling `listen`; test with `supertest`.
```js
import request from 'supertest';
import { createApp } from '../src/app.js';

test('POST /users rejects missing email', async () => {
  const res = await request(createApp()).post('/users').send({});
  expect(res.status).toBe(400);
  expect(res.body.error).toMatch(/email/);
});
```
Call `listen` only in `server.js`.

## Do
- Build the app in `createApp()`; keep `listen` and signal handling in a separate entry file.
- Register order deliberately: security headers (`helmet`), body parser with a size `limit`, routes, 404 handler, then the error handler last with four arguments `(err, req, res, next)`.
- Validate `req.body`, `req.query` and `req.params` with a schema (zod) in middleware.
- Use `express.Router()` per resource and mount with a prefix.
- Set `app.set('trust proxy', ...)` to the real hop count when behind a proxy so `req.ip` and secure cookies work.
- Disable the banner: `app.disable('x-powered-by')` (or use helmet).
- Return JSON errors with one shape and never send stack traces in production.

## Avoid
- Async handlers that throw on Express 4: the rejection is unhandled and the request hangs. Wrap with a helper that calls `next(err)`; Express 5 forwards rejections itself, so check the installed major.
- `app.use(cors())` with no options or `origin: true` plus credentials: open to any site. Allow-list origins.
- `express.json()` with no `limit`, or parsing before auth on public routes: easy memory abuse.
- Error handler registered before routes, or with three arguments: it never runs as an error handler.
- `body-parser` as a separate dependency for new code: use `express.json()`.
- Interpolating `req.query` values into SQL, shell or file paths: use parameters and `path.resolve` with prefix checks.
- Calling `res.send` twice or after `next()`: "headers already sent". Return after responding.

## Review
- [ ] Error handler is last and covers async errors.
- [ ] Every input is schema-validated.
- [ ] CORS, helmet, rate limiting and body limits are explicit.
- [ ] `createApp` is importable by tests; no side effects at import.
- [ ] Secure cookies and `trust proxy` match the deployment.
