<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Incident: stop the harm, then learn

Use when something people depend on is broken or wrong right now, or about to be: an outage, errors or slowness
users can see, wrong data being written, a security event in progress. A bug that hurts nobody yet is an ordinary
FIX (the intake skill's `references/debugging.md`). In Foreman, capture it with the urgent tag (`FIX!:`) so the current
task is checkpointed and the incident takes the focus.

The order matters more than the cleverness: impact first, mitigation second, cause last. Most incidents run long
because someone hunted the root cause while users were still failing.

## The procedure

1. **Declare it.** Open one incident record (a file, ticket or channel) with the start time in UTC and one line of
   impact in the users' terms ("checkout returns 500 for about 30% of requests"). Pass: the record exists before the
   first change to production.
2. **Name the roles.** A lead who decides, a hands-on who changes things, and (past one person) a communicator. Alone,
   you hold all three and write that down. Pass: the record names each role's holder.
3. **Triage by impact** with the severity table: who is affected, how many, since when, and is it getting worse.
   Pass: the record states the severity and the number that set it.
4. **Mitigate before you diagnose.** Reach for the reversible moves first: roll back the last deploy, turn the flag
   off, fail over, scale out, shed or block the bad traffic. Before each action write the effect you expect; after
   it, the effect you saw. Pass: every production change is a timeline row with both.
5. **Prove recovery with the signal that showed the harm**: the same graph, query or error rate, back to its normal
   band, held for 15 minutes (or two of its usual cycles, whichever is longer). "Looks fine" is not a pass.
6. **Communicate on a clock.** Updates every 30 minutes for SEV1, every 60 for SEV2, even when there is no news.
   Each update says the impact now, what was done, and when the next update comes.
7. **Keep the timeline from evidence**: deploy logs, alerts, dashboards, chat, shell history. UTC, one fact per row,
   no blame words. Mark four moments: started, detected, mitigated, resolved.
8. **Close with owned follow-ups.** SEV1 and SEV2 get a blameless review within five working days. Every follow-up
   is a ticket with an owner and a due date (in Foreman, one `fm capture` each), and at least one answers "how
   would we have known sooner". Pass: no follow-up exists only as a sentence in the review.

## Severity

| Severity | Meaning | Response |
|---|---|---|
| SEV1 | most users can't do the core job, data is lost or corrupted, or a security breach is live | all hands now, updates every 30 min, status page |
| SEV2 | a major feature or a whole segment is down, or the core job is badly degraded | owner now, updates every 60 min |
| SEV3 | degraded with a workaround, or a minor feature down | next working hours, a ticket |

When unsure, pick the higher one; lowering it later is free.

## Timeline template

| Time (UTC) | Who | What happened or was done | Expected | Seen |
|---|---|---|---|---|
| 14:02 | alert | checkout 5xx rate 31% (normal < 0.5%) | — | — |
| 14:09 | ana | rolled back deploy 812 → 811 | 5xx under 1% in 5 min | 5xx 0.4% at 14:13 |

## Checks

- [ ] The record has: UTC start, impact in user terms, severity with its number, the role holders.
- [ ] Every production change in the incident is a timeline row with expected and seen effects.
- [ ] Recovery is shown by the same signal that showed the harm, held for the watch period.
- [ ] The four moments (started, detected, mitigated, resolved) have times.
- [ ] Each follow-up is a ticket with an owner and a due date; one of them is about detection.
- [ ] The review names no person as a cause.

## Library cards

`fm lib show incident-response` (roles, comms, severity), `fm lib show postmortems` (the blameless review),
`fm lib show runbooks`, `fm lib show on-call`, `fm lib show status-pages`, `fm lib show slos-alerting` (what
should page), `fm lib show feature-flags` (the kill switch you mitigate with). Read `observability.md` next.
