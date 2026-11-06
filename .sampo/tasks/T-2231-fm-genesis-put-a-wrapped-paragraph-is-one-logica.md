---
id: T-2231
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T23:31:20Z
updated: 2026-10-30T23:46:57Z
base: 27711d6d123663964f4edbb4d2506f57fd85bdc8
base_tree: 02c453b13005e97680718a29c09df227452d4d46
plan0_at: 2026-10-30T23:31:22Z
plan0_scope: []
verified: strong
---
# fm genesis put: a wrapped paragraph is one logical line, so a cold reader's quote across its line break names it (critique puts read such quotes as stray)
## Raw request
> fm genesis put: a wrapped paragraph is one logical line, so a cold reader's quote across its line break names it (critique puts read such quotes as stray)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a FAIL quoting a sentence that spans a plain paragraph's line break names that paragraph; headings, bullets and table rows stay separate lines — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_across_a_wrapped_paragraphs_line_break_names_the_paragraph`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then _logical joins a plain paragraph's unindented continuation lines
## Resume here
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_across_a_wrapped_paragraphs_line_break_names_the_paragraph` → red as expected (exit 1) · Ran 1 test in 0.126s / FAILED (failures=1) [ran] [tree b975d2eee537] (2026-10-30T23:31:32Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_across_a_wrapped_paragraphs_line_break_names_the_paragraph` → ✗ exit 1 · Ran 1 test in 0.177s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree eed450951ab3] (2026-10-30T23:35:07Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_across_a_wrapped_paragraphs_line_break_names_the_paragraph` → exit 0 · Ran 1 test in 0.132s / OK [ran] [tree eed450951ab3] (2026-10-30T23:35:07Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_across_a_wrapped_paragraphs_line_break_names_the_paragraph` → exit 0 · Ran 1 test in 0.134s / OK [ran] [tree eed450951ab3] (2026-10-30T23:35:07Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_quote_across_a_wrapped_paragraphs_line_break_names_the_paragraph` → exit 0 · Ran 1 test in 0.132s / OK [ran] [tree 86491dac5be5] (2026-10-30T23:35:19Z)
- (audit edge) `self: diff read twice; _logical feeds the read, DRIFT and acceptance hashing, so joined paragraphs re-hash once (their acceptance restarts); all 104 genesis tests green` → headings, table rows, fences and blockquotes stay apart; a bullet's lazy unindented continuation joins it as Markdown does; lines inside a fenced block join each other (rare in tower docs, harmless to matching) [tree 86491dac5be5] (2026-10-30T23:35:19Z)
- (audit self) `self: diff read twice; _logical feeds the read, DRIFT and acceptance hashing, so joined paragraphs re-hash once (their acceptance restarts); all 104 genesis tests green` → no findings [tree 86491dac5be5] (2026-10-30T23:35:19Z)
## Log
- 2026-10-30T23:31:20Z created
- 2026-10-30T23:31:21Z focused
- 2026-10-30T23:35:42Z done
- 2026-10-30T23:35:44Z committed 1aba532b (4 files)
- 2026-10-30T23:36:08Z guard authorization added: publish
- 2026-10-30T23:46:57Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2114 [FIX S, done, 2 steps] FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name… — lesson: A seed that paraphrases gen-0 drifts: q…
- T-2228 [FIX S, done, 1 steps] fm genesis put: a cold reader's quote of a line since changed or removed is a resolved finding, not a stray one (puts deadlocked on previou…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: Genesis drift counts a cold-read DRIFT line only when a seed line holds the quote, and writes the seed's line, never the reader's words
- similar finished tasks took 1–5 steps
## Lessons
- Match the reader's unit: a Markdown paragraph is one unit however it wraps, so quotes must be matched per paragraph, not per physical line
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
