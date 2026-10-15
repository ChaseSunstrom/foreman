---
name: contract-testing
title: Contract testing
area: testing
tags: [contract, consumer-driven, pact, openapi, schema, microservices]
detect: [dep:pact-python, dep:@pact-foundation/pact, dep:github.com/pact-foundation/pact-go, dep:schemathesis, file:pacts/*.json]
related: [api-testing, integration-testing, test-doubles, e2e-strategy]
---
A contract pins the request and response shapes between a consumer and a provider, checked on both sides without a shared environment.

## Verify
- `npx jest consumer.pact.test.js`: consumer test runs against the Pact mock and writes a pact file under `pacts/`.
- `pytest -q tests/contract`: provider verification replays recorded interactions against the real app.
- `schemathesis run openapi.yaml --url http://localhost:8000`: the live API conforms to its OpenAPI schema.
- `git diff --stat pacts openapi.yaml`: the contract changed only when intended.

## Test first
The consumer writes the interaction it needs; it fails until the provider satisfies it.
```js
await provider
  .given("order 7 exists")
  .uponReceiving("get order 7")
  .withRequest({ method: "GET", path: "/orders/7" })
  .willRespondWith({ status: 200, body: { id: like(7), status: like("paid") } });
await provider.executeTest(async (mock) => {
  expect((await getOrder(mock.url, 7)).status).toBe("paid");
});
```
Consumer tests sit with the consumer; provider verification sits with the provider and loads the pact or schema.

## Do
- Match on shape and type (`like`, regex), not exact values, so the contract states needs, not data.
- Include only the fields the consumer reads.
- Name provider states and implement each as setup in the provider test.
- Publish or share contracts via a broker or a repository path, and verify on every provider build.
- Test failure responses too (404, 422 body shape).
- Run provider verification before deploy, and gate deploys on it.
- For schema-first APIs, lint the spec in CI and fuzz-check the live service against it.

## Avoid
- Exact-value matchers for generated ids and timestamps: brittle. Use type matchers.
- Contracts that assert business logic: that belongs in provider unit tests. Keep to shape and status.
- Provider states that do nothing: verification passes against empty data. Seed the state.
- Hand-editing pact files: regenerate from consumer tests.
- Treating a green contract as end-to-end proof: it checks the interface only. Keep a few integration checks.
- Letting the schema drift from the code: generate or validate one from the other.

## Review
- [ ] Matchers are type-based and minimal.
- [ ] Every provider state has real setup.
- [ ] Provider verification runs in CI and gates release.
- [ ] Error responses are covered.
- [ ] Contract files are generated, not hand-edited.
