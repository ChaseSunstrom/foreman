---
id: T-2961
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-11-04T12:34:32Z
updated: 2026-11-04T12:39:23Z
trigger: baseline
trigger_key: e4dae617b182a761
baseline: true
base: f4a124dfc702c6165c75e798b2f6975c3a7f309c
base_tree: ee6600f5129778e49344d76864c17702ce9afe90
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-04T12:37:13Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# Baseline red:…
## Raw request
> Baseline red: `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py` fails test_exam.LeanKind.test_the_self_change_gate_refuses_each_planted_growth_by_its_metric_and_dropping_a_check_flips_it, test_left_out.LeftOut.test_no_silent_cut_in_fmcli. Captured by sampo check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
Reading 1 (chosen): the ship's scratch-tree suite had two reds: test_left_out found T-2945's unmarked [:60] cut in louhi.py (real, fix it), and LeanKind's hook-delay plant measured no bench rows at load 30 (it passes off load). Reading 2 (ruled out): the self-change gate is broken; it passes here at normal load, as it did in the 11:34 full check.
## Assumptions (confidence)
## Acceptance criteria
- [x] no silent [:N] cut in louhi (the T-2945 planner line carries the not-a-list marker); test_exam.LeanKind passes off load — verify with `python3 plugin/tests/run.py test_left_out test_exam`
## Non-goals
## Approach (options → choice → why)
1) Mark the cut like the model line beside it (# not a list: a name cut at 60 characters). Likely outcome: test_left_out green. Fails if: the scan wants c.fit instead, which the sibling line shows it doesn't.
2) use what exists: c.fit(c.plain(planner), 60). Likely outcome: green too, but an ellipsis lands in a file other code reads back. Fails if: a reader compares the name.
3) do less: nothing for LeanKind; it is load. Likely outcome: the next ship at lower load passes. Fails if: it is not load, which the off-load pass rules out.
Choice 1 (90%): matches the sibling line.
## Risks and rollback
## Execution prompt
## Steps
1. [x] mark louhi.py's planner cut like the model line beside it; rerun LeanKind at normal load
## Resume here
## Docs impact
none: a code comment
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_left_out test_exam` → exit 0 · Ran 112 tests in 95.9s (28 classes, 16 at a time; slowest: LeanKind 96s, ExamAuthors 79s, JudgmentKinds 74s) / OK [ran] [tree 4563dfdc5760] [world 2f1906870a] (2026-11-04T12:38:55Z)
- (ac 1) `python3 plugin/tests/run.py test_left_out test_exam` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T12:38:55Z [ran] [tree 4563dfdc5760] [world 2f1906870a] (2026-11-04T12:39:02Z)
- (audit intent) `self: the scan's own message named the line; the marker matches the model line beside it; LeanKind rerun at normal load passed (112 tests with test_exam)` → louhi's planner name cut carries the not-a-list marker, so test_left_out passes; LeanKind's hook-delay red was the 30-load ship host, it passes off load [tree 4563dfdc5760] (2026-11-04T12:39:02Z)
- (audit edge) `self: the scan's own message named the line; the marker matches the model line beside it; LeanKind rerun at normal load passed (112 tests with test_exam)` → a planner name over 60 characters is still cut in the answers file, as the model name beside it is [tree 4563dfdc5760] (2026-11-04T12:39:02Z)
## Log
- 2026-11-04T12:34:32Z created
- 2026-11-04T12:37:03Z planned: it has criteria and steps
- 2026-11-04T12:37:12Z focused
- 2026-11-04T12:37:13Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-04T12:39:21Z done
- 2026-11-04T12:39:23Z committed 0c4056bb (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2814 [FIX S, done, 2 steps] Baseline red:… — lesson: Run the suite on the oldest supported Python before shipping: argparse's subparser prog changed in 3.14
- T-2429 [FIX M, done, 1 steps] Baseline red:… — lesson: A test that appends then shifts an mtime is shifting from the wall clock: read the mtime before the write
- T-2286 [FIX M, dropped, 0 steps] Baseline red:…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar finished tasks took 1–2 steps
- start here (files T-2814 touched): plugin/lib/sampo/cli.py
## Regression test
none new: test_left_out.test_no_silent_cut_in_fmcli is the existing test that caught it, red in the ship's scratch tree (ship-4 log, louhi.py:3526) and green now
## Why not caught
T-2945's lane ran its affected tests, not test_left_out, which scans every module; the full suite found it
## Lessons
- A lane's affected tests don't include the repo-wide scans (test_left_out); a merge of new library lines should run them
## Files touched
- plugin/lib/sampo/louhi.py
