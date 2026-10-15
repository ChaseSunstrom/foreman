---
name: cypress
title: Cypress
area: web
tags: [cypress, e2e, component-testing, browser-testing, javascript, ui]
detect: [dep:cypress, file:cypress.config.*]
related: [playwright, testing-library, msw]
---
Cypress: end-to-end and component tests run inside the browser, with retried commands and network stubbing via `cy.intercept`.

## Verify
- `npx cypress run`: all e2e specs headless.
- `npx cypress run --component`: component tests.
- `npx cypress verify`: the binary is installed and runnable.
- `npx tsc --noEmit -p cypress`: typed specs, when a `cypress/tsconfig.json` exists.

## Test first
Start with the visible behavior; alias the request you depend on and wait for it explicitly.
```ts
// cypress/e2e/todos.cy.ts
it("adds a todo", () => {
  cy.intercept("POST", "/api/todos").as("create");
  cy.visit("/");
  cy.findByPlaceholderText("What needs to be done?").type("buy milk{enter}");
  cy.wait("@create").its("response.statusCode").should("eq", 201);
  cy.contains("li", "buy milk").should("be.visible");
});
```
`findBy*` needs `@testing-library/cypress`; otherwise use `cy.contains` and `data-cy` attributes.

## Do
- Select by stable hooks: `data-cy`/`data-testid`, or Testing Library queries by role and label.
- Chain assertions with `.should()` so they retry; do not wrap them in `then`.
- Alias requests with `cy.intercept(...).as("x")` and sync on `cy.wait("@x")`.
- Seed state through the API or `cy.task` (`cy.request`), not by clicking through UI each test.
- Cache login with `cy.session(id, setup)`.
- Set `baseUrl` in `cypress.config.ts` and use relative `cy.visit("/")`.
- Reset state in `beforeEach`, not `afterEach`: the failing state stays inspectable.
- Keep tests independent so any spec can run alone.

## Avoid
- `cy.wait(2000)` fixed delays: flaky and slow. Wait on an alias or an assertion.
- Assigning command results to variables (`const el = cy.get(...)`): commands are async and queued. Use `.then` or aliases.
- Conditional testing on DOM state (`if (el.length)`): non-deterministic. Control the app state first.
- Visiting multiple origins in one test without `cy.origin`: blocked. Test the other origin separately or stub it.
- Long chains of UI login for each test: slow. Use `cy.session`.
- Testing third-party sites: out of your control. Stub them with `cy.intercept`.
- Relying on `.only` left in specs: skips everything else. Lint it out in CI.

## Review
- [ ] Selectors are stable and not tied to CSS classes or text that changes.
- [ ] Assertions retry and network waits use aliases, not sleeps.
- [ ] Each spec seeds its own state and runs independently.
- [ ] Login uses `cy.session` or an API call.
- [ ] No `.only` and no conditional DOM branching.
