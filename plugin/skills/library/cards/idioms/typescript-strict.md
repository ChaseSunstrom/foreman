---
name: typescript-strict
title: TypeScript strict mode
area: idioms
tags: [typescript, strict, types, narrowing, generics, tsconfig]
detect: [file:tsconfig.json]
related: [typescript, javascript-async, eslint, vitest]
---
Strict TypeScript: all strict flags on, unknown at the edges, narrowing and discriminated unions in the middle.

## Verify
- `npx tsc --noEmit`: the project type checks with the repo's tsconfig.
- `npx tsc --noEmit --strict`: strict passes even if the config is loose (for a migration check).
- `npx eslint . --max-warnings 0`: lint, including type-aware rules when configured.
- `npm test`: runtime behavior is unchanged.

## Test first
Pin the type contract with a compile-time assertion plus a runtime check.
```ts
import { expect, expectTypeOf, test } from "vitest";
import { parseId } from "./id";

test("parseId returns a branded id or null", () => {
  expectTypeOf(parseId("a1")).toEqualTypeOf<string | null>();
  expect(parseId("")).toBeNull();
});
```
Use `// @ts-expect-error` to assert that bad usage fails to compile.

## Do
- Enable `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` and `noImplicitOverride`.
- Type external data as `unknown`, then validate (a schema library or a type guard) before use.
- Model states as discriminated unions with a literal `kind` field and check exhaustiveness with a `never` assignment.
- Use `satisfies` to check a value against a type without widening it.
- Use `as const` for literal tables and derive types from them with `typeof` and `keyof`.
- Prefer `readonly` arrays and properties for inputs, and `interface` or `type` for object shapes consistently.
- Use `import type` for type-only imports.

## Avoid
- `any`: it turns off checking for everything it touches. Use `unknown` and narrow.
- `as` casts on API data: they assert without checking. Validate, or use a type guard `x is T`.
- Non-null assertion `!` to silence an error: fix the null case. Use a guard or `??`.
- `enum` for simple string sets: it emits runtime code and has surprising numeric behavior. Use a string-literal union.
- `@ts-ignore`: it hides later errors too. Use `@ts-expect-error` with a reason, which fails when the error disappears.
- Optional chaining everywhere to dodge types: it hides a missing-state bug. Model the state explicitly.
- `Object.keys(o)` typed as `keyof T`: it returns `string[]`. Narrow deliberately.

## Review
- [ ] `tsc --noEmit` is clean and no new `any`, `!` or `@ts-ignore` appeared.
- [ ] Boundaries (HTTP, JSON, env, storage) validate unknown input.
- [ ] Unions are discriminated and `switch` statements are exhaustive.
- [ ] Public types are exported deliberately and not widened by inference.
- [ ] Tests cover the failure branch of each type guard.
