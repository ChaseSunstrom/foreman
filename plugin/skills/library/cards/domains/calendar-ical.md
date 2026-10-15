---
name: calendar-ical
title: Calendar and iCalendar
area: domains
tags: [ical, ics, rrule, timezones, calendar, invites]
detect: [dep:ical.js, dep:icalendar, dep:ics]
related: [bookings, timezones, notifications-system, email-sending]
---
Producing and consuming .ics: stable UIDs, TZID or UTC times, RRULE expansion in local time, line folding, and update sequencing.

## Verify
- `pytest -q tests/test_ical.py`: generation, parsing and recurrence tests pass.
- `python -c "from icalendar import Calendar; Calendar.from_ical(open('out.ics','rb').read())"`: the file parses (needs the icalendar package).
- `grep -c "^BEGIN:VEVENT" out.ics`: event count matches expectation.

## Test first
UID stability and update sequence decide whether clients update or duplicate.
```python
from app.ical import make_ics, parse

def test_reissue_keeps_uid_and_bumps_sequence_with_crlf_and_folding():
    a = make_ics(event_id="e1", title="x" * 120, start="2026-03-08T09:00", tz="America/New_York", seq=0)
    b = make_ics(event_id="e1", title="x" * 120, start="2026-03-08T10:00", tz="America/New_York", seq=1)
    ua, ub = parse(a)["uid"], parse(b)["uid"]
    assert ua == ub == "e1@example.com"
    assert parse(b)["sequence"] == 1
    assert "\r\n" in a and all(len(l) <= 75 for l in a.split("\r\n"))   # folded lines
```

## Do
- Give every event a permanent `UID` (id plus your domain), a `DTSTAMP`, and increment `SEQUENCE` on each change; set `METHOD:REQUEST` or `CANCEL` for invites.
- Write times either as UTC with `Z` or as local time with `TZID` and a matching `VTIMEZONE`; all-day events use `VALUE=DATE` with an exclusive end date.
- Use CRLF line endings, fold lines at 75 octets, and escape commas, semicolons, backslashes and newlines in text.
- Expand `RRULE` in the event's timezone so wall-clock time survives DST; apply `EXDATE`, and use `RECURRENCE-ID` for edited instances.
- Use a library (icalendar, ical.js, ics, rrule) to parse and expand; bound expansion with `COUNT` or an end window.
- Serve feeds as `text/calendar; charset=utf-8` with a private tokenized URL; add `REFRESH-INTERVAL` or `X-PUBLISHED-TTL` as hints.
- Send invites as an attachment with the right method, plus an "Add to calendar" link.
- Test imports from Google, Apple and Outlook exports; each has quirks.

## Avoid
- New UID on each export: clients duplicate events. Keep UIDs permanent.
- Floating local times without TZID: events shift per viewer. State the zone or use UTC.
- Adding 24 hours per day for recurrence: wrong across DST. Expand in local time.
- Unfolded long lines or bare LF: strict parsers reject. Use a library writer.
- Unescaped user text in SUMMARY or DESCRIPTION: broken files or injected properties. Escape.
- Unbounded RRULE expansion (`FREQ=DAILY` forever): memory blow-up. Cap the window.

## Review
- [ ] UID and SEQUENCE are stable and incremented on change.
- [ ] Time zones are explicit and tested across DST.
- [ ] Output parses with at least one independent parser.
- [ ] Text is escaped and folded.
- [ ] Recurrence expansion is bounded.
