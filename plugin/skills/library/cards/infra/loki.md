---
name: loki
title: Grafana Loki
area: infra
tags: [loki, logs, logql, promtail, alloy, labels]
detect: [file:loki-config.yaml, file:loki.yaml, file:loki-config.yml, file:promtail-config.yaml, file:promtail.yaml, file:alloy.config, file:config.alloy]
related: [grafana, prometheus, opentelemetry, kubernetes]
---
Loki: label-indexed log storage queried with LogQL, with low-cardinality labels and structured log lines.

## Verify
- `loki -config.file=loki-config.yaml -verify-config`: the config parses and validates, then exits.
- `curl -s localhost:3100/ready`: Loki reports ready.
- `logcli query '{app="api"} |= "error"' --since=15m`: logs reached Loki and the selector matches.
- `curl -s localhost:3100/loki/api/v1/labels`: the label names present, to spot cardinality problems.
- `promtool check rules loki-rules.yml`: ruler alert and recording rule syntax (LogQL expressions need Loki's ruler to evaluate).

## Test first
Push a known line and assert you can query it, then change the pipeline.
```sh
curl -s -X POST localhost:3100/loki/api/v1/push -H 'Content-Type: application/json' \
  -d "{\"streams\":[{\"stream\":{\"app\":\"t\"},\"values\":[[\"$(date +%s%N)\",\"level=error msg=boom\"]]}]}"
logcli query '{app="t"} | logfmt | level="error"' --since=1m | grep -q boom   # red until parse stage works
```

## Do
- Keep labels few and bounded (`app`, `namespace`, `env`, `cluster`, `level`). Loki indexes only labels.
- Put everything else in the line as structured JSON or logfmt and extract it at query time with `| json` or `| logfmt`.
- Filter selector first, then line filters (`|=`, `!=`, `|~`), then parsers, because filters are cheapest early.
- Use `sum by (level) (count_over_time({app="api"}[5m]))` and `rate(...)` for metrics from logs.
- Ship logs with Grafana Alloy (the successor to Promtail) using `loki.source.*` and `loki.write`, or an OpenTelemetry Collector with the OTLP endpoint.
- Set `limits_config` (`retention_period`, `ingestion_rate_mb`, `max_global_streams_per_user`) and enable the compactor for retention.
- Use object storage with the TSDB index and `schema_config` entries dated by `from`.
- Turn on `auth_enabled: true` with a tenant header (`X-Scope-OrgID`) for multi-tenant setups behind a gateway.

## Avoid
- Labels from high-cardinality values (`user_id`, `trace_id`, `pod_ip`, request path): stream explosion, slow queries and ingest rejections. Put them in the line and parse.
- Promtail for new deployments: end-of-life direction. Use Alloy.
- Changing `schema_config` in place: existing data becomes unreadable. Add a new period with a future `from` date.
- Wide regex line filters `|~ ".*"` first: slow scans. Prefer `|=` literals and narrow selectors.
- Querying with no selector or a broad one over long ranges: timeouts. Narrow labels and time.
- Filesystem storage in production: no durability or scale. Use S3-compatible or similar object storage.
- Unbounded retention with no compactor: disk fills. Configure retention.
- Multi-line stack traces split into many lines: unreadable. Use a multiline stage in the shipper.

## Review
- [ ] Labels are low-cardinality and queries start with a narrow selector.
- [ ] Log lines are structured and parse at query time.
- [ ] Schema, storage, retention and limits are set, with the compactor on.
- [ ] Shipper is Alloy or a Collector, with multiline handling.
