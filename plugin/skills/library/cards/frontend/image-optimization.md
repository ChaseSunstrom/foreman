---
name: image-optimization
title: Image Optimization
area: frontend
tags: [images, avif, webp, srcset, lazy-loading, sharp]
detect: [dep:sharp, dep:imagemin, dep:vite-imagetools, dep:@squoosh/lib, dep:unpic, dep:astro, dep:next]
related: [web-performance, responsive-design, seo, svg-canvas]
---
Ship the smallest correct image: modern formats, responsive sizes, explicit dimensions and the right loading priority.

## Verify
- `cwebp -q 80 in.png -o out.webp`: converts to WebP; compare bytes against the original.
- `avifenc --min 20 --max 40 in.png out.avif`: AVIF encode (from libavif).
- `npx lighthouse http://localhost:4173 --only-categories=performance --quiet`: flags "properly size images", "modern formats" and CLS.
- `curl -sI https://example.com/hero.avif`: `Content-Type`, `Cache-Control` and size on the wire.

## Test first
Check the markup contract: dimensions, sizes and priority.
```ts
import { test, expect } from '@playwright/test';

test('hero is prioritized, others lazy, all sized', async ({ page }) => {
  await page.goto('/');
  const hero = page.locator('img.hero');
  await expect(hero).toHaveAttribute('fetchpriority', 'high');
  await expect(hero).not.toHaveAttribute('loading', 'lazy');
  for (const img of await page.locator('img').all()) {
    await expect(img).toHaveAttribute('width', /\d+/);
    await expect(img).toHaveAttribute('height', /\d+/);
  }
});
```

## Do
- Generate widths (for example 480, 800, 1200, 1600) at build time; emit AVIF then WebP then JPEG inside `<picture>`.
- `<img srcset="… 480w, … 800w" sizes="(min-width: 60rem) 50vw, 100vw">`: `sizes` must reflect the real rendered width.
- Always set `width` and `height` (or CSS `aspect-ratio`) to prevent layout shift.
- Hero or LCP image: `fetchpriority="high"`, no lazy, optionally preload. Others: `loading="lazy"` and `decoding="async"`.
- Quality around 60-80 for photos; use SVG for logos and icons, PNG or lossless WebP for flat UI screenshots.
- Strip metadata (EXIF, location) from user uploads; re-encode on the server.
- Serve from a CDN with long immutable caching on fingerprinted names, or an image service that does format negotiation by `Accept`.
- Provide meaningful `alt` text, empty for decoration.
- Use the framework image component (`next/image`, `astro:assets`) when present, and set its `sizes`.

## Avoid
- Serving a 4000px original to a 400px slot: wasted bytes. Resize per breakpoint.
- `loading="lazy"` on the LCP image: delays the largest paint. Use priority instead.
- Missing `sizes` with `srcset`: browser assumes 100vw and over-downloads. Describe layout.
- Animated GIFs: huge. Use `<video autoplay muted loop playsinline>` with MP4 or WebM.
- Upscaling or double-compressing JPEGs: artifacts. Encode once from the source master.
- Background images in CSS for content images: no lazy loading, alt text or `srcset`. Use `<img>` (or `image-set()` only for decoration).
- Skipping a fallback format: older clients show nothing. Keep the `<img>` JPEG or PNG.

## Review
- [ ] Every image has dimensions, `alt`, and appropriate lazy or priority attributes.
- [ ] `srcset` and `sizes` match the layout; no oversized downloads at mobile width.
- [ ] Modern formats with fallback; photos not shipped as PNG.
- [ ] Uploaded images are re-encoded with metadata stripped.
- [ ] Cache headers are long and immutable for hashed files.
