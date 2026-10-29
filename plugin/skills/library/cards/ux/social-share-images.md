---
name: social-share-images
title: Social Share Images
area: ux
tags: [ux, open-graph, og-image, twitter-card, social, seo]
detect: [dep:@vercel/og, dep:satori]
related: [seo, image-optimization, brand-identity, landing-pages, app-icons-and-favicons]
---
One 1200x630 Open Graph image per page, generated from a template, with title text in the centered safe area.

## Verify
- `curl -s http://localhost:3000/ | grep -oE '<meta (property|name)="(og|twitter):[^>]+>'`: og:title, og:description, og:image, og:url, twitter:card.
- `curl -s -o /tmp/og.png http://localhost:3000/og.png && identify /tmp/og.png`: 1200x630, under 300 KB.
- `curl -sI http://localhost:3000/og.png | grep -i content-type`: image/png or image/jpeg.
- Preview with the platform debuggers (LinkedIn Post Inspector, Facebook Sharing Debugger) after deploy.

## Test first
```ts
import { test, expect } from '@playwright/test';

test('page declares a valid share image', async ({ page, request }) => {
  await page.goto('/blog/hello');
  const url = await page.locator('meta[property="og:image"]').getAttribute('content');
  expect(url).toMatch(/^https:\/\//);
  await expect(page.locator('meta[name="twitter:card"]')).toHaveAttribute('content', 'summary_large_image');
  const res = await request.get(url!);
  expect(res.ok()).toBe(true);
  expect(res.headers()['content-type']).toMatch(/image\/(png|jpeg)/);
  expect((await res.body()).length).toBeLessThan(300_000);
});
```

## Do
- Size 1200x630 (1.91:1), PNG or JPEG, under 300 KB (some platforms reject over 5 MB; keep it small anyway); do not use SVG or WebP, which many scrapers ignore.
- Keep text and logo inside the central 1000x500 area; crops differ per platform and square previews cut the sides.
- Title in 60-70 px bold, at most 2-3 lines, 4.5:1 contrast; logo at 80-120 px; no small text, since it appears at about 500 px wide.
- Generate per page at build or edge time from a template (`satori`, `@vercel/og`, a headless-browser screenshot) with the page title and brand tokens.
- Use absolute `https` URLs for `og:image`; add `og:image:width`, `og:image:height` and `og:image:alt`.
- Set `twitter:card` to `summary_large_image`; fall back to a default brand image if a page has none.
- Cache images with a stable URL, and add a version query when the template changes, since scrapers cache hard.

## Avoid
- Relative URLs, images behind auth, or images blocked in `robots.txt`.
- Dense paragraphs, tiny logos, or the page screenshot as the image.
- One image site-wide for every page.
- Forgetting `og:url` and `og:title`.

## Review
- [ ] Every indexable page has og:title, description, image (1200x630), url, and twitter:card.
- [ ] Text survives a 1:1 center crop and a 500 px preview.
- [ ] Image URL is absolute, public, under 300 KB, with alt text.
- [ ] Preview checked in at least two debugger tools after deploy.
