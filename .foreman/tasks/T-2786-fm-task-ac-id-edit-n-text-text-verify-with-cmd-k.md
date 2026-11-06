---
id: T-2786
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_task*.py, plugin/tests/test_cli.py]
depends_on: []
source: self
created: 2026-11-03T05:20:46Z
updated: 2026-11-03T17:29:22Z
builder_model: sonnet
base: bf52296085ee1871196fbeb0d567362cf45f1d83
base_tree: 17b42647f84c17cdb8bafad92f47029f2238b0c5
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T05:31:49Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_task*.py, plugin/tests/test_cli.py]
lane_stop: merged 2026-11-03T14:26:52Z
verified: strong
---
# fm task ac ID edit N --text reads a verify command typed in the text: 'TEXT :: CMD' (as add and task new take it) or a trailing '— verify with `CMD`' sets the verify instead of being stored as text, unless --verify is also given (then the text keeps the phrase out and --verify wins)
## Raw request
> FIX: fm task ac ID edit N --text '<text> — verify with `cmd`' keeps the old verify command and stores the typed phrase as text, so the criterion then reads two verify commands and runs the old one: three lane merges (T-2765, T-2768, T-2781) were refused on 2026-11-02 for it. Parse a trailing 'verify with `cmd`' (or ':: cmd') in --text into --verify, as fm task new does
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] editing a criterion with --text 'X :: CMD' or 'X — verify with CMD in backticks' stores text X and verify CMD, and the criterion line holds one verify — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_cli for both forms, then the split in task_ac's edit branch; run test_cli
## Resume here
## Docs impact
none: fm task ac -h
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 146 tests in 41.9s (44 classes, 16 at a time; slowest: TaskLifecycle 41s, CaptureAndIntake 22s, StateViews 20s) / OK [ran] [tree 41722639c664] [world 2f1906870a] (2026-11-03T05:34:02Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.48s] [ran] [tree 41722639c664] [world 2f1906870a] (2026-11-03T05:35:06Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 146 tests in 21.9s (44 classes, 16 at a time; slowest: TaskLifecycle 21s, CaptureAndIntake 9s, StateViews 9s) / FAILED (1 classes: test_cli.CaptureAndIntake) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:28:45Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 146 tests in 20.6s (44 classes, 16 at a time; slowest: TaskLifecycle 20s, CaptureAndIntake 9s, StateViews 9s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:28:45Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:28:45Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:28:46Z)
- (audit intent) `self: read the diff; the edit branch splits ' :: ' and a trailing verify-with phrase` → fm task ac edit --text reads a verify command typed into the text [tree 07445d19b39c] (2026-11-03T17:28:46Z)
- (audit edge) `self: read the diff; the edit branch splits ' :: ' and a trailing verify-with phrase` → --verify wins and the phrase still leaves the text; a mid-text phrase stays text; a phrase-only text leaves the old text [tree 07445d19b39c] (2026-11-03T17:28:46Z)
- (audit adversary) `self: read the diff; the edit branch splits ' :: ' and a trailing verify-with phrase` → the parsed verify runs through _refuse_unrunnable and _lint_verify like any other [tree 07445d19b39c] (2026-11-03T17:28:46Z)
- (audit self) `self: read the diff; the edit branch splits ' :: ' and a trailing verify-with phrase` → no findings [tree 07445d19b39c] (2026-11-03T17:28:46Z)
## Log
- 2026-11-03T05:20:46Z created
- 2026-11-03T05:31:21Z planned from capture
- 2026-11-03T05:31:23Z set approved=True
- 2026-11-03T05:31:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2786.builder.md
- 2026-11-03T05:31:47Z focused
- 2026-11-03T05:31:49Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T14:21:31Z criterion 1 verify: `python3 -c pass' or 'X — verify with `python3 -c pass`' stores text X and verify 'python3 -c pass', and the criterion line holds one verify — verify with `python3 plugin/tests/run.py test_cli`` → `python3 plugin/tests/run.py test_cli`
- 2026-11-03T14:21:31Z criterion 1 text: editing a criterion with --text 'X → editing a criterion with --text 'X :: CMD' or 'X — verify with CMD in backticks' stores text X and verify CMD, and the criterion line holds one verify
- 2026-11-03T14:26:52Z merged worktree-agent-a65ac611f034a8e67 (2 file(s))
- 2026-11-03T14:28:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a65ac611f034a8e67
- 2026-11-03T15:07:45Z focused
- 2026-11-03T15:07:46Z paused: focus moved to T-2780
- 2026-11-03T17:05:16Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T17:05:16Z focused
- 2026-11-03T17:05:17Z paused: focus moved to T-2780
- 2026-11-03T17:28:01Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T17:28:01Z focused
- 2026-11-03T17:29:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2756 [FIX S, active, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2766 [FEATURE M, planned, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently a…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/cli.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Lessons
- Parse the same input forms everywhere a criterion is written
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/cli.py
