---
name: distributed-tracing
title: Distributed tracing
area: ops
tags: [tracing, opentelemetry, spans, sampling, context-propagation]
detect: [dep:@opentelemetry/api, dep:opentelemetry-api]
related: [log-pipelines, slos-alerting, canary-releases, incident-response]
---
Propagate trace context across every hop, sample deliberately, and verify one request yields one connected trace.

## Verify
- `curl -si -H 'traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01' https://svc.example.com/api/x`: the service accepts incoming context.
- `curl -s http://localhost:4318/ -o /dev/null -w '%{http_code}\n'`: the OTLP HTTP endpoint of the collector answers (a 404 or 405 still proves it is listening).
- `otelcol validate --config=otel-collector.yaml`: the collector config parses (OpenTelemetry Collector).
- `grep -rn '0af7651916cd43dd8448eb211c80319c' /var/log/app/ | head`: the same trace id shows in logs of every service.
- `ss -ltn | grep -E ':4317|:4318'`: the collector ports are open.

## Test first
Send one request with a known trace id through the whole path and require spans from every service.
```sh
tid=$(openssl rand -hex 16)
curl -s -H "traceparent: 00-$tid-b7ad6b7169203331-01" https://svc.example.com/checkout >/dev/null
sleep 10
n=$(curl -s "$TRACE_BACKEND/api/traces/$tid" | jq '[.. | .serviceName? // empty] | unique | length')
[ "$n" -ge 3 ] || { echo "trace broken: $n services"; exit 1; }
```
The test fails first at the hop that drops context (a queue consumer, an async job, an outbound client).

## Do
- Use W3C `traceparent` and `tracestate` propagation and one SDK family across services.
- Instrument HTTP, gRPC, database, and queue clients first, then add manual spans around business steps.
- Carry context through async boundaries: put it in message headers on the producer and extract it in the consumer.
- Set resource attributes (`service.name`, `service.version`, `deployment.environment`) on every service.
- Run a collector between apps and the backend, with batching, memory limits, and retry.
- Sample sensibly: head sampling for volume, tail sampling in the collector to keep errors and slow traces.
- Put `trace_id` in every log line so logs and traces cross-link.
- Keep attributes low-cardinality for metrics-from-spans, and keep secrets and personal data out of attributes.

## Avoid
- Context lost at a thread pool or async hop: traces split into orphans. Pass context explicitly or use the SDK's context-aware executors.
- 100% sampling in production at scale: cost and overhead. Use tail sampling that keeps errors and the latency tail.
- Different propagation formats per service (B3 and W3C mixed): gaps at the boundary. Standardize, or configure composite propagators.
- Spans with unbounded names (`GET /users/123`): the span list explodes. Use route templates (`GET /users/:id`).
- Exporting straight from the app to the backend with no buffer: backend trouble blocks or drops. Send to a local collector.
- PII in span attributes or URLs: it persists. Scrub in the SDK or the collector.

## Review
- [ ] One synthetic request produces a connected trace across all services.
- [ ] Async and queue hops propagate context.
- [ ] A sampling policy is written, with errors and slow traces always kept.
- [ ] `trace_id` appears in logs.
- [ ] Collector has batching, limits, and its own health metrics monitored.
