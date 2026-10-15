---
name: date-fns
title: date-fns
area: node
tags: [date-fns, dates, time, timezones, formatting, parsing]
detect: [dep:date-fns, dep:date-fns-tz, dep:@date-fns/tz]
related: [i18next, vitest, jest, zod]
---
date-fns: pure date functions, explicit parsing formats, timezone-aware code with fake timers in tests.

## Verify
- `npx tsc --noEmit`: functions accept `Date | number | string` types as declared.
- `TZ=UTC npx vitest run && TZ=America/Los_Angeles npx vitest run`: results do not depend on the machine timezone.
- `grep -rn "new Date(\"" src`: string-parsed dates that depend on engine parsing rules.
- `grep -rn "YYYY\|DD" src`: moment-style tokens that mean something else in date-fns.

## Test first
Pin the clock and the timezone; assert across a DST boundary.
```ts
import { addDays, format } from 'date-fns';
import { vi, test, expect, afterEach } from 'vitest';

afterEach(() => vi.useRealTimers());

test('addDays keeps wall-clock time across DST', () => {
  vi.setSystemTime(new Date(2024, 2, 9, 12, 0)); // local time
  const d = addDays(new Date(), 1);
  expect(format(d, 'yyyy-MM-dd HH:mm')).toBe('2024-03-10 12:00');
});
```
Run it under `TZ=America/New_York`.

## Do
- Import per function: `import { format, parseISO } from 'date-fns'`.
- Use `parseISO` for ISO strings, `parse(str, 'yyyy-MM-dd', new Date())` for custom formats, and check `isValid(result)`.
- Use Unicode tokens: `yyyy` (year), `MM` (month), `dd` (day), `HH` (24h), `mm` (minutes), `ss`, `a`.
- Do date arithmetic with `add`, `sub`, `addDays`, `differenceInCalendarDays`, `startOfDay`, `endOfMonth`, `isBefore`.
- Store and transmit UTC instants (ISO strings with `Z` or epoch ms); convert only for display.
- For zones use `@date-fns/tz` (`TZDate`, `tz()` as the `in` option) or `date-fns-tz` (`formatInTimeZone`, `fromZonedTime`, `toZonedTime`).
- Localize with `import { de } from 'date-fns/locale'` and `format(d, 'PPP', { locale: de })`.
- Inject the clock (pass `now`) into functions so tests need no mocking.

## Avoid
- `YYYY` and `DD` tokens: they throw unless you opt in, because they mean week-year and day-of-year. Use `yyyy` and `dd`.
- `new Date('2024-03-10')` vs `new Date('2024-03-10T00:00')`: the first is UTC, the second local. Parse explicitly with `parseISO`.
- Adding `24 * 3600 * 1000` for "one day": wrong across DST. Use `addDays`.
- Forgetting `isValid`: an Invalid Date flows through and `format` throws RangeError.
- Calling `format(d, 'z')` for a zone name: date-fns itself is local-zone only; use a tz package.
- Importing all locales: bundle bloat. Import only needed ones.

## Review
- [ ] No moment-style tokens; formats are `yyyy-MM-dd` style.
- [ ] Inputs parsed with `parseISO` or `parse` and validated.
- [ ] Tests run in two timezones and cover a DST boundary.
- [ ] Persistence uses UTC; zones are applied at the edge.
- [ ] The current time is injected or faked in tests.
