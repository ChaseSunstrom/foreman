---
name: multi-currency
title: Multi-currency
area: domains
tags: [currency, fx, exchange-rates, iso-4217, rounding, formatting]
detect: [dep:dinero.js, dep:py-moneyed]
related: [money, invoicing-tax, billing-subscriptions, stripe]
---
Handling several currencies: amount plus ISO 4217 code, per-currency minor units, stored FX rates with dates, and locale-aware formatting.

## Verify
- `pytest -q tests/test_currency.py`: conversion, rounding and formatting tests pass.
- `python -c "from decimal import Decimal as D; print(D('10.005').quantize(D('0.01'), rounding='ROUND_HALF_UP'))"`: shows the explicit mode your code must state (prints 10.01).
- `grep -rnE "\* 100|/ 100" src`: hard-coded two-decimal assumptions (review each).

## Test first
Zero-decimal and three-decimal currencies break the "times 100" rule.
```python
from app.money import to_minor, convert

def test_minor_units_differ_per_currency_and_fx_uses_stored_rate():
    assert to_minor("1000", "JPY") == 1000        # 0 decimals
    assert to_minor("12.34", "USD") == 1234
    assert to_minor("1.234", "KWD") == 1234       # 3 decimals
    rate = {"pair": "EUR/USD", "rate": "1.0850", "date": "2026-03-01"}
    assert convert(1000, "EUR", "USD", rate) == 1085   # minor units in, minor units out
```

## Do
- Store `amount_minor` (integer) with `currency` (ISO 4217) on every monetary column; never a bare number.
- Look up the exponent per currency (JPY 0, USD 2, KWD 3) from a library table, not a constant.
- Fix a presentment currency (what the customer sees) and a settlement or reporting currency; record both amounts on a transaction.
- Store the FX rate, its source and timestamp with each converted amount; never recompute history with today's rate.
- Convert with Decimal, round once at the end with a stated mode, and keep rates at higher precision than amounts.
- Refuse to add or compare amounts in different currencies without explicit conversion.
- Format with `Intl.NumberFormat` (JS) or Babel (Python) using the user's locale and the amount's currency.
- Refresh rates on a schedule with a fallback and staleness alert; for payments, use the processor's rate or lock one.
- Handle cash rounding and minimum charge amounts per currency where they apply.

## Avoid
- Floats for money: drift and wrong cents. Use integers or Decimal.
- Assuming two decimals: charging 100 times too much for JPY. Use the currency exponent.
- Summing mixed currencies into one total silently: convert first and label.
- Using a live rate for refunds: customers get a different amount. Refund in the original currency from the original transaction.
- Symbol-only storage (`$`): ambiguous across USD, CAD and AUD. Store the code.
- Formatting by string concatenation: wrong separators and symbol placement. Use locale formatters.

## Review
- [ ] Every amount has a currency.
- [ ] Exponents come from a table.
- [ ] FX rate and date are stored on conversions.
- [ ] Rounding mode is explicit and tested.
- [ ] Formatting uses locale APIs.
