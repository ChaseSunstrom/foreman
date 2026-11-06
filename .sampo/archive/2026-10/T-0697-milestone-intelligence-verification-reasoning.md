---
id: T-0697
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:19Z
updated: 2026-10-09T21:14:19Z
batch: [T-0614, T-0615, T-0634, T-0635, T-0651, T-0652, T-0653]
base: beca70c46a2308dec2289c7381eac3f58e4c4049
base_tree: f4db8634c6c519b53bc18ad2d4c3b434f3d6f7f1
verified: strong
---
# Milestone: Intelligence — Verification reasoning
## Raw request
> T-0614: FEATURE: Typed claims and proof contracts (I058, value 4/5, effort M, risk low)
>   first version: Close-out via fm task finish gains per-claim lines tagged checked/inferred/not evaluated with an evidence pointer; fm pr renders them. Three-valued verdict is the core.
>   what it is: Types each done claim, requires its proof shape, and splits close-outs into claims with evidence.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0615: FEATURE: Verify the verifier (I060, value 4/5, effort M, risk low)
>   first version: Record executed-test count for verify commands (parse pytest/unittest summary) and flag zero or unchanged counts as inconclusive; add negative-twin criterion suggestion in oracle. Hunk ablation exists, skip.
>   what it is: Tests whether a check could ever fail by mutation, broken siblings and executed-test counts.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0634: FEATURE: Stale evidence (I061, value 3/5, effort S, risk low)
>   first version: Evidence entries record the tree id they ran on; fm task done flags evidence older than the last edit to a file the check reads (reuse the audit staleness code). Skip half-lives.
>   what it is: Gives evidence a half-life and re-verifies when inputs change.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0635: FEATURE: Verify the need and the observable (I062, value 3/5, effort S, risk low)
>   first version: Add an 'observable' line to criteria: what the user will see, checked by intent lens and fm smoke; paraphrase-verify via oracle on the paraphrased brief. Instruction plus small template change.
>   what it is: Checks the user's need, observable outcome and interpretations, not only the request.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0651: FEATURE: Independent evidence (I059, value 3/5, effort M, risk low)
>   first version: Make audit prep require a reproducer for each reviewer finding (already verified by hand per audit.md step 4) and add a 'weakest link' line to the builder brief. Skip cross-validating verifiers.
>   what it is: Checks evidence for independence and triangulates criteria, tests and behaviour.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0652: FEATURE: Adversarial verification (I063, value 3/5, effort M, risk low)
>   first version: Add a 'forge a pass' reviewer brief to fm audit prep: read-only agent tries to name a change that satisfies the verify command yet breaks the criterion. Skip auctions and betting; wild pieces are low value.
>   what it is: Panels and red teams try to forge or break a pass.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0653: FEATURE: Verification budgets and track records (I065, value 3/5, effort M, risk low)
>   first version: Compute per-verify-command catch rate from ledger (times it failed then passed, hunks noticed) and show a done-confidence line in fm task done; do not gate on it at first.
>   what it is: Chooses verify methods and spend by cost, risk and historical catch rate.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0614, T-0615, T-0634, T-0635, T-0651, T-0652, T-0653 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0697. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0614: Typed claims and proof contracts (I058, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_verifying.py -k Claims`
- [x] T-0615: Verify the verifier (I060, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_verifying.py -k Verifier`
- [x] T-0634: Stale evidence (I061, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_verifying.py -k Stale`
- [x] T-0635: Verify the need and the observable (I062, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_verifying.py -k Observable`
- [x] T-0651: Independent evidence (I059, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_verifying.py -k Independent`
- [x] T-0652: Adversarial verification (I063, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_verifying.py -k Forge`
- [x] T-0653: Verification budgets and track records (I065, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate`
## Non-goals
## Approach (options → choice → why)
Options: (a) a verification engine that re-derives proofs; (b) extend the close, the evidence recorder, audit prep and the briefs with typed claims and checks of the checks, all model-free; (c) model judges of each claim. Choice: (b). Claims: fm task finish --claim 'checked|inferred|unchecked: <claim> [:: <evidence>]' kept in a Claims section that fm pr renders. Verifier: a run whose test summary says 0 tests ran is recorded inconclusive; the oracle asks for a negative twin per criterion. Stale: the close warns when a file a step's check names changed after that check last ran. Observable: criteria name what the user will see (planning, intent lens, brief template). Independent: reviewer findings need a reproducer; builders name their weakest link. Forge: fm audit prep --forge writes a brief asking for the smallest change that keeps each check green yet breaks its criterion. Track records: the close shows, per verify command, whether it has ever caught a failure here.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0614: Typed claims and proof contracts (I058, value 4/5, effort M, risk low)
2. [x] T-0615: Verify the verifier (I060, value 4/5, effort M, risk low)
3. [x] T-0634: Stale evidence (I061, value 3/5, effort S, risk low)
4. [x] T-0635: Verify the need and the observable (I062, value 3/5, effort S, risk low)
5. [x] T-0651: Independent evidence (I059, value 3/5, effort M, risk low)
6. [x] T-0652: Adversarial verification (I063, value 3/5, effort M, risk low)
7. [x] T-0653: Verification budgets and track records (I065, value 3/5, effort M, risk low)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: verification reasoning), ~/.claude/foreman/plugin/skills/intake/references/planning.md (observable criteria), ~/.claude/foreman/plugin/skills/intake/references/audit.md (intent lens: observable)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_verifying.py` → ✗ exit 1 · Ran 6 tests in 0.4s (7 classes, 16 at a time; slowest: Verifier 0s, Stale 0s, Claims 0s) / FAILED (7 classes) [ran] [tree 8fbc3f1f4ce9] (2026-10-09T21:11:18Z)
- (step 1) `python3 plugin/tests/run.py -p test_verifying.py -k Claims` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Claims 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:13:01Z)
- (step 2) `python3 plugin/tests/run.py -p test_verifying.py -k Verifier` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Verifier 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:13:01Z)
- (step 3) `python3 plugin/tests/run.py -p test_verifying.py -k Stale` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Stale 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:13:02Z)
- (step 4) `python3 plugin/tests/run.py -p test_verifying.py -k Observable` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Observable 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:13:02Z)
- (step 5) `python3 plugin/tests/run.py -p test_verifying.py -k Independent` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Independent 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:13:03Z)
- (step 6) `python3 plugin/tests/run.py -p test_verifying.py -k Forge` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Forge 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:13:03Z)
- (step 7) `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: CatchRate 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:13:04Z)
- (ac 1) `python3 plugin/tests/run.py -p test_verifying.py -k Claims` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Claims 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (ac 2) `python3 plugin/tests/run.py -p test_verifying.py -k Verifier` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Verifier 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (ac 3) `python3 plugin/tests/run.py -p test_verifying.py -k Stale` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Stale 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (ac 4) `python3 plugin/tests/run.py -p test_verifying.py -k Observable` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Observable 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (ac 5) `python3 plugin/tests/run.py -p test_verifying.py -k Independent` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Independent 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (ac 6) `python3 plugin/tests/run.py -p test_verifying.py -k Forge` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Forge 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (ac 7) `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: CatchRate 0s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1245 tests in 64.3s (414 classes, 16 at a time; slowest: Stop 38s, TaskLifecycle 25s, Parallel 21s) / OK [ran] [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (audit intent) `main-thread review of the diff against the seven first versions` → the seven first versions shipped; T-0615's zero-test half already existed (run_command counts 'no tests ran' as a failure, stronger than inconclusive), so the duplicate was removed and the test pins the existing behaviour; the brief template stays unchanged (its sections are parsed by name), the observable rule lives in planning.md, the intent lens and the --ac help [tree 7508a4b58584] (2026-10-09T21:14:18Z)
- (audit edge) `main-thread review of the diff against the seven first versions` → fixed: a duplicate zero-test detector would have recorded the run twice; stale evidence uses only files a check names and a 1 s mtime slack; catch rates count a task as caught only when a failure was followed by a pass of the same command; a check never failing is a hint at 3+ runs, never a gate [tree 7508a4b58584] (2026-10-09T21:14:18Z)
## Log
- 2026-10-09T15:40:19Z created
- 2026-10-09T21:11:00Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_verifying.py -k Claims`
- 2026-10-09T21:11:00Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_verifying.py -k Verifier`
- 2026-10-09T21:11:00Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_verifying.py -k Stale`
- 2026-10-09T21:11:00Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_verifying.py -k Observable`
- 2026-10-09T21:11:00Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_verifying.py -k Independent`
- 2026-10-09T21:11:00Z criterion 6 verify: `` → `python3 plugin/tests/run.py -p test_verifying.py -k Forge`
- 2026-10-09T21:11:00Z criterion 7 verify: `` → `python3 plugin/tests/run.py -p test_verifying.py -k CatchRate`
- 2026-10-09T21:11:00Z focused
- 2026-10-09T21:14:18Z done
- 2026-10-09T21:14:19Z committed 1cba0be (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- decision 2026-10-04: Landscape 2026-10-04 grounded: no new work
- similar finished tasks took 3–7 steps
## Claims
- [checked] every member has its own passing test — evidence: python3 plugin/tests/run.py -p test_verifying.py
- [inferred] catch rates on this project's ledger are meaningful, since the evidence events carry the command and an exit-prefixed result
## Lessons
- Before adding a check, run the thing it guards once by hand: run_command already failed zero-test runs, which a grep for the message would have found in seconds
## Plan gaps
- failed first: step 1 T-0614: Typed claims and proof contracts (I058, value 4/5, effort M, risk low)
## Files touched
- plugin/tests/test_verifying.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmideas.py
- plugin/lib/fmlanes.py
- plugin/skills/intake/references/audit.md
- plugin/skills/intake/references/planning.md
- CHANGELOG.md
