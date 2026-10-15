---
name: error-boundaries
title: Error boundaries
area: frontend
tags: [react, errors, resilience, recovery, monitoring]
detect: [dep:react-error-boundary]
related: [code-splitting, hydration, optimistic-ui, toasts]
---
Contain render failures to a section with a useful fallback, a reset path and error reporting.

## Verify
- `npx vitest run`: a throwing child renders the fallback and reset recovers it.
- `npx playwright test`: forces an API or chunk failure and asserts the page stays usable.
- `npx tsc --noEmit`: fallback props and `onError` signatures.

## Test first
```ts
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ErrorBoundary } from 'react-error-boundary';
import { vi, test, expect } from 'vitest';

let fail = true;
const Bomb = () => { if (fail) throw new Error('boom'); return <p>ok</p>; };

test('fallback shows and retry recovers', async () => {
  vi.spyOn(console, 'error').mockImplementation(() => {});
  render(
    <ErrorBoundary fallbackRender={({ resetErrorBoundary }) =>
      <button onClick={resetErrorBoundary}>Try again</button>}>
      <Bomb />
    </ErrorBoundary>);
  fail = false;
  await userEvent.click(screen.getByRole('button', { name: 'Try again' }));
  expect(screen.getByText('ok')).toBeInTheDocument();
});
```

## Do
- Place boundaries at route level plus around independent widgets (feed, chart, sidebar) so one failure does not blank the page.
- Give the fallback a human message, a retry button wired to reset, and a way out (home link).
- Reset on a changed input with `resetKeys` (route, query id) so navigation clears the error.
- Report from `onError` (or `componentDidCatch`) with the component stack to the monitoring service.
- Pair with Suspense for lazy chunks: catch the load failure and offer reload.
- Give the fallback `role="alert"` and move focus to it if the whole view failed.
- Handle event-handler and async errors yourself (`try/catch`, query error states) and forward to a boundary with state when needed (`useErrorBoundary`).
- Keep the fallback small and dependency-free so it cannot itself throw.

## Avoid
- One boundary at the app root only: any error blanks everything. Add section boundaries.
- Expecting boundaries to catch event handlers, async callbacks, timers or SSR: they do not. Catch those explicitly.
- A fallback that is just "Something went wrong": no recovery. Add retry, context and support info.
- Swallowing the error with no reporting: failures become invisible. Log in `onError`.
- Resetting without clearing the cause (same bad props): instant re-throw loop. Reset with new keys or refetch.
- Showing stack traces or internal messages to users: leak. Show a generic message, log details.
- A fallback that depends on the failed provider or store: it throws too. Keep it self-contained.

## Review
- [ ] Boundaries exist at route and widget level.
- [ ] Fallbacks offer retry and reset on navigation.
- [ ] Errors reach monitoring with component stacks.
- [ ] Async and event errors have explicit handling.
- [ ] Tests cover a throw, the fallback and recovery.
