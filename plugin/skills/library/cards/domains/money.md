---
name: money
title: Money and Currency
area: domains
tags: [money, currency, decimal, rounding, ledger, pricing]
detect: [dep:dinero.js, dep:currency.js, dep:big.js, dep:decimal.js, dep:bignumber.js, dep:py-moneyed, dep:money, dep:joda-money, dep:shopspring/decimal]
related: [stripe, i18n, timezones, postgis]
---
Monetary values as exact integers or decimals with an explicit currency, deliberate rounding, and an append-only ledger.

## Verify
- `node -e "console.log(0.1+0.2)"`: demonstrates why floats are banned (prints 0.30000000000000004).
- `psql -c "\d orders"`: money columns are `numeric(p,s)` or `bigint` minor units plus a currency code, not `float` or `money`.
- `grep -rnE "parseFloat|toFixed|float" src --include=*.ts | grep -i -E "price|amount|total"`: float arithmetic on money.
- The test suite's property tests: sum of allocated parts equals the total.

## Test first
Cover rounding and allocation, where cents vanish.
```ts
import { test, expect } from 'vitest';
import { allocate, addMinor } from './money';

test('splitting 100 cents three ways loses nothing', () => {
  const parts = allocate({ minor: 100n, currency: 'USD' }, 3);
  expect(parts.map(p => p.minor)).toEqual([34n, 33n, 33n]);
  expect(parts.reduce((s, p) => s + p.minor, 0n)).toBe(100n);
});

test('adding different currencies throws', () => {
  expect(() => addMinor({ minor: 1n, currency: 'USD' }, { minor: 1n, currency: 'EUR' })).toThrow();
});
```

## Do
- Store integer minor units (cents) plus ISO 4217 code; or `NUMERIC` in the database and a decimal type in code.
- Know the exponent per currency: JPY has 0 decimals, KWD and BHD have 3. Look it up from a table, never assume 2.
- Choose one rounding mode (usually half-even or half-up per the business rule), apply it once at defined points (line item versus invoice total) and document it.
- Allocate remainders explicitly when splitting (largest remainder method).
- Tax: record rate, jurisdiction and whether prices include tax; compute per line or per invoice by rule.
- Model balances as an append-only ledger of entries that sum, with idempotency keys on postings.
- Convert currencies with a stored rate and timestamp; keep both original and converted amounts.
- Format only at the edge with `Intl.NumberFormat(locale, {style: 'currency', currency})`.

## Avoid
- `float` or `double` for amounts: rounding drift. Use integers or decimals.
- Passing the JSON number 19.99 across services: parsers lose precision. Send minor units as integers or decimal strings.
- Assuming two decimals: breaks JPY and KWD. Use currency exponents.
- Updating a balance column in place: lost updates and no audit. Insert ledger rows within a transaction, with `SELECT ... FOR UPDATE` or constraints.
- Rounding intermediate results then summing: totals differ from line sums. Round at the defined point.
- Database `MONEY` type: locale dependent. Use `numeric`.
- Storing converted amounts without the rate: unreproducible. Store rate and time.
- Negative zero or sign mix-ups for refunds: use a typed direction or signed minor units consistently.

## Review
- [ ] Every amount carries a currency; mixing currencies is a type or runtime error.
- [ ] No float math on money anywhere, including JSON and spreadsheets.
- [ ] Rounding mode and point documented and tested; splits sum to the total.
- [ ] Ledger entries are append-only, idempotent, and reconcile to balances.
- [ ] Display formatting is locale-aware and separate from stored values.
