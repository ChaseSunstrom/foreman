---
name: disaster-recovery
title: Disaster recovery
area: ops
tags: [disaster-recovery, rto, rpo, failover, region, game-day]
detect: []
related: [backups-restore, database-failover, dns, runbooks, incident-response]
---
Disaster recovery means rebuilding service in another failure domain within a stated RTO and RPO, proven by a full exercise.

## Verify
- `dig +short www.example.com`: DNS currently points where you expect, and the failover record exists.
- `terraform plan -detailed-exitcode`: infrastructure code matches reality (exit 0 clean, 2 drift); run it against the recovery environment too.
- `restic snapshots --latest 1`: the newest offsite backup is recent (restic).
- `psql "$DR_DSN" -Atc "select now() - pg_last_xact_replay_timestamp()"`: the DR replica's lag, which is the live RPO (PostgreSQL).
- `curl -fsS https://dr.example.com/healthz`: the recovery environment serves traffic.

## Test first
The test is a game day: declare the primary region lost and bring service up in the recovery site from documented steps only.
- Fix the scenario and success criteria first: data loss at most RPO, service restored within RTO, key user journeys pass.
- Start a timer, cut access to the primary (or simulate it), and follow the runbook with no tribal knowledge.
- Run the smoke suite against the recovered site.
- Record minutes per step, every deviation, and every missing credential or access.
Fail the exercise if RTO or RPO is missed, then fix and repeat; the first run usually fails.

## Do
- Define RTO and RPO per service from business impact, and tier services (what comes back first).
- Keep infrastructure as code so the recovery site is built from the repo, not from memory.
- Replicate data to a separate failure domain (region or provider) with its own credentials, and keep an immutable copy.
- Store the recovery inputs somewhere that survives the disaster: runbooks, DNS and registrar access, secrets, the encryption keys, and the contact list.
- Map dependencies and recovery order (identity, secrets, network, data, then apps), including third parties.
- Decide the failover trigger and who may call it, and how to fail back.
- Keep the recovery site's capacity and quotas sufficient, or document how fast it scales.
- Run game days regularly, including an unannounced one, and feed the lessons into the plan.

## Avoid
- A plan nobody exercised: it fails on the first missing credential. Run the game day.
- Recovery depends on the failed region (the secrets manager, the DNS provider, the CI system there): you cannot start. Place those elsewhere and test without the primary.
- Backups without a restore test: you find corruption at the worst time. Restore on schedule.
- Forgetting failback: the recovery site becomes a permanent, unmonitored production. Plan and rehearse the return.
- RTO written as a wish: a measured restore takes four times longer. Time it and publish the real number.
- Quota and capacity limits in the recovery region: instances cannot launch. Pre-raise limits and check them.

## Review
- [ ] RTO and RPO exist per tier and the last exercise met them.
- [ ] Recovery builds from code and offsite data with separate credentials.
- [ ] Recovery inputs are reachable when the primary is gone.
- [ ] Failover trigger, authority, and failback are documented.
- [ ] Findings from the last exercise are closed or tracked.
