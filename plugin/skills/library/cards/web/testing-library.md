---
name: testing-library
title: Testing Library
area: web
tags: [testing-library, testing, dom, accessibility, react, vue]
detect: [dep:@testing-library/react, dep:@testing-library/vue, dep:@testing-library/dom, dep:@testing-library/svelte, dep:@testing-library/user-event]
related: [react, vue, svelte, msw, playwright, vitest]
---
Testing Library: render a component, query it like a user would (roles, labels, text), and assert on what is visible.

## Verify
- `npx vitest run` (or `npx jest`): the suite passes.
- `npx eslint . --max-warnings 0`: with `eslint-plugin-testing-library` and `eslint-plugin-jest-dom`.
- `npx vitest run --coverage`: behaviors, not lines, are covered (when a coverage provider is installed).

## Test first
Render, act with `user-event`, assert on accessible output.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "./LoginForm";

test("shows an error for a missing password", async () => {
  const user = userEvent.setup();
  render(<LoginForm />);
  await user.type(screen.getByLabelText(/email/i), "a@b.co");
  await user.click(screen.getByRole("button", { name: /log in/i }));
  expect(await screen.findByRole("alert")).toHaveTextContent(/password/i);
});
```

## Do
- Query in this order: `getByRole` (with `name`), `getByLabelText`, `getByPlaceholderText`, `getByText`, then `getByTestId`.
- Use `getBy` for present, `queryBy` for asserting absence, `findBy` for async appearance.
- Create `const user = userEvent.setup()` and `await` every `user.*` call.
- Assert with `jest-dom` matchers: `toBeInTheDocument`, `toBeDisabled`, `toHaveAccessibleName`.
- Use `waitFor` only for assertions; keep one assertion inside.
- Wrap in a custom `render` that supplies providers (router, store, query client) and a fresh state per test.
- Mock the network with MSW rather than mocking `fetch` or hooks.
- Use `within(region)` to scope queries.
- Use `screen.debug()` or `logRoles` locally to find the right query; delete it after.

## Avoid
- Querying by class, tag or `container.querySelector`: couples to markup. Use roles and labels.
- `fireEvent` for user interactions: skips focus, hover and typing events. Use `user-event`.
- `getBy*` to assert absence (it throws): use `queryBy*` with `not.toBeInTheDocument()`.
- Side effects or multiple assertions inside `waitFor`: repeats the side effect and slows failures. Put only the assertion in it.
- Wrapping calls in `act()` by hand: RTL already does it. If you see act warnings, you are missing an `await` or a `findBy`.
- Testing implementation (state values, hook internals, shallow rendering): breaks on refactors. Assert on output.
- Forgetting `await` on `findBy` and `user.*`: the test ends before the assertion runs.
- Asserting snapshots of whole trees: noisy approvals. Assert on specific content.

## Review
- [ ] Queries are role or label based, with `getByTestId` only where nothing else fits.
- [ ] Every async interaction and `findBy` is awaited.
- [ ] No implementation details are asserted.
- [ ] Network is mocked at the boundary and state is fresh per test.
- [ ] The testing-library ESLint plugin reports nothing.
