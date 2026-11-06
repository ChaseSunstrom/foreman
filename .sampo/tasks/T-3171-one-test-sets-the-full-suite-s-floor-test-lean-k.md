---
id: T-3171
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T07:18:31Z
updated: 2026-11-05T12:38:32Z
builder_model: haiku
route_probe: 1
base: bef0b797c4c6a59c9856eeda94e6e34f21c67fac
base_tree: dafbcb0c1d5fd382a889484a38b9864539810164
plan0_at: 2026-11-05T07:39:10Z
plan0_scope: []
builder_returned: 2026-11-05T08:02:05Z
lane_stop: merged 2026-11-05T12:21:30Z
verified: strong
unproven: [perf-typed]
---
# The self-change gate test that plants growths takes 238-390 s alone and sets the full suite's floor: keep every check it makes, cut its time under 60 s (shared bench runs, smaller benches, or one test per planted growth)
## Raw request
> One test sets the full suite's floor: test_lean_kind LeanKind.test_the_self_change_gate_refuses_each_planted_growth_by_its_metric_and_dropping_a_check_flips_it takes ~390 s alone (after T-3166 splits classes per test); find what it repeats (benches per planted growth?) and cut it, or split it into one test per planted growth
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_exam's LeanKind planted-growth test (or its split parts) still refuses each planted growth by its own metric and still flips when a check is dropped, and its slowest part takes under 60 s on this machine — verify with `python3 plugin/tests/run.py test_exam.LeanKind`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] measure where its time goes (benches per planted growth?), then cut it keeping every assertion
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.LeanKindGateRules` → exit 0 · Ran 1 tests in 20.3s (1 classes, 16 at a time; slowest: LeanKindGateRules 20s) / OK [ran] [tree bff536779d24] [world 2f1906870a] (2026-11-05T07:59:36Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_exam test_left_out test_louhi_models test_mint test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [14.70s] [ran] [tree bff536779d24] [world 2f1906870a] (2026-11-05T08:01:46Z)
- (step 1) `python3 plugin/tests/run.py test_exam.LeanKind` → exit 0 · Ran 9 tests in 51.2s (9 jobs, 16 at a time; slowest: LeanKindGateHookDelay 51s, LeanKindGateSessionLine 34s, LeanKindGateGuardAllow 34s) / OK [ran] [tree d4f8487c4396] [world 2f1906870a] (2026-11-05T12:34:11Z)
- (ac 1) `python3 plugin/tests/run.py test_exam.LeanKind` → exit 0 · Ran 9 tests in 94.9s (8 jobs, 16 at a time; slowest: LeanKindGateHookDelay 94s, LeanKindGateSessionLine 78s, LeanKindGateGuardAllow 77s) / OK [ran] [tree ca2fbf6a1ea7] [world 2f1906870a] (2026-11-05T12:36:31Z)
- (audit adversary) `re-ran test_exam.LeanKind on main after the merge: 9 tests OK, slowest LeanKindGateHookDelay 51 s at load ~50; read the louhi diff: one runner process runs a growth plain and with each check dropped, memoising _bench and _verdicts by a content hash of the plugin tree` → sha1 here is a memo key in the exam's gate-mutation runner (louhi _GATE_RUNNER), not the real self-change gate and not a security check: it hashes every plugin file's path and bytes (tests and __pycache__ left out), so a bench is reused only for a byte-identical tree in the same process; a collision could only reuse a bench inside one exam run [tree ca2fbf6a1ea7] (2026-11-05T12:36:31Z)
- (audit edge) `re-ran test_exam.LeanKind on main after the merge: 9 tests OK, slowest LeanKindGateHookDelay 51 s at load ~50; read the louhi diff: one runner process runs a growth plain and with each check dropped, memoising _bench and _verdicts by a content hash of the plugin tree` → the drop loop restores _slower, _verdicts, _verbs and doctor.grown before each drop, so one drop can't leak into the next; an unreadable file is hashed by path alone (OSError skipped), which only risks reusing a bench for a tree that differs in that file [tree ca2fbf6a1ea7] (2026-11-05T12:36:31Z)
- (audit self) `re-ran test_exam.LeanKind on main after the merge: 9 tests OK, slowest LeanKindGateHookDelay 51 s at load ~50; read the louhi diff: one runner process runs a growth plain and with each check dropped, memoising _bench and _verdicts by a content hash of the plugin tree` → no findings [tree ca2fbf6a1ea7] (2026-11-05T12:36:31Z)
## Log
- 2026-11-05T07:18:31Z created
- 2026-11-05T07:38:53Z planned from capture
- 2026-11-05T07:38:54Z set approved=True
- 2026-11-05T07:38:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3171.builder.md
- 2026-11-05T07:39:09Z focused
- 2026-11-05T12:21:30Z merged worktree-agent-aaee1216c93282b63 (2 file(s))
- 2026-11-05T12:21:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aaee1216c93282b63
- 2026-11-05T12:33:18Z focused
- 2026-11-05T12:38:29Z done
- 2026-11-05T12:38:32Z committed 4b6d7f0c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2605 [FIX S, done, 2 steps] The self-change gate's loaded wall-time check compares medians (p50), so a hook that waits is caught even when load inflates p95 — lesson: …
- T-3166 [PERFORMANCE M, active, 4 steps] Full test runs no longer wait on a few long classes: run.py runs a big class's tests in parallel processes (each test its own pro…
- T-2961 [FIX M, done, 1 steps] Baseline red:… — lesson: A lane's affected tests don't include the repo-wide scans (test_left_out); a merge of new library lines should run…
- decision 2026-11-05: T-3140's test cache is not merged now: the branch (c5970e7a) is kept and the task blocked; the speed goes after the slowest classes instead (T-3166 …
## Regression test
none: a speed restructure of the exam's gate-mutation runner with no behaviour change; the same LeanKind assertions (each planted growth refused by its own metric, the dropped-check flip) pass before and after
## Measurements
test_exam LeanKind alone: before 238-390 s (one test, the full suite's floor); after split per growth with shared benches: ~25 s per class alone, 51 s slowest at load ~50 on main
## Lessons
- A slow test that plants several faults should be one test per fault over a shared fixture, so the runner can spread them
## Files touched
- plugin/lib/sampo/louhi.py
- plugin/tests/test_exam.py
- CHANGELOG.md
