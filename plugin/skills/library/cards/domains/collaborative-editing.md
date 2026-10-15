---
name: collaborative-editing
title: Collaborative editing
area: domains
tags: [crdt, yjs, realtime, offline, conflict-resolution, awareness]
detect: [dep:yjs, dep:y-websocket, dep:@automerge/automerge]
related: [rich-text-editors, chat-systems, unicode, file-uploads]
---
Multi-user editing: CRDTs (or OT) for convergence, persisted updates, presence separate from content, and offline merge.

## Verify
- `npx vitest run collab`: convergence tests pass.
- `npx tsc --noEmit`: shared types and provider setup compile.
- `grep -rn "setInterval" src/collab`: polling-based sync left behind (should be empty).

## Test first
Two replicas edit offline, then merge in either order and converge.
```ts
import * as Y from "yjs";

test("concurrent offline edits converge regardless of merge order", () => {
  const a = new Y.Doc(), b = new Y.Doc();
  a.getText("t").insert(0, "hello"); Y.applyUpdate(b, Y.encodeStateAsUpdate(a));
  a.getText("t").insert(5, " A"); b.getText("t").insert(5, " B");
  const ua = Y.encodeStateAsUpdate(a), ub = Y.encodeStateAsUpdate(b);
  Y.applyUpdate(a, ub); Y.applyUpdate(b, ua);
  expect(a.getText("t").toString()).toBe(b.getText("t").toString());
  expect(a.getText("t").toString()).toContain("hello");
});
```

## Do
- Pick a proven CRDT library (Yjs, Automerge) over hand-rolled merge; bind it to the editor through its official binding.
- Persist incremental updates and periodically compact into a snapshot; load = snapshot plus later updates.
- Keep presence (cursors, selections, names) in a separate ephemeral channel, not in the document.
- Authenticate the socket and authorize per document; read-only users must not be able to send updates, enforced on the server.
- Use one shared document per file or page; split huge docs into subdocuments.
- Version snapshots for history and restore; restoring creates a new update, never a rewind of the log.
- Handle reconnect by exchanging state vectors, not full docs.
- Test with a fuzzer: random ops on N replicas, random delivery order, assert equality.

## Avoid
- Last-write-wins on the whole document: concurrent edits are lost. Merge at operation level.
- Storing only the latest rendered HTML: you cannot merge later. Store CRDT state, derive HTML.
- Letting clients write arbitrary types into the shared doc: validate schema on load or in the server hook.
- Unbounded history growth: enable garbage collection and compaction.
- Cursor positions as integer offsets: they shift under edits. Use relative positions from the library.
- Trusting client-side permission checks.

## Review
- [ ] Convergence tested with out-of-order and duplicate updates.
- [ ] Server enforces per-document authz including read-only.
- [ ] Persistence compacts and reloads cleanly.
- [ ] Presence is ephemeral.
- [ ] Offline reconnect path covered.
