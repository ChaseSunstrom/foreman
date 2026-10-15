---
name: preact
title: Preact
area: web
tags: [preact, signals, compat, vite, small, jsx]
detect: [dep:preact, dep:@preact/signals, dep:@preact/preset-vite, dep:preact-render-to-string]
related: [react, vite, testing-library]
---
Preact: a 3 kB React-compatible UI library, with preact/compat for ecosystem libraries and optional signals for state.

## Verify
- `npx tsc --noEmit`: JSX types resolve against preact, not react.
- `npx vitest run`: tests in jsdom or happy-dom.
- `npm run build`: bundle size and alias resolution (check the aliasing worked, not that two copies of the runtime shipped).
- `npx eslint .`: lint.

## Test first
Use `@testing-library/preact`.
```tsx
import { render, screen, fireEvent } from "@testing-library/preact";
import { Counter } from "./Counter";

test("increments", () => {
  render(<Counter />);
  fireEvent.click(screen.getByRole("button"));
  expect(screen.getByText("1")).toBeInTheDocument();
});
```

## Do
- Set `"jsx": "react-jsx"` and `"jsxImportSource": "preact"` in `tsconfig.json`; with Vite use `@preact/preset-vite`.
- To use React-only libraries, alias `react` and `react-dom` to `preact/compat` (and `react/jsx-runtime` to `preact/jsx-runtime`) in the bundler and tsconfig `paths`.
- Use hooks from `preact/hooks`, or from `preact/compat` when sharing code with React.
- Use `@preact/signals` for fine-grained state: `signal`, `computed`, `effect`; render a signal directly in JSX (`{count}`) to update the text node without re-rendering.
- Use `class` or `className`; Preact accepts both.
- Use `onInput` for text inputs: Preact maps `onChange` to the native change event unless compat is in use.
- Use `preact-render-to-string` for SSR and `hydrate` on the client.
- Keep a single copy of preact in the lockfile (`npm ls preact`).

## Avoid
- Importing from `react` without the alias: two runtimes load, hooks break with "invalid hook call" style errors. Add the alias.
- Using `onChange` for live typing without compat: it fires on blur. Use `onInput`.
- Relying on React 18/19-only features (`use`, server components, concurrent transitions): not present. Use patterns Preact documents.
- Reading `signal.value` in a component, then expecting fine-grained updates: reading `.value` subscribes the whole component. Pass the signal itself into JSX for text updates.
- Mutating arrays or objects held in a signal in place: no notification. Assign a new value.
- Mixing `preact/compat` aliasing in some tools but not others (bundler vs test runner vs TypeScript): configure all three.

## Review
- [ ] Aliases and JSX settings agree across bundler, test runner and TypeScript.
- [ ] Only one preact copy is installed.
- [ ] Inputs use `onInput` where live updates matter.
- [ ] Signals are updated immutably and passed directly where text-only updates are wanted.
- [ ] Bundle size was checked after adding compat libraries.
