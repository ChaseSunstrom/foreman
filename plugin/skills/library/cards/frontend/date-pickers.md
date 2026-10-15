---
name: date-pickers
title: Date pickers
area: frontend
tags: [dates, forms, a11y, timezone, input]
detect: [dep:react-day-picker]
related: [forms, i18n, aria-patterns, keyboard-navigation]
---
Prefer native date inputs; when a custom calendar is required, handle keyboard, locale and time zones correctly.

## Verify
- `npx playwright test`: fills the input, uses the calendar by keyboard, checks the submitted value.
- `TZ=Pacific/Kiritimati npx vitest run`: date logic holds in an extreme time zone.
- `TZ=America/Los_Angeles npx vitest run`: same suite in a negative offset.

## Test first
A date-only value must not shift with the time zone.
```ts
import { expect, test } from 'vitest';
import { toIsoDate } from './dates';

test('date-only values round-trip without a day shift', () => {
  const d = new Date(2026, 2, 1); // local midnight, 1 March 2026
  expect(toIsoDate(d)).toBe('2026-03-01');
});
// toIsoDate = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
// Run under several TZ values; toISOString().slice(0,10) fails this in some of them.
```

## Do
- Start with `<input type="date">`, with `min`, `max`, `required` and a visible `<label>`. It gives locale, keyboard and mobile pickers free.
- For a custom calendar use a `role="grid"` of day buttons with roving tabindex: arrows by day and week, PageUp or PageDown by month, Home and End by week bounds, Enter or Space selects, Escape closes.
- Allow typing as well as picking; parse with a stated format and show the format as a hint (`aria-describedby`).
- Store date-only values as `YYYY-MM-DD` strings, never as midnight UTC timestamps. Store instants as ISO with offset or UTC.
- Format with `Intl.DateTimeFormat(locale, { timeZone })`; take the first day of week from locale.
- Mark disabled dates with `aria-disabled` and explain why; keep today visually and programmatically identifiable (`aria-current="date"`).
- Announce the visible month and year when navigating (live region or labelled heading).
- Return focus to the input after selection closes the popover.

## Avoid
- `new Date('2026-03-01')` for a local date: it parses as UTC and shows the previous day west of Greenwich. Build with parts or a date library.
- `toISOString().slice(0, 10)` on a local date: shifts across midnight in non-UTC zones. Format local parts.
- Day-of-month math with `setDate` across DST using 24-hour millisecond adds: use calendar arithmetic.
- Click-only calendars with `div` cells: no keyboard. Use buttons in a grid.
- Hardcoding `MM/DD/YYYY`: ambiguous globally. Use locale formatting or ISO.
- Range pickers that allow end before start with no message: validate and explain.

## Review
- [ ] Native input used unless a requirement rules it out.
- [ ] Date-only and instant values are stored differently and tested across time zones.
- [ ] Calendar is fully keyboard operable with labelled controls.
- [ ] Format hint and error text are associated with the input.
- [ ] Locale and first weekday come from the user, not hardcoded.
