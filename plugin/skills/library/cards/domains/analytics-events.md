---
name: analytics-events
title: Product analytics events
area: domains
tags: [analytics, events, tracking, schema, privacy, funnels]
detect: [dep:posthog-js, dep:posthog, dep:@segment/analytics-node]
related: [gdpr, ab-testing, webhooks, timezones]
---
Event tracking: a typed event schema, stable identity, dedupe by event id, consent gating, and server-side truth for money events.

## Verify
- `pytest -q tests/test_events.py`: schema validation and dedupe tests pass.
- `npx tsc --noEmit`: event names and properties type-check at call sites.
- `grep -rnE "track\(['\"]" src`: raw string event names that bypass the typed catalog (should be empty).

## Test first
A retried delivery must not double count.
```python
from app.events import ingest

def test_same_event_id_is_counted_once(db):
    e = {"id": "evt_1", "name": "checkout_completed", "user_id": "u1",
         "ts": "2026-03-08T01:59:59Z", "props": {"value_cents": 1999}}
    ingest(db, e); ingest(db, e)
    assert db.count("events", name="checkout_completed") == 1

def test_unknown_event_name_is_rejected(db):
    with pytest.raises(ValueError):
        ingest(db, {"id": "evt_2", "name": "Checkout Completed!"})
```

## Do
- Keep one catalog: snake_case `object_action` names, a typed props schema each, an owner and a version.
- Every event carries a client-generated id, UTC timestamp, anonymous id and, after login, user id; alias once at login.
- Store raw events append-only; derive sessions, funnels and cohorts downstream.
- Send revenue and state-change events from the server, not the browser.
- Gate non-essential tracking on consent; support delete-by-user.
- Drop or hash PII in properties; allowlist property keys.
- Batch and retry client sends with the same event id; use `sendBeacon` on unload.

## Avoid
- Free-text event names (`Clicked Buy`, `clicked_buy`): two series. Enforce the catalog in types.
- Counting from client timestamps alone: clocks drift. Record received time too and bucket by it.
- Tracking only in the browser: ad blockers drop 10 to 30 percent. Mirror critical events server-side.
- Unbounded property cardinality (full URLs, ids as keys): the warehouse explodes. Bucket or hash.
- Re-identifying users per page: merges identities wrongly. Alias once.
- Schema changes that rename in place: dashboards break. Version and dual-write.

## Review
- [ ] New events exist in the catalog with typed props.
- [ ] Event ids make ingestion idempotent.
- [ ] Consent and deletion paths are covered.
- [ ] No PII in properties.
- [ ] Money and signup events are server-emitted.
