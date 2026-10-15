---
name: bullmq
title: BullMQ
area: node
tags: [bullmq, queue, redis, jobs, worker, retries]
detect: [dep:bullmq]
related: [node, nestjs, vitest, zod]
---
BullMQ job queues on Redis: idempotent workers, bounded retries with backoff, graceful shutdown, no job loss.

## Verify
- `npx tsc --noEmit`: job data and return types line up (use `Queue<Data, Result, Name>`).
- `redis-cli ping`: Redis is reachable for integration tests.
- `redis-cli config get maxmemory-policy`: must be `noeviction`, or queued jobs can be evicted.
- `npx vitest run`: worker tests against a real Redis.

## Test first
Run a real worker in the test against a test Redis and assert the retry outcome.
```ts
import { Queue, Worker, QueueEvents } from 'bullmq';
const connection = { host: '127.0.0.1', port: 6379 };

test('retries then fails after attempts exhausted', async () => {
  const q = new Queue('t-q', { connection }); const ev = new QueueEvents('t-q', { connection });
  let calls = 0;
  const w = new Worker('t-q', async () => { calls++; throw new Error('boom'); }, { connection });
  const job = await q.add('x', {}, { attempts: 2, backoff: { type: 'fixed', delay: 10 } });
  await expect(job.waitUntilFinished(ev)).rejects.toThrow('boom');
  expect(calls).toBe(2);
  await w.close(); await q.obliterate({ force: true }); await q.close(); await ev.close();
});
```

## Do
- Give workers and `QueueEvents` their own connections; a worker needs `maxRetriesPerRequest: null` on an ioredis instance you pass in.
- Make processors idempotent; use `jobId` for dedupe and key side effects on it.
- Set `attempts` and `backoff` (`exponential`) per job or in `defaultJobOptions`.
- Set `removeOnComplete` and `removeOnFail` (counts or age) so Redis does not grow forever.
- Listen for `worker.on('error')` and `'failed'`; an unhandled `error` event crashes the process.
- Shut down with `await worker.close()` on SIGTERM so active jobs finish.
- Throw `UnrecoverableError` to skip further retries.
- Use `FlowProducer` for parent/child dependencies and `upsertJobScheduler` for repeatable jobs.

## Avoid
- Long CPU work in the processor: it blocks the event loop and jobs stall. Use sandboxed processors (a file path) or a separate process.
- Storing large payloads in job data: store a reference (id or key) instead.
- Dropping `worker.on('error')`: connection blips become uncaught exceptions.
- Redis `maxmemory-policy` other than `noeviction`: keys silently vanish.
- Relying on exactly-once: delivery is at-least-once, so stalled jobs rerun.
- Legacy `QueueScheduler`: not needed in current versions; remove it.

## Review
- [ ] Retries are bounded, with backoff, and the failure path is tested.
- [ ] Processors are idempotent and keyed by job id.
- [ ] Completed and failed jobs are pruned.
- [ ] Graceful shutdown closes workers, queues and events.
- [ ] Error and failed listeners exist on every worker.
