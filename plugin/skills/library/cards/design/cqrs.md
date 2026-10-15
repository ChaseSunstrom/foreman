---
name: cqrs
title: CQRS
area: design
tags: [cqrs, read-model, commands, queries, projections, consistency]
detect: []
related: [event-sourcing, event-driven, outbox-pattern, domain-driven-design, read-replicas]
---
Separate the write path (commands that enforce invariants) from read models shaped for queries, and accept that reads lag.

## Verify
- `pytest -q -k "command or projection"`: commands validate, projections rebuild.
- `git grep -nE "import .*(read_model|queries)" -- src/domain`: the write side never imports read models.
- `git grep -nE "\.(query|select)\(" -- src/commands`: handlers do not run reporting queries.

## Test first
Pin the invariant on the write side, then prove the projection catches up and can be rebuilt from scratch.
```python
def test_projection_rebuild_matches_live(store, projector):
    handle(PlaceOrder(id="o1", qty=2), store)
    handle(CancelOrder(id="o1"), store)
    projector.catch_up()
    live = projector.read("o1")
    projector.reset(); projector.catch_up()
    assert projector.read("o1") == live == {"id": "o1", "status": "cancelled"}

def test_command_rejects_invalid_state(store):
    handle(CancelOrder(id="o1"), store)
    with pytest.raises(InvalidTransition):
        handle(CancelOrder(id="o1"), store)
```

## Do
- Commands return an id or ack, not data. Queries never mutate.
- Update read models from events (outbox or log), idempotently, keyed by event id or version.
- Keep a version or checkpoint per projection so replays are safe and resumable.
- Make rebuild-from-zero a tested operation; add a new read model by backfilling.
- Return the write version to the client so a follow-up read can wait for `>= version`.

## Avoid
- Splitting stores when one table and a view would do: CQRS costs a pipeline. Start with separate models over the same DB.
- Reading from the projection inside a command to decide validity: it is stale. Validate against write-side state.
- Non-idempotent projectors: redelivery double counts. Upsert by key and version.
- Showing users their own write missing: wait for version, or read-your-writes from the write store.
- Sharing one class for command and query shapes: they drift apart. Keep separate DTOs.

## Review
- [ ] Invariants enforced only on the write side.
- [ ] Projectors idempotent and replayable.
- [ ] Lag is measured and surfaced.
- [ ] Read-your-writes path defined for the UI.
