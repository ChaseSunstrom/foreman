---
name: web-workers
title: Web Workers
area: frontend
tags: [performance, workers, threads, comlink, offscreen]
detect: [dep:comlink]
related: [code-splitting, web-performance, virtualized-lists, file-drop]
---
Move CPU-heavy work off the main thread with dedicated workers, typed messages, transferables and cleanup.

## Verify
- `npx tsc --noEmit`: message types and worker entry compile (use the `webworker` lib for worker files).
- `npx vitest run`: pure logic extracted from the worker is tested directly.
- `npx playwright test`: the real worker runs in a browser and the UI stays responsive.

## Test first
Keep the logic a plain function, test it, then wrap it.
```ts
// parse.ts
export function parseCsv(text: string): string[][] {
  return text.trim().split('\n').map(l => l.split(','));
}
// parse.test.ts
import { expect, test } from 'vitest';
import { parseCsv } from './parse';

test('parses rows and columns', () => {
  expect(parseCsv('a,b\n1,2\n')).toEqual([['a', 'b'], ['1', '2']]);
});
// worker.ts: self.onmessage = e => self.postMessage(parseCsv(e.data));
```

## Do
- Create with `new Worker(new URL('./w.ts', import.meta.url), { type: 'module' })` so the bundler emits and hashes it.
- Define a message protocol (`{ id, type, payload }`) and match responses by `id`.
- Transfer large buffers: `postMessage(buf, [buf])` to avoid structured-clone copies.
- Terminate on unmount and when superseded: `worker.terminate()`; also support cancellation by id or `AbortSignal`.
- Handle `onerror` and `onmessageerror`; reject the pending promise.
- Report progress with periodic messages for long jobs and keep the UI showing a status.
- Use `OffscreenCanvas` for canvas rendering and a pool sized near `navigator.hardwareConcurrency` for parallel jobs.
- Wrap the API with Comlink if the call surface is large.

## Avoid
- Spawning a worker per keystroke or item: startup cost dominates. Reuse one or a small pool.
- Posting objects with functions, DOM nodes or class instances: the clone throws or loses methods. Send plain data.
- Touching `document` or `window` in a worker: not available. Use `self` and message back.
- Never terminating: orphaned workers hold memory after navigation. Clean up in the effect return.
- Moving trivial work into a worker: message overhead exceeds the gain. Measure first.
- Ignoring stale replies: a slow earlier job overwrites a newer result. Compare `id` before applying.

## Review
- [ ] Heavy logic is a pure function with a unit test.
- [ ] Worker lifecycle is bound to the owning component.
- [ ] Errors and cancellation reach the caller.
- [ ] Large payloads use transfer, not copy.
- [ ] Out-of-order responses cannot overwrite newer state.
