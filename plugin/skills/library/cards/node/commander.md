---
name: commander
title: Commander.js
area: node
tags: [commander, cli, arguments, options, subcommands, node]
detect: [dep:commander]
related: [oclif, ink, node, vitest, npm-publishing]
---
Commander CLIs: declared options and arguments, subcommands with actions, correct exit codes, testable parse.

## Verify
- `node bin/cli.js --help`: help text lists every command and option as intended.
- `node bin/cli.js nope; echo $?`: unknown command prints an error and exits non-zero.
- `npx tsc --noEmit`: typed option objects (or `@commander-js/extra-typings`) compile.
- `npx vitest run`: tests call `program.parseAsync(argv, { from: 'user' })` with exit overridden.

## Test first
Build the program in a factory so tests get a fresh instance.
```ts
import { makeProgram } from '../src/cli';

test('rejects a non-numeric --port', async () => {
  const p = makeProgram().exitOverride();
  p.configureOutput({ writeErr: () => {}, writeOut: () => {} });
  await expect(p.parseAsync(['serve', '--port', 'abc'], { from: 'user' }))
    .rejects.toMatchObject({ code: 'commander.invalidArgument' });
});
```

## Do
- Export a `makeProgram()` that returns a `new Command()`; call `.parse()` only in the bin file.
- Declare with `.option('-p, --port <n>', 'port', parseIntStrict, 3000)`, `.requiredOption`, `.argument('<file>')`, `.choices` via `new Option(...).choices([...])`.
- Use `parseAsync` when any action is async, and `await` it in the bin file.
- Write validators that throw `InvalidArgumentError`; commander prints a clean message.
- Define subcommands with `.command('name').description(...).action(...)`; use `.addHelpText` for examples.
- In actions the signature is `(args..., options, command)`; read global options with `command.optsWithGlobals()`.
- Set exit codes with `process.exitCode = 1` and let the process drain; send errors to stderr and data to stdout.
- Add `#!/usr/bin/env node` and a `bin` entry; ensure the file is executable in the package.

## Avoid
- `.parse()` with async actions: rejections go unhandled. Use `parseAsync`.
- Option names in camelCase when the flag is kebab: `--dry-run` becomes `opts.dryRun`.
- `parseInt` directly as the option parser: commander passes the previous value as the second argument, which becomes the radix. Wrap it.
- Calling `process.exit()` inside actions: breaks tests and truncates output. Throw or set `exitCode`.
- Mutating a shared module-level `program` across tests: state leaks. Use a factory.
- Boolean flags with defaults of `true` and no `--no-` form: unreachable. Define `--no-color` style options.

## Review
- [ ] Help output and error messages were read, not assumed.
- [ ] Bad input produces a non-zero exit and a stderr message.
- [ ] Async actions run through `parseAsync`.
- [ ] Program built by a factory and covered by tests.
- [ ] `bin` entry, shebang and file mode are right.
