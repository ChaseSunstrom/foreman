---
name: rxjs
title: RxJS
area: node
tags: [rxjs, observable, reactive, operators, angular, streams]
detect: [dep:rxjs]
related: [typescript-generics, vitest, jest, nestjs]
---
RxJS pipelines: pick the right flattening operator, always unsubscribe, test timing with marble tests.

## Verify
- `npx tsc --noEmit`: operator chains still type-check end to end.
- `npx eslint . --max-warnings 0`: lint (rxjs-specific rules only if the project has them configured).
- `npx vitest run` (or `npx jest`): the suite, including TestScheduler marble tests.
- `npx tsc --noEmit --noUnusedLocals`: dead imports from the old `rxjs/operators` path are caught.

## Test first
Use `TestScheduler` so time is virtual and assertions are deterministic.
```ts
import { TestScheduler } from 'rxjs/testing';
import { debounceTime } from 'rxjs';

test('debounces to the last value', () => {
  new TestScheduler((a, e) => expect(a).toEqual(e)).run(({ cold, expectObservable }) => {
    const src = cold('a-b-c---|');
    expectObservable(src.pipe(debounceTime(2))).toBe('------c-|', { c: 'c' });
  });
});
```
Write the marble first, watch it fail, then add the operator.

## Do
- Import operators and creators from `rxjs` (v7+ single entry); `rxjs/operators` is the legacy path.
- Choose flattening on purpose: `switchMap` (latest wins, search), `concatMap` (ordered queue), `mergeMap` with a concurrency arg (parallel), `exhaustMap` (ignore while busy, submit buttons).
- Put `catchError` inside the inner observable so the outer stream survives; return `EMPTY` or a fallback.
- End subscriptions with `takeUntil(destroy$)`, `take(1)`, `firstValueFrom`/`lastValueFrom`, or the framework async pipe.
- Share hot work with `shareReplay({ bufferSize: 1, refCount: true })` or `share()`.
- Use `combineLatest` for state, `forkJoin` for one-shot parallel requests, `withLatestFrom` to sample.
- Type subjects: `BehaviorSubject<T>` for current state, expose `.asObservable()`.

## Avoid
- Nested `subscribe` inside `subscribe`: leaks and races. Flatten with `switchMap`/`concatMap`.
- `toPromise()`: deprecated and removed in v8. Use `firstValueFrom` or `lastValueFrom` (they reject on empty unless `defaultValue` is set).
- `shareReplay(1)` without `refCount: true` on a long-lived source: the source never unsubscribes.
- `mergeMap` for user-triggered saves: responses reorder. Use `concatMap` or `exhaustMap`.
- Errors thrown outside `catchError` terminate the stream permanently; handle per inner request.
- Exposing a raw `Subject` publicly: callers can `next()` it. Expose `.asObservable()`.

## Review
- [ ] Every subscription has a defined end (takeUntil, take, async pipe, or toPromise-replacement).
- [ ] Flattening operator matches the intended concurrency semantics.
- [ ] `catchError` placement keeps the outer stream alive where it should.
- [ ] No nested subscribes and no side effects hidden in `map`; use `tap`.
- [ ] Timing behavior has a marble test, not a real `setTimeout`.
