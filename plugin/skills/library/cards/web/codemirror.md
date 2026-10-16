---
name: codemirror
title: CodeMirror 6
area: web
tags: [codemirror, editor, typescript, frontend, extensions, state]
detect: [dep:@codemirror/*, dep:codemirror, dep:@lezer/*, dep:@replit/codemirror-*]
related: [rich-text-editors, typescript, vitest, playwright, react]
---
CodeMirror 6: an immutable EditorState changed by transactions, an EditorView over it, and behaviour added as extensions.

## Verify
- `npm ls @codemirror/state @codemirror/view`: exactly one copy of each; two copies break extensions at runtime.
- `npx tsc --noEmit`: extensions, facets and commands type-check against the installed packages.
- `npx vitest run`: state logic (commands, StateFields, linters) tested on an EditorState, no DOM.
- `npx playwright test`: typing, completion and keymaps in a real browser.

## Test first
Most behaviour is state-only: build a state, apply a transaction, assert on the document or the field.
```ts
import { test, expect } from "vitest";
import { EditorState, EditorSelection } from "@codemirror/state";
import { wrapInBold } from "./commands";

test("wrapInBold surrounds the selection", () => {
  let state = EditorState.create({ doc: "hello", selection: EditorSelection.single(0, 5) });
  wrapInBold({ state, dispatch: (tr) => { state = tr.state; } });
  expect(state.doc.toString()).toBe("**hello**");
});
```

## Do
- Create once: `new EditorView({ state: EditorState.create({ doc, extensions }), parent })`, and `view.destroy()` on teardown.
- Change content through `view.dispatch({ changes: { from, to, insert } })`; never edit the DOM.
- Put settings that change at runtime (language, theme, read-only) in a `Compartment` and `reconfigure` it.
- Keep custom state in a `StateField` and derived decorations in a field or a `ViewPlugin`.
- Write commands as `(view) => boolean` (or `{ state, dispatch }`) and bind them with `keymap.of([...])`.
- Use the language packages (`@codemirror/lang-*`) with `@codemirror/language` for highlighting and folding.
- Add `linter(...)` from `@codemirror/lint` and `autocompletion(...)` from `@codemirror/autocomplete` as extensions.

## Avoid
- Two versions of `@codemirror/state` in the bundle ("Unrecognized extension value"): dedupe the packages.
- Recreating the view on every React render: lost undo history and cursor. Create in an effect, keep a ref.
- Replacing the whole state to update text: history and selection reset. Dispatch changes.
- Reading `view.state` captured earlier inside async code: it's stale. Read it again when you act.
- Mixing CodeMirror 5 examples (`CodeMirror.fromTextArea`, `cm.setValue`) into a 6 codebase: different API.
- Building large decoration sets on every update: slow typing. Map them through changes, rebuild only what moved.

## Review
- [ ] One view per editor, destroyed on teardown.
- [ ] All edits go through transactions.
- [ ] Runtime options live in compartments.
- [ ] `@codemirror/*` packages resolve to single copies.
- [ ] State logic has tests that need no DOM.
