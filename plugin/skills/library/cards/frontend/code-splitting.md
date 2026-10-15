---
name: code-splitting
title: Code splitting
area: frontend
tags: [performance, bundle, dynamic-import, lazy, routes]
detect: [dep:vite-bundle-visualizer]
related: [lazy-loading, web-performance, error-boundaries, hydration]
---
Ship less JS up front: split by route and heavy feature with dynamic `import()`, and handle load failure.

## Verify
- `npx vite build`: prints per-chunk sizes (Vite projects).
- `npx tsc --noEmit`: dynamic import types resolve.
- `npx playwright test`: asserts a chunk is requested only after navigation.

## Test first
The editor chunk must not load on the home page.
```ts
import { test, expect } from '@playwright/test';

test('editor chunk loads on demand', async ({ page }) => {
  const js: string[] = [];
  page.on('request', r => r.url().endsWith('.js') && js.push(r.url()));
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  expect(js.some(u => /editor/i.test(u))).toBe(false);
  await page.getByRole('link', { name: 'Editor' }).click();
  await expect.poll(() => js.some(u => /editor/i.test(u))).toBe(true);
});
```

## Do
- Split at routes first (`React.lazy(() => import('./Settings'))`, framework route-level splitting), then at heavy leaves (charts, editors, PDF, maps).
- Wrap lazy components in `<Suspense fallback={...}>` with a fallback sized like the content.
- Wrap them in an error boundary that offers retry: chunk fetches fail on flaky networks and after deploys.
- Preload on intent: `onMouseEnter` or `onFocus` calls the same `import()` to warm the chunk.
- Import named exports narrowly (`import { debounce } from 'lodash-es'`), avoid barrel files in hot paths.
- Keep a bundle budget in CI and inspect with a visualizer after adding a dependency.
- Load third-party scripts with `async` or `defer`, after interaction when possible.

## Avoid
- Splitting everything: dozens of tiny chunks add waterfalls. Split at route and heavy-feature level.
- A `Suspense` fallback of `null` or a spinner of a different size: layout shift. Match dimensions.
- No retry for a failed dynamic import after a deploy (stale hashed filename): show reload and retry, or reload once on `ChunkLoadError`.
- Lazy-loading above-the-fold components: slower first paint. Keep them in the main chunk.
- `import()` with a fully dynamic template string: the bundler cannot resolve it. Use a static map of loaders.
- Importing a whole icon or utility library for one function: tree-shaking often fails. Import the single path.

## Review
- [ ] Initial JS is route-scoped; heavy features are lazy.
- [ ] Every lazy boundary has a sized fallback and an error boundary with retry.
- [ ] Hover or focus warm-up exists for likely next routes.
- [ ] Bundle size is measured before and after the change.
- [ ] No dynamic imports with unresolvable paths.
