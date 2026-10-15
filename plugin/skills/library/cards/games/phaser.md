---
name: phaser
title: Phaser
area: games
tags: [phaser, javascript, typescript, html5, arcade-physics, scenes]
detect: [dep:phaser]
related: [game-loop, game-physics, pathfinding, vitest]
---
Phaser 3 games: scenes with preload, create and update, Arcade physics, asset keys loaded once, logic split from scene code for testing.

## Verify
- `npx tsc --noEmit`: types check, including scene and config usage (TypeScript projects).
- `npx vitest run`: unit tests for logic modules pass in Node, with no canvas.
- `npm run build`: the production bundle builds.
- `npx eslint .`: lint passes.

## Test first
Phaser needs a canvas, so test plain logic classes in Node and keep scenes thin.
```ts
import { describe, it, expect } from "vitest";
import { Mover } from "../src/logic/mover";

describe("Mover", () => {
  it("advances by speed times dt", () => {
    const m = new Mover(0, 100);
    m.update(0.5);
    expect(m.x).toBe(50);
  });
  it("clamps to the world width", () => {
    const m = new Mover(790, 100, 800);
    m.update(1);
    expect(m.x).toBe(800);
  });
});
```

## Do
- Load every asset in `preload()` with a unique key (`this.load.image("player", url)`), and refer to it by key in `create()`.
- Configure the game once: `type: Phaser.AUTO`, `scale` with a fit mode, `physics: { default: "arcade" }`, and a scene list.
- Use `update(time, delta)` with `delta` in milliseconds, or prefer velocity on physics bodies so Arcade handles it.
- Use physics groups and `this.physics.add.collider` or `overlap` for collisions, with callbacks that only record the event.
- Use `this.events` and `this.registry` to communicate between scenes, and `this.scene.start` to switch.
- Clean up in the scene `shutdown` event (`this.events.once("shutdown", ...)`): timers, listeners and tweens you added.
- Use texture atlases and sprite sheets, and object pools through groups with `setActive(false)` and `setVisible(false)`.

## Avoid
- Creating game objects every frame in `update`: GC churn. Pool them or create in `create()`.
- Loading assets in `create()` without waiting: the texture is missing and shows a green box. Load in `preload`.
- Moving sprites by setting x and y on physics bodies: collisions break. Set velocity or use `body.reset`.
- Registering global DOM or `input` listeners without removing them on shutdown: duplicates after restart. Clean up in the shutdown event.
- Assuming a fixed frame rate: `delta` varies. Use delta or physics velocity.
- Importing browser-only Phaser code in unit tests: it touches `window`. Keep tested logic Phaser-free.

## Review
- [ ] Asset keys are unique, and each is loaded in `preload`.
- [ ] Scene shutdown removes timers, tweens and listeners.
- [ ] No object allocation inside `update`.
- [ ] Logic classes are tested without Phaser.
- [ ] The build output loads in a browser with no console errors.
