---
name: node-streams
title: Node streams
area: node
tags: [streams, backpressure, pipeline, transform, async-iterators, web-streams]
detect: []
related: [node, undici, sharp, worker-threads]
---
Node streams: compose with pipeline, respect backpressure, destroy on error, convert to async iterators.

## Verify
- `node --test`: tests that finish only if the stream ends (a hang means a missing end or error path).
- `node --trace-warnings app.js`: shows MaxListeners and unhandled stream error warnings with origins.
- `node -e "require('node:stream/promises')"`: promise-based `pipeline` and `finished` exist.
- `npx tsc --noEmit`: stream element types in generics compile.

## Test first
Test transforms with in-memory sources and `pipeline`; include the failure path.
```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { Readable, Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';

test('pipeline rejects when a transform errors', async () => {
  const boom = new Transform({ transform(chunk, _e, cb) { cb(new Error('bad')); } });
  await assert.rejects(
    pipeline(Readable.from(['a', 'b']), boom, async function (src) { for await (const _ of src); }),
    /bad/,
  );
});
```

## Do
- Connect stages with `stream/promises` `pipeline(a, b, c)`: it forwards errors and destroys every stream.
- Consume with `for await (const chunk of readable)` and produce with `Readable.from(iterable)` or async generators.
- Honor backpressure: when `write()` returns `false`, wait for `'drain'` (`await once(w, 'drain')`).
- Implement `Transform` with `transform(chunk, enc, cb)` and `flush(cb)`; call `cb(err)` or `this.push(...)`.
- Use `objectMode: true` for non-buffer chunks and set `highWaterMark` deliberately.
- Add `AbortSignal` via the `signal` option or `pipeline(..., { signal })` for cancellation.
- Use `stream.compose`, `Readable.toWeb` and `Readable.fromWeb` to bridge Web Streams.
- Limit sizes: count bytes in a Transform and error past a cap for uploads.

## Avoid
- `a.pipe(b).pipe(c)`: errors do not propagate and streams leak. Use `pipeline`.
- Ignoring `'error'` on a stream: an unhandled `error` event crashes the process.
- Ignoring the `write()` return value in a loop: the buffer grows without bound (memory blowup on large files).
- Mixing `'data'` listeners with `for await` or `pipe`: chunks go to the wrong consumer. Use one mode.
- Buffering a whole stream with `chunks.push` to concat: defeats streaming. Process per chunk.
- Forgetting `callback` in `_write`/`_transform`: the stream stalls forever.

## Review
- [ ] Every composition uses `pipeline`, and errors propagate.
- [ ] Backpressure respected in manual writes.
- [ ] Failure and early-close paths are tested.
- [ ] Memory stays flat on large inputs (checked with a large fixture).
- [ ] Size caps and abort signals exist for untrusted sources.
