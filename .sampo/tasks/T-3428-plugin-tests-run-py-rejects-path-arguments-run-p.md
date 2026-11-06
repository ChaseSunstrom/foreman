---
id: T-3428
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/tests/run.py, plugin/tests/test_run.py]
depends_on: []
source: discovered
created: 2026-11-06T10:44:03Z
updated: 2026-11-06T15:44:00Z
base: f8457be6a61386262269a9f8e3e0c7d704b88462
base_tree: 2996a2fb3e249ab137edca947d27e1689c12fbfa
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T10:44:38Z
plan0_scope: []
builder_returned: 2026-11-06T10:46:05Z
lane_stop: merged 2026-11-06T11:01:23Z
verified: strong
unproven: [meaning]
---
# plugin/tests/run.py rejects path arguments ('run.py plugin/tests/test_genesis.py -k…
## Raw request
> FIX: plugin/tests/run.py rejects path arguments ('run.py plugin/tests/test_genesis.py -k Memo' → no test matches), so a builder's criterion written that way refuses its lane merge (T-3375 tonight); accept plugin/tests/test_X.py and test_X.py paths as the module name test_X
## Interpretation
run.py parse maps path-form names (plugin/tests/test_X.py, ./, bare test_X.py, absolute) to test_X; other paths error.
## Assumptions (confidence)
## Acceptance criteria
- [x] path-form test names map to their module — verify with `python3 plugin/tests/run.py test_run.Args`
## Non-goals
## Approach (options → choice → why)
Normalize a.names in parse(); realpath dir must equal HERE; ap.error otherwise.
## Risks and rollback
## Execution prompt
## Steps
1. [x] path names in run.py parse, tested
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_run.Args` → ✗ exit 1 · Ran 4 tests in 1.5s (1 jobs, 16 at a time; slowest: Args 0s) / FAILED (1 classes: test_run.Args) [ran] [tree d7e477e9750b] [world 2f1906870a] (2026-11-06T10:44:44Z)
- (step 1) `python3 plugin/tests/run.py test_run.Args` → exit 0 · Ran 4 tests in 15.3s (1 jobs, 16 at a time; slowest: Args 0s) / OK [ran] [tree 0d985a691d72] [world 2f1906870a] (2026-11-06T10:45:08Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ci_annotations test_doctor test_left_out test_models test_rename_scan test_run && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.55s] [ran] [tree 0d985a691d72] [world 2f1906870a] (2026-11-06T10:45:50Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 30b093776bff] (2026-11-06T11:01:26Z)
- (ac 1) `python3 plugin/tests/run.py test_run.Args` → exit 0 · Ran 4 tests in 0.4s (1 jobs, 16 at a time; slowest: Args 0s) / OK [ran] [tree 30b093776bff] [world 2f1906870a] (2026-11-06T11:01:29Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 30b093776bff] (2026-11-06T11:01:29Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 30b093776bff] (2026-11-06T11:01:29Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 30b093776bff] (2026-11-06T11:01:29Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 30b093776bff] (2026-11-06T11:01:29Z)
## Log
- 2026-11-06T10:44:03Z created
- 2026-11-06T10:44:30Z set tier=S
- 2026-11-06T10:44:36Z planned: it has criteria and steps
- 2026-11-06T10:44:37Z focused
- 2026-11-06T10:44:38Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T11:01:23Z merged worktree-agent-a10361e5e39ded53f (2 file(s))
- 2026-11-06T11:01:24Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a10361e5e39ded53f
- 2026-11-06T11:01:24Z focused
- 2026-11-06T11:01:25Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/run.py', 'plugin/tests/test_run.py']
- 2026-11-06T11:01:25Z scope: widened at merge to the reviewed lane's own diff (6a388139d), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T11:01:54Z done
- 2026-11-06T11:01:57Z committed 23770af00 (1 file)
- 2026-11-06T15:44:00Z not reverted: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_claims.Claims, test_close_gates.CloseGates already fail on 6a388139d's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3411 [FIX M, done, 2 steps] A criterion verify written as 'python3 -m unittest test_X.Class' only runs from… — lesson: none: a reviewed builder lane; its lessons are i…
- T-2988 [FIX S, done, 1 steps] A criterion's verify that names a state/ path relative to the repo always fails in a… — lesson: When the same refusal hits twice from one c…
- T-2783 [CLEAN S, done, 1 steps] The rename ratchet sees every old module name a test or library passes as a string: test_rename_aliases' scanner walks every argument (ke…
- decision 2026-11-04: Filed gen-4's Missions 2-8 past rune step's 'build: Mission 1, focus T-2910' line instead of stopping there; the main thread builds the eight tasks …
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 path names in run.py parse, tested
## Files touched
- plugin/tests/test_run.py
- plugin/tests/run.py
- CHANGELOG.md
