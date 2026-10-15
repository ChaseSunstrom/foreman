---
name: invoicing-tax
title: Invoicing and sales tax
area: domains
tags: [invoicing, tax, vat, rounding, credit-notes, numbering]
detect: []
related: [money, multi-currency, billing-subscriptions, stripe, pdf-generation]
---
Invoices: immutable documents, gapless numbering, line-level tax with defined rounding, credit notes instead of edits.

## Verify
- `pytest -q tests/test_invoice.py`: totals, rounding and numbering tests pass.
- `python -c "from decimal import Decimal as D; print(D('0.125').quantize(D('0.01')))"`: shows the default half-even result your rounding must state explicitly.
- `grep -rn "float" src/billing`: no floats in money paths (should be empty).

## Test first
Per-line and per-invoice rounding differ by a cent; pick one and pin it.
```python
from decimal import Decimal as D
from app.invoice import build

def test_tax_rounds_once_per_invoice_total_by_rate():
    lines = [{"net": D("0.33"), "rate": D("0.20")}] * 3
    inv = build(lines, rounding="per_invoice")
    assert inv.net == D("0.99")
    assert inv.tax == D("0.20")        # 0.198 rounded once; per-line would give 0.21
    assert inv.gross == D("1.19")
```

## Do
- Use Decimal or integer minor units; state the rounding mode (half-up for tax is common) and where it applies, per the jurisdiction.
- Freeze an invoice when issued: seller and buyer details, tax ids, rates, rule used, and FX rate with its date.
- Number sequentially without gaps in a transaction per series; drafts get no number.
- Correct with a credit note that references the original; never edit or delete an issued invoice.
- Determine tax from place of supply: buyer country, business or consumer, product type, a valid VAT id (validate via VIES for EU B2B reverse charge).
- Show tax per rate in a summary table; label reverse charge and zero rates.
- Use a tax engine or provider for US sales tax nexus and rate lookup instead of a hand-kept table.

## Avoid
- Recomputing old invoices from current prices or rates: store the numbers issued.
- Prices that are tax-inclusive in one place and exclusive in another: add an explicit `tax_inclusive` flag and derive net from gross consistently.
- Numbering from `max(id)+1` without a lock: duplicates or gaps. Use a counter row with `SELECT ... FOR UPDATE`.
- Rounding each tax line and also the total, then reporting a mismatch: round at one defined level.
- Charging VAT on a valid EU B2B sale without checking the id's validity date.
- Deleting voided invoices: void with a reason and keep the number.

## Review
- [ ] Rounding mode and level are documented and tested.
- [ ] Issued invoices are immutable; corrections use credit notes.
- [ ] Numbering is gapless under concurrency.
- [ ] Tax rule, rate and FX snapshot are stored on the invoice.
- [ ] Currency is stored with every amount.
