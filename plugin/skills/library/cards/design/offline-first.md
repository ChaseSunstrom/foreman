---
name: offline-first
title: Offline-first
area: design
tags: [offline, sync, local-first, queue, conflict-resolution, mobile]
detect: []
related: [crdts, idempotency, optimistic-locking, retries-backoff, websockets]
---
The client reads and writes a local store first, queues mutations durably, and syncs idempotently when the network returns.

## Verify
- `pytest -q -k sync`: queue, replay and conflict tests against a fake server.
- `npx playwright test`: browser flow with the network toggled off, when the project uses Playwright.
- `git grep -nE "navigator\.onLine" -- src`: it is not the sole signal for connectivity; sync attempts decide.

## Test first
Mutate offline, crash, restart, reconnect twice: the server must apply the change once.
```python
def test_offline_writes_replay_once_after_restart(tmp_path, server):
    c = Client(tmp_path, server); server.online = False
    c.update("note1", "hello")                       # queued with op id
    assert c.read("note1") == "hello"                # visible locally
    c = Client(tmp_path, server)                      # restart: queue persisted
    server.online = True
    c.sync(); c.sync()                                # duplicate delivery
    assert server.applied == [("note1", "hello")]
    assert c.pending() == 0
```

## Do
- Persist the local store and the outbound mutation queue (IndexedDB, SQLite), so a crash loses nothing.
- Give each mutation a client-generated id (UUID) and make the server idempotent on it.
- Send intent-style operations or patches with a base version rather than full-state overwrites.
- Pull changes with a cursor or since-token; apply them transactionally and idempotently.
- Pick a conflict policy per entity: last-writer-wins on server-assigned order, field-level merge, a CRDT, or prompt the user.
- Retry with backoff and jitter; let a manual sync button and visible pending state exist.
- Use client-generated ids for new records so they can be referenced before sync.
- Version the local schema and migrate it on app upgrade.

## Avoid
- Treating `navigator.onLine` or reachability as truth: captive portals lie. Try the request and handle failure.
- An in-memory queue: closing the app loses edits. Persist.
- Replaying non-idempotent mutations: duplicates after retry. Dedupe by op id.
- Silent LWW with client clocks: skew drops edits. Use server order or logical clocks.
- Unbounded local growth: prune synced tombstones and caches.

## Review
- [ ] Queue durable across restart.
- [ ] Server dedupes mutation ids.
- [ ] Conflict policy documented per entity.
- [ ] Pending and failed sync state visible to the user.
