---
name: slos-alerting
title: SLOs and alerting
area: ops
tags: [slo, sli, alerting, prometheus, burn-rate, error-budget]
detect: [file:alert*.rules.yml]
related: [on-call, runbooks, uptime-monitoring, incident-response, distributed-tracing]
---
Define SLIs from user-visible requests, set SLOs with error budgets, and page on budget burn rate, not on causes.

## Verify
- `promtool check rules alerts.rules.yml`: rule syntax and expressions parse (Prometheus).
- `promtool test rules alerts.test.yml`: alert rules fire and stay quiet on synthetic series.
- `promtool query instant http://localhost:9090 'sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))'`: the SLI returns a real number.
- `amtool check-config alertmanager.yml`: routing config parses.
- `amtool config routes test --config.file=alertmanager.yml severity=page team=api`: a labeled alert reaches the intended receiver.

## Test first
Unit-test the alert with `promtool test rules` before shipping it: a burn of 14x must fire, a blip must not.
```yaml
rule_files: [alerts.rules.yml]
evaluation_interval: 1m
tests:
  - interval: 1m
    input_series:
      - series: 'http_requests_total{job="api",code="500"}'
        values: '0+60x70'
      - series: 'http_requests_total{job="api",code="200"}'
        values: '0+1000x70'
    alert_rule_test:
      - eval_time: 65m
        alertname: ApiErrorBudgetFastBurn
        exp_alerts:
          - exp_labels: {severity: page, job: api}
```
Add a second test with healthy input and `exp_alerts: []`.

## Do
- Pick SLIs as ratios of good events to valid events: availability (non-5xx), latency (under a threshold bucket), freshness.
- State the SLO and window (for example 99.9% over 30 days) and compute the error budget from it.
- Alert on multi-window burn rate: a fast pair (1 h and 5 m at about 14x) pages, a slow pair (6 h and 30 m at about 6x) pages or tickets, and a 3 d and 6 h pair tickets.
- Put `severity`, `team`, `service`, and a `runbook_url` annotation on every alert.
- Page only on symptoms a human must act on now; send the rest to tickets or dashboards.
- Use `for:` clauses to ride out blips, and group, inhibit, and deduplicate in Alertmanager.
- Review the pages each week: delete or tune any alert that was noisy or not actionable.
- Use the remaining budget to decide release pace.

## Avoid
- Paging on CPU, memory, or one pod restart: users did not notice. Page on the SLI and graph causes.
- Alerts with no runbook link: the responder starts from zero. Require an annotation and lint for it.
- Averages for latency: the tail hides. Use histogram quantiles or the bucket ratio.
- An SLO of 100%: no budget, no change. Pick a target from what users tolerate.
- An alert that cannot fire because the metric disappeared: use `absent()` or a heartbeat (`vector(1)` watchdog) to page on silence.
- Untested rules: a typo means silent failure. Cover each with `promtool test rules`.

## Review
- [ ] Each SLO has a written SLI query, target, window, and owner.
- [ ] Alerts use burn rate over two windows, with severities routed correctly.
- [ ] Every paging alert has a runbook link and a `promtool` unit test.
- [ ] A watchdog alert proves the pipeline and routing are alive.
- [ ] Alert noise is reviewed on a schedule.
