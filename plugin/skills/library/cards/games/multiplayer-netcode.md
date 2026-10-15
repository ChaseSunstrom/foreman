---
name: multiplayer-netcode
title: Multiplayer netcode
area: games
tags: [multiplayer, netcode, prediction, rollback, interpolation, authoritative-server]
detect: [dep:colyseus, dep:@colyseus/core, dep:com.unity.netcode.gameobjects, dep:com.unity.netcode, dep:geckos.io, dep:enet]
related: [game-loop, game-physics, unity-ecs]
---
Game networking: authoritative server, client prediction and reconciliation, snapshot interpolation, lag-tolerant tests with simulated loss.

## Verify
- Run the project's test target with a simulated-link test (for example `pytest -q` or `npm test`): the protocol survives latency, loss and reordering in process.
- `grep -rnE "trust|isHost|authority" src`: lists where authority decisions are made, each of which must live server-side.
- `grep -rnE "Date\.now|time\.time|random\(" src/sim`: finds nondeterminism that breaks rollback or reconciliation.

## Test first
Wrap the transport in a fake link with delay, drop and reorder. Assert the client converges to the server state.
```python
def test_client_reconciles_after_dropped_snapshot():
    link = FakeLink(latency=0.1, loss=0.3, seed=1)
    server, client = Server(link), Client(link)
    for tick in range(300):
        client.send_input(tick, move=1)
        server.tick(); client.tick()
    assert abs(client.predicted.x - server.state[client.id].x) < 0.01

def test_server_rejects_speed_hack():
    server = Server(FakeLink())
    server.apply_input(player=1, move=100.0)
    assert server.state[1].speed <= MAX_SPEED
```

## Do
- Make the server authoritative: clients send inputs (not positions), the server simulates and broadcasts snapshots.
- Tag every input with a tick number. The client predicts locally, keeps a ring buffer of unacked inputs, and on each snapshot replays the unacked inputs from the server state.
- Render remote entities about 100 ms in the past by interpolating between two snapshots. Extrapolate only briefly.
- Use unreliable channels for fast state and reliable ordered channels for events such as chat and spawns.
- Send deltas, quantise floats (positions to fixed bits), and bound packet size to avoid fragmentation (stay below roughly 1200 bytes).
- Run the simulation on a fixed tick shared by both ends, with no wall-clock reads in it.
- Add handshake, protocol version, heartbeat and timeout so dead peers are dropped.

## Avoid
- Trusting client-sent state (position, damage, cooldown): cheating is trivial. Validate inputs server-side against the rules.
- Variable-dt simulation on both ends: prediction diverges. Use a fixed tick.
- Interpolating at the latest snapshot: motion stutters on jitter. Buffer and render in the past.
- Reliable ordered channel for movement: one lost packet stalls everything behind it. Use unreliable plus sequence numbers.
- Testing only on localhost: bugs hide at zero latency. Add simulated latency, jitter and loss to tests.
- Unbounded input or snapshot queues: memory growth under lag. Cap and drop oldest.

## Review
- [ ] Server validates every client input and owns all game-affecting state.
- [ ] Prediction, reconciliation and interpolation each have a test with loss and delay.
- [ ] Messages are versioned, size-bounded and rate-limited per peer.
- [ ] No wall-clock or unseeded random in the shared simulation.
- [ ] Disconnect, reconnect and timeout paths are covered.
