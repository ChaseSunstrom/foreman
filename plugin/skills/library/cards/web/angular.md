---
name: angular
title: Angular
area: web
tags: [angular, typescript, signals, rxjs, components, ui]
detect: [dep:@angular/core, file:angular.json]
related: [typescript, playwright, cypress, tailwind, sass]
---
Angular apps: standalone components, signals, dependency injection, typed reactive forms, RxJS at the edges.

## Verify
- `npx ng build`: AOT build catches template type errors.
- `npx ng test --watch=false`: unit tests (the configured runner).
- `npx ng lint`: lint, when a linter is configured.
- `npx tsc --noEmit -p tsconfig.app.json`: strict TypeScript.

## Test first
Test with `TestBed` in `*.spec.ts` beside the component; use `HttpTestingController` for HTTP.
```ts
import { TestBed } from "@angular/core/testing";
import { CounterComponent } from "./counter.component";

it("increments", () => {
  const f = TestBed.createComponent(CounterComponent);
  f.nativeElement.querySelector("button").click();
  f.detectChanges();
  expect(f.nativeElement.textContent).toContain("1");
});
```

## Do
- Write standalone components (`imports: [...]` in `@Component`) and `provideRouter`/`provideHttpClient` in `app.config.ts`.
- Use `signal`, `computed` and `effect` for local state; `input()`, `output()` and `model()` for component APIs.
- Use `inject(Service)` and `providedIn: "root"` services.
- Use built-in control flow (`@if`, `@for (x of xs; track x.id)`) in templates.
- Set `changeDetection: ChangeDetectionStrategy.OnPush`.
- Use typed reactive forms (`FormBuilder.nonNullable`), and the `async` pipe or `toSignal` for observables.
- Lazy-load routes with `loadComponent` or `loadChildren`.
- Enable `strict` and `strictTemplates`.

## Avoid
- NgModules, `*ngIf`/`*ngFor` and `@Input()` decorators in new code: use standalone, `@if`/`@for` and `input()`.
- Manual `subscribe` in components with no teardown: leaks. Use `async` pipe, `toSignal`, `takeUntilDestroyed()`.
- Nested subscribes: use `switchMap`/`concatMap`/`forkJoin`.
- Mutating objects held in OnPush inputs: no update. Replace with a new reference or use signals.
- `any` and `$any()` in templates to silence errors: fix the type.
- `@for` without `track`: compile error, and `track $index` on reorderable lists causes DOM churn. Track a stable id.
- `bypassSecurityTrustHtml` on user data: XSS. Sanitize or bind as text.
- Calling functions in templates that do real work: runs every change detection. Use `computed`.

## Review
- [ ] No unmanaged subscriptions remain.
- [ ] OnPush components get immutable or signal inputs.
- [ ] Forms are typed and validators live on the control.
- [ ] Routes are lazy where the feature is large.
- [ ] `ng build` passes under strict templates with no `any` added.
