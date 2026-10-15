---
name: inventory
title: Inventory and stock
area: domains
tags: [inventory, stock, reservations, concurrency, ledger, oversell]
detect: []
related: [billing-subscriptions, bookings, webhooks, money]
---
Stock tracking: an append-only movement ledger, reservations with expiry, and atomic decrements so concurrent checkouts never oversell.

## Verify
- `pytest -q tests/test_inventory.py`: ledger, reservation and concurrency tests pass.
- `pytest -q -k concurrent`: parallel reservations never exceed on-hand stock.
- `grep -rn "quantity = quantity\|stock -= " src`: read-modify-write updates outside the atomic path (should be empty).

## Test first
Two buyers, one unit.
```python
from concurrent.futures import ThreadPoolExecutor
from app.inventory import reserve, OutOfStock

def test_last_unit_cannot_be_reserved_twice(db):
    db.set_stock("sku1", 1)
    def go(i):
        try: reserve(db, "sku1", 1, order=f"o{i}"); return True
        except OutOfStock: return False
    with ThreadPoolExecutor(8) as ex:
        results = list(ex.map(go, range(8)))
    assert results.count(True) == 1
    assert db.available("sku1") == 0
```

## Do
- Store movements (receipt, reservation, release, sale, adjustment, return) as an append-only ledger with reason and actor; on-hand is the sum or a cached counter updated in the same transaction.
- Decrement atomically: `UPDATE stock SET available = available - :n WHERE sku = :s AND available >= :n`, then check the affected row count.
- Reserve at checkout with an expiry; a sweeper releases expired holds; convert to sale on payment.
- Track per location and per lot or serial when expiry or recalls matter; pick by FEFO or FIFO.
- Make every movement idempotent by a unique key (order id plus line).
- Separate on-hand, reserved and available; show available.
- Reconcile counts with cycle counts as adjustment entries, never silent edits.

## Avoid
- Read, check, then write in application code: races oversell. Use the conditional update or row lock.
- Releasing a reservation twice on retry: key releases by reservation id.
- Deleting or editing past movements: corrections go in as new rows.
- Negative stock allowed by accident: add a `CHECK (available >= 0)` constraint unless backorders are intended.
- Caching availability on product pages as truth: re-check at reserve time.
- Bundles decrementing only the parent: decrement components.

## Review
- [ ] Stock changes only through ledger-writing functions.
- [ ] A DB constraint or conditional update prevents negatives.
- [ ] Reservations expire and release is idempotent.
- [ ] Concurrency test exists.
- [ ] Returns and cancellations restock via movements.
