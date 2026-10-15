---
name: bookings
title: Bookings and scheduling
area: domains
tags: [bookings, scheduling, availability, timezones, double-booking, slots]
detect: []
related: [timezones, calendar-ical, inventory, notifications-system]
---
Appointment and reservation systems: time-range overlap, DB-enforced no double booking, DST-safe recurrence, and local-time display.

## Verify
- `pytest -q tests/test_bookings.py`: overlap, DST and concurrency tests pass.
- `psql "$DATABASE_URL" -c "\d bookings"`: an exclusion constraint on the time range exists (Postgres).
- `pytest -q -k "dst or concurrent"`: the two nastiest cases pass.

## Test first
A weekly 09:00 slot must stay 09:00 local across the spring DST change.
```python
from datetime import datetime
from zoneinfo import ZoneInfo
from app.bookings import occurrences

def test_weekly_nine_am_stays_nine_am_across_dst():
    tz = ZoneInfo("America/New_York")
    start = datetime(2026, 3, 2, 9, 0, tzinfo=tz)
    got = occurrences(start, "WEEKLY", count=2, tz="America/New_York")
    assert got[1].astimezone(tz).hour == 9           # Mar 9, after the 8th shift
    assert got[1].utcoffset() != got[0].utcoffset()
```

## Do
- Store instants as UTC `tstzrange` plus the resource's IANA timezone; recurrence rules in local time.
- Use half-open ranges `[start, end)` so back-to-back bookings do not overlap.
- Enforce no overlap in the database: Postgres `EXCLUDE USING gist (resource_id WITH =, during WITH &&)` with `btree_gist`; elsewhere a unique slot row per resource and interval.
- Hold a slot briefly (pending with expiry) while payment completes, then confirm.
- Compute availability as working hours minus bookings minus buffers minus holidays, in the resource's timezone.
- Generate slots on demand from rules instead of materializing years.
- Make confirm and cancel idempotent; keep cancellation windows and refund rules as data.

## Avoid
- Check-then-insert for availability: two users win. Let the constraint reject and map the error to 409.
- Adding `timedelta(days=7)` to a UTC datetime for recurrence: drifts an hour at DST. Add in local time, then convert.
- Showing times in the server's timezone: render in the viewer's and name the zone.
- Treating nonexistent local times (spring gap) or repeated ones (fall) as valid: reject or resolve explicitly with `fold`.
- Closed intervals: the 10:00 end collides with the 10:00 start.
- Deleting canceled bookings: mark canceled, keep history.

## Review
- [ ] A DB-level constraint prevents overlap.
- [ ] Ranges are half-open, UTC, with the zone stored.
- [ ] DST gap and overlap days are tested.
- [ ] Holds expire.
- [ ] Emails and calendar invites show the local time with zone.
