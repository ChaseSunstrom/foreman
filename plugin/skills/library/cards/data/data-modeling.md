---
name: data-modeling
title: Data modeling
area: data
tags: [schema, modeling, normalization, constraints, keys, dimensional]
detect: []
related: [postgres, sql-migrations, dbt, postgres-indexes]
---
Relational and analytical schema design: keys, constraints, normalization, time and money types, and the dimensional layer.

## Verify
- `psql -c "\d+ tablename"`: PK, FKs, NOT NULL, CHECK and unique constraints are present.
- `psql -c "SELECT conrelid::regclass, conname FROM pg_constraint WHERE contype = 'f'"`: foreign keys exist where relationships do.
- `psql -c "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'orders'"`: types are as intended (timestamptz, numeric, not float or text).
- `dbt test`: uniqueness, not-null and relationship tests on analytical models, when dbt is used.

## Test first
Test that the database itself rejects bad data.
```python
def test_db_rejects_orphan_and_negative_amount(db):
    with pytest.raises(Exception):
        db.execute("INSERT INTO order_items(order_id, qty) VALUES (999, 1)")   # FK
    with pytest.raises(Exception):
        db.execute("INSERT INTO orders(id, total_cents) VALUES (1, -5)")       # CHECK
```

## Do
- Give every table a primary key; add a natural-key `UNIQUE` constraint alongside surrogate keys.
- Push rules into the schema: `NOT NULL`, `CHECK`, `UNIQUE`, `FOREIGN KEY ... ON DELETE` chosen deliberately.
- Normalize OLTP to third normal form; denormalize only for a measured read need, and name the source of truth.
- Money: integer minor units or `numeric(p,s)` with a currency code; never floating point.
- Time: store UTC instants (`timestamptz` in Postgres), keep the zone name separately only if needed.
- Soft delete via a `deleted_at` column needs partial unique indexes (`WHERE deleted_at IS NULL`).
- Analytics: star schema with fact tables at a declared grain and dimensions with surrogate keys; handle slowly changing dimensions with valid_from and valid_to.
- Use enums via a lookup table or CHECK, and many-to-many via a junction table with a composite key.

## Avoid
- Floats for money or quantities needing exactness: rounding drift. Use integer cents or numeric.
- Naive local timestamps: DST ambiguity. Store UTC.
- Constraints enforced only in app code: concurrent writers break them. Add the DB constraint.
- Comma-separated lists or JSON arrays for relations: no FK, no joins. Use a child table.
- One giant "entity-attribute-value" table: no typing, slow queries. Model real columns.
- Facts without a stated grain: double counting in joins. Document one row equals one what.
- Random UUIDv4 as the clustered primary key on write-heavy tables: index fragmentation. Prefer time-ordered ids (UUIDv7) or bigint.

## Review
- [ ] Every table has a PK and meaningful uniqueness constraints.
- [ ] Relationships have foreign keys; delete behavior chosen.
- [ ] Money, time and id types are justified.
- [ ] Denormalized data names its source of truth.
- [ ] Fact tables declare grain; dimensions have keys and history policy.
