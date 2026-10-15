---
name: svelte
title: Svelte
area: web
tags: [svelte, javascript, typescript, ui, runes, components]
detect: [dep:svelte, ext:.svelte]
related: [sveltekit, vitest, testing-library, playwright, tailwind]
---
Svelte 5 components with runes (`$state`, `$derived`, `$effect`, `$props`) and compile-time reactivity.

## Verify
- `npx svelte-check --tsconfig ./tsconfig.json`: component and template types, a11y warnings.
- `npx eslint . --max-warnings 0`: with `eslint-plugin-svelte`.
- `npx vitest run`: component tests with `@testing-library/svelte`.
- `npm run build`: production build.

## Test first
Render with Testing Library for Svelte in `*.test.ts`, then assert via roles.
```ts
import { render, screen } from "@testing-library/svelte";
import userEvent from "@testing-library/user-event";
import { expect, test } from "vitest";
import Counter from "./Counter.svelte";

test("increments", async () => {
  render(Counter);
  await userEvent.click(screen.getByRole("button"));
  expect(screen.getByText("1")).toBeInTheDocument();
});
```
Vitest needs the Svelte plugin and the `browser` resolve condition for component tests.

## Do
- Declare state with `let n = $state(0)`, derived with `$derived(n * 2)`, props with `let { a, b = 1 } = $props()`.
- Use `$effect` for side effects only and return a cleanup function from it.
- Use event attributes (`onclick={...}`) and snippets (`{#snippet}` with `{@render}`) in Svelte 5.
- Give `{#each items as item (item.id)}` a keyed block for reorderable lists.
- Share state across modules in `.svelte.ts` files using `$state` in exported objects.
- Use `bind:value` for form fields and `$bindable()` for props the child writes back.
- Fix svelte-check a11y warnings rather than silencing them.

## Avoid
- Svelte 4 syntax in a runes component: `export let`, `$:`, `on:click`, `<slot>`, `createEventDispatcher`. Use `$props`, `$derived`/`$effect`, `onclick`, snippets, callback props.
- `$effect` that sets state derived from other state: loops and extra runs. Use `$derived`.
- Exporting a reassigned `$state` primitive from a module: importers lose reactivity. Export an object, or getters and setters.
- Destructuring a `$state` object and expecting updates: you copy values. Read through the object.
- `{@html userInput}`: XSS. Sanitize or render as text.
- Unkeyed `{#each}` with inputs inside: values stick to the wrong row. Add a key.
- Mutating props that are not `$bindable`: warns and diverges.

## Review
- [ ] No Svelte 4 idioms remain in runes components.
- [ ] Every `$effect` is a real side effect and cleans up what it creates.
- [ ] Reorderable each-blocks are keyed.
- [ ] svelte-check passes with no suppressed a11y warnings.
- [ ] Tests assert user-visible output, not component internals.
