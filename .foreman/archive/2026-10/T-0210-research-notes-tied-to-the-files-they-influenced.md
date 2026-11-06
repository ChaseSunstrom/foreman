---
id: T-0210
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-04T04:10:53Z
updated: 2026-10-04T04:57:16Z
base: fefe3c73e0ea371643e5f29591860bb69360b9e0
base_tree: 2f3d43629f3ed31ac7b9ac337b7b7328dea972d8
verified: strong
---
# Research notes that cite repo files are marked stale in recall once those files change after the note
## Raw request
> Research notes tied to the files they influenced: flag a note stale when those files change
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a recalled research note whose cited file changed after it was written is labelled stale with that file; an untouched one isn't — verify with `python3 plugin/tests/run.py -k test_recall`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test first, then cited paths + git check in fmrecall.recall
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_recall` → exit 0 · Ran 12 tests in 7.7s (4 classes, 16 at a time; slowest: Recall 8s, RedGreen 1s, Memory 1s) / OK [ran] [tree b0c22b6f0608] (2026-10-04T04:55:45Z)
- `python3 plugin/tests/run.py -k test_recall` → ✗ exit 1 · Ran 12 tests in 7.7s (4 classes, 16 at a time; slowest: Recall 8s, RedGreen 1s, Memory 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b0c22b6f0608] (2026-10-04T04:56:01Z)
- `python3 plugin/tests/run.py -k test_recall` → exit 0 · Ran 12 tests in 7.7s (4 classes, 16 at a time; slowest: Recall 8s, RedGreen 1s, Memory 1s) / OK [ran] [tree b0c22b6f0608] (2026-10-04T04:56:01Z)
- (ac 1) `python3 plugin/tests/run.py -k test_recall` → exit 0 · Ran 12 tests in 7.6s (4 classes, 16 at a time; slowest: Recall 8s, RedGreen 1s, Memory 1s) / OK [ran] [tree b0c22b6f0608] (2026-10-04T04:57:16Z)
- (audit self) `self checklist: only files that exist in the repo count as cited (≤ 12 per note); one git log per research hit shown (≤ 4), 10 s timeout, errors mean not stale; recall stays ~0.1 s on this project` → pass [tree b0c22b6f0608] (2026-10-04T04:57:16Z)
## Log
- 2026-10-04T04:10:53Z created
- 2026-10-04T04:54:24Z planned from capture
- 2026-10-04T04:54:25Z focused
- 2026-10-04T04:57:16Z done
- 2026-10-04T04:57:16Z committed 64b3600 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- research T-0206-review: Verdict: changes needed.** There is one MEDIUM robustness bug and two LOWs. I found no HIGH SSRF hole. I traced this by reading the code and did …
- research brainstorm-20260926-super3-slate: Build: G1 evidence that proves nothing (0 tests ran / no tests collected) is recorded as a failure · G2 pre-audit flags test t…
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
## Files touched
- plugin/tests/test_recall.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
