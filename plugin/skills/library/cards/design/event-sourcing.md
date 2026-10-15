---
name: event-sourcing
title: Event sourcing
area: design
tags: [event-sourcing, cqrs, aggregates, projections, snapshots, replay]
detect: [dep:eventstore, dep:@eventstore/db-client, dep:eventsourcing, dep:axon-*, dep:marten, dep:Marten, dep:esdb]
related: [event-driven, domain-driven-design, sagas, idempotency, state-machines]
---
State stored as an append-only event log, with aggregates rebuilt by folding events and read models built as projections.

## Verify
- `pytest -q tests/domain`: aggregate behavior given past events (pure, no database).
- `pytest -q tests/projections`: replaying the full log yields the same read model as live processing.
- `psql -c "select stream_id, version, count(*) from events group by 1,2 having count(*) > 1"`: no duplicate versions per stream (Postgres store with a `(stream_id, version)` key).

## Test first
Given/when/then on the aggregate with no I/O.
```python
def test_cannot_ship_unpaid_order():
    order = Order.rehydrate([OrderPlaced(id="o1", total=500)])
    with pytest.raises(DomainError, match="not paid"):
        order.ship()

def test_pay_emits_event():
    order = Order.rehydrate([OrderPlaced(id="o1", total=500)])
    assert order.pay(500) == [OrderPaid(id="o1", amount=500)]
```

## Do
- Treat events as immutable facts in the past tense. Commands decide, then emit zero or more events.
- Make `apply(event)` pure state mutation with no validation and no side effects, so replay is deterministic.
- Append with expected version (optimistic concurrency) and unique `(stream_id, version)`. Retry or surface conflict on mismatch.
- Upcast old event versions at read time instead of rewriting history.
- Build read models as projections that store their checkpoint and are idempotent. Rebuild by resetting and replaying.
- Snapshot only when replay cost demands it, and store the snapshot with its version.
- Keep the event payload free of derived data you can recompute, but include what the decision needed at that time (prices, rates).
- Store metadata: correlation ID, causation ID, actor, timestamp.

## Avoid
- Side effects (email, HTTP) inside `apply` or during replay: they fire again on every rebuild. Do them in reactors keyed on new events.
- Editing or deleting stored events to fix a bug: append a compensating event or upcast.
- Reading current time or random values inside `apply`: replay differs. Put them in the event at decision time.
- Sharing one aggregate across business concepts, producing huge streams: split along invariants.
- Treating projections as the source of truth, or reading them to enforce invariants: they lag. Enforce in the aggregate.
- Event-sourcing everything by default: use it where history and audit matter, plain tables elsewhere.
- PII in immutable events with no erasure plan: encrypt per subject and drop the key, or keep PII outside the log.

## Review
- [ ] `apply` is pure, and replay from zero reproduces current state in a test.
- [ ] Appends use expected version, and a conflict test exists.
- [ ] Projections are idempotent, checkpointed and rebuildable.
- [ ] Event schemas are versioned with upcasters, not edited.
- [ ] A GDPR or erasure strategy exists for personal data.
