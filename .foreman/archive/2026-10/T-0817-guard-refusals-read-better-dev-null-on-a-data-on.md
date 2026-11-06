---
id: T-0817
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-14T18:02:44Z
updated: 2026-10-14T18:07:53Z
batch: [T-0813, T-0814, T-0815]
base: edb5d6775d9eeb1a65a889881298212487064b8e
base_tree: 2039e63e2572fdff70477f0ccdbc3d407ec9cbc2
verified: strong
---
# Guard refusals read better: /dev/null on a data-only python -c, a state-direct hint that points to fm research, and pat…
## Raw request
> T-0813: Guard: a data-only python3 -c reading a download may redirect 2>/dev/null (fmguard.py:1637 refuses any redirect; 2>&1 is already skipped at :831)
> T-0814: Guard hint for state-direct blocks says: download to scratch, then fm research — not 'name it literally' (fmguard.py:113; state-direct isn't authorizable)
> T-0815: rule_id names path-only refusals by tool or 'path', not 'other' (fmguard.py:55; brief:other is the top rule at 4x)
## Interpretation
Do T-0813, T-0814, T-0815 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0817. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0813: Guard: a data-only python3 -c reading a download may redirect 2>/dev/null (fmguard.py:1637 works — verify with `python3 plugin/tests/run.py test_guard_pipes`
- [x] T-0814: Guard hint for state-direct blocks says: download to scratch, then fm research — not 'name works — verify with `python3 plugin/tests/run.py test_safety`
- [x] T-0815: Rule_id names path-only refusals by tool or 'path', not 'other' (fmguard.py:55; brief:othe works — verify with `python3 plugin/tests/run.py test_safety`
## Non-goals
## Approach (options → choice → why)
Options: (a) per-fix minimal edits in fmguard (redirs to /dev/null dropped in the data-only python -c check; _hint branch on state-direct; rule_id falls back to the tool word); (b) new hint table keyed by category; (c) leave as is and document. Chose (a): three local edits, each with one test; (b) adds machinery for one case.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0813: Guard: a data-only python3 -c reading a download may redirect 2>/dev/null (fmguard.py:1637
2. [x] T-0814: Guard hint for state-direct blocks says: download to scratch, then fm research — not 'name
3. [x] T-0815: Rule_id names path-only refusals by tool or 'path', not 'other' (fmguard.py:55; brief:othe
## Resume here
## Docs impact
none: refusal wording and rule ids are self-describing
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_safety test_guard_pipes` → exit 0 · Ran 24 tests in 1.0s (16 classes, 16 at a time; slowest: CleanupGate 1s, SecretsGate 1s, RuleIds 1s) / OK [ran] [tree 2a5d935940b2] (2026-10-14T18:04:33Z)
- (step 2) `python3 plugin/tests/run.py test_safety test_guard_pipes` → exit 0 · Ran 24 tests in 1.0s (16 classes, 16 at a time; slowest: CleanupGate 1s, SecretsGate 1s, RuleIds 1s) / OK [ran] [tree 2a5d935940b2] (2026-10-14T18:04:34Z)
- (step 3) `python3 plugin/tests/run.py test_safety test_guard_pipes` → exit 0 · Ran 24 tests in 1.0s (16 classes, 16 at a time; slowest: CleanupGate 1s, SecretsGate 1s, RuleIds 1s) / OK [ran] [tree 2a5d935940b2] (2026-10-14T18:04:35Z)
- `python3 plugin/tests/run.py test_safety test_guard_pipes` → ✗ exit 1 · Ran 24 tests in 1.3s (16 classes, 16 at a time; slowest: CleanupGate 1s, SecretsGate 1s, RuleIds 1s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 2a5d935940b2] (2026-10-14T18:04:38Z)
- `python3 plugin/tests/run.py test_safety test_guard_pipes` → exit 0 · Ran 24 tests in 1.0s (16 classes, 16 at a time; slowest: CleanupGate 1s, SecretsGate 1s, RuleIds 1s) / OK [ran] [tree 2a5d935940b2] (2026-10-14T18:04:38Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  claude code features Claude Code 2.1.299 supports every Claude Code feature Foreman uses / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                35.9    37.2     150  [0] / SessionEnd                  32.1    36.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 15:37 UTC; python3 [ran] [tree 2a5d935940b2] (2026-10-14T18:07:37Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_pipes` → exit 0 · Ran 11 tests in 0.3s (10 classes, 16 at a time; slowest: EvalVarsAndComputedNames 0s, PipeIntoShell 0s, IfsForms 0s) / OK [ran] [tree 2a5d935940b2] (2026-10-14T18:07:52Z)
- (ac 2) `python3 plugin/tests/run.py test_safety` → exit 0 · Ran 13 tests in 1.1s (6 classes, 16 at a time; slowest: CleanupGate 1s, SecretsGate 1s, RuleIds 1s) / OK [ran] [tree 2a5d935940b2] (2026-10-14T18:07:52Z)
- (ac 3) `python3 plugin/tests/run.py test_safety` → exit 0 · Ran 13 tests in 1.1s (6 classes, 16 at a time; slowest: CleanupGate 1s, SecretsGate 1s, RuleIds 1s) / OK [ran] [tree 2a5d935940b2] (2026-10-14T18:07:52Z)
- (audit intent) `self: three local guard edits, each with a red→green test; fm replay over the corpus: 0 newly allowed of 1,320 new commands` → T-0813 a data-only python -c may send output to /dev/null (2>json.py still refused); T-0814 every state-direct refusal now names the legal route (scratchpad, then fm research add NAME --file PATH), keeping the 'name it literally' hint for targets that really are elsewhere; T-0815 path-only refusals read brief:path / core:path, not :other [tree 2a5d935940b2] (2026-10-14T18:07:52Z)
- (audit adversary) `self: three local guard edits, each with a red→green test; fm replay over the corpus: 0 newly allowed of 1,320 new commands` → the allowance is the exact token /dev/null: a quoted, relative or ../ spelling is not equal and still refuses; /dev/null can't be planted by the agent; test_guard_diff's dangerous-form corpus and fm replay stayed green [tree 2a5d935940b2] (2026-10-14T18:07:52Z)
## Log
- 2026-10-14T18:02:44Z created
- 2026-10-14T18:02:58Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_guard_pipes`
- 2026-10-14T18:02:58Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_safety`
- 2026-10-14T18:02:58Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_safety`
- 2026-10-14T18:03:02Z focused
- 2026-10-14T18:07:52Z done
- 2026-10-14T18:07:53Z committed e5df801 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 3–7 steps
## Why not caught
none: the friction digest (fm friction) is the check that caught them; it worked as designed
## Lessons
- A refusal hint must name the route that works for the target the agent wanted, not only the route for a different target
## Files touched
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_safety.py
- plugin/lib/fmguard.py
