---
name: kafka-connect
title: Kafka Connect
area: data
tags: [kafka, connect, connectors, smt, dlq, converters]
detect: [file:connect-distributed.properties]
related: [kafka, debezium, etl-pipelines]
---
Kafka Connect connectors: config via the REST API, converters, error handling with a DLQ, offsets and task health.

## Verify
- `curl -s localhost:8083/connectors?expand=status`: every connector and task is RUNNING.
- `curl -s localhost:8083/connector-plugins`: the plugin is installed on the worker.
- `curl -s -X PUT -H 'Content-Type: application/json' -d @conn.json localhost:8083/connector-plugins/<ConnectorClass>/config/validate`: config errors before deploying.
- `curl -s localhost:8083/connectors/NAME/status`: task state and the failing trace.

## Test first
Test the config as data and the behavior with a bad record.
```python
def test_connector_config_has_dlq_and_converters():
    c = json.load(open("connectors/orders-sink.json"))["config"]
    assert c["errors.tolerance"] == "all"
    assert c["errors.deadletterqueue.topic.name"]
    assert c["value.converter"].endswith("JsonConverter") or "schema.registry.url" in str(c)
```

## Do
- Version-control each connector's JSON and apply it with `PUT /connectors/NAME/config` (idempotent create or update).
- Set converters explicitly per connector: `key.converter`, `value.converter` (Avro, Protobuf or JSON with a schema registry).
- Sinks: `errors.tolerance=all`, `errors.deadletterqueue.topic.name`, `errors.deadletterqueue.context.headers.enable=true`, `errors.log.enable=true`.
- Size `tasks.max` to partitions or tables; more tasks than partitions sits idle.
- Run distributed mode with replication factor 3 for `config.storage.topic`, `offset.storage.topic`, `status.storage.topic`.
- Keep secrets out of configs with `config.providers` and a file or vault provider (`${file:...}`).
- Use SMTs sparingly for light reshaping (`ExtractField`, `RegexRouter`); heavy logic belongs in a stream job.
- Restart a failed task with `POST /connectors/NAME/tasks/0/restart`.

## Avoid
- Putting passwords in connector JSON: the REST API returns them. Use config providers.
- Default `errors.tolerance=none` on sinks with dirty data: one poison record halts the task. Use a DLQ.
- Mismatched converters (schemaless JSON in, Avro expected): deserialization errors. Align with the producer.
- `tasks.max` guessed high for a source that supports one task: no gain, extra cost.
- Standalone mode in production: offsets in a local file, no failover.
- Changing a connector name to "restart": offsets are keyed by name, you reprocess or skip data. Pause, then resume, or reset offsets deliberately.

## Review
- [ ] Connector configs in version control, validated through the validate endpoint.
- [ ] DLQ and error logging set on sinks.
- [ ] Converters explicit; schema registry reachable.
- [ ] Internal topics replicated.
- [ ] Alerts on task state FAILED.
