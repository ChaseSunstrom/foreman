---
name: component-tests
title: Component tests
area: testing
tags: [testing, component, ui, react, vue, testing-library, rendering]
detect: [dep:@testing-library/react, dep:@testing-library/vue, dep:@testing-library/svelte, dep:@testing-library/dom, dep:@vue/test-utils, dep:@storybook/test]
related: [unit-test-design, snapshot-testing, accessibility-testing, http-mocking, e2e-strategy]
---
Component tests render one UI unit with real children and a faked network, then act and assert as a user would, through roles and text.

## Verify
- `npx vitest run` (or `npx jest`): the component suite passes in jsdom or happy-dom.
- `npx vitest run --coverage`: the branches in the component are exercised (needs a coverage provider).
- `npx tsc --noEmit`: props and event types still line up.
- `npx eslint . --ext .tsx`: Testing Library lint rules catch bad queries when `eslint-plugin-testing-library` is configured.

## Test first
Render, interact like a user, assert visible outcomes.
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("shows an error for an empty name", async () => {
  const user = userEvent.setup();
  render(<SignupForm onSubmit={jest.fn()} />);
  await user.click(screen.getByRole("button", { name: /sign up/i }));
  expect(await screen.findByRole("alert")).toHaveTextContent(/name is required/i);
});
```

## Do
- Query by role and accessible name first (`getByRole`), then label and text; use test ids only as a last resort.
- Drive input with `user-event` (typing, clicking, tabbing), not `fireEvent`, so focus and event order are realistic.
- Use `findBy*` and `waitFor` for async UI; use `queryBy*` to assert absence.
- Fake the network at the boundary (MSW or a stub fetch), not the child components.
- Wrap the component in the real providers it needs (router, store, theme) through a shared `renderWithProviders` helper.
- Test states: loading, empty, error, success, disabled, and long or odd content.
- Assert callbacks with the exact arguments the parent receives.
- Check keyboard operation and focus for interactive widgets.

## Avoid
- Asserting on state, class names or internal methods: tests break on refactor. Assert what a user sees.
- Shallow rendering that stubs every child: integration bugs hide. Render real children, stub only the network.
- `await new Promise(r => setTimeout(r, 500))`: slow and flaky. Use `findBy*` or `waitFor`.
- `getByTestId` everywhere: ignores accessibility. Use roles and labels.
- Snapshot of the whole tree as the only assertion: unreadable diffs approved blindly. Assert specific outcomes.
- Wrapping every assertion inside `waitFor` with side effects: retries repeat the action. Keep actions outside.

## Review
- [ ] Queries are role-first and accessible.
- [ ] Interactions use `user-event`; async uses `findBy` or `waitFor`.
- [ ] Network is faked; children are real.
- [ ] Loading, error and empty states are covered.
- [ ] No assertions on internals or class names.
