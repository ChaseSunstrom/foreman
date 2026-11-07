---
id: T-2679
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T21:52:27Z
updated: 2026-11-02T22:01:57Z
base: 6a4e4a506c481f9b3d962c77382a90a5e0344f3d
base_tree: 37c80f3d08ed6a0467af181a91ae9b09c862dc51
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-02T22:00:39Z
plan0_scope: []
verified: strong
unproven: [research-uncited]
---
# Kill test M-02 (code as a regenerable cache of intent and proofs): rebuild three deleted spec-suite modules from their spec and tests alone, two blind attempts each
## Raw request
> Kill test M-02 (code as a regenerable cache of intent and proofs): rebuild three deleted spec-suite modules from their spec and tests alone, two blind attempts each
## Interpretation
1. (chosen) M-02's own kill line, run as written: delete three spec-suite modules and have a tool-less headless child rebuild each from the task commit's spec and the test file alone, two attempts each; viable if at least two of three pass every original test. This is the generation's floor: an extreme or massive moonshot advanced from idea to kill.
2. A wider trial (all eight modules, several models). Rejected for the kill stage: the kill test is the cheapest experiment that could prove M-02 wrong; the slice stage widens it.
## Assumptions (confidence)
## Acceptance criteria
- [x] the M-02 kill result (viable or not-yet, with the per-module pass counts) is in moonshot.md's Kill line with this task as evidence and its Stage is kill — verify with `fm genesis moonshot status`
## Non-goals
## Approach (options → choice → why)
1. A scratch script builds the suite with bench/spec-suite/make.py, asks fmideas.run_child (no tools, no hooks, no MCP, budget-checked) for semver, table and ranges, writes each answer and runs its unittest module. Likely outcome: viable (the specs are complete by design). Fails if: the child can't see what the tests import (base files are included for that).
2. use what exists: fm bench duel on the spec suite. Fails if: the duel runs an agent with tools, which can read git history and recover the deleted source, so it isn't blind.
3. do less: one module. Fails if: one pass or fail says nothing about two of three.
Choice 1 (85%): blind by construction, six calls, and the verdict rule is the kill line's own.
## Risks and rollback
Blast radius (fm graph blast): co-changes bench/spec-suite/README.md, bench/spec-suite/hard.py, CHANGELOG.md, MASTER.md, bench/spec-suite/impossible.py.
## Execution prompt
## Steps
1. [x] build the spec suite in scratch; for semver, table and ranges, ask a tool-less child for the module from the commit-message spec and the test file only, two attempts each, and run each module's tests
2. [x] record the result in moonshot.md (Kill → viable or not-yet, Evidence T-2679, Stage kill)
## Resume here
## Docs impact
none: the catalogue is Foreman state in the Genesis tower, not a repo doc
## Verification evidence
- (step 1) `python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/kill_m02.py /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/moon/killrun` → exit 0 · "verdict": "viable" / } [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:01:07Z)
- (step 2) `grep -q 'Evidence: T-2679' state/projects/foreman-4a056f/research/genesis/moonshot.md` → exit 0 · (no output) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:01:54Z)
- (ac 1) `fm genesis moonshot status` → exit 0 · - Floor: advance at least one extreme or massive moonshot by a stage and write 'Advanced: M-NN <stage> (T-NNNN)' in gen-3/mission-moonshot.md; fm genesis check holds it once gen-4 exists. Every built [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:01:54Z)
- (ac 1) `fm genesis moonshot status` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:01:54Z [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:01:55Z)
- (audit intent) `self: blind by construction: the child had no tools, saw only the spec commit message, the test file and the base files; each answer was written into a fresh build and its unittest module run` → the moonshot's own kill line, run as written; the result and its caveat are in the catalogue [tree 37c80f3d08ed] (2026-11-02T22:01:55Z)
- (audit edge) `self: blind by construction: the child had no tools, saw only the spec commit message, the test file and the base files; each answer was written into a fresh build and its unittest module run` → the spec suite's specs are complete by construction, so the kill is a weak bar; the slice uses Foreman's own code, whose specs are not [tree 37c80f3d08ed] (2026-11-02T22:01:55Z)
## Log
- 2026-11-02T21:52:27Z created
- 2026-11-02T22:00:39Z focused
- 2026-11-02T22:00:39Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-02T22:01:57Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-02: Recommendation: the floor's kill test this generation is M-02's (rebuild three deleted spec-suite modules from their specs and tests alone, two atte…
- T-2626 [FEATURE L, done, 4 steps] Every Genesis generation advances the moonshot campaign (MOONSHOT.md A, steer 2026-11-02): one catalogue across generations toward 100 …
- T-2675 [RESEARCH M, done, 3 steps] Moonshot campaign, generation 3: file the first 20 moonshots (M-01 to M-20) in moonshot.md and have them rated blind by the strongest …
- decision 2026-11-02: [costly] [cites: user steer 2026-11-02: MOONSHOT.md part A] [check: pending T-2626] Standing rule (MOONSHOT.md part A): the moonshot campaign is que…
## Decision
Recommendation: M-02 is viable at the kill stage (3 of 3 spec-suite modules rebuilt blind passed every test) and moves to its slice: regenerate one of Foreman's own small modules from its briefs, CHANGELOG lines and tests, where the spec is not complete by construction. Would change if: the slice fails on Foreman's own module, which would mean intent and proofs don't pin real code yet (Stage not-yet, blocker named).
## Lessons
- A kill test on a fixture built to be fully specified passes easily; name that ceiling in the result and make the slice the harder case
