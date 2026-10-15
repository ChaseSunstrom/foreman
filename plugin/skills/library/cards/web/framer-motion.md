---
name: framer-motion
title: Framer Motion
area: web
tags: [framer-motion, motion, react, animation, layout, gestures]
detect: [dep:framer-motion, dep:motion]
related: [react, tailwind, testing-library]
---
Framer Motion (now also published as motion): declarative React animation with variants, layout animations, AnimatePresence and gestures.

## Verify
- `npx tsc --noEmit`: motion props and variants type-check.
- `npx eslint .`: lint.
- `npx vitest run`: behavior tests (animations are not asserted frame by frame).
- `npx playwright test`: real-browser check of enter, exit and layout transitions.

## Test first
Assert on state and presence, and disable animation in tests rather than timing frames.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Toast } from "./Toast";

test("toast leaves the DOM after dismiss", async () => {
  render(<Toast message="Saved" />);
  await userEvent.click(screen.getByRole("button", { name: /dismiss/i }));
  await vi.waitFor(() => expect(screen.queryByText("Saved")).toBeNull());
});
```

## Do
- Import from the package the project uses (`framer-motion` or `motion/react`); do not mix both.
- Use `motion.div` with `initial`, `animate`, `exit` and `transition`; define reusable `variants` and propagate them to children.
- Wrap conditional elements in `<AnimatePresence>` and give each a stable `key`; use `mode="wait"` when swapping.
- Animate `transform` and `opacity` (`x`, `y`, `scale`, `opacity`) for smooth, GPU-friendly motion.
- Use the `layout` prop (and `layoutId` for shared elements) instead of animating width and height by hand.
- Use `useReducedMotion` or `MotionConfig reducedMotion="user"` to respect the OS setting.
- Use motion values (`useMotionValue`, `useTransform`) for scroll or drag-linked effects without re-rendering React.

## Avoid
- A conditional `motion` element without `AnimatePresence`: the `exit` animation never plays. Wrap it.
- Missing or index-based `key` on presence children: wrong element exits. Use stable ids.
- Animating `width`, `height`, `top`, `left`: layout thrash. Use transforms or `layout`.
- Storing animated values in React state and updating per frame: re-renders. Use motion values.
- Ignoring `prefers-reduced-motion`: accessibility failure. Configure reduced motion.
- `AnimatePresence` placed inside the conditional: it unmounts with the child. Keep it outside.
- Mixing the CSS `transition` property with motion-controlled properties: they fight. Choose one.

## Review
- [ ] Exits animate (presence and keys are right).
- [ ] Only transform and opacity animate on hot paths.
- [ ] Reduced motion is respected.
- [ ] One import source for the library across the repo.
- [ ] Tests do not depend on animation timing.
