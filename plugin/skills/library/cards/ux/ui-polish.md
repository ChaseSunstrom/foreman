---
name: ui-polish
title: UI Polish
area: ux
tags: [ux, polish, details, states, shadows, radius, motion]
detect: []
related: [visual-hierarchy, spacing-scales, animation, design-systems, dark-mode, skeleton-loading]
---
The last 10 percent: consistent radius, layered shadows, every state designed, crisp text, smooth 150-250 ms motion.

## Verify
- `grep -rhoE "border-radius: *[^;]+" src | sort | uniq -c | sort -rn`: more than 3 radii is drift.
- `grep -rhoE "box-shadow: *[^;]+" src | sort -u | wc -l`: shadows should come from 3-4 tokens.
- `npx playwright test --grep states`: hover, focus, active, disabled and empty states render.
- `grep -rn "outline: *none\|outline: *0" src`: removed focus rings.

## Test first
Every interactive element must show a visible focus style.
```ts
import { test, expect } from '@playwright/test';

test('focus is visible on every control', async ({ page }) => {
  await page.goto('/');
  const controls = await page.locator('a[href], button, input, select, textarea').all();
  for (const c of controls.slice(0, 40)) {
    if (!(await c.isVisible())) continue;
    await c.focus();
    const s = await c.evaluate(e => { const x = getComputedStyle(e); return [x.outlineStyle, x.outlineWidth, x.boxShadow]; });
    expect(s[0] !== 'none' || s[2] !== 'none').toBe(true);
  }
});
```

## Do
- Pick radius steps (4, 8, 16, full) and use nested radius = outer radius minus padding.
- Layer shadows: a tight one plus a soft one, low opacity (`0 1px 2px rgb(0 0 0 / .06), 0 8px 24px rgb(0 0 0 / .08)`); in dark mode use lighter surfaces, not darker shadows.
- Design all states: default, hover, focus-visible, active, disabled, loading, error, empty.
- Transitions 120-250 ms with ease-out on enter; animate color, opacity and transform only.
- Use `-webkit-font-smoothing: antialiased` sparingly, `tabular-nums` for numbers in tables, and `text-wrap: balance` on headings.
- Align optically: icons next to text align to the cap height; center play triangles by eye.
- Keep 1px borders at 8-12 percent ink; use `border-color` tokens in both themes.
- Set `color-scheme`, `accent-color` and `::selection` colors; style scrollbars lightly with `scrollbar-color`.
- Make hit areas larger than visuals (44 px) with padding or pseudo-elements.

## Avoid
- `outline: none` with no replacement.
- Different radii or shadow recipes per component.
- Hover-only affordances; layout shift on hover (bold text changes width).
- Polish before structure: fix hierarchy and spacing first.

## Review
- [ ] Radius, shadow and border values come from a short token list.
- [ ] Every interactive element has all its states and a visible focus ring.
- [ ] Motion is brief, compositor-only and respects reduced motion.
- [ ] Numbers use tabular figures where they align.
