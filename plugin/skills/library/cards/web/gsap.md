---
name: gsap
title: GSAP
area: web
tags: [gsap, animation, timeline, scrolltrigger, tween]
detect: [dep:gsap, dep:@gsap/react]
related: [animation, react, accessibility, web-performance]
---
GSAP: imperative tween and timeline engine with ScrollTrigger; every animation needs an owner that reverts it.

## Verify
- `npx tsc --noEmit`: tween vars and plugin imports type-check.
- `npx eslint .`: lint, including react-hooks rules for the cleanup.
- `npx playwright test --grep motion`: end state with `reducedMotion: 'reduce'` and with motion on.
- `npx vite build --report 2>&1 | grep -i gsap`: confirms only the plugins you register are bundled.

## Test first
Assert the end state, not frames; jump timelines to the end instead of sleeping.
```ts
import gsap from "gsap";
import { buildIntro } from "./intro";

test("intro ends visible and leaves no tweens behind", () => {
  document.body.innerHTML = `<h1 class="hero" style="opacity:0"></h1>`;
  const ctx = gsap.context(() => buildIntro(".hero"));
  gsap.globalTimeline.progress(1);
  expect(getComputedStyle(document.querySelector(".hero")!).opacity).toBe("1");
  ctx.revert();
  expect(gsap.globalTimeline.getChildren().length).toBe(0);
});
```

## Do
- Create animations inside `gsap.context(() => {...}, scopeEl)` and call `ctx.revert()` on unmount; in React use `useGSAP` from `@gsap/react` with a `scope` ref.
- Call `gsap.registerPlugin(ScrollTrigger)` once, at the app entry, not per component.
- Build sequences with `gsap.timeline({ defaults: { duration: 0.6, ease: "power2.out" } })` and position tweens with labels or `"<"`, not hand-added delays.
- Animate transforms (`x`, `y`, `scale`, `rotation`) and `opacity`; use `autoAlpha` to also toggle visibility.
- Use `gsap.matchMedia()` for responsive and `(prefers-reduced-motion: reduce)` branches; it reverts on change.
- Call `ScrollTrigger.refresh()` after fonts and images load, and `ScrollTrigger.kill()` on teardown.
- Use `gsap.quickTo` for pointer-follow values instead of creating a tween per mousemove.

## Avoid
- Selectors like `".box"` in React without a `scope`: they hit other components. Scope or use refs.
- Tweens created in render or in an effect with no revert: duplicates under StrictMode double-invoke.
- Touching `window` or `document` at module top in SSR frameworks: import plugins inside the effect or a client-only module.
- Animating `width`, `height`, `top`, `left`: layout thrash. Use transforms or `Flip`.
- Importing `gsap/all`: ships every plugin. Import only the ones used.
- Mixing CSS `transition` on the same properties: the two fight.

## Review
- [ ] Every tween and ScrollTrigger is created in a context and reverted on cleanup.
- [ ] Plugins are registered once and imported individually.
- [ ] A reduced-motion branch exists (matchMedia or a skipped timeline).
- [ ] Nothing GSAP runs during server render.
- [ ] Tests jump to the end state and do not wait on durations.
