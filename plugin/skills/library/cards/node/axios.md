---
name: axios
title: Axios
area: node
tags: [axios, http, client, interceptors, timeouts, retries]
detect: [dep:axios]
related: [undici, zod, vitest, jest]
---
Axios HTTP client: one configured instance, explicit timeouts, typed responses validated at the edge, safe error handling.

## Verify
- `npx tsc --noEmit`: response generics and error narrowing compile.
- `npm ls axios`: a single resolved version (duplicates hide interceptor config).
- `npm audit --omit=dev`: advisories against the installed axios.
- `npx vitest run`: client tested against a mock server (msw or nock), not live hosts.

## Test first
Assert behavior against a stubbed network.
```ts
import axios, { isAxiosError } from 'axios';
import nock from 'nock';
import { api } from '../src/api';

test('maps a 404 to a typed NotFound without leaking headers', async () => {
  nock('https://svc.test').get('/users/9').reply(404, { error: 'nope' });
  const err = await api.get('/users/9').catch(e => e);
  expect(isAxiosError(err) && err.response?.status).toBe(404);
});
```

## Do
- Build one instance: `axios.create({ baseURL, timeout: 10_000, headers })`; share it.
- Always set `timeout`; the default is none. For hard cancellation pass `signal: AbortSignal.timeout(ms)`.
- Narrow errors with `axios.isAxiosError(e)` and branch on `e.response?.status`, `e.code` (`ECONNABORTED`, `ERR_CANCELED`).
- Validate `response.data` with a schema (zod) at the boundary; the `<T>` generic is not runtime checking.
- Cancel with `AbortController` (`signal`); `CancelToken` is deprecated.
- Retry only idempotent requests, with backoff and jitter (a small interceptor or `axios-retry`).
- Attach auth in a request interceptor; on 401 refresh once, guarded by a single in-flight promise.
- Set `maxContentLength` and `maxBodyLength` for untrusted endpoints.

## Avoid
- No timeout: a stalled server hangs the caller forever. Set one on the instance.
- Logging whole `AxiosError` objects: they include request headers (Authorization). Log status, code and URL only.
- Passing user-controlled URLs directly: SSRF. Allowlist hosts and block private ranges.
- `validateStatus: () => true` everywhere, then forgetting to check status: failures look like success.
- Mutating `axios.defaults` globally in libraries: use an instance.
- Trusting `<T>` as validation: parse the data.

## Review
- [ ] One instance with `baseURL` and a `timeout`.
- [ ] Errors are narrowed with `isAxiosError` and mapped to domain errors.
- [ ] Response data validated before use.
- [ ] Retries only on safe methods, with a cap.
- [ ] Secrets never appear in logs or error messages.
