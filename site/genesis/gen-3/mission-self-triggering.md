# Mission 1 — self-triggering (gen 3, #11)

Parent: gen-3/seed.md row 1 → gen-0.md #11: "Self-triggering. Schedules, file and event triggers, CI and issue
watchers, so work starts without me. Installs (timers, units) get queued for one yes." gen-0's goal, MUSTs and NEVERs
are quoted in the seed and apply here unchanged.

## Capability
Work that starts without the user, and a trigger layer whose silence means something. Grounded before filing: standing
orders (fm orders), the hourly model-free tick and the nightly run (fmnight.tick, T-2356), trigger routes and precision
(fm triggers, T-2276), staged installs (T-2357), timer liveness from systemd (T-2542) and a skipped night that exits 0
(T-2593) are built. The watch exam kind (T-2360) already replays events against a hidden key, so the brainstorm's top
idea, a fake-clock week harness, is a duplicate and is not filed.
What it lacks: fmnight.tick skips the CI fetch and the issue watch without a word when the repo has no watch yes, is
marked sensitive, or the network is off (fmnight.py: `repo = None if meta.get("sensitive")`, `ask = net and ci_ok …`,
`if net and repo and repo in repos`). A quiet night and a night the tick was blind read the same, in fm doctor and in
the session note.

## Grounding
- Brief 1: fmnight.tick's CI and issue branches (fmnight.py lines 400-420) skip on `meta.get("sensitive")`, a missing
  watch yes (`ci_ok`, `repos`) and `net`, and record nothing; fmdoctor.check_night_timers shows only staged, foreign
  and dead timers.

## Gaps this Mission targets (coverage: #11)
- operate × CLI and verify × headless/server: what the tick could not watch, and why, named where the user looks.
- Not in this Mission: a simulated week (the watch exam kind covers it), a canary order (no chain failure on record),
  live-tick grading (waits on the user's install; carried by the seed).

## Ideas (from the brainstorm, grounded)
### Grade the quiet gaps: say what the tick could not cover
Each tick records, per trigger kind (CI, issues), whether it was blind and why (no watch yes, sensitive, network
off). fm doctor's night-timers row and the session's Watch line name a blind kind with the one command that opens it
(fm night --watch, or why it stays shut). Prior art: cron's MAILTO reports output, not the jobs that never ran; GitHub
Actions shows skipped jobs in a run. Better by: it names the skipped trigger kinds and the reason, so quiet means quiet.

## Approaches
1. Record blind kinds in the tick's result (`res["blind"] = [(kind, why)]`), cache the newest in state, show them in
   fm doctor and the Watch line. Likely outcome: a user sees in one line that CI isn't watched and why. Fails if: the
   reason is noise every hour (shown once a day, and only when it changed).
2. use what exists: put the reasons in the tick's existing notes list. Fails if: notes are for errors, and doctor
   never reads them.
3. do less: document the conditions in the night skill. Fails if: a user never reads it at the moment it matters.

Choice: 1 (80%): one field in the tick's result and one doctor row; nothing new runs.

## Exam
The watch kind (T-2360) gains one variant per blind reason: a repo whose CI turns red while it has no watch yes, is
marked sensitive, or the tick runs with FOREMAN_NO_NET. The hidden key expects no fetch, no work started, and the tick's
result naming CI as blind with that reason; the existing watch grader reads the tick's result. The held-out share
follows the kind's split. Its unit check: a test that each of the three reasons produces its blind line and an
approved repo produces none.

## Long-horizon goal (end of run)
A user whose CI isn't watched sees, in fm doctor, that the tick is blind to it and the command that opens it.

## Lean
One list in the tick's result, one cached field, one row's text. No new verb, no hook cost.

## Tier share
Brief 1 is tier 3: self-triggering whose silence can be trusted.

## Done when
fm doctor and the session's Watch line name each trigger kind the tick could not cover, with its reason and the command
that opens it, and say nothing when every kind is covered; the watch kind's blind variants pass; the tests above pass;
MASTER.md (fmnight), CHANGELOG and the night skill's watch section say it. No site page: the night page already lists
what the tick watches, and this adds one line there.

## Briefs (fm intake)
```
FEATURE: the tick names what it could not watch: fmnight.tick records each trigger kind it skipped (CI, issues) with the reason (no watch yes, sensitive, network off); fm doctor's night-timers row and the session Watch line name each blind kind with the command that opens it, and stay quiet when every kind is covered; the watch exam kind gains a blind variant per reason; MASTER, CHANGELOG, the night skill and the site's night page say it
```
