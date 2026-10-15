---
name: websockets
title: WebSockets
area: design
tags: [websocket, realtime, protocol, heartbeat, reconnect, backpressure]
detect: [dep:ws, dep:socket.io, dep:websockets, dep:gorilla/websocket, dep:tokio-tungstenite, dep:@fastify/websocket]
related: [server-sent-events, event-driven, retries-backoff, concurrency]
---
WebSocket endpoints with an authenticated handshake, a versioned message envelope, heartbeats and bounded queues.

## Verify
- `npx wscat -c ws://localhost:8080/ws`: connect and exchange a message by hand.
- `curl -si -H 'Connection: Upgrade' -H 'Upgrade: websocket' -H 'Sec-WebSocket-Version: 13' -H 'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==' localhost:8080/ws`: the server answers 101 or rejects an unauthenticated upgrade with 401 or 403.
- `npm test` (or `pytest -q`, `go test -race ./...`): the suite, including connect, drop and reconnect cases.

## Test first
Open a real socket to an ephemeral-port server. Assert the protocol, not internals.
```js
test("rejects unknown message type with an error frame, stays open", async () => {
  const ws = new WebSocket(`ws://localhost:${port}/ws?token=${validToken}`);
  await once(ws, "open");
  ws.send(JSON.stringify({ v: 1, type: "nope" }));
  const [raw] = await once(ws, "message");
  expect(JSON.parse(raw)).toMatchObject({ type: "error", code: "unknown_type" });
  expect(ws.readyState).toBe(WebSocket.OPEN);
});
```

## Do
- Authenticate during the HTTP upgrade (cookie, or a short-lived ticket in the query or first message). Check `Origin` against an allowlist.
- Define an envelope: `{v, type, id, payload}`, validate every inbound frame, and ignore unknown fields.
- Send ping frames on an interval and close connections that miss pongs. Idle proxies drop silent sockets.
- Bound per-connection send queues and message size. Drop or close slow consumers rather than buffering without limit.
- Make clients reconnect with exponential backoff and jitter, and resume from a last-seen event ID.
- Authorize each subscription or action, not just the connection.
- Clean up subscriptions and timers on `close` and `error`.

## Avoid
- No `Origin` check on cookie-authenticated sockets: cross-site WebSocket hijacking. Compare it to an allowlist.
- Putting a long-lived JWT in the URL: it lands in logs. Use a one-time ticket that expires in seconds.
- Assuming a message arrives once and in order across reconnects: carry sequence numbers and make handlers idempotent.
- `JSON.parse` of frames without try/catch or schema validation: one bad frame crashes the handler. Validate and reply with an error frame.
- Holding state only in one process while running several instances: use a pub/sub backplane (Redis or similar) and sticky routing as needed.
- Reconnecting immediately in a tight loop: it creates a thundering herd after a deploy. Back off with jitter.

## Review
- [ ] Handshake authenticates and checks `Origin`.
- [ ] Inbound frames are validated and size-limited, and errors are returned as frames.
- [ ] Heartbeat and idle timeouts exist on both ends.
- [ ] Send queues are bounded, and slow clients are closed.
- [ ] A test covers reconnect and resume, and multi-instance fan-out is addressed.
