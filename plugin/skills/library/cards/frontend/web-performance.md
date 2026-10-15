---
name: web-performance
title: Web Performance
area: frontend
tags: [performance, core-web-vitals, lcp, inp, cls, bundle]
detect: [dep:lighthouse, dep:@lhci/cli, dep:web-vitals, dep:webpack-bundle-analyzer, dep:rollup-plugin-visualizer, dep:vite-bundle-visualizer]
related: [image-optimization, responsive-design, pwa, seo, animation]
---
Front-end speed measured by Core Web Vitals: LCP, INP and CLS, with budgets enforced in CI.

## Verify
- `npx lhci autorun`: Lighthouse CI run against budgets in `lighthouserc` assertions.
- `npx lighthouse http://localhost:4173 --only-categories=performance --output=json --output-path=./lh.json`: lab metrics for a production build.
- `npx vite build`: build output lists chunk sizes; check against the budget.
- `curl -sI -H "Accept-Encoding: br" https://example.com/app.js`: compression and cache headers actually served.

## Test first
Make the budget a failing check before optimizing.
```json
{
  "ci": {
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", {"maxNumericValue": 2500}],
        "cumulative-layout-shift": ["error", {"maxNumericValue": 0.1}],
        "total-byte-weight": ["error", {"maxNumericValue": 500000}]
      }
    }
  }
}
```
Save as `lighthouserc.json`, run `npx lhci autorun` on the preview build, watch it fail, then fix.

## Do
- Measure the production build under throttling; profile before changing.
- LCP: preload the hero image (`<link rel="preload" as="image" fetchpriority="high">`), inline critical CSS, avoid client-only rendering of above-the-fold content.
- CLS: set `width` and `height` or `aspect-ratio` on media; reserve space for ads and embeds; use `font-display: swap` with a metric-matched fallback.
- INP: break long tasks (`scheduler.yield()` or chunked work), debounce inputs, move heavy work to a Web Worker.
- Split by route with dynamic `import()`; analyze the bundle and replace heavy libraries.
- Cache fingerprinted assets with `Cache-Control: public, max-age=31536000, immutable`; HTML with revalidation.
- `loading="lazy"` for below-the-fold images, never for the LCP image.
- Serve Brotli, HTTP/2 or 3, and `preconnect` only to origins used at load.
- Collect real-user data with `web-vitals`; lab numbers differ.

## Avoid
- Lazy-loading the hero image: delays LCP. Use `fetchpriority="high"` instead.
- Render-blocking third-party scripts in `<head>`: add `defer` or `async`, or load after interaction.
- Importing a whole library (`import _ from "lodash"`): use per-function imports or native methods.
- Animating `width`, `top` or `left`: triggers layout. Animate `transform` and `opacity`.
- Optimizing from a dev-server Lighthouse run: unminified, uncompressed. Test the built preview.
- Preloading everything: contention slows the critical resource. Preload one or two.
- Layout reads and writes interleaved in a loop (forced reflow): batch reads first.

## Review
- [ ] Budgets for LCP, CLS, INP and total JS are asserted in CI.
- [ ] LCP element identified and prioritized; no layout shift from late media or fonts.
- [ ] No new heavy dependency without a bundle size comparison.
- [ ] Caching headers correct for hashed assets and HTML.
- [ ] Real-user metrics reported, not only lab runs.
