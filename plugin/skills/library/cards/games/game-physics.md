---
name: game-physics
title: Game physics
area: games
tags: [physics, collision, rigidbody, fixed-step, tunnelling, determinism]
detect: [dep:matter-js, dep:pymunk, dep:planck, dep:planck-js, dep:rapier2d, dep:@dimforge/rapier2d]
related: [game-loop, godot-gdscript, unity, pathfinding]
---
Game physics: fixed-step integration, collision shapes and layers, continuous detection for fast bodies, kinematic character control.

## Verify
- Run the project's headless physics tests (for example `pytest -q`, `cargo test` or `npm test`): bodies step and collide with no renderer.
- `grep -rnE "dt *\*|delta *\*" src | grep -i "velocity\|force"`: finds variable-dt integration that should move into the fixed step.
- `grep -rn "position *[+-]\?= " src`: finds teleports that bypass collision.

## Test first
Assert on the physical outcome after N fixed steps, not on one frame.
```python
def test_fast_ball_does_not_tunnel_through_wall():
    w = World(gravity=(0, 0))
    ball = w.add_ball(x=0, vx=500.0, radius=0.5)
    w.add_wall(x=10, thickness=0.2)
    for _ in range(60):
        w.step(1 / 60)
    assert ball.x < 10

def test_rest_state_is_stable():
    w = World(gravity=(0, -9.8))
    b = w.add_box(y=0.5, on_ground=True)
    for _ in range(120):
        w.step(1 / 60)
    assert abs(b.vy) < 0.01
```

## Do
- Step physics at a fixed rate (50 or 60 Hz) and interpolate render positions between steps.
- Use collision layers and masks to say what hits what, so you avoid per-pair checks in game code.
- Move characters with the engine's kinematic API (velocity plus slide or `MovePosition`), not by writing position.
- Use continuous collision detection or swept shapes for bullets and anything faster than a shape's size per step.
- Keep the scale sane: about 0.1 to 10 units for dynamic bodies (the metre-sized assumption of Box2D-style engines).
- Use simple convex shapes or primitives for colliders. Keep detailed meshes for rendering.
- Put sensors and triggers on separate layers with overlap callbacks, and apply gameplay effects outside the solver callback.

## Avoid
- Variable `dt` in the solver: stacks explode and results differ per machine. Use a fixed step and clamp frame time.
- Changing bodies, joints or shapes inside a collision callback: the world is locked or corrupt. Queue changes and apply after the step.
- Concave mesh colliders on dynamic bodies: unstable or unsupported. Decompose into convex pieces.
- Scaling a rigidbody's transform at runtime: shapes desync. Rebuild the shape.
- Asserting exact floats: compare with a tolerance, since solvers are not bit-identical across platforms.
- Huge mass ratios between touching bodies: jitter. Keep ratios modest or use joints.

## Review
- [ ] Physics steps at a fixed rate independent of rendering.
- [ ] Fast objects use continuous or swept collision, with a test showing no tunnelling.
- [ ] Layers and masks are defined in one place.
- [ ] No body mutation from inside contact callbacks.
- [ ] Tests use tolerances and cover resting, collision and trigger cases.
