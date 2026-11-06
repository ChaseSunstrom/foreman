---
id: T-1796
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-27T22:29:30Z
updated: 2026-10-27T22:33:05Z
base: 06d0deef98d97282c5e1bb8e5204751236bbf562
base_tree: a78f611d12e87dd811f76ee8a48c26a804a78f6f
plan0_at: 2026-10-27T22:29:31Z
plan0_scope: []
verified: strong
---
# Cut Foreman's usage burn: compact at 200k, builders on Sonnet, watchdog for headless runs
## Raw request
> Cut Foreman's usage burn: compact at 200k, builders on Sonnet, watchdog for headless runs
## Interpretation
Usage burns because the main sessions re-read ~350-380k tokens of context on every reply (1M window; CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 compacts only near 700k; last 7 days: main sessions 750M input-equivalent, 4570 of 7140 Foreman replies over 300k) and M builder lanes keep Opus (161 runs, 234M, 22% of all). Same work, fewer tokens; no new throttling (the user's 75% rule stands).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm setup adds CLAUDE_CODE_AUTO_COMPACT_WINDOW=200k and every builder lane runs on Sonnet — verify with `python3 plugin/tests/run.py test_setup test_lanes`
## Non-goals
## Approach (options → choice → why)
Options: (a) lower the percent override (tied to whatever window the model has, brittle); (b) CLAUDE_CODE_AUTO_COMPACT_WINDOW=200k, an absolute window, so the 70% override compacts near 140k; (c) pause drive by pace (contradicts 'budgets bite from 75%'); (d) clear context between tasks (no CC hook can). Chosen (b), plus every builder on Sonnet (the main thread still reviews) with autoCompactWindow in its frontmatter (CC 2.1.312 honors it), plus CLAUDE_CODE_RETRY_WATCHDOG for headless fm run so it waits out a usage limit and resumes after the reset.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for the compact window env and the Sonnet M builder
2. [x] fmsetup ENV, fmlanes model, fm-builder autoCompactWindow, watchdog env for fm run
3. [x] apply to the user's settings with fm setup and confirm
## Resume here
## Docs impact
CHANGELOG.md Unreleased entry; no other doc names the compact env or the builder model
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_setup test_lanes` → ✗ exit 1 · Ran 68 tests in 20.7s (14 classes, 16 at a time; slowest: Lanes 20s, Install 4s, Uninstall 2s) / FAILED (2 classes) [ran] [tree 73fee575e01d] (2026-10-27T22:30:18Z)
- (step 2) `python3 plugin/tests/run.py test_setup test_lanes` → exit 0 · Ran 68 tests in 13.0s (14 classes, 16 at a time; slowest: Lanes 13s, Install 3s, Uninstall 1s) / OK [ran] [tree cd1531416afd] (2026-10-27T22:30:49Z)
- (step 3) `python3 -c "import json,sys;e=json.load(open('~/.claude/settings.json'))['env'];sys.exit(e.get('CLAUDE_CODE_AUTO_COMPACT_WINDOW')!='200k')"` → exit 0 · (no output) [ran] [tree c9a4d5cbe682] (2026-10-27T22:31:44Z)
- (ac 1) `python3 plugin/tests/run.py test_setup test_lanes` → exit 0 · Ran 68 tests in 12.8s (14 classes, 16 at a time; slowest: Lanes 13s, Install 2s, Uninstall 1s) / OK [ran] [tree c7af71a1e20b] (2026-10-27T22:32:49Z)
- (audit intent) `self-review of a 16-line diff (economy mode, weekly usage 95%): install stays additive (a user's own window wins, uninstall reverses env_added); CC 2.1.312 parses 200k; frontmatter autoCompactWindow only lowers the window` → the burn was per-reply context (main 750M of 1055M input-equivalent in 7 days) and Opus M builders (234M); both addressed without throttling, keeping the user's 75% rule [tree c7af71a1e20b] (2026-10-27T22:32:49Z)
- (audit edge) `self-review of a 16-line diff (economy mode, weekly usage 95%): install stays additive (a user's own window wins, uninstall reverses env_added); CC 2.1.312 parses 200k; frontmatter autoCompactWindow only lowers the window` → a 200k-window model sees no change; a user who wants 1M context sets the env themselves and install leaves it; old CC ignores the unknown frontmatter key [tree c7af71a1e20b] (2026-10-27T22:32:49Z)
- (audit operator) `self-review of a 16-line diff (economy mode, weekly usage 95%): install stays additive (a user's own window wins, uninstall reverses env_added); CC 2.1.312 parses 200k; frontmatter autoCompactWindow only lowers the window` → running sessions keep their old window until restarted; CHANGELOG says so [tree c7af71a1e20b] (2026-10-27T22:32:49Z)
## Log
- 2026-10-27T22:29:30Z created
- 2026-10-27T22:29:30Z focused
- 2026-10-27T22:32:14Z scope: CHANGELOG.md for the release note; test_builder.py held the old M-builder-on-Opus assertion
- 2026-10-27T22:32:14Z steer: dropped the RETRY_WATCHDOG step: fm run already waits out a usage limit (USAGE_LIMIT, --wait) and fails over
- 2026-10-27T22:33:04Z done
- 2026-10-27T22:33:05Z committed 235932b8 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1795 [PERFORMANCE M, dropped, 3 steps] Cut Foreman's usage burn: compact at 200k, builders on Sonnet, watchdog for headless runs
- playbook Strategic Compact Skill (fm playbooks show context/strategic-compact)
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- decision 2026-10-23: Pause the feature backlog (112 FEATURE items: 77 M, 34 S, 1 L) until weekly usage is back on pace; every FIX, SECURITY, PERFORMANCE and CLEAN item i…
## Measurements
context per main reply (7 days): Foreman 384k, volt 342k, gitter 379k avg → projected ≤140k peak, ~85k avg with the 200k window; M builder lanes: 161 Opus runs, 234M input-equivalent → Sonnet
## Lessons
- Usage burn is per-reply context, not Foreman's notes: cache reads x replies dominated (3.6B tokens a week), and a 1M window with a percent override compacts far too late; set an absolute window
## Plan gaps
- failed first: step 1 failing tests for the compact window env and the Sonnet M builder
## Files touched
- plugin/tests/test_lanes.py
- plugin/tests/test_setup.py
- plugin/lib/fmlanes.py
- plugin/lib/fmsetup.py
- plugin/agents/fm-builder.md
- plugin/tests/test_builder.py
- CHANGELOG.md
