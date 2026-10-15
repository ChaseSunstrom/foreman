---
name: optimistic-locking
title: Optimistic locking
area: design
tags: [concurrency, versioning, etag, database, lost-update, conflict]
detect: []
related: [distributed-locks, idempotency, rest-api-design, retries-backoff, concurrency]
---
Detect lost updates by writing only if the row's version is unchanged, and surface a conflict instead of overwriting.

## Verify
- `pytest -q -k "version or conflict"`: two-writer conflict tests.
- `git grep -nE "version\s*=\s*version\s*\+\s*1|If-Match" -- src`: updates bump and check the version.
- `psql -c "\d TABLE"`: the version column is `NOT NULL` with a default.

## Test first
Two writers load the same version; the second must fail, not clobber.
```python
def test_second_writer_gets_conflict(db):
    doc = create_doc(db, body="a")
    w1 = load_doc(db, doc.id); w2 = load_doc(db, doc.id)
    save_doc(db, w1, body="b")                  # version 1 -> 2
    with pytest.raises(ConflictError):
        save_doc(db, w2, body="c")              # still thinks version 1
    assert load_doc(db, doc.id).body == "b"

def test_http_if_match(client, doc):
    r = client.put(f"/docs/{doc.id}", json={"body": "x"}, headers={"If-Match": '"0"'})
    assert r.status_code == 412
```

## Do
- Add an integer `version` (or use `xmin` or a row hash). Update with `UPDATE t SET ..., version = version + 1 WHERE id = ? AND version = ?` and check the affected row count.
- Expose it over HTTP as `ETag` and require `If-Match` on PUT, PATCH and DELETE; return 412 (or 409) on mismatch, 428 when the header is missing.
- ORMs: use the built-in (JPA `@Version`, SQLAlchemy `version_id_col`, Rails `lock_version`, EF concurrency token).
- On conflict, either return the current state to the client or re-read, re-apply the intent and retry a bounded number of times with jitter.
- Keep the version check in the same statement as the write; never read the version then write separately.
- Use pessimistic `SELECT ... FOR UPDATE` only for short, high-contention critical sections.

## Avoid
- Check then update in two statements: races return. Put the version in the `WHERE`.
- Ignoring zero rows affected: silent lost update. Treat as conflict.
- Retrying blindly on conflict with stale input: loops or overwrites. Re-read and re-apply.
- Timestamps as versions: clock ties and precision loss. Use a counter.
- Bumping version only in some code paths (bulk updates, raw SQL): checks fail open. Route all writes through one place or a trigger.

## Review
- [ ] Every update statement checks and bumps the version.
- [ ] Affected-row count is inspected.
- [ ] API uses ETag and If-Match with 412 or 428.
- [ ] Retries are bounded and re-read first.
