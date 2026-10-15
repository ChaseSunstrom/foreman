---
name: idempotency
title: Idempotency
area: design
tags: [idempotency, retries, dedupe, keys, exactly-once, payments]
detect: []
related: [retries-backoff, event-driven, background-jobs, sagas, rest-api-design]
---
Make repeated requests, messages and jobs produce one effect, using idempotency keys, unique constraints and stored results.

## Verify
- `curl -si -X POST localhost:8080/payments -H 'Idempotency-Key: k1' -d '{"amount":500}' && curl -si -X POST localhost:8080/payments -H 'Idempotency-Key: k1' -d '{"amount":500}'`: the second response replays the first (same ID and status), with no second charge.
- `curl -si -X POST localhost:8080/payments -H 'Idempotency-Key: k1' -d '{"amount":999}'`: same key, different body returns 422 or 409.
- `psql -c "select key, count(*) from idempotency_keys group by 1 having count(*) > 1"`: no duplicate keys (expect no rows).

## Test first
Send the same request twice, then two at once.
```python
def test_same_key_charges_once(client, ledger):
    h = {"Idempotency-Key": "k1"}
    a = client.post("/payments", json={"amount": 500}, headers=h)
    b = client.post("/payments", json={"amount": 500}, headers=h)
    assert a.json()["id"] == b.json()["id"] and ledger.total() == 500

def test_concurrent_same_key_charges_once(client, ledger):
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda _: client.post("/payments", json={"amount": 500},
                                          headers={"Idempotency-Key": "k2"}), range(8)))
    assert ledger.total() == 500
```

## Do
- Require a client-generated key (UUID) on unsafe, non-idempotent operations such as `POST` that move money or send messages.
- Store the key with a hash of the request, the status and the response, under a unique constraint.
- Claim the key first (insert with unique constraint), then do the work, then store the result. A concurrent duplicate gets 409 or waits.
- Commit the key record and the business effect in one transaction when they share a database.
- Expire keys after a documented window (24 hours is common).
- On a key reuse with different parameters, reject it instead of replaying.
- For message consumers, use the message ID (or a natural key such as order and event type) with a processed table.
- Prefer naturally idempotent operations: `PUT` of a full state, `INSERT ... ON CONFLICT DO NOTHING`, set-not-increment.

## Avoid
- Check-then-insert without a unique constraint: two requests both pass the check. Let the database enforce it.
- Deduplicating in memory or per instance: restarts and other instances reprocess. Use shared storage.
- Replaying only on success: a stored failure that is retryable should allow retry, while a stored success must replay. Define which statuses are final.
- Server-generated keys for the same retry: the client can't resend them. The client must own the key.
- Keys that don't include the user or tenant: one user's key can collide with another's. Scope the key.
- Incrementing counters on retried operations (`balance += x`): use a ledger row keyed by operation ID.

## Review
- [ ] A unique constraint enforces the key, and a concurrency test exists.
- [ ] The request hash is compared, and mismatches are rejected.
- [ ] Keys are scoped per user or tenant and expire on schedule.
- [ ] Effect and key record commit atomically or in a defined order with recovery.
- [ ] Consumers dedupe by message ID.
