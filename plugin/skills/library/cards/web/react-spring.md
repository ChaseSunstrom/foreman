---
name: react-spring
title: React Spring
area: web
tags: [react-spring, react, animation, physics, springs]
detect: [dep:@react-spring/web, dep:@react-spring/three, dep:react-spring]
related: [react, animation, accessibility, framer-motion]
---
React Spring: physics-based animation for React; springs animate values outside React state so components do not re-render per frame.

## Verify
- `npx tsc --noEmit`: spring config and `animated` component types.
- `npx eslint .`: lint, including hook rules.
- `npx vitest run`: behavior tests with animation skipped.
- `npx playwright test`: enter, leave and gesture flows in a real browser.

## Test first
Turn animation off globally so the end state is immediate.
```tsx
import { Globals } from "@react-spring/web";
import { render, screen } from "@testing-library/react";
import { Drawer } from "./Drawer";

beforeAll(() => Globals.assign({ skipAnimation: true }));

test("drawer opens to its full width", () => {
  render(<Drawer open />);
  expect(screen.getByTestId("drawer")).toHaveStyle({ transform: "translateX(0px)" });
});
```

## Do
- Import from `@react-spring/web` (or `/three`, `/native`) and use `animated.div`, never a plain element, for animated styles.
- Use `useSpring`, `useSprings` and `useTrail` for values; `useTransition` for mount and unmount; pass stable `keys`.
- Pass `config` presets (`config.gentle`) or `{ tension, friction, mass }`; use `clamp: true` to stop overshoot.
- Animate `transform` and `opacity`; interpolate with `.to()` for derived values.
- Use the imperative API (`api.start`, `api.stop`) from gestures (`@use-gesture/react`) to avoid re-renders.
- Respect reduced motion: `Globals.assign({ skipAnimation: prefersReduced })` or set `immediate: true`.
- Treat springs as interruptible: start a new target, do not queue.

## Avoid
- Plain elements with animated values: they render the object, not the number. Use `animated.*`.
- Putting spring values into React state: it defeats the point and re-renders per frame.
- `useTransition` without stable keys: the wrong item leaves.
- Duration-style thinking: springs have no fixed time, so tests must not wait on one.
- Mixing CSS transitions on the same property.

## Review
- [ ] All animated styles go through `animated` components.
- [ ] Transitions have stable keys.
- [ ] Reduced motion makes changes immediate.
- [ ] Tests skip animation instead of sleeping.
- [ ] Gesture-driven updates use the imperative API.
