---
name: opentelemetry
title: OpenTelemetry
area: infra
tags: [opentelemetry, otel, tracing, metrics, collector, otlp]
detect: [dep:@opentelemetry/api, dep:@opentelemetry/sdk-node, dep:opentelemetry-api, dep:opentelemetry-sdk, dep:go.opentelemetry.io/otel, dep:opentelemetry-*, file:otel-collector-config.yaml, file:otelcol.yaml]
related: [prometheus, grafana, loki, sentry]
---
OpenTelemetry: vendor-neutral traces, metrics and logs through SDKs, OTLP and the Collector.

## Verify
- `otelcol validate --config otel-collector-config.yaml`: the Collector config parses and components exist (binary name varies by distribution, such as `otelcol-contrib`).
- `curl -s localhost:13133`: the Collector's health_check extension reports up.
- `curl -s localhost:8888/metrics | grep otelcol_receiver_accepted_spans`: the Collector accepted spans.
- `OTEL_TRACES_EXPORTER=console <run app>`: the SDK emits spans locally without a backend.
- `env | grep ^OTEL_`: the service name, endpoint and protocol are set.

## Test first
Test instrumentation with an in-memory exporter and assert on finished spans.
```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

def test_checkout_emits_span():
    exp = InMemorySpanExporter()
    tp = TracerProvider(); tp.add_span_processor(SimpleSpanProcessor(exp))
    checkout(tracer=tp.get_tracer("t"), order_id="o1")
    assert [s.name for s in exp.get_finished_spans()] == ["checkout"]
```

## Do
- Set `OTEL_SERVICE_NAME` and `OTEL_RESOURCE_ATTRIBUTES` (`deployment.environment`, `service.version`), and `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Export OTLP to a local Collector (gRPC 4317 or HTTP 4318), and keep batching, retries and sampling there.
- Initialize the SDK before the app's imports and handlers, and shut down providers to flush on exit.
- Use auto-instrumentation for frameworks and add manual spans for business operations, with semantic-convention attribute names.
- Record errors on spans with `record_exception` and `set_status`.
- Propagate context with W3C `traceparent` and propagate across async and queue boundaries.
- In the Collector, order processors: `memory_limiter` first, then `batch` last, and wire receivers, processors and exporters in `service.pipelines`.
- Sample with `parentbased_traceidratio` or tail sampling in the Collector.

## Avoid
- Putting `memory_limiter` after `batch`: no protection from overload. Make it the first processor.
- Defining a component but not adding it under `service.pipelines`: it silently does nothing. Wire it.
- Unbounded attribute values (user ids as metric attributes, full URLs): cardinality explosion. Use bounded attributes on metrics.
- Old attribute names (`http.method`, `http.url`) in new code: renamed in semantic conventions. Use the current names for your SDK version.
- Wrong protocol and port pair (gRPC on 4318 or HTTP on 4317): connection errors. Match `OTEL_EXPORTER_OTLP_PROTOCOL`.
- Logging PII or secrets into span attributes: they ship to the backend. Redact with an `attributes` or `transform` processor.
- Creating a tracer provider per request: leaks. Create once at startup.
- No service name: spans show as `unknown_service`. Set it.

## Review
- [ ] Service name, environment and version resources are set.
- [ ] Collector pipelines wire every declared component with limiter and batch ordering.
- [ ] Spans and metrics carry bounded attributes, and no secrets.
- [ ] The provider flushes on shutdown and a test asserts spans.
