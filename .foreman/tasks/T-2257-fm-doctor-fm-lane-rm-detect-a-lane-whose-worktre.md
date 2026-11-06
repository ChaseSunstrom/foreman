---
id: T-2257
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T03:40:47Z
updated: 2026-10-31T04:03:15Z
base: 0bfa5276d2457a3e8bb58be912e0b5d2e2cb13f3
base_tree: ec7ee2ffcda9a01c2fae6245a8592e03822b7da8
plan0_at: 2026-10-31T03:43:59Z
plan0_scope: []
verified: strong
---
# A lane whose worktree creation was cut off is found and repaired: fm doctor names it and fm lane rm moves it aside
## Raw request
> fm doctor / fm lane rm: detect a lane whose worktree creation was cut off (0-byte branch ref, all-empty files, locked admin dir) and repair it in one step: today fetch fails with 'bad object' and fm lane rm refuses it as uncommitted work
## Interpretation
The last session ended while a builder worktree was being created: the branch ref was a 0-byte file and all 2037 files empty. git fetch failed with 'bad object', fm lane rm refused it as uncommitted work, and the repair took a manual move, unlock and prune.
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane with a 0-byte branch ref and an all-empty worktree (an interrupted creation) is reported by fm doctor as corrupt with the fix, and fm lane rm ID --why moves the folder and the ref aside into the project's state (never deleting), unlocks and prunes the worktree entry, and frees the task; git fetch works after — verify with `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor`
## Non-goals
## Approach (options → choice → why)
Options: (1) detect the corrupt shape (0-byte ref, no non-empty file) and repair in lane rm, moving aside into state (chosen: reversible, one command); (2) delete it (destroys evidence); (3) only report in doctor (leaves the manual steps). Choice 1, plus the doctor report.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: a temp repo with a lane, its ref truncated to 0 bytes and its files emptied; fm doctor names it; fm lane rm repairs it; fetch from a local remote works
2. [x] one _ref_state helper (fmlanes.py:103/297/689/863 use rev-parse); doctor check; lane rm repair path
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor 2>&1 | tail -30` → exit 0 · Ran 96 tests in 62.863s / OK [ran] [tree 9f1fa75299bf] (2026-10-31T03:46:45Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor 2>&1 | tail -30` → exit 0 · Ran 96 tests in 62.863s / OK [ran] [tree 9f1fa75299bf] (2026-10-31T03:46:45Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor` → exit 0 · Ran 96 tests in 44.484s / OK [ran] [tree 9f1fa75299bf] (2026-10-31T03:47:33Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_builder test_crash_hygiene test_doctor test_lanes test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [27.79s] [ran] [tree 9f1fa75299bf] (2026-10-31T03:48:34Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|Assertion)"` → exit 0 · Ran 98 tests in 18.260s / OK [ran] [tree 1ac355f2188a] (2026-10-31T03:56:21Z)
- `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor` → ✗ exit 1 · Ran 98 tests in 29.611s / FAILED (failures=1, errors=2) (start tree + this task's tests) [ran] [tree 1ac355f2188a] (2026-10-31T04:01:13Z)
- `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor` → exit 0 · Ran 98 tests in 29.571s / OK [ran] [tree 1ac355f2188a] (2026-10-31T04:01:13Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor` → exit 0 · Ran 98 tests in 18.244s / OK [ran] [tree 84fa7ade3784] (2026-10-31T04:01:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_lanes test_doctor` → exit 0 · Ran 98 tests in 17.088s / OK [ran] [tree 69c342b136af] (2026-10-31T04:02:44Z)
- (audit intent) `self + one fm-reviewer pass; all findings fixed with tests` → doctor names a cut-off lane, lane rm moves folder/ref/admin dir/reflog aside and prunes, fetch works after (test_lanes red-to-green proven) [tree 69c342b136af] (2026-10-31T04:02:44Z)
- (audit edge) `self + one fm-reviewer pass; all findings fixed with tests` → emptied or relative admin gitdir still matches the stale lock; a git failure is an error, never 'missing'; one racing ref can't make doctor PASS [tree 69c342b136af] (2026-10-31T04:02:44Z)
- (audit operator) `self + one fm-reviewer pass; all findings fixed with tests` → nothing is deleted; the wreck dir keeps the old sha recoverable via the copied reflog [tree 69c342b136af] (2026-10-31T04:02:44Z)
## Log
- 2026-10-31T03:40:47Z created
- 2026-10-31T03:42:41Z recon evidence: fmlanes.py:297/103/689/863 rev-parse a 0-byte ref as missing; one _ref_state helper used by fm doctor (fmdoctor.py:1930) and lane rm
- 2026-10-31T03:43:38Z planned from capture
- 2026-10-31T03:43:39Z set approved=True
- 2026-10-31T03:43:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2257.builder.md
- 2026-10-31T03:43:58Z focused
- 2026-10-31T04:00:03Z merged worktree-agent-a2ac1c61758329df0 (4 file(s))
- 2026-10-31T04:00:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2ac1c61758329df0
- 2026-10-31T04:00:03Z focused
- 2026-10-31T04:01:45Z scope: plugin/lib/fmlanes.py, plugin/lib/fmdoctor.py, plugin/tests/test_lanes.py, CHANGELOG.md, MASTER.md
- 2026-10-31T04:03:13Z done
- 2026-10-31T04:03:15Z committed c8e5da75 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2256 [FIX S, done, 1 steps] Recover git after the interrupted T-2072 builder worktree (0-byte branch ref breaks fetch) — lesson: An interrupted worktree creation leave…
- T-1825 [FEATURE M, done, 3 steps] FEATURE: fm run (headless) skips a model call when the tree and the failing check's output — lesson: count list items by line start, no…
- research T-1667-review: Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the t…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
## Why not caught
no test interrupted lane creation midway; test_lanes now builds the truncated ref and empty tree
## Lessons
- Repair paths for a half-written git structure must match by more than one key: the field that names the link is often the one the crash truncated
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmlanes.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
