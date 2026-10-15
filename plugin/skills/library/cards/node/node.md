---
name: node
title: Node.js
area: node
tags: [node, javascript, typescript, runtime, server, esm]
detect: [file:package.json, file:.nvmrc, file:.node-version]
related: [npm-publishing, pnpm, tsconfig, vitest, jest, eslint]
---
Node.js services and libraries: ESM vs CommonJS, the built-in test runner, async error handling, graceful shutdown.

## Verify
- `node --version && node -e "console.log(process.versions.v8)"`: the runtime matches `engines` and `.nvmrc`.
- `node --check src/index.js`: syntax parses (plain JS only).
- `node --test`: the built-in runner finds and runs `*.test.js` files.
- `npm ls --all 2>&1 | grep -i "invalid\|missing"`: no broken dependency tree.
- `npm audit --omit=dev`: known advisories in production deps.

## Test first
Use `node:test` and `node:assert/strict` unless the repo already uses Jest or Vitest. Tests sit beside the code or in `test/`.
```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseAmount } from '../src/amount.js';

test('parseAmount rejects negatives', () => {
  assert.throws(() => parseAmount('-5'), { name: 'RangeError' });
});
```
Run with `node --test`.

## Do
- Pick one module system. Set `"type": "module"` for ESM; ESM needs file extensions in relative imports (`./a.js`).
- Use `node:` prefixes for built-ins (`node:fs/promises`, `node:path`).
- Validate `process.env` once at startup and fail fast; never read env scattered through code.
- Handle `SIGTERM`/`SIGINT`: stop accepting connections, drain, then `process.exit`.
- Use `AbortController` and `AbortSignal.timeout(ms)` for fetch and I/O timeouts.
- Use `stream/promises` `pipeline` for streams so errors propagate and handles close.
- Pin the runtime with `engines.node` and `.nvmrc`; run CI on that version.

## Avoid
- Unhandled promise rejections (fatal by default): `await` every promise or attach `.catch`; do not paper over with a global `unhandledRejection` handler.
- Sync fs or crypto (`readFileSync`, `pbkdf2Sync`) in request paths: they block the event loop. Use promise APIs.
- `new Buffer()`: deprecated and unsafe. Use `Buffer.from` or `Buffer.alloc`.
- `__dirname` in ESM: it is undefined. Use `import.meta.dirname` or `fileURLToPath(import.meta.url)`.
- `require` of an ESM-only package from CJS without checking support: fails or differs by version. Use dynamic `import()`.
- Building paths or SQL by string concatenation from user input: use `path.resolve` plus a prefix check, and parameterized queries.
- Global `fetch` with no timeout: hangs forever. Pass `signal`.

## Review
- [ ] No floating promises; async handlers have error paths.
- [ ] Env is parsed and validated in one module.
- [ ] Graceful shutdown closes servers, pools and timers.
- [ ] Production deps contain no dev-only packages; lockfile is committed.
- [ ] No blocking sync calls on hot paths.
