---
name: custom-cursors
title: Custom Cursors
area: frontend
tags: [cursor, pointer, css, hover, input, motion]
detect: []
related: [micro-interactions, gesture-input, accessibility, animation, responsive-design]
---
Restyle the cursor with CSS first; follow-cursor effects only on fine pointers, with the native cursor still usable.

## Verify
- `npx playwright test --grep cursor`: asserts the computed `cursor` on interactive elements.
- `grep -rn "cursor: *none" src`: every hit needs a visible replacement and a pointer-type guard.
- Devtools Performance panel: pointermove work under 16.7 ms a frame; no layout.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('links keep a pointer cursor and the native cursor is not hidden', async ({ page }) => {
  await page.goto('/');
  const c = await page.getByRole('link').first().evaluate(e => getComputedStyle(e).cursor);
  expect(c).toBe('pointer');
  const body = await page.evaluate(() => getComputedStyle(document.body).cursor);
  expect(body).not.toBe('none');
});
```

## Do
- CSS cursor images: `cursor: url(cursor.svg) 4 4, auto;` always with a keyword fallback; 32 by 32 px or smaller (browsers cap near 128 px).
- Standard keywords carry meaning: `pointer` for links, `grab` and `grabbing` for drag, `not-allowed` for disabled, `text` for editable.
- A follow-cursor element: `position: fixed; pointer-events: none; transform: translate3d(x, y, 0)` updated in `requestAnimationFrame` from a stored pointer position, with lerp smoothing around 0.15-0.25.
- Enable only inside `@media (hover: hover) and (pointer: fine)`; touch devices get nothing.
- Under `prefers-reduced-motion: reduce`, drop smoothing so the shape tracks exactly.
- Keep a visible focus ring for keyboard users; a cursor follower never replaces it.
- Make the follower at least 3:1 against backgrounds, or use `mix-blend-mode: difference`.

## Avoid
- `cursor: none` on the page: users lose track of the pointer when the script lags or fails.
- Cursor lag above one frame at normal speed; smoothing should feel responsive.
- Hover-revealed content that only the custom cursor triggers.
- Large cursor images; they get clipped near window edges.
- Writing `left` and `top` per move.

## Review
- [ ] The default cursor returns if scripts fail.
- [ ] Touch and coarse pointers are excluded.
- [ ] Standard semantic cursors still appear on links, text and disabled controls.
- [ ] The follower is invisible to assistive tech and does not intercept clicks.
