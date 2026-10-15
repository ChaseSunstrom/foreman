---
name: worker-threads
title: Node worker_threads
area: node
tags: [worker-threads, concurrency, cpu, threads, sharedarraybuffer, pool]
detect: []
related: [node, node-streams, sharp, vitest]
---
node:worker_threads for CPU-bound work: pooled workers, message protocols with errors, transfer instead of copy, clean shutdown.

## Verify
- `node --check worker.js`: the worker file parses.
- `node -e "const {isMainThread}=require('node:worker_threads');console.log(isMainThread)"`: the module is available and `true` on the main thread.
- `npx tsc --noEmit`: message types shared between main and worker compile.
- `node --test`: tests that start a worker and assert it terminates (a hang means a leaked worker).

## Test first
Assert both the result and that the worker exits.
```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Worker } from 'node:worker_threads';

test('worker returns a result and exits cleanly', async () => {
  const w = new Worker(new URL('./square.worker.js', import.meta.url), { workerData: 7 });
  const [msg] = await Promise.race([
    new Promise(r => w.once('message', m => r([m]))),
    new Promise((_, rej) => w.once('error', rej)),
  ]);
  assert.equal(msg, 49);
  assert.equal(await new Promise(r => w.once('exit', r)), 0);
});
```

## Do
- Use workers for CPU-heavy work only; I/O is already async on the main thread.
- Pool a fixed number of workers (about `os.availableParallelism() - 1`) and queue tasks, rather than spawn per task; a library such as piscina does this.
- Define a message protocol with an id and a `type`; reply with `{ id, ok, value | error }` and serialize errors to plain objects.
- Handle `error`, `messageerror` and `exit` events on every worker; reject pending tasks on exit with a non-zero code.
- Transfer large buffers: `postMessage(buf, [buf.buffer])`; share state with `SharedArrayBuffer` plus `Atomics`.
- Use `workerData` for startup input and `parentPort.postMessage` for results.
- Use `worker.terminate()` or let the worker finish; call `worker.unref()` for background pools.
- Use `MessageChannel` or `BroadcastChannel` for worker-to-worker traffic.

## Avoid
- A worker per request: startup costs tens of milliseconds each and exhausts memory. Pool.
- Passing functions, class instances with methods, or DOM-like objects: structured clone drops or throws on them. Pass plain data.
- Ignoring the `error` event: an uncaught exception in the worker is otherwise lost and the caller waits forever.
- Racing on shared memory without `Atomics`: torn reads. Use `Atomics.load/store/wait`.
- Copying large arrays on every message: slow. Transfer the underlying ArrayBuffer.
- Blocking the worker's event loop but expecting cancellation: `terminate()` is the only hard stop.

## Review
- [ ] Task is CPU-bound and measured to benefit.
- [ ] Pool size bounded; queue has a limit or backpressure.
- [ ] Errors and exits reject pending work.
- [ ] Large payloads are transferred or shared, not cloned.
- [ ] Shutdown terminates workers so the process can exit.
