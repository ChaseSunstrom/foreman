---
id: T-1598
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/tests/fixtures/guard_evasions.jsonl, plugin/tests/fixtures/guard_gaps.jsonl, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T20:19:06Z
updated: 2026-10-22T20:22:20Z
base: cf3af3586f58f8acb60afa8b9d6bc05f745c5f41
base_tree: 3ad67d061b068f14d1f057bbb011101e1be336df
plan0_at: 2026-10-22T20:19:48Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard false block: git checkout -b NAME and git switch -c NAME are refused as tree writes
## Raw request
> Guard false block: git checkout -b NAME and git switch -c NAME are refused as tree writes (core in Foreman's checkout; home folder, /tmp) though they change no files; git stash push and pull --ff-only do rewrite files and stay refused
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] git checkout -b NAME and git switch -c/--create NAME with no start point pass in Foreman's checkout; with a start point they stay refused — verify with `cd plugin/tests && python3 -m unittest test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] a new branch at HEAD writes no files
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.PluginChanges` → red as expected (exit 1) · Ran 12 tests in 0.260s / FAILED (failures=4) [ran] [tree 72ff72deaac8] (2026-10-22T20:20:04Z)
- `cd plugin/tests && python3 -m unittest test_guard.PluginChanges` → ✗ exit 1 · Ran 12 tests in 0.256s / FAILED (failures=4) (start tree + this task's tests) [ran] [tree 090d4a735676] (2026-10-22T20:21:59Z)
- `cd plugin/tests && python3 -m unittest test_guard.PluginChanges` → exit 0 · Ran 12 tests in 0.253s / OK [ran] [tree 090d4a735676] (2026-10-22T20:21:59Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard test_guard_evasions test_guard_cases` → exit 0 · Ran 146 tests in 5.375s / OK [ran] [tree 090d4a735676] (2026-10-22T20:22:05Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard` → exit 0 · Ran 131 tests in 2.523s / OK [ran] [tree 090d4a735676] (2026-10-22T20:22:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard` → exit 0 · Ran 131 tests in 2.497s / OK [ran] [tree 5e3385be1fb3] (2026-10-22T20:22:11Z)
- (audit adversary) `self: intent: new branches at HEAD pass · adversary: a start point, a pathspec, -B/-C, extra options and git -c core.hooksPath / GIT_CONFIG_PARAMETERS still refuse; a branch name starting with - isn't exempt · edge: obfuscated forms (g''it, \git, $'git', C=git, arrays) follow the same rule; the evasion corpus regenerated (5 gaps moved to the corpus) · operator: no install change · maintainer: PluginChanges red first; 162 guard tests pass; 5,000 real commands unchanged` → git -c core.hooksPath=/tmp/h checkout -b x → system; GIT_CONFIG_PARAMETERS form → system; checkout -b x origin/main → core; checkout -B → core [tree 5e3385be1fb3] (2026-10-22T20:22:11Z)
- (audit self) `self: intent: new branches at HEAD pass · adversary: a start point, a pathspec, -B/-C, extra options and git -c core.hooksPath / GIT_CONFIG_PARAMETERS still refuse; a branch name starting with - isn't exempt · edge: obfuscated forms (g''it, \git, $'git', C=git, arrays) follow the same rule; the evasion corpus regenerated (5 gaps moved to the corpus) · operator: no install change · maintainer: PluginChanges red first; 162 guard tests pass; 5,000 real commands unchanged` → no findings [tree 5e3385be1fb3] (2026-10-22T20:22:11Z)
## Log
- 2026-10-22T20:19:06Z created
- 2026-10-22T20:19:47Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md']
- 2026-10-22T20:19:47Z focused
- 2026-10-22T20:20:51Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/tests/fixtures/guard_evasions.jsonl', 'plugin/tests/fixtures/guard_gaps.jsonl', 'CHANGELOG.md']
- 2026-10-22T20:22:19Z done
- 2026-10-22T20:22:20Z committed 7982d368 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- T-0859 [FIX S, done, 1 steps] Guard: a bare git init in a folder that's already a repo isn't a tree write over core (3 f
- research T-1263-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** approve with nits. I could only read files here, so I did…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 1–6 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Why not caught
checkout and switch were classed as tree writes whatever their arguments
## Lessons
- Branch creation is a ref change, not a tree write: classify git subcommands by what they do with these exact arguments, not by name
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/fixtures/guard_evasions.jsonl
- plugin/tests/fixtures/guard_gaps.jsonl
- CHANGELOG.md
