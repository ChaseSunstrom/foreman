---
name: scroll-snap-carousels
title: Scroll-Snap Carousels
area: frontend
tags: [css, scroll-snap, carousel, overflow, touch, keyboard]
detect: []
related: [css-layout, keyboard-navigation, gesture-input, accessibility, layout-shift]
---
Carousels built on overflow scrolling and scroll-snap: no JavaScript for the core, with keyboard, labels and no autoplay.

## Verify
- `npx playwright test --grep carousel`: scrolls the track, asserts the snapped slide, and drives it with the keyboard.
- `npx axe-cli http://localhost:3000`: checks region labels and focusable scroll containers.
- `grep -rn "scroll-snap-type" src`: confirm each container pairs with `scroll-snap-align` on its children.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('next button moves to the following slide', async ({ page }) => {
  await page.goto('/');
  const track = page.locator('.track');
  const first = await track.evaluate(e => e.scrollLeft);
  await page.getByRole('button', { name: 'Next slide' }).click();
  await expect.poll(() => track.evaluate(e => e.scrollLeft)).toBeGreaterThan(first);
});
```

## Do
- Core CSS: `.track { display: grid; grid-auto-flow: column; grid-auto-columns: 80%; overflow-x: auto; scroll-snap-type: x mandatory; overscroll-behavior-x: contain; scrollbar-width: none; } .slide { scroll-snap-align: center; }`.
- Prefer `proximity` over `mandatory` when slides can be taller than the viewport, so users are not trapped.
- Add `scroll-padding-inline` for peeking neighbors, and `scroll-snap-stop: always` to stop swipes skipping slides.
- Buttons call `track.scrollBy({ left: slideWidth, behavior: 'smooth' })`; set behavior `auto` under `prefers-reduced-motion`.
- Make the container reachable: `tabindex="0"`, `role="region"`, `aria-label="Featured"`; arrow keys then scroll natively.
- Native pagination: `::scroll-button()` and `::scroll-marker` (Chromium 135+) give buttons and dots in CSS; feature-detect and keep the manual buttons.
- Reserve slide height with `aspect-ratio` to avoid layout shift; lazy-load images beyond the second slide.
- Mark off-screen slides' focusable content: use IntersectionObserver to set `inert` if tab order matters.

## Avoid
- Autoplay that moves on its own: fails WCAG 2.2.2 without a pause control, and fights user scrolling.
- Hiding the scrollbar with no other affordance of more content.
- `scroll-snap-type` on the page-level scroller of long content: janky and traps.
- Dots-only navigation of 10 or more slides.
- JS carousels libraries when scroll-snap suffices; they cost 20-60 KB.

## Review
- [ ] Touch, trackpad, keyboard and buttons all move between slides.
- [ ] No autoplay; reduced-motion users get non-smooth scrolling.
- [ ] The track has a name and a focus indicator.
- [ ] Slides reserve space; images beyond the fold are lazy.
