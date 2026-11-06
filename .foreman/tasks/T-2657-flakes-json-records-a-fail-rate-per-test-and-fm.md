---
id: T-2657
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/tests/test_flake_rates.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T19:50:25Z
builder_model: sonnet
base: 901f844428bf8ab9510231db17d59a2b2bd70fd8
base_tree: 5f31a4559af1fbaf38c868223b43647584a3ed60
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T19:35:17Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmdoctor.py, plugin/tests/test_flake_rates.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T19:39:31Z
verified: strong
---
# flakes.json counts each flaky test's fails and passes; fm doctor lists the three worst by fail rate with the command that flakes them
## Raw request
> FEATURE: flakes.json records a fail rate per test and fm doctor lists the worst (c24: Flaky test quarantine; value 2, effort S, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a test that fails 2 of 4 runs on one tree reads 50% in flakes.json and heads fm doctor's flaky row; a damaged entry is dropped, never the ledger — verify with `python3 plugin/tests/run.py test_flake_rates`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] fail and pass counts in note_flakes; the doctor row
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_flake_rates 2>&1 | tail -5` → ✗ exit 1 · Ran 2 tests in 1.7s (1 classes, 16 at a time; slowest: FlakeRates 0s) / FAILED (1 classes: test_flake_rates.FlakeRates) [ran] [tree db0f8ea66ced] [world 2f1906870a] (2026-11-02T19:35:40Z)
- (step 1) `python3 plugin/tests/run.py test_flake_rates` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: FlakeRates 0s) / OK [ran] [tree dc8d22ad4a7c] [world 2f1906870a] (2026-11-02T19:36:27Z)
- (step 2) `python3 plugin/tests/run.py test_flake_rates test_gate_friction` → exit 0 · Ran 14 tests in 2.6s (3 classes, 16 at a time; slowest: Typos 2s, Flakes 2s, FlakeRates 0s) / OK [ran] [tree dc8d22ad4a7c] [world 2f1906870a] (2026-11-02T19:36:29Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_anergy test_core test_crash_hygiene test_doctor test_flake_rates test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.99s] [ran] [tree dc8d22ad4a7c] [world 2f1906870a] (2026-11-02T19:36:56Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 9.9s (24 classes, 16 at a time; slowest: Fences 9s, DocsProof 3s, TaskLifecycle 2s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:44:32Z)
- (ac 1) `python3 plugin/tests/run.py test_flake_rates` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: FlakeRates 0s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:44:39Z)
- `python3 plugin/tests/run.py test_flake_rates test_gate_friction` → exit 0 · Ran 14 tests in 3.2s (3 classes, 16 at a time; slowest: Typos 3s, Flakes 2s, FlakeRates 0s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:44:39Z)
- (audit edge) `self: builder diff read: note_flakes counts fails and passes, clamped to non-negative ints; the doctor row reads three worst with bounded text` → old entries with only count start from it; damaged entries are skipped; passes count only on the same tree as a pending failure, so the rate leans high (noted in the brief) [tree 1c68dd523ead] (2026-11-02T19:44:39Z)
- (audit self) `self: builder diff read: note_flakes counts fails and passes, clamped to non-negative ints; the doctor row reads three worst with bounded text` → no findings [tree 1c68dd523ead] (2026-11-02T19:44:39Z)
- `python3 plugin/tests/run.py test_flake_rates test_gate_friction` → exit 0 · Ran 14 tests in 2.2s (3 classes, 16 at a time; slowest: Typos 2s, Flakes 1s, FlakeRates 0s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:49:40Z)
- (audit edge) `self: builder diff read: note_flakes counts fails and passes, clamped to non-negative ints; the doctor row reads three worst with bounded text` → old entries with only count start from it; damaged entries are skipped; passes count only on the same tree as a pending failure, so the rate leans high (noted in the brief) [tree 1c68dd523ead] (2026-11-02T19:49:40Z)
- (audit self) `self: builder diff read: note_flakes counts fails and passes, clamped to non-negative ints; the doctor row reads three worst with bounded text` → no findings [tree 1c68dd523ead] (2026-11-02T19:49:40Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T19:35:04Z planned from capture
- 2026-11-02T19:35:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2657.builder.md
- 2026-11-02T19:35:17Z focused
- 2026-11-02T19:35:17Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T19:39:31Z merged worktree-agent-acc8a89478a4c47a7 (3 file(s))
- 2026-11-02T19:41:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acc8a89478a4c47a7
- 2026-11-02T19:44:21Z focused
- 2026-11-02T19:45:48Z paused: focus moved to T-2642
- 2026-11-02T19:49:36Z focused
- 2026-11-02T19:49:37Z scope: the other files in its range came from the T-2657, T-2642 and T-2643 lanes merged between this task's base and its close, and from T-2634 and T-2643 committed on main; none is this task's edit
- 2026-11-02T19:50:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2643 [FEATURE S, planned, 3 steps] fm doctor checks, at most once a day, that each model name Foreman pins (fmgenesis.REVIEW_MODELS, the exam and steer defaults) still…
- T-2641 [FEATURE S, active, 3 steps] A removed fm verb or flag prints its tombstone (what replaced it and the task that removed it) instead of argparse's bare error; firs…
- T-2642 [FEATURE S, planned, 3 steps] fm ship refuses to push when the tree it would push isn't the tree its tests ran on (an edit or checkout between the gates and the p…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_doctor.py
## Lessons
- A flake ledger that only names tests can't rank them; counting both outcomes is what makes the worst one findable
## Files touched
- plugin/tests/test_flake_rates.py
- plugin/lib/fmcore.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- plugin/lib/fmrelease.py
- plugin/tests/test_ship.py
