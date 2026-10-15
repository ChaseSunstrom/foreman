---
name: winston
title: Winston
area: node
tags: [winston, logging, transports, formats, rotation, observability]
detect: [dep:winston, dep:winston-daily-rotate-file]
related: [pino, express, node]
---
Winston logging: composed formats, explicit transports, error stacks preserved, handlers for uncaught exceptions.

## Verify
- `npx tsc --noEmit`: logger config and metadata types compile.
- `node -e "require('./dist/logger').info('x')"`: emits a line in the configured format.
- `npx vitest run`: tests attach a memory transport and assert on entries.
- `grep -rn "console\.\(log\|error\)" src`: stray console calls that bypass the logger.

## Test first
Use a stream transport to capture entries.
```ts
import winston from 'winston';
import { Writable } from 'node:stream';

test('logs errors with message and stack', () => {
  const chunks: string[] = [];
  const log = winston.createLogger({
    format: winston.format.combine(winston.format.errors({ stack: true }), winston.format.json()),
    transports: [new winston.transports.Stream({
      stream: new Writable({ write(c, _e, cb) { chunks.push(String(c)); cb(); } }) })],
  });
  log.error(new Error('boom'));
  expect(JSON.parse(chunks[0])).toMatchObject({ level: 'error', message: 'boom' });
  expect(JSON.parse(chunks[0]).stack).toContain('Error: boom');
});
```

## Do
- Compose formats in order: `format.combine(format.timestamp(), format.errors({ stack: true }), format.json())`.
- Use `format.colorize()` and `format.simple()` only in the dev console transport.
- Set `level` from env; choose npm levels or define `levels` once and keep consistent.
- Add `defaultMeta: { service }` and `logger.child({ requestId })` for context.
- Use `exceptionHandlers` and `rejectionHandlers` to log uncaught errors; set `exitOnError` deliberately.
- Rotate files with `winston-daily-rotate-file` (`maxSize`, `maxFiles`, `zippedArchive`) or log to stdout and let the platform collect.
- Call `logger.end()` and wait for `finish` before `process.exit` so buffers flush.
- Use `format((info) => ...)()` custom formats for redaction.

## Avoid
- `log.error('failed', err)` expecting the stack: without `format.errors({ stack: true })` it is lost. Pass the error first or add the format.
- A logger with no transports: winston warns and drops logs. Add one explicitly.
- Writing unbounded log files: add rotation or log to stdout.
- Logging secrets in metadata objects: redact in a custom format.
- Synchronous `process.exit()` right after logging: truncates output. Wait for `finish`.
- Building a new logger per call: use one module-level instance.

## Review
- [ ] Transports and levels differ appropriately between dev and production.
- [ ] Error stacks appear in output, verified by a test.
- [ ] Uncaught exceptions and rejections are handled.
- [ ] Rotation or an external collector bounds disk use.
- [ ] Sensitive fields are redacted.
