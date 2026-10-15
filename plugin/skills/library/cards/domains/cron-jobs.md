---
name: cron-jobs
title: Cron and Scheduled Jobs
area: domains
tags: [cron, scheduler, jobs, systemd-timers, idempotency, locking]
detect: [dep:node-cron, dep:cron, dep:croniter, dep:apscheduler, dep:celery, dep:bullmq, dep:node-schedule, dep:quartz, dep:sidekiq-cron, dep:robfig/cron, file:crontab, file:*.timer, file:.github/workflows/*.yml]
related: [timezones, webhooks, email-sending, legacy-code]
---
Scheduled work that is safe to rerun, never overlaps itself, runs in a known timezone and reports failures.

## Verify
- `crontab -l`: installed schedule (cron has a minimal environment, so check PATH and absolute paths).
- `systemd-analyze calendar "Mon..Fri *-*-* 09:00"`: next elapse times for a systemd calendar expression.
- `systemctl list-timers`: timers, last and next run.
- `flock -n /tmp/job.lock ./job.sh; echo $?`: a second concurrent run exits immediately (nonzero) instead of overlapping.

## Test first
Make the job a plain function and test idempotence and overlap.
```python
def test_job_is_idempotent(db, clock):
    clock.set("2025-01-31T00:00:00Z")
    db.add_unbilled_subscription("sub_1")
    run_billing(db, clock)
    run_billing(db, clock)          # rerun after a crash or double fire
    assert db.invoices_for("sub_1") == 1

def test_second_instance_is_skipped_when_lock_held(db):
    with db.advisory_lock("billing"):
        assert run_billing_locked(db) == "skipped"
```

## Do
- Make every job idempotent: key work by period or item id with a unique constraint, so reruns and catch-up are safe.
- Prevent overlap with a lock (`flock`, Postgres advisory lock, Redis lock with TTL, or `concurrency` in CI) and add a timeout.
- Set the timezone explicitly (`CRON_TZ`, scheduler `timezone`, systemd `OnCalendar=... Europe/Berlin`), or use UTC and document it.
- Jitter start times of many jobs (not all at `0 0 * * *`).
- Log start, end, duration, counts; alert on failure and on silence with a heartbeat or dead-man check (a ping URL after success).
- Process in batches with a checkpoint so a crash resumes.
- With multiple app instances, run the scheduler once (a leader, a dedicated worker, or a queue with repeatable jobs), not in every web process.
- Decide catch-up policy for missed runs (systemd `Persistent=true`, APScheduler `misfire_grace_time`).
- Keep a manual trigger command for the same code path.

## Avoid
- In-process timers (`setInterval`, `node-cron`) inside a scaled web app: runs N times. Use one scheduler or a lock.
- Local-time schedules without DST thought: skipped or doubled runs at 02:30. Use UTC or a zone-aware scheduler, test the transitions.
- Relying on the interactive shell environment: cron has `PATH=/usr/bin:/bin`. Use absolute paths and set variables.
- Swallowing failures: cron mails nobody. Exit nonzero, log, alert.
- Jobs longer than their interval with no lock: pile up. Lock or extend the interval.
- `*/5 * * * *` that polls what a webhook or event could push: wasted load. Prefer events.
- Day-of-month 31 or `0 0 30 2 *` assumptions: never fires in some months. Use month-end logic in code.
- Non-idempotent side effects (emails, charges) with auto retry: duplicates. Record a send key.

## Review
- [ ] Rerun and overlap are safe and tested.
- [ ] Timezone is explicit; DST cases considered.
- [ ] Failure and missed-run alerts exist.
- [ ] Only one instance triggers each job.
- [ ] Work is batched with checkpoints and has a timeout.
