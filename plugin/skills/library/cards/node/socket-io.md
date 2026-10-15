---
name: socket-io
title: Socket.IO
area: node
tags: [socketio, websocket, realtime, rooms, server, client]
detect: [dep:socket.io, dep:socket.io-client]
related: [express, fastify, nestjs, vitest, zod]
---
Socket.IO servers: typed events, rooms, auth in the handshake, acks for request/response, adapters for scaling out.

## Verify
- `npx tsc --noEmit`: typed event maps match emitters and listeners.
- `npx vitest run`: integration tests with a real server on an ephemeral port.
- `node -e "require('socket.io')"`: the server package resolves (not only the client).
- `npx eslint . --max-warnings 0`: lint.

## Test first
Start a real server on port 0 and connect a real client.
```ts
import { createServer } from 'node:http';
import { Server } from 'socket.io';
import { io as connect } from 'socket.io-client';

test('rejects a connection without a token', async () => {
  const http = createServer(); const srv = new Server(http);
  srv.use((s, next) => next(s.handshake.auth.token ? undefined : new Error('unauthorized')));
  await new Promise<void>(r => http.listen(0, r));
  const c = connect(`http://localhost:${(http.address() as any).port}`, { autoConnect: false });
  const err = await new Promise<Error>(r => { c.on('connect_error', r); c.connect(); });
  expect(err.message).toBe('unauthorized');
  c.close(); srv.close();
});
```

## Do
- Declare event maps: `new Server<ClientToServer, ServerToClient, InterServer, SocketData>(...)`.
- Authenticate in `io.use(...)` middleware from `socket.handshake.auth`, never from a first event.
- Validate every inbound payload (zod) before use; treat client data as untrusted.
- Use acks (`socket.emit('x', data, cb)` and `emitWithAck`) with a `timeout(ms)` for request/response.
- Scope broadcasts with rooms (`socket.join`, `io.to(room).emit`); join a per-user room on connect.
- Scale out with an adapter (Redis or similar) and sticky sessions when long-polling is enabled.
- Set `cors.origin` to an explicit list on the server.

## Avoid
- `cors: { origin: '*' }` with credentials: lock it to known origins.
- Registering listeners inside other handlers: they stack on every event. Register once per connection.
- Creating a client per render in a UI: connect once, clean up with `socket.off` and `close()`.
- Assuming delivery: events are lost while disconnected. Resync state on `connect`, or use connection state recovery.
- `io.emit` for per-user data: leaks to everyone. Target a room or socket id.
- Multiple server nodes without an adapter: broadcasts only reach local sockets.

## Review
- [ ] Handshake auth is enforced and tested for the failing case.
- [ ] Every inbound event validates its payload and handles a missing ack callback.
- [ ] Listeners are removed on disconnect or component teardown.
- [ ] CORS origins and transports are explicit.
- [ ] Multi-instance deployment has an adapter and sticky sessions.
