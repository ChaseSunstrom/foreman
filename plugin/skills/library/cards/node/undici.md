---
name: undici
title: Undici
area: node
tags: [undici, http, fetch, agent, pool, mocking]
detect: [dep:undici]
related: [axios, node, vitest, node-streams]
---
Undici (Node's HTTP client): reuse Agents and Pools, consume every body, set timeouts, test with MockAgent.

## Verify
- `npx tsc --noEmit`: request options and body mixin types compile.
- `node -e "console.log(process.versions.undici)"`: the undici bundled with this Node (compare with the installed package).
- `npx vitest run`: tests using `MockAgent` with `disableNetConnect()`.
- `node --test`: the same checks with the built-in runner if the project uses it.

## Test first
Mock at the dispatcher so no socket opens.
```ts
import { MockAgent, setGlobalDispatcher, request } from 'undici';

test('surfaces non-2xx and consumes the body', async () => {
  const mock = new MockAgent(); mock.disableNetConnect(); setGlobalDispatcher(mock);
  mock.get('https://api.test').intercept({ path: '/x' }).reply(500, 'bad');
  const { statusCode, body } = await request('https://api.test/x');
  expect(statusCode).toBe(500);
  expect(await body.text()).toBe('bad');
  await mock.close();
});
```

## Do
- Create one `Agent` or `Pool` per origin and pass `dispatcher`; keep-alive only helps if connections are reused.
- Always consume or destroy the body: `await body.text()`, `.json()`, `body.dump()` or iterate it.
- Set `headersTimeout`, `bodyTimeout` and `connect: { timeout }` on the Agent; add `signal: AbortSignal.timeout(ms)` per request.
- Check `statusCode` yourself: `request` does not throw on 4xx or 5xx.
- Follow redirects explicitly with the `interceptors.redirect` composition or `maxRedirections` in versions that support it; `fetch` follows by default.
- Use `stream` or `pipeline` for large downloads rather than buffering.
- Use `ProxyAgent` or `EnvHttpProxyAgent` for proxies instead of ad hoc env handling.
- Match the package version with the Node-bundled global `fetch` when mixing `FormData` or `Request` types.

## Avoid
- Ignoring `body` on `request()`: the socket stays held and the pool stalls. Consume it or call `body.dump()`.
- A new `Client` per request: connection churn. Reuse an Agent.
- Mixing an npm `undici` `FormData`/`Headers` instance with global `fetch` from another version: type and runtime mismatch. Use the same source for both.
- Letting `fetch` hang with no signal: add `AbortSignal.timeout`.
- Disabling TLS verification (`rejectUnauthorized: false`) to fix a cert error: fix the CA instead.

## Review
- [ ] Every response body is consumed or destroyed on all code paths.
- [ ] Shared dispatcher with timeouts configured.
- [ ] Status handled explicitly.
- [ ] Tests use `MockAgent` with network disabled.
- [ ] No TLS verification bypass.
