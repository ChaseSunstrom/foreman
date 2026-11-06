---
id: T-0234
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: [T-0227]
source: user
created: 2026-10-04T05:27:19Z
updated: 2026-10-04T09:14:55Z
base: 747532e11d5de5f071328324ea6dceca6065e6a8
base_tree: b883fbf7b87a6da563223dd6d2eda7d8512e4049
verified: strong
---
# Implementation subagents in lane worktrees — a foreman:fm-builder agent (Edit/Write/Bash)
## Raw request
> FEATURE: implementation subagents in lane worktrees — a foreman:fm-builder agent (Edit/Write/Bash) works one S/M task inside its own lane worktree and returns a commit; the main thread reviews the diff and merges; budgeted and capped at 2 at once #T-0227
> CONTEXT: fm lane (fmlanes.py) makes worktrees with their own active task; fm run --parallel merges lanes; the delegation reference says the main thread does all edits — this adds a bounded exception
> DONE-WHEN: the agent file exists with a lane-only contract, fm lane gives a builder brief, and delegate.md documents when and how to merge
## Interpretation
A bounded exception to 'the main thread does all edits': an independent S/M task can go to a foreman:fm-builder subagent that works it in its own git worktree while the main thread does other work, and hands back a commit on a branch. The main thread reviews the diff, merges it, re-verifies on the merged tree and closes the task. At most two builders at once; every launch is budget-checked.
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/agents/fm-builder.md exists with Edit/Write/Bash tools and a worktree-only contract (fm focus first, test-first, evidence, commit on its branch, never push/merge/close, nothing outside its worktree) — verify with `python3 plugin/tests/run.py -p test_builder.py -k Agent`
- [x] fm lane brief ID writes a self-contained builder brief (request, interpretation, criteria with verify commands, steps, the contract) and prints the Agent call with isolation worktree; it refuses an L task, a task held or active elsewhere, and a third builder in flight — verify with `python3 plugin/tests/run.py -p test_builder.py -k Brief`
- [x] the builder flow works end to end in a linked worktree: fm focus there binds the task to it, the main checkout sees it held, and after the branch merges, fm focus in main brings it back — verify with `python3 plugin/tests/run.py -p test_builder.py -k Flow`
- [x] delegate.md documents when to use a builder and how to review, merge, re-verify and close — verify with `grep -c 'fm lane brief' plugin/skills/intake/references/delegate.md`
## Non-goals
## Approach (options → choice → why)
(a) fm lane new + a builder told to cd into <repo>.lanes/ID — the harness resets a shell cwd outside the session's folder, so the guard would resolve the main checkout's task; (b) Claude Code's Agent isolation: "worktree" — the harness creates the worktree and keeps the agent's cwd in it; the builder's first command, fm focus ID, binds the task to that worktree (fm focus already sets meta lane = the checkout it runs in), so the hooks' guard, touches, evidence and gates resolve the builder's task there. → (b): native platform feature, no new lane machinery. fm lane brief ID writes the builder's self-contained brief, refuses L tasks, held/active tasks and a third builder in flight, checks the subagent budget, marks the task, and prints the Agent call. The builder commits on its branch but doesn't close the task (closing needs reviewer lenses it can't spawn); the main thread merges, refocuses, re-runs the criteria and finishes.
## Risks and rollback
A builder runs Edit/Write/Bash under the same guard as the main thread (hooks apply to subagent calls); its worktree path decides the guard's project. Two builders editing the same files conflict at merge: the brief tells the main thread to pick independent tasks. Rollback: revert; the agent file is inert unless launched.
## Execution prompt
## Steps
1. [x] tests first: plugin/tests/test_builder.py
2. [x] plugin/agents/fm-builder.md
3. [x] fm lane brief (fmlanes.py) + parser
4. [x] delegate.md, MASTER, CHANGELOG; review; commit
## Resume here
<!-- auto -->
- 2026-10-04T09:04:08Z steps 0/4 done
- git: foreman/build; 14 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmdoctor.py, plugin/lib/fmlanes.py, plugin/lib/fmsecond.py, plugin/skills/intake/references/delegate.md
- touched since last checkpoint: plugin/tests/test_followups.py
## Docs impact
plugin/skills/intake/references/delegate.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_builder.py` → ✗ exit 1 · Ran 4 tests in 0.8s (3 classes, 16 at a time; slowest: Brief 1s, Flow 0s, Agent 0s) / FAILED (3 classes) [ran] [tree 9119dbf15a69] (2026-10-04T08:52:37Z)
- (step 2) `python3 plugin/tests/run.py -p test_builder.py -k Agent && python3 plugin/tests/run.py -p "test_doc*"` → exit 0 · Ran 42 tests in 8.5s (13 classes, 16 at a time; slowest: Command 8s, DocsDrift 1s, RestoreState 0s) / OK [ran] [tree c505cef506ce] (2026-10-04T09:00:27Z)
- (step 3) `python3 plugin/tests/run.py -p test_builder.py` → exit 0 · Ran 4 tests in 1.7s (3 classes, 16 at a time; slowest: Brief 2s, Flow 1s, Agent 0s) / OK [ran] [tree c505cef506ce] (2026-10-04T09:00:29Z)
- (step 4) `grep -c 'fm lane brief' plugin/skills/intake/references/delegate.md` → exit 0 · 1 [ran] [tree c505cef506ce] (2026-10-04T09:00:29Z)
- (step 1) `python3 plugin/tests/run.py -p test_builder.py -k Contract` → exit 0 · Ran 4 tests in 1.8s (1 classes, 16 at a time; slowest: Contract 2s) / OK [ran] [tree 5ba7b95a6678] (2026-10-04T09:11:32Z)
- (step 3) `python3 plugin/tests/run.py -p test_builder.py -k Brief` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Brief 1s) / OK [ran] [tree 5ba7b95a6678] (2026-10-04T09:11:33Z)
- (step 3) `python3 plugin/tests/run.py -p test_builder.py -k Flow` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Flow 0s) / OK [ran] [tree 5ba7b95a6678] (2026-10-04T09:11:34Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.1    31.4     150  [0] / SessionEnd                  28.0    29.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 791 te [ran] [tree 5ba7b95a6678] (2026-10-04T09:12:35Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_builder.py && python3 plugin/tests/run.py -p "test_doc*" && python3 plugin/tests/run.py -p "test_lane*"` → 17/20 hunks proven; unproven: plugin/lib/fmguard.py @@ -27 +27 @@ class Ctx:; plugin/lib/fmguard.py @@ -106,0 +110,3 @@ def _message(block, ctx):; plugin/lib/fmlanes.py @@ -75 +142 @@ def remove(p, b, main): [inconclusive] [ran] [tree 5ba7b95a6678] (2026-10-04T09:14:09Z)
- (step 1) `python3 plugin/tests/run.py -p test_builder.py` → exit 0 · Ran 8 tests in 1.8s (4 classes, 16 at a time; slowest: Contract 2s, Brief 1s, Flow 0s) / OK [ran] [tree 5573d716abff] (2026-10-04T09:14:38Z)
- (ac 1) `python3 plugin/tests/run.py -p test_builder.py -k Agent` → exit 0 · Ran 1 tests in 0.0s (1 classes, 16 at a time; slowest: Agent 0s) / OK [ran] [tree 5573d716abff] (2026-10-04T09:14:47Z)
- (ac 2) `python3 plugin/tests/run.py -p test_builder.py -k Brief` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Brief 1s) / OK [ran] [tree 5573d716abff] (2026-10-04T09:14:47Z)
- (ac 3) `python3 plugin/tests/run.py -p test_builder.py -k Flow` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Flow 0s) / OK [ran] [tree 5573d716abff] (2026-10-04T09:14:47Z)
- (ac 4) `grep -c 'fm lane brief' plugin/skills/intake/references/delegate.md` → exit 0 · 1 [ran] [tree 5573d716abff] (2026-10-04T09:14:47Z)
- (audit adversary) `one fm-reviewer pass (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine (a builder's worktree only, main checkout never scratch), task done/finish/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, and a Ctx signature whose crash the hook's committed-library fallback masks in proof runs — captured as T-0297). Guard replay 0 newly allowed` → builder escapes tested — writes outside, closing its task, handing itself back, deleting other branches [tree 5573d716abff] (2026-10-04T09:14:47Z)
- (audit edge) `one fm-reviewer pass (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine (a builder's worktree only, main checkout never scratch), task done/finish/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, and a Ctx signature whose crash the hook's committed-library fallback masks in proof runs — captured as T-0297). Guard replay 0 newly allowed` → harness-named branches, a lane switched off its branch, a never-launched brief, main checkout under /tmp [tree 5573d716abff] (2026-10-04T09:14:47Z)
- (audit intent) `one fm-reviewer pass (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine (a builder's worktree only, main checkout never scratch), task done/finish/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, and a Ctx signature whose crash the hook's committed-library fallback masks in proof runs — captured as T-0297). Guard replay 0 newly allowed` → four criteria met with tests; Claude Code's isolation worktree is the native rung [tree 5573d716abff] (2026-10-04T09:14:47Z)
- (audit adversary) `one fm-reviewer pass over all five lenses (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine, close/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, a Ctx signature whose crash the committed-library fallback masks in proof runs — T-0297). Guard replay 0 newly allowed` → builder escapes tested — writes outside, closing its task, handing itself back, deleting other branches [tree 5573d716abff] (2026-10-04T09:14:55Z)
- (audit edge) `one fm-reviewer pass over all five lenses (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine, close/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, a Ctx signature whose crash the committed-library fallback masks in proof runs — T-0297). Guard replay 0 newly allowed` → harness-named branches, a lane switched off its branch, a never-launched brief, main checkout under /tmp [tree 5573d716abff] (2026-10-04T09:14:55Z)
- (audit intent) `one fm-reviewer pass over all five lenses (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine, close/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, a Ctx signature whose crash the committed-library fallback masks in proof runs — T-0297). Guard replay 0 newly allowed` → four criteria met with tests; Claude Code's isolation worktree is the native rung [tree 5573d716abff] (2026-10-04T09:14:55Z)
- (audit operator) `one fm-reviewer pass over all five lenses (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine, close/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, a Ctx signature whose crash the committed-library fallback masks in proof runs — T-0297). Guard replay 0 newly allowed` → delegate.md walks brief → launch → review → merge → lane rm → refocus → re-verify → finish; fm doctor and the docs test accept exactly one editing agent [tree 5573d716abff] (2026-10-04T09:14:55Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses (T-0234-review-1): 3 MEDIUM — fm lane rm could delete any merged branch the lane switched to (main included); the never-close contract was prose only; writes outside the worktree weren't confined — and 3 LOW (builder slot leak, branch cleanup with a missing folder, test gaps). All reproduced as failing tests, then enforced: a non-grantable guard category confine, close/audit/drop and fm lane changes refused from a builder's lane, rm deletes only foreman/ID or the branch recorded at focus and never a default branch, take-back frees the slot. Hunks 17/20 (rest: a docstring, the confine message now asserted, a Ctx signature whose crash the committed-library fallback masks in proof runs — T-0297). Guard replay 0 newly allowed` → one new agent file, one fmlanes function, one guard category; tests cover each refusal [tree 5573d716abff] (2026-10-04T09:14:55Z)
## Log
- 2026-10-04T05:27:19Z created
- 2026-10-04T05:27:30Z set tier=L
- 2026-10-04T08:52:10Z set approved=True
- 2026-10-04T08:52:15Z focused
- 2026-10-04T08:55:37Z paused: focus moved to T-0291
- 2026-10-04T08:59:53Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-04T08:59:53Z focused
- 2026-10-04T09:04:09Z paused: focus moved to T-0291
- 2026-10-04T09:09:00Z scope: commit 91c65ce (T-0291) already carries this task's agent file, lane parser choice and MASTER/CHANGELOG lines (file-level attribution of shared files); fmlanes/fmdoctor/delegate/tests land in this task's commit
- 2026-10-04T09:09:00Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-04T09:09:00Z focused
- 2026-10-04T09:14:55Z done
- 2026-10-04T09:14:55Z committed f856062 (11 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- research T-0167-review: Verdict:** changes needed. One HIGH finding (a hang) and two MEDIUM ones. I traced each finding below by reading the code. I did not run any of t…
- research T-0227-review: HIGH, missing: the UI half of the request is not built. [stale: plugin/lib/fmbudget.py, plugin/lib/fmwatch.py, plugin/tests/helpers.py changed si…
## Lessons
- A contract a subagent must keep needs enforcement where it acts (guard category, refused commands), not only words in its prompt
## Files touched
- plugin/tests/test_builder.py
- plugin/agents/fm-builder.md
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- plugin/skills/intake/references/delegate.md
- plugin/lib/fmdoctor.py
- plugin/tests/test_docs.py
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_followups.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
