---
name: notifications-system
title: Notifications system
area: domains
tags: [notifications, push, email, preferences, digests, queues]
detect: [dep:web-push, dep:@novu/node]
related: [email-sending, sms, chat-systems, webhooks, timezones]
---
Multi-channel notifications: events to per-user preferences to channel workers, deduped and rate-limited, with an in-app inbox as source of truth.

## Verify
- `pytest -q tests/test_notifications.py`: routing, preferences and dedupe tests pass.
- `pytest -q -k "quiet_hours or digest"`: time-sensitive rules pass.
- `grep -rn "send_email(\|send_push(" src | grep -v notifications/`: direct sends bypassing the pipeline (should be empty).

## Test first
Preferences and dedupe both gate delivery.
```python
from app.notify import notify

def test_opted_out_channel_skipped_and_duplicate_event_sent_once(db, outbox):
    db.prefs("u1", {"comment": {"email": False, "push": True}})
    notify(db, user="u1", kind="comment", key="c:42", payload={})
    notify(db, user="u1", kind="comment", key="c:42", payload={})
    assert [m.channel for m in outbox] == ["push"]
    assert db.inbox_count("u1") == 1
```

## Do
- Separate event, notification (per user, stored in the inbox) and delivery (per channel attempt with status).
- Dedupe on `(user, kind, key)`; use a stable key from the source entity, not a timestamp.
- Preference matrix per kind and channel, plus global mute and quiet hours in the user's timezone; transactional messages (security, receipts) bypass marketing opt-outs but stay logged.
- Deliver in workers with retries, backoff and a dead-letter queue; one channel failing must not block the others.
- Batch bursts into digests (same kind within a window); cap per-user rate.
- Handle push token lifecycle: register, rotate, and delete on invalid-token responses.
- Provide unsubscribe in every email and a one-click link; honor it immediately.
- Template with localization and per-channel length limits.
- Mark read state on the inbox record and sync across devices.

## Avoid
- Sending inline in the request that caused the event: slow and lossy. Enqueue.
- Fan-out to all followers synchronously: spikes. Chunk and queue.
- Keeping dead push tokens: wasted sends and provider penalties. Prune on error.
- Timestamps as dedupe keys: retries become new notifications. Use entity keys.
- Quiet hours computed in server time: wake users. Use the user's zone.
- Notifying the actor of their own action: filter self-events.

## Review
- [ ] Every send path goes through the pipeline.
- [ ] Preferences, quiet hours and unsubscribe are enforced and tested.
- [ ] Dedupe key is stable.
- [ ] Failures retry and eventually dead-letter.
- [ ] Inbox is the source of truth for read state.
