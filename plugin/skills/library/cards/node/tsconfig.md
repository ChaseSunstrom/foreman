---
name: tsconfig
title: tsconfig and TypeScript compiler
area: node
tags: [typescript, tsconfig, compiler, strict, modules, types]
detect: [file:tsconfig.json, file:tsconfig.*.json, dep:typescript]
related: [node, vite, vitest, eslint, esbuild, rollup]
---
`tsconfig.json` for Node and library projects: strictness, module resolution, project references, declaration output.

## Verify
- `npx tsc --noEmit`: type-checks the project with no output.
- `npx tsc --showConfig`: the fully resolved config after `extends`.
- `npx tsc --listFilesOnly | grep -v node_modules`: which source files are in the program (catches wrong `include`).
- `npx tsc -b`: builds the project-reference graph in dependency order.
- `npx tsc --noEmit --traceResolution | grep "'pkg'"`: how a module specifier resolves, for import errors.

## Test first
The failing check is a type test: code that must not compile.
```ts
// src/ids.test-d.ts (or any file included in the program)
import type { UserId, OrderId } from './ids';
declare const u: UserId;
// @ts-expect-error branded ids must not be interchangeable
const o: OrderId = u;
```
`@ts-expect-error` itself errors if the line becomes valid, so `tsc --noEmit` fails first and passes once the types are right.

## Do
- Turn on `"strict": true`, plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` for new code.
- For Node ESM set `"module": "nodenext"` and `"moduleResolution": "nodenext"`; use `.js` extensions in relative imports.
- For bundled apps (Vite, esbuild) use `"moduleResolution": "bundler"` with `"module": "esnext"`.
- Set `target` to the runtime (for example `es2022`) and `lib` to match it.
- Use `"isolatedModules": true` (or `verbatimModuleSyntax`) when a transpiler like esbuild or SWC emits the code; write `import type` for types.
- Use `"declaration": true`, `"declarationMap": true` and `outDir` for libraries; set `"skipLibCheck": true` for speed.
- Split configs: `tsconfig.base.json` shared, `tsconfig.json` for the editor and tests, `tsconfig.build.json` excluding tests.
- Use project references with `composite: true` in monorepos and run `tsc -b`.

## Avoid
- `"strict": false` or `any` to silence errors: bugs ship. Fix the type or narrow with a guard.
- `"moduleResolution": "node"` (node10) for modern ESM or `exports` packages: types are not found. Use `nodenext` or `bundler`.
- `paths` aliases without a matching runtime resolver: compiles but fails at run time. Mirror them in the bundler, Node loader or `tsx` setup.
- Relying on the compiler to emit under Vite/esbuild: they strip types without checking. Run `tsc --noEmit` in CI.
- `include` omitted or too broad: picks up `dist` or tests into the build. Set `include` and `exclude`.
- `esModuleInterop` mismatches that make `import x from 'cjs-pkg'` fail: set it consistently or use `module: nodenext` semantics.
- Mixing `types` arrays carelessly: `"types": []` hides `@types/node` and `@types/jest` globals. List what you need.

## Review
- [ ] `strict` is on and no blanket `any`.
- [ ] `module`/`moduleResolution` match the runtime or bundler.
- [ ] CI runs `tsc --noEmit` apart from the build tool.
- [ ] Build config excludes tests; `outDir` is outside `include`.
- [ ] Alias `paths` are mirrored at runtime.
