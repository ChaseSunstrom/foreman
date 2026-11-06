---
id: T-1179
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_file_map_close.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-16T12:20:10Z
updated: 2026-10-16T12:31:35Z
base: 8a2f90ed97a704a36866dc03e677ccc19f450367
base_tree: 98ebaabdad6810404a9284aef7cfba8f038caeda
plan0_at: 2026-10-16T12:21:22Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_file_map_close.py, CHANGELOG.md]
verified: strong
---
# Catch it earlier: T-0787 ran test_workflows only; the doctor's file-map rule is checked by
## Raw request
> T-1178 (MASTER file map row for plugin/workflows (fm doctor fails release-check without it)) wasn't caught before it shipped: T-0787 ran test_workflows only; the doctor's file-map rule is checked by release-check in the full gates
## Interpretation
A task that adds a new top-level entry under plugin/ in a repo whose MASTER.md has a File map can't close until the map lists it: fm task finish runs fmdoctor.check_file_map when the task's changed files include a plugin/<entry> the map doesn't cover, and refuses naming the entry and the row to add. Otherwise the gap shows only in release-check during the full gates.
## Assumptions (confidence)
## Acceptance criteria
- [x] finish refuses a task that added plugin/newdir/x with no map row, naming plugin/newdir; with the row it closes; a repo with no MASTER.md file map is unaffected — verify with `python3 plugin/tests/run.py test_file_map_close`
## Non-goals
## Approach (options → choice → why)
Options: (a) in the close's checks (next to the docs gate), call fmdoctor.check_file_map(root, MASTER.md) only when a changed file's plugin/<entry> isn't covered, refusing with its message; (b) a test that runs check_file_map on the real repo, linked to every plugin/ file (runs too often); (c) a PostToolUse warning on directory creation (Write doesn't create dirs explicitly). Choice: (a): cheap, only on the rare trigger, enforced by Foreman, not remembered.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_file_map_close.py)
2. [x] The file-map gate in fm task finish
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_file_map_close` → ✗ exit 1 · Ran 4 tests in 1.2s (1 classes, 16 at a time; slowest: FileMapClose 0s) / FAILED (1 classes) [ran] [tree 1429f84ece84] (2026-10-16T12:21:43Z)
- (step 2) `python3 plugin/tests/run.py test_file_map_close` → exit 0 · Ran 4 tests in 0.4s (1 classes, 16 at a time; slowest: FileMapClose 0s) / OK [ran] [tree 3b3396eabfed] (2026-10-16T12:21:54Z)
- (ac 1) `python3 plugin/tests/run.py test_file_map_close test_cli` → exit 0 · Ran 106 tests in 21.0s (29 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 8s, AuditPrep 7s) / OK [ran] [tree fda321eb1f9b] (2026-10-16T12:29:58Z)
- (ac 1) `python3 plugin/tests/run.py test_file_map_close` → exit 0 · Ran 4 tests in 0.3s (1 classes, 16 at a time; slowest: FileMapClose 0s) / OK [ran] [tree 12daab8ec822] (2026-10-16T12:30:04Z)
- (audit edge) `self: reviewed merged diff: runs fmdoctor.check_file_map only when the task's diff touches plugin/<entry>, refuses only for entries this task changed that the map lacks; a map problem the task didn't cause doesn't block it` → no MASTER.md or no File map section: unaffected; a renamed doctor message would stop the gate, and its test would fail [tree 12daab8ec822] (2026-10-16T12:30:04Z)
- (audit self) `self: reviewed merged diff: runs fmdoctor.check_file_map only when the task's diff touches plugin/<entry>, refuses only for entries this task changed that the map lacks; a map problem the task didn't cause doesn't block it` → no findings [tree 12daab8ec822] (2026-10-16T12:30:04Z)
## Log
- 2026-10-16T12:20:10Z created
- 2026-10-16T12:21:04Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_file_map_close.py', 'CHANGELOG.md'], status=planned
- 2026-10-16T12:21:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1179.builder.md
- 2026-10-16T12:21:22Z focused
- 2026-10-16T12:29:33Z merged worktree-agent-afeb00249871aca57 (2 file(s))
- 2026-10-16T12:29:36Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afeb00249871aca57
- 2026-10-16T12:29:36Z focused
- 2026-10-16T12:31:34Z done
- 2026-10-16T12:31:35Z committed 42183320 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-0952 [FEATURE S, done, 1 steps] --affected also runs tests that historically change together with the edited files (the map's co-change pairs), so a hooks.json edit ru…
- decision 2026-10-16: T-1040 self-approved under full autonomy: per-row branches with a rail and compact finished calls, chat setting tree\
- similar finished tasks took 1–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Plan gaps
- failed first: step 1 Failing tests (test_file_map_close.py)
## Files touched
- plugin/tests/test_file_map_close.py
- plugin/lib/fmcli.py
- CHANGELOG.md
