---
name: sqlite-wal
title: SQLite WAL mode
area: data
tags: [sqlite, wal, concurrency, pragma, busy-timeout, durability]
detect: []
related: [sqlite, sql-migrations]
---
SQLite in WAL mode: one writer with many readers, correct pragmas, and checkpoint and busy-lock failure modes.

## Verify
- `sqlite3 app.db "PRAGMA journal_mode"`: returns wal.
- `sqlite3 app.db "PRAGMA wal_checkpoint(TRUNCATE)"`: returns 0 as the first column when the checkpoint completes; the -wal file shrinks.
- `sqlite3 app.db "PRAGMA integrity_check"`: ok.
- `sqlite3 app.db "PRAGMA foreign_keys"`: 1 on every connection that matters (it is per connection).

## Test first
Prove a reader is not blocked by a writer, and a second writer waits rather than fails.
```python
def test_reader_not_blocked_and_writer_waits(tmp_path):
    a = sqlite3.connect(tmp_path/"d.db"); a.execute("PRAGMA journal_mode=WAL")
    b = sqlite3.connect(tmp_path/"d.db", timeout=2)
    a.execute("CREATE TABLE t(x)"); a.commit()
    a.execute("BEGIN IMMEDIATE"); a.execute("INSERT INTO t VALUES(1)")
    assert b.execute("SELECT count(*) FROM t").fetchone()[0] == 0
```

## Do
- Set per connection: `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA busy_timeout=5000; PRAGMA foreign_keys=ON`. `journal_mode=WAL` persists in the file; the others do not.
- Start write transactions with `BEGIN IMMEDIATE` so lock contention appears at the start, not as a failure mid-transaction on upgrade.
- Keep write transactions tiny and have one write path or a small pool of writers.
- Keep reads in short transactions: a long-lived reader stops checkpoints and grows the WAL.
- Back up with `sqlite3 app.db ".backup out.db"` or `VACUUM INTO`, never by copying the .db alone while live.
- Keep the db, -wal and -shm files on the same local filesystem.

## Avoid
- WAL on network filesystems (NFS, SMB): shared memory locking is unreliable and corrupts. Use a local disk.
- No `busy_timeout`: immediate `database is locked` errors. Set one.
- Deferred transactions that read then write: they fail with SQLITE_BUSY on upgrade, ignoring the timeout. Use `BEGIN IMMEDIATE`.
- Copying only `app.db` for backup: committed data may live in the -wal file. Use the backup command.
- `synchronous=OFF` for convenience: power loss can corrupt. NORMAL is the WAL-appropriate setting.
- Unbounded WAL growth from a never-finishing reader: monitor file size, close idle cursors.

## Review
- [ ] Pragmas applied on every new connection.
- [ ] Write transactions use BEGIN IMMEDIATE and are short.
- [ ] Backup uses the online backup path.
- [ ] Database lives on local disk.
- [ ] WAL size monitored or periodic checkpoint exists.
