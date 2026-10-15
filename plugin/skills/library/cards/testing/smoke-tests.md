---
name: smoke-tests
title: Smoke tests
area: testing
tags: [testing, smoke, deploy, health, ci, post-deploy, release]
detect: []
related: [e2e-strategy, integration-testing, api-testing, test-pyramid]
---
A small, fast, read-mostly suite that proves a deployed build is alive and wired to its dependencies, run after every deploy.

## Verify
- `curl -fsS https://HOST/healthz`: the health endpoint returns success (`-f` makes HTTP errors exit non-zero).
- `curl -fsS https://HOST/readyz | jq -e '.db == "ok"'`: readiness reports the dependencies it checked (needs jq).
- `./smoke.sh; echo $?`: the smoke script exits 0 only when every check passes.
- `pytest -m smoke -q` (or `npx playwright test --grep @smoke`): the tagged smoke subset runs on its own.

## Test first
Write the smoke check, run it against the broken or missing deploy to see it fail, then deploy.
```bash
#!/usr/bin/env bash
set -euo pipefail
base="${BASE_URL:?set BASE_URL}"
curl -fsS --max-time 5 "$base/healthz" >/dev/null
curl -fsS --max-time 5 "$base/api/version" | grep -q "\"sha\":\"${EXPECTED_SHA:?}\""
curl -fsS --max-time 10 "$base/api/items?limit=1" | grep -q '"items"'
echo "smoke ok"
```

## Do
- Keep it under a couple of minutes and a handful of checks: liveness, version or commit sha, one read through each critical dependency (database, cache, queue).
- Assert the deployed version matches the one just released, so you do not test the old pods.
- Make checks read-only or use a dedicated test tenant; clean up anything written.
- Put timeouts on every request and retry briefly while the rollout settles, then fail.
- Run the suite from outside the cluster, through the real public route (DNS, TLS, load balancer).
- Trigger rollback or alert on failure; make the exit code the contract.
- Tag the subset in the main test suite (`smoke` marker) to reuse it, with environment from variables.
- Run it in staging first, then production.

## Avoid
- A health endpoint that always returns 200: it proves only that the process runs. Check dependencies in readiness.
- Smoke checks that write production data without cleanup: pollution. Use read-only calls or a test tenant.
- No timeout or retry window: either hangs or flakes during rollout. Bound and retry.
- Growing the smoke suite into full regression: slow, so it gets skipped. Keep it tiny.
- Running only inside the pod: misses routing and TLS faults. Call the public URL.
- Not pinning the expected version: an old instance passes. Compare the release sha.

## Review
- [ ] Checks cover liveness, version and each critical dependency.
- [ ] Runs against the real public route with timeouts.
- [ ] Failure exits non-zero and blocks or rolls back the release.
- [ ] Read-only or isolated test data.
- [ ] Runtime stays within a couple of minutes.
