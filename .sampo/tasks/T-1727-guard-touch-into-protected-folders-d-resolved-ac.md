---
id: T-1727
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, plugin/tests/test_guard_evasions.py, plugin/tests/guard_corpus*, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T03:33:02Z
updated: 2026-10-23T05:05:44Z
batch: [T-1680, T-1487, T-1482]
base: eba3e2b1e976c55e006c19f50e9d3e1eb9276a01
base_tree: 0cf8b41c796a5fc41de2458bf80f7903d7792c4a
plan0_at: 2026-10-23T03:33:50Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, plugin/tests/test_guard_evasions.py, plugin/tests/guard_corpus*, CHANGELOG.md]
verified: strong
---
# Guard: touch into protected folders, $D resolved across ; and &&, obfuscated snapshot commands
## Raw request
> T-1680: Guard: touch NEW_FILE in a protected folder (Claude Code's plugin cache, e.g. ~/.claude/plugins/cache/x/hooks/hooks.json) is allowed while echo/cp/truncate there are refused; touch creating a file there should be judged as a write (found by T-1605's probe)
> T-1487: Guard false block: D=/literal; mkdir -p $D && git init -q $D && printf … > $D/p.sh is refused as a tree write over protected core: with ; mixed with && the env is None, $D is unresolved and the guess falls back to cwd (fmguard.py:2382-2394, 2700-2705, 1880-1884). Make it resolve, add the forms to test_guard_diff FORMS (and keep D=~ … git init blocked), and say '$D unresolved' instead of 'git init writes its folder'
> T-1482: Guard corpus: cover the obfuscated forms of the four bench SNAPSHOT commands (git reset --hard HEAD~5, git checkout -- ., git clean, git stash drop…) from a disposable git folder, so a variant like \git reset --hard that skips the snapshot is caught; T-1263 left them out because their verdict depends on the tree
## Interpretation
Do T-1680, T-1487, T-1482 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1727. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1680: touch creating a file in a protected folder (Claude Code's plugin cache) is judged as a write and refused like echo, cp and truncate there — verify with `python3 plugin/tests/run.py test_guard.ProtectedTouch`
- [x] T-1487: D=/literal; mkdir -p $D && git init -q $D && printf … > $D/p.sh resolves $D and passes outside core; D=~ … git init $D still refuses; the message says '$D unresolved' when it can't resolve — verify with `cd plugin/tests && python3 -m unittest test_guard_diff test_guard.GitInitTarget`
- [x] T-1482: the evasion corpus covers obfuscated forms of the bench SNAPSHOT commands (\git reset --hard, quoted or env-prefixed git checkout -- ., git clean, git stash drop) run from a disposable git folder, and each is snapshotted or refused — verify with `python3 plugin/tests/run.py test_guard_evasions`
## Non-goals
## Approach (options → choice → why)
Three guard fixes, each test-first in the existing tables. (1) T-1680: touch with a path that doesn't exist yet in a protected folder creates a file: judge it with the same write check as echo > / cp / truncate (options: a touch special case in the write-target finder (chosen: one place every caller routes through); refuse every touch in protected folders (rejected: touch on an existing file only changes times); leave it (rejected: a new hooks.json in the plugin cache runs as a hook)). (2) T-1487: an assignment D=/literal before ; or && must resolve $D for later commands in the same line; keep D=~ … git init $D refused; say '$D unresolved' when it can't. (3) T-1482: add the obfuscated SNAPSHOT forms to test_guard_evasions with a disposable git folder; fix the guard if a form skips the snapshot. Never loosen any existing refusal; every existing guard test stays green.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1680: Guard: touch NEW_FILE in a protected folder (Claude Code's plugin cache, e.g. ~/.claude/pl
2. [x] T-1487: failing tests
3. [x] T-1487: resolve the variable across ; and &&
4. [x] T-1482: Guard corpus: cover the obfuscated forms of the four bench SNAPSHOT commands (git reset --
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.ProtectedTouch` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: ProtectedTouch 0s) / OK [ran] [tree 6de76b190c5c] (2026-10-23T03:44:05Z)
- (step 2) `python3 plugin/tests/run.py test_guard.GitInitTarget` → ✗ exit 1 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: GitInitTarget 0s) / FAILED (1 classes) [ran] [tree 6de76b190c5c] (2026-10-23T03:44:11Z)
- (step 3) `python3 plugin/tests/run.py test_guard.GitInitTarget test_guard_diff` → exit 0 · Ran 5 tests in 6.0s (2 classes, 16 at a time; slowest: GuardAgainstBash 6s, GitInitTarget 0s) / OK [ran] [tree c724eb92bfc9] (2026-10-23T03:46:26Z)
- (step 4) `python3 plugin/tests/run.py test_guard_evasions` → exit 0 · Ran 4 tests in 1.4s (2 classes, 16 at a time; slowest: GuardEvasions 1s, SnapshotForms 1s) / OK [ran] [tree ea6e1f74d211] (2026-10-23T03:47:30Z)
- (step 4) `python3 plugin/tests/run.py test_guard_evasions test_guard.ProtectedTouch test_guard.GitCAfterC test_guard.GitInitTarget` → exit 0 · Ran 10 tests in 11.9s (5 classes, 16 at a time; slowest: GuardEvasions 11s, SnapshotForms 11s, GitInitTarget 1s) / OK [ran] [tree 87f4058eed10] (2026-10-23T04:20:53Z)
- (step 4) `python3 plugin/tests/run.py test_guard_evasions test_guard.ProtectedTouch test_guard.GitCAfterC test_guard.GitInitTarget` → exit 0 · Ran 12 tests in 5.8s (5 classes, 16 at a time; slowest: SnapshotForms 6s, GuardEvasions 2s, ProtectedTouch 1s) / OK [ran] [tree f2b708a6d6d0] (2026-10-23T04:53:34Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.ProtectedTouch` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: ProtectedTouch 0s) / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:03:25Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_guard_diff test_guard.GitInitTarget test_guard.GitCAfterC` → exit 0 · Ran 6 tests in 5.278s / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:03:31Z)
- (ac 3) `python3 plugin/tests/run.py test_guard_evasions` → exit 0 · Ran 7 tests in 2.0s (2 classes, 16 at a time; slowest: SnapshotForms 2s, GuardEvasions 1s) / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:03:33Z)
- (step 1) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_evasions test_guard_git test_snapshots test_hooks` → exit 0 · Ran 488 tests in 49.1s (106 classes, 16 at a time; slowest: Stop 49s, NoTaskGate 35s, PreToolUse 29s) / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:04:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard_diff test_guard.GitInitTarget` → exit 0 · Ran 5 tests in 5.277s / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:04:46Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.ProtectedTouch` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: ProtectedTouch 0s) / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:04:55Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_guard_diff test_guard.GitInitTarget` → exit 0 · Ran 5 tests in 5.535s / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:04:55Z)
- (ac 3) `python3 plugin/tests/run.py test_guard_evasions` → exit 0 · Ran 7 tests in 1.9s (2 classes, 16 at a time; slowest: SnapshotForms 2s, GuardEvasions 1s) / OK [ran] [tree 2c91f0affb1c] (2026-10-23T05:04:55Z)
- (audit intent) `two fm-reviewer passes: first found a HIGH loosening (-C <core> -C $D) plus nested-cwd, per-kind dedupe, variables, touch-then-run false block, unlink-then-touch, latency and a weak test; second found no loosening and a MEDIUM nested relative cd plus nits; all fixed test-first; 488 guard and hook tests pass after the merge; hook bench Bash p95 98.8 ms CPU (budget 150)` → touch creating a file in a protected folder is a write; $D set to an absolute path or ~ is read where it points for git init and -C; obfuscated discarding git commands are snapshotted like plain ones [tree 2c91f0affb1c] (2026-10-23T05:04:55Z)
- (audit adversary) `two fm-reviewer passes: first found a HIGH loosening (-C <core> -C $D) plus nested-cwd, per-kind dedupe, variables, touch-then-run false block, unlink-then-touch, latency and a weak test; second found no loosening and a MEDIUM nested relative cd plus nits; all fixed test-first; 488 guard and hook tests pass after the merge; hook bench Bash p95 98.8 ms CPU (budget 150)` → compared every refusal of the base on the touched paths: none loosened (reviewer verified); -C $D is read both alone and under the previous folder; a computed or quoted git name, eval, sh -c and sh <<< are all recorded for a snapshot in the folder they run in; an unfollowable cd saves nothing and says so rather than saving the wrong repo [tree 2c91f0affb1c] (2026-10-23T05:04:55Z)
- (audit edge) `two fm-reviewer passes: first found a HIGH loosening (-C <core> -C $D) plus nested-cwd, per-kind dedupe, variables, touch-then-run false block, unlink-then-touch, latency and a weak test; second found no loosening and a MEDIUM nested relative cd plus nits; all fixed test-first; 488 guard and hook tests pass after the merge; hook bench Bash p95 98.8 ms CPU (budget 150)` → touch -c/--no-create and abbreviated --da/--ref/--ti take their values; touch then run is allowed (not a written script); saves share one deadline [tree 2c91f0affb1c] (2026-10-23T05:04:55Z)
- (audit operator) `two fm-reviewer passes: first found a HIGH loosening (-C <core> -C $D) plus nested-cwd, per-kind dedupe, variables, touch-then-run false block, unlink-then-touch, latency and a weak test; second found no loosening and a MEDIUM nested relative cd plus nits; all fixed test-first; 488 guard and hook tests pass after the merge; hook bench Bash p95 98.8 ms CPU (budget 150)` → the hook's note says what was saved where, or why nothing was [tree 2c91f0affb1c] (2026-10-23T05:04:55Z)
## Log
- 2026-10-23T03:33:02Z created
- 2026-10-23T03:33:13Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_guard.ProtectedTouch`
- 2026-10-23T03:33:13Z criterion 1 text: T-1680: Guard: touch NEW_FILE in a protected folder (Claude Code's plugin cache, e.g. ~/.claude/pl works → T-1680: touch creating a file in a protected folder (Claude Code's plugin cache) is judged as a write and refused like echo, cp and truncate there
- 2026-10-23T03:33:17Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_guard_evasions`
- 2026-10-23T03:33:17Z criterion 3 text: T-1482: Guard corpus: cover the obfuscated forms of the four bench SNAPSHOT commands (git reset -- works → T-1482: the evasion corpus covers obfuscated forms of the bench SNAPSHOT commands (\git reset --hard, quoted or env-prefixed git checkout -- ., git clean, git stash drop) run from a disposable git folder, and each is snapshotted or refused
- 2026-10-23T03:33:29Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_guard_diff.py', 'plugin/tests/test_guard_evasions.py', 'plugin/tests/guard_corpus*', 'CHANGELOG.md']
- 2026-10-23T03:33:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1727.builder.md
- 2026-10-23T03:33:49Z focused
- 2026-10-23T05:03:19Z merged worktree-agent-a983f36746e405765 (7 file(s))
- 2026-10-23T05:03:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a983f36746e405765
- 2026-10-23T05:03:24Z focused
- 2026-10-23T05:04:33Z scope: plugin/lib/fmhooks.py (_snapshot_note: the guard's discards, one deadline), plugin/tests/fixtures/gen_evasions.py (docstring), plugin/tests/test_guard_git.py, test_snapshots.py, test_hooks.py, CHANGELOG.md
- 2026-10-23T05:05:44Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1263-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I could only read files here, so I did…
- T-1585 [SECURITY M, done, 7 steps] Batch: Guard: interpreter one-liners that read…; Guard: env -u CLAUDECODE (or CLAUDE_COD…; Guard gaps (noticed in T-156… — lesson: Rep…
- research T-1517-review: Verdict:** approve with nits. I found no bypass of the guard lock, no guard rule change, and nothing dangerous or secret in the allow-corpus. The…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/test_guard_diff.py, plugin/tests/test_guard_evasions.py; re-ground the plan against them before editing
## Why not caught
T-1263's corpus left the snapshot commands out because their verdict depends on the tree; T-1605's probe found touch; the $D join was a reported false block
## Lessons
- When the guard reads a command for one purpose (verdict), let other consumers (snapshots) reuse that reading instead of a cruder second parse
## Plan gaps
- failed first: step 2 T-1487: failing tests
## Files touched
- plugin/tests/test_guard_evasions.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard_diff.py
- plugin/lib/fmhooks.py
- plugin/tests/fixtures/gen_evasions.py
- CHANGELOG.md
