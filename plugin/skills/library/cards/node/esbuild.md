---
name: esbuild
title: esbuild
area: node
tags: [esbuild, bundler, transpiler, build, typescript, fast]
detect: [dep:esbuild, file:esbuild.config.js, file:esbuild.config.mjs]
related: [tsconfig, vite, rollup, node]
---
esbuild: fast bundling and TypeScript/JSX transpilation, with no type checking.

## Verify
- `npx esbuild src/index.ts --bundle --platform=node --outfile=dist/index.js`: the entry bundles.
- `npx tsc --noEmit`: types, since esbuild strips them and never checks.
- `node dist/index.js --help`: the built artifact starts (use any harmless flag your entry supports).
- `npx esbuild src/index.ts --bundle --metafile=meta.json --outfile=/dev/null`: writes a metafile for inspecting what got bundled.

## Test first
Build in a test and assert on the output or metafile.
```js
import { build } from 'esbuild';
import { test } from 'node:test';
import assert from 'node:assert/strict';

test('server bundle does not include dev-only code', async () => {
  const r = await build({ entryPoints: ['src/index.ts'], bundle: true, platform: 'node',
    write: false, metafile: true, logLevel: 'silent' });
  const inputs = Object.keys(r.metafile.inputs);
  assert.ok(!inputs.some((p) => p.includes('devtools')));
});
```

## Do
- Set `platform` (`node`, `browser`, `neutral`), `target` and `format` (`esm`, `cjs`, `iife`) explicitly.
- Use `--external` (or `packages: 'external'`) for server bundles so `node_modules` stays unbundled.
- Use `minify`, `sourcemap` and `metafile` in production builds.
- Run `tsc --noEmit` as a separate type-check step.
- Keep config in a script using the JS API (`build`, `context` with `watch()` and `serve()` for dev).
- Define compile-time constants with `define: { 'process.env.NODE_ENV': '"production"' }`.
- Declare `tsconfig` options esbuild respects (`paths`, `jsx`, `target`, `useDefineForClassFields`) in `tsconfig.json`.
- Add the `banner` option to supply `require` when bundling ESM output that includes CJS deps for Node.

## Avoid
- Assuming it type-checks: type errors ship. Add `tsc --noEmit`.
- `emitDecoratorMetadata` expectations (NestJS, TypeORM): unsupported. Use a plugin or a tsc/swc build for those apps.
- Bundling native addons (`.node` files) or packages that read files relative to themselves: breaks at runtime. Mark them external.
- Using the old `esbuild.serve()` signature or `incremental: true`: removed. Use `context()` then `ctx.serve()` and `ctx.rebuild()`.
- Output `cjs` for code using top-level `await`: unsupported. Use `esm`.
- Forgetting `bundle: true`: imports stay as-is and nothing is bundled.
- Forgetting `define` for `process.env.NODE_ENV` in browser builds: libraries ship dev branches.

## Review
- [ ] A type-check step exists apart from esbuild.
- [ ] `platform`, `target` and `format` are explicit.
- [ ] Native modules and node_modules are external for server builds.
- [ ] Decorator-metadata frameworks are not built with esbuild alone.
- [ ] Production build has minify and sourcemap settings chosen.
