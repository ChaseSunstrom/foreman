---
name: anime-js
title: Anime.js
area: web
tags: [anime, animejs, animation, timeline, svg]
detect: [dep:animejs, dep:anime]
related: [animation, svg-canvas, accessibility, gsap]
---
Anime.js: small DOM, SVG and CSS animation engine with timelines, staggers and a scoped lifecycle in v4.

## Verify
- `npx tsc --noEmit`: targets and params type-check (v4 ships types; v3 needs `@types/animejs`).
- `npx eslint .`: lint.
- `npx playwright test --grep motion`: final styles with and without reduced motion.
- `npx vite build`: bundle check; v4 is tree-shakable, so import named functions.

## Test first
Seek to the end and assert the style, instead of waiting.
```ts
import { animate } from "animejs";

test("card slides to its resting place", () => {
  document.body.innerHTML = `<div class="card"></div>`;
  const a = animate(".card", { translateX: 100, duration: 500, autoplay: false });
  a.seek(a.duration);
  expect(document.querySelector<HTMLElement>(".card")!.style.transform).toContain("100px");
  a.revert();
});
```

## Do
- Check the installed major: v4 uses `import { animate, createTimeline, stagger } from "animejs"`; v3 uses a default `anime()` call. Do not mix syntax.
- Group animations with `createScope({ root })` and call `scope.revert()` on cleanup (v4); in v3 call `anim.pause()` and drop the reference.
- Use `createTimeline()` and offsets for sequences; `stagger()` for lists.
- Animate transforms and opacity; use `utils.set` for initial states.
- Draw SVG paths with `svg.createDrawable`, and move along paths with `svg.createMotionPath`.
- Gate on `matchMedia("(prefers-reduced-motion: reduce)")` and jump to the end state.
- Keep handles and `.revert()` them when the owning component unmounts.

## Avoid
- Selecting by broad class names across the page: scope the root.
- Starting animations during SSR: the package touches the DOM; run in an effect.
- Relying on callbacks for logic, such as `complete`, when the animation may be reverted or interrupted.
- Animating layout properties.
- Importing the whole namespace when only `animate` is used.

## Review
- [ ] Syntax matches the installed major version.
- [ ] Scopes or handles are reverted on teardown.
- [ ] Reduced motion is handled.
- [ ] Tests seek instead of sleeping.
- [ ] Only needed functions are imported.
