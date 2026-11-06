---
id: T-2250
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T01:26:07Z
updated: 2026-10-31T01:53:08Z
base: 3e8600d521e6132a8c2d3e1f664fa785e89634c6
base_tree: dca330ddd55533f6687c1c17f76c7f78b2041f2e
plan0_at: 2026-10-31T01:39:19Z
plan0_scope: []
verified: strong
---
# fm find --capture keys twin leads in scan order like rank and fm prove
## Raw request
> fmfind.capture keys twin leads in ranked order while rank and fm prove key them in scan order (file, line, finder), so a twin pair can get different keys from fm find --capture than from fm prove
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two identical leads in one file get the same keys from fm find --capture, fm find --rank and fm prove whatever their rank order, so a capture's dedupe and a proof's lift name the same lead — verify with `cd plugin/tests && python3 -m unittest -q test_find`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: twin leads in a long and a short function, keys from capture equal rank's and prove's; capture keys over (file, line, finder) order
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find 2>&1 | tail -15` → exit 0 · Ran 53 tests in 26.599s / OK [ran] [tree 26f4512c09eb] (2026-10-31T01:40:15Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find 2>&1 | tail -15` → exit 0 · Ran 53 tests in 26.599s / OK [ran] [tree 26f4512c09eb] (2026-10-31T01:40:15Z)
- `cd plugin/tests && python3 -m unittest -q test_find` → ✗ exit 1 · Ran 53 tests in 24.317s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree a440cfa7a3f9] (2026-10-31T01:51:32Z)
- `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 53 tests in 24.429s / OK [ran] [tree a440cfa7a3f9] (2026-10-31T01:51:32Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 53 tests in 25.444s / OK [ran] [tree 16aeb17995f0] (2026-10-31T01:52:07Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 53 tests in 24.521s / OK [ran] [tree 16aeb17995f0] (2026-10-31T01:52:33Z)
- (audit edge) `self: keyed numbers twins in (file, line, finder) order and returns pairs in the given order, so capture still files best-ranked first while keys match rank and prove; prove's own sort dropped; ties keep input order (stable sort); test_find 53 green, red-to-green proven` → twin leads reordered by effort keep their scan-order keys; identical twins tie and keep scan order [tree 16aeb17995f0] (2026-10-31T01:52:33Z)
- (audit self) `self: keyed numbers twins in (file, line, finder) order and returns pairs in the given order, so capture still files best-ranked first while keys match rank and prove; prove's own sort dropped; ties keep input order (stable sort); test_find 53 green, red-to-green proven` → no findings [tree 16aeb17995f0] (2026-10-31T01:52:33Z)
## Log
- 2026-10-31T01:26:07Z created
- 2026-10-31T01:38:31Z planned from capture
- 2026-10-31T01:38:31Z set approved=True
- 2026-10-31T01:38:57Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2250.builder.md
- 2026-10-31T01:39:19Z focused
- 2026-10-31T01:50:41Z merged worktree-agent-afe50efd998036b2c (3 file(s))
- 2026-10-31T01:50:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afe50efd998036b2c
- 2026-10-31T01:50:41Z focused
- 2026-10-31T01:52:07Z scope: plugin/lib/fmfind.py (keyed), plugin/lib/fmprove.py, plugin/tests/test_find.py, CHANGELOG.md
- 2026-10-31T01:53:05Z done
- 2026-10-31T01:53:08Z committed 71c3ca59 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2125-review: Verdict:** approve with nits. I found no HIGH issues. There are three MEDIUM design gaps worth fixing or capturing, plus some LOW nits. I did not…
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- research T-2127-review: Approve with nits. Changes needed only if the poll cost is a concern (finding 1). I ran no tests, so the acceptance criterion is checked by readi…
- decision 2026-10-31: [cites: T-2132 review (edge MEDIUM)] fm find --rank's proof lift is up to 1.25x, capped at 0.98x the lowest unproven score of any more severe kind i…
## Lessons
- Numbering that depends on iteration order must fix its own order inside the helper, not trust each caller to sort
## Files touched
- plugin/lib/fmfind.py
- plugin/lib/fmprove.py
- plugin/tests/test_find.py
- CHANGELOG.md
