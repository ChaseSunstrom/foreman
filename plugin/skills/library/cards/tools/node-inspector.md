---
name: node-inspector
title: Node.js inspector
area: tools
tags: [node, debugger, inspector, devtools, profiling, javascript]
detect: [file:package.json, file:.vscode/launch.json]
related: [flamegraphs, memory-leaks, perf]
---
Debug and profile Node.js with `--inspect`, Chrome DevTools or an editor, plus built-in profilers.

## Verify
- `node --inspect-brk script.js`: starts paused on the first line and prints the debugger address.
- `node --test`: the built-in test runner suite passes (Node 18 and later).
- `node --cpu-prof script.js`: writes a `.cpuprofile` file you can load in DevTools.
- `node --heap-prof script.js`: writes a `.heapprofile` for allocation sampling.
- `node --trace-warnings script.js`: where each process warning originates.

## Test first
Reproduce with a failing test, then debug that test.
```js
import test from "node:test";
import assert from "node:assert/strict";
import { parse } from "./parse.js";

test("parse rejects empty input", () => {
  assert.throws(() => parse(""), /empty/);
});
```
Debug it with `node --inspect-brk --test parse.test.js`, then attach.

## Do
- Attach with DevTools at `chrome://inspect` or an editor launch config; `--inspect=127.0.0.1:9229` is the default bind.
- Use `debugger;` statements only while debugging; breakpoints and logpoints in the UI are cleaner.
- Pass `--enable-source-maps` for TypeScript or bundled code so stacks point to source.
- Use `node --inspect-wait` to wait for a debugger to attach before running.
- Diagnose hangs with `process.on("SIGUSR1")` default (starts the inspector on a running process) or a `--report-on-signal` diagnostic report.
- Take heap snapshots from DevTools Memory tab; compare two snapshots to find growth.
- For async stack traces, keep `async`/`await` rather than raw callbacks.
- Use `NODE_DEBUG=http,net` style env flags for core module tracing.

## Avoid
- Binding the inspector to `0.0.0.0` or exposing port 9229: remote code execution for anyone who connects. Keep it on localhost and tunnel over `ssh -L`.
- Leaving `debugger;` or `--inspect` in production start scripts.
- Profiling a minified or transpiled build without source maps: names are unreadable.
- Ignoring unhandled promise rejections: Node terminates on them by default in modern versions. Find the origin with `--trace-warnings` or `--unhandled-rejections=strict`.
- Profiling a tiny run: sampling needs steady load. Run representative work for several seconds.
- Debugging only under `nodemon` restarts: breakpoints reset. Use `--watch` with a stable inspector port or restart attach.

## Review
- [ ] Inspector is bound to localhost only and absent from production config.
- [ ] No `debugger;` statements committed.
- [ ] The fix is covered by a test that failed first.
- [ ] Profiles were taken with source maps and representative load.
