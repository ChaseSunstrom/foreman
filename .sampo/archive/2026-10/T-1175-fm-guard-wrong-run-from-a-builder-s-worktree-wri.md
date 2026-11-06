---
id: T-1175
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmreplay.py, plugin/tests/test_guard_cases.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T12:12:00Z
updated: 2026-10-16T12:29:30Z
base: ecd0600fe542fd014dd1a4a80d9e885d334f7b79
base_tree: 94d0490e9d5e2a4ddbad8446d15e20d8389ae5be
plan0_at: 2026-10-16T12:21:20Z
plan0_scope: [plugin/lib/fmreplay.py, plugin/tests/test_guard_cases.py, CHANGELOG.md]
verified: strong
---
# Fm guard wrong run from a builder's worktree writes into the main checkout's corpus (PLUGI
## Raw request
> fm guard wrong run from a builder's worktree writes into the main checkout's corpus (PLUGIN_ROOT's plugin/tests/fixtures), dirtying the main tree mid-gates and storing worktree-relative cwds: write to the corpus of the cwd's own Foreman checkout (git root holding plugin/tests/fixtures), never another checkout's
## Interpretation
fm guard wrong stores a case in the corpus of the Foreman checkout the command runs in: run inside a builder's worktree, the case lands in that worktree's plugin/tests/fixtures/guard_cases.jsonl with a cwd relative to that worktree's root; outside any Foreman checkout, in PLUGIN_ROOT's repo as now.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm guard wrong run inside a second Foreman checkout writes that checkout's corpus with a cwd relative to its root and leaves PLUGIN_ROOT's corpus untouched — verify with `python3 plugin/tests/run.py test_guard_cases`
## Non-goals
## Approach (options → choice → why)
Options: (a) repo_root()/cases_path() take the cwd and walk up to the nearest git root holding plugin/lib/fmreplay.py and plugin/tests/fixtures, falling back to PLUGIN_ROOT's repo; (b) refuse fm guard wrong outside PLUGIN_ROOT's repo (blocks builders from adding labels); (c) an explicit --corpus flag (easy to forget). Choice: (a); FOREMAN_GUARD_CASES still overrides for tests.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a second checkout (copied fixture tree) gets the case; the main corpus unchanged
2. [x] checkout-aware repo_root/cases_path in fmreplay
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_cases` → ✗ exit 1 · Ran 10 tests in 4.6s (1 classes, 16 at a time; slowest: GuardCases 4s) / FAILED (1 classes) [ran] [tree 411607baa8aa] (2026-10-16T12:21:42Z)
- (step 2) `python3 plugin/tests/run.py test_guard_cases` → ✗ exit 1 · Ran 10 tests in 4.5s (1 classes, 16 at a time; slowest: GuardCases 4s) / FAILED (1 classes) [ran] [tree 0fb4da600694] (2026-10-16T12:21:54Z)
- (step 2) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 10 tests in 9.3s (1 classes, 16 at a time; slowest: GuardCases 9s) / OK [ran] [tree 2d9840fad264] (2026-10-16T12:22:51Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases test_replay test_night` → exit 0 · Ran 38 tests in 3.4s (12 classes, 16 at a time; slowest: Night 3s, Replay 3s, NightGuards 2s) / OK [ran] [tree 75e691ee0964] (2026-10-16T12:27:36Z)
- `python3 plugin/tests/run.py test_guard_cases` → ✗ exit 1 · Ran 10 tests in 4.9s (1 classes, 16 at a time; slowest: GuardCases 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 98ebaabdad68] (2026-10-16T12:27:53Z)
- `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 10 tests in 4.0s (1 classes, 16 at a time; slowest: GuardCases 4s) / OK [ran] [tree 98ebaabdad68] (2026-10-16T12:27:53Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 10 tests in 4.0s (1 classes, 16 at a time; slowest: GuardCases 4s) / OK [ran] [tree 98ebaabdad68] (2026-10-16T12:27:57Z)
- (audit adversary) `self: reviewed merged diff: cases_path and the cwd helpers follow the checkout cwd is in (marker plugin/lib/fmguard.py), falling back to PLUGIN_ROOT; repo_root stays PLUGIN_ROOT's for the night job's own-repo check; FOREMAN_GUARD_CASES still overrides` → labels still only reach tests; a lane can no longer dirty the main checkout's corpus [tree 98ebaabdad68] (2026-10-16T12:27:57Z)
- (audit edge) `self: reviewed merged diff: cases_path and the cwd helpers follow the checkout cwd is in (marker plugin/lib/fmguard.py), falling back to PLUGIN_ROOT; repo_root stays PLUGIN_ROOT's for the night job's own-repo check; FOREMAN_GUARD_CASES still overrides` → outside any checkout the case goes to PLUGIN_ROOT's corpus as before [tree 98ebaabdad68] (2026-10-16T12:27:57Z)
- (audit self) `self: reviewed merged diff: cases_path and the cwd helpers follow the checkout cwd is in (marker plugin/lib/fmguard.py), falling back to PLUGIN_ROOT; repo_root stays PLUGIN_ROOT's for the night job's own-repo check; FOREMAN_GUARD_CASES still overrides` → no findings [tree 98ebaabdad68] (2026-10-16T12:27:57Z)
- `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 10 tests in 1.8s (1 classes, 16 at a time; slowest: GuardCases 2s) / OK [ran] [tree 98ebaabdad68] (2026-10-16T12:28:52Z)
- (audit adversary) `self: reviewed merged diff: cases_path and the cwd helpers follow the checkout cwd is in (marker plugin/lib/fmguard.py), falling back to PLUGIN_ROOT; repo_root stays PLUGIN_ROOT's for the night job's own-repo check; FOREMAN_GUARD_CASES still overrides` → labels still only reach tests; a lane can no longer dirty the main checkout's corpus [tree 98ebaabdad68] (2026-10-16T12:28:52Z)
- (audit edge) `self: reviewed merged diff: cases_path and the cwd helpers follow the checkout cwd is in (marker plugin/lib/fmguard.py), falling back to PLUGIN_ROOT; repo_root stays PLUGIN_ROOT's for the night job's own-repo check; FOREMAN_GUARD_CASES still overrides` → outside any checkout the case goes to PLUGIN_ROOT's corpus as before [tree 98ebaabdad68] (2026-10-16T12:28:52Z)
- (audit self) `self: reviewed merged diff: cases_path and the cwd helpers follow the checkout cwd is in (marker plugin/lib/fmguard.py), falling back to PLUGIN_ROOT; repo_root stays PLUGIN_ROOT's for the night job's own-repo check; FOREMAN_GUARD_CASES still overrides` → no findings [tree 98ebaabdad68] (2026-10-16T12:28:52Z)
## Log
- 2026-10-16T12:12:00Z created
- 2026-10-16T12:12:36Z set scope=['plugin/lib/fmreplay.py', 'plugin/tests/test_guard_cases.py', 'CHANGELOG.md'], status=planned
- 2026-10-16T12:15:07Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1175.builder.md
- 2026-10-16T12:21:19Z focused
- 2026-10-16T12:27:28Z merged worktree-agent-a66bd9eb1230c36de (2 file(s))
- 2026-10-16T12:27:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a66bd9eb1230c36de
- 2026-10-16T12:27:31Z focused
- 2026-10-16T12:28:50Z scope: guard_cases.jsonl was written and reverted by the builder's red run (before the fix, fm guard wrong wrote PLUGIN_ROOT's corpus); the file is unchanged against HEAD
- 2026-10-16T12:29:29Z done
- 2026-10-16T12:29:30Z committed 8a2f90ed (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1125 [FIX S, done, 1 steps] Guard false positive: a command 'cd ROOT && python3 heredoc writing CHANGELOG.md (relative — lesson: Before calling a guard block a false p…
- T-1162 [FEATURE M, done, 2 steps] Add `fm guard wrong "<cmd>" --should allow|block` to store a labelled case that `fm replay — lesson: a guard verdict can depend on wher…
- research T-0296-review-1: Verdict:** approve with nits. I found no HIGH findings. I read the diff and `fmcore`'s `find_project`/`routing` but did not run any tests. [sta…
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–2 steps
- likely tests for the scope: plugin/tests/test_replay.py
## Plan gaps
- failed first: step 1 Failing test: a second checkout (copied fixture tree) gets the case; the main corpus unchanged
- failed first: step 2 checkout-aware repo_root/cases_path in fmreplay
## Files touched
- plugin/tests/test_guard_cases.py
- plugin/tests/fixtures/guard_cases.jsonl
- plugin/lib/fmreplay.py
- CHANGELOG.md
