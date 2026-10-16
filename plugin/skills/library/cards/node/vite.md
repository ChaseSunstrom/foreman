---
name: vite
title: Vite
area: node
tags: [vite, bundler, dev-server, frontend, esm, build]
detect: [dep:vite, dep:@vitejs/plugin-*, file:vite.config.ts, file:vite.config.js, file:vite.config.mjs]
related: [vitest, tsconfig, eslint, rollup, esbuild]
---
Vite projects: dev server, production build through Rollup, env handling, plugins and `vite.config`.

## Verify
- `npx vite build`: the production bundle builds.
- `npx vite preview`: serves the built output, which catches dev-only behavior.
- `npx tsc --noEmit`: types, since Vite transpiles without checking.
- `npx vitest run`: tests share the Vite config and transforms.

## Test first
Vitest reads `vite.config`, so aliases and plugins behave as in the app. Put a config assertion or unit test beside the code.
```ts
import { describe, it, expect } from 'vitest';
import { apiUrl } from '../src/config';

describe('apiUrl', () => {
  it('fails loudly when VITE_API_URL is missing', () => {
    expect(() => apiUrl({})).toThrow(/VITE_API_URL/);
  });
});
```
Pass `import.meta.env` into the function so it is testable.

## Do
- Export config with `defineConfig`; use the function form `({ mode }) => ({...})` when config depends on mode.
- Expose client env only with the `VITE_` prefix and read it through `import.meta.env`.
- Set `base` for subpath deploys and `build.target` to the browsers you support.
- Alias with `resolve.alias` and mirror it in `tsconfig` `paths` (or use `vite-tsconfig-paths`).
- Proxy API calls in dev via `server.proxy` instead of enabling CORS broadly.
- Split vendor chunks only after measuring (`build.rollupOptions.output.manualChunks`).
- Import assets with `new URL('./a.png', import.meta.url)` or as modules; use `public/` for fixed URLs.
- Run `vite build --mode staging` with a matching `.env.staging`.

## Avoid
- `process.env.X` in client code: undefined in the browser. Use `import.meta.env.VITE_X`.
- Putting secrets in `VITE_*` variables: they ship in the bundle. Keep secrets server-side.
- CommonJS-only dependencies with `require` in source: breaks in dev ESM. Use `import`, or add the package to `optimizeDeps.include`.
- A stale `node_modules/.vite` cache after linking or changing deps: dev behaves oddly. Run `vite --force`.
- Assuming dev equals prod: dev is unbundled. Always run `build` and `preview` before shipping.
- Relative asset URLs with a wrong `base`: broken paths on subpath hosting. Set `base`.
- Hard-coding `localhost` in `server.host` or `proxy` and exposing the dev server publicly: set `server.host` deliberately.

## Review
- [ ] Only public values use `VITE_`.
- [ ] `build` and `preview` were run, not just dev.
- [ ] Aliases are mirrored in the TypeScript config.
- [ ] `base` and `build.target` match the deployment.
- [ ] Type-check is a separate CI step.
