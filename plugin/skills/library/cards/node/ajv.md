---
name: ajv
title: Ajv
area: node
tags: [ajv, json-schema, validation, formats, compile, security]
detect: [dep:ajv, dep:ajv-formats, dep:ajv-errors]
related: [typebox, zod, fastify, express]
---
Ajv JSON Schema validation: compile once, enable strict mode and formats, coerce deliberately, report errors safely.

## Verify
- `npx tsc --noEmit`: `JSONSchemaType<T>` or type guards compile against the schemas.
- `node -e "const A=require('ajv');new A({strict:true}).compile(require('./schema.json'));console.log('ok')"`: the schema itself compiles under strict mode.
- `npx vitest run`: valid and invalid sample documents per schema.
- `npm ls ajv`: one major version (frameworks like fastify and eslint bundle their own).

## Test first
Table-test valid and invalid documents, including unknown keys.
```ts
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import schema from '../schemas/user.json';

const ajv = addFormats(new Ajv({ allErrors: true }));
const validate = ajv.compile(schema);

test.each([
  [{ email: 'a@b.co', age: 3 }, true],
  [{ email: 'nope', age: 3 }, false],
  [{ email: 'a@b.co', age: 3, admin: true }, false], // additionalProperties: false
])('%j -> %s', (doc, ok) => { expect(validate(doc)).toBe(ok); });
```

## Do
- Create one `Ajv` instance per app; `compile` each schema once at startup and reuse the validate function.
- Keep `strict` on (default) so unknown keywords and typos fail at compile time.
- Add `ajv-formats` for `email`, `uuid`, `date-time`: without it, formats throw in strict mode.
- Set `additionalProperties: false` and `required` explicitly on object schemas.
- Use `validate.errors` right after a failed call, with `instancePath`, `keyword`, `message`; map them to an API error shape.
- Use `JSONSchemaType<T>` or a `validate` as type guard (`if (validate(x)) { x is T }`) for typing.
- Pick the draft entry point: default `ajv` is draft-07; use `ajv/dist/2019` or `ajv/dist/2020` for newer drafts.
- Use `coerceTypes` and `useDefaults` only for query strings and config, and know they mutate the data.

## Avoid
- Compiling inside a request handler: slow and memory-leaking cache. Compile at startup.
- `strict: false` to silence warnings: hides schema mistakes. Fix the schema or register the keyword with `ajv.addKeyword`.
- Reading `validate.errors` after a later call: it is overwritten per call. Copy it immediately.
- Compiling schemas that come from users: ReDoS via `pattern` and resource exhaustion. Restrict or avoid.
- `removeAdditional: true` as the main defense: it silently drops fields. Prefer rejecting.
- Echoing raw `errors` including `data` back to clients: leaks values. Return paths and messages only.

## Review
- [ ] Validators are compiled once and reused.
- [ ] Strict mode on, formats installed, objects closed with `additionalProperties`.
- [ ] Error output is mapped and does not echo submitted data.
- [ ] Tests cover valid, invalid and extra-property inputs.
- [ ] Only one Ajv major in the dependency tree.
