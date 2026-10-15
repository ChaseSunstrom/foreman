---
name: event-schemas
title: Event schemas
area: design
tags: [events, schema, compatibility, avro, protobuf, versioning]
detect: []
related: [event-driven, event-sourcing, outbox-pattern, api-versioning, message-ordering]
---
Events are a public contract: give each a schema, an explicit version, and a compatibility rule enforced in CI.

## Verify
- `pytest -q -k "schema or contract"`: old payloads still parse, new ones validate.
- `buf breaking --against '.git#branch=main'`: Protobuf changes are backward compatible (when using buf).
- `git grep -nE "schema_version|\"type\":" -- src/events`: every event carries a type and version.

## Test first
Replay stored old events through the current consumer; ignore unknown fields.
```python
@pytest.mark.parametrize("fixture", glob("tests/events/OrderPlaced.v*.json"))
def test_consumer_handles_every_historic_version(fixture):
    evt = json.load(open(fixture))
    order = on_order_placed(evt)                      # must not raise
    assert order.id and order.total >= 0

def test_unknown_fields_are_ignored():
    evt = {**load("OrderPlaced.v2.json"), "future_field": {"x": 1}}
    assert on_order_placed(evt).id == evt["order_id"]
```

## Do
- Envelope every event: `id`, `type`, `schema_version`, `occurred_at`, `producer`, `correlation_id`, `aggregate_id`, and a `data` payload.
- Define schemas in a registry or repo (JSON Schema, Avro, Protobuf) and validate on publish and consume.
- Evolve additively: add optional fields with defaults; never remove, rename, retype or reuse a field number or name.
- For breaking changes, publish a new type or version (`OrderPlaced.v2`), run both during migration, then retire v1.
- Name events as past-tense facts (`OrderPlaced`), carrying the data consumers need, with ids not whole entities.
- Tolerant reader: consumers ignore unknown fields and fail clearly on missing required ones.
- Keep golden fixtures of every published version and replay them in tests.

## Avoid
- Changing a field's meaning while keeping its name: silent consumer bugs. Add a new field.
- Making a field required later: old events fail. Keep optional or version up.
- Putting timestamps without timezone: ambiguity. Use UTC ISO-8601 or epoch with a unit.
- Events that mirror table rows: leaks internals and couples consumers. Model the business fact.
- No compatibility check in CI: breakage reaches production. Gate on a compatibility tool.

## Review
- [ ] Schema and version on every event.
- [ ] Compatibility check runs in CI.
- [ ] Historic fixtures replayed in consumer tests.
- [ ] Breaking changes use a new version with a migration window.
