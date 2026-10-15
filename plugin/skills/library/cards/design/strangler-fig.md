---
name: strangler-fig
title: Strangler fig
area: design
tags: [migration, legacy, refactoring, routing, incremental, rewrite]
detect: []
related: [modular-monolith, microservices, feature-flags, api-versioning, zero-downtime-migrations]
---
Replace a legacy system one route or capability at a time behind a facade, with the ability to roll each slice back instantly.

## Verify
- `pytest -q -k parity`: old and new implementations agree on recorded traffic.
- `curl -si localhost:8080/orders/1 -H "X-Route: legacy"`: the legacy path still answers (the header name is whatever your router honours).
- `git grep -nE "legacy|route_to_new" -- src/routing`: the routing table is the single switch point.

## Test first
Run the same requests against both and diff; then prove rollback.
```python
def test_new_matches_legacy_on_golden_traffic(legacy, new, golden_requests):
    for req in golden_requests:
        a, b = legacy.handle(req), new.handle(req)
        assert (a.status, normalise(a.body)) == (b.status, normalise(b.body)), req

def test_flag_flip_rolls_back(router, flags):
    flags.set("orders_new", True);  assert router.target("/orders/1") == "new"
    flags.set("orders_new", False); assert router.target("/orders/1") == "legacy"
```

## Do
- Put a facade (proxy, gateway or router) in front first; it initially forwards everything to legacy.
- Migrate by vertical slice (one route or capability with its data), smallest and lowest risk first.
- Switch with a flag or percentage rollout per tenant or user; keep legacy live until the slice is proven.
- Shadow traffic or dark-launch: send to both, serve legacy, compare results and log diffs.
- Decide data ownership per slice: sync both ways, or move ownership once with a cut-over. Avoid two writers for one record.
- Add an anti-corruption layer so the new code does not adopt legacy models.
- Delete the legacy path and routing flag once the slice is stable; track the remaining percentage.

## Avoid
- Big-bang rewrite with a date: it overruns and ships late. Slice it.
- Both systems writing the same data with no owner: divergence. Pick one writer per record.
- Leaving the flags forever: dead legacy paths remain. Schedule deletion.
- Skipping parity tests: behaviour quirks that clients rely on break. Replay recorded traffic.
- Migrating the hardest module first: no learning curve. Start small.

## Review
- [ ] Facade fronts all traffic.
- [ ] Each slice has parity checks and a rollback flag.
- [ ] One writer per record at any time.
- [ ] Legacy removal is tracked.
