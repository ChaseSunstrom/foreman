---
id: T-3361
type: FEATURE
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/scout.py, plugin/tests/test_scout.py]
depends_on: []
source: followup
created: 2026-11-06T05:54:19Z
updated: 2026-11-06T07:05:05Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ac12cb26e76ccc047
lane_branch: worktree-agent-ac12cb26e76ccc047
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:56:50Z
plan0_scope: [plugin/lib/sampo/scout.py, plugin/tests/test_scout.py]
builder_returned: 2026-11-06T07:03:47Z
---
# Release watch fires again: scout's Claude Code probe compares latest and installed against CC_TESTED alone (auto-update made installed == latest, so nothing was ever filed while CC_TESTED sat 14 releases behind), fetches the changelog only when latest moves, and files one 'Adapt to Claude Code {v}' task per tested version with the changelog bullets since CC_TESTED
## Raw request
> Release watch fires again: scout's Claude Code probe compares latest and installed against CC_TESTED alone (auto-update made installed == latest, so nothing was ever filed while CC_TESTED sat 14 releases behind), fetches the changelog only when latest moves, and files one 'Adapt to Claude Code {v}' task per tested version with the changelog bullets since CC_TESTED
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] with latest = installed = 2.1.350 and tested 2.1.304, one task is filed listing the changelog bullets; a rerun files nothing; the changelog is fetched only when latest moves (state/cc-changelog.md, cc_changelog_seen) — verify with `python3 plugin/tests/run.py test_scout`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a stubbed latest and changelog
2. [x] probe on CC_TESTED; changelog fetch via research.fetch; one keyed task
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_scout` → ✗ exit 1 · Ran 38 tests in 218.6s (6 jobs, 16 at a time; slowest: Scout 67s, Mandate 6s, ScoutDrive 6s) / FAILED (3 classes: test_scout.ScoutProbes, test_scout.Scout, test_scout.ScoutDrive) (ran] (tree ff6d2948864f] (world 2f1906870a] (2026-11-06T06:06:45Z)
- (step 2) `python3 plugin/tests/run.py test_scout` → ✗ exit 1 · Ran 38 tests in 100.9s (12 jobs, 16 at a time; slowest: Scout.test_dry_writes_nothing_and_never_refreshes_sources 19s, Mandate 5s, Scout.test_fm_scout_dry_runs_from_the_cli 5s) / FAILED (1 classes: te (ran] (tree 54f94154f0a7] (world 2f1906870a] (2026-11-06T06:21:48Z)
- (step 1) `python3 plugin/tests/run.py test_scout.ScoutProbes` → exit 0 · Ran 10 tests in 85.4s (1 jobs, 16 at a time; slowest: ScoutProbes 1s) / OK (ran] (tree aac3de748e59] (world 2f1906870a] (2026-11-06T06:25:49Z)
- (step 2) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 38 tests in 253.2s (12 jobs, 16 at a time; slowest: Scout.test_dry_writes_nothing_and_never_refreshes_sources 14s, Mandate 4s, Scout.test_fm_scout_dry_runs_from_the_cli 3s) / OK (ran] (tree aac3de748e59] (world 2f1906870a] (2026-11-06T06:30:04Z)
- (step 2) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 40 tests in 51.0s (12 jobs, 16 at a time; slowest: Scout.test_dry_writes_nothing_and_never_refreshes_sources 11s, Scout.test_fm_scout_dry_runs_from_the_cli 3s, Mandate 3s) / OK (ran] (tree 86e54fe5bb48] (world 2f1906870a] (2026-11-06T06:59:26Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_scout test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2122 tests in 332.0s (651 jobs, 16 at a time; slowest: LeanKindGateHookDelay 84s, JudgmentKinds 69s, LeanKindGateGuardAllow 62s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree 86e54fe5bb48] (world 2f1906870a] (2026-11-06T07:05:05Z)
## Log
- 2026-11-06T05:54:19Z created
- 2026-11-06T05:56:47Z focused
- 2026-11-06T05:56:50Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1391 [FEATURE M, done, 1 steps] Upstream watch: when a pinned source's sha moves, one finding lists added, removed and ren — lesson: Ask the remote before fetching it:…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-0944 [FEATURE M, done, 4 steps] Adopt Claude Code 2.1.296–2.1.301: install it, fix subagent turn.start in the pane, re-verify hooks, move Text bold to weight, record t…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_scout.py
