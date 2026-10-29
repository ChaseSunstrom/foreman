---
name: theatre-js
title: Theatre.js
area: web
tags: [theatre, theatrejs, animation, timeline, studio, keyframes]
detect: [dep:@theatre/core, dep:@theatre/studio, dep:@theatre/r3f]
related: [three-js, react-three-fiber, animation, web-performance]
---
Theatre.js: keyframe animation toolkit; author in Studio, ship only `@theatre/core` with the exported state.

## Verify
- `npx tsc --noEmit`: prop types from `types.*` helpers.
- `npx eslint .`: lint.
- `npx playwright test --grep theatre`: the sheet plays to the end and the object values match.
- `npx vite build && grep -c "theatre/studio" dist/assets/*.js`: expect 0 matches in production.

## Test first
Run the sheet in core only, with exported state, and assert a value at a position.
```ts
import { getProject, types } from "@theatre/core";
import state from "./intro.theatre-project-state.json";

test("logo opacity is 1 at the end", () => {
  const sheet = getProject("Intro", { state }).sheet("Main");
  const logo = sheet.object("logo", { opacity: types.number(0, { range: [0, 1] }) });
  let value = -1;
  logo.onValuesChange(v => (value = v.opacity));
  sheet.sequence.position = sheet.sequence.length;
  expect(value).toBe(1);
});
```

## Do
- Load Studio only in development: `if (import.meta.env.DEV) { studio.initialize() }` behind a dynamic import.
- Export the project state from Studio, commit the JSON, and pass it to `getProject(name, { state })`.
- Define each animatable with `sheet.object(key, props)` using `types.number`, `types.compound`, `types.rgba` and ranges.
- Subscribe with `onValuesChange` and write to the DOM or scene; return the unsubscribe on cleanup.
- Play with `sheet.sequence.play({ iterationCount, range })` and `await project.ready` first.
- With R3F, use `@theatre/r3f` `editable` components and `SheetProvider`.
- Offer a skip path (`sequence.position = length`) for reduced motion.

## Avoid
- Shipping `@theatre/studio` to users: large and editable by anyone.
- Renaming sheets or objects after exporting: keyframes detach silently.
- Playing before `project.ready` resolves.
- Not unsubscribing `onValuesChange` listeners.
- Editing the state JSON by hand.

## Review
- [ ] Studio is dev-only and absent from the build.
- [ ] Project state JSON is committed and loaded.
- [ ] Object keys are stable and tested.
- [ ] Subscriptions are cleaned up.
- [ ] A reduced-motion path jumps to the end.
