---
name: ink
title: Ink
area: node
tags: [ink, react, terminal, tui, cli, components]
detect: [dep:ink, dep:ink-testing-library]
related: [commander, oclif, vitest, jest, tsconfig]
---
Ink terminal UIs: React components for the CLI, input via hooks, clean exit and non-TTY fallbacks.

## Verify
- `npx tsc --noEmit`: JSX types compile (`"jsx": "react-jsx"` in tsconfig).
- `node dist/cli.js < /dev/null | cat`: runs without a TTY and does not crash or hang.
- `npx vitest run`: component tests via `ink-testing-library`.
- `node --input-type=module -e "import 'ink'"`: ESM resolves (Ink is ESM only).

## Test first
Render to a frame string and drive stdin.
```tsx
import React from 'react';
import { render } from 'ink-testing-library';
import { Counter } from '../src/Counter';

test('increments on space', async () => {
  const { lastFrame, stdin } = render(<Counter />);
  expect(lastFrame()).toContain('0');
  stdin.write(' ');
  await new Promise(r => setTimeout(r, 20));
  expect(lastFrame()).toContain('1');
});
```

## Do
- Use `<Box>` (flexbox via Yoga) and `<Text>`; all text must be inside `<Text>`.
- Read keys with `useInput((input, key) => ...)`; handle `key.escape`, `key.return`, arrows, `key.ctrl && input === 'c'` explicitly if `exitOnCtrlC` is false.
- Exit by calling `useApp().exit()`, and `await waitUntilExit()` from the object `render()` returns.
- Use `<Static>` for log lines that should print once above the live area.
- Check `useStdin().isRawModeSupported` (or `process.stdout.isTTY`) before enabling input; print plain output otherwise.
- Keep async work in `useEffect` with cleanup, and set state only while mounted.
- Size with `useStdout().stdout.columns` or `<Box width="100%">`; test narrow widths.
- Write package as ESM: `"type": "module"` and `.js` extensions in imports.

## Avoid
- Strings outside `<Text>`: runtime error "Text string must be rendered inside <Text>". Wrap them.
- `console.log` while Ink renders: it garbles the frame. Use `<Static>` or render the text.
- `useInput` without `isActive` gating on unfocused components: every component receives keys. Pass `{ isActive }`.
- `useInput` in non-TTY or CI: raw mode throws. Guard with `isRawModeSupported`.
- Timers or intervals without cleanup: the process never exits.
- `require('ink')` from CommonJS: fails. Convert to ESM or use dynamic `import()`.

## Review
- [ ] Non-interactive runs (pipe, CI) degrade to plain output.
- [ ] The process exits cleanly and with the right code.
- [ ] Input handlers are focus-gated and escape/quit keys exist.
- [ ] Effects clean up timers and listeners.
- [ ] ESM, JSX and tsconfig settings are consistent.
