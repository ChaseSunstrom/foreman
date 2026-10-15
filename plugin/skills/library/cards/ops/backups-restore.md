---
name: backups-restore
title: Backups and restore tests
area: ops
tags: [backup, restore, retention, restic, encryption, rpo]
detect: [file:restic*, file:*.borg]
related: [disaster-recovery, database-failover, secrets-rotation, runbooks]
---
A backup counts only when a scheduled restore test has passed; measure RPO and RTO from real restores.

## Verify
- `restic snapshots`: snapshots exist and the newest is recent (restic).
- `restic check --read-data-subset=5%`: repository integrity, sampling the stored data.
- `restic restore latest --target /tmp/restore-test --include /path/critical`: a real restore completes.
- `pg_restore --list backup.dump | head`: a PostgreSQL dump is readable.
- `sha256sum -c manifest.sha256`: restored files match the recorded checksums.

## Test first
Write the restore test before the backup job is called done: it restores into a scratch location and asserts content.
```sh
set -e
d=$(mktemp -d)
restic restore latest --target "$d" --include /srv/app/data
test -s "$d/srv/app/data/db.sqlite"
sqlite3 "$d/srv/app/data/db.sqlite" 'PRAGMA integrity_check;' | grep -qx ok
n=$(sqlite3 "$d/srv/app/data/db.sqlite" 'select count(*) from users;')
[ "$n" -gt 0 ]
rm -rf "$d"
```
Run it on a schedule and alert on failure or on a stale latest snapshot.

## Do
- Follow 3-2-1: three copies, two media, one offsite; add an immutable or offline copy against ransomware.
- Encrypt client-side; keep the key and repository password outside the backed-up system (a password manager and a sealed offline copy).
- Take consistent snapshots: database dump or filesystem snapshot, not copied live files.
- Write down RPO and RTO, then time a full restore and compare.
- Set retention (daily, weekly, monthly) with a pruning policy, and check that prune cannot delete the only good copy.
- Alert on backup absence: no success in N hours is a page, not a log line.
- Use a separate credential for the backup job that can write but not delete.
- Restore in a clean environment, to prove the backup has no hidden dependency on the original host.

## Avoid
- Counting "job succeeded" as a good backup: exit 0 can hide empty or corrupt output. Restore and check content.
- Backups stored on the same host or account as the data: one compromise or failure takes both. Replicate off-account with separate credentials.
- Losing the encryption key with the machine: the backups are unreadable. Store it separately and test recovery from it.
- Backing up a running database by file copy: torn pages. Use the engine's dump or snapshot tooling.
- Pruning with a bug in the policy: months vanish. Dry-run first (`--dry-run`) and keep an offline copy.
- Never testing restore time: the RTO is a guess. Time it each quarter.

## Review
- [ ] A restore test runs on a schedule, passes, and alerts when it fails.
- [ ] The newest backup age is monitored.
- [ ] One copy is offsite and immutable or offline, under separate credentials.
- [ ] Key and passphrase recovery was tested without the original host.
- [ ] RPO and RTO are written and match measured restores.
