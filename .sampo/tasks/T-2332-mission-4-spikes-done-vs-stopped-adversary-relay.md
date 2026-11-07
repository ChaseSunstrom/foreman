---
id: T-2332
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:42:17Z
updated: 2026-10-31T13:53:58Z
verified: strong
---
# Mission 4 spikes: done-vs-stopped adversary, relay race, reopened-ticket miner — each gets a verdict; holes the adversary finds are fixed test-first
## Raw request
> Mission 4 spikes: done-vs-stopped adversary, relay race, reopened-ticket miner — each gets a verdict; holes the adversary finds are fixed test-first
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal verdict never reads finished on a vacuous or pipe-masked done-when, or on gates that skipped red tests — verify with `python3 plugin/tests/run.py test_goal`
- [x] a relay race over five kill points redoes and loses nothing — verify with `python3 plugin/tests/run.py test_goal -k relay_race`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Adversary: craft states that make the verdict say finished wrongly; red test each; fix in fmmandate.verdict
2. [x] Relay race: five kill points, a fresh session resumes from disk alone; count redone and lost items
3. [x] Reopened-ticket miner: commits within 30 days of a task's close touching its files; does fm goal plan's list predict them? Record the verdict
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_goal test_mandate test_hooks test_mcp` → exit 0 · Ran 284 tests in 38.4s (48 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 25s, PreToolUse 21s) / OK [ran] [tree a197c69893ba] (2026-10-31T13:43:49Z)
- (step 2) `python3 plugin/tests/run.py test_goal -k relay_race` → exit 0 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: GoalAcrossDays 2s) / OK [ran] [tree c29c0c2f146e] (2026-10-31T13:44:42Z)
- (step 3) `python3 /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/miner.py ~/.claude/foreman` → exit 0 · tasks: 1561, tasks with a follow-up fix in 30 days: 341 (21%), fix commits: 905, predicted by the standard contents list: 184 (20%) / what the fixes added beyond the task's own surfaces: {'code only': [ran] [tree c29c0c2f146e] (2026-10-31T13:45:12Z)
- (step 1) `python3 plugin/tests/run.py test_goal test_mandate` → exit 0 · Ran 34 tests in 4.5s (8 classes, 16 at a time; slowest: GoalReview 4s, GoalAcrossDays 4s, GoalEstimate 3s) / OK [ran] [tree 6719f271e558] (2026-10-31T13:53:18Z)
- (step 2) `python3 plugin/tests/run.py test_goal -k relay_race` → exit 0 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: GoalAcrossDays 2s) / OK [ran] [tree 6719f271e558] (2026-10-31T13:53:21Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 33 tests in 4.4s (7 classes, 16 at a time; slowest: GoalReview 4s, GoalAcrossDays 4s, GoalEstimate 3s) / OK [ran] [tree 6b9d0c2d88ac] (2026-10-31T13:53:37Z)
- (ac 2) `python3 plugin/tests/run.py test_goal -k relay_race` → exit 0 · Ran 1 tests in 2.0s (1 classes, 16 at a time; slowest: GoalAcrossDays 2s) / OK [ran] [tree 6b9d0c2d88ac] (2026-10-31T13:53:37Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 3 MEDIUM fixed test-first (|| true and ; true masked fallbacks now flagged in c.lint_verify; skipped red tests named; the relay race asserts the resume line at every point), 2 LOW fixed (exact 11 kill points; pipe reason preferred); the _VACUOUS ls/cat overreach noted for Mission 4's critique (safe direction: reads stopped, not finished); full suite 4886 OK` → each spike has a verdict: adversary found 6 wrong-finished states, all fixed; relay race 0 redone, 0 lost over 11 kill points; miner: 21% of tasks reworked within 30 days, standard list predicts 1 in 5 [tree 6b9d0c2d88ac] (2026-10-31T13:53:37Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 3 MEDIUM fixed test-first (|| true and ; true masked fallbacks now flagged in c.lint_verify; skipped red tests named; the relay race asserts the resume line at every point), 2 LOW fixed (exact 11 kill points; pipe reason preferred); the _VACUOUS ls/cat overreach noted for Mission 4's critique (safe direction: reads stopped, not finished); full suite 4886 OK` → true, echo ok, exit 0, :, x | cat, x || true, x; true, x || echo ok and a skipped-red gates run all read stopped (tested); exit 1 after || still counts as able to fail [tree 6b9d0c2d88ac] (2026-10-31T13:53:37Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 3 MEDIUM fixed test-first (|| true and ; true masked fallbacks now flagged in c.lint_verify; skipped red tests named; the relay race asserts the resume line at every point), 2 LOW fixed (exact 11 kill points; pipe reason preferred); the _VACUOUS ls/cat overreach noted for Mission 4's critique (safe direction: reads stopped, not finished); full suite 4886 OK` → an unrelated task's red-first tests hold the goal at stopped, named in the cause so the owner shows [tree 6b9d0c2d88ac] (2026-10-31T13:53:37Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 3 MEDIUM fixed test-first (|| true and ; true masked fallbacks now flagged in c.lint_verify; skipped red tests named; the relay race asserts the resume line at every point), 2 LOW fixed (exact 11 kill points; pipe reason preferred); the _VACUOUS ls/cat overreach noted for Mission 4's critique (safe direction: reads stopped, not finished); full suite 4886 OK` → causes name the reason (no behaviour checked, fallback, pipe, skipped tests) in one line [tree 6b9d0c2d88ac] (2026-10-31T13:53:37Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 3 MEDIUM fixed test-first (|| true and ; true masked fallbacks now flagged in c.lint_verify; skipped red tests named; the relay race asserts the resume line at every point), 2 LOW fixed (exact 11 kill points; pipe reason preferred); the _VACUOUS ls/cat overreach noted for Mission 4's critique (safe direction: reads stopped, not finished); full suite 4886 OK` → one rule in c.lint_verify serves task verifies and goal checks; substring filter on its messages noted in the review [tree 6b9d0c2d88ac] (2026-10-31T13:53:37Z)
## Log
- 2026-10-31T13:42:17Z created
- 2026-10-31T13:42:34Z approach: complete version = every crafted wrong-finished state is a red test then a verdict cause; relay race measured over 5 kill points from disk alone; miner run over git history with a recorded verdict. Options: (1) verdict causes for vacuous/pipe-masked checks and skipped red tests, via c.lint_verify [chosen: one rule, reused]; (2) refuse vacuous done-whens at fm goal item [breaks every fixture and plan --apply's shared check]; (3) run each check at item time to catch a base pass [slow per item; kept as a finding]
- 2026-10-31T13:45:12Z spike verdicts: adversary — 5 vacuous/pipe-masked done-whens and a gates run that skipped red tests each read finished; fixed (verdict causes, red→green). Relay race — 9 kill points (before work, mid-task, after a checkpoint, a dropped task replaced, the last item mid-task): 0 redone, 0 lost; held. Reopened-ticket miner (60 days, hub files excluded) — 21% of 1561 tasks got a follow-up fix to their own code within 30 days (905 fix commits); the standard contents list would have predicted 20% of them (docs/site/pane/tests the task skipped), 80% are code-only rework no contents list names; _misses' 7-day reopen signal sees none (follow-ups are new tasks). Finding for the critique: feed later fix commits on a task's files into fm goal plan's checklist
- 2026-10-31T13:47:00Z scope: plugin/lib/fmmandate.py, plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md
- 2026-10-31T13:53:21Z correction: the relay race has 11 kill points (5 direct, 6 after a close), asserted exactly; review fixes: || true / ; true masked fallbacks now flagged by c.lint_verify (_masked), skipped red tests named, the resume line asserted present at every point
- 2026-10-31T13:53:21Z scope: plugin/lib/fmcore.py (lint_verify _masked)
- 2026-10-31T13:53:58Z done
## Follow-ups captured
## Lessons
- Every done signal needs a check that can fail; lint the check where the verdict reads it, not only where it's typed
