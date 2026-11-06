---
id: T-2497
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T19:05:34Z
updated: 2026-11-01T22:04:18Z
base: ee25fa27a9f9848fbff7108af8244c34922701bc
base_tree: 42905c5004de0fca73ad569bf02e8e06a7e410a1
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-01T21:50:48Z
plan0_scope: []
verified: strong
---
# The plan's percent against its base rate: when a plan's Choice N (NN%) sits 20+ points…
## Raw request
> FEATURE: the plan's percent against its base rate: when a plan's Choice N (NN%) sits 20+ points from the type and tier base rate (either way), the plan gate and fm next name the rate and the gap; a note, never a refusal
> DONE-WHEN: a Choice of 75% on a pair whose base rate is 96% gets one note naming both numbers; a Choice within 20 points gets none
## Interpretation
Readings: (a) likeliest: when a plan's Choice N (NN%) sits 20+ points from the base rate of its type and tier (either way: today's first rows are 75% stated on a 96% base, under), one note names both numbers where the number is stated and read: when the Approach section is written (fm task set), at focus, and in fm next while the task is active; never a refusal. (b) Refuse plans off their base rate: rejected, the user said a note, and a refusal would push numbers toward the base rate instead of toward honesty. Fails if: the pair has few closes (base_rate falls back to all closes, said in the note).
## Assumptions (confidence)
## Acceptance criteria
- [x] a Choice of 75% on a pair whose base rate is 96% gets one note naming both numbers from fm task set and fm focus, and fm next shows it while active; a Choice within 20 points gets none; no history gives none — verify with `python3 plugin/tests/run.py test_judgment.BaseRateNote`
## Non-goals
## Approach (options → choice → why)
1) fmoutcomes.base_note(p, b): the choice percent (c.stated_confidence, the gate's parser) against base_rate(type, tier), a note when 20+ apart naming both and whether the pair or all closes set the base; fm task set prints it after an Approach write, fm focus prints it, fm next shows it for the active task. Fails if: base_rate is None (no history): no note. 2) use what exists: record_stated already computes the base at focus: print there only. Fails if: the plan is written before focus (the usual order), so the note would come after the number is fixed. 3) do less: a line in fm outcomes --judgment. Fails if: it is read after the fact, never while stating. Choice 1 (85%): the note appears when the number is written and while the task runs, from the same parser and base the ledger uses.
## Risks and rollback
fm next runs every turn: base_rate reads outcomes, so the note is computed once at focus and kept in brief meta (base_note) for fm next to print. Rollback: revert; the meta key is ignored by older code.
## Execution prompt
## Steps
1. [x] red tests: BaseRateNote (task set, focus, next, within 20, no history)
2. [x] fmoutcomes.base_note + the three surfaces
3. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment.BaseRateNote` → ✗ exit 1 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: BaseRateNote 1s) / FAILED (1 classes: test_judgment.BaseRateNote) [ran] [tree c9f28f4fa7e9] (2026-11-01T21:51:28Z)
- (step 1) `python3 plugin/tests/run.py test_judgment.BaseRateNote test_cli` → exit 0 · Ran 145 tests in 35.0s (45 classes, 16 at a time; slowest: TaskLifecycle 35s, StateViews 17s, CaptureAndIntake 17s) / OK [ran] [tree 108c779141fd] (2026-11-01T21:55:24Z)
- (step 2) `python3 plugin/tests/run.py test_judgment.BaseRateNote test_cli` → exit 0 · Ran 145 tests in 33.6s (45 classes, 16 at a time; slowest: TaskLifecycle 33s, CaptureAndIntake 16s, StateViews 16s) / OK [ran] [tree 108c779141fd] (2026-11-01T21:55:59Z)
- (step 3) `python3 plugin/tests/run.py test_judgment.BaseRateNote test_cli` → exit 0 · Ran 145 tests in 37.3s (45 classes, 16 at a time; slowest: TaskLifecycle 37s, CaptureAndIntake 17s, StateViews 16s) / OK [ran] [tree 108c779141fd] (2026-11-01T21:56:37Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment.BaseRateNote` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: BaseRateNote 1s) / OK [ran] [tree 108c779141fd] (2026-11-01T22:03:27Z)
- (audit intent) `self-review: base_note reuses the gate's parser (c.stated_confidence) and the ledger's base_rate; computed when an Approach is written and at first focus, kept in meta, printed by fm next without recomputing; never raises` → Mission 2 brief 2: a plan's number meets its record while it's being stated (today's 75% on a 96% base shows as 21 points under) [tree 108c779141fd] (2026-11-01T22:03:27Z)
- (audit edge) `self-review: base_note reuses the gate's parser (c.stated_confidence) and the ledger's base_rate; computed when an Approach is written and at first focus, kept in meta, printed by fm next without recomputing; never raises` → no history, no stated choice, or within 20 points give no note; a pair with under 20 closes says the base came from all closes [tree 108c779141fd] (2026-11-01T22:03:27Z)
## Log
- 2026-11-01T19:05:34Z created
- 2026-11-01T21:37:51Z planned: it has criteria and steps
- 2026-11-01T21:37:51Z set approved=True
- 2026-11-01T21:50:48Z focused
- 2026-11-01T21:50:48Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-01T21:56:37Z scope: fmoutcomes base_note, fmcli task set/focus/next, test_judgment BaseRateNote, MASTER, CHANGELOG
- 2026-11-01T22:04:15Z done
- 2026-11-01T22:04:18Z committed 81f9205c (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2496 [FEATURE M, done, 3 steps] Ship bets: fm ship --chance NN records a write-once "ship" bet keyed by the pushed… — lesson: the fastest honest score for a stated con…
- research T-2335-review: Changes needed, but only for the MEDIUM items. I read the code and could not run it; no shell was available. The 9 PlanContent tests are green in…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
## Lessons
- a note fm next prints every turn must be computed once at a state change and kept, never recomputed per turn
## Plan gaps
- failed first: step 1 red tests: BaseRateNote (task set, focus, next, within 20, no history)
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmcli.py
- plugin/lib/fmoutcomes.py
- CHANGELOG.md
- MASTER.md
