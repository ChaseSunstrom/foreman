---
name: chat-systems
title: Chat systems
area: domains
tags: [chat, websockets, messaging, ordering, presence, delivery]
detect: [dep:socket.io, dep:stream-chat]
related: [webrtc, notifications-system, unicode, rich-text-editors]
---
Realtime chat: per-conversation ordering, client-id dedupe, ack and resume on reconnect, read state, and fan-out across nodes.

## Verify
- `pytest -q tests/test_chat.py`: ordering, dedupe and resume tests pass.
- `npx vitest run chat`: client reducer handles duplicate, out-of-order and reconnect events.
- `grep -rn "Date.now()" src/chat`: client clock used for ordering (should be empty).

## Test first
A retried send after a dropped ack must not duplicate.
```python
from app.chat import send, history

def test_resend_with_same_client_id_is_deduped(db):
    a = send(db, conv="c1", user="u1", client_id="x1", body="hi")
    b = send(db, conv="c1", user="u1", client_id="x1", body="hi")
    assert a.id == b.id
    assert [m.body for m in history(db, "c1")] == ["hi"]
    assert a.seq == 1                    # server-assigned, monotonic per conversation
```

## Do
- Persist first, then broadcast. Assign a per-conversation `seq` on the server; clients order by it.
- Clients send a `client_id`; the server dedupes on `(conversation, client_id)` and acks with the stored id and seq.
- On reconnect the client sends its last seen seq; the server replays the gap. Use exponential backoff with jitter.
- Fan out across nodes with Redis pub/sub or a broker; keep sockets stateless.
- Authorize every join and send against membership; check on the server, not the client.
- Keep read state as a per-user last-read seq per conversation; unread count is the difference.
- Paginate history by seq cursor; render optimistic messages as pending until acked.
- Send heartbeats; mark presence with TTL, not by the disconnect event alone.
- Cap message size, rate limit per user, and escape on render.

## Avoid
- Ordering by client or arrival time: ties and skew reorder messages. Use server seq.
- Broadcasting before the DB commit: a crash shows a message that never existed.
- Presence as a boolean set on connect and cleared on disconnect: crashes leave users online. Use a TTL.
- One global room for all sockets: use per-conversation channels and authorize joins.
- Rendering message HTML unsanitized: stored XSS. Render text or sanitize.
- Unbounded history load on open: cursor paginate.

## Review
- [ ] Sends are idempotent by client id.
- [ ] Reconnect replays from last seq.
- [ ] Join and send are authorized server-side.
- [ ] Output is escaped or sanitized.
- [ ] Multi-node fan-out is tested or reasoned.
