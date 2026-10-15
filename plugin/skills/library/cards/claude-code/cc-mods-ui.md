---
name: cc-mods-ui
title: UI mods (function-hook plugins)
area: claude-code
tags: [claude-code, mods, ui, tsx, atoms, engine-api]
detect: [file:hooks/register.tsx]
related: [cc-mod-testing, cc-plugins, cc-plugin-manifest, cc-statusline]
---
A UI mod is a plugin whose `hooks/register.tsx` exports a `register(on, options)` function that handles engine events and renders TSX; the manifest `types` field points at its `.d.ts`.

## Verify
- `claude plugin test <mod-dir>`: runs the mod's test files against the engine harness.
- `claude plugin validate <mod-dir>`: manifest and paths.
- `npx tsc --noEmit -p <mod-dir>`: types against the engine declaration file (when a `tsconfig.json` is present).
- `grep -n "export declare" <mod-dir>/.claude-plugin/types/claude-code/index.d.ts | head`: the real API surface to code against.

## Test first
Test pure functions directly and the event flow through the harness (see the mod-testing card).
```tsx
import { expect, test } from 'claude-code/testing'
import { toasts } from '../hooks/register'
test('no toast on the first snapshot', () => { expect(toasts(null, VIEW)).toEqual([]) })
```

## Do
- Shape: `export const register: Register = (on, options) => { on('session.start', async ($, e, next) => { ...; return next(e) }) }`; `userConfig` values arrive as `options`.
- Always call `next(e)` (or return its result) so other handlers in the chain run.
- Hold shared state in atoms: `atom({ plugin: 'name', key: 'view' } as const, initial)`; change them with `update($, atom, fn)` and read with `read($, atom)`.
- Register slash commands with `$.command.register({ name, description })` and handle them with `on('command.run', { command: 'name' }, ...)`.
- Poll with `$.clock.every(ms, fn)` and cancel the previous timer on restart; persist small values with `$.store`.
- Render with the engine's `Box` and `Text` components and give each element a stable `key`.
- Export pure helpers (formatting, diffing, view logic) so they unit test without the engine.
- Validate untyped input (`typeof e.cwd === 'string'`) before using it.

## Avoid
- Forgetting `next(e)`: later handlers and the default behavior silently stop.
- Several pollers after repeated `session.start`: cancel the old timer first.
- Inline heavy work in render: it runs often. Compute in handlers, store in atoms.
- Writing files or state from a tool-call path without a deliberate guard: use typed commands for privileged actions.
- Coding against remembered API names: read the `.d.ts`; unknown members compile only against a wrong type file.
- Unkeyed list children: the pane flickers or loses state. Add `key`.

## Review
- [ ] Every handler returns `next(e)`.
- [ ] Atoms are namespaced by plugin.
- [ ] Timers are cancelled on restart.
- [ ] Pure helpers are exported and tested.
- [ ] `claude plugin test` is green.
