---
name: jest
title: Jest
area: node
tags: [jest, testing, mocks, coverage, typescript, unit-tests]
detect: [dep:jest, dep:ts-jest, dep:@swc/jest, dep:babel-jest, file:jest.config.*]
related: [vitest, nestjs, express, eslint, tsconfig]
---
Jest tests: config and transforms, mocking modules and timers, async assertions, coverage thresholds.

## Verify
- `npx jest --ci`: the suite runs without writing new snapshots.
- `npx jest --coverage`: coverage report and any configured thresholds.
- `npx jest path/to/file.test.ts -t "name"`: one test while iterating.
- `npx jest --detectOpenHandles`: finds leaked handles that stop the process from exiting.
- `npx jest --listTests`: confirms which files the config actually matches.

## Test first
Write the failing assertion beside the module as `*.test.ts`.
```ts
import { applyDiscount } from './pricing';

describe('applyDiscount', () => {
  it('never returns a negative price', () => {
    expect(applyDiscount(10, 1.5)).toBe(0);
  });
  it('rejects NaN', async () => {
    expect(() => applyDiscount(NaN, 0.1)).toThrow(RangeError);
  });
});
```
Use `await expect(promise).rejects.toThrow(...)` for async failures.

## Do
- Pick one transform: `ts-jest`, `@swc/jest` (faster) or `babel-jest`; configure it in `jest.config`.
- Use `jest.fn()`, `jest.spyOn(obj, 'm')` and `jest.mock('./mod')`; restore with `restoreMocks: true` or `afterEach(jest.restoreAllMocks)`.
- Control time with `jest.useFakeTimers()` and `jest.advanceTimersByTime()`; call `jest.useRealTimers()` afterward.
- Return or `await` every promise in a test.
- Set `coverageThreshold` in config and `collectCoverageFrom` to include untested files.
- Use `test.each` for table-driven cases.
- Set `testEnvironment` explicitly (`node` for servers, `jsdom` for DOM).
- Isolate DB or network tests from unit tests with projects or file naming.

## Avoid
- Forgetting `await` or `return` on async assertions: the test passes before the assertion runs. Await it, or use `expect.assertions(n)`.
- `jest.mock` after imports expecting it to apply: it is hoisted only by the babel/ts transform; with ESM it does not hoist. Use `jest.unstable_mockModule` and dynamic imports for native ESM.
- Mocks leaking between tests: set `clearMocks`/`restoreMocks`, and reset module state with `jest.resetModules()`.
- Snapshots of large objects or HTML: reviewers rubber-stamp updates. Assert on specific fields.
- `--forceExit` to hide a hanging suite: masks leaks. Close servers, pools and timers in `afterAll`.
- Testing implementation details (`toHaveBeenCalledTimes` on internals): breaks on refactor. Assert outputs and effects.
- `ts-jest` with `isolatedModules` off on huge repos: slow. Use `@swc/jest` or enable isolated modules and type-check separately.

## Review
- [ ] Each test fails without the change it covers.
- [ ] Async tests await and mocks are restored.
- [ ] No snapshot is larger than one screen.
- [ ] Coverage thresholds exist and include all source.
- [ ] Open handles are cleaned up; no `--forceExit`.
