---
name: envoy
title: Envoy proxy
area: infra
tags: [envoy, proxy, xds, listeners, clusters, load-balancing, tls]
detect: [file:envoy.yaml, file:envoy*.yaml]
related: [istio, haproxy, nginx, traefik]
---
Envoy proxy configuration: listeners, routes and clusters validated before running, with explicit timeouts, health checks and admin lockdown.

## Verify
- `envoy --mode validate -c envoy.yaml`: config parses and validates without starting.
- `curl -s localhost:9901/clusters`: upstream hosts and health flags (admin interface).
- `curl -s localhost:9901/config_dump`: the config Envoy actually loaded.
- `curl -s localhost:9901/stats | grep upstream_rq_`: request counters and failures by cluster.

## Test first
Validate, then smoke-test the route.
```bash
envoy --mode validate -c envoy.yaml          # fails on a typo'd field
envoy -c envoy.yaml --base-id 1 & sleep 1
test "$(curl -s -o /dev/null -w '%{http_code}' localhost:10000/api/health)" = 200
test "$(curl -s -o /dev/null -w '%{http_code}' localhost:10000/nope)" = 404
```

## Do
- Use the v3 API: `typed_config` with `@type` URLs such as `type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager`.
- Define `clusters` with explicit `connect_timeout`, `lb_policy`, `health_checks` and `circuit_breakers` thresholds.
- Set route `timeout` and `retry_policy` (`retry_on`, `num_retries`, `per_try_timeout`) per route.
- Terminate TLS with `DownstreamTlsContext` and set minimum TLS version and ciphers; use `UpstreamTlsContext` with SNI and validation context for backends.
- Bind the admin interface to `127.0.0.1` only.
- Use `access_log` with a JSON format and `stat_prefix` on every filter for metrics.
- Use `outlier_detection` to eject bad hosts and `max_connections` to bound load.
- For dynamic setups use xDS with the ADS config source and ACK/NACK monitoring.

## Avoid
- Deprecated v2 or `config:` fields and `tls_context`: use `transport_socket` with typed config.
- Admin on `0.0.0.0`: it exposes shutdown and config dump. Bind to localhost.
- Missing `connect_timeout`: default is short, and a typo or omission gives 503 `UF` flags. Set it deliberately.
- Retries enabled on POST without idempotency: duplicate writes. Restrict `retry_on` and methods.
- `validation_context` absent on upstream TLS: Envoy does not verify the server. Add trusted CA and SAN matchers.
- Reading 503 as a backend error: check `response_flags` in logs (`UH`, `UF`, `NR`) to tell no-healthy-host, connect failure and no-route apart.

## Review
- [ ] `--mode validate` passes in CI.
- [ ] Every cluster has timeouts, health checks and limits.
- [ ] Upstream TLS verifies certificates.
- [ ] Admin is local-only.
- [ ] Retries match idempotency.
