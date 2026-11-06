---
id: T-2207
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T19:59:28Z
updated: 2026-10-30T23:01:29Z
base: eec155411337cfb772f1d6692ced18a771e1c8ad
base_tree: 3c921f6666e7c057d91c6fab7815f4e718790aef
plan0_at: 2026-10-30T22:48:09Z
plan0_scope: []
verified: strong
---
# Cold reads converge: a line read clean stays accepted while unchanged and the charter holds; a later FAIL on it is advisory; genesis_read counts carried fails
## Raw request
> nothing measures whether carried findings cut the rounds; the genesis_read ledger events per name already give the round count, so the next long filing (T-2182's mission-genesis.md) is the before/aft…
> (noticed by an agent; research T-2205-review)
## Interpretation
Tower puts re-judge every unchanged line with a stochastic Haiku reader, so long files fail 1-4 lines a round indefinitely (ledger: mission-exam 31 rounds, mission-genesis 24 and failing, coverage 11; T-2182, T-2221, T-2223 blocked). Make a put converge without weakening the read: every line still gets a cold read; one already read clean, unchanged, under the same gen-0/steers/standing intent, can't block again; the event says how many fails were carried, so the round effect is measured.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fail on a line read clean before, unchanged under the same charter, files the doc with an advisory; a changed line or a new steer blocks again; genesis_read records carried — verify with `python3 plugin/tests/run.py test_genesis.GenesisRead`
## Non-goals
## Approach (options → choice → why)
Options: (a) per-line acceptance keyed on the line text and the charter hash, later fails on accepted lines shown as advisories; (b) a FAIL counts only if 2 of 3 independent reads name it (3x cost, lower recall on real issues); (c) read only the diff lines (loses whole-file context; the reader can't see contradictions); (d) raise the 3-attempt limit (doesn't converge). Choice (a): the reader still sees the whole file every put, new or changed lines and earlier fails still block, a new steer or gen-0 change voids acceptance, and nothing that was blocking is hidden (advisories print). ponytail: the exam tail isn't in the key (it grows every run), so a claim staled by new exam lines stays advisory until the line changes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: accepted-line test in GenesisRead
2. [x] _read: accepted lines per file + charter hash, advisories, carried count
3. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → red as expected (exit 1) · Ran 5 tests in 1.8s (1 classes, 16 at a time; slowest: GenesisRead 2s) / FAILED (1 classes) [ran] [tree 0cc36a321239] (2026-10-30T22:48:26Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → exit 0 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: GenesisRead 2s) / OK [ran] [tree c6b2b20fb261] (2026-10-30T22:48:57Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 99 tests in 6.3s (13 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 4s, GenesisLive 4s) / OK [ran] [tree c6b2b20fb261] (2026-10-30T22:49:03Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.3s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 74b9ae01c51e] (2026-10-30T22:49:25Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → red as expected (exit 1) · Ran 6 tests in 2.3s (1 classes, 16 at a time; slowest: GenesisRead 2s) / FAILED (1 classes) [ran] [tree 4e1d6fddd781] (2026-10-30T22:53:11Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → exit 0 · Ran 6 tests in 3.3s (1 classes, 16 at a time; slowest: GenesisRead 3s) / OK [ran] [tree d38a74b0c745] (2026-10-30T22:53:55Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_guard_exec_vectors` → exit 0 · Ran 145 tests in 6.5s (20 classes, 16 at a time; slowest: GenesisCheck 6s, GenesisSweep 5s, GenesisLive 5s) / OK [ran] [tree d38a74b0c745] (2026-10-30T22:54:02Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.3s (21 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree d38a74b0c745] (2026-10-30T22:54:10Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisRead` → exit 0 · Ran 6 tests in 3.3s (1 classes, 16 at a time; slowest: GenesisRead 3s) / OK [ran] [tree d38a74b0c745] (2026-10-30T22:54:42Z)
- (audit intent) `one fm-reviewer five-lens pass (research/T-2207-review.md): 2 HIGH, 2 MEDIUM, 3 LOW, all fixed test-first` → converges (accepted lines can't block alone) while every line still gets a whole-file read [tree d38a74b0c745] (2026-10-30T22:54:42Z)
- (audit adversary) `one fm-reviewer five-lens pass (research/T-2207-review.md): 2 HIGH, 2 MEDIUM, 3 LOW, all fixed test-first` → earlier unmet fails never accepted; a second fail blocks; two unflagged reads needed; heading-scoped hashes; key covers reader prompt, charter and exam tail; accepted file is guard-protected state (test) [tree d38a74b0c745] (2026-10-30T22:54:42Z)
- (audit edge) `one fm-reviewer five-lens pass (research/T-2207-review.md): 2 HIGH, 2 MEDIUM, 3 LOW, all fixed test-first` → quote matching several lines carries only if all are accepted; unread rounds leave acceptance untouched [tree d38a74b0c745] (2026-10-30T22:54:42Z)
- (audit operator) `one fm-reviewer five-lens pass (research/T-2207-review.md): 2 HIGH, 2 MEDIUM, 3 LOW, all fixed test-first` → carried_lines in the ledger, advisories printed [tree d38a74b0c745] (2026-10-30T22:54:42Z)
- (audit maintainer) `one fm-reviewer five-lens pass (research/T-2207-review.md): 2 HIGH, 2 MEDIUM, 3 LOW, all fixed test-first` → two tests cover acceptance, revocation, unmet fails, change, move, steer and exam [tree d38a74b0c745] (2026-10-30T22:54:42Z)
## Log
- 2026-10-30T19:59:28Z created
- 2026-10-30T22:48:08Z set tier=M, type=FEATURE, title=Cold reads converge: a line read clean stays accepted while unchanged and the charter holds; a later FAIL on it is advisory; genesis_read counts carried fails
- 2026-10-30T22:48:08Z planned: it has criteria and steps
- 2026-10-30T22:48:09Z focused
- 2026-10-30T22:54:39Z scope: plugin/tests/test_guard_exec_vectors.py — review asked for a guard test that genesis-accepted.json can't be forged (test only, guard unchanged)
- 2026-10-30T22:55:05Z done
- 2026-10-30T22:55:07Z committed d846701f (5 files)
- 2026-10-30T22:56:27Z guard authorization added: publish
- 2026-10-30T23:01:29Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- T-2191 [FEATURE L, done, 4 steps] The user's standing intent (steer 2026-10-30 #7, STANDING INTENT): file it in the tower… — lesson: A rule that says 'a format check is …
- research T-2205-review: Verdict: changes needed (2 MEDIUM intent/edge, 1 MEDIUM edge, 4 LOW); reviewer ran nothing (read-only).
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (second): standing rule] Every tower file (seed, mission, critique, coverage, not-yet, exam entry) gets a cold H…
- similar finished tasks took 4–4 steps
## Lessons
- A convergence rule for a stochastic gate must never let one miss outweigh a recorded fail: acceptance needs repeated agreement and any later fail revokes it
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_guard_exec_vectors.py
