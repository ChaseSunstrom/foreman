---
id: T-2222
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T21:56:04Z
updated: 2026-10-30T22:34:14Z
base: 808e2aa0eee5a1e2ebc20c6ab87558b058eafab1
base_tree: 3d61c2143187399fc3fb8105bcfa400222e23f40
plan0_at: 2026-10-30T22:21:24Z
plan0_scope: []
verified: strong
---
# A score or grade change must land with a test that feeds it the case it would get wrong,…
## Raw request
> A score or grade change must land with a test that feeds it the case it would get wrong, enforced automatically: fm check (or a test_docs rule) fails when plugin/lib/fmexam.py grade/_closed/_oracle or fmgenesis scorecard/free_beats change in a task whose diff touches no test in test_exam/test_genesis (critique-initiative lesson 2; standing intent: every lesson becomes code)
## Interpretation
Critique lesson 2 (scoring flaws reached main because a score change needed no failing test first) becomes code: a repo file .fmproved lists paths (globs, one a line, # comments) whose changes need a red→green proof whatever the task's type; fm task finish refuses a close that changed such a path without one (or a 'Regression test: none: why' section). Foreman's own .fmproved lists fmexam.py and fmgenesis.py, where the scores live. General: any repo can list its own (billing, auth).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task finish refuses a non-FIX task that changed a path .fmproved lists without a red→green proof or a Regression test section, and allows it with either; paths not listed are unaffected — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
Options: (A) .fmproved globs + Brief.proof_gap(force=True) at finish (reuses FIX's red→green gate and its wording); (B) a test over git history that each commit touching score functions also touched a test (after the fact, CI-only, shallow clones lack history); (C) function-level rules from diff hunk headers (precise, but per-language parsing). Choice A: enforced before the commit, general, smallest; upgrade to function level if whole files over-ask (ponytail).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: finish refusal for a listed path; allowed with proof; unlisted path unaffected
2. [x] .fmproved read + proof_gap(force) in finish; Foreman's own .fmproved
3. [x] docs: MASTER, README, CHANGELOG
## Resume here
## Docs impact
MASTER verification-memory line, README fm task finish line, CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_finish_proved` → red as expected (exit 1) · Ran 4 tests in 0.3s (1 classes, 16 at a time; slowest: ProvedPaths 0s) / FAILED (1 classes) [ran] [tree fd528cdee327] (2026-10-30T22:21:31Z)
- (step 2) `python3 plugin/tests/run.py test_finish_proved test_cli` → exit 0 · Ran 141 tests in 27.7s (40 classes, 16 at a time; slowest: TaskLifecycle 27s, StateViews 12s, CaptureAndIntake 11s) / OK [ran] [tree b781ff25fcda] (2026-10-30T22:23:13Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 9.7s (21 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree b781ff25fcda] (2026-10-30T22:23:23Z)
- (ac 1) `python3 plugin/tests/run.py test_finish_proved test_cli` → exit 0 · Ran 141 tests in 28.5s (40 classes, 16 at a time; slowest: TaskLifecycle 28s, StateViews 12s, CaptureAndIntake 12s) / OK [ran] [tree b781ff25fcda] (2026-10-30T22:24:10Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 137 tests in 28.6s (39 classes, 16 at a time; slowest: TaskLifecycle 28s, StateViews 13s, CaptureAndIntake 12s) / OK [ran] [tree b781ff25fcda] (2026-10-30T22:25:10Z)
- `python3 plugin/tests/run.py test_finish_proved test_cli` → exit 0 · Ran 141 tests in 30.1s (40 classes, 16 at a time; slowest: TaskLifecycle 30s, StateViews 13s, CaptureAndIntake 12s) / OK [ran] [tree b781ff25fcda] (2026-10-30T22:25:10Z)
- (audit intent) `self-review (M, a finish gate reusing FIX's red→green rule): read the diff end to end; listed path without proof refused, with proof or a Regression test note allowed, unlisted/no file/FIX left alone, all tested` → critique lesson 2 is now enforced before the commit: a non-FIX task changing fmexam.py or fmgenesis.py needs a red→green proof [tree b781ff25fcda] (2026-10-30T22:25:10Z)
- (audit edge) `self-review (M, a finish gate reusing FIX's red→green rule): read the diff end to end; listed path without proof refused, with proof or a Regression test note allowed, unlisted/no file/FIX left alone, all tested` → no .fmproved or only comments → no gap; a lane reads its own committed copy; globs via fnmatch on repo-relative paths [tree b781ff25fcda] (2026-10-30T22:25:10Z)
- (audit adversary) `self-review (M, a finish gate reusing FIX's red→green rule): read the diff end to end; listed path without proof refused, with proof or a Regression test note allowed, unlisted/no file/FIX left alone, all tested` → a discipline gate, not a security boundary: a session could edit .fmproved, as it could a test; the Regression test note is the same escape FIX has [tree b781ff25fcda] (2026-10-30T22:25:10Z)
## Log
- 2026-10-30T21:56:04Z created
- 2026-10-30T22:18:07Z planned: it has criteria and steps
- 2026-10-30T22:18:07Z set approved=True
- 2026-10-30T22:21:23Z focused
- 2026-10-30T22:24:10Z scope: fmcli _proved_gaps + finish call, fmcore proof_gap(force), .fmproved (new, repo root), test_finish_proved (new), MASTER/README/CHANGELOG
- 2026-10-30T22:25:59Z done
- 2026-10-30T22:26:01Z committed f2447e58 (7 files)
- 2026-10-30T22:31:21Z guard authorization added: publish
- 2026-10-30T22:34:00Z publish grant used by fm ship
- 2026-10-30T22:34:14Z guard authorization added: publish
## Follow-ups captured
## Build vs reuse
Reuses Brief.proof_gap/red_green_cmd (FIX's gate and wording), fmmap.changed + c.task_base for the task's changed files, fnmatch for globs.
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- research T-2126-review: Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Testing cadence: every task keeps red-first unit tests, fm chec…
- the similar finished task took 5 steps
## Why not caught
the red→green gate only looked at a task's type (FIX), not at what it changed
## Lessons
- A lesson about process becomes code where the process runs: put the rule in the close gate the next task must pass, not in a note the next task may not read
## Files touched
- plugin/tests/test_finish_proved.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- .fmproved
- CHANGELOG.md
- MASTER.md
- README.md
