---
name: deno
title: Deno
area: node
tags: [deno, typescript, runtime, permissions, jsr, server]
detect: [file:deno.json, file:deno.jsonc, file:deno.lock]
related: [node, bun, hono, tsconfig]
---
Deno projects: permission flags, `deno.json` tasks and imports, built-in test, lint, fmt and type-check tooling.

## Verify
- `deno check **/*.ts`: type-checks every module.
- `deno lint`: built-in linter.
- `deno fmt --check`: formatting.
- `deno test`: runs `*_test.ts` and `*.test.ts` files.
- `deno task`: lists the tasks defined in `deno.json`.

## Test first
Use `Deno.test` with `jsr:@std/assert`. Tests live beside the code as `*_test.ts`.
```ts
import { assertEquals, assertRejects } from "jsr:@std/assert";
import { parseId } from "./id.ts";

Deno.test("parseId rejects empty", async () => {
  await assertRejects(async () => parseId(""), Error, "empty");
});
Deno.test("parseId trims", () => assertEquals(parseId(" 7 "), 7));
```
Run `deno test`; add `--allow-read` etc. only as the test needs.

## Do
- Declare tasks and the import map in `deno.json` (`"tasks"`, `"imports"`); run with `deno task dev`.
- Grant the narrowest permission: `--allow-net=api.example.com`, `--allow-read=./data`, `--allow-env=PORT`.
- Import with `jsr:` or `npm:` specifiers and map them in `imports`, with a version range.
- Commit `deno.lock`; run CI with `--frozen` so the lockfile is not rewritten.
- Serve with `Deno.serve` and read `Deno.env.get` once at startup.
- Use `import.meta.main` to guard entry-point code.

## Avoid
- `-A` / `--allow-all` in scripts and Dockerfiles: removes the sandbox. List exact permissions.
- `https://deno.land/std@...` imports and `deno.land/x` for new code: legacy. Use `jsr:@std/...`.
- `std/http` `serve()`: removed. Use `Deno.serve`.
- Bare `import "lodash"` with no map entry: fails. Use `npm:lodash` or add it to `imports`.
- Extensionless relative imports: Deno requires the `.ts` extension.
- `Deno.run`: removed. Use `new Deno.Command(...)`.
- Unpinned remote imports: builds change over time. Pin versions and keep the lock.

## Review
- [ ] Every permission flag is scoped; no `-A`.
- [ ] `deno.json` has tasks for check, lint, fmt, test.
- [ ] Imports use `jsr:`/`npm:` with versions; lockfile committed.
- [ ] Entry point guarded by `import.meta.main` where it is also imported.
