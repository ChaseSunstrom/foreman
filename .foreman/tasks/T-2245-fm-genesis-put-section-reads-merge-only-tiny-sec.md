---
id: T-2245
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T00:46:37Z
updated: 2026-10-31T00:56:47Z
base: 5eef1336d9300ad143ac58b83ddc4d1563c872f6
base_tree: 5f7018374dd7bcf15375842bfa198251669837aa
plan0_at: 2026-10-31T00:46:38Z
plan0_scope: []
verified: strong
---
# fm genesis put: section reads merge only tiny sections, by characters, so a critique of paragraph sections gets one read per section (T-2243 merged nine into one: paragraphs count as one logical line since T-2231)
## Raw request
> fm genesis put: section reads merge only tiny sections, by characters, so a critique of paragraph sections gets one read per section (T-2243 merged nine into one: paragraphs count as one logical line since T-2231)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a file whose sections are each one long paragraph is read one section at a time; sections under 300 characters still share a read, and a group never chains past 1500 characters — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_paragraph_sections_each_get_a_read_and_only_tiny_ones_merge`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then _groups merges by characters
## Resume here
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_paragraph_sections_each_get_a_read_and_only_tiny_ones_merge` → red as expected (exit 1) · Ran 1 test in 0.134s / FAILED (failures=1) [ran] [tree 199a2466883e] (2026-10-31T00:47:05Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_paragraph_sections_each_get_a_read_and_only_tiny_ones_merge` → ✗ exit 1 · Ran 1 test in 0.264s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree b10238a9d5ba] (2026-10-31T00:48:39Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_paragraph_sections_each_get_a_read_and_only_tiny_ones_merge` → exit 0 · Ran 1 test in 0.257s / OK [ran] [tree b10238a9d5ba] (2026-10-31T00:48:39Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_paragraph_sections_each_get_a_read_and_only_tiny_ones_merge` → exit 0 · Ran 1 test in 0.255s / OK [ran] [tree b10238a9d5ba] (2026-10-31T00:48:39Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_paragraph_sections_each_get_a_read_and_only_tiny_ones_merge` → exit 0 · Ran 1 test in 0.260s / OK [ran] [tree c6c53d658ae8] (2026-10-31T00:48:40Z)
- (audit edge) `self: diff read twice; merging now needs a tiny section and a bounded group, so no chain can swallow the file; the 12-read cap still bounds cost; test_genesis green` → a critique of paragraph sections gets one read per section; tiny sections join the read before them up to 1500 characters; a file of bullets still splits on the logical-line floor [tree c6c53d658ae8] (2026-10-31T00:48:40Z)
- (audit self) `self: diff read twice; merging now needs a tiny section and a bounded group, so no chain can swallow the file; the 12-read cap still bounds cost; test_genesis green` → no findings [tree c6c53d658ae8] (2026-10-31T00:48:40Z)
## Log
- 2026-10-31T00:46:37Z created
- 2026-10-31T00:46:37Z focused
- 2026-10-31T00:49:03Z done
- 2026-10-31T00:49:05Z committed 0b67a815 (4 files)
- 2026-10-31T00:53:59Z guard authorization added: publish
- 2026-10-31T00:56:47Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2231 [FIX S, done, 1 steps] fm genesis put: a wrapped paragraph is one logical line, so a cold reader's quote across its line break names it (critique puts read such q…
- T-2243 [FEATURE M, done, 3 steps] fm genesis put: judge a long narrative tower file section by section (one cold read per… — lesson: Splitting a check into parts must ke…
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- decision 2026-10-30: T-2166: 'exam entry' in steer 2 means spec.md; exam.jsonl grade lines stay exempt
- similar finished tasks took 1–3 steps
## Lessons
- Two changes that each count 'lines' differently compose badly: T-2231 made a paragraph one line, and T-2243's size rules silently treated every paragraph section as short
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
