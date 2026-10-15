---
name: crdts
title: CRDTs
area: design
tags: [crdt, replication, convergence, merge, collaboration, eventual-consistency]
detect: []
related: [offline-first, multi-region, event-sourcing, message-ordering, websockets]
---
Use data types whose merge is commutative, associative and idempotent, so replicas converge regardless of delivery order or duplication.

## Verify
- `pytest -q -k crdt`: the three merge laws and convergence tests.
- `pytest -q -k "merge" --hypothesis-show-statistics`: property tests ran (when using Hypothesis).
- `git grep -nE "Date\.now\(\)|time\.time\(\)" -- src/crdt`: no wall-clock timestamps deciding merges.

## Test first
Pin the algebraic laws with random operation orders.
```python
@given(a=states(), b=states(), c=states())
def test_merge_laws(a, b, c):
    assert merge(a, b) == merge(b, a)                         # commutative
    assert merge(merge(a, b), c) == merge(a, merge(b, c))     # associative
    assert merge(a, a) == a                                    # idempotent

def test_replicas_converge_any_order():
    r1, r2 = Counter("r1"), Counter("r2")
    r1.inc(); r1.inc(); r2.inc()
    x = merge(r1.state, r2.state); y = merge(r2.state, r1.state)
    assert value(x) == value(y) == 3
```

## Do
- Choose the type by the need: G-Counter and PN-Counter (counts), LWW-Register (single value, loses concurrent writes), OR-Set (add and remove), sequence CRDTs for text and lists.
- Prefer a maintained library (Yjs, Automerge, or the data types in Riak and Redis Enterprise) over hand-written sequence CRDTs.
- Identify each replica with a unique id and use logical clocks (Lamport or version vectors), not wall time.
- State-based: ship full or delta state and merge. Operation-based: needs reliable, deduplicated causal delivery.
- Garbage-collect tombstones and metadata once all replicas have seen them, with a defined compaction protocol.
- Test with randomised partitions, duplicate and reordered delivery.
- Keep invariants that CRDTs cannot hold (uniqueness, non-negative balance) behind coordination.

## Avoid
- LWW with wall clocks across devices: clock skew silently drops writes. Use logical clocks or an OR-Set.
- Counters that decrement through a G-Counter: wrong. Use a PN-Counter.
- Unbounded tombstones: documents grow forever. Plan compaction.
- Assuming converged means correct for the user: merged text may be semantically wrong. Surface conflicts where it matters.
- Enforcing a balance limit with CRDTs alone: concurrent debits overspend. Use escrow or a coordinator.

## Review
- [ ] Type fits the semantics, including concurrent remove and add.
- [ ] Merge laws covered by property tests.
- [ ] No wall-clock dependency in merges.
- [ ] Tombstone and metadata growth bounded.
