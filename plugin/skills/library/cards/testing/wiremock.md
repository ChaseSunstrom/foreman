---
name: wiremock
title: WireMock
area: testing
tags: [testing, http, mocking, stubs, java, api, integration]
detect: [dep:wiremock, dep:wiremock-standalone, dep:wiremock-jre8, dep:com.github.tomakehurst.wiremock*, file:mappings/*.json]
related: [http-mocking, contract-testing, integration-testing, test-doubles]
---
WireMock: a real HTTP server that stubs third-party APIs so tests exercise the actual client, serialization and timeouts.

## Verify
- `java -jar wiremock-standalone.jar --port 8089 --verbose`: the standalone server starts and logs each request match.
- `curl -s localhost:8089/__admin/mappings`: the stubs the server actually loaded.
- `curl -s localhost:8089/__admin/requests/unmatched`: no request fell through to a 404 (empty list means every call hit a stub).
- `mvn -q test` (or `gradle test`): the suite passes against the stubs.

## Test first
Point the client under test at the WireMock base URL and assert on both the result and the request it sent.
```java
@RegisterExtension
static WireMockExtension wm = WireMockExtension.newInstance()
    .options(wireMockConfig().dynamicPort()).build();

@Test
void retriesOnceOn503() {
    wm.stubFor(get("/rates").inScenario("r").whenScenarioStateIs(STARTED)
        .willReturn(status(503)).willSetStateTo("up"));
    wm.stubFor(get("/rates").inScenario("r").whenScenarioStateIs("up")
        .willReturn(okJson("{\"usd\":1.0}")));
    var rate = new RateClient(wm.baseUrl()).fetch();
    assertEquals(1.0, rate.usd());
    wm.verify(2, getRequestedFor(urlEqualTo("/rates")));
}
```

## Do
- Use `dynamicPort()` and inject `baseUrl()` into the client; never hard-code a port.
- Stub failure modes: `withFixedDelay`, `Fault.CONNECTION_RESET_BY_PEER`, 429 with `Retry-After`, malformed bodies.
- Verify the outbound request (headers, body, count) with `verify`, not just the response handling.
- Match narrowly: method, path, and the body fields that matter (`matchingJsonPath`), so wrong requests fail loudly.
- Record real traffic once (`--record-mappings`) to bootstrap stubs, then trim to what the test needs.
- Reset stubs and the request journal between tests (the extension does this per test).
- Use scenarios for stateful sequences like retry or pagination.

## Avoid
- Catch-all stubs like `urlMatching(".*")`: they hide wrong URLs. Match exact paths.
- Mocking the HTTP client class instead of the wire: serialization and header bugs pass. Stub at the server.
- A shared static server with stubs left from earlier tests: order-dependent failures. Reset per test.
- Never asserting unmatched requests: a typo'd path silently returns 404. Check `findAllUnmatchedRequests()` in teardown.
- Committing huge recorded mappings with real tokens or PII: scrub them before commit.
- Stubs that drift from the real API: pair with a contract test or periodic replay against the provider.

## Review
- [ ] Client base URL is injected and points at the dynamic port.
- [ ] Each test stubs at least one error or timeout path.
- [ ] Request verification covers headers and body, not only count.
- [ ] No leftover stubs between tests; unmatched requests fail the test.
- [ ] Recorded mappings contain no secrets.
