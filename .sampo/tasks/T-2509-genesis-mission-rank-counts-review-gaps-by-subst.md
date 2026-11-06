---
id: T-2509
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-01T20:18:07Z
updated: 2026-11-01T21:32:22Z
base: f95fac52bf2e5d3f889e674628914b37352872a1
base_tree: 002b2dd7f539dbe6ac872cb739024125b764b2db
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T21:28:36Z
plan0_scope: []
verified: strong
---
# Genesis mission rank counts review gaps by whole word
## Raw request
> FIX: genesis _mission_rank counts review gaps by substring (review.count(bare)), so a short area name like 'ux' also matches 'flux'; count whole-word matches (re.findall with \b) and pin it with a test (T-2502 review, edge lens)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an area named 'UX' gets no review score from a gap mentioning 'flux'; a gap naming 'UX' scores it — verify with `python3 plugin/tests/run.py test_genesis.GapMapValue`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then count with word boundaries
## Resume here
## Docs impact
none: MASTER's 'review gap naming it' still holds
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GapMapValue.test_a_review_gap_scores_an_area_by_whole_word_only` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GapMapValue 0s) / FAILED (1 classes: test_genesis.GapMapValue) [ran] [tree 5084794adeb4] (2026-11-01T21:28:49Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GapMapValue` → exit 0 · Ran 5 tests in 1.0s (1 classes, 16 at a time; slowest: GapMapValue 1s) / OK [ran] [tree e4cf8f36609e] (2026-11-01T21:29:04Z)
- `python3 plugin/tests/run.py test_genesis.GapMapValue.test_a_review_gap_scores_an_area_by_whole_word_only` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: GapMapValue 0s) / FAILED (1 classes: test_genesis.GapMapValue) (start tree + this task's tests) [ran] [tree e4cf8f36609e] (2026-11-01T21:29:08Z)
- `python3 plugin/tests/run.py test_genesis.GapMapValue.test_a_review_gap_scores_an_area_by_whole_word_only` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: GapMapValue 0s) / OK [ran] [tree e4cf8f36609e] (2026-11-01T21:29:08Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GapMapValue` → exit 0 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: GapMapValue 1s) / OK [ran] [tree e4cf8f36609e] (2026-11-01T21:29:11Z)
- (audit edge) `self-review: the review part of a Mission's value counts whole-word mentions of the area's name, escaped for regex` → 'flux' no longer scores 'UX'; a name with regex characters is escaped; the count per mention is unchanged [tree e4cf8f36609e] (2026-11-01T21:29:11Z)
- (audit self) `self-review: the review part of a Mission's value counts whole-word mentions of the area's name, escaped for regex` → no findings [tree e4cf8f36609e] (2026-11-01T21:29:11Z)
## Log
- 2026-11-01T20:18:07Z created
- 2026-11-01T21:15:54Z planned from capture
- 2026-11-01T21:28:35Z focused
- 2026-11-01T21:28:36Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T21:29:08Z scope: fmgenesis _mission_rank review count, test_genesis GapMapValue test
- 2026-11-01T21:30:03Z done
- 2026-11-01T21:30:07Z committed 9d7437a1 (2 files)
- 2026-11-01T21:32:22Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2159-review: Approve with nits. I read the diff, `coverage.md` and the callers, but ran no commands, so the two verify commands are unrun. [stale: plugin/lib/…
- research T-2093-review: Verdict: changes needed.** One MEDIUM defect lets the not-yet check pass an item that has an empty field. The other findings are LOW. I traced th…
- T-2064 [FIX S, done, 1 steps] test_ship's --check test fails when a commit hash ends in 'add' (substring match on 'add a') — lesson: Asserting a short phrase is absent f…
- decision 2026-10-30: [revisited: coverage must be real] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: python3 plugin/tests…
## Plan gaps
- failed first: step 1 red test, then count with word boundaries
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
