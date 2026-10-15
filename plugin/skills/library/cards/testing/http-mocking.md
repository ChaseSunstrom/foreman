---
name: http-mocking
title: HTTP mocking
area: testing
tags: [testing, http, mocking, stubs, network, msw, responses, nock]
detect: []
related: [wiremock, test-doubles, contract-testing, api-testing, async-tests]
---
Stub outbound HTTP at the network boundary so the real client code runs, failures are scriptable, and unexpected calls fail the test.

## Verify
- `pytest -q` with `responses` or `respx` active: the suite passes and any unmocked request raises instead of reaching the network.
- `npx jest` with `msw` set to `onUnhandledRequest: "error"`: unmatched calls fail the test (JavaScript).
- `go test ./...` using `httptest.NewServer`: the client talks to a real local server (Go).
- `unshare -n pytest -q` (Linux): with no network at all, the suite still passes, proving nothing escapes.

## Test first
Mock the wire, then assert on the request sent and the behavior on a bad response.
```python
import httpx, respx

@respx.mock
def test_client_raises_on_502():
    route = respx.get("https://api.example.com/rates").mock(
        return_value=httpx.Response(502))
    with pytest.raises(UpstreamError):
        fetch_rates()
    assert route.call_count == 1
```
```js
server.use(http.get("https://api.example.com/rates",
  () => new HttpResponse(null, { status: 502 })));
await expect(fetchRates()).rejects.toThrow("upstream");
```

## Do
- Mock at the transport (`respx`, `responses`, `msw`, `nock`, `httptest`), not by replacing your own client wrapper.
- Fail on unmatched requests so a typo'd URL or missing mock is loud.
- Script the failure matrix: 4xx, 5xx, 429 with `Retry-After`, timeout, connection reset, invalid JSON, empty body, slow response.
- Assert the request: method, path, query, headers (auth), and body.
- Build responses from realistic captured payloads; keep them as small fixture files.
- Register handlers per test and reset them in teardown.
- Back mocks with a contract test or scheduled check against the real provider so they cannot rot.

## Avoid
- Patching `requests.get` or `fetch` globally with a lambda: the client's headers, retries and parsing go untested. Mock the transport.
- Allowing real network by default: flaky and slow, and may hit production. Block it.
- Mocks that always return success: error handling ships untested. Add the failure cases.
- Hand-written payloads that differ from the real API: tests pass, production fails. Capture real ones.
- Handlers defined once at module level and mutated by tests: leaks. Reset per test.
- Asserting only the return value: a wrong request still passes. Assert what was sent.

## Review
- [ ] Mocking is at the transport; unmatched requests fail.
- [ ] Error, timeout and retry paths are exercised.
- [ ] Requests are asserted, including auth headers.
- [ ] Payloads match the real API and are checked against it.
- [ ] Handlers are reset between tests.
