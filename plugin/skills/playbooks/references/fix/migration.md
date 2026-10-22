<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Schema and data migrations

Use when a change alters a live database: a new, renamed or dropped column or table, a type change, a new
constraint or index, or a backfill. The rule underneath: old code and new code both run against the schema
during a deploy, so every step must work with both.

Built on library cards: `fm lib show zero-downtime-migrations` (expand, migrate, contract),
`fm lib show sql-migrations` (tools and file layout), `fm lib show migration-tests` (testing up and down),
`fm lib show postgres-locking` (which DDL takes which lock), `fm lib show feature-flags` (switching reads).

## The procedure

1. **Classify the change.** Additive (new nullable column, new table, new index) ships in one step.
   Anything that renames, retypes, drops or tightens (`NOT NULL`, unique, foreign key) is a multi-step change.
   Pass: the brief names the class and, if multi-step, lists the releases below.
2. **Set a lock budget before any DDL.** Every DDL statement runs with a short lock timeout, so a blocked
   migration fails fast instead of queueing every query behind it: Postgres `SET LOCAL lock_timeout = '5s'`
   inside the migration's transaction (plain `SET` for the statements that can't run in one, below), MySQL
   `SET SESSION lock_wait_timeout = 5`. On timeout, retry a few times with a pause, then stop and report.
   Pass: the timeout is in the migration file.
3. **Expand.** Add the new shape next to the old one: new column nullable or with a constant default, new table,
   index built online (Postgres `CREATE INDEX CONCURRENTLY`, outside a transaction). A failed concurrent build
   leaves an `INVALID` index: drop it before retrying. Pass: the previous release's test suite passes against
   the expanded schema.
4. **Dual-write.** Ship code that writes both old and new shapes and still reads the old one.
5. **Backfill in batches** (snippet below): keyset paging by primary key, a bounded batch, a commit per batch,
   idempotent (`WHERE new IS NULL`), resumable after a crash. Pass: a rerun changes zero rows, and a count
   query shows no unfilled rows.
6. **Switch reads** to the new shape, behind a flag where the risk is high. Watch error rates for a full
   traffic cycle before going on.
7. **Contract.** Stop writing the old shape in one release; drop it in a later one. Tighten without a long
   lock, per engine. Postgres check or foreign key: `ADD CONSTRAINT … NOT VALID`, then `VALIDATE CONSTRAINT`.
   Postgres `NOT NULL` (17 and older): `ADD CONSTRAINT c CHECK (col IS NOT NULL) NOT VALID`, `VALIDATE
   CONSTRAINT c`, then `ALTER COLUMN col SET NOT NULL` (it uses the valid check instead of scanning), then drop
   `c`. Unique can't be `NOT VALID`: `CREATE UNIQUE INDEX CONCURRENTLY i …`, then `ADD CONSTRAINT u UNIQUE
   USING INDEX i`.
8. **Rollback is written, not assumed.** Each step has its down path, tested `down` then `up` on a copy. A step
   that destroys data (drop, narrowing type) has none: say so and take a backup first. Pass: the brief names
   the irreversible step and the backup.

## A backfill that survives a crash and a rerun

Runs as is (stdlib `sqlite3`); in production add a short sleep between batches and log `last`.

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("create table users(id integer primary key, name text, display_name text)")
db.executemany("insert into users(name) values (?)", [(f"u{i}",) for i in range(2500)])
last = 0
while True:
    ids = [r[0] for r in db.execute(
        "select id from users where id > ? and display_name is null order by id limit 1000", (last,))]
    if not ids:
        break
    db.execute("update users set display_name = name where id between ? and ? and display_name is null",
               (ids[0], ids[-1]))
    db.commit()
    last = ids[-1]
assert db.execute("select count(*) from users where display_name is null").fetchone()[0] == 0
```

## Never in one deploy

- Rename a column or table that running code reads.
- Add `NOT NULL` to a column that existing code may still leave empty.
- Drop a column in the same release that stops reading it.
- Run a backfill as one `UPDATE` over the whole table.
