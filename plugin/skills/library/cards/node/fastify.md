---
name: fastify
title: Fastify
area: node
tags: [fastify, node, http, api, plugins, json-schema]
detect: [dep:fastify]
related: [node, zod, vitest, express]
---
Fastify services: encapsulated plugins, JSON Schema validation and serialization, `inject` testing.

## Verify
- `npx tsc --noEmit`: types, including route generics.
- `npx eslint .`: lint.
- `npm test`: the suite, using `app.inject()` with no port.
- `node -e "import('./src/app.js').then(async m=>{const a=await m.build();await a.ready();await a.close()})"`: every plugin loads and `ready` resolves.

## Test first
Build the app in a factory and use `inject`.
```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { build } from '../src/app.js';

test('POST /items validates body', async (t) => {
  const app = await build();
  t.after(() => app.close());
  const res = await app.inject({ method: 'POST', url: '/items', payload: {} });
  assert.equal(res.statusCode, 400);
});
```

## Do
- Export `build(opts)` that returns the instance; call `listen` only in the entry file.
- Put each feature in a plugin (`fastify.register(plugin, { prefix })`); share state with `decorate` and wrap with `fastify-plugin` only when it must escape encapsulation.
- Give every route a `schema` (`body`, `querystring`, `params`, `response`); response schemas also speed serialization and strip unlisted fields.
- Use `setErrorHandler` for one error shape; throw errors with `statusCode`.
- Use the built-in `logger` (pino); pass a request-scoped `request.log`.
- Use `@fastify/*` official plugins (`cors`, `helmet`, `rate-limit`, `jwt`) and register them first.
- Close with `await app.close()` and run `onClose` hooks for pools.

## Avoid
- Mixing `async` handlers with the `done` callback: call one or the other. Return the payload or `reply.send` in async handlers, never both.
- Calling `reply.send` and also returning a value: double send. Return `reply` if you sent.
- Routes with no schema: no validation, slow serialization, no docs. Add one.
- `fastify-plugin` on everything: breaks encapsulation and leaks decorators. Use it only for shared decorators.
- Forgetting `await` on `register`/`ready` in tests: routes are not loaded yet.
- Using Express middleware by default: use `@fastify/middie` or `@fastify/express` only for a legacy bridge.
- Reading `request.body` before schema validation succeeded in a `preValidation` hook: it is unvalidated.

## Review
- [ ] Every route has body, params, query and response schemas.
- [ ] One error handler and one error shape.
- [ ] Plugins are encapsulated unless they must share decorators.
- [ ] Tests use `inject` and close the app.
- [ ] Logging redacts auth headers and secrets.
