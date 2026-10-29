---
name: tweakpane
title: Tweakpane
area: web
tags: [tweakpane, gui, debug, parameters, creative-coding]
detect: [dep:tweakpane, dep:@tweakpane/core, dep:@tweakpane/plugin-essentials]
related: [three-js, p5js, svg-canvas, web-performance]
---
Tweakpane: compact GUI for tweaking parameters live; a development tool that must not reach production.

## Verify
- `npx tsc --noEmit`: binding keys and option types (v4 uses `addBinding`).
- `npx eslint .`: lint.
- `npx vite build && grep -l tweakpane dist/assets/*.js`: expect no match in the production build.
- `npx playwright test --grep params`: URL or preset values load into the scene.

## Test first
Keep parameters in a plain object and test that, not the pane.
```ts
import { PARAMS, clampParams } from "./params";

test("params clamp to their declared ranges", () => {
  const out = clampParams({ ...PARAMS, speed: 999, count: -5 });
  expect(out.speed).toBeLessThanOrEqual(10);
  expect(out.count).toBeGreaterThanOrEqual(1);
});
```

## Do
- Check the major: v4 uses `pane.addBinding(obj, "key", opts)` and `addButton`; v3 used `addInput`.
- Keep a single `PARAMS` object that the scene reads each frame; the pane mutates it.
- Give bindings `min`, `max`, `step` for numbers and `options` for lists; use `addFolder` to group.
- Load the pane lazily and only in development: `if (import.meta.env.DEV) { const { Pane } = await import("tweakpane"); ... }`.
- Use `pane.on("change", ...)` or the per-binding `on("change")`; throttle expensive rebuilds.
- Export and import presets with `pane.exportState()` and `pane.importState()`.
- Call `pane.dispose()` on teardown, and use the Essentials plugin for FPS graphs.

## Avoid
- Shipping the pane to users unless it is a feature: hide behind a query flag.
- Reading the pane values directly in logic; read `PARAMS`.
- Rebuilding geometry on every `change` event while dragging a slider.
- Using v3 snippets with v4 installed.
- Forgetting to dispose: duplicate panes during hot reload.

## Review
- [ ] Pane code is dev-only or flag-gated and lazy.
- [ ] Parameters live in a typed object with ranges.
- [ ] Heavy rebuilds are throttled.
- [ ] `dispose()` runs on teardown and HMR.
- [ ] Presets round-trip through export and import.
