---
name: aws-cloudwatch
title: AWS CloudWatch
area: cloud
tags: [aws, cloudwatch, logs, metrics, alarms, observability, emf]
detect: [dep:@aws-sdk/client-cloudwatch, dep:@aws-sdk/client-cloudwatch-logs, dep:aws-embedded-metrics, dep:@aws-lambda-powertools/metrics]
related: [aws-lambda, aws-ecs, aws-eks, aws-ec2, cloud-cost]
---
CloudWatch logs, metrics and alarms: structured JSON logs with retention, custom metrics through EMF, alarms with a missing-data policy that notify someone.

## Verify
- `aws logs describe-log-groups --query 'logGroups[?retentionInDays==null].logGroupName'`: groups that never expire.
- `aws cloudwatch describe-alarms --state-value INSUFFICIENT_DATA --query 'MetricAlarms[].AlarmName'`: alarms watching nothing.
- `aws cloudwatch describe-alarms --query 'MetricAlarms[].[AlarmName,AlarmActions,TreatMissingData]'`: each alarm has an action and a deliberate missing-data setting.
- `aws logs start-query --log-group-name G --start-time S --end-time E --query-string 'fields @timestamp, @message | filter level="ERROR" | limit 20'`: Logs Insights query works against the JSON fields.
- `aws cloudwatch set-alarm-state --alarm-name A --state-value ALARM --state-reason test`: the notification path fires.

## Test first
Assert the log line is parseable JSON with the fields alarms depend on.
```python
def test_error_log_has_level_and_request_id(caplog_json):
    handle({"id": "bad"})
    rec = caplog_json[-1]
    assert rec["level"] == "ERROR" and rec["request_id"]
```

## Do
- Log one JSON object per line with `level`, `message`, a request or trace id and the service name. Insights then filters by field.
- Set retention on every log group in IaC. Create the group yourself so the default never-expire does not apply.
- Emit custom metrics with Embedded Metric Format or the Powertools metrics helper, not a PutMetricData call per request.
- Keep metric dimensions low in cardinality (service, route, status class). A user id as a dimension multiplies cost.
- Alarm on symptoms: error rate, latency p99, queue age, DLQ depth. Set `TreatMissingData` on purpose (`notBreaching` for sparse traffic, `breaching` for heartbeats).
- Use composite alarms to reduce noise, and route actions to SNS wired to a pager or chat.
- Build one dashboard per service with the same four golden signals.
- Add metric filters for log patterns that have no native metric, and subscription filters to ship logs where needed.

## Avoid
- Logging secrets, tokens or full request bodies: logs are widely readable. Redact before logging.
- Unbounded retention: cost grows forever. Set days by data class.
- Alarms with no actions: they only color a console. Add an SNS action and test it.
- High-cardinality dimensions: each combination is a new billed metric. Move ids to log fields.
- Alarms on averages for latency: they hide the tail. Use percentiles via `ExtendedStatistic`.
- One PutMetricData per event: throttling and cost. Batch or use EMF.
- Debug-level logging in production by default: use a level variable.

## Review
- [ ] Log groups declared with retention.
- [ ] Logs are structured and redacted.
- [ ] Alarms cover errors, latency and backlog, each with an action and tested path.
- [ ] Custom metrics have bounded dimensions.
- [ ] A dashboard shows the service's health at a glance.
