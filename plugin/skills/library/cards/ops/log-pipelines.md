---
name: log-pipelines
title: Log pipelines
area: ops
tags: [logging, pipeline, structured-logs, retention, loki, vector]
detect: [file:vector.toml, file:fluent-bit.conf]
related: [distributed-tracing, slos-alerting, cost-monitoring, incident-response]
---
Ship structured logs with correlation ids through a buffered pipeline, and prove delivery, parsing, and retention with a canary line.

## Verify
- `vector validate vector.toml`: the Vector config parses and its components connect (Vector).
- `journalctl -u <unit> -o json -n 1 | jq .`: the source emits parseable JSON.
- `logger -t pipeline-canary "canary $(date +%s)"`: write a marker line to trace end to end.
- `df -h /var/log /var/lib/<buffer-dir>`: disks for logs and pipeline buffers have headroom.
- `journalctl --disk-usage`: journal size is bounded.

## Test first
Send a canary and require it to appear in the backend within a deadline; fail if it does not.
```sh
id="canary-$(date +%s)-$RANDOM"
logger -t pipeline-canary "$id"
for i in $(seq 30); do
  curl -s -G "$LOG_BACKEND/query" --data-urlencode "q=$id" | grep -q "$id" && exit 0
  sleep 2
done
echo "canary lost"; exit 1
```
Run it as a recurring probe and alert on failure; also test that a malformed line is dead-lettered, not dropped.

## Do
- Log JSON with fixed keys: `ts` (UTC, RFC 3339), `level`, `service`, `env`, `msg`, `trace_id`, `request_id`.
- Write to stdout and stderr (or the journal), and let the agent ship; apps do not manage files or rotation.
- Use disk-backed buffers in the agent so a backend outage does not lose or block logs; set a bounded size and an explicit overflow policy.
- Parse and normalize at the edge agent (timestamps, levels), and keep the raw line when parsing fails.
- Keep label or index cardinality low; high-cardinality values (user id, request id) go in the body, not labels.
- Redact secrets and personal data before shipping (tokens, passwords, emails), with a test.
- Set retention per class (debug short, audit long) and enforce it in the backend.
- Make audit and security logs tamper-evident and ship them off-host.

## Avoid
- Unstructured text with ad hoc regexes: parsing breaks on a format change. Emit JSON at the source.
- Request-id or user-id as an index label: the index explodes and queries crawl. Keep labels to a few bounded fields.
- Logging at debug in production by default: volume and cost balloon. Use sampling or a runtime toggle with an expiry.
- Memory-only buffers: a restart or outage loses the very window you need. Use disk buffering.
- Logging secrets or full request bodies: they sit in storage for the retention period. Redact and test for it.
- No delivery monitoring: the pipeline fails silently. Run the canary and alert on ingest lag and drop counters.

## Review
- [ ] Logs are structured and carry a trace or request id.
- [ ] A canary probe proves end-to-end delivery and alerts on failure.
- [ ] Buffers are disk-backed and bounded, with overflow behavior stated.
- [ ] Redaction has a test, and retention is configured per class.
- [ ] Label cardinality and ingest volume are monitored.
