---
name: vitest
title: Vitest
area: node
tags: [vitest, testing, vite, mocks, coverage, typescript]
detect: [dep:vitest, file:vitest.config.*, file:vitest.workspace.*]
related: [vite, jest, tsconfig, eslint, zod]
---
Vitest tests: Vite-native config, `vi` mocks and fake timers, in-source and typed tests, coverage providers.

## Verify
- `npx vitest run`: one non-watch pass; the CI form (plain `vitest` watches).
- `npx vitest run path/to/file.test.ts -t "name"`: one test while iterating.
- `npx vitest run --coverage`: coverage (needs `@vitest/coverage-v8` or `-istanbul` installed).
- `npx vitest typecheck`: runs `*.test-d.ts` type tests (when `typecheck` is enabled).
- `npx tsc --noEmit`: types of the tests themselves.

## Test first
Tests sit beside the code as `*.test.ts`. Import `describe`, `it` and `expect` from `vitest` unless `globals: true`.
```ts
import { describe, it, expect, vi } from 'vitest';
import { retry } from './retry';

describe('retry', () => {
  it('gives up after 3 attempts', async () => {
    const fn = vi.fn().mockRejectedValue(new Error('boom'));
    await expect(retry(fn, { attempts: 3 })).rejects.toThrow('boom');
    expect(fn).toHaveBeenCalledTimes(3);
  });
});
```

## Do
- Share config with the app: `vitest.config.ts` using `defineConfig` (or `mergeConfig(viteConfig, ...)`) so aliases and plugins match.
- Set `environment` per file or project (`node`, `jsdom`, `happy-dom`); default is `node`.
- Mock with `vi.mock('./mod', () => ({...}))` (hoisted to the top of the file), `vi.spyOn`, `vi.fn`; reset with `restoreMocks: true` or `vi.restoreAllMocks()`.
- Use `vi.hoisted()` for variables the `vi.mock` factory needs.
- Fake time with `vi.useFakeTimers()` and `vi.useRealTimers()`; use `vi.stubEnv` and `vi.unstubAllEnvs`.
- Use `test.each`, `it.concurrent` where tests are independent, and `expect.poll` for eventually-true conditions.
- Set `coverage.include`, `coverage.thresholds` and `coverage.provider`.
- Use `projects` (or the workspace file in older versions) for mixed environments.

## Avoid
- Running bare `vitest` in CI: it enters watch mode and hangs. Use `vitest run`.
- Jest globals (`jest.fn`, `jest.mock`): undefined. Use `vi`.
- A `vi.mock` factory referencing top-level variables: it is hoisted above them and they are undefined. Use `vi.hoisted`.
- Not awaiting async expectations (`expect(p).rejects`): the test passes early. Await them.
- Separate config for tests that drops Vite aliases and plugins: imports fail only under test. Merge with the app config.
- Assuming `@vitest/coverage-*` ships with Vitest: install the provider and match its version to `vitest`.
- Mock state leaking across tests: set `mockReset`/`restoreMocks` in config.

## Review
- [ ] CI uses `vitest run`.
- [ ] Config extends the app's Vite config.
- [ ] Mocks are restored and factories use `vi.hoisted` for shared values.
- [ ] Async assertions are awaited.
- [ ] Coverage provider is installed with thresholds set.
