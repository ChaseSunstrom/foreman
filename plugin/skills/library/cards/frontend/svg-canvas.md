---
name: svg-canvas
title: SVG and Canvas
area: frontend
tags: [svg, canvas, graphics, svgo, webgl, charts]
detect: [ext:.svg, dep:svgo, dep:@svgr/webpack, dep:vite-plugin-svgr, dep:d3, dep:konva, dep:pixi.js, dep:three]
related: [animation, accessibility, web-performance, image-optimization]
---
Choose SVG for scalable, accessible, styleable shapes and Canvas for many pixels or per-frame drawing; optimize and size both.

## Verify
- `npx svgo -f assets/icons -o dist/icons`: minify a folder of SVGs.
- `npx svgo --pretty input.svg -o out.svg`: single file, readable output to diff.
- `npx playwright test --grep graphics`: screenshot comparison of the rendered result.
- `xmllint --noout file.svg`: the file is well-formed XML.

## Test first
Test data to shape mapping as pure code; snapshot the rendered output.
```ts
import { expect, test } from 'vitest';
import { barPath } from './chart';

test('bar scales to the domain and stays inside the viewBox', () => {
  const r = barPath({ value: 50, max: 100, width: 200, height: 100 });
  expect(r).toEqual({ x: 0, y: 50, width: 200, height: 50 });
});
```
Keep the scale and layout math outside the drawing code so it is testable without a DOM.

## Do
- Set `viewBox` and omit fixed `width` and `height` (or set them via CSS) so the SVG scales.
- Style with `currentColor` and CSS custom properties so themes and dark mode work for inline SVG.
- Give meaningful graphics `role="img"` plus `<title>` and `aria-labelledby`; mark decoration `aria-hidden="true"`.
- Inline small icons or use a `<symbol>` sprite with `<use href="#id">`; use `<img>` for large static art.
- Run SVGO in the build but keep `viewBox` (the default `removeViewBox` has been off in recent presets; check your config).
- Canvas: size the backing store for the pixel ratio (`canvas.width = cssWidth * devicePixelRatio`, then `ctx.scale`).
- Drive canvas animation with `requestAnimationFrame`; clear and redraw only dirty regions; use `OffscreenCanvas` in a worker for heavy work.
- Above a few thousand elements, switch from SVG to canvas or WebGL.

## Avoid
- Blurry canvas on retina screens: forgetting the devicePixelRatio scale. Scale backing store and context.
- Missing `viewBox`: SVG will not scale with its container. Add it.
- Inline SVG with duplicated `id`s (gradients, clip paths): collisions across icons. Prefix ids or let SVGO prefix them.
- Using user-supplied SVG with `innerHTML` or `<img>` treated as safe: scripts and external refs. Sanitize with DOMPurify (SVG profile) or serve as `<img>` only.
- Canvas content with no text alternative: invisible to assistive tech. Provide a table or `aria-label` description.
- Thousands of animated SVG nodes: DOM cost. Use canvas.
- Creating new objects, gradients or paths in every frame: GC pauses. Reuse them.

## Review
- [ ] SVGs have `viewBox`, are optimized, and use `currentColor` where themed.
- [ ] Informative graphics are named; decorative ones hidden from assistive tech.
- [ ] Canvas handles resize and devicePixelRatio, and cancels its animation frame on unmount.
- [ ] Untrusted SVG is sanitized or isolated.
- [ ] Element count suits the chosen technology.
