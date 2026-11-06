---
id: T-0134
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmserve.py, plugin/lib/fmwatch.py, plugin/lib/fmlanes.py, plugin/lib/fmsync.py, plugin/tests/test_lanes.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-03T04:52:05Z
updated: 2026-10-03T08:45:30Z
base: 4c8703731a4d080f868ac8baf7dd6b8a55732096
base_tree: 1717ad9267f10552423965bacaa4f6288c300e11
verified: strong
---
# Lanes: a git worktree is a lane of its project with its own active task
## Raw request
> also maybe allow things in parallel? unless that will cause context/sub agent issues?
## Interpretation
Parallel work needs isolation first: today a linked git worktree isn't Foreman's project at all (no briefs, no gates: edits there skip the discipline), and there is one active task per project, so a second session focusing a task pauses the first. A lane is a linked worktree of a registered repo: it shares the project's state, keeps its own active task (focus there pauses only that lane's task), its git work (snapshots, diffs, commits) happens in its own files, and the main checkout's next/queue never offers a task active in another lane. fm lane new|list|rm manage them. Running lanes in parallel (fm run --parallel) is the follow-up, built on this.
## Assumptions (confidence)
## Acceptance criteria
- [x] From a linked worktree, fm resolves the main project with the lane set; focusing a task there doesn't pause the main checkout's active task and vice versa; each side's next/queue skips the other's active task; the edit gate in a lane needs that lane's active task; fm task finish --commit there commits on the lane's branch — verify with `python3 plugin/tests/run.py -k test_lanes`
- [x] fm lane new T-… makes a worktree on branch foreman/T-…; fm lane list shows lanes and their tasks; fm lane rm refuses uncommitted work — verify with `python3 plugin/tests/run.py -k test_lanes`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) per-session active tasks keyed by FOREMAN_DRIVE_TASK in one checkout: no isolation, two sessions' edits mix in snapshots, gates and commits; (b) lanes as git worktrees: Project gains lane (its worktree root; root becomes that path so every git operation stays in the lane; dir stays the main project's state), briefs focused in a lane record meta.lane, active_brief(briefs, lane) and focus/queue filter by it. Choice: (b): isolation is git's own, and the change is a filter at the few places the single-active rule lives. Self-critique: 19 active_brief calls must pass the lane (a missed one would read the main lane's task: covered by tests from a lane for hooks, fm next, focus, finish); worktree removal is destructive, so fm lane rm refuses uncommitted work.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests from a worktree
2. [x] Project.lane in find_project; lane-aware active_brief, focus and queue
3. [x] Pass the lane at every active_brief call
4. [x] fm lane new|list|rm
5. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Lanes paragraph, file map), CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_lanes` → ✗ exit 1 · Ran 4 tests in 1.0s (1 classes, 16 at a time; slowest: Lanes 1s) / FAILED (1 classes) [ran] [tree f36f92b17633] (2026-10-03T08:37:15Z)
- (step 2) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 1ee0c3721966] (2026-10-03T08:40:53Z)
- (step 3) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 1ee0c3721966] (2026-10-03T08:40:55Z)
- (step 4) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 1ee0c3721966] (2026-10-03T08:40:56Z)
- (step 1) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: Lanes 1s) / OK [ran] [tree 1ee0c3721966] (2026-10-03T08:40:58Z)
- (step 5) `grep -q T-0134 MASTER.md && grep -q T-0134 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 1ee0c3721966] (2026-10-03T08:40:58Z)
- (step 1) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 8 tests in 2.3s (1 classes, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree 95fff8b1d410] (2026-10-03T08:45:00Z)
- (step 2) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 8 tests in 2.4s (1 classes, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree 95fff8b1d410] (2026-10-03T08:45:03Z)
- (step 3) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 8 tests in 2.4s (1 classes, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree 95fff8b1d410] (2026-10-03T08:45:06Z)
- (step 4) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 8 tests in 2.4s (1 classes, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree 95fff8b1d410] (2026-10-03T08:45:08Z)
- (step 5) `grep -q main_view MASTER.md && grep -q T-0134 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 95fff8b1d410] (2026-10-03T08:45:08Z)
- (ac 1) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 8 tests in 2.4s (1 classes, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (ac 2) `python3 plugin/tests/run.py -k test_lanes` → exit 0 · Ran 8 tests in 2.4s (1 classes, 16 at a time; slowest: Lanes 2s) / OK [ran] [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (ac 3) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:44 UTC); cached (fm check --fresh reruns) [ran] [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (audit intent) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → lanes deliver the isolation parallel work needs (own active task, own files, own branch, queues that don't overlap); running lanes in parallel is T-0167, which depends on this [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (audit adversary) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → lane new/rm take paths from state and git only; rm never deletes uncommitted or ignored files and keeps unmerged branches; task set can't create a second active task [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (audit edge) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → submodules and unregistered worktrees resolve as before; a hand-deleted lane is listed, freed and re-creatable; moving a task between checkouts retakes its start point [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (audit operator) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → the main session's statusline and dashboard never show a lane's task; sync keeps one mirror; lane list and focus refusals say how to free a task [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (audit maintainer) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → the single-active rule now lives in active_brief(briefs, lane) and held_elsewhere/lane_view, with every caller passing p.lane; fmlanes is a small module; MASTER describes the model [tree 95fff8b1d410] (2026-10-03T08:45:20Z)
- (audit intent) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → lanes deliver the isolation parallel work needs (own active task, own files, own branch, queues that don't overlap); running lanes in parallel is T-0167, which depends on this [tree 95fff8b1d410] (2026-10-03T08:45:30Z)
- (audit adversary) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → lane new/rm take paths from state and git only; rm never deletes uncommitted or ignored files and keeps unmerged branches; task set can't create a second active task [tree 95fff8b1d410] (2026-10-03T08:45:30Z)
- (audit edge) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → submodules and unregistered worktrees resolve as before; a hand-deleted lane is listed, freed and re-creatable; moving a task between checkouts retakes its start point [tree 95fff8b1d410] (2026-10-03T08:45:30Z)
- (audit operator) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → the main session's statusline and dashboard never show a lane's task; sync keeps one mirror; lane list and focus refusals say how to free a task [tree 95fff8b1d410] (2026-10-03T08:45:30Z)
- (audit maintainer) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: the shared view files and the .foreman mirror are the main checkout's view whichever lane wrote (test: status.json keeps main's task); fm lane rm refuses ignored files and prunes a hand-deleted lane (test), lane list shows it as missing; the committed-library fallback passes the lane; fm task set can't start a task around focus (test); auto-evidence from a lane lands on the lane's task (test). 8 lane tests, 581 total.` → the single-active rule now lives in active_brief(briefs, lane) and held_elsewhere/lane_view, with every caller passing p.lane; fmlanes is a small module; MASTER describes the model [tree 95fff8b1d410] (2026-10-03T08:45:30Z)
## Log
- 2026-10-03T04:52:05Z created
- 2026-10-03T04:52:49Z steer: make sure parallel things don't cause context/speed/quality/usage issues too
- 2026-10-03T08:36:38Z planned from capture
- 2026-10-03T08:36:39Z set approved=True
- 2026-10-03T08:36:39Z self-approved (full autonomy) after self-critique: the risk is a missed active_brief call site; every hook and command path that reads the active task gets a lane test
- 2026-10-03T08:36:39Z focused
- 2026-10-03T08:39:29Z scope: plugin/lib/fmlanes.py — fm lane's own module (new, list, rm), registered lazily like the others
- 2026-10-03T08:43:09Z scope: plugin/lib/fmsync.py — review finding 2: the .foreman mirror is the main checkout's, never a lane's branch-point copy
- 2026-10-03T08:45:30Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmserve.py', 'plugin/lib/fmwatch.py', 'plugin/lib/fmlanes.py', 'plugin/lib/fmsync.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-03T08:45:30Z done
- 2026-10-03T08:45:30Z committed 102164a (10 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- T-0136 [FIX M, done, 3 steps] Work done while a task was paused isn't its own change — lesson: When several callers read the same derived value (task_base), fix the valu…
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py, plugin/tests/test_serve.py
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmwatch.py; re-ground the plan against them before editing
## Lessons
- When a 'single X per project' rule becomes 'per lane', grep every reader of X and every writer of files derived from X: the shared view files were the leak no call-site rewrite would have found.
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmserve.py
- plugin/lib/fmwatch.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmsync.py
