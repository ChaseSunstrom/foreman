---
id: T-1182
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmreplay.py, plugin/tests/test_guard_cases.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T13:22:32Z
base: 5c89b4829cd6dc3edf9e3f0623bedc7d56929ecb
base_tree: 1756d51ce11cb310c562f56393661466f045bcc5
plan0_at: 2026-10-16T13:19:51Z
plan0_scope: [plugin/lib/fmreplay.py, plugin/tests/test_guard_cases.py, CHANGELOG.md]
verified: strong
---
# The `fm replay` gate also checks the labelled guard cases (plugin/tests/fixtures/guard_cas
## Raw request
> FEATURE: The `fm replay` gate also checks the labelled guard cases (plugin/tests/fixtures/guard_cases.jsonl) and fails on a drifted or broken case, so any task touching fmguard.py meets them at its gates.
> DONE-WHEN: a test in plugin/tests/test_guard_cases.py runs `fm replay` with a drifted labelled case and sees a non-zero exit naming it, and a clean corpus passes.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm replay (the gate) exits 1 naming a drifted or broken labelled case, and passes with a clean corpus — verify with `python3 plugin/tests/run.py test_guard_cases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_guard_cases
2. [x] The default replay path checks the cases too
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_cases` → ✗ exit 1 · Ran 11 tests in 25.0s (1 classes, 16 at a time; slowest: GuardCases 25s) / FAILED (1 classes) [ran] [tree 0f9031cc01c6] (2026-10-16T13:20:21Z)
- (step 2) `python3 plugin/tests/run.py test_guard_cases test_replay` → exit 0 · Ran 19 tests in 24.3s (3 classes, 16 at a time; slowest: GuardCases 24s, Replay 3s, Core 0s) / OK [ran] [tree 6eebec891c21] (2026-10-16T13:20:53Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 11 tests in 28.5s (1 classes, 16 at a time; slowest: GuardCases 28s) / OK [ran] [tree 89ec0f44425b] (2026-10-16T13:21:47Z)
- (step 1) `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 11 tests in 28.5s (1 classes, 16 at a time; slowest: GuardCases 28s) / OK [ran] [tree 89ec0f44425b] (2026-10-16T13:21:47Z)
- (audit adversary) `self: the default replay (the configured gate) now loads the labelled cases, lists drifted ones and exits 1 on drift or broken lines, whatever --accept says (labels aren't a baseline); ran fm replay here: green with the 6 committed cases` → a drifted allow label can't be accepted away; only fixing the guard or the label clears it [tree 89ec0f44425b] (2026-10-16T13:21:47Z)
- (audit edge) `self: the default replay (the configured gate) now loads the labelled cases, lists drifted ones and exits 1 on drift or broken lines, whatever --accept says (labels aren't a baseline); ran fm replay here: green with the 6 committed cases` → no corpus file: no cases line, no failure [tree 89ec0f44425b] (2026-10-16T13:21:47Z)
- (audit self) `self: the default replay (the configured gate) now loads the labelled cases, lists drifted ones and exits 1 on drift or broken lines, whatever --accept says (labels aren't a baseline); ran fm replay here: green with the 6 committed cases` → no findings [tree 89ec0f44425b] (2026-10-16T13:21:47Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T13:19:50Z set tier=S, scope=['plugin/lib/fmreplay.py', 'plugin/tests/test_guard_cases.py', 'CHANGELOG.md']
- 2026-10-16T13:19:50Z focused
- 2026-10-16T13:22:31Z done
- 2026-10-16T13:22:32Z committed d4cdaa9d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1175 [FIX S, done, 2 steps] Fm guard wrong run from a builder's worktree writes into the main checkout's corpus (PLUGI
- T-1162 [FEATURE M, done, 2 steps] Add `fm guard wrong "<cmd>" --should allow|block` to store a labelled case that `fm replay — lesson: a guard verdict can depend on wher…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_replay.py
## Plan gaps
- failed first: step 1 Failing test in test_guard_cases
## Files touched
- plugin/tests/test_guard_cases.py
- plugin/lib/fmreplay.py
- CHANGELOG.md
