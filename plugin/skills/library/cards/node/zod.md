---
name: zod
title: Zod
area: node
tags: [zod, validation, schema, typescript, parsing, types]
detect: [dep:zod]
related: [trpc, hono, express, nestjs, vitest, tsconfig]
---
Zod schemas as the single source of runtime validation and static types at trust boundaries.

## Verify
- `npx tsc --noEmit`: inferred types line up where schemas are consumed.
- `npx vitest run`: schema tests pass, including failure cases.
- `npm ls zod`: one `zod` major in the tree (libraries that take schemas need the same one).

## Test first
Assert on `safeParse` results, both accept and reject.
```ts
import { it, expect } from 'vitest';
import { SignupSchema } from '../src/schemas';

it('rejects a short password and names the field', () => {
  const r = SignupSchema.safeParse({ email: 'a@x.io', password: 'abc' });
  expect(r.success).toBe(false);
  if (!r.success) expect(r.error.issues[0].path).toEqual(['password']);
});
```

## Do
- Define the schema once and derive the type: `type Signup = z.infer<typeof SignupSchema>`.
- Parse at every boundary: request bodies, env, webhooks, third-party API responses, `JSON.parse` output.
- Use `safeParse` to return a 4xx with `error.issues`; use `parse` only where a throw is correct.
- Parse env once: `const env = EnvSchema.parse(process.env)` at startup.
- Coerce strings from query or env explicitly with `z.coerce.number()`, with bounds (`.int().min(1).max(100)`).
- Use `z.object({...}).strict()` when extra keys must be rejected (default strips them).
- Model unions with `z.discriminatedUnion('type', [...])` for better errors and speed.
- Use `.refine`/`.superRefine` for cross-field rules, with a `path`.
- Use `z.input<>` for what callers send and `z.output<>` when transforms change the type.

## Avoid
- `z.coerce.boolean()` for env flags: any non-empty string, including `"false"`, becomes `true`. Use `z.enum(['true','false']).transform(v => v === 'true')`.
- Casting (`as Signup`) instead of parsing: no runtime check. Parse.
- Hand-writing a TypeScript interface that duplicates the schema: it drifts. Infer.
- Validating only on the client: servers must re-validate.
- `z.string()` for emails, URLs and ids with no format: use `.email()`, `.url()`, `.uuid()` (or v4 top-level helpers such as `z.email()`), plus `.max()`.
- Mixing zod v3 and v4 imports and APIs across packages: errors like missing `_def`. Align versions and check `error.format()` vs `z.treeifyError` per major.
- Exposing raw `ZodError` to clients with schema internals: map to a stable error shape.

## Review
- [ ] Every external input is parsed, not cast.
- [ ] Strings have length bounds; numbers have ranges.
- [ ] Env is validated at boot.
- [ ] Error responses use a stable shape.
- [ ] One zod major across the repo.
