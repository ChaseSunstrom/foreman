---
name: xterm
title: xterm.js
area: web
tags: [terminal, xterm, pty, frontend, typescript, addons]
detect: [dep:@xterm/*, dep:xterm, dep:xterm-addon-*]
related: [tauri, electron, websockets, vitest, playwright]
---
xterm.js: a terminal emulator for the browser, fed bytes from a pty and sized by an addon; @xterm/headless runs it without a DOM.

## Verify
- `npm ls @xterm/xterm xterm`: one terminal package; the scoped `@xterm/*` and old `xterm`/`xterm-addon-*` aren't mixed.
- `npx tsc --noEmit`: addons and the terminal agree on versions and types.
- `npx vitest run`: rendering logic checked against `@xterm/headless` buffers.
- `npx playwright test`: the terminal opens, fits its container and echoes input in a browser.

## Test first
Write to a headless terminal and read its buffer back.
```ts
import { test, expect } from "vitest";
import { Terminal } from "@xterm/headless";

test("the prompt lands on the first line", async () => {
  const term = new Terminal({ cols: 20, rows: 2 });
  await new Promise<void>((done) => term.write("$ ls\r\n", done));
  expect(term.buffer.active.getLine(0)?.translateToString(true)).toBe("$ ls");
});
```

## Do
- Import the stylesheet (`@xterm/xterm/css/xterm.css`); without it the terminal lays out wrongly.
- Create the terminal, `term.open(container)`, then load `FitAddon` and call `fit()` once the container has a size.
- Refit on container resize (a ResizeObserver), and send the new `cols` and `rows` to the pty from `term.onResize`.
- Send keystrokes with `term.onData(data => pty.write(data))`; write pty output with `term.write(data)`.
- Use the write callback (or batch output) for large streams so the UI keeps up.
- Call `term.dispose()` and stop the pty when the view unmounts.

## Avoid
- Calling `fit()` before `open()` or while the container is hidden: zero size. Fit after it is visible.
- Mixing `xterm` with `@xterm/*` packages: two copies and broken addons. Use the scoped packages throughout.
- Forgetting to resize the pty after a fit: wrapped, garbled output. Forward `onResize`.
- Writing megabytes in one call: a frozen tab. Chunk with the write callback.
- Echoing input locally as well as from the pty: doubled characters. Let the pty echo.

## Review
- [ ] One terminal package family is installed.
- [ ] The stylesheet is imported.
- [ ] Fit runs after open and on every resize, and the pty learns the size.
- [ ] Large output is flow-controlled.
- [ ] Terminal and pty are disposed together.
