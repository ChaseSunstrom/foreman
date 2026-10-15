---
name: timezones
title: Dates and Timezones
area: domains
tags: [timezone, dst, utc, datetime, scheduling, iana]
detect: [dep:luxon, dep:date-fns-tz, dep:dayjs, dep:moment-timezone, dep:@js-temporal/polyfill, dep:pytz, dep:tzdata, dep:arrow, dep:chrono-tz]
related: [cron-jobs, i18n, unicode, money]
---
Store instants in UTC, store zone names for human schedules, convert only at the edges, and test across DST.

## Verify
- `TZ=America/New_York date -d '2025-03-09 02:30'`: how the system handles a nonexistent DST local time.
- `python -c "from zoneinfo import ZoneInfo; from datetime import datetime; print(datetime(2025,11,2,1,30,tzinfo=ZoneInfo('America/New_York')).utcoffset())"`: ambiguous hour resolves via `fold`.
- `node -e "console.log(new Intl.DateTimeFormat('en',{timeZone:'Asia/Kolkata',timeStyle:'long'}).format(new Date()))"`: runtime tz data is present.
- `psql -c "select now(), current_setting('TIMEZONE')"`: server zone known; columns are `timestamptz`.

## Test first
Pin the clock and cross a DST boundary.
```python
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.schedule import next_daily

NY = ZoneInfo("America/New_York")

def test_daily_9am_stays_9am_across_spring_forward():
    start = datetime(2025, 3, 8, 9, 0, tzinfo=NY)
    nxt = next_daily(start)
    assert nxt.hour == 9 and nxt.day == 9
    assert nxt - start == timedelta(hours=23)
```

## Do
- Persist instants as UTC (`timestamptz`, ISO 8601 with `Z`, epoch); persist the user's IANA zone (`America/New_York`) separately.
- For future events at local time (meetings, alarms), store local datetime plus zone and resolve to UTC at fire time, since rules change.
- Do date math in the local zone with a real library (`zoneinfo`, Temporal, Luxon), then convert.
- Calendar dates with no time (birthdays, due dates) are plain dates; do not attach a zone.
- Inject a clock in code so tests control "now".
- Keep tzdata updated in containers (the `tzdata` package).
- Display with `Intl.DateTimeFormat` using the viewer's zone and an explicit `timeZoneName` where ambiguity matters.
- Test spring-forward (missing hour), fall-back (repeated hour), month end, leap day and zones with 30 or 45 minute offsets.

## Avoid
- Storing local time without a zone: unrecoverable. Use UTC plus zone.
- Fixed offsets (`-05:00`) as a zone: breaks at DST. Use IANA names.
- Adding `24 * 3600` seconds for "tomorrow": wrong on DST days. Add calendar days in the zone.
- `new Date('2025-03-09')`: parsed as UTC while `new Date('2025-03-09T00:00')` is local. Parse explicitly.
- Naive datetimes in Python (`datetime.now()`, `utcnow()`, deprecated): use `datetime.now(timezone.utc)` and aware objects.
- Abbreviations (`EST`, `CST`, `IST`): ambiguous. Use IANA ids.
- Midnight as "start of day": some zones skip it on DST. Use library `startOf('day')`.
- Comparing dates as strings across zones: normalize to instants first.

## Review
- [ ] All stored timestamps are UTC instants; user zone stored as an IANA name.
- [ ] No naive datetimes or fixed offsets in business logic.
- [ ] Recurring local-time events survive DST both ways.
- [ ] Clock is injectable; tests pin it.
- [ ] tzdata is current in every runtime image.
