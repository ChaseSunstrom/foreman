---
id: T-0884
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:29:55Z
updated: 2026-10-15T15:55:31Z
base: 8e02e1f27d1ad86f48a49629afb6d8272c3cadc8
base_tree: 2fc458e1fb62e46733e9198119a16f7463e2db08
verified: strong
---
# Snapshot uncommitted work before a Bash command discards it (git reset --hard, checkout --
## Raw request
> FEATURE: Snapshot uncommitted work before a Bash command discards it (git reset --hard, checkout -- paths / -f, restore without --staged, clean -f, stash drop/clear, switch -f / --discard-changes); fm snapshots lists them with the command that restores one
> CONTEXT: round 5 #1 (deferred T-0868). The guard asks only for these on the default branch; on a feature branch they run unasked, and Claude Code's rewind covers its file tools, not Bash
> MUST: snapshot only when the tree has uncommitted changes; never block the command; a snapshot is a commit under refs/foreman/snapshots so gc keeps it; fm tidy prunes ones older than 14 days
## Interpretation
Before a Bash command that throws away uncommitted work runs (git reset --hard/--merge, checkout -f/--/paths, restore of the worktree, clean -f, switch -f/--discard-changes, rm -f, merge/rebase/cherry-pick/revert/am --abort), Foreman saves the working files (untracked included, ignored not) as a commit under refs/foreman/snapshots when they differ from HEAD, tells Claude the sha and the restore command, and fm snapshots lists them. Never blocks or asks; fm tidy prunes snapshots older than 14 days.
## Assumptions (confidence)
## Acceptance criteria
- [x] a discarding git command with changes leaves a snapshot that restores them; a clean tree or a harmless command leaves none — verify with `python3 plugin/tests/run.py test_snapshots`
## Non-goals
## Approach (options → choice → why)
1) Snapshot in the PreToolUse hook once the guard allows the command (chosen: no friction, works on every branch, the commit survives gc under its ref). 2) Block these commands and ask (friction; the guard asks only on the default branch on purpose). 3) git stash before the command (changes the user's stash list and the tree; surprising). 4) Autosnapshot on every edit (cost on every call). Complete version: detection via the guard's own tokenizer (wrappers, env, sudo stripped; -C honoured), snapshot only when the tree differs from HEAD, identity-independent commit, fm snapshots list with restore line, tidy prune, docs. Ceiling: a cd earlier in the command isn't followed (snapshots the session's repo); stash drop/clear not covered (fsck keeps dangling stashes ~2 weeks).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: test_snapshots.py (hook saves, restore works, clean tree/harmless cmd saves nothing, detection table)
2. [x] fmguard.discards_work + fmcore.snapshot + hook note
3. [x] fm snapshots verb, tidy prune, docs (MASTER, CHANGELOG)
## Resume here
<!-- auto -->
- 2026-10-15T15:44:46Z steps 3/3 done
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmtidy.py, plugin/tests/test_snapshots.py
- touched since last checkpoint: plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmtidy.py, plugin/lib/fmcli.py, plugin/tests/test_snapshots.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER §9 Work snapshots; CHANGELOG round 5
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_snapshots` → exit 0 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: Snapshots 1s) / OK [ran] [tree c613a0b26727] (2026-10-15T15:41:15Z)
- (step 2) `python3 plugin/tests/run.py test_snapshots test_guard test_guard_git test_hooks test_tidy test_help` → exit 0 · Ran 267 tests in 27.6s (69 classes, 16 at a time; slowest: Stop 28s, PreToolUse 15s, SessionStart 12s) / OK [ran] [tree c613a0b26727] (2026-10-15T15:41:49Z)
- (step 3) `python3 plugin/tests/run.py test_snapshots test_tidy test_help test_docs` → exit 0 · Ran 51 tests in 1.8s (18 classes, 16 at a time; slowest: Apply 2s, Snapshots 1s, Repeats 1s) / OK [ran] [tree 2c25c6f6618e] (2026-10-15T15:42:09Z)
- (step 2) `python3 plugin/tests/run.py test_snapshots test_guard test_guard_git test_hooks test_tidy test_help test_cli` → exit 0 · Ran 357 tests in 30.2s (93 classes, 16 at a time; slowest: Stop 30s, TaskLifecycle 21s, PreToolUse 18s) / OK [ran] [tree d65208253f96] (2026-10-15T15:52:53Z)
- (step 3) `python3 plugin/tests/run.py test_snapshots test_docs` → exit 0 · Ran 37 tests in 1.8s (11 classes, 16 at a time; slowest: Snapshots 2s, TaskLifecycle 1s, TaskDocsDrift 0s) / OK [ran] [tree d65208253f96] (2026-10-15T15:52:55Z)
- (ac 1) `python3 plugin/tests/run.py test_snapshots` → exit 0 · Ran 6 tests in 1.9s (1 classes, 16 at a time; slowest: Snapshots 2s) / OK [ran] [tree d65208253f96] (2026-10-15T15:55:30Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge): 3 MEDIUM + 6 LOW; all fixed but two LOWs kept as documented limits (untracked secrets ride in the local ref 14 days; repo fsmonitor as worktree_tree everywhere). Hook p95 39 ms on non-discarding commands; fm replay 0 newly allowed` → every discarding form the brief names saves the work first (tree or stash commits), the note gives the sha and a restore line that works from any subdirectory; a clean tree, a blocked command, a harmless command or a heredoc mentioning one saves nothing (tests: 6, restore round trip included) [tree d65208253f96] (2026-10-15T15:55:30Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge): 3 MEDIUM + 6 LOW; all fixed but two LOWs kept as documented limits (untracked secrets ride in the local ref 14 days; repo fsmonitor as worktree_tree everywhere). Hook p95 39 ms on non-discarding commands; fm replay 0 newly allowed` → review found the 5 s hook timeout could block a command on a big untracked tree: the save now has 3 s and reports when it couldn't; commit-tree runs with gpgSign off (no pinentry hang) and a fixed identity; the command text reaches only the commit message (redacted, control chars stripped), never a ref name [tree d65208253f96] (2026-10-15T15:55:30Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge): 3 MEDIUM + 6 LOW; all fixed but two LOWs kept as documented limits (untracked secrets ride in the local ref 14 days; repo fsmonitor as worktree_tree everywhere). Hook p95 39 ms on non-discarding commands; fm replay 0 newly allowed` → cd before the git call, sh -c text, ~ and $VARS in -C, worktree remove --force, stash drop/clear and branch-named folders handled; --git-dir/--work-tree and python-spawned git stay out (MASTER limits) [tree d65208253f96] (2026-10-15T15:55:30Z)
## Log
- 2026-10-15T15:29:55Z created
- 2026-10-15T15:39:18Z focused
- 2026-10-15T15:45:13Z paused: focus moved to T-0887
- 2026-10-15T15:49:01Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T15:49:01Z focused
- 2026-10-15T15:49:02Z review (intent/adversary/edge): accepted — stash drop/clear, cd and bash -c and ~ in -C, hook timeout 5 s (bound the snapshot to ~3 s, say when not saved), vacuous clean-tree test, branch-named dirs, restore line from a subdirectory (:/ and -C), worktree remove --force, control chars; kept as documented limits — secrets in untracked files ride along in local refs 14 days, repo fsmonitor (as worktree_tree everywhere), --git-dir/--work-tree
- 2026-10-15T15:55:31Z done
- 2026-10-15T15:55:31Z committed ae42999 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round5-20261015: Probe: `fm ideas` with capability map + unspoken needs, 2 rounds, past every earlier ideas.md (brainstorm-20261015-101633): 54 new t…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–6 steps
## Lessons
- A hook that does real work before a tool call inherits the hook's timeout and its onFailure: give that work a budget under the timeout and say when it ran out, or 'never blocks' quietly becomes 'blocks on big repos'
## Files touched
- plugin/tests/test_snapshots.py
- plugin/lib/fmguard.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmtidy.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
