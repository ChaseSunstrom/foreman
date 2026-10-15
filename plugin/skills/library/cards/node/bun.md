---
name: bun
title: Bun
area: node
tags: [bun, javascript, typescript, runtime, test, bundler]
detect: [file:bun.lock, file:bun.lockb, file:bunfig.toml, dep:bun-types, dep:@types/bun]
related: [node, vitest, tsconfig, hono]
---
Bun as runtime, package manager, bundler and test runner (`bun test`, `Bun.serve`, `bun install`).

## Verify
- `bun --version`: the pinned version matches CI and the Dockerfile.
- `bun install --frozen-lockfile`: lockfile is in sync with `package.json`.
- `bun test`: runs `*.test.ts` and `*.spec.ts` files.
- `bunx tsc --noEmit`: types, since Bun runs TypeScript without checking it.
- `bun build ./src/index.ts --outdir dist --target bun`: the bundle builds.

## Test first
`bun:test` is Jest-shaped. Tests sit beside the code as `*.test.ts`.
```ts
import { test, expect } from "bun:test";
import { app } from "./app";

test("GET /health returns ok", async () => {
  const res = await app.fetch(new Request("http://t/health"));
  expect(res.status).toBe(200);
  expect(await res.json()).toEqual({ ok: true });
});
```
Run `bun test`; `bun test --watch` while iterating.

## Do
- Type-check separately with `tsc --noEmit`; Bun strips types and never fails on them.
- Use `Bun.serve({ fetch })` or a Web-standard framework (Hono, Elysia); handlers take `Request` and return `Response`.
- Keep `bunfig.toml` for test preload and registry settings.
- Commit the lockfile (`bun.lock`) and install with `--frozen-lockfile` in CI.
- Use `Bun.file()` and `Bun.write()` for file I/O; use `Bun.env` or `process.env`.
- Read `.env` automatically; do not add `dotenv`.
- Add `@types/bun` as a dev dependency for types.

## Avoid
- Assuming Node-API parity: some `node:` modules and native addons differ. Run the real workload before migrating.
- Mixing `bun.lockb` and `bun.lock` or other lockfiles (`package-lock.json`): installs diverge. Keep one.
- Trusting `bun run` to catch type errors: it will not. Add the `tsc` step to CI.
- Using `bun test` mocks from Jest by name (`jest.fn`): use `mock()` and `spyOn` from `bun:test`.
- Deploying with `bun --hot` or `--watch`: dev only.
- Installing and running lifecycle scripts of untrusted deps: Bun skips them by default; list vetted packages in `trustedDependencies` only.

## Review
- [ ] One lockfile, installed frozen in CI.
- [ ] A `tsc --noEmit` step exists.
- [ ] Docker image and CI pin the Bun version.
- [ ] `trustedDependencies` lists only vetted packages.
