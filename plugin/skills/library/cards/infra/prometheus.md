---
name: prometheus
title: Prometheus
area: infra
tags: [prometheus, metrics, alerting, promql, monitoring, scrape]
detect: [file:prometheus.yml, file:prometheus.yaml, file:alerts.yml, file:rules/*.yml, file:*.rules.yml, file:alertmanager.yml]
related: [grafana, loki, opentelemetry, kubernetes]
---
Prometheus: pull-based metrics with scrape configs, recording and alerting rules, and PromQL that survives resets and cardinality.

## Verify
- `promtool check config prometheus.yml`: the config and referenced rule files are valid.
- `promtool check rules rules/*.yml`: rule syntax and PromQL expressions.
- `promtool test rules tests/*.yml`: rule unit tests with synthetic series.
- `promtool check metrics < /tmp/metrics.txt`: exposition output follows naming conventions (pipe `curl -s target/metrics`).
- `amtool check-config alertmanager.yml`: the routing tree and receivers parse.

## Test first
Rule unit tests live in `tests/*.yml` and run with `promtool test rules`.
```yaml
rule_files: [../rules/alerts.yml]
evaluation_interval: 1m
tests:
  - interval: 1m
    input_series:
      - series: 'up{job="api", instance="a"}'
        values: '1 1 0 0 0 0'
    alert_rule_test:
      - eval_time: 5m
        alertname: InstanceDown
        exp_alerts:
          - exp_labels: { severity: page, job: api, instance: a }
```
Red first: no alert fires until the `InstanceDown` rule with `for: 3m` exists.

## Do
- Name metrics `<namespace>_<name>_<unit>` with base units, and suffix counters `_total`.
- Use `rate()` or `increase()` on counters over a window of at least 4x the scrape interval.
- Use `histogram_quantile(0.99, sum by (le, job) (rate(x_bucket[5m])))` and aggregate buckets before the quantile.
- Add `for:` to alerts to avoid flapping, and `labels.severity`, `annotations.summary` and `runbook_url`.
- Precompute expensive queries as recording rules named `level:metric:operations`.
- Keep label values bounded: never user ids, URLs with ids or timestamps.
- Use service discovery with `relabel_configs` to keep only wanted targets, and `metric_relabel_configs` to drop noisy series.
- Alert on symptoms (error ratio, latency SLO burn) more than on causes.

## Avoid
- `rate()` of a gauge, or a counter without `rate`: wrong results. Use `deriv` for gauges and `rate` for counters.
- `rate(x[1m])` with a 1m scrape interval: too few samples, so gaps. Use `[5m]`.
- `avg(rate(...))` of per-instance quantiles: statistically wrong. Aggregate histogram buckets then take the quantile.
- High-cardinality labels (user_id, request path with ids): memory blowups. Normalize routes and drop labels.
- Alerts on `up == 0` with no `for`: pages on a single failed scrape. Add `for: 5m`.
- Division with unmatched labels (`a / b`): returns empty. Use `on(...)` or `ignoring(...)`.
- Using Prometheus as long-term or event storage: configure remote write to a durable store.
- Absent alerts missed: use `absent()` or `absent_over_time()` for metrics that can disappear.

## Review
- [ ] `promtool check config`, `check rules` and `test rules` pass.
- [ ] Each alert has `for`, severity, summary and a runbook link.
- [ ] Label cardinality is bounded and metric names follow conventions.
- [ ] Windows in `rate` are at least four scrape intervals.
