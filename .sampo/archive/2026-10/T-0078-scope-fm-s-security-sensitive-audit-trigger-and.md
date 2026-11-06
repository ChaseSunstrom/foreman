---
id: T-0078
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/**, plugin/tests/**, CHANGELOG.md, README.md, MASTER.md]
depends_on: []
source: self
created: 2026-09-27T13:12:41Z
updated: 2026-10-03T04:32:42Z
base: 0765a28482c9690711f0b1e4fbb70959f3bb279d
base_tree: 6c173200971d54b7c07746c2aac8081542866e3e
verified: ok
---
# A task's own changes: diff from a working-tree snapshot taken at focus, not the last commit
## Raw request
> Scope fm's security-sensitive audit trigger (and audit prep's diff) to the task's own changes, not the whole uncommitted tree — evidence: T-0038 and T-0039, one-sentence prompt/digest changes, each needed an adversary audit because earlier tasks' uncommitted package.json and guard.mjs edits were in the tree
## Interpretation
T-0078 + T-0079: the security trigger, scope check, audit prep and --affected judge everything since the start commit, so uncommitted work from before the task (or a never-committed repo) makes every task own every file: adversary lenses and scope logs for files it never touched.
## Assumptions (confidence)
## Acceptance criteria
- [x] work from before the task isn't its change; its own sensitive edit to an already-dirty file still is; works with no commit — verify with `python3 -m unittest discover -s plugin/tests -q -p test_diff_gates.py`
- [x] all gates — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) at focus record base_tree = worktree_tree() (a git tree of the working files, untracked included; no commit needed) and diff base_tree against the current worktree tree; fall back to the start commit when the tree object is gone; (b) subtract files dirty at focus from the changed list. Choice (a): exact per-line diff, so a sensitive edit to a file that was already dirty still counts, and it works with no commits. (b) would miss those edits.
## Risks and rollback
Risk: under-triggering the adversary lens (security). Mitigation: per-line diff from the snapshot (not a file subtraction), fallback to the start commit, tests for the already-dirty case. Rollback: revert the commit; base_tree is an extra meta field old code ignores.
## Execution prompt
## Steps
1. [x] red tests
2. [x] base_tree at focus; task_base/task_diff; fmmap.changed diffs trees
3. [x] use in done, audit prep, --affected
4. [x] gates, docs, one reviewer pass
## Resume here
<!-- auto -->
- 2026-10-03T04:19:43Z step 4/4: gates, docs, one reviewer pass
- git: foreman/build; 16 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/evals/guard-force-push/prompt.md, plugin/evals/guard-publish/prompt.md, plugin/evals/intake-block/prompt.md, plugin/evals/mid-task-capture/prompt.md, plugin/evals/one-liner/prompt.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py
- failures met: json.decoder.jsondecodeerror: expecting ',' delimiter: line 0 column 0 (char 0)
## Docs impact
CHANGELOG.md: task judged by its own changes
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -q -p test_diff_gates.py -k dirty -k before_the_task` → red: pre-task work counted as the task's (1 failure); the already-dirty guard test passes (2026-10-03T03:59:48Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -q -p test_diff_gates.py` → exit 0 · Ran 10 tests in 4.598s / OK [ran] [tree 6c173200971d] (2026-10-03T04:18:32Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -q -p test_diff_gates.py` → 10 pass; 2 new fail without the lib change (stash check) (2026-10-03T04:18:32Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -q -p test_diff_gates.py` → done(), audit prep and --affected use task_base (2026-10-03T04:18:32Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → ✗ exit 1 · 1 of 4 failed: python3 -m unittest discover -s plugin/tests -q → ✗ exit 1 · Ran 535 tests in 198.689s / FAILED (failures=4) [ran] [tree eedef54ae32a] (2026-10-03T04:25:35Z)
- (step 4) `fm check: python3 -m unittest discover -s plugin/tests -q; fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · 4 passed: python3 -m unittest discover -s plugin/tests -q → exit 0 · Ran 535 tests in 167.925s / OK; fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                34.6    36.1     150  [0] / SessionEnd                  31.7    37.0     150  [0] [ran] [tree 4e5e744bbf3d] (2026-10-03T04:32:15Z)
- (step 4) `fm check` → gates exit 0; reviewer findings fixed (fail closed, focus log) (2026-10-03T04:32:15Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -q -p test_diff_gates.py` → exit 0 · Ran 11 tests in 5.380s / OK [ran] [tree 4e5e744bbf3d] (2026-10-03T04:32:27Z)
- (ac 2) `fm check` → exit 0 · ✓ all 4 gates passed on this exact tree already (run at 04:32 UTC); cached (fm check --fresh reruns) [ran] [tree 4e5e744bbf3d] (2026-10-03T04:32:27Z)
- (audit intent) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → a task is judged by its own changes; pre-task work and never-committed repos no longer force adversary/scope noise [tree 4e5e744bbf3d] (2026-10-03T04:32:27Z)
- (audit adversary) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → the task's own + lines are always diffed (already-dirty file, mid-task commits); base fields aren't settable via fm task set; a diff git can't produce now fails closed with the reason (tested with an unreadable file) [tree 4e5e744bbf3d] (2026-10-03T04:32:27Z)
- (audit edge) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → no commits (tested), pruned snapshot falls back to the start commit, never-focused tasks keep the old path, git failure in changed() falls back to the wider list [tree 4e5e744bbf3d] (2026-10-03T04:32:27Z)
- (audit operator) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → focus logs when the snapshot fails; diff timeout raised to 300 s to match audit prep [tree 4e5e744bbf3d] (2026-10-03T04:32:27Z)
- (audit maintainer) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → one task_base/task_diff pair used by done, audit prep, --affected and fmmap.changed [tree 4e5e744bbf3d] (2026-10-03T04:32:27Z)
- (audit intent) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → a task is judged by its own changes; pre-task work and never-committed repos no longer force adversary/scope noise [tree 4e5e744bbf3d] (2026-10-03T04:32:33Z)
- (audit adversary) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → the task's own + lines are always diffed (already-dirty file, mid-task commits); base fields aren't settable via fm task set; a diff git can't produce now fails closed with the reason (tested with an unreadable file) [tree 4e5e744bbf3d] (2026-10-03T04:32:33Z)
- (audit edge) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → no commits (tested), pruned snapshot falls back to the start commit, never-focused tasks keep the old path, git failure in changed() falls back to the wider list [tree 4e5e744bbf3d] (2026-10-03T04:32:33Z)
- (audit operator) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → focus logs when the snapshot fails; diff timeout raised to 300 s to match audit prep [tree 4e5e744bbf3d] (2026-10-03T04:32:33Z)
- (audit maintainer) `one fm-reviewer pass (research T-0078-review); MEDIUM fail-open and LOW silent snapshot failure fixed test-first` → one task_base/task_diff pair used by done, audit prep, --affected and fmmap.changed [tree 4e5e744bbf3d] (2026-10-03T04:32:33Z)
## Log
- 2026-09-27T13:12:41Z created
- 2026-10-03T03:59:35Z planned from capture
- 2026-10-03T03:59:36Z focused
- 2026-10-03T03:59:53Z user approved core in Claude Code's permission prompt
- 2026-10-03T04:02:31Z paused: focus moved to T-0119
- 2026-10-03T04:18:27Z focused
- 2026-10-03T04:19:43Z paused: focus moved to T-0121
- 2026-10-03T04:21:29Z focused
- 2026-10-03T04:32:33Z scope: the mods/foreman-ui changes are T-0121's (done), uncommitted in the same tree; this task was focused before snapshots existed
- 2026-10-03T04:32:33Z done
- 2026-10-03T04:32:42Z includes T-0079: Scope check and security pre-audit use the whole uncommitted tree, so in a never-committed
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-final-operator: Not directly related. I have sufficient evidence now. Let me finalize.
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- research brainstorm-20260926-super-slate: Built under T-0071, in rounds (inbox items folded in):
- research t0018-r9-adversary-maintainer: HIGH — ADVERSARY — `plugin/lib/fmcli.py:710-716` (via `_agent_report` at `plugin/lib/fmcli.py:607-610`) — unguarded non-regular f…
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, plugin/tests/test_guard.py, plugin/tests/test_hooks.py, plugin/tests/test_ideas.py, plugin/tests/test_plugins.py, pl…
## Preflight
Changed in scope since this was planned (2026-09-27): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmideas.py, plugin/lib/fmmap.py, plugin…; re-ground the plan against them before editing
## Lessons
- A check that reads a diff must tell empty from unavailable; fail closed on unavailable
## Files touched
- plugin/tests/test_diff_gates.py
- plugin/lib/fmcore.py
- plugin/lib/fmmap.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
