---
name: javascript-async
title: JavaScript async patterns
area: idioms
tags: [javascript, async, promises, concurrency, abort, event-loop]
detect: []
related: [javascript, typescript-strict, node, vitest]
---
Promises and async/await done right: concurrency on purpose, errors always handled, cancellation wired through.

## Verify
- `node --test`: runs the built-in test runner over the repo's tests.
- `npx eslint .`: lint with the repo's rules (enable `no-floating-promises` through typescript-eslint in TS code).
- `node --unhandled-rejections=strict script.js`: an unhandled rejection crashes loudly instead of warning.

## Test first
Assert on rejection and timing without real waits.
```js
import test from "node:test";
import assert from "node:assert/strict";
import { fetchAll } from "./fetch-all.js";

test("fetchAll rejects when any request fails", async () => {
  const ok = async () => 1;
  const bad = async () => { throw new Error("boom"); };
  await assert.rejects(fetchAll([ok, bad]), /boom/);
});
```
Use fake timers (`mock.timers`, or the framework's equivalent) instead of `setTimeout` waits.

## Do
- Run independent work together with `Promise.all`, and use `Promise.allSettled` when partial failure is acceptable.
- Await in a sequence only when each step needs the previous result.
- Always `await` or return a promise. Handle rejections with `try/catch` or `.catch`.
- Pass an `AbortSignal` to `fetch` and your own functions, and use `AbortSignal.timeout(ms)` for deadlines.
- Limit concurrency for large fan-outs with a small pool, not 10,000 simultaneous calls.
- Use `for await ... of` for async iterables and streams.
- Use `Promise.withResolvers()` only where the runtime supports it.

## Avoid
- `array.forEach(async ...)`: it does not wait. Use `for ... of` with `await`, or `Promise.all(array.map(...))`.
- Awaiting inside a loop for independent calls: serial and slow. Collect promises and `Promise.all` them.
- A floating promise (no await, no catch): failures vanish or crash later. Await it or attach `.catch`.
- `new Promise(async (resolve) => ...)`: a throw inside is lost. Write an `async` function.
- `return promise` inside `try/catch` without `await`: the catch never fires. Use `return await`.
- Mixing callbacks and promises by hand: wrap once with `util.promisify` or a single `new Promise`.
- `setTimeout` as synchronization: it hides race conditions. Await the actual event.

## Review
- [ ] Every promise is awaited, returned or explicitly caught.
- [ ] Independent operations run concurrently and bounded.
- [ ] Network and long calls take an abort signal or timeout.
- [ ] Cleanup runs in `finally`.
- [ ] Tests cover rejection and cancellation paths.
