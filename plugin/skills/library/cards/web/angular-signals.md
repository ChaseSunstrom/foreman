---
name: angular-signals
title: Angular Signals
area: web
tags: [angular, signals, computed, effect, zoneless, inputs]
detect: [dep:@angular/core]
related: [angular, angular-rxjs, typescript]
---
Angular signals: fine-grained reactive state with signal, computed, effect, signal inputs and RxJS interop.

## Verify
- `npx ng build`: AOT template and type checks.
- `npx ng test --watch=false`: unit tests (the runner depends on the project setup).
- `npx tsc --noEmit -p tsconfig.app.json`: type check of the app config.
- `npx ng lint`: if a lint builder is configured.

## Test first
Set inputs through the fixture and read the DOM after `detectChanges`.
```ts
import { TestBed } from "@angular/core/testing";
import { CounterComponent } from "./counter.component";

it("doubles the count", () => {
  const f = TestBed.createComponent(CounterComponent);
  f.componentRef.setInput("count", 2);
  f.detectChanges();
  expect(f.nativeElement.textContent).toContain("4");
});
```

## Do
- Hold state in `signal<T>()`; change it with `set` or `update(v => ...)` using immutable values.
- Derive with `computed(() => ...)`; it is lazy, cached and read-only.
- Use `input()`, `input.required<T>()`, `output()` and `model()` for component APIs in versions that provide them; read inputs by calling them.
- Use `effect` sparingly, for side effects such as logging or syncing to storage; create it in an injection context.
- Bridge with `toSignal(obs$, { initialValue })` and `toObservable(sig)` from `@angular/core/rxjs-interop`.
- Use `ChangeDetectionStrategy.OnPush` with signals, and `@if` / `@for` (with `track`) in templates.
- Expose `asReadonly()` from services so only the owner writes.

## Avoid
- Writing signals inside `computed`: it throws. Compute purely.
- Using `effect` to derive state into another signal: use `computed` or `linkedSignal` where available.
- Mutating objects held in a signal (`s().items.push(x)`): no notification. Replace with a new value via `update`.
- Calling `toSignal` outside an injection context: it errors. Call it in a field initializer or pass `{ injector }`.
- `toSignal` on an observable that can error without handling: reading throws. Add `catchError` upstream.
- Forgetting to call the signal in the template (`count` vs `count()`): you render the function.
- Reading signals in an `effect` you expect to be untracked: use `untracked(() => ...)` for reads that must not subscribe.

## Review
- [ ] State is immutable-updated and derived values use `computed`.
- [ ] `effect` is limited to side effects and not used to sync state.
- [ ] Services expose readonly signals.
- [ ] Observables crossing into signals have an initial value and error handling.
- [ ] Components are OnPush and templates call signals.
