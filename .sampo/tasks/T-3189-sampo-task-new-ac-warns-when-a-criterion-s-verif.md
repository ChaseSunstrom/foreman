---
id: T-3189
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T10:01:20Z
updated: 2026-11-05T15:04:44Z
builder_model: haiku
base: 0a1f4fbaf468bf79b653a59b92600b1b5b9a6991
base_tree: 12d413512b97e0c7fdc604940d46b789eda8e0f2
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T10:08:21Z
plan0_scope: []
builder_returned: 2026-11-05T10:11:15Z
lane_stop: refused 2026-11-05T14:55:54Z
postmerge_red: test_board_verbs.BoardVerbs, test_tool_taint.ToolTaint
postmerge_sha: 1c691625f3060f92cb864860e608ae39cb249cd5
verified: strong
unproven: [data]
---
# sampo task new and task ac warn when a criterion's verify command can't run in a fresh lane: a cd into a folder then npx/npm/yarn with no committed package.json or lockfile there, a run.py target that matches no test, or a program not on PATH
## Raw request
> sampo task new/ac warns when a criterion's verify command can't run in a fresh lane: a cd into a folder with npx/npm/yarn and no committed package.json or lockfile, a run.py name that matches no test (T-3186), or a tool not on PATH; T-3113's npx vitest criterion passed only in its builder's lane (untracked node_modules) and failed at merge
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] adding a criterion whose verify is 'cd mods/x && npx vitest run' (no committed package.json there), 'python3 plugin/tests/run.py test_nope', or 'nosuchtool --x' prints a warning naming why it can't run in a fresh lane; a runnable verify prints none — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests then the warnings
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 151 tests in 29.8s (46 classes, 16 at a time; slowest: TaskLifecycle 29s, CaptureAndIntake 15s, StateViews 14s) / OK [ran] [tree 6f7700b8ff5a] [world 2f1906870a] (2026-11-05T10:10:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_doctor test_left_out test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [13.82s] [ran] [tree 6f7700b8ff5a] [world 2f1906870a] (2026-11-05T10:11:09Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_board_verbs test_tool_taint` → exit 0 · Ran 169 tests in 22.6s (159 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 22s, BoardVerbs.test_round_close_lists_the_newest_20_and_counts_the_rest 10s, BoardVerbs.test_release_check [ran] [tree 1a6b7bff6b74] [world 2f1906870a] (2026-11-05T15:02:31Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 152 tests in 63.6s (46 jobs, 16 at a time; slowest: TaskLifecycle 60s, CaptureAndIntake 33s, StateViews 22s) / FAILED (2 classes: test_cli.HelpRegistrations, test_cli.VerifyFreshLane) (start tree + this task's tests) [ran] [tree 0f6dc2ab407f] [world 2f1906870a] (2026-11-05T15:04:17Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 152 tests in 16.5s (140 jobs, 16 at a time; slowest: StateViews.test_state_md_is_bounded 16s, TaskLifecycle.test_next_agrees_with_the_done_gate_after_evidence_only_updates 6s, AffectedPairs.test_o [ran] [tree 0f6dc2ab407f] [world 2f1906870a] (2026-11-05T15:04:17Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T15:04:17Z [ran] [tree 0f6dc2ab407f] [world 2f1906870a] (2026-11-05T15:04:24Z)
- (audit edge) `re-landed after a false revert: its post-merge verify judged a tree still holding T-3160 (reverted 17 min earlier) and blamed T-3189 for T-3160's BoardVerbs/ToolTaint failures; re-applied on today's main by sampo edit from its own diff (core.py and test_cli.py now equal its merged tree), test_cli test_board_verbs test_tool_taint 169 OK, proved red→green; T-3213 captured for the misattribution` → a cd then npx/npm/yarn with no committed package.json or lockfile there warns; a run.py target that matches no test warns; a program not on PATH warns; a plain verify command stays quiet [tree 0f6dc2ab407f] (2026-11-05T15:04:24Z)
- (audit adversary) `re-landed after a false revert: its post-merge verify judged a tree still holding T-3160 (reverted 17 min earlier) and blamed T-3189 for T-3160's BoardVerbs/ToolTaint failures; re-applied on today's main by sampo edit from its own diff (core.py and test_cli.py now equal its merged tree), test_cli test_board_verbs test_tool_taint 169 OK, proved red→green; T-3213 captured for the misattribution` → the check only reads the verify command's text and the repo's tracked files to warn; it runs nothing and blocks nothing, so a hostile command string can at most print a warning; the card files the gate names are T-3160's, merged and reverted within this task's window, not on disk now [tree 0f6dc2ab407f] (2026-11-05T15:04:24Z)
- (audit self) `re-landed after a false revert: its post-merge verify judged a tree still holding T-3160 (reverted 17 min earlier) and blamed T-3189 for T-3160's BoardVerbs/ToolTaint failures; re-applied on today's main by sampo edit from its own diff (core.py and test_cli.py now equal its merged tree), test_cli test_board_verbs test_tool_taint 169 OK, proved red→green; T-3213 captured for the misattribution` → no findings [tree 0f6dc2ab407f] (2026-11-05T15:04:24Z)
- (audit edge) `re-landed after a false revert: its post-merge verify judged a tree still holding T-3160 (reverted 17 min earlier) and blamed T-3189 for T-3160's BoardVerbs/ToolTaint failures; re-applied on today's main by sampo edit from its own diff (core.py and test_cli.py now equal its merged tree), test_cli test_board_verbs test_tool_taint 169 OK, proved red→green; T-3213 captured for the misattribution` → a cd then npx/npm/yarn with no committed package.json or lockfile there warns; a run.py target that matches no test warns; a program not on PATH warns; a plain verify command stays quiet [tree 0f6dc2ab407f] (2026-11-05T15:04:38Z)
- (audit adversary) `re-landed after a false revert: its post-merge verify judged a tree still holding T-3160 (reverted 17 min earlier) and blamed T-3189 for T-3160's BoardVerbs/ToolTaint failures; re-applied on today's main by sampo edit from its own diff (core.py and test_cli.py now equal its merged tree), test_cli test_board_verbs test_tool_taint 169 OK, proved red→green; T-3213 captured for the misattribution` → the check only reads the verify command's text and the repo's tracked files to warn; it runs nothing and blocks nothing, so a hostile command string can at most print a warning; the card files the gate names are T-3160's, merged and reverted within this task's window, not on disk now [tree 0f6dc2ab407f] (2026-11-05T15:04:38Z)
- (audit self) `re-landed after a false revert: its post-merge verify judged a tree still holding T-3160 (reverted 17 min earlier) and blamed T-3189 for T-3160's BoardVerbs/ToolTaint failures; re-applied on today's main by sampo edit from its own diff (core.py and test_cli.py now equal its merged tree), test_cli test_board_verbs test_tool_taint 169 OK, proved red→green; T-3213 captured for the misattribution` → no findings [tree 0f6dc2ab407f] (2026-11-05T15:04:38Z)
## Log
- 2026-11-05T10:01:20Z created
- 2026-11-05T10:08:06Z planned from capture
- 2026-11-05T10:08:10Z set approved=True
- 2026-11-05T10:08:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3189.builder.md
- 2026-11-05T10:08:20Z focused
- 2026-11-05T10:08:21Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T14:28:49Z merged worktree-agent-ab518560f3a7aba39 (2 file(s))
- 2026-11-05T14:28:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab518560f3a7aba39
- 2026-11-05T14:55:54Z red after merge: test_board_verbs.BoardVerbs, test_tool_taint.ToolTaint; 1c691625f reverted
- 2026-11-05T15:00:14Z focused
- 2026-11-05T15:04:39Z affected tests waived: the failing names are test_callcards, test_self_aware and test_smith_cards: modules of T-3160/T-3126, merged then reverted inside this task's window and not on disk; T-3189's own tests (test_cli 152, 
- 2026-11-05T15:04:40Z done
- 2026-11-05T15:04:44Z committed af8b9891 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Mobile build failures: Xcode, Expo, Flutter (fm playbooks show build/mobile-build)
- research T-2049-review: Changes needed. The lint logic is sound and the AC-named test looks right. One MEDIUM finding is on the card-admission path. I had no shell, so I…
- T-3143 [FIX S, active, 1 steps] Briefs, criteria templates and playbooks name 'claude plugin test mods/foreman-ui' for the UI mod, never 'cd mods/foreman-ui && npx vites…
- decision 2026-10-31: Narrow the code freeze during the long-tier runs: lanes off the session path (T-2294 builder doc, T-2156 ci-watch, T-2279 doctor, T-2296 friction di…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/core.py
- CHANGELOG.md
- MASTER.md
- docs/map/files-lib-3.md
- plugin/cards/_lib/cardkit.py
- plugin/cards/failing-frame/card.json
- plugin/cards/failing-frame/check.py
- plugin/cards/failing-frame/gen.py
- plugin/cards/failing-frame/harness.py
- plugin/cards/failing-frame/tests.json
- plugin/cards/py-callers/card.json
- plugin/cards/py-callers/check.py
- plugin/cards/py-callers/gen.py
- plugin/cards/py-callers/tests.json
- plugin/cards/py-none-guard/card.json
- plugin/cards/py-none-guard/check.py
- plugin/cards/py-none-guard/gen.py
- plugin/cards/py-none-guard/tests.json
- plugin/cards/py-outline/card.json
- plugin/cards/py-outline/check.py
- plugin/cards/py-outline/gen.py
- plugin/cards/py-outline/tests.json
- plugin/lib/fmcallcards.py
- plugin/lib/fmselfaware.py
- plugin/lib/sampo/callcards.py
- plugin/lib/sampo/landlock.py
- plugin/lib/sampo/selfaware.py
- plugin/lib/sampo/smith.py
- plugin/tests/test_callcards.py
