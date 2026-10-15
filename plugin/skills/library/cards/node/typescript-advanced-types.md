---
name: typescript-advanced-types
title: TypeScript advanced types
area: node
tags: [typescript, conditional-types, mapped-types, template-literals, discriminated-unions, satisfies]
detect: []
related: [typescript-generics, tsconfig, zod, typebox]
---
Advanced TypeScript types: discriminated unions, mapped and conditional types, template literals, satisfies, exhaustive checks.

## Verify
- `npx tsc --noEmit`: the types compile.
- `npx tsc --noEmit --noUncheckedIndexedAccess`: index access returns `T | undefined` as it does at runtime.
- `npx vitest run --typecheck`: runs `*.test-d.ts` assertions.
- `npx tsc --noEmit --extendedDiagnostics`: shows type instantiation counts when a type is slow.

## Test first
Assert the resulting type and that misuse fails.
```ts
import { expectTypeOf, test } from 'vitest';
import type { Handlers, Event } from '../src/events';

test('Handlers maps every event type to its payload', () => {
  expectTypeOf<Handlers['click']>().toEqualTypeOf<(e: { x: number }) => void>();
  // @ts-expect-error missing handler for 'key'
  const h: Handlers = { click: () => {} };
  expectTypeOf<Event>().toMatchTypeOf<{ type: string }>();
});
```

## Do
- Model state as a discriminated union with a literal tag (`{ status: 'ok'; data: T } | { status: 'err'; error: E }`) and narrow with `switch`.
- Finish `switch` with `const _x: never = value` (or `satisfies never`) for exhaustiveness.
- Use `satisfies` to check a literal against a type while keeping its narrow inferred type.
- Build mapped types with key remapping: `{ [K in keyof T as \`on${Capitalize<K & string>}\`]: (v: T[K]) => void }`.
- Use conditional types with `infer`: `T extends Promise<infer U> ? U : T`; wrap in `[T]` to prevent distribution when needed.
- Prefer built-ins: `Awaited`, `ReturnType`, `Parameters`, `Extract`, `Exclude`, `Omit`, `Pick`, `Readonly`, `NonNullable`, `Record`.
- Use `as const` for literal tables and derive unions with `typeof table[number]`.
- Brand ids with `string & { readonly __brand: 'UserId' }` and mint them in one function.

## Avoid
- `Omit` on a union: it collapses the members. Use a distributive helper (`T extends unknown ? Omit<T, K> : never`).
- Deeply recursive conditional types on large inputs: "type instantiation is excessively deep". Add a depth counter or simplify.
- Enums for string unions: runtime code and numeric pitfalls. Use `as const` objects or literal unions.
- `Function`, `{}` and `Object` as types: nearly everything matches. Use specific signatures and `Record<string, unknown>`.
- Type assertions (`as Foo`) to satisfy a union: runtime mismatch. Narrow with a guard or `in` check.
- Optional-chaining a discriminant instead of narrowing: loses the union relationship.

## Review
- [ ] Unions have a literal discriminant and exhaustive handling.
- [ ] No assertion hides a runtime-unchecked shape.
- [ ] Helper types have type-level tests for pass and fail cases.
- [ ] Type build time is acceptable (`--extendedDiagnostics`).
- [ ] Runtime validation (zod or typebox) backs types that come from outside.
