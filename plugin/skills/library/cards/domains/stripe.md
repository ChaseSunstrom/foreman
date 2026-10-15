---
name: stripe
title: Stripe Payments
area: domains
tags: [stripe, payments, checkout, subscriptions, webhooks, billing]
detect: [dep:stripe, dep:@stripe/stripe-js, dep:@stripe/react-stripe-js, dep:stripe-java, dep:Stripe.net]
related: [webhooks, money, auth-providers, gdpr]
---
Stripe integrations: Checkout or Payment Intents, webhook-driven fulfillment, idempotent requests, test-mode verification.

## Verify
- `stripe listen --forward-to localhost:4242/webhook`: forwards test events locally and prints the signing secret.
- `stripe trigger payment_intent.succeeded`: fires a sample event at your handler.
- `stripe logs tail`: live API requests and errors in test mode.
- `grep -rnE "sk_(live|test)_" . --exclude-dir=node_modules`: no secret key committed.

## Test first
Drive the webhook handler with a signed payload; fulfillment must be idempotent.
```python
import stripe, time, json
def signed(payload: dict, secret: str) -> tuple[bytes, str]:
    body = json.dumps(payload).encode()
    ts = int(time.time())
    sig = stripe.WebhookSignature._compute_signature(f"{ts}.{body.decode()}", secret)
    return body, f"t={ts},v1={sig}"

def test_fulfills_once(client, db):
    body, hdr = signed(CHECKOUT_COMPLETED, "whsec_test")
    for _ in range(2):
        assert client.post("/webhook", data=body, headers={"Stripe-Signature": hdr}).status_code == 200
    assert db.orders_for("cs_123") == 1
```
Alternatively, generate the header via `stripe.Webhook.generate_test_header` where your SDK provides one.

## Do
- Create a Checkout Session or PaymentIntent on the server; amounts and price ids come from your catalog, never from the client.
- Fulfill from webhooks (`checkout.session.completed`, `invoice.paid`, `payment_intent.succeeded`), not from the success redirect.
- Verify signatures against the raw request body with `stripe.webhooks.constructEvent` (or SDK equivalent) and the endpoint secret.
- Return 2xx quickly; process async; store the `event.id` and skip repeats.
- Send an `Idempotency-Key` header on creates that may be retried.
- Store Stripe ids (`cus_`, `sub_`, `pi_`) on your records; sync subscription state from events.
- Use the Customer Portal for plan changes and cancelation.
- Pin the API version in the client and upgrade deliberately.
- Money in integer minor units with explicit `currency`.

## Avoid
- Parsing JSON before verifying: the signature breaks on re-serialized bodies. Use the raw bytes (`express.raw`, `request.get_data()`).
- Trusting the client's `amount` or `price`: tampering. Compute server-side.
- Granting access on the redirect to `success_url`: users can visit it directly. Wait for the webhook or retrieve the session server-side.
- Assuming one delivery or ordered events: handle duplicates and out-of-order by fetching current object state.
- Live secret keys in front-end code or repos: only the publishable key ships. Use env secrets and restricted keys.
- Legacy Charges or Sources, or the old `stripe.redirectToCheckout` pattern: use Checkout Sessions and Payment Intents.
- Testing only the happy path: cover declines (card `4000000000000002`), 3D Secure, and failed renewals.

## Review
- [ ] Webhook verifies signature, dedupes by event id, and returns fast.
- [ ] No fulfillment from client-side signals.
- [ ] Amounts are server-derived integers with currency.
- [ ] Retries are idempotent; keys are scoped to the operation.
- [ ] Test-mode flows cover decline, 3DS, refund and subscription lapse.
