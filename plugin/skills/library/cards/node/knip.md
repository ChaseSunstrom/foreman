---
name: knip
title: Knip
area: node
tags: [knip, dead-code, unused-exports, dependencies, lint, typescript]
detect: [dep:knip]
related: [tsconfig, eslint, vitest, pnpm, node]
---
Knip finds unused files, dependencies, exports and class members in a JavaScript or TypeScript project; it reports and does not change code.

## Verify
- `./node_modules/.bin/knip`: the project's own install runs; exit code 1 means issues were reported, 0 means clean.
- `./node_modules/.bin/knip --production`: only production entry points count, so test-only code is not hiding unused exports.
- `grep -rn "knip" package.json`: the script or devDependency is wired in, so CI runs the same check.
- `./node_modules/.bin/knip --help`: the installed version prints its flags; check them before relying on one.

## Test first
Knip is a static report, so the test is a fixture: an orphan file must show up in the output.
```ts
import { spawnSync } from 'node:child_process';
import { writeFileSync, rmSync } from 'node:fs';
import { test, expect } from 'vitest';

test('a file nothing imports is reported as unused', () => {
  writeFileSync('src/orphan.ts', 'export const unused = 1;\n');
  try {
    const out = spawnSync('./node_modules/.bin/knip', { encoding: 'utf8' }).stdout;
    expect(out).toContain('src/orphan.ts');
  } finally {
    rmSync('src/orphan.ts', { force: true });
  }
});
```

## Do
- Keep the config in one file (`knip.json`, `knip.jsonc`, or `knip.ts` at the root) and commit it.
- Declare real entry points (`entry`) for scripts, configs and generated code that nothing imports directly.
- Run it in CI with the other static checks, and fail the build on its exit code.
- Fix findings in the order: unused files, then dependencies, then exports.
- Check each dependency finding with `grep` before removing it: a tool may load it by name from a config.
- Use `ignoreDependencies` or `ignore` with a comment saying why.

## Avoid
- Deleting every flagged export of a published library: consumers import them from outside the repo. Mark public entry files instead.
- Trusting a dependency finding for a CLI or plugin loaded by string (in a config or script): knip cannot see every dynamic load. Add it to `ignoreDependencies` with a reason.
- Running it once and never in CI: the findings come back.
- Ignoring a whole directory to silence one file: list the file.
- Running it in a repo with no installed dependencies: the import graph is missing, and results are noise. Install first.
- Calling a registry-fetching runner in scripts that run offline: it may try the network. Call the local install path.

## Review
- [ ] The check runs in CI and fails on its exit code.
- [ ] Entry points cover scripts, configs and generated files.
- [ ] Each ignore has a reason next to it.
- [ ] Public API exports are kept on purpose, not deleted by the report.
- [ ] A removed dependency is confirmed unused by grep and by a test run.
