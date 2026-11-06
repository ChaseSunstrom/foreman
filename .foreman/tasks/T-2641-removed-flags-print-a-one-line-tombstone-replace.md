---
id: T-2641
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_tombstones.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T19:49:33Z
builder_model: sonnet
base: 410b2964ae4ff484ed0b51ba30d8c7c3593e4f85
base_tree: 2447aa25eacae35162142d2e08d919463676cf06
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T19:35:16Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_tombstones.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T19:38:51Z
verified: strong
---
# A removed fm verb or flag prints its tombstone (what replaced it and the task that removed it) instead of argparse's bare error; first entry fm night --print-timer (removed in T-2475)
## Raw request
> FEATURE: Removed flags print a one-line tombstone (replacement and version) instead of an argparse error (c08: CLI ergonomics and doctor; value 3, effort S, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm night --print-timer exits 2 naming T-2475 and the replacement, and an unknown flag with no tombstone keeps argparse's message and the unknown_word event — verify with `python3 plugin/tests/run.py test_tombstones test_gate_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] a TOMBSTONES table read on the parser's error path
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tombstones test_gate_friction` → exit 0 · Ran 14 tests in 5.6s (3 classes, 16 at a time; slowest: Typos 5s, Flakes 3s, Tombstones 0s) / OK [ran] [tree bef2e3b659df] [world 2f1906870a] (2026-11-02T19:36:03Z)
- (step 2) `python3 plugin/tests/run.py test_tombstones test_gate_friction` → exit 0 · Ran 14 tests in 4.1s (3 classes, 16 at a time; slowest: Typos 3s, Flakes 3s, Tombstones 1s) / OK [ran] [tree bef2e3b659df] [world 2f1906870a] (2026-11-02T19:36:07Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_paused test_robustness test_tombstones test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [16.44s] [ran] [tree bef2e3b659df] [world 2f1906870a] (2026-11-02T19:36:53Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:43:25Z)
- (ac 1) `python3 plugin/tests/run.py test_tombstones test_gate_friction` → exit 0 · Ran 14 tests in 2.2s (3 classes, 16 at a time; slowest: Typos 2s, Flakes 1s, Tombstones 0s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:43:29Z)
- (audit edge) `self: builder diff read: a TOMBSTONES table read only on the parser's error path; a tombstoned flag logs no unknown_word vote` → an unknown flag with no tombstone keeps argparse's message and its friction event (tested); a removed flag under a nested subcommand needs a wider key (noted) [tree 1c68dd523ead] (2026-11-02T19:43:29Z)
- (audit self) `self: builder diff read: a TOMBSTONES table read only on the parser's error path; a tombstoned flag logs no unknown_word vote` → no findings [tree 1c68dd523ead] (2026-11-02T19:43:29Z)
- `python3 plugin/tests/run.py test_tombstones test_gate_friction` → exit 0 · Ran 14 tests in 3.7s (3 classes, 16 at a time; slowest: Typos 3s, Flakes 2s, Tombstones 1s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:48:18Z)
- (audit edge) `self: builder diff read: a TOMBSTONES table read only on the parser's error path; a tombstoned flag logs no unknown_word vote` → an unknown flag with no tombstone keeps argparse's message and its friction event (tested); a removed flag under a nested subcommand needs a wider key (noted) [tree 1c68dd523ead] (2026-11-02T19:48:18Z)
- (audit self) `self: builder diff read: a TOMBSTONES table read only on the parser's error path; a tombstoned flag logs no unknown_word vote` → no findings [tree 1c68dd523ead] (2026-11-02T19:48:18Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T19:35:04Z planned from capture
- 2026-11-02T19:35:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2641.builder.md
- 2026-11-02T19:35:15Z focused
- 2026-11-02T19:35:16Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T19:38:51Z merged worktree-agent-a790ee6b04948dc4e (2 file(s))
- 2026-11-02T19:41:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a790ee6b04948dc4e
- 2026-11-02T19:43:15Z focused
- 2026-11-02T19:44:21Z paused: focus moved to T-2657
- 2026-11-02T19:48:11Z focused
- 2026-11-02T19:48:12Z scope: the other files in its range came from the T-2657, T-2642 and T-2643 lanes merged between this task's base and its close, and from T-2634 and T-2643 committed on main; none is this task's edit
- 2026-11-02T19:49:33Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2657 [FEATURE S, planned, 3 steps] flakes.json counts each flaky test's fails and passes; fm doctor lists the three worst by fail rate with the command that flakes them
- T-2643 [FEATURE S, planned, 3 steps] fm doctor checks, at most once a day, that each model name Foreman pins (fmgenesis.REVIEW_MODELS, the exam and steer defaults) still…
- T-2642 [FEATURE S, planned, 3 steps] fm ship refuses to push when the tree it would push isn't the tree its tests ran on (an edit or checkout between the gates and the p…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Lessons
- Removing a flag deserves a tombstone in the same change, so the next person who reaches for it learns where it went
## Files touched
- plugin/tests/test_tombstones.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/lib/fmrelease.py
- plugin/tests/test_flake_rates.py
- plugin/tests/test_ship.py
