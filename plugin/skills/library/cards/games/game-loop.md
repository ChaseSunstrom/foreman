---
name: game-loop
title: Game loop and timing
area: games
tags: [game, loop, timestep, delta-time, determinism, frame-rate]
detect: []
related: [game-physics, multiplayer-netcode, pygame, phaser]
---
Game loop design: fixed-step simulation, decoupled rendering, delta-time clamping, deterministic updates you can test without a window.

## Verify
- Run the project's headless simulation test target (for example `pytest -q`, `cargo test` or `npm test`): the simulation steps with no window or GPU.
- `grep -rn "sleep(\|setTimeout(\|Thread.Sleep" src`: finds frame pacing done by sleeping instead of a timestep.
- `grep -rniE "random\(|rand\(|Date\.now|time\.time" src`: finds nondeterministic sources inside simulation code.

## Test first
Make the step a pure function of state, input and `dt`. Assert that 60 small steps equal one second.
```python
def test_fixed_step_matches_total_time():
    w = World(x=0.0, vx=10.0)
    for _ in range(60):
        w.step(1 / 60)
    assert abs(w.x - 10.0) < 1e-6

def test_huge_frame_is_clamped():
    loop = Loop(step=1 / 60, max_frame=0.25)
    assert loop.steps_for(5.0) <= 15
```

## Do
- Use a fixed simulation step with an accumulator: add the frame time, run `while acc >= step`, then render once with an interpolation factor `acc / step`.
- Clamp the frame time (about 0.25 s) so a stall or breakpoint cannot cause a spiral of death.
- Read input once per frame into a snapshot, and let the simulation consume the snapshot.
- Use a monotonic clock (`perf_counter`, `performance.now`, `Stopwatch`), never wall time.
- Keep simulation free of rendering calls so it can run headless and be replayed.
- Seed one RNG instance and pass it in. Record seed and inputs to reproduce a run.
- Vsync or frame cap paces rendering. The step size alone defines simulation speed.

## Avoid
- Multiplying by variable `dt` for physics: results vary with frame rate and tunnelling appears. Integrate with a fixed step.
- Sleeping to hit 60 fps: drift and jitter. Use vsync or a timed wait to a deadline.
- Missing clamp on `dt`: after a pause everything teleports. Clamp and cap steps per frame.
- Global `random` calls in the simulation: replays diverge. Inject a seeded RNG.
- Iterating a collection while adding or removing entities: queue spawns and removals, apply after the pass.
- Doing asset loading inside the update: hitches. Load ahead or in a background step.

## Review
- [ ] The simulation step takes explicit `dt` and runs under a test with no window.
- [ ] Frame time is clamped and steps per frame are capped.
- [ ] Rendering interpolates, and does not mutate simulation state.
- [ ] Randomness and time come from injected sources.
- [ ] Entity spawns and removals are deferred until the end of a pass.
