---
name: typebox
title: TypeBox
area: node
tags: [typebox, json-schema, validation, typescript, fastify, static]
detect: [dep:@sinclair/typebox, dep:typebox]
related: [ajv, zod, fastify, typescript-advanced-types]
---
TypeBox: JSON Schema builders that infer TypeScript types, validated with Ajv or the built-in compiler.

## Verify
- `npx tsc --noEmit`: `Static<typeof Schema>` types resolve and match usage.
- `npx vitest run`: valid and invalid samples through the same validator the app uses.
- `node -e "console.log(JSON.stringify(require('@sinclair/typebox').Type.Object({a:require('@sinclair/typebox').Type.String()})))"`: schema emits plain JSON Schema.
- `npm ls @sinclair/typebox`: one copy; Fastify type providers need the same instance.

## Test first
Prove the schema and the inferred type agree.
```ts
import { Type, type Static } from '@sinclair/typebox';
import { Value } from '@sinclair/typebox/value';

const User = Type.Object({ id: Type.String({ format: 'uuid' }), age: Type.Integer({ minimum: 0 }) },
  { additionalProperties: false });
type User = Static<typeof User>;

test('rejects negative age and extra keys', () => {
  const ok: User = { id: '8d1b9c5e-1c9a-4f3e-9d6b-2f5f8a1b7c10', age: 4 };
  expect(Value.Check(User, { ...ok, age: -1 })).toBe(false);
  expect(Value.Check(User, { ...ok, extra: 1 })).toBe(false);
});
```

## Do
- Define the schema once and derive the type: `type T = Static<typeof S>`.
- Close objects with `{ additionalProperties: false }` for inputs from outside.
- Use `Type.Optional`, `Type.Union`, `Type.Literal`, `Type.Array`, `Type.Record`, `Type.Ref` with `Type.Recursive` for self-reference.
- Validate with `Value.Check` and list failures with `Value.Errors` for diagnostics, or compile with `TypeCompiler.Compile(S)` for hot paths.
- With Fastify use `@fastify/type-provider-typebox` so route schemas type handlers and validate in one step.
- With Ajv, register formats (`ajv-formats`) yourself; TypeBox schemas do not validate `format` by themselves in Ajv without it.
- Use `Value.Default`, `Value.Clean`, `Value.Convert` explicitly when you want defaults, stripping, or coercion; they are not automatic.
- Use `Type.Transform` with `Value.Decode` / `Value.Encode` for parsed types such as dates.

## Avoid
- Hand-writing a TypeScript interface next to the schema: they drift. Derive with `Static`.
- Assuming `Value.Check` coerces or strips: it only checks. Call `Convert` or `Clean` first when needed.
- Unregistered custom formats in the built-in checker: `format` strings fail. Register with `FormatRegistry.Set`.
- Using `Type.Any` or `Type.Unknown` as an escape hatch for inputs: skips validation.
- Mixing major versions of the package between app and plugins: schema symbols differ and checks fail. Dedupe.
- Trusting schema defaults on `Static` types: defaults are not applied unless you call `Value.Default`.

## Review
- [ ] One schema is the source for both runtime checks and types.
- [ ] Inbound objects are closed and formats are registered.
- [ ] Coercion, defaults and cleaning are explicit.
- [ ] Tests include an invalid and an extra-property case.
- [ ] Single package instance across the tree.
