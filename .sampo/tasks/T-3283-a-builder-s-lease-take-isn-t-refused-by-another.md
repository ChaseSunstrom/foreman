---
id: T-3283
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/bus.py, plugin/tests/test_bus.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:31:24Z
updated: 2026-11-06T05:32:59Z
builder_model: haiku
base: 423f6b4814a0c4a570268fbbb0e65fa671096c91
base_tree: 49c4583d2e3853d7c3a1df586653785b955ed560
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T02:33:39Z
plan0_scope: [plugin/lib/sampo/bus.py, plugin/tests/test_bus.py, CHANGELOG.md]
builder_returned: 2026-11-06T02:37:19Z
lane_stop: refused 2026-11-06T05:32:59Z
verified: strong
postmerge_red: test_batch_edit.LaneMax, test_claims.Claims, test_diff_gates.DiffGates
postmerge_sha: 2218d3e0a0ca7c50512e9b6886b6319e0c6a54a6
---
# A builder's lease take isn't refused by another lane's brief pre-claim (advisory since T-1138 for edits, still refusing in fm lease take)
## Raw request
> A builder's lease take isn't refused by another lane's brief pre-claim (advisory since T-1138 for edits, still refusing in fm lease take)
## Interpretation
Reading 1 (chosen): on 2026-11-06, 13 builder lanes ran at once and one (T-3265) stopped because fm lease take refused symbols in kalevala.py, rune.py and cli.py that other lanes' briefs had pre-claimed file-wide from their scope. Edits already treat lane pre-claims as advisory (bus.conflict, T-1138); the take path (bus.py ~621, via claim_overlaps) still refuses them, so a careful builder waits up to 25 minutes for nothing. Fix the take path to note a lane pre-claim, not refuse it. Reading 2 (ruled out): stop lane briefs from pre-claiming at all. Ruled out because the pre-claims still tell lanes and the lead where overlaps are; only the refusal is wrong.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lease take FILE::SYM by one lane over another lane's lane-<id> pre-claim of FILE::* succeeds (with a one-line note naming the pre-claim), while an explicit lease of another session still refuses — verify with `python3 plugin/tests/run.py test_bus`
## Non-goals
## Approach (options → choice → why)
1. In the take path, drop lane- pre-claims from the refusing hits and print them as a note. Likely outcome: a few lines in bus.py; edits and takes agree.
2. Pre-claim symbols, not whole files. Likely outcome: needs the symbols before the builder has read the code; fails if the brief can't know them.
3. Do less: tell builders to pass --warn. Likely outcome: works today, but every new builder relearns it by waiting.

Choice 1 (90%): it makes the take path match the edit path's rule from T-1138. Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_bus: lane A pre-claims cli.py, lane B's take of cli.py::x is refused today
2. [x] claim_overlaps' refusal path in the take skips lane- pre-claims; note them instead
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bus` → ✗ exit 1 · Ran 24 tests in 12.8s (7 jobs, 16 at a time; slowest: Watch 10s, Lease 8s, Approvals 4s) / FAILED (1 classes: test_bus.Lease) [ran] [tree 2c5025bd2654] [world 2f1906870a] (2026-11-06T02:34:29Z)
- (step 2) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 24 tests in 8.5s (19 jobs, 16 at a time; slowest: Bus 7s, Conductor 7s, Approvals 7s) / OK [ran] [tree 44272ec6a942] [world 2f1906870a] (2026-11-06T02:34:53Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bus test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [61.88s] [ran] [tree 44272ec6a942] [world 2f1906870a] (2026-11-06T02:36:31Z)
- `python3 plugin/tests/run.py test_bus` → ✗ exit 1 · Ran 24 tests in 191.7s (7 jobs, 16 at a time; slowest: Watch 8s, Lease 6s, Approvals 4s) / FAILED (1 classes: test_bus.Lease) (start tree + this task's tests) [ran] [tree 5035a34136e6] [world 2f1906870a] (2026-11-06T05:24:15Z)
- `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 24 tests in 55.9s (23 jobs, 16 at a time; slowest: Approvals 6s, FailingMark 3s, Bus.test_a_message_reaches_its_session_once_and_all_reach_everyone 3s) / OK [ran] [tree 5035a34136e6] [world 2f1906870a] (2026-11-06T05:24:15Z)
- (audit self) `lane reviewed by an fm-reviewer before merge (earlier round, verdict merge); re-read the merged diff in bus.py cmd_lease: a lane pre-claim is skipped with a note only for lane-<id> claims, explicit leases of other sessions still refuse; test_bus red at the start tree, green now` → no findings [tree 5035a34136e6] (2026-11-06T05:25:36Z)
- (ac 1) `python3 plugin/tests/run.py test_bus` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T05:24:15Z [ran] [tree 5035a34136e6] [world 2f1906870a] (2026-11-06T05:25:40Z)
- (audit self) `lane review before merge; self audit after the merge; red to green proved` → no findings [tree 5035a34136e6] (2026-11-06T05:25:40Z)
## Log
- 2026-11-06T02:31:24Z created
- 2026-11-06T02:31:33Z set scope=['plugin/lib/sampo/bus.py', 'plugin/tests/test_bus.py', 'CHANGELOG.md']
- 2026-11-06T02:33:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3283.builder.md
- 2026-11-06T02:33:37Z focused
- 2026-11-06T02:33:39Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T05:19:36Z merged worktree-agent-aa9eeb0169e73b1d0 (2 file(s))
- 2026-11-06T05:19:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa9eeb0169e73b1d0
- 2026-11-06T05:19:47Z focused
- 2026-11-06T05:27:40Z done
- 2026-11-06T05:27:51Z committed 378389b90 (16 files)
- 2026-11-06T05:32:59Z red after merge: test_batch_edit.LaneMax, test_claims.Claims, test_diff_gates.DiffGates; 2218d3e0a reverted
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- decision 2026-10-31: [costly] Tower filing waits for the user's call on the cold-read rule: Missions 5-8's files and the Mission 3-4 critiques stay unfiled after 4-12 pu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_bus.py
## Preflight
Changed in scope since this was planned (2026-11-06): CHANGELOG.md, plugin/lib/sampo/bus.py, plugin/tests/test_bus.py; re-ground the plan against them before editing
## Lessons
- Advisory claims must never be enforced by a second tool that reads the same record: check every reader when a record's meaning is advisory.
## Plan gaps
- failed first: step 1 failing test in test_bus: lane A pre-claims cli.py, lane B's take of cli.py::x is refused today
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/sampo/bus.py
- CHANGELOG.md
