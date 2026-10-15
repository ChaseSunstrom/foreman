---
name: sms
title: SMS messaging
area: domains
tags: [sms, twilio, messaging, compliance, webhooks, e164]
detect: [dep:twilio]
related: [phone-numbers, webhooks, notifications-system, unicode]
---
Sending and receiving SMS: E.164 numbers, segment math, opt-out compliance, idempotent delivery-status webhooks.

## Verify
- `pytest -q tests/test_sms.py`: segmenting, opt-out and status-callback tests pass with the provider stubbed.
- `python -c "import phonenumbers as p; print(p.is_valid_number(p.parse('+14155550100')))"`: the number library is wired (swap in your own number).
- `grep -rn "STOP" src tests`: an inbound opt-out handler exists and is tested.

## Test first
Pin the segment-count edge: one non-GSM character flips the encoding.
```python
from app.sms import segments

def test_unicode_char_switches_to_ucs2_and_shrinks_segments():
    assert segments("a" * 160) == 1
    assert segments("a" * 161) == 2          # GSM-7 multipart: 153 per part
    assert segments("a" * 69 + "’") == 2  # curly quote forces UCS-2: 70 limit
    assert segments("a" * 70) == 1
```

## Do
- Store numbers as E.164 only; validate and normalize at the edge.
- Keep a message table: id, to, body, provider_sid, status, error_code, created. Update status from callbacks, never from the send response alone.
- Make send idempotent with your own message id so a retry never double-texts.
- Verify the provider's webhook signature on every inbound and status callback; dedupe by provider sid and ignore out-of-order statuses (delivered after sent).
- Honor STOP, UNSUBSCRIBE, CANCEL, END, QUIT and START/HELP; persist consent per number with timestamp and source.
- Respect quiet hours in the recipient's timezone and rate limits per sender.
- Estimate cost from segment count before bulk sends.

## Avoid
- Treating a 2xx from send as delivered: it only means queued. Track status callbacks.
- Sending to numbers without recorded opt-in: carriers block the sender. Gate sends on consent.
- Smart quotes and emoji in templates by accident: the message becomes UCS-2 and costs more segments. Normalize or show the count.
- Trusting the From of an inbound webhook without signature check: anyone can post to it.
- Retrying on carrier error codes that are permanent (invalid or landline number): mark the number bad.
- Logging full message bodies and numbers: treat as PII.

## Review
- [ ] Consent is checked before every non-transactional send.
- [ ] Webhooks verify signatures and are idempotent.
- [ ] Opt-out keywords are handled in the inbound path and covered by a test.
- [ ] Segment count and encoding are computed, not assumed.
- [ ] Provider credentials come from env or a secret store.
