---
name: webpack
title: webpack
area: node
tags: [webpack, bundler, loaders, build, code-splitting, javascript]
detect: [dep:webpack, dep:webpack-cli, file:webpack.config.js, file:webpack.config.ts]
related: [esbuild, rollup, vite, eslint, tsconfig]
---
webpack builds: config modes, loaders and plugins, code splitting, caching and bundle size checks.

## Verify
- `npx webpack --mode production`: the production build completes with no errors.
- `npx webpack --mode production --json > stats.json`: emits stats for size and duplicate analysis.
- `npx webpack configtest`: the config validates against the schema.
- `npx tsc --noEmit`: types, when loaders transpile only.

## Test first
Test config behavior with a tiny build that fails first, using the Node API.
```js
const webpack = require('webpack');
const config = require('../webpack.config.js');

test('production build emits a hashed main bundle', (done) => {
  webpack({ ...config, mode: 'production', output: { ...config.output, path: '/tmp/out' } }, (err, stats) => {
    expect(err).toBeNull();
    expect(stats.hasErrors()).toBe(false);
    expect(Object.keys(stats.toJson().assetsByChunkName)).toContain('main');
    done();
  });
});
```
Export a function config as `(env, argv) => ({...})` when you need mode-aware settings and call it in the test.

## Do
- Set `mode` explicitly; production enables minification and tree shaking.
- Use `output.filename: '[name].[contenthash].js'` for long-term caching.
- Configure `optimization.splitChunks` and use dynamic `import()` for route-level splitting.
- Turn on `cache: { type: 'filesystem' }` for faster rebuilds.
- Use asset modules (`type: 'asset/resource'`) instead of `file-loader`/`url-loader`.
- Mark side-effect-free packages with `"sideEffects": false` in package.json to enable tree shaking.
- Use `resolve.alias` and `resolve.extensions` deliberately; keep them in sync with the TypeScript config.
- Analyze size with `webpack-bundle-analyzer` before optimizing.

## Avoid
- `file-loader`, `url-loader`, `raw-loader`: deprecated since webpack 5. Use asset modules.
- `devtool: 'eval'` or inline source maps in production: leaks source and bloats output. Use `source-map` or `hidden-source-map`.
- Putting secrets in `DefinePlugin` or `EnvironmentPlugin`: they are inlined into the bundle.
- Legacy options from webpack 4 (`node: { fs: 'empty' }`, `NamedModulesPlugin`): invalid in 5. Use `resolve.fallback`.
- `import _ from 'lodash'` for one function: bundles everything. Import `lodash/fn` or use `lodash-es`.
- Running `webpack-dev-server` output as production: use the built assets.
- Ignoring "asset size limit" warnings: they signal a missing split.

## Review
- [ ] `mode` set; hashed filenames in production.
- [ ] Loaders match webpack 5 (asset modules, no deprecated loaders).
- [ ] No secrets in `DefinePlugin`.
- [ ] Dynamic imports split heavy routes.
- [ ] Source map setting suits production.
