---
id: T-1751
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T05:06:05Z
updated: 2026-10-23T05:09:30Z
batch: [T-1744, T-1745]
base: ab143eebce9771edd6e47e381a50f61b9c1597c2
base_tree: 2c91f0affb1c9c346db89b2f917057b7fdc4b33e
plan0_at: 2026-10-23T05:07:08Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, CHANGELOG.md]
verified: strong
---
# Guard: mv judged at its source too (moving a protected file out removes it), git -C X clone url dir judged under X
## Raw request
> T-1744: Guard: mv SOURCE out of a protected folder (mv ~/.claude/plugins/cache/x/hooks/hooks.json /tmp/x, or out of core) isn't refused because _write_targets returns only mv's destination; a move removes the source and must be judged as a write there too
> T-1745: Guard: git -C X clone url dir judges dir without joining it onto X
## Interpretation
Do T-1744, T-1745 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1751. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1744: mv with a source in a protected folder (plugin cache, core, Claude Code settings) is refused like a write there; moving an unprotected file is unchanged — verify with `python3 plugin/tests/run.py test_guard.MoveSource`
- [x] T-1745: git -C X clone url dir judges X/dir (and dir alone when absolute), so a clone into a protected folder via -C is refused — verify with `python3 plugin/tests/run.py test_guard.GitCAfterC`
## Non-goals
## Approach (options → choice → why)
Ground in fmguard._write_targets (mv returns only the destination) and _under_git_c (from T-1727). mv: return every source operand as well as the destination (a move removes its sources), honouring -t DIR and --target-directory. Capture other source-removing forms (rsync --remove-source-files) rather than widen this task. clone: join the destination onto the -C folder list exactly as T-1727's checkout and clean paths do. Never loosen an existing refusal; every guard suite stays green; add both forms to test_guard_diff FORMS if that table covers the shape.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1744: Guard: mv SOURCE out of a protected folder (mv ~/.claude/plugins/cache/x/hooks/hooks.json
2. [x] T-1745: Guard: git -C X clone url dir judges dir without joining it onto X
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.MoveSource test_guard.GitCAfterC` → red as expected (exit 1) · Ran 3 tests in 0.5s (2 classes, 16 at a time; slowest: GitCAfterC 0s, MoveSource 0s) / FAILED (2 classes) [ran] [tree 7e4357f7e1df] (2026-10-23T05:07:37Z)
- (step 2) `cd ~/.claude/foreman && python3 plugin/tests/run.py test_guard.MoveSource test_guard.GitCAfterC 2>&1 | grep -E "arg=|^OK|FAILED \(" | head -10` → exit 0 · OK [ran] [tree 65f839ee981b] (2026-10-23T05:08:24Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_evasions test_guard_git test_guard_cases test_guard_pipes test_guard_hardening test_snapshots` → exit 0 · Ran 290 tests in 10.5s (84 classes, 16 at a time; slowest: Mutation 10s, GuardAgainstBash 7s, Trust 6s) / OK [ran] [tree 65f839ee981b] (2026-10-23T05:08:40Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.MoveSource` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: MoveSource 0s) / OK [ran] [tree 79f2bffd493d] (2026-10-23T05:09:08Z)
- (ac 2) `python3 plugin/tests/run.py test_guard.GitCAfterC` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: GitCAfterC 0s) / OK [ran] [tree 79f2bffd493d] (2026-10-23T05:09:09Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.MoveSource` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: MoveSource 0s) / OK [ran] [tree 79f2bffd493d] (2026-10-23T05:09:17Z)
- (ac 2) `python3 plugin/tests/run.py test_guard.GitCAfterC` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: GitCAfterC 0s) / OK [ran] [tree 79f2bffd493d] (2026-10-23T05:09:17Z)
- (audit adversary) `self: _write_targets keeps its old destination list unchanged (so nothing loosens) and adds mv's sources (all positionals with -t, all but the last otherwise) and rsync --remove-source-files' sources; git clone's destination and --separate-git-dir are joined under the -C folders with T-1727's _under_git_c; 290 guard tests pass; fm replay: 0 newly blocked, 0 newly allowed, 124 labelled cases, 0 drifted` → mv, mv -t, mv --target-directory= and rsync --remove-source-files out of the plugin cache or core are refused; git -C core clone url dir is refused; absolute destinations still win; cp and plain rsync (copies) are unchanged [tree 79f2bffd493d] (2026-10-23T05:09:17Z)
- (audit edge) `self: _write_targets keeps its old destination list unchanged (so nothing loosens) and adds mv's sources (all positionals with -t, all but the last otherwise) and rsync --remove-source-files' sources; git clone's destination and --separate-git-dir are joined under the -C folders with T-1727's _under_git_c; 290 guard tests pass; fm replay: 0 newly blocked, 0 newly allowed, 124 labelled cases, 0 drifted` → moving a project file without an active task is now refused at its source as well as its destination (both are in the project, so the verdict is the same); mv's sources include an extra name when -t is given, which only widens [tree 79f2bffd493d] (2026-10-23T05:09:17Z)
- (audit self) `self: _write_targets keeps its old destination list unchanged (so nothing loosens) and adds mv's sources (all positionals with -t, all but the last otherwise) and rsync --remove-source-files' sources; git clone's destination and --separate-git-dir are joined under the -C folders with T-1727's _under_git_c; 290 guard tests pass; fm replay: 0 newly blocked, 0 newly allowed, 124 labelled cases, 0 drifted` → no findings [tree 79f2bffd493d] (2026-10-23T05:09:17Z)
## Log
- 2026-10-23T05:06:05Z created
- 2026-10-23T05:06:18Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_guard.MoveSource`
- 2026-10-23T05:06:18Z criterion 1 text: T-1744: Guard: mv SOURCE out of a protected folder (mv ~/.claude/plugins/cache/x/hooks/hooks.json works → T-1744: mv (and cp --remove-destination? no: mv only) with a SOURCE in a protected folder (plugin cache, core, Claude Code settings) is refused like a write there; mv into an unprotected folder of an unprotected file is unchanged
- 2026-10-23T05:06:18Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_guard.GitCAfterC`
- 2026-10-23T05:06:18Z criterion 2 text: T-1745: Guard: git -C X clone url dir judges dir without joining it onto X works → T-1745: git -C X clone url dir judges X/dir (and dir alone when absolute), so a clone into a protected folder via -C is refused
- 2026-10-23T05:06:19Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_guard_diff.py', 'CHANGELOG.md']
- 2026-10-23T05:06:28Z criterion 1 text: T-1744: mv (and cp --remove-destination? no: mv only) with a SOURCE in a protected folder (plugin cache, core, Claude Code settings) is refused like a write there; mv into an unprotected folder of an unprotected file is unchanged → T-1744: mv with a source in a protected folder (plugin cache, core, Claude Code settings) is refused like a write there; moving an unprotected file is unchanged
- 2026-10-23T05:07:08Z focused
- 2026-10-23T05:09:28Z done
- 2026-10-23T05:09:30Z committed b21f5582 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1727 [SECURITY M, done, 4 steps] Guard: touch into protected folders, $D resolved across ; and &&, obfuscated snapshot commands — lesson: When the guard reads a comman…
- T-0722 [FIX S, done, 3 steps] Close-out friction: audit prep reads a builder's branch; a refused commit can be retried
- T-0817 [FIX M, done, 3 steps] Guard refusals read better: /dev/null on a data-only python -c, a state-direct hint that points to fm research, and pat… — lesson: A refusa…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 3–4 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
the write-target finder modelled copies, where only the destination changes; no row moved a protected file out
## Lessons
- A move is a delete at its source: judge both ends
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
