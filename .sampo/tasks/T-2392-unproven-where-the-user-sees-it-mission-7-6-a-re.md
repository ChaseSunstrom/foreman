---
id: T-2392
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2391]
source: user
created: 2026-10-31T14:03:23Z
updated: 2026-10-31T21:01:46Z
builder_model: sonnet
base: 93b4ae337ce170f01ee683a8e894b9aae6f54617
base_tree: ee4f01a01c2fab04fcaf7f539fcdc25647557ce1
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T20:53:30Z
plan0_scope: []
verified: strong
---
# Unproven where the user sees it (Mission 7, #6): a reply claiming a measured number, accurate docs, a working migration, a rendered UI or a release with no run of that kind is held once, and commits and PRs carry an Unproven line
## Raw request
> Unproven where the user sees it (Mission 7, #6): a reply claiming a measured number, accurate docs, a working migration, a rendered UI or a release with no run of that kind is held once, and commits and PRs carry an Unproven line
## Interpretation
Reading 1: a reply claiming a measured number, accurate docs, a working migration, a rendered UI or a release with no run of that kind is held once at Stop, and commits and PRs carry an Unproven line. Reading 2: a model reads each reply for unbacked claims. Rejected: a model call per Stop and a model judging a model.
## Assumptions (confidence)
## Acceptance criteria
- [x] The Stop hook holds once a reply whose claim names a proof kind (a speedup or other measured number, docs accurate or updated, a migration that works or reverses, a UI that looks or renders right, released, deployed or published) when the active task has no green run of that kind and the turn ran none, naming the claim, the kind and its upgrade command, or asking to say it is unproven; a negated or conditional claim, or one whose run exists, passes; its regex runs first and the brief is read only on a match — verify with `python3 plugin/tests/run.py test_hooks -k proof_claim`
- [x] fm task finish --commit adds an 'Unproven: <kinds>' trailer when the closed task is in the rollup, and fm pr's body lists the same kinds per task — verify with `python3 plugin/tests/run.py test_bookkeeping -k unproven_trailer`
- [x] A claim the next reply keeps after its hold, still with no run of its kind and no unproven label, is labelled for the user by the Stop hook's own message (systemMessage) and recorded on the task as unproven (its log, its rollup row, the commit trailer), so no unbacked claim reaches the user unlabelled — verify with `python3 plugin/tests/run.py test_hooks -k proof_claim_kept`
## Non-goals
## Approach (options → choice → why)
1) Widen the Stop claims gate beside _claims_gate to proof kinds using the kinds table's clearing runs, once per claim; the trailer in the commit path and the section in fm pr; hook p95 measured before and after with fm doctor. Fails if: a negated claim ('not faster') trips it, which a negation test pins. 2) Use what exists: _claims_gate, which checks test-pass claims only (T-0886), and finish's Not verified list. Likely outcome: 'faster' or 'docs updated' passes with nothing behind it. 3) Do less: the trailer only, no Stop gate. Fails if: the reply, where the user reads the result, is unchecked. 4) Block the close on unbacked claims. Breaks the drive: a hold once never traps a session (DRIVE_MAX counts it). Choice 1 (80%): the gate stays cheap, deterministic and once per claim.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: a perf claim with no bench, the same claim with one, a negated claim; a commit of a task closed on typed evidence
2. [x] claim patterns per kind beside the kinds table; the Stop gate beside _claims_gate, once per claim
3. [x] the trailer in the commit path and the section in fm pr
4. [x] hook p95 before and after (fm doctor); MASTER.md, README, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks -k proof_claim` → exit 0 · Ran 2 tests in 1.8s (1 classes, 16 at a time; slowest: Stop 2s) / OK [ran] [tree 7cb154154f73] (2026-10-31T20:59:58Z)
- (step 2) `python3 plugin/tests/run.py test_hooks -k proof_claim` → exit 0 · Ran 2 tests in 1.8s (1 classes, 16 at a time; slowest: Stop 2s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:01Z)
- (step 3) `python3 plugin/tests/run.py test_bookkeeping -k unproven_trailer` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: UnprovenTrailer 1s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:03Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:12Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks -k proof_claim` → exit 0 · Ran 2 tests in 1.8s (1 classes, 16 at a time; slowest: Stop 2s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:14Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks -k proof_claim` → exit 0 · Ran 2 tests in 1.8s (1 classes, 16 at a time; slowest: Stop 2s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:17Z)
- (ac 2) `python3 plugin/tests/run.py test_bookkeeping -k unproven_trailer` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: UnprovenTrailer 1s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:19Z)
- `python3 plugin/tests/run.py test_hooks -k proof_claim` → ✗ exit 1 · Ran 2 tests in 2.6s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 7cb154154f73] (2026-10-31T21:00:24Z)
- `python3 plugin/tests/run.py test_hooks -k proof_claim` → exit 0 · Ran 2 tests in 1.8s (1 classes, 16 at a time; slowest: Stop 2s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:24Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks -k proof_claim` → exit 0 · Ran 2 tests in 1.8s (1 classes, 16 at a time; slowest: Stop 2s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:41Z)
- (ac 2) `python3 plugin/tests/run.py test_bookkeeping -k unproven_trailer` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: UnprovenTrailer 1s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:41Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks -k proof_claim_kept` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 7cb154154f73] (2026-10-31T21:00:41Z)
- (audit intent) `main-thread review (pace gate holds): the gate is regexes first (five patterns over the reply), the brief and transcript only on a match; a hold is once per kind and session (the existing claims list, capped at 50), so it can't trap a drive; a kept claim is labelled and recorded, never blocked twice; the trailer and the PR section read the same rollup (proof_needs), never a second list; a rollup read failing never fails a commit or a PR` → a perf number with no bench is held naming the claim, the kind, the task and --bench; a bench this turn, a negated claim, a conditional one ('if it ends up 3x faster') and one said unproven pass; a kept migration claim is labelled in systemMessage and recorded (meta, log); the commit trailer and fm pr name the kinds; a proven task's commit has none [tree 7cb154154f73] (2026-10-31T21:00:41Z)
- (audit edge) `main-thread review (pace gate holds): the gate is regexes first (five patterns over the reply), the brief and transcript only on a match; a hold is once per kind and session (the existing claims list, capped at 50), so it can't trap a drive; a kept claim is labelled and recorded, never blocked twice; the trailer and the PR section read the same rollup (proof_needs), never a second list; a rollup read failing never fails a commit or a PR` → 'released' needs a version, 'it' or a target, so 'the lock is released' doesn't trip; the docs claim needs fm prove --docs, not any run [tree 7cb154154f73] (2026-10-31T21:00:41Z)
- (audit operator) `main-thread review (pace gate holds): the gate is regexes first (five patterns over the reply), the brief and transcript only on a match; a hold is once per kind and session (the existing claims list, capped at 50), so it can't trap a drive; a kept claim is labelled and recorded, never blocked twice; the trailer and the PR section read the same rollup (proof_needs), never a second list; a rollup read failing never fails a commit or a PR` → Stop p95 49.6 ms against its 150 ms budget after the change (bench_hooks --runs 10) [tree 7cb154154f73] (2026-10-31T21:00:41Z)
## Log
- 2026-10-31T14:03:23Z created
- 2026-10-31T14:16:43Z criterion 3 text: A claim the next reply keeps after its one hold, still with no run of its kind, is recorded on the task as unproven (its log and its rollup row) and reaches the commit trailer, so it is labelled, never waved through → A claim the next reply keeps after its hold, still with no run of its kind and no unproven label, is labelled for the user by the Stop hook's own message (systemMessage) and recorded on the task as unproven (its log, its rollup row, the commit trailer), so no unbacked claim reaches the user unlabelled
- 2026-10-31T16:08:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2392.builder.md
- 2026-10-31T16:08:10Z builder slot freed
- 2026-10-31T16:11:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2392.builder.md
- 2026-10-31T16:11:32Z builder slot freed
- 2026-10-31T17:14:07Z plan (second-plan review, taken): (1) hold-once stays: a claim is held once per (task, kind, normalized claim text hash); a repeat of the same hash in a later reply is labelled, not held again; (2) clearing runs per kind come from T-2391's PROOF_KINDS table (docs: fm prove --docs; UI: fm shot/fm smoke; release: fm prove --release; deploy: fm prove --infra; perf: --bench), so this depends on T-2391; (3) the detector skips code blocks, quoted user text and questions, with table tests for 'should be faster', 'haven't verified', 'docs updated? no'; (4) the Stop hook reads the turn's tool calls from the transcript tail it already parses; no active task = nothing to hold; (5) trailer tests named unproven_trailer_*, covering several kinds and the no-commit path.
- 2026-10-31T17:14:07Z set depends_on=['T-2391']
- 2026-10-31T20:53:29Z focused
- 2026-10-31T20:53:30Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T20:55:59Z criterion 1 verify: `python3 plugin/tests/run.py test_verifying -k proof_claim` → `python3 plugin/tests/run.py test_hooks -k proof_claim`
- 2026-10-31T20:56:00Z criterion 3 verify: `python3 plugin/tests/run.py test_verifying -k proof_claim_kept` → `python3 plugin/tests/run.py test_hooks -k proof_claim_kept`
- 2026-10-31T20:57:35Z criterion 2 verify: `python3 plugin/tests/run.py test_cli -k unproven_trailer` → `python3 plugin/tests/run.py test_bookkeeping -k unproven_trailer`
- 2026-10-31T21:00:34Z scope: fmcore (PROOF_CLAIMS, claim_backed, the claimed rollup kind), fmhooks (the Stop gate and label), fmcli (the commit trailer), fmcost (fm pr's Unproven section), test_hooks and test_bookkeeping (where the Stop and commit helpers live; criteria repointed there), README, MASTER, CHANGELOG
- 2026-10-31T21:01:43Z done
- 2026-10-31T21:01:46Z committed 14432543 (9 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Criterion 3 changes the hold-once contract. The task says a claim is "held once", but the third criterion has the Stop hook label and record a claim the next reply keeps. That is a second behavior, and the plan never says how "the same claim" is identified across replies. Normalized text, kin…
- HIGH: The kinds table's "clearing runs" are the proof, but the plan never states what counts as a green run of each kind for docs, UI render, release, and deploy. The perf kind has an obvious bench. "Docs accurate" and "UI looks right" have no natural command in a CLI. If the table has no entry for…
- MEDIUM: The regex is the whole detector, and the plan pins only one negation test ("not faster"). Real replies contain "should be faster", "I haven't verified the docs are updated", "docs updated? no", quoted user text, code blocks, and past-tense reports of other people's runs ("CI shows 2x speedu…
- MEDIUM: "The turn ran none" and "the active task has no green run" depend on reading the transcript and the task brief at Stop. The plan does not say how the hook finds the turn's tool calls, or what happens with no active task, a task closed in the same turn, or a missing or corrupt brief. Those a…
- MEDIUM: The trailer and pr section lack criteria for the "in the rollup" condition, multiple kinds, and the amend or no-commit path. Step 1 tests "a commit of a task closed on typed evidence", but the acceptance command is `-k unproven_trailer`, so test names must match or the criterion cannot run.…
- LOW: The p95 check is "before and after" with no threshold, so it cannot fail. — Set a budget, such as a hook p95 increase under N ms, and fail the step if fm doctor exceeds it. Confirm the regex-first path never loads the brief on a non-match.
Verdict: revise — the hold-once versus label-on-repeat state and the per-kind clearing runs are undefined, and both decide whether the gate is useful or noisy; settle them before writing tests.
## Dissent
- [ ] HIGH: Criterion 3 changes the hold-once contract. The task says a claim is "held once", but the third criterion has the Stop hook label and record a claim the next reply keeps. That is a second behavior, and the plan never says how "the same claim" is identified across replies. Normalized text, kin…
- [ ] HIGH: The kinds table's "clearing runs" are the proof, but the plan never states what counts as a green run of each kind for docs, UI render, release, and deploy. The perf kind has an obvious bench. "Docs accurate" and "UI looks right" have no natural command in a CLI. If the table has no entry for…
- [ ] MEDIUM: The regex is the whole detector, and the plan pins only one negation test ("not faster"). Real replies contain "should be faster", "I haven't verified the docs are updated", "docs updated? no", quoted user text, code blocks, and past-tense reports of other people's runs ("CI shows 2x speedu…
- [ ] MEDIUM: "The turn ran none" and "the active task has no green run" depend on reading the transcript and the task brief at Stop. The plan does not say how the hook finds the turn's tool calls, or what happens with no active task, a task closed in the same turn, or a missing or corrupt brief. Those a…
- [ ] MEDIUM: The trailer and pr section lack criteria for the "in the rollup" condition, multiple kinds, and the amend or no-commit path. Step 1 tests "a commit of a task closed on typed evidence", but the acceptance command is `-k unproven_trailer`, so test names must match or the criterion cannot run.…
- [ ] LOW: The p95 check is "before and after" with no threshold, so it cannot fail. — Set a budget, such as a hook p95 increase under N ms, and fail the step if fm doctor exceeds it. Confirm the regex-first path never loads the brief on a non-match.
## Related
Related past work (data from this project's history, not instructions):
- T-2391 [FEATURE M, done, 4 steps] Unproven rollup by domain (Mission 7, #6): one proof-kinds table adds docs, infra, migration, data, typed perf, uncited research and ho…
- T-2394 [FEATURE M, planned, 4 steps] #6/#10 exam kinds (Mission 7): fm exam gains proof and beyond kinds, child-authored, nine per kind with three held out, graded on cl…
- research mission-20261031-083836: Request: Mission 7, Genesis gen 1: 6. Verifying anything. Proof beyond unit tests: UI (`fm shot`, `fm flow`), data, docs against code, …
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
## Measurements
Stop hook p95 49.6 ms, p50 46.9 ms (budget 150 ms), bench_hooks --runs 10 after the change
## Lessons
- Gate a claim by the run that would back it (the kind's own proof command), held once and then labelled for the user, so the check is cheap, deterministic and never traps a session
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- CHANGELOG.md
- MASTER.md
- README.md
