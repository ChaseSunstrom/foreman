---
id: T-1758
type: FIX
tier: S
status: done
priority: urgent
scope: [plugin/rules/foreman.md, plugin/evals/**]
depends_on: []
source: user
created: 2026-10-23T06:36:07Z
updated: 2026-10-23T06:36:55Z
base: c3b9aed259646d2d798e7f4f7a5a1d042887afc4
base_tree: cdbfded9c1dc6975ab266a3f6fc9a8eeedf66bcc
plan0_at: 2026-10-23T06:36:11Z
plan0_scope: [plugin/rules/foreman.md, plugin/evals/**]
verified: strong
---
# Rules file over the doctor's 6,400-char budget since T-1520 (6,416): trim it back under
## Raw request
> Rules file over the doctor's 6,400-char budget since T-1520 (6,416): trim it back under
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the rules file fits the footprint budget — verify with `python3 plugin/tests/run.py test_doctor.CoreIntegrity.test_description_budget`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] trim plugin/rules/foreman.md under 6,400 chars, regenerate the eval prompts
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor.CoreIntegrity.test_description_budget` → red as expected (exit 1) · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: CoreIntegrity 0s) / FAILED (1 classes) [ran] [tree cdbfded9c1dc] (2026-10-23T06:36:17Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_docs test_evals` → ✗ exit 1 · run.py: no test matches test_evals [ran] [tree 833b4d3938eb] (2026-10-23T06:36:24Z)
- (step 1) `python3 plugin/tests/run.py test_doctor test_docs` → exit 0 · Ran 133 tests in 8.6s (38 classes, 16 at a time; slowest: Fences 8s, Command 2s, TaskLifecycle 2s) / OK [ran] [tree 833b4d3938eb] (2026-10-23T06:36:36Z)
- (audit intent) `self` → pass: 6,394 chars, under the 6,400 budget; fm which stays in the rules (the parity test needs it); fm help is still named by fm which's own output [tree 833b4d3938eb] (2026-10-23T06:36:44Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor.CoreIntegrity.test_description_budget` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: CoreIntegrity 0s) / OK [ran] [tree 833b4d3938eb] (2026-10-23T06:36:45Z)
- (audit intent) `self: one-line trim` → under budget, parity line kept [tree 833b4d3938eb] (2026-10-23T06:36:45Z)
- (audit self) `self: one-line trim` → no findings [tree 833b4d3938eb] (2026-10-23T06:36:45Z)
- (audit intent) `self: one-line trim` → under budget, parity line kept [tree 833b4d3938eb] (2026-10-23T06:36:52Z)
- (audit adversary) `self: one-line trim` → the guard eval prompts changed only by the regenerated rules text (the removed fm help aside); no guard instruction or category text moved [tree 833b4d3938eb] (2026-10-23T06:36:52Z)
- (audit self) `self: one-line trim` → no findings [tree 833b4d3938eb] (2026-10-23T06:36:52Z)
## Log
- 2026-10-23T06:36:07Z created
- 2026-10-23T06:36:10Z set priority=urgent, scope=['plugin/rules/foreman.md', 'plugin/evals/**']
- 2026-10-23T06:36:11Z focused
- 2026-10-23T06:36:53Z done
- 2026-10-23T06:36:55Z committed a46608be (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-1569 [FIX S, done, 1 steps] Playbooks index over its 10,000-char budget: doctor's footprint check and the release check fail — lesson: An index that every new file mus…
- T-1140 [PERFORMANCE M, done, 2 steps] PreToolUse p95 is 210 ms over the last 200 runs, over the 150 ms SLO since 1.2.31 (fm doct — lesson: On a hot path, find the one re…
- decision 2026-10-20: T-1276 trims no fm verb: measured right, fm-only command output is 0.9% of what entered the context over three days (the 3.5% counted test runs chai…
## Regression test
existing: test_doctor.CoreIntegrity.test_description_budget already guards the budget and is red on main (6,416 chars); the miss was the push, not a missing test
## Why not caught
T-1520's close ran only its affected tests, and the push followed a background fm check piped through tail: the notification's exit 0 was tail's, while the gate itself said ✗
## Lessons
- A gate run in the background must not be piped through tail: read its ✓/✗ line (or its own exit code) before pushing
## Files touched
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
