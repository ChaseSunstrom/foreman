---
name: outbox-pattern
title: Transactional outbox
area: design
tags: [outbox, messaging, consistency, database, events, reliability]
detect: []
related: [idempotency, event-driven, sagas, message-ordering, background-jobs]
---
Write the business row and its outgoing event in one DB transaction, then a relay publishes it at least once.

## Verify
- `pytest -q -k outbox`: the crash and duplicate tests below pass.
- `git grep -nE "publish\(|producer\.send" -- src`: every broker publish sits in the relay, never inside a request handler.
- `psql -c "select count(*) from outbox where published_at is null and created_at < now() - interval '5 min'"`: the backlog is not stuck.

## Test first
Fail the broker, commit, then recover: the event must still go out, once per consumer effect.
```python
def test_event_survives_broker_outage(db, broker):
    broker.down = True
    place_order(db, order_id=1)          # one tx: orders row + outbox row
    relay_once(db, broker)               # publish fails, row stays unpublished
    assert db.scalar("select count(*) from outbox where published_at is null") == 1
    broker.down = False
    relay_once(db, broker); relay_once(db, broker)
    assert [m.key for m in broker.sent].count("order-1") >= 1
    assert db.scalar("select count(*) from outbox where published_at is null") == 0
```

## Do
- Insert the outbox row (id, aggregate id, type, payload, created_at, published_at) inside the same transaction as the state change.
- Relay by polling with `FOR UPDATE SKIP LOCKED` in batches, or by tailing the WAL with CDC. Mark published only after the broker acks.
- Put a stable event id in every message so consumers dedupe (see idempotency).
- Key messages by aggregate id so per-aggregate order holds.
- Delete or archive published rows on a schedule; index `published_at is null`.

## Avoid
- Publish after commit in the handler: a crash between the two loses the event. Write the outbox row instead.
- Publish before commit: consumers see state that rolls back. Same fix.
- Marking published before the broker ack: loses events on failure. Mark after ack, accept duplicates.
- Several relays without row locks: duplicate floods and reordering. Use `SKIP LOCKED` per aggregate or a single leader.
- Unbounded table growth: polls slow down. Purge by age.

## Review
- [ ] State change and outbox insert share one transaction.
- [ ] Relay marks published only after broker ack.
- [ ] Consumers dedupe on event id.
- [ ] Outbox backlog age is monitored and alerted.
- [ ] Old rows are purged.
