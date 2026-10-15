---
name: secrets-rotation
title: Secrets rotation
area: ops
tags: [secrets, rotation, credentials, keys, vault, leaks]
detect: []
related: [certificate-rotation, linux-hardening, wireguard, backups-restore]
---
Rotate every secret on a schedule and on suspicion, using overlap so rotation causes no outage, and prove the old one is dead.

## Verify
- `gitleaks detect --source . --no-banner`: no secrets committed in the working repo's history (gitleaks).
- `git log -p -S'AKIA' --all --oneline | head`: search history for a known secret prefix.
- `curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $OLD_TOKEN" https://api.example.com/me`: the old credential returns 401 or 403 after revocation.
- `curl -s -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $NEW_TOKEN" https://api.example.com/me`: the new credential works.
- `aws iam list-access-keys --user-name <user>`: key ages and status (AWS).

## Test first
Make rotation a rehearsed script and test it in staging with traffic running: it must finish with zero failed requests and the old secret rejected.
```sh
set -e
new=$(./gen-secret.sh)
./store-secret.sh service/api-key "$new"      # store as an additional valid secret
./reload-consumers.sh                           # consumers pick up new value
curl -fsS -H "Authorization: Bearer $new" "$URL" >/dev/null
./revoke-secret.sh "$OLD_ID"
code=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $OLD" "$URL")
[ "$code" = 401 ] || { echo "old secret still valid"; exit 1; }
```
Run it on a schedule so the first real rotation is not the first rotation.

## Do
- Keep secrets in a secrets manager or sealed store, never in git, images, or chat; inject at runtime through environment, files on tmpfs, or an agent.
- Prefer short-lived, dynamically issued credentials (database users, cloud tokens, workload identity) over long-lived static ones.
- Rotate with overlap: add the new secret, move consumers, confirm, then revoke the old (dual-valid window).
- Give each consumer its own credential, so one leak has a small scope and revocation is surgical.
- Have consumers re-read secrets on signal or interval without a redeploy.
- Scan for leaks in pre-commit and CI, and treat any leaked secret as compromised: rotate first, clean history second.
- Keep an inventory with owner, location, age, and rotation interval, and alert when overdue.
- Audit access to the secrets store, and alert on unusual reads.

## Avoid
- Revoking the old secret before consumers use the new one: an outage. Overlap, verify, then revoke.
- One shared secret across services and environments: a leak burns everything and you cannot tell the source. Issue one per consumer and per environment.
- Removing a leaked secret from git and calling it done: it persists in clones and caches. Rotate it.
- Secrets in environment dumps, process lists, and logs: redact, avoid command-line arguments, and use files with mode 600.
- Rotation that needs a human at midnight with a wiki page: it will be skipped. Automate and rehearse.
- Never testing revocation: the old key may still work. Call with it and expect rejection.

## Review
- [ ] No secrets in repos or images, with a scanner in CI.
- [ ] Rotation is scripted, overlapped, and rehearsed in staging with no failed requests.
- [ ] Every secret is in the inventory with an owner and interval, with overdue alerts.
- [ ] Old credentials were shown to fail after rotation.
- [ ] Credentials are per consumer, per environment, and short-lived where possible.
