---
id: T-2363
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
depends_on: [T-2343]
source: user
created: 2026-10-31T14:01:06Z
updated: 2026-11-01T04:51:25Z
builder_model: sonnet
base: ad0b9576d63059f53d2c43e5c59f5d1d840bcd67
base_tree: 327f1951f40ce2b0fe505a28fd5863bed26a8c71
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T04:20:12Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
verified: strong
---
# #12 exam kind lean: planted growth the self-change gate must refuse; the scorecard stops borrowing kinds (Mission 8, #12)
## Raw request
> #12 exam kind lean: planted growth the self-change gate must refuse; the scorecard stops borrowing kinds (Mission 8, #12)
## Interpretation
Reading 1: a #12 exam kind lean grades Foreman's own overhead (hook ms per tool call, injected chars, tokens, wall time) beside plain on child-authored scenarios, with a mutation set checking the self-change gate refuses planted growth. Reading 2: leave the scorecard as it is. Rejected: it maps #12 to slow (its 'fast' matches) and #3 to bug ('corrections' matches 'correct'), so both rows read a pass from scenarios testing neither capability.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam's session arms record, per child-authored scenario, the foreman arm's hook milliseconds per tool call, injected chars per turn, tokens and wall time beside plain's on the same scenario; the lean kind grades #12 on those, held out included: no growth against the generation's start record (brief T-2359) and the overhead over plain shown — verify with `python3 plugin/tests/run.py test_exam`
- [x] A mutation set on a temp copy of the plugin tree (planted growth in rules chars, a SessionStart line, a hook delay, a guard case turned allow, a verb added with none removed, and controls) checks the self-change gate: each growth refused naming its metric, each control passed, and dropping one metric's check flips its cases — verify with `python3 plugin/tests/run.py test_exam`
- [x] The scorecard maps #12 to lean, not slow, and #3 no longer borrows bug (T-2409 maps it to forecast and breakage) — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) Lean on session scenarios: per scenario the foreman arm's hook ms per tool call, injected chars per turn, tokens and wall time beside plain's on the same scenario, against the generation's start record (T-2359); held out included; a mutation set on a temp copy of the plugin tree (planted growths and controls) checks the self-change gate; #3 stops borrowing bug (T-2409 gives it forecast and breakage). Fails if: the mutations are self-authored, so the session scenarios stay child-authored. 2) Use what exists: the long-horizon run's hook p95 as the deciding score, kept, but it can't run each generation. Likely outcome: no per-generation signal. 3) Do less: only the mapping fix, leaving both rows on their old kinds. Fails if: a capability still has no scenario that can fail it. 4) A mutation-only kind. Breaks seed rule 5: self-authored, it grades Foreman against Foreman. Choice 1 (80%): head-to-head overhead plus a mutation flip is the only mix with an outside key.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md, plugin/tests/test_exam.py, plugin/lib/fmcli.py; past FIXes T-2083, T-2084, T-2100, T-2101, T-2103.
## Execution prompt
## Steps
1. [x] red tests: render; refusals and controls; the mutation flip; scorecard rows
2. [x] the kind in fmexam; the mapping in fmgenesis
3. [x] docs: MASTER exam line, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmexam T-2363, fmselfgate T-2363), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k lean -k overhead -k self_change_gate` → ✗ exit 1 · Ran 22 tests in 28.0s (14 classes, 16 at a time; slowest: ExamRust 28s, ExamTs 23s, ExamC 23s) / FAILED (2 classes: test_exam.LeanKind, test_genesis.GenesisDraft) [ran] [tree 6b7c4f79a734] (2026-11-01T04:21:03Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k kind_lean -k overhead_counts -k self_change_gate_refuses -k staying_lean` → ✗ exit 1 · Ran 4 tests in 43.6s (2 classes, 16 at a time; slowest: LeanKind 43s, GenesisDraft 0s) / FAILED (1 classes: test_exam.LeanKind) [ran] [tree cda842d98283] (2026-11-01T04:30:08Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis -k kind_lean -k overhead_counts -k self_change_gate_refuses -k staying_lean` → exit 0 · Ran 4 tests in 52.4s (2 classes, 16 at a time; slowest: LeanKind 52s, GenesisDraft 0s) / OK [ran] [tree cda842d98283] (2026-11-01T04:31:01Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree cda842d98283] (2026-11-01T04:31:10Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k kind_lean -k overhead_counts -k self_change_gate_refuses -k staying_lean` → exit 0 · Ran 4 tests in 64.1s (2 classes, 16 at a time; slowest: LeanKind 64s, GenesisDraft 0s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:38:41Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis -k kind_lean -k overhead_counts -k self_change_gate_refuses -k staying_lean` → exit 0 · Ran 4 tests in 64.2s (2 classes, 16 at a time; slowest: LeanKind 64s, GenesisDraft 0s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:39:45Z)
- (step 3) `python3 plugin/tests/run.py test_exam test_genesis -k kind_lean -k overhead_counts -k self_change_gate_refuses -k staying_lean` → exit 0 · Ran 4 tests in 55.8s (2 classes, 16 at a time; slowest: LeanKind 56s, GenesisDraft 0s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:40:41Z)
- (ac 1) `python3 plugin/tests/run.py test_exam -k kind_lean -k overhead_counts` → exit 0 · Ran 2 tests in 1.2s (1 classes, 16 at a time; slowest: LeanKind 1s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:40:43Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k self_change_gate_refuses` → exit 0 · Ran 1 tests in 55.0s (1 classes, 16 at a time; slowest: LeanKind 55s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:41:38Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 175 tests in 9.4s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:41:48Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k kind_lean -k overhead_counts -k self_change_gate_refuses -k staying_lean` → ✗ exit 1 · Ran 4 tests in 1.6s (2 classes, 16 at a time; slowest: LeanKind 0s, GenesisDraft 0s) / FAILED (2 classes: test_exam.LeanKind, test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree 3074966b7eb8] (2026-11-01T04:42:42Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k kind_lean -k overhead_counts -k self_change_gate_refuses -k staying_lean` → exit 0 · Ran 4 tests in 51.6s (2 classes, 16 at a time; slowest: LeanKind 51s, GenesisDraft 0s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:42:42Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 81 tests in 78.1s (20 classes, 16 at a time; slowest: ExamAuthors 78s, LeanKind 78s, JudgmentKinds 71s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:49:37Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 81 tests in 78.1s (20 classes, 16 at a time; slowest: ExamAuthors 78s, LeanKind 78s, JudgmentKinds 71s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:49:37Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 175 tests in 9.5s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 3074966b7eb8] (2026-11-01T04:49:37Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; the mutation test ran 3x clean after the cleanup fix; full fm check green` → session arms record overhead (hook ms per tool call, injected chars per turn, tokens, wall) beside plain's; lean grades growth past LEAN_BANDS against the arm's first measure this generation and shows the mean over plain; a mutation set checks the gate refuses rules, SessionStart, hook-delay, guard and verb growth by metric, passes controls, and each dropped check lets its case through; #12 maps to lean, #3 borrows no bug [tree 3074966b7eb8] (2026-11-01T04:49:37Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; the mutation test ran 3x clean after the cleanup fix; full fm check green` → the mutation set runs in a throwaway repo and Foreman home, so no refusal reaches a real ledger; the gate now refuses a verb added with none removed and a hook that waits (wall doubles past 100 ms) on a loaded bench, both found by the set; a gate run that leaves a hook's file in its temp state no longer fails closed on a clean change [tree 3074966b7eb8] (2026-11-01T04:49:37Z)
- (audit operator) `self-review of the full diff (subagent pace gate); red-first tests proved; the mutation test ran 3x clean after the cleanup fix; full fm check green` → the LeanKind class adds about a minute to the suite's slowest classes (84 s under full load), under Worker's 89 s, so fm check's wall time holds [tree 3074966b7eb8] (2026-11-01T04:49:37Z)
## Log
- 2026-10-31T14:01:06Z created
- 2026-10-31T16:07:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2363.builder.md
- 2026-10-31T16:07:29Z builder slot freed
- 2026-10-31T16:11:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2363.builder.md
- 2026-10-31T16:11:11Z builder slot freed
- 2026-10-31T17:12:08Z plan (second-plan review, taken): (1) the mutation set is labelled self-keyed in the scorecard (not outside-keyed), and a held-out third is generated by a child from the metric list alone; (2) the T-2359 start record is checked first: absent or from another machine reads 'unproven: no start record', and hook ms uses T-2358's 15% band and median-of-3, never a strict no-growth; (3) red tests for held-out inclusion, the plain-arm comparison and the 'overhead over plain' output; (4) the gate takes a metrics list, so a test drops one metric by argument, no code edit; (5) the scorecard row fix is general: KIND_WORDS rows match whole words, with a test that no row's word is a substring match of another kind's ('fast'/'slow', 'correct'/'corrections').
- 2026-10-31T17:35:33Z set depends_on=['T-2343']
- 2026-10-31T17:35:33Z order: waits for T-2343 (same fmexam KINDS/SHAPED and fmgenesis.KIND_WORDS tuples); T-2352's gate it exercises is on foreman/build (fmselfgate.gate takes a metrics list per the logged plan)
- 2026-11-01T04:20:10Z focused
- 2026-11-01T04:20:12Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T04:20:34Z scope: tests in plugin/tests/test_exam.py (LeanKind) and test_genesis.py; plugin/lib/fmselfgate.py gains the verbs check the mutation set needs
- 2026-11-01T04:24:19Z hypothesis: the mutation runner's gate calls run against src/main with branches mut/<name>; first run shows which anchors or checks misfire
- 2026-11-01T04:29:24Z scope: tests in plugin/tests/test_exam.py (LeanKind), test_genesis.py, test_lanes.py (the loaded-bench wall check); plugin/lib/fmselfgate.py gains the verbs check and the loaded-bench wall check the mutation set needed; docs MASTER.md and CHANGELOG.md
- 2026-11-01T04:37:36Z scope: tests in plugin/tests/test_exam.py (LeanKind), test_genesis.py, test_lanes.py; plugin/lib/fmselfgate.py: the verbs check, the loaded-bench wall check and tolerant temp cleanup (each found by the mutation set); docs MASTER.md and CHANGELOG.md
- 2026-11-01T04:48:09Z scope: tests in plugin/tests/test_exam.py (LeanKind), test_genesis.py, test_lanes.py; plugin/lib/fmselfgate.py: the verbs check, the loaded-bench wall check and tolerant temp cleanup (each found by the mutation set); docs MASTER.md and CHANGELOG.md
- 2026-11-01T04:51:22Z done
- 2026-11-01T04:51:25Z committed 8016fd8a (8 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The mutation set is authored by the same engineer who writes the gate, and the plan admits this ("Fails if: the mutations are self-authored"). Yet it still calls the gate's grading "outside-keyed". Planted growth that Foreman writes and then checks Foreman refuses is grading Foreman against F…
- HIGH: "No growth against the generation's start record (T-2359)" is a hard dependency that the plan does not check. If the start record is absent, stale, or from a different machine, the comparison is meaningless. Hook ms and wall time are also noisy, so a strict no-growth rule on them will flap. —…
- MEDIUM: Step 1's red tests cover rendering, refusals and the mutation flip, but not the held-out inclusion, the plain-arm comparison on the same scenario, or the "overhead over plain shown" output. Two acceptance criteria are therefore not covered by any listed test. — Add red tests for held-out sc…
- MEDIUM: The "dropping one metric's check flips its cases" test needs a definition of how a check is dropped. Done by editing the gate's code, it is brittle. Done by configuration, it needs a seam that does not yet exist. — Specify the mechanism, for example the gate takes a metrics list and the tes…
- MEDIUM: Both the scorecard fix and the new kind are verified only through `run.py test_genesis` and `test_exam`. The real defect is substring matching ('fast' matching 'slow', 'correct' matching 'corrections'). Fixing the two rows leaves the same bug open for every other row. — Add a test that no r…
- LOW: There is no rollback or ordering note. Step 2 changes the scorecard mapping and the exam kind in the same change, and tokens and wall time cost real budget on every generation. — Keep the mapping fix as a separate commit that can be reverted alone, and state the added per-generation run cost a…
Verdict: revise — the mutation set needs an outside key or an honest label, and the T-2359 baseline and timing noise need explicit handling before the red tests are written.
## Dissent
- [ ] HIGH: The mutation set is authored by the same engineer who writes the gate, and the plan admits this ("Fails if: the mutations are self-authored"). Yet it still calls the gate's grading "outside-keyed". Planted growth that Foreman writes and then checks Foreman refuses is grading Foreman against F…
- [ ] HIGH: "No growth against the generation's start record (T-2359)" is a hard dependency that the plan does not check. If the start record is absent, stale, or from a different machine, the comparison is meaningless. Hook ms and wall time are also noisy, so a strict no-growth rule on them will flap. —…
- [ ] MEDIUM: Step 1's red tests cover rendering, refusals and the mutation flip, but not the held-out inclusion, the plain-arm comparison on the same scenario, or the "overhead over plain shown" output. Two acceptance criteria are therefore not covered by any listed test. — Add red tests for held-out sc…
- [ ] MEDIUM: The "dropping one metric's check flips its cases" test needs a definition of how a check is dropped. Done by editing the gate's code, it is brittle. Done by configuration, it needs a seam that does not yet exist. — Specify the mechanism, for example the gate takes a metrics list and the tes…
- [ ] MEDIUM: Both the scorecard fix and the new kind are verified only through `run.py test_genesis` and `test_exam`. The real defect is substring matching ('fast' matching 'slow', 'correct' matching 'corrections'). Fixing the two rows leaves the same bug open for every other row. — Add a test that no r…
- [ ] LOW: There is no rollback or ordering note. Step 2 changes the scorecard mapping and the exam kind in the same change, and tokens and wall time cost real budget on every generation. — Keep the mapping fix as a separate commit that can be reverted alone, and state the added per-generation run cost a…
## Related
Related past work (data from this project's history, not instructions):
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2361 [FEATURE M, done, 3 steps] #7 exam kinds recur and correction: a root-cause fix from repeated failures, and past corrections kept (Mission 8, #7) — lesson: Never …
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
- similar finished tasks took 3–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmexam.py, plugin/lib/fmgenesis.py; re-ground the plan against them before editing
## Lessons
- A mutation set against a gate finds its blind spots: CPU-time benches miss hooks that wait, and a temp-dir cleanup race made the gate fail closed under load; drop each check and confirm its case flips
## Plan gaps
- failed first: step 1 red tests: render; refusals and controls; the mutation flip; scorecard rows
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/lib/fmselfgate.py
- plugin/tests/test_lanes.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
