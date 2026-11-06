---
id: T-1428
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlib.py, plugin/tests/test_library.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T20:29:52Z
updated: 2026-10-22T15:35:47Z
base: ff0d502d92927b2865a8e0ce62cc443708dc5018
base_tree: d9f8abdd5acfab2fbf07b90011a4ec30110d2d82
plan0_at: 2026-10-22T15:30:56Z
plan0_scope: [plugin/lib/fmlib.py, plugin/tests/test_library.py, CHANGELOG.md]
verified: strong
---
# fm lib source: one swap at a time, and rm clears stray folders
## Raw request
> fm lib: two fm lib source update runs of the same name at once can interfere with each other's renames (no lock); and fm lib source rm only takes [a-z0-9-]+ names, so a stray dot or .old- folder can't be removed through fm (T-1412 builder)
## Interpretation
source_add's replace swaps final→final.old-PID and tmp→final with no lock, so two updates of one source can interleave their renames (fmlib.py ~597-606); fm lib source rm takes only [a-z0-9-]+ so a stray .tmp-NAME-PID or NAME.old-PID folder (left by a crash) can't be removed through fm.
## Assumptions (confidence)
## Acceptance criteria
- [x] an update waits for a held swap lock instead of interleaving; rm removes a stray .old-/.tmp- folder and still refuses ../ or a path — verify with `cd plugin/tests && python3 -m unittest test_library.LibSources.test_source_swap_is_locked_and_rm_clears_strays`
## Non-goals
## Approach (options → choice → why)
Take fmcore.lock on the sources folder around the swap only (the clone stays outside it, so a slow network doesn't block others). rm: accept [a-z0-9.-]+ names that aren't . or .., resolve to a direct child folder of the sources dir, and say what was removed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] lock the swap, widen rm safely
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_source_swap_is_locked_and_rm_clears_strays` → ✗ exit 1 · Ran 1 test in 0.458s / FAILED (failures=1) [ran] [tree f82df9def6d4] (2026-10-22T15:31:00Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_source_swap_is_locked_and_rm_clears_strays` → exit 0 · Ran 1 test in 3.002s / OK [ran] [tree 24fc6b94c791] (2026-10-22T15:31:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_source_swap_is_locked_and_rm_clears_strays` → exit 0 · Ran 1 test in 2.853s / OK [ran] [tree 720879fd3016] (2026-10-22T15:33:15Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.LibSources.test_source_swap_is_locked_and_rm_clears_strays` → exit 0 · Ran 1 test in 2.961s / OK [ran] [tree b04b93387f98] (2026-10-22T15:33:20Z)
- (audit adversary) `self: c.lock on state/locks/lib-sources around the two renames only (the clone stays outside, so a slow network blocks nobody); rm accepts [a-z0-9.-]+ minus . and .., must be a real folder directly in the sources dir, not a link. Test holds the lock 1.5 s and sees the update wait, removes both stray shapes, refuses ., .., ../x, kit/../..; test_library, test_lib_source_kill, test_lib_hostile green.` → rm can't leave the sources folder: no slash allowed, . and .. refused, links refused [tree b04b93387f98] (2026-10-22T15:33:20Z)
- (audit edge) `self: c.lock on state/locks/lib-sources around the two renames only (the clone stays outside, so a slow network blocks nobody); rm accepts [a-z0-9.-]+ minus . and .., must be a real folder directly in the sources dir, not a link. Test holds the lock 1.5 s and sees the update wait, removes both stray shapes, refuses ., .., ../x, kit/../..; test_library, test_lib_source_kill, test_lib_hostile green.` → a held lock past 5 s raises LockTimeout before any rename, so the source stays as it was [tree b04b93387f98] (2026-10-22T15:33:20Z)
- (audit self) `self: c.lock on state/locks/lib-sources around the two renames only (the clone stays outside, so a slow network blocks nobody); rm accepts [a-z0-9.-]+ minus . and .., must be a real folder directly in the sources dir, not a link. Test holds the lock 1.5 s and sees the update wait, removes both stray shapes, refuses ., .., ../x, kit/../..; test_library, test_lib_source_kill, test_lib_hostile green.` → no findings [tree b04b93387f98] (2026-10-22T15:33:20Z)
## Log
- 2026-10-21T20:29:52Z created
- 2026-10-22T15:03:02Z planned from capture
- 2026-10-22T15:30:55Z focused
- 2026-10-22T15:35:45Z done
- 2026-10-22T15:35:47Z committed e6be6b88 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1412 [FIX M, done, 2 steps] fm lib source add or update killed at any step leaves the previous index intact and recoverable — lesson: A two-rename swap needs a recover…
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- research T-1396-review: Verdict: changes needed.** I found two crashes on a malformed marketplace, one way the trust ledger can be laundered, and some bypasses and false…
- decision 2026-10-20: Foreman Code's TUI (T-1283) is a stdlib curses client of fm code's --json event stream with a widget layer that themes and extensions build on; exte…
- similar past tasks were M: consider --tier M
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmlib.py, plugin/tests/test_library.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmlib.py
- CHANGELOG.md
