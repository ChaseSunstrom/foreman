---
id: T-2238
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:06:08Z
updated: 2026-10-31T01:57:31Z
inferred_deps: [T-2185]
inferred_why: T-2185: named in its request
base: 596e3e9a0ef18c4d9dee2e4e85a33ca40714cb56
base_tree: 12e58bf74a7276a7d982e217deb5b95f0b860806
plan0_at: 2026-10-31T01:39:13Z
plan0_scope: []
verified: strong
---
# fm find hotspots: rank files by git bug-fix history
## Raw request
> fm find hotspots: rank files by git bug-fix history (git log with fsmonitor and hooks off, no repo code run), as the input the bug rung reviews first (T-2185 rung b)
## Interpretation
T-2185 rung b: before a model reviews files for bugs (rung a, T-2242), rank them by where bugs were fixed before: files touched by many fix commits hold more bugs. Lexical commit-subject match, git only, no repo code.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find --hotspots PATH lists tracked files ranked by how many fix commits (subject says fix, bug, crash, regress, broken, revert of a fix) touched them in the last 500 commits, with counts and JSON; git runs with fsmonitor and hooks off, no repo code runs, symlinks and untracked files never count; fmfind.hotspots(root, n) returns the same rows for the bug rung — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots`
## Non-goals
## Approach (options → choice → why)
Options: (1) git log --name-only over fix-subject commits, counted per tracked file (chosen: cheap, no deps, works on any git repo); (2) git blame churn x age (slower, needs per-file blame); (3) issue tracker links (not local). Choice 1; decay by age is a later knob.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (FindHotspots) on a temp repo with fix and non-fix commits, a symlink and a renamed file
2. [x] fmfind.hotspots and fm find --hotspots
3. [x] docs (MASTER fmfind, CHANGELOG)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots 2>&1 | tail -15` → ✗ exit 1 · Ran 5 tests in 0.034s / FAILED (errors=5) [ran] [tree 879792ac9ffa] (2026-10-31T01:40:20Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots 2>&1 | tail -15` → ✗ exit 1 · Ran 5 tests in 0.360s / FAILED (failures=1) [ran] [tree e7fb461118f4] (2026-10-31T01:40:28Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots` → exit 0 · Ran 5 tests in 0.264s / OK [ran] [tree 4db950810463] (2026-10-31T01:40:54Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.32s] [ran] [tree 4db950810463] (2026-10-31T01:41:27Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)"` → ✗ exit 1 · Ran 12 tests in 0.532s / FAILED (failures=7) [ran] [tree 86dc51b24351] (2026-10-31T01:44:01Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)"` → exit 0 · Ran 64 tests in 17.917s / OK [ran] [tree f6d11ae76aa3] (2026-10-31T01:44:57Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_find test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.49s] [ran] [tree 0610a71ac1cb] (2026-10-31T01:45:46Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots` → ✗ exit 1 · Ran 12 tests in 0.628s / FAILED (failures=1, errors=10) (start tree + this task's tests) [ran] [tree 9600c4e8a386] (2026-10-31T01:55:46Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots` → exit 0 · Ran 12 tests in 0.634s / OK [ran] [tree 9600c4e8a386] (2026-10-31T01:55:46Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 65 tests in 17.696s / OK [ran] [tree 9600c4e8a386] (2026-10-31T01:56:09Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 65 tests in 17.705s / OK [ran] [tree 9600c4e8a386] (2026-10-31T01:56:27Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 65 tests in 17.724s / OK [ran] [tree 9600c4e8a386] (2026-10-31T01:56:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHotspots` → exit 0 · Ran 12 tests in 0.628s / OK [ran] [tree 9600c4e8a386] (2026-10-31T01:56:57Z)
- (audit intent) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 0d3b912f: git runs with showSignature off and every gpg program /bin/false (a forged-gpgsig test leaves no sentinel), --relative so a subdirectory path matches, -z records so odd names count, whole-word fix subjects (fixtures and Bugzilla don't count; a revert counts only when it reverts a fix), a git failure exits 2 with a warning instead of a clean-looking empty list, --hotspots with --rank or --capture is a usage error; test_find 65 green, red-to-green proven; on Foreman's repo it ranks CHANGELOG, MASTER, fmcli, fmexam, fmfind` → a ranked list of tracked files by fix commits in the last 500 non-merge commits, the input for the bug rung [tree 9600c4e8a386] (2026-10-31T01:56:57Z)
- (audit adversary) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 0d3b912f: git runs with showSignature off and every gpg program /bin/false (a forged-gpgsig test leaves no sentinel), --relative so a subdirectory path matches, -z records so odd names count, whole-word fix subjects (fixtures and Bugzilla don't count; a revert counts only when it reverts a fix), a git failure exits 2 with a warning instead of a clean-looking empty list, --hotspots with --rank or --capture is a usage error; test_find 65 green, red-to-green proven; on Foreman's repo it ranks CHANGELOG, MASTER, fmcli, fmexam, fmfind` → repo config can't run code through fsmonitor, hooks, signature checks or gpg programs; names are defanged; output bounded by commits, renameLimit and a timeout [tree 9600c4e8a386] (2026-10-31T01:56:57Z)
- (audit edge) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 0d3b912f: git runs with showSignature off and every gpg program /bin/false (a forged-gpgsig test leaves no sentinel), --relative so a subdirectory path matches, -z records so odd names count, whole-word fix subjects (fixtures and Bugzilla don't count; a revert counts only when it reverts a fix), a git failure exits 2 with a warning instead of a clean-looking empty list, --hotspots with --rank or --capture is a usage error; test_find 65 green, red-to-green proven; on Foreman's repo it ranks CHANGELOG, MASTER, fmcli, fmexam, fmfind` → subdirectory paths, tab and quote names, renames, symlinks and untracked files, a git failure all tested [tree 9600c4e8a386] (2026-10-31T01:56:57Z)
- (audit maintainer) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 0d3b912f: git runs with showSignature off and every gpg program /bin/false (a forged-gpgsig test leaves no sentinel), --relative so a subdirectory path matches, -z records so odd names count, whole-word fix subjects (fixtures and Bugzilla don't count; a revert counts only when it reverts a fix), a git failure exits 2 with a warning instead of a clean-looking empty list, --hotspots with --rank or --capture is a usage error; test_find 65 green, red-to-green proven; on Foreman's repo it ranks CHANGELOG, MASTER, fmcli, fmexam, fmfind` → _git is now the one git helper for fm find (fsmonitor, hooks, quotepath, gpg overrides in one place) [tree 9600c4e8a386] (2026-10-31T01:56:57Z)
## Log
- 2026-10-31T00:06:08Z created
- 2026-10-31T01:38:20Z planned from capture
- 2026-10-31T01:38:21Z set approved=True
- 2026-10-31T01:38:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2238.builder.md
- 2026-10-31T01:39:13Z focused
- 2026-10-31T01:55:43Z merged worktree-agent-aca16939251dadca2 (5 file(s))
- 2026-10-31T01:55:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aca16939251dadca2
- 2026-10-31T01:55:44Z focused
- 2026-10-31T01:56:56Z scope: plugin/lib/fmfind.py (_git, hotspots, cmd_find), plugin/lib/fmcli.py (--hotspots flag), plugin/tests/test_find.py, MASTER.md, CHANGELOG.md
- 2026-10-31T01:57:31Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2185 [FEATURE L, planned, 7 steps] Initiative detection ladder (steer 2026-10-30 #4, capability #1): fm find stays the free…
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
- the similar finished task took 5 steps
## Lessons
- Every git read on an untrusted repo needs the full set of config overrides that can execute: fsmonitor, hooks, gpg programs and signature display, not just the first two
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmfind.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
