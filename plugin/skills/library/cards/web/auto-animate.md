---
name: auto-animate
title: AutoAnimate
area: web
tags: [auto-animate, formkit, animation, lists, transitions]
detect: [dep:@formkit/auto-animate]
related: [animation, react, vue, accessibility]
---
AutoAnimate: one call adds enter, exit and move transitions to a parent's children, with zero config.

## Verify
- `npx tsc --noEmit`: the ref and options types.
- `npx eslint .`: lint.
- `npx vitest run`: behavior tests with animation disabled.
- `npx playwright test --grep list`: add, remove and reorder animate and settle in a real browser.

## Test first
Assert DOM state, and turn the animation off through the controller so the test does not wait on it.
```tsx
import autoAnimate from "@formkit/auto-animate";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { TodoList } from "./TodoList";

test("removing an item removes it from the list with animation disabled", async () => {
  render(<TodoList initial={["a", "b"]} />);
  const list = screen.getByRole("list");
  autoAnimate(list).disable(); // controller: enable() / disable()
  await userEvent.click(screen.getAllByRole("button", { name: /remove/i })[0]);
  expect(screen.getAllByRole("listitem")).toHaveLength(1);
});
```

## Do
- React: `const [parent] = useAutoAnimate()` and attach `ref={parent}` to the container; Vue: `v-auto-animate`; plain: `autoAnimate(el)`.
- Give list children stable `key`s so moves are detected as moves, not remounts.
- Pass options as needed: `{ duration: 250, easing: "ease-out" }`, or a custom plugin function.
- Toggle with the returned controller: `[parent, enable] = useAutoAnimate(); enable(false)`.
- Honor reduced motion; the library disables itself under `prefers-reduced-motion: reduce`, so verify that stays true if you pass a custom plugin.
- Apply it to the stable parent that persists, and let children come and go.
- Keep animated children simple (no `position: fixed` or heavy layout).

## Avoid
- Attaching to a parent that itself mounts and unmounts: nothing animates.
- Index keys on reorderable lists.
- Using it for choreographed sequences: use GSAP or Motion.
- Combining with other libraries animating the same children.
- Waiting on animation in tests with fixed sleeps.

## Review
- [ ] Parent is persistent and children have stable keys.
- [ ] Reduced motion is still honored.
- [ ] Tests wait on DOM state.
- [ ] No second animation system touches the same nodes.
- [ ] Options live in a stable reference.
