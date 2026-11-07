---
id: T-0957
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:43Z
updated: 2026-10-15T22:03:10Z
base: b595b8924a0e85f5032f946390d81bd4332a7572
base_tree: cef0333733f104deb481d2dc63ff793b2f9c3043
verified: strong
---
# Hooks: idle stops recorded, plan mode holds drive, the user's words and permission mode logged, what's new after an upgrade
## Raw request
> Hooks: idle stops recorded, plan mode holds drive, the user's words and permission mode logged, what's new after an upgrade
## Interpretation
Board clusters r2-session-liveness (at the end of stop() in fmhooks.py ~1817, with no reason and queue or active non-empty, log idle_stop; fm doctor shows a 7-day count), plan-mode (fmhooks.py ~576: hold = is_plan_only(text) or payload permission_mode == 'plan'), intake + misc #272 (after parse_intake ~539 log a 'prompt' ledger event with c.fit(c.redact(text),2000) and permission_mode, skipped in sensitive projects) and r4-digest-unify (SessionStart compares plugin.json's version with a stored last-seen version and prints that version's CHANGELOG bullets once).
## Assumptions (confidence)
## Acceptance criteria
- [x] A Stop with queued or active work and no drive nudge logs one idle_stop event, and fm doctor shows the 7-day count — verify with `python3 plugin/tests/run.py -k BoardHooks`
- [x] A UserPromptSubmit payload with permission_mode plan holds drive the way a plan-only prompt does — verify with `python3 plugin/tests/run.py -k BoardHooks`
- [x] UserPromptSubmit logs a redacted prompt event of at most 2000 chars with the permission mode, and logs none in a sensitive project — verify with `python3 plugin/tests/run.py -k BoardHooks`
- [x] The first SessionStart after Foreman's version changes prints that version's CHANGELOG bullets once, and the next one doesn't — verify with `python3 plugin/tests/run.py -k BoardHooks`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardHooks class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
<!-- auto -->
- 2026-10-15T21:55:46Z steps 3/3 done
- git: foreman/build; 4 uncommitted: MASTER.md, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, plugin/tests/test_board_hooks.py
- touched since last checkpoint: plugin/tests/test_board_hooks.py, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/hooksfix.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, MASTER.md
## Docs impact
MASTER, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_board_hooks` → exit 0 · Ran 5 tests in 1.5s (2 classes, 16 at a time; slowest: BoardHooks 1s, WhatsNew 0s) / OK [ran] [tree 4019332ba7b0] (2026-10-15T21:54:59Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_board_hooks test_doctor test_scout` → exit 0 · Ran 211 tests in 31.5s (39 classes, 16 at a time; slowest: Stop 31s, Command 25s, Scout 19s) / OK [ran] [tree 4019332ba7b0] (2026-10-15T21:55:31Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 31 tests in 1.1s (10 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree 4019332ba7b0] (2026-10-15T21:55:32Z)
- (step 2) `python3 plugin/tests/run.py test_board_hooks test_hooks test_doctor` → exit 0 · Ran 198 tests in 31.6s (37 classes, 16 at a time; slowest: Stop 32s, Command 25s, PreToolUse 17s) / OK [ran] [tree b466ff2b8a29] (2026-10-15T22:03:07Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardHooks` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: BoardHooks 1s) / OK [ran] [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardHooks` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: BoardHooks 1s) / OK [ran] [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardHooks` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: BoardHooks 1s) / OK [ran] [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
- (ac 4) `python3 plugin/tests/run.py -k BoardHooks` → exit 0 · Ran 3 tests in 1.5s (1 classes, 16 at a time; slowest: BoardHooks 1s) / OK [ran] [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
- (audit intent) `one fm-reviewer pass (sonnet): 2 medium, 3 low; all fixed test-first (the waiting-stop bug reproduced first)` → idle stops counted, plan mode holds drive, prompts logged redacted, what's new shown once per upgrade [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
- (audit edge) `one fm-reviewer pass (sonnet): 2 medium, 3 low; all fixed test-first (the waiting-stop bug reproduced first)` → background waits and reloads aren't idle; a copy without CHANGELOG keeps the note for later; headless runs never use it up [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
- (audit adversary) `one fm-reviewer pass (sonnet): 2 medium, 3 low; all fixed test-first (the waiting-stop bug reproduced first)` → prompts are redacted before the 2000-char cut and never logged in a sensitive project [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
- (audit operator) `one fm-reviewer pass (sonnet): 2 medium, 3 low; all fixed test-first (the waiting-stop bug reproduced first)` → one ledger append per stop with open work and per prompt; doctor prefilters bytes [tree b466ff2b8a29] (2026-10-15T22:03:09Z)
## Log
- 2026-10-15T21:12:43Z created
- 2026-10-15T21:30:35Z grounding: plan-only hold at fmhooks.py:578 (hold = c.is_plan_only(text)) → hold = c.is_plan_only(text) or pl.get('permission_mode') == 'plan'; idle_stop event in stop() where no drive reason is given though queue/active exist; prompt event (c.redact, fit 2000, permission_mode) in UserPromptSubmit unless meta sensitive; SessionStart compares meta 'seen_version' to the plugin version and prints that version's CHANGELOG bullets once. Touches the Stop path T-0950 just changed: main thread, after T-0950 commits.
- 2026-10-15T21:40:41Z focused
- 2026-10-15T21:41:34Z paused: focus moved to T-0954
- 2026-10-15T21:50:53Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T21:50:53Z focused
- 2026-10-15T21:55:47Z paused: focus moved to T-0955
- 2026-10-15T22:00:41Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T22:00:41Z focused
- 2026-10-15T22:03:10Z done
- 2026-10-15T22:03:10Z committed 9349f19 (3 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- research T-0318-surfaces: 1. **Answer.** Foreman has a per-project JSON view model (`fm ui --json`) and a read-only MCP server. The only cross-project data are a hand-re…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- decision 2026-10-15: T-0950: no board-leftover probe
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
## Lessons
- Record 'seen' only after the thing was actually shown, or a missing input silently burns the one-time note
## Files touched
- plugin/tests/test_board_hooks.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- MASTER.md
- CHANGELOG.md
