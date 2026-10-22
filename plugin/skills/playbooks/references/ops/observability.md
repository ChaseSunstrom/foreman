<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Observability: signals worth having

Use when adding a service, endpoint, job or queue; when an incident timeline had a gap ("we couldn't tell when it
started"); or when someone asks to "add logging". Every signal costs money and attention, so each one must answer a
question someone will ask during an incident (`incident.md`).

## The procedure

1. **Write the questions first.** Is it up? Is it slow, and for whom? Which deploy changed it? Where in the request
   did the time go? Is the queue keeping up? Pass: a short table in the service's docs maps each question to the
   signal that answers it; a signal with no question is removed.
2. **Metrics: RED per entry point, USE per resource.** Every inbound endpoint, consumer or job gets rate, errors
   and duration; duration is a histogram (read p50, p95, p99), never only an average. Every pool that can run out
   (connections, workers, queue, disk, memory) gets utilisation, saturation (queue depth, wait time) and errors.
3. **Keep labels bounded.** Labels hold a small fixed set: route template (`/orders/{id}`), method, status class,
   region, version. Never user ids, request ids, emails or raw paths. Pass: no metric exceeds 1,000 series; check
   the top series counts in your metrics backend after a load test.
4. **Logs are events, one JSON object per line.** Fixed fields: `ts` (UTC, ISO 8601), `level`, `event` (a stable
   snake_case name, not a sentence), `service`, `version`, `trace_id`. Values go in fields, never interpolated into
   text. Fields are an allowlist, so secrets and personal data can't leak by accident. Pass: the logger's test
   below, or your stack's equal, runs in CI.
5. **Levels mean actions.** `error`: a person must act. `warn`: degraded but handled (a retry succeeded, a fallback
   served). `info`: state changes (start, stop, config loaded, deploy). `debug`: off in production. Pass: an
   `error` line that nobody would act on is a defect.
6. **Traces follow the request across every hop.** Propagate W3C `traceparent` through HTTP calls, queue messages
   and scheduled jobs. One span per network hop or unit of work, not per function. Put `trace_id` on every log line.
   Keep every error and every slow trace; sample the rest.
7. **Stamp the version** on metrics, logs and traces, so a deploy shows as a boundary on every graph.
8. **Alert on symptoms, page on budget burn.** Page only for what users feel (error rate, latency, SLO burn); causes
   (CPU, disk at 70%) go to a ticket queue. Every page links its runbook. Pass: each paging rule names its runbook.
9. **Run a fire drill.** Break something on purpose in a test environment (a failing dependency, a slow query) and
   walk from the alert to the trace to the log line. Pass: done in under five minutes, and the path written in the
   runbook.

## A structured logger with the standard library

Python's `logging` can emit the event lines above without a dependency. The allowlist drops anything not named, as
the self-check shows:

```python
import io, json, logging, time

class JsonLines(logging.Formatter):
    FIELDS = ("trace_id", "route", "status", "ms")  # the allowlist: nothing else is written

    def format(self, r):
        out = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(r.created)) + f".{int(r.msecs):03d}Z",
               "level": r.levelname.lower(), "event": r.getMessage(), "service": r.name}
        out.update({k: getattr(r, k) for k in self.FIELDS if hasattr(r, k)})
        if r.exc_info:
            out["error"] = self.formatException(r.exc_info)
        return json.dumps(out, separators=(",", ":"), default=str)

buf = io.StringIO()
handler = logging.StreamHandler(buf)
handler.setFormatter(JsonLines())
log = logging.getLogger("orders")
log.addHandler(handler)
log.setLevel(logging.INFO)
log.info("request_done", extra={"trace_id": "4bf92f35", "route": "/orders/{id}", "status": 200, "ms": 41,
                                "password": "hunter2"})
line = json.loads(buf.getvalue())
assert line["event"] == "request_done" and line["status"] == 200 and line["ts"].endswith("Z")
assert "password" not in line, "the allowlist dropped it"
```

Add `version` the same way (a `logging.Filter` that sets it on every record), and keep the `event` names in one
place so a rename is a reviewed change.

## Checks

- [ ] Every entry point has rate, errors and a duration histogram; every finite pool has a saturation signal.
- [ ] No metric label holds an id, email or raw path; the largest metric stays under 1,000 series.
- [ ] Log lines parse as JSON and carry `ts`, `level`, `event`, `service`, `version`, `trace_id`.
- [ ] A test proves a non-allowlisted field (a password) never reaches the log.
- [ ] One request yields one trace across every service and queue it touches.
- [ ] Each paging rule is a user-facing symptom and links a runbook.
- [ ] The fire drill's path from alert to log line is written down.

## Library cards

`fm lib show opentelemetry` (SDKs, OTLP, the Collector), `fm lib show prometheus`, `fm lib show grafana`,
`fm lib show loki`, `fm lib show log-pipelines` (structured logs, correlation ids),
`fm lib show distributed-tracing`, `fm lib show slos-alerting`, `fm lib show sentry`, `fm lib show pii-logging`,
`fm lib show runbooks`.
