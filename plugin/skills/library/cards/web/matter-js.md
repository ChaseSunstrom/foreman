---
name: matter-js
title: Matter.js
area: web
tags: [matter, physics, 2d, engine, rigid-body, canvas]
detect: [dep:matter-js, dep:@types/matter-js]
related: [game-physics, game-loop, svg-canvas, web-performance]
---
Matter.js: 2D rigid-body physics engine; you own the render loop, the timestep and the cleanup.

## Verify
- `npx tsc --noEmit`: with `@types/matter-js`.
- `npx eslint .`: lint.
- `npx vitest run`: headless simulation tests.
- `npx playwright test --grep physics`: rendering and pointer interaction in a real browser.

## Test first
Step the engine by hand at a fixed delta; no renderer, no clock.
```ts
import Matter from "matter-js";

test("a box falls and rests on the ground", () => {
  const engine = Matter.Engine.create();
  const ground = Matter.Bodies.rectangle(0, 100, 400, 20, { isStatic: true });
  const box = Matter.Bodies.rectangle(0, 0, 20, 20);
  Matter.Composite.add(engine.world, [ground, box]);
  for (let i = 0; i < 600; i++) Matter.Engine.update(engine, 1000 / 60);
  expect(box.position.y).toBeGreaterThan(50);
  expect(Math.abs(box.velocity.y)).toBeLessThan(0.1);
  Matter.World.clear(engine.world, false);
  Matter.Engine.clear(engine);
});
```

## Do
- Step with a fixed delta (`Engine.update(engine, 1000 / 60)`) in your own `requestAnimationFrame` loop, or use a `Runner` with `isFixed: true`.
- For determinism, avoid `Math.random` in setup (use a seeded RNG), and step the same count; seed any custom randomness.
- Draw with `Render` for prototypes, but use your canvas, SVG or Pixi for products; read `body.position` and `body.angle`.
- Tag bodies with `label` or `plugin` data and use `Events.on(engine, "collisionStart", ...)` to react.
- Use collision `category` and `mask` filters rather than checking pairs by hand.
- Clean up on teardown: `Runner.stop`, `Render.stop`, `Events.off`, `World.clear`, `Engine.clear`, and remove the canvas.
- Scale the world: Matter works best with bodies of 10 to 100 units; do not simulate in meters.
- Pause when hidden (`visibilitychange`) and reduce bodies for reduced motion.

## Avoid
- A variable timestep from raw frame time: unstable stacking and tunneling. Clamp or fix it.
- Thin fast bodies: they tunnel through walls. Thicken walls or add substeps.
- Creating and discarding bodies without removing them from the world.
- Hundreds of complex compound bodies: use simple shapes.
- Testing against wall-clock time.

## Review
- [ ] Timestep is fixed or clamped.
- [ ] Simulation tests step manually and assert settled values.
- [ ] Teardown stops runners and clears the world.
- [ ] Collision filters are used instead of manual pair checks.
- [ ] Hidden tabs pause the simulation.
