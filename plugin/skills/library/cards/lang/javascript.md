---
name: javascript
title: JavaScript
area: lang
tags: [javascript, node, esm, eslint, npm, async]
detect: [ext:.js, ext:.mjs, ext:.cjs, file:package.json]
related: [typescript, nodejs, eslint, vitest]
---
JavaScript baseline: ES modules, eslint, a lockfile, node:test or vitest, and careful async and equality semantics.

## Verify
- `node --check src/index.js`: the file parses (syntax only).
- `npx eslint .`: lint.
- `npm test`: the project's test script.
- `npm ci`: the lockfile installs cleanly and matches package.json.

## Test first
Use the project's runner; `node --test` needs no dependency. Files `*.test.js`.
```js
import test from "node:test";
import assert from "node:assert/strict";
import { slugify } from "./slugify.js";

test("slugify drops punctuation", () => {
  assert.equal(slugify("Hi, World!"), "hi-world");
});
```

## Do
- Set `"type": "module"` for ESM and include file extensions in relative imports.
- Use `const` by default, `let` when reassigned; use `===`, optional chaining and `??`.
- Use `async`/`await` with `try`/`catch`; run independent work with `Promise.all` (or `allSettled` when partial failure is fine).
- Use `AbortController` and timeouts on `fetch`; check `res.ok` before parsing.
- Commit `package-lock.json` (or the repo's lockfile) and install with `npm ci` in CI.
- Use `structuredClone` for deep copies and `URL`/`URLSearchParams` for URLs.

## Avoid
- Un-awaited promises (a floating `save()`): errors vanish. `await` them or attach `.catch`; enable `no-floating-promises` or `require-await` style rules.
- `await` in a loop over independent calls: serial and slow. Collect and `Promise.all`.
- `||` for defaults when `0`, `""` or `false` are valid: use `??`.
- `JSON.parse(JSON.stringify(x))` for cloning: drops Dates, undefined, Maps. Use `structuredClone`.
- `fetch` assumed to reject on 404 or 500: it does not. Check `res.ok`.
- `eval`, `new Function` and string-built `innerHTML` with user data: injection. Use `textContent` or a sanitizer.
- Mixing `require` and `import` in one package without checking `"type"`: runtime `ERR_REQUIRE_ESM` or `exports is not defined`. Pick one.
- `parseInt(x)` without a radix on user text, or `==` between mixed types: surprising coercion.

## Review
- [ ] No floating promises; errors from async paths reach a handler.
- [ ] External input validated before use; no `eval` or unsafe HTML.
- [ ] Lockfile updated and `npm ci` passes.
- [ ] Module format (ESM or CJS) is consistent with `package.json`.
- [ ] Network calls have timeouts and check status.
