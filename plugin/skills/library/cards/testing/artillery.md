---
name: artillery
title: Artillery
area: testing
tags: [testing, load, performance, yaml, node, http, websocket]
detect: [dep:artillery, dep:artillery-plugin-expect, file:artillery.yml, file:artillery*.yml]
related: [k6, gatling, locust, performance-regression]
---
Artillery: YAML scenarios with arrival phases, expectations and ensure thresholds that fail the run on SLO breach.

## Verify
- `artillery run test.yml`: runs the scenario and prints latency percentiles and error counts.
- `artillery run --output report.json test.yml`: writes a JSON result for CI parsing.
- `artillery run -e staging test.yml`: selects a named environment from the `config.environments` block.
- `artillery quick --count 10 --num 5 http://localhost:3000/health`: a fast smoke burst against one URL.

## Test first
Write the `ensure` thresholds first; a run that exceeds them fails with a non-zero exit code.
```yaml
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60
      arrivalRate: 10
  plugins:
    ensure: {}
  ensure:
    thresholds:
      - http.response_time.p95: 400
    conditions:
      - expression: "http.codes.200 > 0 and http.codes.500 == 0"
scenarios:
  - flow:
      - get:
          url: "/items"
          expect:
            - statusCode: 200
```

## Do
- Use arrival phases (warm-up, ramp, sustain) rather than one flat rate.
- Add `expect` per request and `ensure` thresholds globally.
- Load data with `payload` CSV files and capture values with `capture` for chained requests.
- Use `environments` for target and rates; keep secrets in env vars, referenced as `{{ $processEnvironment.TOKEN }}`.
- Add `think` between steps to mimic users.
- Use `processor` JS functions for signed requests or custom data generation.
- Save JSON output as a CI artifact and compare p95 across runs.

## Avoid
- Judging by the console summary only: thresholds are missing so nothing fails. Add `ensure`.
- Flat unrealistic rate from second zero: cold-start noise. Add a warm-up phase.
- Same payload every request: caches flatter results. Use a payload file.
- Running the generator on a laptop over wifi: the network is the bottleneck. Run near the target.
- Counting only HTTP 200: a 200 with an error body passes. Add `expect` on body content (`hasProperty`, `equals`).
- Pointing at production without a rate cap and approval: use a staging environment.

## Review
- [ ] Phases model realistic arrival, with a warm-up.
- [ ] `ensure` thresholds and `expect` checks exist.
- [ ] Payloads are varied; secrets come from env.
- [ ] Target is a safe environment.
- [ ] Results are stored for comparison.
