---
id: T-2248
type: FIX
tier: S
status: done
priority: urgent
scope: []
depends_on: []
source: baseline
created: 2026-10-31T01:16:01Z
updated: 2026-10-31T01:18:39Z
baseline: true
base: 5df339d823c535ce938ad175cefc9876e9d05e74
base_tree: 1056db833d97c3f8b7aeb038500b0ad723224541
plan0_at: 2026-10-31T01:16:52Z
plan0_scope: []
verified: strong
---
# Baseline red: `python3 plugin/tests/run.py` fails…
## Raw request
> Baseline red: `python3 plugin/tests/run.py` fails test_which.Which.test_foremans_own_release_tool_is_not_a_users_release. Captured by fm check: the gates are red, so fix this before new work (it may not be this task's doing).
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm which "ship a release" lists release/release-and-changelog again, with T-2070's new release playbooks present — verify with `cd plugin/tests && python3 -m unittest -q test_which`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the playbook's header names shipping a release (it was crowded out of the top five by T-2070's go and mobile release playbooks, which say ship)
## Resume here
## Docs impact
none: internal ranking
## Verification evidence
- `cd plugin/tests && python3 -m unittest -q test_which` → ✗ exit 1 · Ran 15 tests in 2.959s / FAILED (failures=2) (start tree + this task's tests) [ran] [tree 9dd82b8141f9] (2026-10-31T01:18:04Z)
- `cd plugin/tests && python3 -m unittest -q test_which` → exit 0 · Ran 15 tests in 2.740s / OK [ran] [tree 9dd82b8141f9] (2026-10-31T01:18:04Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_which` → exit 0 · Ran 15 tests in 2.639s / OK [ran] [tree 9dd82b8141f9] (2026-10-31T01:18:16Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_which` → exit 0 · Ran 15 tests in 2.634s / OK [ran] [tree 9dd82b8141f9] (2026-10-31T01:18:20Z)
- (audit edge) `self: rank's name words are now a name's last segment, so a folder shared by every book in it no longer ties them; the folder still counts once in the text, so a 'ui' task still finds ui/ books; skills (foreman:x) and commands (fm x) have no slash and are unchanged; test_which 15 green` → a task word that is only a folder name now lists a book only if the book holds half the task's words; checked ui and release queries [tree 9dd82b8141f9] (2026-10-31T01:18:20Z)
- (audit self) `self: rank's name words are now a name's last segment, so a folder shared by every book in it no longer ties them; the folder still counts once in the text, so a 'ui' task still finds ui/ books; skills (foreman:x) and commands (fm x) have no slash and are unchanged; test_which 15 green` → no findings [tree 9dd82b8141f9] (2026-10-31T01:18:20Z)
## Log
- 2026-10-31T01:16:01Z created
- 2026-10-31T01:16:51Z set tier=S
- 2026-10-31T01:16:51Z planned: it has criteria and steps
- 2026-10-31T01:16:51Z set approved=True
- 2026-10-31T01:16:52Z focused
- 2026-10-31T01:18:16Z scope: plugin/lib/fmwhich.py (the root cause, rank's name words), the playbook header and test_which
- 2026-10-31T01:18:37Z done
- 2026-10-31T01:18:39Z committed ffe35a62 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2085 [FIX M, dropped, 0 steps] Baseline red: `python3 plugin/tests/run.py` fails…
- T-2021 [FIX M, dropped, 0 steps] Baseline red: `python3 plugin/tests/run.py` fails…
- T-2150 [FIX S, done, 1 steps] Baseline red: `python3 plugin/tests/run.py` fails… — lesson: a new key field (done) needs a sweep of every test that iterates fmexam.KINDS,…
- decision 2026-10-30: [revisited: no idea is killed for ambition] [cites: user steer 2026-10-29: NO IDEA IS KILLED FOR AMBITION] [check: python3 plugin/tests/run.py test_…
- the similar finished task took 1 steps
- start here (files T-2150 touched): plugin/tests/test_find.py
## Lessons
- A name segment shared by a whole folder can't discriminate inside it; weighting it ties every member and the tiebreak decides
## Files touched
- plugin/skills/playbooks/references/release/release-and-changelog.md
- plugin/lib/fmwhich.py
- plugin/tests/test_which.py
