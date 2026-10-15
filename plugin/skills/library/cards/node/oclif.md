---
name: oclif
title: oclif
area: node
tags: [oclif, cli, commands, plugins, flags, manifest]
detect: [dep:@oclif/core, dep:oclif]
related: [commander, ink, node, npm-publishing]
---
oclif CLIs: class-based commands with typed flags, manifest and README generation, testable `run`.

## Verify
- `npx tsc --noEmit`: command classes, `Flags` and `Args` types compile.
- `./bin/run.js --help`: help for the root and for each topic renders (use `./bin/dev.js` for TypeScript dev).
- `npx oclif manifest`: builds `oclif.manifest.json`, which proves every command loads.
- `npx oclif readme`: regenerates the README command docs; the diff should be intentional.

## Test first
Run commands in process with `runCommand` from `@oclif/test`.
```ts
import { runCommand } from '@oclif/test';

test('greet fails without a required name', async () => {
  const { error } = await runCommand(['greet']);
  expect(error?.oclif?.exit).toBe(2);
});

test('greet prints a greeting', async () => {
  const { stdout } = await runCommand(['greet', '--name', 'Ada']);
  expect(stdout).toContain('Hello, Ada');
});
```

## Do
- One class per file under `src/commands`, extending `Command`; nested folders become topics (`user create`).
- Define `static args = { file: Args.string({ required: true }) }` and `static flags = { force: Flags.boolean({ char: 'f' }) }`.
- Parse with `const { args, flags } = await this.parse(MyCommand)`; use `Flags.integer({ min, max })` or `parse` for validation.
- Output with `this.log` (stdout), `this.logToStderr`, `this.warn`; fail with `this.error(msg, { exit: 2 })`.
- Support `static enableJsonFlag = true` and return an object from `run()` for machine output.
- Add `static examples` and `static description`; the README and help come from them.
- Configure `oclif` in package.json: `bin`, `dirname`, `commands`, `topicSeparator`, and `plugins` (for example the help or autocomplete plugins).
- Ship `oclif.manifest.json` in `files` (generated in `prepack`) for fast startup.

## Avoid
- Calling `process.exit` in `run`: use `this.exit(code)` or `this.error`.
- Forgetting `static args`/`flags` and reading `process.argv`: no validation or help.
- ESM and CJS mismatch: match `"type"` and tsconfig `module` to the oclif template; wrong choice gives load errors from `bin/run.js`.
- Stale `oclif.manifest.json` committed: regenerate on pack, not by hand.
- Logging data with `console.log`: bypasses `--json` handling. Use `this.log` and return values.

## Review
- [ ] Every command has description, examples and typed flags/args.
- [ ] Errors use `this.error` with deliberate exit codes.
- [ ] `--json` output is stable and tested where enabled.
- [ ] Manifest and README regenerated, and `files` includes them.
- [ ] Tests use `runCommand`, not child processes, unless testing the bin.
