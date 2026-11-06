---
id: T-1009
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-16T01:12:01Z
updated: 2026-10-16T01:30:43Z
base: 9fab93447e9ccb392e5a5d75d021194df8e438c0
base_tree: 01a3caeefae6d3a876ac0d570c6ccd802b782197
verified: strong
---
# fm task finish --why-not-caught: no follow-up when the task's own edits already added the catching test
## Raw request
> fm task finish --why-not-caught always captures a 'catch it earlier' follow-up, even when the close already added the missing test (T-1007 → T-1008, dropped); let a flag (--caught-now or a test file in the diff) skip it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a finish whose task touched a test file (c.TESTISH) captures no 'Catch it earlier' task and says the catch landed; one that touched none still captures it — verify with `python3 plugin/tests/run.py test_diagnosis`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: both cases in the close-out tests
2. [x] fmcli finish: skip the capture when c.task_touches(p, b.id) holds a TESTISH path; one line naming it
3. [x] docs: CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_diagnosis` → ✗ exit 1 · Ran 6 tests in 1.3s (5 classes, 16 at a time; slowest: WhyNotCaught 1s, Ladder 1s, Fingerprint 1s) / FAILED (1 classes) [ran] [tree 1f7ed4d09bdd] (2026-10-16T01:30:22Z)
- (step 2) `python3 plugin/tests/run.py test_diagnosis test_finish_self_docs` → exit 0 · Ran 10 tests in 2.7s (6 classes, 16 at a time; slowest: WhyNotCaught 3s, Ladder 1s, Fingerprint 1s) / OK [ran] [tree 968b3366bd69] (2026-10-16T01:30:30Z)
- (step 3) `grep -q 'T-1009' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 8387d0e34f9f] (2026-10-16T01:30:38Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 6 tests in 1.4s (5 classes, 16 at a time; slowest: WhyNotCaught 1s, Ladder 1s, Fingerprint 1s) / OK [ran] [tree 8387d0e34f9f] (2026-10-16T01:30:40Z)
- (audit edge) `self` → a task with no test file touched still gets its follow-up (existing test); 'none: …' still captures nothing; any TESTISH path the hooks saw counts [tree 8387d0e34f9f] (2026-10-16T01:30:40Z)
- (ac 1) `python3 plugin/tests/run.py test_diagnosis` → exit 0 · Ran 6 tests in 1.3s (5 classes, 16 at a time; slowest: WhyNotCaught 1s, Ladder 1s, Fingerprint 1s) / OK [ran] [tree 8387d0e34f9f] (2026-10-16T01:30:42Z)
- (audit edge) `ported the recorded session's change and test; added the one-line notice the brief asked for` → no test touched → follow-up as before [tree 8387d0e34f9f] (2026-10-16T01:30:42Z)
- (audit self) `ported the recorded session's change and test; added the one-line notice the brief asked for` → no findings [tree 8387d0e34f9f] (2026-10-16T01:30:42Z)
## Log
- 2026-10-16T01:12:01Z created
- 2026-10-16T01:12:54Z planned from capture
- 2026-10-16T01:12:57Z criterion 1 verify: `python3 plugin/tests/run.py test_close_out` → `python3 plugin/tests/run.py test_finish`
- 2026-10-16T01:13:00Z criterion 1 verify: `python3 plugin/tests/run.py test_finish` → `python3 plugin/tests/run.py test_diagnosis`
- 2026-10-16T01:30:13Z focused
- 2026-10-16T01:30:42Z done
- 2026-10-16T01:30:43Z committed f8bddf5 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0952 [FEATURE S, done, 1 steps] --affected also runs tests that historically change together with the edited files (the map's co-change pairs), so a hooks.json edit ru…
- T-0879 [FEATURE S, done, 0 steps] Catch it earlier: the test only covered tracked, already-linked tests; the map is built fr
- research mission-20261014-103352.pack: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. etc.…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 0–1 steps
- start here (files T-0952 touched): plugin/tests/test_cli.py, plugin/lib/fmcli.py
## Plan gaps
- failed first: step 1 test: both cases in the close-out tests
## Files touched
- plugin/tests/test_diagnosis.py
- plugin/lib/fmcli.py
- CHANGELOG.md
