<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Text, time and money: encodings, time zones, amounts

Use when code reads or writes text from outside (files, HTTP, a database, a terminal), stores or compares
timestamps, schedules anything by the calendar, or handles prices, totals, tax or currency. Bugs here pass every
test written in one locale, one time zone and round numbers.

Built on library cards: `fm lib show unicode` (normalisation, graphemes), `fm lib show timezones` (UTC storage,
zone rules), `fm lib show time-in-tests` (freezing the clock), `fm lib show money` (minor units, rounding),
`fm lib show i18n` (formatting per locale).

## The procedure

1. **Name the boundary.** List every place text, a time or an amount crosses into or out of the program.
   Each crossing gets one explicit decision below; nothing relies on a platform default.
2. **Bytes: decode once at the edge, with a named encoding.** `open(p, encoding="utf-8")`, not the locale
   default; HTTP bodies by their declared charset; invalid input fails or uses `errors="replace"` on purpose.
   Pass: grep finds no `open(` on text without `encoding=` in the changed files.
3. **Text: normalise before comparing, hashing or using as a key** (NFC for storage, NFKC plus `casefold()`
   for identifiers and search). Length limits say what they count: bytes, code points or user-visible
   characters. Pass: a test feeds the composed and the decomposed spelling and gets one result.
4. **Time: store and compute instants in UTC; keep the zone name (`Europe/London`), not an offset (`+01:00`),
   for anything a human scheduled.** Convert to local time only to display or to apply calendar rules.
   Pass: no naive `datetime.now()` or `Date()` without a zone in the changed code.
5. **Calendar maths knows about DST.** "Tomorrow at 9" and "in 24 hours" differ twice a year; local times that
   don't exist (spring forward) or happen twice (fall back) need a stated rule. Pass: a test crosses a DST
   change with a frozen clock.
6. **Money: integers of minor units or a decimal type, never binary floats**, with the currency stored beside
   the amount. Round once, at a stated step, with a stated rule (half-even or half-up), and allocate splits so
   the parts sum to the whole. Pass: a test splits 100.00 three ways and the parts add back to 100.00.
7. **Format last, per locale**: digits, separators, currency symbol and date order come from the locale library,
   not string concatenation.

## Four facts to test against

Runs as is (Python 3.9+, stdlib only; `zoneinfo` needs the system time-zone database or the `tzdata` package).

```python
import unicodedata
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_EVEN
from zoneinfo import ZoneInfo

a, b = "café", "café"                      # same text, two code-point spellings
assert a != b and unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b)
assert len("👍🏽") == 2 and len("👍🏽".encode("utf-8")) == 8   # code points ≠ bytes ≠ what a reader sees
assert "é".encode("utf-8").decode("latin-1") == "Ã©"          # mojibake: right bytes, wrong decoder

lon = ZoneInfo("Europe/London")
start = datetime(2026, 3, 28, 12, 0, tzinfo=lon)                # the day before the clocks go forward
nxt = start + timedelta(days=1)                                 # wall-clock maths: 12:00 the next day...
assert nxt.hour == 12 and nxt.astimezone(timezone.utc) - start.astimezone(timezone.utc) == timedelta(hours=23)

assert 0.1 + 0.2 != 0.3 and round(2.675, 2) == 2.67             # floats can't hold cents
assert Decimal("2.675").quantize(Decimal("0.01"), ROUND_HALF_EVEN) == Decimal("2.68")
```
