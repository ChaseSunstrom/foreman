---
id: T-1521
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlib.py, plugin/tests/test_library.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T17:40:41Z
updated: 2026-10-22T17:48:12Z
base: 49d12b665a45082ca1e368dd3c5bc4657323714a
base_tree: 5b3943b1a8d9313397b5bce28bc00108f523023c
plan0_at: 2026-10-22T17:47:20Z
plan0_scope: [plugin/lib/fmlib.py, plugin/tests/test_library.py, CHANGELOG.md]
verified: strong
---
# Fm lib show accepts a card name with its group prefix (web/three-js, frontend/typography):
## Raw request
> fm lib show accepts a card name with its group prefix (web/three-js, frontend/typography): two builders hit 'not found' with the prefixed names briefs use
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib show web/three-js shows the three-js card; a wrong group prefix is still not found — verify with `cd plugin/tests && python3 -m unittest test_library.LibrarySearch.test_show_takes_the_group_prefix`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] resolve group/name to the card in that group
## Resume here
## Docs impact
CHANGELOG.md line
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_library.LibrarySearch.test_show_takes_the_group_prefix` → ✗ exit 1 · Ran 1 test in 0.577s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 3699c4593777] (2026-10-22T17:47:36Z)
- `cd plugin/tests && python3 -m unittest test_library.LibrarySearch.test_show_takes_the_group_prefix` → exit 0 · Ran 1 test in 0.567s / OK [ran] [tree 3699c4593777] (2026-10-22T17:47:36Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.LibrarySearch.test_show_takes_the_group_prefix` → exit 0 · Ran 1 test in 0.596s / OK [ran] [tree 3699c4593777] (2026-10-22T17:47:44Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_library.LibrarySearch` → exit 0 · Ran 4 tests in 1.645s / OK [ran] [tree 3699c4593777] (2026-10-22T17:47:47Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library.LibrarySearch` → exit 0 · Ran 4 tests in 1.652s / OK [ran] [tree 3699c4593777] (2026-10-22T17:47:49Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.LibrarySearch.test_show_takes_the_group_prefix` → exit 0 · Ran 1 test in 0.688s / OK [ran] [tree 8016b4970c97] (2026-10-22T17:47:51Z)
- (audit edge) `self: test-first (red on the start tree, green now); the prefix resolves only when the card really sits in that group folder, so games/three-js stays not found; plain names, plugin:skill names and sections unchanged; LibrarySearch green` → a name with several slashes uses its last segment and the folder before it; a card name containing / can't exist (file names) [tree 8016b4970c97] (2026-10-22T17:47:51Z)
- (audit self) `self: test-first (red on the start tree, green now); the prefix resolves only when the card really sits in that group folder, so games/three-js stays not found; plain names, plugin:skill names and sections unchanged; LibrarySearch green` → no findings [tree 8016b4970c97] (2026-10-22T17:47:51Z)
## Log
- 2026-10-22T17:40:41Z created
- 2026-10-22T17:47:14Z set scope=['plugin/lib/fmlib.py', 'plugin/tests/test_library.py', 'CHANGELOG.md']
- 2026-10-22T17:47:19Z focused
- 2026-10-22T17:47:27Z criterion 1 verify: `cd plugin/tests && python3 -m unittest test_library.Library.test_show_takes_the_group_prefix` → `cd plugin/tests && python3 -m unittest test_library.LibrarySearch.test_show_takes_the_group_prefix`
- 2026-10-22T17:48:10Z done
- 2026-10-22T17:48:12Z committed ab79d5b2 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1036-review: Verdict** — changes needed. Three correctness gaps in the injection path (displaced cards, wildcard deps, files outside the project). The rest is…
- research T-0933-review: Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex…
- research T-1389-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. The three criteria are met, but the quara…
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
## Why not caught
briefs started naming group/name after the cards were grouped
## Lessons
- Accept the names your own briefs generate.
## Files touched
- plugin/tests/test_library.py
- plugin/lib/fmlib.py
- CHANGELOG.md
