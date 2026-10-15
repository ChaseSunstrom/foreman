---
name: billing-subscriptions
title: Billing and subscriptions
area: domains
tags: [billing, subscriptions, proration, dunning, entitlements, webhooks]
detect: []
related: [stripe, money, webhooks, invoicing-tax, timezones]
---
Subscription billing: a local state machine fed by provider webhooks, proration, trials, dunning, and entitlements derived from state.

## Verify
- `pytest -q tests/test_billing.py`: state transitions, proration and webhook idempotency pass.
- `grep -rn "is_premium\|plan ==" src`: entitlement checks scattered outside one function (should route through `entitlements()`).
- `python -m pytest -q -k "webhook and duplicate"`: replayed events change nothing.

## Test first
The nastiest case: a duplicate and out-of-order webhook.
```python
from app.billing import handle_event

def test_duplicate_and_stale_events_are_noops(db, sub):
    paid = {"id": "evt_2", "type": "invoice.paid", "created": 200, "sub": sub.id}
    failed = {"id": "evt_1", "type": "invoice.payment_failed", "created": 100, "sub": sub.id}
    handle_event(db, paid); handle_event(db, paid)
    handle_event(db, failed)             # older than last applied event
    assert db.sub(sub.id).status == "active"
    assert db.processed_count("evt_2") == 1
```

## Do
- Model states explicitly: trialing, active, past_due, canceled, plus `cancel_at_period_end`. Allow only listed transitions.
- Treat the provider as source of truth for payment state; store its ids, status, period start and end, and last event time.
- Derive access from one `entitlements(account)` function; grace period for past_due.
- Prorate on plan change from period boundaries in integer minor units; use the provider's proration where available and show a preview first.
- Run dunning on a schedule: retry cadence, emails, then cancel; log every step.
- Record the plan snapshot per invoice so price changes don't rewrite history.
- Keep seat or usage counts as events summed per period.

## Avoid
- Granting access on the checkout redirect: users can hit it unpaid. Grant on the verified webhook.
- Float money or month math like `+30 days`: use calendar months and clamp the day (Jan 31 renews Feb 28).
- Applying webhooks in arrival order: compare event time or fetch current state, and dedupe by event id.
- Hard-deleting canceled subscribers: keep records for invoices and reactivation.
- Trial abuse by re-signup: key trials on payment fingerprint or account, not email alone.
- Timezone-local renewal dates: store UTC.

## Review
- [ ] Webhook handler is signature-checked and idempotent.
- [ ] Transitions are table-driven and tested, including cancel and reactivate.
- [ ] Money is integer minor units with currency.
- [ ] Access goes through one entitlement function.
- [ ] Failed payment path has a tested grace and end.
