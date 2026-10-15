---
name: typescript-generics
title: TypeScript generics
area: node
tags: [typescript, generics, constraints, inference, types, api-design]
detect: []
related: [typescript-advanced-types, tsconfig, zod, vitest]
---
TypeScript generics: constrain what you accept, let inference do the work, and prove the types with type-level tests.

## Verify
- `npx tsc --noEmit`: the typing compiles under the project's strict config.
- `npx tsc --noEmit --strict`: catches code that only passes under loose settings.
- `npx vitest run --typecheck`: runs `*.test-d.ts` type tests (vitest typecheck mode).
- `npx tsd`: type assertions for libraries that use tsd (only if configured).

## Test first
Write the type test so a wrong signature fails to compile.
```ts
import { expectTypeOf, test } from 'vitest';
import { pick } from '../src/pick';

test('pick narrows to the chosen keys', () => {
  const r = pick({ a: 1, b: 'x', c: true }, ['a', 'c']);
  expectTypeOf(r).toEqualTypeOf<{ a: number; c: boolean }>();
  // @ts-expect-error unknown key is rejected
  pick({ a: 1 }, ['z']);
});
```

## Do
- Constrain parameters: `<T extends object>`, `<K extends keyof T>`, `<T extends readonly unknown[]>`.
- Make type parameters appear in the arguments so they infer; if a parameter appears once, you probably do not need it.
- Use defaults (`<T = unknown>`) for optional explicitness, and `unknown` rather than `any` as the fallback.
- Use `const` type parameters (`<const T extends readonly string[]>`) to infer literal tuples without `as const` at call sites.
- Use overloads or conditional return types when the return depends on an argument; keep the implementation signature loose and tested.
- Prefer `NoInfer<T>` to stop a secondary argument from widening inference.
- Name parameters meaningfully when there are several (`TInput`, `TOutput`), single `T` is fine for one.
- Add `@ts-expect-error` cases for what must not compile.

## Avoid
- `any` to silence a generic error: it propagates silently. Add a constraint or a narrowing function.
- Type parameters used only in the return type: callers can assert anything. Derive it from inputs or take a schema.
- Casting inside the implementation without a comment and a test: the signature lies. Isolate the cast in one helper.
- Over-constraining (`T extends string` when `PropertyKey` suffices) or under-constraining (accessing `T["x"]` unconstrained).
- Generic classes where a function would do: extra surface and variance trouble.
- Relying on inference of `[]` or `{}` literals: widens to `never[]` or `{}`. Annotate the parameter type.

## Review
- [ ] Each type parameter is constrained and appears at least twice (input and output).
- [ ] Inference works at call sites with no explicit type arguments.
- [ ] Type-level tests cover a passing and a failing call.
- [ ] No `any` or unchecked casts leak through the public signature.
- [ ] Error messages for misuse are readable.
