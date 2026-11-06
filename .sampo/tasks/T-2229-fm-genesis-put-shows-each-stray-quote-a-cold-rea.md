---
id: T-2229
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T23:26:59Z
updated: 2026-10-30T23:32:56Z
base: 3680d750a422acd91004ec92b9b590d2ca6d1480
base_tree: 14554bd9c4dc6925d62eb24db6405442a32f672d
plan0_at: 2026-10-30T23:27:00Z
plan0_scope: []
verified: strong
---
# fm genesis put shows each stray quote: a cold reader's FAIL that names no line prints its own words, so the writer sees what it misquoted
## Raw request
> fm genesis put shows each stray quote: a cold reader's FAIL that names no line prints its own words, so the writer sees what it misquoted
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a stray FAIL quote is printed (plain, cut short) beside its why — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_stray_quote_is_shown_so_the_writer_can_see_what_it_misquoted`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then _named returns the quote and _read prints it for strays
## Resume here
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_stray_quote_is_shown_so_the_writer_can_see_what_it_misquoted` → red as expected (exit 1) · Ran 1 test in 0.134s / FAILED (failures=1) [ran] [tree 7910a1f7f0ef] (2026-10-30T23:27:07Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_stray_quote_is_shown_so_the_writer_can_see_what_it_misquoted` → ✗ exit 1 · Ran 1 test in 0.271s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 3d828346d5ac] (2026-10-30T23:28:20Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_stray_quote_is_shown_so_the_writer_can_see_what_it_misquoted` → exit 0 · Ran 1 test in 0.138s / OK [ran] [tree 3d828346d5ac] (2026-10-30T23:28:20Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_stray_quote_is_shown_so_the_writer_can_see_what_it_misquoted` → exit 0 · Ran 1 test in 0.133s / OK [ran] [tree 3d828346d5ac] (2026-10-30T23:28:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_stray_quote_is_shown_so_the_writer_can_see_what_it_misquoted` → exit 0 · Ran 1 test in 0.135s / OK [ran] [tree 02c453b13005] (2026-10-30T23:28:32Z)
- (audit edge) `self: diff read twice; quotes are c.plain'd and cut to 80 before printing; all three _named unpack sites (FAIL read, stray count, DRIFT hits/stray) updated; whole test_genesis green` → a stray with no WHY now prints too (it was hidden); a quote under 8 characters prints as it was matched [tree 02c453b13005] (2026-10-30T23:28:32Z)
- (audit self) `self: diff read twice; quotes are c.plain'd and cut to 80 before printing; all three _named unpack sites (FAIL read, stray count, DRIFT hits/stray) updated; whole test_genesis green` → no findings [tree 02c453b13005] (2026-10-30T23:28:32Z)
## Log
- 2026-10-30T23:26:59Z created
- 2026-10-30T23:26:59Z focused
- 2026-10-30T23:28:55Z done
- 2026-10-30T23:28:57Z committed 27711d6d (4 files)
- 2026-10-30T23:30:08Z guard authorization added: publish
- 2026-10-30T23:32:56Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2114 [FIX S, done, 2 steps] FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name… — lesson: A seed that paraphrases gen-0 drifts: q…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2228 [FIX S, done, 1 steps] fm genesis put: a cold reader's quote of a line since changed or removed is a resolved finding, not a stray one (puts deadlocked on previou…
- decision 2026-10-30: Genesis drift counts a cold-read DRIFT line only when a seed line holds the quote, and writes the seed's line, never the reader's words
- similar finished tasks took 1–4 steps
## Lessons
- An error that says something was wrong without showing it can't be acted on: show the untrusted text, plain'd and cut, beside the verdict
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
