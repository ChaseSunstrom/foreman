---
name: lenis
title: Lenis smooth scroll
area: web
tags: [lenis, smooth-scroll, scroll, raf, scrolltrigger]
detect: [dep:lenis, dep:@studio-freight/lenis, dep:@studio-freight/react-lenis]
related: [animation, accessibility, web-performance, gsap]
---
Lenis: lightweight smooth-scroll that keeps native scrolling semantics; one instance, one driver loop, always destroyed.

## Verify
- `npx tsc --noEmit`: options and event types.
- `npx eslint .`: lint, including effect cleanup.
- `npx playwright test --grep scroll`: anchor links, keyboard scrolling and `scrollTo` land on the right offset.
- `npx lighthouse http://localhost:3000 --only-categories=performance,accessibility --quiet`: no regression after adding it.

## Test first
Drive the instance directly and assert the position, with smoothing disabled.
```ts
import Lenis from "lenis";

test("scrollTo with immediate lands on target", () => {
  const lenis = new Lenis({ autoRaf: false });
  lenis.scrollTo(400, { immediate: true });
  expect(Math.round(lenis.scroll)).toBe(400);
  lenis.destroy();
  expect(document.documentElement.classList.contains("lenis")).toBe(false);
});
```

## Do
- Create exactly one `new Lenis()` per page and share it through a module or context.
- Own the loop in one place: `autoRaf: true`, or drive `lenis.raf(time)` from the single `requestAnimationFrame` or `gsap.ticker` you already have, never both.
- With GSAP ScrollTrigger: `lenis.on("scroll", ScrollTrigger.update)`, `gsap.ticker.add(t => lenis.raf(t * 1000))` and `gsap.ticker.lagSmoothing(0)`.
- Include the recommended `lenis/dist/lenis.css`, which sets `html.lenis` rules.
- Call `lenis.destroy()` on unmount and remove any ticker callback you added.
- Nested scrollers need `data-lenis-prevent`; modals should call `lenis.stop()` and `lenis.start()` on close.
- Skip creating the instance when `prefers-reduced-motion: reduce` matches.

## Avoid
- Two instances or two rAF loops: double-speed, jitter and leaks.
- Creating it during SSR: guard with `typeof window` or a client-only effect.
- `scroll-behavior: smooth` in CSS alongside it: they fight.
- Smoothing scroll on touch with large `lerp` values: it feels laggy. Keep defaults.
- `position: fixed` content measured from `window.scrollY` without reading `lenis.scroll`.

## Review
- [ ] One instance, one frame driver, destroyed on cleanup.
- [ ] Reduced motion disables smoothing.
- [ ] Anchor links, keyboard and find-in-page still work.
- [ ] Inner scroll areas and modals are handled.
- [ ] Scroll-linked libraries read the Lenis position.
