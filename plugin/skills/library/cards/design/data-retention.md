---
name: data-retention
title: Data retention
area: design
tags: [retention, privacy, gdpr, purge, ttl, compliance, deletion]
detect: []
related: [soft-deletes, audit-trails, multi-region, background-jobs, multi-tenancy]
---
Every data class has a stated retention period, an automated purge, and an erasure path that reaches backups, caches, search and copies.

## Verify
- `pytest -q -k "retention or purge or erasure"`: purge and erasure tests.
- `git grep -niE "retention|expires_at|purge" -- src config`: each store has a declared policy.
- `psql -c "select count(*) from TABLE where created_at < now() - interval '400 days'"`: nothing lingers beyond its window (adjust table and interval).

## Test first
Expired rows go, live rows stay, and an erasure request leaves no personal data behind.
```python
def test_purge_and_erasure(db, search, clock):
    old = add_event(db, user=1, at=clock.now() - days(400))
    new = add_event(db, user=1, at=clock.now())
    purge_expired(db, clock, max_age=days(365))
    assert exists(db, old.id) is False and exists(db, new.id) is True
    erase_user(db, search, user=1)
    assert db.scalar("select count(*) from events where user_id=1") == 0
    assert search.query("user:1") == []
    assert audit_has(db, "user.erased", user=1)       # keep proof, not the data
```

## Do
- Inventory data stores (DB, object storage, logs, analytics, search, caches, backups) and assign a period and owner to each.
- Store a timestamp that drives expiry (`created_at`, `expires_at`); partition large tables by time so purge is a cheap drop.
- Run purge as a scheduled, idempotent, batched job with a dry-run mode and metrics.
- Implement erasure and export per subject, covering all stores and downstream processors; keep a minimal record that it happened.
- Set native TTLs where available (object lifecycle rules, Redis `EXPIRE`, TTL indexes).
- Let backups age out on a defined schedule, and re-apply erasures when restoring.
- Minimise at write time: do not collect or log what you will not need; hash or truncate identifiers.

## Avoid
- Soft delete as the only deletion: data persists. Add a purge after the window.
- Purging in one huge `DELETE`: long locks and bloat. Batch or drop partitions.
- Forgetting derived copies (search index, analytics, caches, exports): erase through events or a registry.
- Logs with personal data and infinite retention: scrub at ingestion and set log lifecycle.
- Legal holds ignored: add a hold flag that blocks purge for flagged subjects.

## Review
- [ ] Policy exists for every store, including backups and logs.
- [ ] Purge is automated, batched and monitored.
- [ ] Erasure covers derived data.
- [ ] Legal hold path exists.
