---
id: T-2228
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T23:13:22Z
updated: 2026-10-30T23:25:34Z
base: d846701fa112b353aba131f1a291b65a0fcfde2b
base_tree: d38a74b0c745996baa597c42083caa273449ad94
plan0_at: 2026-10-30T23:13:23Z
plan0_scope: []
verified: strong
---
# fm genesis put: a cold reader's quote of a line since changed or removed is a resolved finding, not a stray one (puts deadlocked on previous-reads)
## Raw request
> fm genesis put: a cold reader's quote of a line since changed or removed is a resolved finding, not a stray one (puts deadlocked on previous-reads)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a FAIL quoting only a previous read's line the file no longer holds passes; a quote of no line then or now still fails closed — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in GenesisRead, then filter strays against previous-reads lines in fmgenesis._read
## Resume here
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray` → red as expected (exit 1) · Ran 1 test in 0.198s / FAILED (failures=1) [ran] [tree bd6ad822c419] (2026-10-30T23:13:32Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray` → exit 0 · Ran 1 test in 0.264s / OK [ran] [tree 2431c2620527] (2026-10-30T23:14:06Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray` → ✗ exit 1 · Ran 1 test in 0.319s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 2431c2620527] (2026-10-30T23:14:12Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray` → exit 0 · Ran 1 test in 0.257s / OK [ran] [tree 2431c2620527] (2026-10-30T23:14:12Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray test_genesis.GenesisRead.test_a_quote_without_its_backticks_or_cut_with_an_ellipsis_still_names_its_line` → ✗ exit 1 · Ran 2 tests in 0.457s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 9adb7353bde4] (2026-10-30T23:18:21Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray test_genesis.GenesisRead.test_a_quote_without_its_backticks_or_cut_with_an_ellipsis_still_names_its_line` → exit 0 · Ran 2 tests in 0.450s / OK [ran] [tree 9adb7353bde4] (2026-10-30T23:18:21Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray` → exit 0 · Ran 1 test in 0.343s / OK [ran] [tree 9adb7353bde4] (2026-10-30T23:18:22Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray test_genesis.GenesisRead.test_a_quote_without_its_backticks_or_cut_with_an_ellipsis_still_names_its_line` → ✗ exit 1 · Ran 2 tests in 0.455s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 14554bd9c4dc] (2026-10-30T23:21:50Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray test_genesis.GenesisRead.test_a_quote_without_its_backticks_or_cut_with_an_ellipsis_still_names_its_line` → exit 0 · Ran 2 tests in 0.449s / OK [ran] [tree 14554bd9c4dc] (2026-10-30T23:21:50Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray` → exit 0 · Ran 1 test in 0.331s / OK [ran] [tree 14554bd9c4dc] (2026-10-30T23:21:51Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_of_a_line_since_changed_or_removed_is_resolved_not_stray` → exit 0 · Ran 1 test in 0.336s / OK [ran] [tree 14554bd9c4dc] (2026-10-30T23:22:17Z)
- (audit adversary) `fm-reviewer self+adversary, two passes: 2 MEDIUM and 2 LOW found, all fixed test-first (research/T-2228-review.md)` → a trivial edit can't shed a finding (re-keyed to the edited line, 0.96 alike); a quote of gone text is a stray and fails closed [tree 14554bd9c4dc] (2026-10-30T23:22:17Z)
- (audit edge) `fm-reviewer self+adversary, two passes: 2 MEDIUM and 2 LOW found, all fixed test-first (research/T-2228-review.md)` → removed line drops its finding and a pass clears genesis-reads.json; 0.8 cutoff measured against coverage rows (max 0.77 between distinct rows) [tree 14554bd9c4dc] (2026-10-30T23:22:17Z)
- (audit self) `fm-reviewer self+adversary, two passes: 2 MEDIUM and 2 LOW found, all fixed test-first (research/T-2228-review.md)` → no findings [tree 14554bd9c4dc] (2026-10-30T23:22:17Z)
## Log
- 2026-10-30T23:13:22Z created
- 2026-10-30T23:13:22Z focused
- 2026-10-30T23:22:40Z done
- 2026-10-30T23:22:42Z committed 3680d750 (4 files)
- 2026-10-30T23:22:53Z guard authorization added: publish
- 2026-10-30T23:25:34Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2114 [FIX S, done, 2 steps] FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name… — lesson: A seed that paraphrases gen-0 drifts: q…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: Genesis drift counts a cold-read DRIFT line only when a seed line holds the quote, and writes the seed's line, never the reader's words
- similar finished tasks took 2–5 steps
## Lessons
- A cold reader's memory must follow the text it judges: findings keyed on exact lines deadlock once the writer revises them; key by similarity with a cutoff measured on the real file
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
