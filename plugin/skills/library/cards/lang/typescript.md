---
name: typescript
title: TypeScript
area: lang
tags: [typescript, tsc, eslint, vitest, strict, types]
detect: [ext:.ts, ext:.tsx, file:tsconfig.json, dep:typescript]
related: [javascript, nodejs, vitest, eslint, react]
---
TypeScript baseline: strict tsconfig, tsc as the type gate, eslint, a real test runner, and types narrowed at the boundaries.

## Verify
- `npx tsc --noEmit`: the whole project type-checks (bundlers often skip this).
- `npx eslint .`: lint, including type-aware rules if configured.
- `npm test`: the project's runner (vitest, jest or node:test).
- `npx tsc --showConfig`: the effective config, to confirm `strict` is on.

## Test first
Vitest or Jest, files `*.test.ts` beside the source or in `test/`. Test the failing input, not only the happy path.
```ts
import { describe, expect, it } from "vitest";
import { parseId } from "./parseId";

describe("parseId", () => {
  it("rejects non-numeric input", () => {
    expect(() => parseId("abc")).toThrow(/invalid/i);
  });
});
```

## Do
- Enable `"strict": true`; add `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` for new code.
- Validate external data (JSON, env, request bodies) with a schema library such as zod, then infer the type from it.
- Use discriminated unions and exhaustive `switch` with a `never` check instead of flags and optional fields.
- Use `unknown` for untrusted values and narrow it; use `satisfies` to check a literal without widening it.
- Use `import type` for type-only imports; keep `module` and `moduleResolution` consistent with the runtime (`NodeNext` for Node ESM).
- Export explicit return types on public functions.

## Avoid
- `any` and `as` casts to silence errors: the bug moves to runtime. Narrow with a guard or schema.
- `JSON.parse(x) as Foo`: no validation happens. Parse with a schema.
- Non-null `!` on values that can really be missing: throws later. Handle the null case.
- `enum` where a union of string literals suffices: runtime code plus quirks (numeric reverse maps). Use `as const` objects or unions.
- `// @ts-ignore`: hides all errors on the line. Use `@ts-expect-error` with a reason so it fails when fixed.
- Relative imports without extensions under `NodeNext`: runtime resolution fails. Write `./x.js`.
- `{}` or `Object` as a type: matches almost everything. Use `Record<string, unknown>` or a real shape.

## Review
- [ ] `tsc --noEmit` is clean with no new `any`, `@ts-ignore` or unexplained casts.
- [ ] Every boundary (HTTP, storage, env) is validated, not cast.
- [ ] Unions are exhaustively handled.
- [ ] Public API types are explicit and exported types did not change by accident.
- [ ] Tests cover an error path and run in CI.
