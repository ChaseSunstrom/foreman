---
name: mobile-offline-sync
title: Mobile Offline Sync
area: mobile
tags: [offline, sync, local-first, conflicts, queue, mobile]
detect: []
related: [core-data, swiftdata, flutter, react-native, push-notifications]
---
Offline-first mobile sync: a local database as source of truth, an outbox of mutations, idempotent replay and explicit conflict rules.

## Verify
- `npm test`: sync engine and server idempotency tests pass (substitute the project's runner: `swift test`, `flutter test` or `./gradlew test`).
- `grep -rnE "Date\(\)|DateTime\.now|System\.currentTimeMillis" --include=*.swift --include=*.kt --include=*.ts --include=*.dart .`: lists wall-clock use that may be driving conflict resolution, for review.

## Test first
Test the sync engine with a fake transport that drops, duplicates and reorders requests.
```ts
test('replaying a queued mutation twice applies it once', async () => {
  const server = fakeServer();
  const db = memoryDb();
  await db.enqueue({ id: 'm1', op: 'rename', itemId: 1, name: 'B' });
  await sync(db, server);
  await sync(db, server);               // retry after a lost ack
  expect(server.items[1].name).toBe('B');
  expect(server.applied).toEqual(['m1']);   // idempotent by mutation id
});
```

## Do
- Read the UI from the local database only, observe it for changes, and update the screen from sync results, never from the network response directly.
- Write each change to the local database and an outbox table in one transaction, with a client generated mutation id (UUID) and a per-device sequence.
- Make server endpoints idempotent by mutation id, and return per-mutation results so partial success is handled.
- Pull with a server cursor or version token (`since=<token>`), not a client clock, and apply deltas in a transaction.
- Define conflict policy per entity: last-writer-wins on a server-assigned version, field-level merge, or a visible conflict for the user. Use version checks (`If-Match`, `baseVersion`).
- Use tombstones (`deleted_at`) for deletes, and purge them after all clients have synced.
- Schedule sync with the platform scheduler (WorkManager, BGTaskScheduler) with network constraints, plus exponential backoff with jitter, and sync on foreground and after local writes.
- Show sync state (pending count, last synced, error) to the user, and keep failed mutations until resolved.

## Avoid
- Treating a cache as a database: reads that fall back to the network mid-render give flicker and offline failures. Make the local store authoritative.
- Client wall-clock timestamps for ordering: clocks drift and users change them. Use server versions or hybrid logical clocks.
- Non-idempotent retries (create-without-id): duplicates after a lost response. Use client generated ids.
- Auto-increment ids assigned by the server before sync: offline-created rows lack ids. Use UUIDs.
- Dropping a mutation after a fixed number of failures: data loss. Park it, surface it and retry.
- Syncing in one huge payload on the main thread: memory spikes. Page and batch it in the background.
- Migrations that break queued mutations: version the outbox payload format.

## Review
- [ ] UI reads only from the local store, and writes go through the outbox transaction.
- [ ] Every mutation has an id, and the server dedupes it.
- [ ] Conflict policy is documented per entity and tested.
- [ ] Deletes use tombstones, and the cursor is server issued.
- [ ] Failure, retry and offline start paths are tested with a faulty fake transport.
