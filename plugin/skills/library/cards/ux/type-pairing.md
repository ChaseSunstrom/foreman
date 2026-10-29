---
name: type-pairing
title: Typeface Pairing
area: ux
tags: [ux, typography, fonts, pairing, web-fonts]
detect: []
related: [typography, type-scales, brand-identity, web-performance, layout-shift]
---
Two families at most, contrasting in structure but sharing proportions, loaded fast with no layout jump.

## Verify
- `grep -rhoE "font-family: *[^;]+" src | sort -u`: counts distinct stacks; more than 3 is a smell.
- `npx playwright test --grep fonts`: checks the loaded font list.
- `npx lighthouse http://localhost:3000 --only-categories=performance`: flags font display and preload issues.
- `ls -la public/fonts/*.woff2`: each file under about 50 KB.

## Test first
Assert at most two families are in use on a page.
```ts
import { test, expect } from '@playwright/test';

test('page uses at most two font families', async ({ page }) => {
  await page.goto('/');
  const fams = await page.evaluate(() => {
    const s = new Set<string>();
    document.querySelectorAll('body *').forEach(e =>
      s.add(getComputedStyle(e).fontFamily.split(',')[0].trim()));
    return [...s].filter(f => !/mono|ui-monospace/i.test(f));
  });
  expect(fams.length).toBeLessThanOrEqual(2);
});
```

## Do
- Pair by contrast: a serif heading with a sans body, or one superfamily using weights (the safest option).
- Match x-height and width across the pair; a wide display face over a narrow body face clashes.
- Add a third family only for code (monospace).
- Self-host variable fonts as `woff2` with `font-display: swap` and `<link rel="preload" as="font" crossorigin>` for the one or two above-the-fold files.
- Tune the fallback with `size-adjust`, `ascent-override` and `descent-override` so swap causes no layout shift.
- Subset to the needed scripts with `unicode-range` and keep 2-3 weights (400, 600, 700).
- Use a system stack as a fallback: `system-ui, -apple-system, "Segoe UI", sans-serif`.

## Avoid
- Two similar-but-different sans faces: reads as an error, not a choice.
- Many weights and italics loaded "just in case".
- Third-party font CDNs without need: privacy, an extra connection and a render block.
- Display faces for body text under 18px.

## Review
- [ ] No more than two families, plus optional monospace.
- [ ] Fonts are self-hosted woff2, preloaded when above the fold, with a metric-adjusted fallback.
- [ ] Switching from fallback to web font moves nothing (layout shift 0 for text).
- [ ] The pairing is recorded in the tokens or brand notes.
