---
id: T-2097
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/lib/fmcli.py, plugin/tests/test_genesis.py, plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T05:04:20Z
updated: 2026-10-30T13:56:40Z
base: e2204cf8b505dac9b5b688b20408dc480cb19f28
base_tree: 97540478a4ffa4ab682f370ad4cefe610d10159c
plan0_at: 2026-10-30T13:42:00Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/lib/fmcli.py, plugin/tests/test_genesis.py, plugin/tests/test_exam.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# fm exam scorecard: per §2 capability, the held-out split's pass rate from graded runs,…
## Raw request
> FEATURE: fm exam scorecard: per §2 capability, the held-out split's pass rate from graded runs, exit 1 when any capability is under its bar; the gate for gen-0 DONE-WHEN and §8's scorecards
## Interpretation
gen-0 DONE-WHEN needs 'every §2 capability passes its held-out exam', and §8's report a capability scorecard. fm exam scorecard [--agent foreman] [--bar 0.8]: per gen-0 §2 capability (fmgenesis._caps + _kinds), the newest graded result of each held-out scenario of its kinds from exam.jsonl lines of that agent; closed/graded and rate; state pass | under | too few (<3 graded held out) | no exam kind; #13 (a capability naming genesis) is scored on its own exam, the draft-genesis lines. Exit 1 unless every capability passes. Needs each graded line to say which scenarios it graded: fm exam grade and fm genesis exam add answered {train, holdout} ids (older lines carry none and are skipped: regrade).
## Assumptions (confidence)
## Acceptance criteria
- [x] scorecard rows: pass, under, too few, no exam kind; newest result per scenario wins; train lines never count; #13 from draft-genesis; exit 1 unless all pass — verify with `python3 plugin/tests/run.py test_genesis`
- [x] fm exam grade (oracle, real run) writes answered ids and its capability passes on the scorecard — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
Per-capability bars; G-tower (genesis session arm) as part of #13; a pane/site surface (captured follow-up); changing gen-0 or its kinds mapping.
## Approach (options → choice → why)
Score from exam.jsonl lines plus an additive answered-ids field (approach 1 of 4 in Approaches): durable after the run dir is gone, no model, no rerun.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: scorecard states + grade's answered ids
2. [x] answered ids in fmexam.grade and fmgenesis.exam lines; fmgenesis.scorecard; fm exam scorecard verb with --bar
3. [x] MASTER, CHANGELOG, help
## Resume here
<!-- auto -->
- 2026-10-30T13:52:48Z step 1/3: red tests: scorecard states + grade's answered ids
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
- touched since last checkpoint: plugin/lib/fmcli.py, CHANGELOG.md, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, MASTER.md
## Docs impact
MASTER fmexam row, CHANGELOG, exam --help
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamGen.test_a_graded_held_out_run_lands_on_the_capability_scorecard test_genesis.GenesisDraft.test_scorecard_grades_each_capability_on_its_newest_held_out_results` → ✗ exit 1 · Ran 2 tests in 1.3s (2 classes, 16 at a time; slowest: ExamGen 1s, GenesisDraft 0s) / FAILED (2 classes) [ran] [tree 72920664c511] (2026-10-30T13:44:58Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 104 tests in 26.8s (22 classes, 16 at a time; slowest: ExamGen 26s, ExamAuthors 21s, GenesisLive 18s) / OK [ran] [tree 2251115fd0b9] (2026-10-30T13:46:51Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.3s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 4ef7b92c9680] (2026-10-30T13:47:17Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.5s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree 4ef7b92c9680] (2026-10-30T13:47:26Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 26 tests in 22.0s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 4ef7b92c9680] (2026-10-30T13:47:48Z)
- (audit intent) `fm-reviewer` → met both ACs; rate over graded documented (gen-1 floor of 3 held out); #13 by name as the brief says; bar checked, unknown agent named [tree d0bed52f4308] (2026-10-30T13:51:14Z)
- (audit maintainer) `fm-reviewer` → added a real fm genesis exam answered-ids assertion; dropped unused train ids [tree d0bed52f4308] (2026-10-30T13:51:14Z)
- (audit edge) `fm-reviewer` → ok: old lines, non-list fields, non-str ids skipped; missing-tool ids split by rsplit; nan/80 bar refused [tree d0bed52f4308] (2026-10-30T13:51:14Z)
- (audit adversary) `fm-reviewer` → exam.jsonl writable through fm genesis put: captured T-2155 (pre-existing, same class as select) [tree d0bed52f4308] (2026-10-30T13:51:14Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 104 tests in 21.9s (22 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 14s, ExamRust 12s) / OK [ran] [tree d0bed52f4308] (2026-10-30T13:51:41Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.5s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree d0bed52f4308] (2026-10-30T13:51:46Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 26 tests in 22.4s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree d0bed52f4308] (2026-10-30T13:52:08Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.4s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree d0bed52f4308] (2026-10-30T13:52:17Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 78 tests in 4.7s (12 classes, 16 at a time; slowest: GenesisLive 4s, GenesisSweep 4s, GenesisCheck 3s) / OK [ran] [tree d0bed52f4308] (2026-10-30T13:53:11Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 26 tests in 21.8s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 12s, ExamRust 12s) / OK [ran] [tree d0bed52f4308] (2026-10-30T13:53:11Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis test_docs` → exit 0 · Ran 184 tests in 19.7s (43 classes, 16 at a time; slowest: ExamGen 19s, ExamAuthors 13s, ExamRust 13s) / OK [ran] [tree d0bed52f4308] (2026-10-30T13:53:11Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 findings fixed, 1 captured T-2155` → old lines without answered ids, non-list fields and non-str ids are skipped; missing-tool ids parse; a bar of 80 or nan is refused [tree d0bed52f4308] (2026-10-30T13:53:11Z)
## Log
- 2026-10-30T05:04:20Z created
- 2026-10-30T13:41:54Z set type=FEATURE, tier=M, scope=['plugin/lib/fmexam.py', 'plugin/lib/fmgenesis.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_genesis.py', 'plugin/tests/test_exam.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-30T13:41:54Z planned: it has criteria and steps
- 2026-10-30T13:41:59Z focused
- 2026-10-30T13:53:51Z done
- 2026-10-30T13:53:53Z committed 8b675f9d (7 files)
- 2026-10-30T13:54:20Z guard authorization added: publish
- 2026-10-30T13:56:40Z publish grant used by fm ship
## Follow-ups captured
## Approaches
1 (chosen) score from exam.jsonl lines + an additive answered-ids field: durable after the run dir is gone, no model, no rerun. 2 re-derive answered ids from the run's answers dir: breaks once runs are tidied. 3 re-grade on the fly: reruns hidden checks, slow. 4 per-kind counts in the line: loses newest-per-scenario.
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- decision 2026-10-30: Genesis selection (fm genesis select) scores the exam's train split, never the held-out third; held-out only grades a capability done
- similar finished tasks took 4–5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Lessons
- A gate that reads hand-written fixture lines needs one test through the real writer too: the scorecard test built exam.jsonl lines itself, so dropping answered= from fm genesis exam passed every test
## Plan gaps
- failed first: step 1 red tests: scorecard states + grade's answered ids
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/test_exam.py
- plugin/lib/fmcli.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
