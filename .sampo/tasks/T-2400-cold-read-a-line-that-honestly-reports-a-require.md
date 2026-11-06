---
id: T-2400
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:06:19Z
updated: 2026-10-31T14:21:32Z
base: db1c051d2f0b2fe4a2cf1f7d5712d3076fb40b4d
base_tree: afd942523155d6ef3a56e9b92c3c7b6a4697ef27
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-10-31T14:06:20Z
plan0_scope: []
verified: strong
---
# Cold read: a line that honestly reports a requirement as unmet doesn't break it; fail what a line claims or hides
## Raw request
> Cold read: a line that honestly reports a requirement as unmet doesn't break it; fail what a line claims or hides
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] READ_CHILD says an honest gap report breaks nothing, and a false completion claim still blocks — verify with `python3 plugin/tests/run.py test_genesis -k honest_gap`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test (the prompt line; a stubbed FAIL on a claimed-done line with a grounded BREAKS still blocks), then the READ_CHILD line
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 163 tests in 9.4s (17 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 7s, GenesisLive 6s) / OK [ran] [tree 2ee7623c03cc] (2026-10-31T14:07:06Z)
- `python3 plugin/tests/run.py test_genesis -k honest_gap` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: GenesisRead 0s) / FAILED (1 classes: test_genesis.GenesisRead) (start tree + this task's tests) [ran] [tree 2ee7623c03cc] (2026-10-31T14:07:08Z)
- `python3 plugin/tests/run.py test_genesis -k honest_gap` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GenesisRead 0s) / OK [ran] [tree 2ee7623c03cc] (2026-10-31T14:07:08Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis -k honest_gap` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GenesisRead 0s) / OK [ran] [tree 0ed24519fdbd] (2026-10-31T14:07:09Z)
- (audit adversary) `self-review: one READ_CHILD sentence scoping MUST checks to what a line claims, hides or plans, matching seed rule 7's text; a grounded FAIL still blocks (tested); recorded with fm decide --kind costly for the user's review in the final report; the read key changes, so tower files re-read once` → false completion claims and gaming still fail (the prompt keeps them; a grounded FAIL blocks, tested) [tree 0ed24519fdbd] (2026-10-31T14:07:09Z)
- (audit self) `self-review: one READ_CHILD sentence scoping MUST checks to what a line claims, hides or plans, matching seed rule 7's text; a grounded FAIL still blocks (tested); recorded with fm decide --kind costly for the user's review in the final report; the read key changes, so tower files re-read once` → no findings [tree 0ed24519fdbd] (2026-10-31T14:07:09Z)
## Log
- 2026-10-31T14:06:19Z created
- 2026-10-31T14:06:20Z focused
- 2026-10-31T14:06:20Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-10-31T14:07:08Z scope: plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-10-31T14:07:33Z done
- 2026-10-31T14:07:35Z committed d4a33b4f (4 files)
- 2026-10-31T14:14:30Z guard authorization added: publish
- 2026-10-31T14:21:32Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: [costly] Cold read clarification: a line that reports a requirement as unmet, open or unproven doesn't break it; the reader fails only what a line c…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2206 [FIX M, dropped, 2 steps] fm genesis put's cold read sees what earlier failed reads of the same file named, so it checks those were met instead of re-litigating t…
- T-2246 [FEATURE M, done, 2 steps] A cold-read FAIL blocks only when it quotes, verbatim, the gen-0 line, steer or standing-intent clause it breaks; an ungrounded one is …
## Lessons
- A grounded citation can still be misapplied: say what breaking a rule looks like, not only which rules count
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
