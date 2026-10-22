<!-- Foreman's own playbook (written for Foreman, not ported). -->
# SQL: query review, indexes and plans

Use when a query is slow, a page times out on the database, a new query or index goes into review, or an ORM
call might be issuing more SQL than it looks. Schema changes belong in `migration.md`.

Built on library cards: `fm lib show query-tuning` (reading plans), `fm lib show postgres-indexes` and
`fm lib show mysql-indexes` (index types per engine), `fm lib show n-plus-one` (ORM loops),
`fm lib show postgres-locking` (what DDL and long transactions block).

## The procedure

1. **Capture the real query.** Take the SQL the database actually ran (query log, `pg_stat_statements`, the ORM's
   echo setting), with real parameter values, not the ORM source. Pass: the brief quotes the SQL text.
2. **Count the calls first.** One page that runs the same statement N times is an N+1, and no index fixes it.
   Pass: you state the number of statements per request, before and after.
3. **Read the plan on production-shaped data.** Postgres `EXPLAIN (ANALYZE, BUFFERS)`, MySQL `EXPLAIN ANALYZE`,
   SQLite `EXPLAIN QUERY PLAN`. A plan on a ten-row dev table says nothing. `EXPLAIN ANALYZE` executes the
   statement: run it on writes only inside a transaction you roll back. Pass: the plan is in the evidence, with row counts.
4. **Find the expensive node**, the one with the most time or buffers, not the first line. Signs: a full scan
   feeding a `LIMIT`, estimated rows off from actual rows by 10× or more (stale statistics: refresh them first
   with `ANALYZE <table>` in Postgres or `ANALYZE TABLE <table>` in MySQL, which takes a brief lock), a sort spilling to disk, a nested loop over thousands of outer rows.
5. **Fix the query before adding an index.** A function or cast on an indexed column (`lower(email) = …`,
   `created_at::date = …`), a leading-wildcard `LIKE '%x'`, `OR` across columns and `SELECT *` each defeat or
   bloat the plan. Pass: you name which of these you checked.
6. **Index for the query's shape:** equality columns first, then the range or sort column; include the selected
   columns only if that makes it covering. Every index slows writes and costs disk, so name the query it serves.
   On a live Postgres table build it with `CREATE INDEX CONCURRENTLY` (see `migration.md`).
7. **Prove it.** Same plan command, same data, before and after; plus the endpoint's timing. Pass: the slow
   node is gone and the wall time dropped, both recorded with `fm task evidence`.

## A plan you can read in ten seconds

Runs as is (stdlib `sqlite3`); the same before/after habit applies to any engine.

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("create table orders(id integer primary key, customer_id int, created_at text)")
q = "select id from orders where customer_id = ? order by created_at desc limit 20"
plan = lambda: [row[3] for row in db.execute("explain query plan " + q, (1,))]
print(plan())  # ['SCAN orders', 'USE TEMP B-TREE FOR ORDER BY']
db.execute("create index orders_customer_created on orders(customer_id, created_at)")
print(plan())  # ['SEARCH orders USING COVERING INDEX orders_customer_created (customer_id=?)']
```

## Review checks for any new query

- Parameters are bound, never formatted into the SQL string.
- Every query on a growing table has a `LIMIT` or a bounded `WHERE`, and paging is keyset (`WHERE id > ?`),
  not a deep `OFFSET`.
- No statement runs inside a loop over rows that a join or `IN (…)` could fetch at once.
- A transaction holds no locks across a network call or user wait.
