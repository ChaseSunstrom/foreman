---
name: angular-rxjs
title: Angular RxJS
area: web
tags: [angular, rxjs, observables, operators, http, subscriptions]
detect: [dep:rxjs]
related: [angular, angular-signals, typescript]
---
RxJS in Angular: HttpClient streams, flattening operators, subscription cleanup and marble-style tests.

## Verify
- `npx ng build`: AOT and type checks, including `async` pipe types.
- `npx ng test --watch=false`: unit tests.
- `npx tsc --noEmit -p tsconfig.app.json`: strict types for stream generics.
- `npx eslint .`: with an rxjs lint plugin it flags nested subscribes and missing unsubscribe.

## Test first
Use `HttpTestingController` for HTTP streams and `TestScheduler` for timing.
```ts
import { TestBed } from "@angular/core/testing";
import { provideHttpClient } from "@angular/common/http";
import { HttpTestingController, provideHttpClientTesting } from "@angular/common/http/testing";
import { UserService } from "./user.service";

it("maps the API user", () => {
  TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
  const svc = TestBed.inject(UserService);
  let name = "";
  svc.name$(1).subscribe(n => (name = n));
  TestBed.inject(HttpTestingController).expectOne("/api/users/1").flush({ name: "Ada" });
  expect(name).toBe("Ada");
});
```

## Do
- Prefer the `async` pipe in templates, or `toSignal`, so Angular subscribes and unsubscribes.
- Where you subscribe manually, end with `takeUntilDestroyed()` (from `@angular/core/rxjs-interop`) in an injection context.
- Pick the flattening operator by intent: `switchMap` for latest-wins (search), `concatMap` for ordered writes, `exhaustMap` for ignore-while-busy (submit), `mergeMap` for parallel.
- Use `catchError` inside the inner observable so one failure does not kill the outer stream.
- Debounce input with `debounceTime` and `distinctUntilChanged` before `switchMap`.
- Share expensive streams with `shareReplay({ bufferSize: 1, refCount: true })`.
- Type streams and keep operators in `pipe()` chains small and named.

## Avoid
- Subscribing inside a subscribe: use a flattening operator.
- Manual `subscribe` without cleanup in components: leaks and ghost updates. Use `async`, `takeUntilDestroyed` or `toSignal`.
- `shareReplay(1)` without `refCount: true` on long-lived sources: the source never unsubscribes.
- `catchError` on the outer stream for a request in `switchMap`: the stream completes after the first error. Catch inside.
- `toPromise()`: deprecated. Use `firstValueFrom` or `lastValueFrom`.
- `Subject` exposed publicly: expose `asObservable()` and keep `next` private.
- `mergeMap` for search-as-you-type: stale responses can arrive out of order. Use `switchMap`.

## Review
- [ ] Every manual subscription has a teardown path.
- [ ] No nested subscribes, and each flattening operator is chosen on purpose.
- [ ] Errors are handled inside inner streams and surfaced to the UI.
- [ ] Subjects are private and shared streams use `refCount`.
- [ ] HTTP behavior is tested with `HttpTestingController`.
