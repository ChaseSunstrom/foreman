---
name: sql-window-functions
title: SQL window functions
area: data
tags: [sql, window, ranking, running-total, partition, analytics]
detect: []
related: [sql-ctes, query-tuning, postgres-indexes, dbt]
---
Window functions: ranking, running totals, lag and lead, frames, and the filtering rules that trip people.

## Verify
- `psql -c "EXPLAIN ANALYZE <query>"`: WindowAgg sits over a Sort that an index on (partition, order) columns could remove.
- `psql -c "<query> LIMIT 20"`: spot-check ties, first rows per partition and NULL ordering by eye.
- `sqlfluff lint query.sql`: style and ambiguity lint, when the project uses sqlfluff.

## Test first
Test ties, partitions and frame edges with a tiny fixed table.
```python
def test_top_per_group_with_ties_and_running_total(db):
    db.execute("INSERT INTO s VALUES ('a',10),('a',10),('a',5),('b',1)")
    rows = db.execute("""SELECT g, v, row_number() OVER (PARTITION BY g ORDER BY v DESC),
                                  rank() OVER (PARTITION BY g ORDER BY v DESC)
                         FROM s ORDER BY g, 3""").fetchall()
    assert [r[3] for r in rows if r[0] == 'a'] == [1, 1, 3]
```

## Do
- Pick the function for tie behavior: `row_number` (unique), `rank` (gaps), `dense_rank` (no gaps).
- Top N per group: compute the rank in a subquery or CTE, then filter `WHERE rn <= N` in the outer query.
- Running total: `sum(x) OVER (PARTITION BY k ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`. State the frame explicitly.
- Compare to previous row with `lag(x, 1) OVER (...)`; supply the default argument for the first row.
- Moving average: `avg(x) OVER (ORDER BY d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`.
- Reuse a definition with `WINDOW w AS (PARTITION BY k ORDER BY ts)` and `OVER w`.
- Always add a deterministic tie-breaker to ORDER BY (`ORDER BY ts, id`).
- Index `(partition_col, order_col)` so the sort is avoided on big tables.

## Avoid
- Filtering on a window result in the same `WHERE`: not allowed, windows run after WHERE. Wrap in a subquery or CTE (or use `QUALIFY` on engines that support it).
- Relying on the default frame with `ORDER BY`: it is RANGE to the current row, so ties are summed together and `last_value` returns surprises. Use `ROWS` and an explicit frame.
- `ORDER BY` without a unique tie-breaker in `row_number`: non-deterministic results between runs.
- Forgetting `PARTITION BY`: one global window over all rows.
- `last_value` with the default frame: returns the current row. Add `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.
- Using a self-join or correlated subquery for running totals: quadratic. Use a window.
- NULL ordering assumed: specify `NULLS FIRST` or `NULLS LAST` where it matters.

## Review
- [ ] Ranking function chosen for the tie semantics required.
- [ ] Frames are explicit (ROWS versus RANGE stated).
- [ ] ORDER BY inside windows is deterministic.
- [ ] Window results filtered in an outer query.
- [ ] Large partitions have a supporting index or a bounded input.
