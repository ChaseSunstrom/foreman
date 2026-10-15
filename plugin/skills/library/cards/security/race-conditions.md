---
name: race-conditions
title: Race conditions
area: security
tags: [security, concurrency, toctou, transactions, idempotency, locking]
detect: []
related: [authorization, rate-limiting, idor, webhook-signatures]
---
Check-then-act on balances, coupons, tokens and uniqueness must be atomic in the database, with idempotency keys and concurrency tests.

## Verify
- `pytest -q -k concurrent`: the parallel-request tests pass repeatedly.
- `pytest -q -k concurrent --count=20`: stable across runs, when `pytest-repeat` is installed.
- `git grep -nE "SELECT .* FOR UPDATE|select_for_update|with_for_update|ON CONFLICT|UNIQUE" -- ':!*test*'`: the atomic guards exist where state is checked then changed.

## Test first
Fire the same request in parallel and count successes.
```python
from concurrent.futures import ThreadPoolExecutor

def test_single_use_coupon_redeems_once(client, coupon, user):
    def redeem(_):
        return client.post("/redeem", json={"code": coupon.code}, headers=user).status_code
    with ThreadPoolExecutor(20) as ex:
        codes = list(ex.map(redeem, range(20)))
    assert codes.count(200) == 1
    assert coupon.refresh().uses == 1
```

## Do
- Put the invariant in the database: a UNIQUE constraint, a CHECK (`balance >= 0`), or a conditional `UPDATE ... SET x = x - 1 WHERE x > 0` then check the affected row count.
- Where reads decide writes, lock the row (`SELECT ... FOR UPDATE`) inside one transaction, or use optimistic version columns and retry.
- Require idempotency keys on payments and other retried writes. Store them with a unique index.
- Make token redemption atomic: delete or mark used in the same statement that validates it.
- Use serializable or repeatable-read isolation only where you have tested it, and handle retries.
- Take a distributed lock with an expiry only for work that spans services, and still keep the DB constraint.
- Move file checks and writes to open-with-exclusive-create instead of exists-then-open.

## Avoid
- `if balance >= amount: balance -= amount` in app code: two requests pass the check. Use a conditional UPDATE.
- Checking uniqueness with a SELECT before an INSERT: add a unique index and handle the violation.
- Caching a permission or limit, then acting later: re-check inside the transaction.
- Single-process mutexes in multi-worker services: they protect nothing across workers. Use the DB.
- Testing only sequentially: add parallel tests, since the bug appears only under concurrency.
- Rate limits that read then write a counter: use an atomic increment.

## Review
- [ ] Each check-then-act has an atomic form in the database.
- [ ] Idempotency keys exist for money and external side effects.
- [ ] Single-use tokens are consumed in one statement.
- [ ] A parallel test covers each limited resource.
- [ ] Retries on serialization failure are bounded.
