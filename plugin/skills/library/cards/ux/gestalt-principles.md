---
name: gestalt-principles
title: Gestalt Principles
area: ux
tags: [ux, gestalt, proximity, similarity, grouping, perception]
detect: []
related: [visual-hierarchy, spacing-scales, grid-systems, forms, bento-grids]
---
Use proximity, similarity, common region, continuity and closure so grouping is visible without labels or borders.

## Verify
- `npx playwright test --grep grouping`: measures gaps inside versus between groups.
- `npx playwright screenshot http://localhost:3000/settings /tmp/s.png`, then blur with `convert /tmp/s.png -blur 0x6 /tmp/s-blur.png`: the groups should still show.
- `grep -rnE "<hr|border-(top|bottom): *1px" src`: separators that whitespace could replace.

## Test first
Group gap must be at least twice the item gap.
```ts
import { test, expect } from '@playwright/test';

test('between-group space is at least 2x within-group space', async ({ page }) => {
  await page.goto('/settings');
  const g = await page.$$eval('fieldset', fs => fs.map(f => {
    const r = f.getBoundingClientRect();
    const kids = [...f.querySelectorAll('label')].map(l => l.getBoundingClientRect());
    return { top: r.top, bottom: r.bottom, inner: kids.length > 1 ? kids[1].top - kids[0].bottom : 0 };
  }));
  for (let i = 1; i < g.length; i++) {
    const between = g[i].top - g[i - 1].bottom;
    expect(between).toBeGreaterThanOrEqual(2 * g[i].inner);
  }
});
```

## Do
- Proximity: related items sit 8 px apart, unrelated groups 24-32 px apart (3-4x); this is the strongest cue, so use it first.
- Similarity: same style for same function (all links one color, all primary actions one fill); a style change means a change in meaning.
- Common region: a card or tinted background groups content; use sparingly, one level of nesting.
- Alignment and continuity: keep a shared left edge so the eye follows a line down the page.
- Closure: an icon or progress ring can be incomplete and still read; use that for lightweight marks.
- Figure/ground: raise the focused layer with shadow or scrim (modal over dimmed page).
- Label next to its field (4-8 px), far from the previous field (16-24 px).

## Avoid
- Equal spacing everywhere: nothing groups.
- A border around every item plus a card plus a divider: three signals for one grouping.
- Same look for unlike things, or different looks for the same thing (two blues for links).
- Labels equidistant between two fields.

## Review
- [ ] A blurred screenshot still shows the groups.
- [ ] Between-group space is at least 2x within-group space.
- [ ] A style is used for one meaning only.
- [ ] Boxes and rules appear only where spacing alone fails.
