---
name: pino
title: Pino
area: node
tags: [pino, logging, json, redaction, transports, observability]
detect: [dep:pino, dep:pino-http, dep:pino-pretty]
related: [winston, express, fastify, node]
---
Pino structured JSON logging: child loggers, redaction, request correlation, pretty output in dev only.

## Verify
- `npx tsc --noEmit`: logger usage and child bindings type-check.
- `node app.js | head -n 3`: output is one JSON object per line (no pretty-printer in the production path).
- `npx vitest run`: tests capture logs through a writable destination stream.
- `grep -rn "console\.log" src`: stray console calls that bypass the logger.

## Test first
Write to an in-memory stream and assert the redaction.
```ts
import pino from 'pino';

test('redacts the authorization header', () => {
  const lines: string[] = [];
  const log = pino({ redact: ['req.headers.authorization'] },
    { write: (s: string) => { lines.push(s); } });
  log.info({ req: { headers: { authorization: 'Bearer secret' } } }, 'hit');
  expect(lines[0]).not.toContain('secret');
  expect(JSON.parse(lines[0]).req.headers.authorization).toBe('[Redacted]');
});
```

## Do
- Create one root logger; derive `log.child({ module, requestId })` for context.
- Use the merge-object-first signature: `log.info({ userId }, 'message')`, and `{ err }` for errors so the `err` serializer runs.
- Configure `redact` paths (or `{ paths, censor, remove }`) for tokens, passwords, cookies.
- Set level from env (`level: process.env.LOG_LEVEL ?? 'info'`); keep `fatal`, `error`, `warn`, `info`, `debug`, `trace` meanings.
- Use `pino-http` (or the framework's built-in `logger` option in Fastify) for request logs with a request id.
- Pretty-print in dev through `pino-pretty` as a transport or piped CLI, never in production.
- Flush on exit: `pino.final` is gone, so use `logger.flush()` for async destinations and end transports on shutdown.
- Format levels as strings with `formatters.level` if the log platform wants labels.

## Avoid
- `log.info('user ' + id)` string concatenation: no structured fields. Pass an object.
- `log.error(err)` as the only argument without a message and `{ err }`: loses serialization. Use `log.error({ err }, 'failed to X')`.
- Logging whole request or response bodies: PII and size. Log ids and sizes.
- `transport: { target: 'pino-pretty' }` in production: slower and not machine readable.
- Creating loggers per request without `child`: duplicates config and loses the bindings.
- Wrong `redact` path syntax: use dot or bracket paths, and `*` only matches one level.

## Review
- [ ] Redaction covers every secret-bearing path and has a test.
- [ ] Errors are logged under `err` with a message.
- [ ] Request ids propagate through child loggers.
- [ ] No pretty transport in production config.
- [ ] No leftover `console.*` calls.
