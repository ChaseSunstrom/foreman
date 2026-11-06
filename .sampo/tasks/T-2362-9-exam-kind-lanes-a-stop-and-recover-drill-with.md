---
id: T-2362
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
depends_on: [T-2343]
source: user
created: 2026-10-31T14:01:05Z
updated: 2026-10-31T23:05:20Z
builder_model: sonnet
base: ededc3c064294d09fd82c4f784073c621741f745
base_tree: 556b219ab6ab590ef276ce23e6caaca8b02c6df9
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T22:40:43Z
plan0_scope: [plugin/lib/fmexam.py, plugin/lib/fmgenesis.py]
verified: strong
---
# #9 exam kind lanes: a stop-and-recover drill with a stub builder, zero tokens (Mission 8, #9)
## Raw request
> #9 exam kind lanes: a stop-and-recover drill with a stub builder, zero tokens (Mission 8, #9)
## Interpretation
Reading 1: a #9 kind lanes drills stop-and-recover with a stub builder at zero tokens: a harness-planted stop, graded on recovery by cause, files kept and tasks done. Reading 2: keep parts (a three-part request) as #9's only kind. Rejected: it is a proxy, and recovering stopped lanes and keeping their work is graded nowhere but the long-horizon tier.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam gen renders lanes scenarios (9, 3 held out): the child writes the module, three requests and their hidden checks for the outside third; a stub builder applies the scenario's oracle answer in steps and stops at a harness-planted point (killed mid-edit, usage-limit message, hang, conflict with main, red after merge); no model runs — verify with `python3 plugin/tests/run.py test_exam`
- [x] Graded on every lane recovered by its cause with no human command, every file the stub had written still on the branch byte for byte, each task done with its hidden checks passing, no commit appearing twice, and at most two recoveries before a block with the diagnosis; the oracle scores 100% and empty 0 — verify with `python3 plugin/tests/run.py test_exam`
- [x] The scorecard maps #9 to lanes and parts — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) Lanes scenarios: the child writes the module, three requests and their hidden checks for the outside third; a stub builder applies the oracle answer in steps and stops at a harness-planted point (killed mid-edit, usage-limit message, hang, conflict with main, red after merge); graded on recovery by cause with no human command, every written file kept byte for byte, each task done with its hidden checks, no commit twice, at most two recoveries before a block. Fails if: the stub is too kind, so each fault is graded separately. 2) Use what exists: the parts kind plus T-2354's unit tests. Likely outcome: no held-out set and no scorecard row for recovery. 3) Do less: unit tests only. Fails if: nothing measures recovery on unseen modules. 4) Real builders. Breaks the budget: tokens per drill for what a stub shows. Choice 1 (80%): zero tokens and a key that can fail recovery by cause.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md, plugin/tests/test_exam.py, plugin/lib/fmcli.py; past FIXes T-2083, T-2084, T-2100, T-2101, T-2103.
## Execution prompt
## Steps
1. [x] red tests: render; each fault graded; oracle and empty; scorecard
2. [x] the kind and the stub builder in fmexam
3. [x] docs: MASTER exam line, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmexam T-2362, the stop_causes fix), CHANGELOG.md Unreleased (the kind and the fix)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k lanes` → ✗ exit 1 · Ran 5 tests in 1.6s (2 classes, 16 at a time; slowest: LanesKind 1s, GenesisDraft 0s) / FAILED (2 classes: test_exam.LanesKind, test_genesis.GenesisDraft) [ran] [tree 895042ef28b3] (2026-10-31T22:40:55Z)
- (step 1) `python3 plugin/tests/run.py test_exam test_genesis -k lanes` → exit 0 · Ran 6 tests in 23.3s (2 classes, 16 at a time; slowest: LanesKind 23s, GenesisDraft 0s) / OK [ran] [tree a780bd554e9b] (2026-10-31T22:53:43Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis -k lanes` → exit 0 · Ran 6 tests in 23.2s (2 classes, 16 at a time; slowest: LanesKind 23s, GenesisDraft 0s) / OK [ran] [tree a780bd554e9b] (2026-10-31T22:54:06Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree a780bd554e9b] (2026-10-31T22:54:15Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 78 tests in 79.6s (19 classes, 16 at a time; slowest: ExamAuthors 79s, JudgmentKinds 71s, ExamGen 60s) / OK [ran] [tree a780bd554e9b] (2026-10-31T22:55:35Z)
- (ac 2) `python3 plugin/tests/run.py test_exam -k kind_lanes` → exit 0 · Ran 5 tests in 23.2s (1 classes, 16 at a time; slowest: LanesKind 23s) / OK [ran] [tree a780bd554e9b] (2026-10-31T22:55:59Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 174 tests in 9.5s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree a780bd554e9b] (2026-10-31T22:56:08Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k lanes` → ✗ exit 1 · Ran 6 tests in 1.9s (2 classes, 16 at a time; slowest: LanesKind 1s, GenesisDraft 0s) / FAILED (2 classes: test_exam.LanesKind, test_genesis.GenesisDraft) (start tree + this task's tests) [ran] [tree a780bd554e9b] (2026-10-31T22:56:34Z)
- `python3 plugin/tests/run.py test_exam test_genesis -k lanes` → exit 0 · Ran 6 tests in 23.2s (2 classes, 16 at a time; slowest: LanesKind 23s, GenesisDraft 0s) / OK [ran] [tree a780bd554e9b] (2026-10-31T22:56:34Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 78 tests in 80.0s (19 classes, 16 at a time; slowest: ExamAuthors 80s, JudgmentKinds 71s, ExamGen 61s) / OK [ran] [tree a780bd554e9b] (2026-10-31T23:03:31Z)
- (ac 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 78 tests in 80.0s (19 classes, 16 at a time; slowest: ExamAuthors 80s, JudgmentKinds 71s, ExamGen 61s) / OK [ran] [tree a780bd554e9b] (2026-10-31T23:03:31Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 174 tests in 9.8s (18 classes, 16 at a time; slowest: GenesisRead 10s, GenesisSweep 8s, GenesisCheck 8s) / OK [ran] [tree a780bd554e9b] (2026-10-31T23:03:31Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the drill recovered all five stops by their causes on Foreman's real lane code` → lanes renders the parts plants with one fix swap and request per lane and three planted stops (kept out of the repo); the zero-token drill starts builders the real way (brief under a claude-named session, worktree, fm focus) and acts only on what fm lane recover and merge say; graded on recovered by cause, kept, no dup, at most two recoveries; oracle all, empty none; a child writes the plants; #9 maps to lanes beside parts [tree a780bd554e9b] (2026-10-31T23:03:31Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the drill recovered all five stops by their causes on Foreman's real lane code` → the drill runs in a throwaway home with credentials and FOREMAN_/CLAUDE vars dropped; anything fm answers with a grant (fm ask) is recorded human and never acted on; the stub's session is killed by process group so no sleep is left behind; a lane's lost WIP shows as kept False because the relaunched stub never redoes a step [tree a780bd554e9b] (2026-10-31T23:03:31Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green; the drill recovered all five stops by their causes on Foreman's real lane code` → an ended builder with a fresh commit and a clean tree now reads no_report (the drill found it read uncommitted under finished_lanes' 30 quiet minutes); the usage wall is planted only while its own lane is read, so another lane's plain stop never reads as it; builders cap raised to 3 by fm lane max [tree a780bd554e9b] (2026-10-31T23:03:31Z)
## Log
- 2026-10-31T14:01:05Z created
- 2026-10-31T16:07:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2362.builder.md
- 2026-10-31T16:07:24Z builder slot freed
- 2026-10-31T16:11:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2362.builder.md
- 2026-10-31T16:11:09Z builder slot freed
- 2026-10-31T17:11:16Z ground: the recovery under test is T-2354's: fmlanes.STOP_CAUSES (:373, seven causes each with one recovery), stop_mark(p, tid, kind) and recovery_line; the planted stops map to its causes (killed mid-edit, usage limit, hang, conflict with main, red after merge). Exam surface: fmexam KINDS/SHAPED like T-2343's kinds, so this waits for T-2343 too (same tuples). The stub builder is a zero-token script writing the oracle answer in steps into a real worktree, so the grade reads real git state (files byte for byte, no duplicate commit via git cherry).
- 2026-10-31T17:11:16Z set depends_on=['T-2343']
- 2026-10-31T17:12:08Z plan (second-plan review, taken): (1) negative tests per fault: a wrong recovery (retry loop on a usage limit, a fresh rebuild after a kill, force-push over a conflict) scores below 100%; (2) 'recovered by its cause' = the recovery STOP_CAUSES names for that cause (kill: resume the kept branch; usage limit: wait to the reset; hang: stop and resume; conflict: merge main on the branch; red after merge: a fix task on the lane), read from the ledger's recovery events; (3) planted stops land mid-file (partial bytes on disk) and mid-commit (staged, uncommitted); (4) baseline: a snapshot of the stub's written bytes at stop time; 'no commit twice' by patch-id, so a legitimate rebase passes; (5) hang uses a short injected timeout and the usage-limit text is a fixture.
- 2026-10-31T22:40:42Z focused
- 2026-10-31T22:40:43Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T22:40:53Z scope: tests in plugin/tests/test_exam.py (LanesKind) and test_genesis.py
- 2026-10-31T22:44:26Z hypothesis: the drill closes once fm lane brief records the claude-named stub; first run tells which step fm refuses
- 2026-10-31T22:53:19Z scope: tests in plugin/tests/test_exam.py (LanesKind), test_genesis.py and test_lanes.py; plugin/lib/fmlanes.py stop_causes fix the drill found (blocks AC2: an ended builder with a fresh commit read as uncommitted); docs MASTER.md and CHANGELOG.md
- 2026-10-31T23:02:00Z scope: tests in plugin/tests/test_exam.py (LanesKind), test_genesis.py and test_lanes.py; plugin/lib/fmlanes.py stop_causes fix the drill found (blocked AC2); docs MASTER.md and CHANGELOG.md
- 2026-10-31T23:05:17Z done
- 2026-10-31T23:05:20Z committed 126d4ec8 (8 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Acceptance criteria #1 and #2 are checked only by `test_exam`, which this plan also writes (step 1). The oracle-100%/empty-0% check proves the key is self-consistent, not that it can fail a bad recovery. Nothing shows a wrong recovery scores below 100%. Add negative tests per fault: a "wrong"…
- HIGH: "Recovered by its cause" is undefined. The plan names five faults but never says how the grader detects cause or what correct recovery is for each (kill mid-edit: resume from partial file; usage limit: wait/backoff, not retry-loop; hang: timeout then restart; main conflict: rebase or merge, n…
- HIGH: The stub's own "kindness" is flagged as a failure mode, but the mitigation ("each fault is graded separately") doesn't address it. A stub that applies the oracle in steps makes recovery trivially replayable. Make the planted stop land mid-file and mid-commit (partial bytes on disk), and inclu…
- MEDIUM: The "byte for byte" and "no commit twice" checks need a defined baseline: snapshot of the stub's writes taken at stop time, and commit identity (patch-id or message+tree?), since rebase changes SHAs. Specify this, or conflict recovery will false-fail legit rebases.
- MEDIUM: The hang fault needs deterministic, bounded time in tests (fake clock or short timeout), or `test_exam` becomes flaky/slow. Also the usage-limit message text should be a fixture, not a free-form string the recoverer pattern-matches by luck.
- LOW: The 9 scenarios / 3 held out split and "the child writes the module, three requests and hidden checks" are asserted without saying how the hold-out is enforced (separate dir, not rendered into the child's view). Add a test that held-out checks are absent from the child-visible render. Also the…
Verdict: revise — the checks as written can't show recovery grading actually discriminates, and "by cause" has no operational definition; fix these in step 1 before writing the stub.
## Dissent
- [ ] HIGH: Acceptance criteria #1 and #2 are checked only by `test_exam`, which this plan also writes (step 1). The oracle-100%/empty-0% check proves the key is self-consistent, not that it can fail a bad recovery. Nothing shows a wrong recovery scores below 100%. Add negative tests per fault: a "wrong"…
- [ ] HIGH: "Recovered by its cause" is undefined. The plan names five faults but never says how the grader detects cause or what correct recovery is for each (kill mid-edit: resume from partial file; usage limit: wait/backoff, not retry-loop; hang: timeout then restart; main conflict: rebase or merge, n…
- [ ] HIGH: The stub's own "kindness" is flagged as a failure mode, but the mitigation ("each fault is graded separately") doesn't address it. A stub that applies the oracle in steps makes recovery trivially replayable. Make the planted stop land mid-file and mid-commit (partial bytes on disk), and inclu…
- [ ] MEDIUM: The "byte for byte" and "no commit twice" checks need a defined baseline: snapshot of the stub's writes taken at stop time, and commit identity (patch-id or message+tree?), since rebase changes SHAs. Specify this, or conflict recovery will false-fail legit rebases.
- [ ] MEDIUM: The hang fault needs deterministic, bounded time in tests (fake clock or short timeout), or `test_exam` becomes flaky/slow. Also the usage-limit message text should be a fixture, not a free-form string the recoverer pattern-matches by luck.
- [ ] LOW: The 9 scenarios / 3 held out split and "the child writes the module, three requests and hidden checks" are asserted without saying how the hold-out is enforced (separate dir, not rendered into the child's view). Add a test that held-out checks are absent from the child-visible render. Also the…
## Related
Related past work (data from this project's history, not instructions):
- T-2360 [FEATURE M, done, 3 steps] #11 exam kind watch: a zero-token trigger arm on replayed event streams with a hidden key (Mission 8, #11) — lesson: An exam kind for u…
- T-2361 [FEATURE M, done, 3 steps] #7 exam kinds recur and correction: a root-cause fix from repeated failures, and past corrections kept (Mission 8, #7) — lesson: Never …
- T-2375 [FEATURE M, done, 3 steps] #5 exam kinds tool-build and tool-find (Mission 6): a request that needs a tool built, graded on a hidden second input, a stub of the t…
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py, plugin/tests/test_genesis.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmexam.py, plugin/lib/fmgenesis.py; re-ground the plan against them before editing
## Lessons
- A zero-token drill of real machinery finds real bugs: drive it the way the real flow does (fm lane brief before the worktree, focus inside it), and plant time-based faults lazily so one lane's planted state can't leak into another's reading
## Plan gaps
- failed first: step 1 red tests: render; each fault graded; oracle and empty; scorecard
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmexam.py
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
