---
name: embla-carousel
title: Embla Carousel
area: web
tags: [embla, carousel, slider, touch, react]
detect: [dep:embla-carousel, dep:embla-carousel-react, dep:embla-carousel-autoplay]
related: [react, accessibility, css-layout, web-performance]
---
Embla Carousel: dependency-free, plugin-based carousel; you supply the markup and CSS, it supplies scroll physics.

## Verify
- `npx tsc --noEmit`: API, options and plugin types.
- `npx eslint .`: lint, including effect cleanup.
- `npx vitest run`: logic tests with a mocked API.
- `npx playwright test --grep carousel`: swipe, buttons and keyboard in a real browser.

## Test first
Test your wiring against a fake API, since jsdom has no layout.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";

const api = { scrollNext: vi.fn(), scrollPrev: vi.fn(), canScrollNext: () => true, canScrollPrev: () => false, on: vi.fn(), off: vi.fn() };
vi.mock("embla-carousel-react", () => ({ default: () => [vi.fn(), api] }));

import { Gallery } from "./Gallery";

test("next button advances the carousel", async () => {
  render(<Gallery />);
  await userEvent.click(screen.getByRole("button", { name: /next/i }));
  expect(api.scrollNext).toHaveBeenCalled();
});
```

## Do
- Use the structure `viewport (overflow:hidden) > container (display:flex) > slides (flex: 0 0 100%)` and `useEmblaCarousel(options, [plugins])`.
- Subscribe with `api.on("select", fn)` and unsubscribe in the effect cleanup; read `selectedScrollSnap()` for the index.
- Memoize the options object and plugins array so the carousel is not re-initialized each render.
- Give slides `role="group"`, `aria-roledescription="slide"`, `aria-label="2 of 6"`; the root `role="region"` with `aria-roledescription="carousel"`.
- Provide visible prev and next buttons, disabled by `canScrollPrev` and `canScrollNext`, and keep slides keyboard-reachable.
- Autoplay: use the plugin with `stopOnInteraction: true`, and disable it for reduced motion.
- Lazy-load slide images beyond the first with `loading="lazy"` and explicit dimensions.

## Avoid
- Options created inline each render: re-init loops and lost position.
- Autoplay with no pause control: fails WCAG 2.2.2.
- Hiding off-screen slides from focus order without managing it.
- Percent heights and images without sizes: layout shift on load.
- Forgetting `api.reInit()` after the slide count changes (it auto-handles resize, not content swaps without a key).

## Review
- [ ] Options and plugins are stable references.
- [ ] Event listeners are removed on cleanup.
- [ ] Controls and aria roles are present.
- [ ] Autoplay can be paused and respects reduced motion.
- [ ] Images have dimensions and lazy loading.
