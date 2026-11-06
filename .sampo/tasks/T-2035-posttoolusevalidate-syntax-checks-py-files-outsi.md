---
id: T-2035
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T19:48:41Z
updated: 2026-10-29T20:04:33Z
base: 84c44ebd8f2ad883a77185963c7dab09e4e20eac
base_tree: 85c48479d346b9d743c0d2555c8c754b724c0c3c
plan0_at: 2026-10-29T19:59:49Z
plan0_scope: []
verified: strong
---
# PostToolUseValidate syntax-checks .py files outside the project (a scratchpad method…
## Raw request
> PostToolUseValidate syntax-checks .py files outside the project (a scratchpad method snippet meant for pasting) and blocks with 'unparsable'; limit it to files under the repo, like T-2032's claim check
## Interpretation
A .py draft outside the project (a scratch snippet that starts indented) is blocked by the write validator as unparsable, costing a turn to explain; Python outside the project root isn't code the project runs, so it isn't syntax-checked. JSON stays checked everywhere (fm edit drafts).
## Assumptions (confidence)
## Acceptance criteria
- [x] A .py fragment outside the repo passes; inside it still blocks; bad JSON outside still blocks — verify with `python3 plugin/tests/run.py test_onwrite`
## Non-goals
## Approach (options → choice → why)
In _onwrite, skip _syntax_note for .py files whose path is outside p.root (the same relpath test the project validators use); frontmatter and JSON checks unchanged.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test in test_onwrite, then the _onwrite change
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- `python3 plugin/tests/run.py test_onwrite -k test_python_that_does_not_compile_blocks` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: OnWrite 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 61ca3812dee9] (2026-10-29T20:00:13Z)
- `python3 plugin/tests/run.py test_onwrite -k test_python_that_does_not_compile_blocks` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: OnWrite 0s) / OK [ran] [tree 61ca3812dee9] (2026-10-29T20:00:13Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.8    32.1     150  [0] / SessionEnd                  24.2    26.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 61ca3812dee9] (2026-10-29T20:03:38Z)
- (ac 1) `python3 plugin/tests/run.py test_onwrite` → exit 0 · Ran 10 tests in 6.7s (1 classes, 16 at a time; slowest: OnWrite 6s) / OK [ran] [tree 61ca3812dee9] (2026-10-29T20:03:54Z)
- (audit intent) `self-review of the diff: _onwrite skips only the .py compile for paths outside p.root; JSON, frontmatter, card lint unchanged; rel moved up and reused by the project validators` → a scratch .py snippet (starts indented) no longer blocks; inside the repo a broken .py still blocks (test) [tree 61ca3812dee9] (2026-10-29T20:03:54Z)
- (audit edge) `self-review of the diff: _onwrite skips only the .py compile for paths outside p.root; JSON, frontmatter, card lint unchanged; rel moved up and reused by the project validators` → a builder lane's worktree is its own p.root (find_project), so its .py files stay checked; JSON drafts outside still block (test) [tree 61ca3812dee9] (2026-10-29T20:03:54Z)
- (audit self) `self-review of the diff: _onwrite skips only the .py compile for paths outside p.root; JSON, frontmatter, card lint unchanged; rel moved up and reused by the project validators` → no findings [tree 61ca3812dee9] (2026-10-29T20:03:54Z)
## Log
- 2026-10-29T19:48:41Z created
- 2026-10-29T19:59:48Z set type=FIX, tier=S
- 2026-10-29T19:59:48Z planned: it has criteria and steps
- 2026-10-29T19:59:48Z focused
- 2026-10-29T20:04:32Z done
- 2026-10-29T20:04:33Z committed 00ec968b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2032 [FIX S, done, 2 steps] Stop hook's claim check flags a future 'when the gates pass' as a claim, and counts a… — lesson: A check keyed to 'the project' should reso…
- T-1980 [FIX M, done, 4 steps] Batch keeps DONE-WHEN verify, gates name why-not-caught, fm ship marks its test run, first_touch keeps project files — lesson: A marker tha…
- T-1781 [FIX S, done, 1 steps] Guard false refusal: cd /abs/scratch && date && for f in a b; do cp /repo/$f full/$f; done — lesson: A conservative bail-out (any backslash…
- decision 2026-10-28: T-1838 step 3: the per-turn hint still does not name the top routed book
- similar finished tasks took 1–4 steps
## Lessons
- A validator that blocks should stop at the project's edge for files the project never runs; drafts elsewhere are the author's business
## Files touched
- plugin/tests/test_onwrite.py
- CHANGELOG.md
- plugin/lib/fmhooks.py
