---
id: T-3333
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/lib/sampo/sync.py, plugin/tests/test_kalevala.py]
depends_on: [T-3321]
source: followup
created: 2026-11-06T04:32:03Z
updated: 2026-11-06T04:32:03Z
---
# Fleet: Kalevala across machines: towers are claims (tower:<name>), only the holder steps and watches a tower, exam.jsonl and acts merge by line, generation numbers come from a claim
## Raw request
> Fleet: Kalevala across machines: towers are claims (tower:<name>), only the holder steps and watches a tower, exam.jsonl and acts merge by line, generation numbers come from a claim
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] two clones stepping one project against a bare remote run each tower once per round and log each act once; a vanished machine's towers are taken over after its lease lapses; exam.jsonl and the acts log travel and merge by line; keep/revert is computed identically on both from the merged scores — verify with `python3 plugin/tests/run.py test_kalevala`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] two-clone test, red  <- CURRENT
2. [ ] tower claims in step and _decide
3. [ ] line-merge travel for exam.jsonl, acts, steers.md
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:32:03Z created
## Follow-ups captured
