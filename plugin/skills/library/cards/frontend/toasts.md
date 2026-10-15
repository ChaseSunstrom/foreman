---
name: toasts
title: Toasts and notifications
area: frontend
tags: [toast, notifications, a11y, live-region, feedback]
detect: [dep:sonner]
related: [aria-patterns, optimistic-ui, dialogs, focus-management]
---
Transient feedback announced to assistive tech, pausable, dismissible and never the only record of an error.

## Verify
- `npx playwright test`: toast appears, is announced, pauses on hover and focus, dismisses.
- `npx @axe-core/cli http://localhost:3000`: region roles and names.
- `npx vitest run`: Testing Library finds `role="status"` text after the action.

## Test first
```ts
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { App } from './App';

test('saving announces success in a status region', async () => {
  render(<App />);
  await userEvent.click(screen.getByRole('button', { name: 'Save' }));
  const status = await screen.findByRole('status');
  expect(status).toHaveTextContent('Saved');
  await userEvent.click(screen.getByRole('button', { name: 'Dismiss' }));
  expect(screen.queryByRole('status')).not.toBeInTheDocument();
});
```

## Do
- Mount one persistent container (`role="region"`, `aria-label="Notifications"`) with `aria-live="polite"`; use `role="alert"` for errors.
- Add messages to an existing live region after mount; the container must exist before the content.
- Keep text short and specific ("Project renamed"), and include an Undo action when the operation is reversible.
- Auto-dismiss only non-critical toasts, with 5 to 8 seconds minimum and more for longer text; pause on hover, focus and when the tab is hidden.
- Make every toast dismissible with a labelled button, and reachable by keyboard (a hotkey to jump to the region is a plus).
- Cap the visible stack (about 3), queue the rest, and dedupe identical messages by id.
- Respect `prefers-reduced-motion` for entrance animation.
- Position away from primary controls and above mobile browser chrome (`env(safe-area-inset-bottom)`).

## Avoid
- Errors that only show as a toast: they vanish before they are read. Put persistent field or banner errors in the page and use the toast as a bonus.
- Injecting a live region together with its text: it is not announced. Mount first, update after.
- Auto-dismissing toasts that hold an action: users cannot reach Undo. Keep them until acted on or longer.
- Stealing focus on every toast: it interrupts typing. Announce, do not focus.
- Toast spam for each item in a bulk action: send one summary.
- Color-only status: add an icon and text.
- Hover-only dismiss controls: unreachable by keyboard and touch.

## Review
- [ ] Live region exists before messages and uses the correct politeness.
- [ ] Toasts pause on hover and focus, and are dismissible by keyboard.
- [ ] Critical errors persist elsewhere on the page.
- [ ] Stack is capped and deduped.
- [ ] Actions inside toasts outlive their timer.
