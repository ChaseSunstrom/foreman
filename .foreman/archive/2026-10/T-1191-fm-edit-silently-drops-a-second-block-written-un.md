---
id: T-1191
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmedit.py, plugin/tests/test_batch_edit.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T13:00:40Z
updated: 2026-10-16T13:06:42Z
base: 84cc2ff72f020e52cfa66d8bb68218b98bd2a29d
base_tree: 2075782874fea57c16172f9d95ee9d218d89e92a
plan0_at: 2026-10-16T13:03:54Z
plan0_scope: [plugin/lib/fmedit.py, plugin/tests/test_batch_edit.py, CHANGELOG.md]
verified: strong
---
# Fm edit silently drops a second <<< === >>> block written under the same @@ file header (o
## Raw request
> fm edit silently drops a second <<< === >>> block written under the same @@ file header (only blocks with their own @@ line parse; the count check compares @@ headers, not <<< blocks): apply every block under the last @@ header, or refuse naming the dropped block
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two <<< === >>> blocks under one @@ header both apply; a lone <<< block with no @@ before it is refused; a typo'd block is still refused, never skipped — verify with `python3 plugin/tests/run.py test_batch_edit`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in test_batch_edit
2. [x] parse_spec: blocks after a header belong to it; count <<< lines
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_batch_edit` → ✗ exit 1 · Ran 24 tests in 16.3s (4 classes, 16 at a time; slowest: BatchEdit 16s, Sub 4s, Hint 3s) / FAILED (1 classes) [ran] [tree ce6ec489ab94] (2026-10-16T13:04:21Z)
- (step 2) `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 24 tests in 14.0s (4 classes, 16 at a time; slowest: BatchEdit 14s, Sub 4s, Hint 3s) / OK [ran] [tree cca060646585] (2026-10-16T13:04:46Z)
- `python3 plugin/tests/run.py test_batch_edit` → ✗ exit 1 · Ran 24 tests in 22.6s (4 classes, 16 at a time; slowest: BatchEdit 22s, Sub 2s, Hint 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 58dd966dc419] (2026-10-16T13:05:38Z)
- `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 24 tests in 22.2s (4 classes, 16 at a time; slowest: BatchEdit 22s, Sub 6s, Hint 5s) / OK [ran] [tree 58dd966dc419] (2026-10-16T13:05:38Z)
- (ac 1) `python3 plugin/tests/run.py test_batch_edit` → exit 0 · Ran 24 tests in 10.2s (4 classes, 16 at a time; slowest: BatchEdit 10s, Sub 2s, Hint 2s) / OK [ran] [tree 58dd966dc419] (2026-10-16T13:05:49Z)
- (audit edge) `self: blocks after a header belong to it until the next header; a block before any header is refused; completeness counted by <<< lines, so a typo'd block anywhere refuses the whole batch instead of being skipped` → an old text holding a line that is exactly <<< miscounts and refuses (the message points at the JSON form) [tree 58dd966dc419] (2026-10-16T13:05:49Z)
- (audit self) `self: blocks after a header belong to it until the next header; a block before any header is refused; completeness counted by <<< lines, so a typo'd block anywhere refuses the whole batch instead of being skipped` → no findings [tree 58dd966dc419] (2026-10-16T13:05:49Z)
## Log
- 2026-10-16T13:00:40Z created
- 2026-10-16T13:03:52Z set scope=['plugin/lib/fmedit.py', 'plugin/tests/test_batch_edit.py', 'CHANGELOG.md']
- 2026-10-16T13:03:53Z focused
- 2026-10-16T13:06:41Z done
- 2026-10-16T13:06:42Z committed 2937170e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1089-review: Verdict: changes needed.** I found no guard bypass. I could not run anything, because this audit is read-only, so everything below is from readin…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–6 steps
## Plan gaps
- failed first: step 1 Failing tests in test_batch_edit
## Files touched
- plugin/tests/test_batch_edit.py
- plugin/lib/fmedit.py
- CHANGELOG.md
