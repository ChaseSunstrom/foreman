---
id: T-0343
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-06T03:23:38Z
updated: 2026-10-06T03:24:59Z
base: 6a160b357cbae14449e449024770f4d57b9a2aa0
base_tree: dd7e0d1da8624b9b3be93d5b99a6e3747f25e226
verified: strong
---
# Related past work keeps one slot for a matching decision
## Raw request
> Related past work at fm task new/focus should include matching decisions.md rows: T-0333 re-built 'edit a criterion in place', which a 2026-10-04 decision had dropped (T-0305), and nothing surfaced it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a decision that matches a new task is recalled even when more than four briefs match better — verify with `python3 plugin/tests/run.py -k test_recall`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test (red)
2. [x] reserve a decision slot
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_recall.Recall.test_a_matching_decision` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: Recall 2s) / OK [ran] [tree 55de7941ace9] (2026-10-06T03:24:10Z)
- (step 1) `python3 plugin/tests/run.py -k test_recall.Recall.test_a_matching_decision` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: Recall 2s) / FAILED (1 classes) [ran] [tree 866d366e6b2e] (2026-10-06T03:24:32Z)
- (step 1) `python3 plugin/tests/run.py -k test_recall.Recall.test_a_matching_decision` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: Recall 2s) / OK [ran] [tree 78e75c205c98] (2026-10-06T03:24:49Z)
- (ac 1) `python3 plugin/tests/run.py -k test_recall` → exit 0 · Ran 13 tests in 9.8s (4 classes, 16 at a time; slowest: Recall 10s, RedGreen 2s, Memory 1s) / OK [ran] [tree 78e75c205c98] (2026-10-06T03:24:59Z)
- (step 2) `python3 plugin/tests/run.py -k test_recall` → exit 0 · Ran 13 tests in 9.8s (4 classes, 16 at a time; slowest: Recall 10s, RedGreen 2s, Memory 1s) / OK [ran] [tree 78e75c205c98] (2026-10-06T03:24:59Z)
- (audit self) `self-review: one decision slot, only when a decision passes recall's own match threshold (≥2 shared words) and isn't already in the top four; the real T-0333 query now surfaces the decision` → no findings [tree 78e75c205c98] (2026-10-06T03:24:59Z)
## Log
- 2026-10-06T03:23:38Z created
- 2026-10-06T03:24:02Z planned from capture
- 2026-10-06T03:24:02Z focused
- 2026-10-06T03:24:59Z done
- 2026-10-06T03:24:59Z committed 9f7e08e (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0043 [FEATURE M, done, 0 steps] Fm recall — surface related past briefs (with outcomes and a tier hint), decisions (with s
- research T-0262-review-1: LOW** — `plugin/lib/fmcore.py:230-239`: the creation-time check is sound. `realpath` plus the `top + os.sep` prefix rejects `../`, absolute pat…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research T-0263-review-1: Findings come from reading the diff plus `fmcore.py`, `fmmap.py` and `fmrecall.py`. I did not run any tests. Line numbers for new code are diff…
- similar past tasks were M: consider --tier M
## Lessons
- Ranking mixes kinds that answer different questions; a kind that says 'don't' (a decision) needs a reserved place, not a fair fight with kinds that say 'how'.
## Files touched
- plugin/tests/test_recall.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
