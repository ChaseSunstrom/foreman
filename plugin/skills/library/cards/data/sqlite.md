---
name: sqlite
title: SQLite
area: data
tags: [sql, sqlite, embedded, database, wal, migrations]
detect: [dep:better-sqlite3, dep:sqlite3, dep:aiosqlite, dep:rusqlite, dep:sqlx, dep:mattn/go-sqlite3, dep:modernc.org/sqlite, dep:sqlite-jdbc, ext:.sqlite, ext:.db, file:*.sqlite3]
related: [sql-migrations, query-tuning, postgres, duckdb]
---
SQLite: one writer, WAL mode, foreign keys opted in per connection, parameterized statements.

## Verify
- `sqlite3 app.db "PRAGMA integrity_check;"`: file is not corrupt (expects `ok`).
- `sqlite3 app.db "PRAGMA foreign_key_check;"`: no orphaned rows (empty output).
- `sqlite3 app.db "EXPLAIN QUERY PLAN <query>"`: SEARCH using an index, not SCAN.
- `sqlite3 app.db "PRAGMA journal_mode;"`: `wal` on the file you ship.

## Test first
Use a temp file or `:memory:` per test with the real migrations applied.
```python
def test_fk_enforced(conn):
    conn.execute("PRAGMA foreign_keys=ON")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("insert into orders(user_id) values (999)")
```
Fails if the schema lacks the FK or the pragma is not set.

## Do
- Set per connection: `PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;`.
- Use `synchronous=NORMAL` with WAL for speed; keep `FULL` where power loss matters.
- Bind parameters (`?`, `:name`), never format SQL strings.
- Batch writes inside one transaction; use `BEGIN IMMEDIATE` for write transactions to avoid upgrade deadlocks.
- Declare `STRICT` tables (3.37+) for real type checks and `WITHOUT ROWID` only when measured.
- Use one writer connection and many readers; never share a connection across threads unless the driver allows it.
- Back up with `.backup` or `VACUUM INTO`, not by copying a live file.

## Avoid
- Assuming foreign keys work: they are off by default per connection. Run the pragma on every open.
- Copying `app.db` alone while in WAL mode: you lose `-wal` contents. Use `.backup`.
- Default type affinity for dates and booleans: values store as anything. Use ISO-8601 text or integers with a `CHECK`, or `STRICT`.
- Long-held read transactions in WAL: the WAL grows without checkpointing. Close them.
- `SQLITE_BUSY` ignored: set `busy_timeout` and retry writes.
- Network filesystems (NFS, SMB) for the db file: locking is unreliable. Keep it local.
- `ALTER TABLE` expecting full support: many changes need the create-copy-rename recipe.

## Review
- [ ] Connection setup sets foreign_keys, WAL and busy_timeout.
- [ ] Writes are batched in transactions; no per-row autocommit loops.
- [ ] Every query uses bind parameters.
- [ ] Backup path does not copy a live database file.
- [ ] Schema changes go through versioned migrations.
