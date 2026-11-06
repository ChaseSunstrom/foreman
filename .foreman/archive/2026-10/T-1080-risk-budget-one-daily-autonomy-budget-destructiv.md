---
id: T-1080
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmrisk.py, plugin/lib/fmcore.py, plugin/lib/fmbudget.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/lib/fmserve.py, plugin/lib/fmnight.py, plugin/lib/fmideas.py, plugin/tests/test_risk.py, plugin/tests/test_guard.py, plugin/tests/test_night.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T09:04:41Z
base: b5e4debe2bbcb210db2a75ba6327a0032e42d861
base_tree: b15f6fd04fab8a938077ffa0cd939a7add833e86
plan0_at: 2026-10-16T08:45:40Z
plan0_scope: [plugin/lib/fmrisk.py, plugin/lib/fmcore.py, plugin/lib/fmbudget.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/tests/test_risk.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Risk budget: one daily autonomy budget (destructive asks, reverts, failed closes) that slo
## Raw request
> FEATURE: Risk budget: one daily autonomy budget (destructive asks, reverts, failed closes) that slows autonomy when spent (wild C8)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
One daily risk budget for autonomy. Destructive asks, reverts and failed closes each spend weighted points; past the cap, autonomy slows (fmbudget.degrade gives a reason) until the ledger day rolls. fm risk shows it, and fm risk set --day N --because changes the cap with a logged reason.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm risk --json` reports spent, cap and slowed, and the slowing rises once the cap is reached — verify with `python3 plugin/tests/run.py test_risk`
- [x] when spent, `degrade()` returns a reason and `fm risk set --day N --because` changes the cap — verify with `python3 plugin/tests/run.py test_risk`
- [x] past the cap, effective autonomy steps down one notch (full→standard, standard→slow) and fm next / fm risk say why; the next ledger day restores it — verify with `python3 plugin/tests/run.py test_risk`
- [x] fm risk set is user-only through the guard (Claude can't move its own brake) — verify with `python3 plugin/tests/run.py test_risk test_guard`
## Non-goals
## Approach (options → choice → why)
fmrisk.py sums weighted ledger events for today; degrade() consults slow(). The cap and its changes are kept in meta with the reason. Options considered: a hard stop (too blunt), or per-category caps (more knobs than value).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: log 3 weighted events, set a cap of 2, and `fm risk` shows "slowed". `fmbudget.degrade()` is non-empty. The ledger-day boundary resets the count.
2. [x] Create `plugin/lib/fmrisk.py` and a lazy `risk` command in `fmcli.py`.
3. [x] Hook `slow()` into `degrade()` in `fmbudget.py`.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_risk` → ✗ exit 1 · Ran 5 tests in 2.5s (1 classes, 16 at a time; slowest: Risk 2s) / FAILED (1 classes) [ran] [tree 85d723aabd73] (2026-10-16T08:46:31Z)
- (step 2) `python3 plugin/tests/run.py test_risk test_guard test_core test_serve test_outcomes test_budget test_hooks test_lanes` → exit 0 · Ran 417 tests in 100.3s (101 classes, 16 at a time; slowest: Stop 100s, PreToolUse 80s, SessionStart 75s) / OK [ran] [tree 49c71e4d3ee1] (2026-10-16T08:50:16Z)
- (step 3) `python3 plugin/tests/run.py test_risk test_guard test_core test_serve test_outcomes test_budget test_hooks test_lanes test_night test_ideas test_cli` → ✗ exit 1 · Ran 558 tests in 222.6s (141 classes, 16 at a time; slowest: Stop 222s, PreToolUse 129s, TaskLifecycle 121s) / FAILED (1 classes) [ran] [tree f652a47aa134] (2026-10-16T08:59:26Z)
- (step 3) `python3 plugin/tests/run.py test_risk test_guard test_core test_serve test_outcomes test_budget test_hooks test_lanes test_night test_ideas test_cli` → exit 0 · Ran 558 tests in 47.6s (141 classes, 16 at a time; slowest: Stop 47s, TaskLifecycle 32s, PreToolUse 32s) / OK [ran] [tree c8faace65e84] (2026-10-16T09:03:19Z)
- (ac 1) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 6 tests in 2.3s (1 classes, 16 at a time; slowest: Risk 2s) / OK [ran] [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (ac 2) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 6 tests in 2.3s (1 classes, 16 at a time; slowest: Risk 2s) / OK [ran] [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (ac 3) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 6 tests in 2.3s (1 classes, 16 at a time; slowest: Risk 2s) / OK [ran] [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (ac 4) `python3 plugin/tests/run.py test_risk test_guard` → exit 0 · Ran 119 tests in 5.3s (50 classes, 16 at a time; slowest: GuardAgainstBash 5s, Risk 3s, Hook 2s) / OK [ran] [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (step 1) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 6 tests in 2.3s (1 classes, 16 at a time; slowest: Risk 2s) / OK [ran] [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (audit intent) `fm-reviewer (intent, adversary, edge, operator, maintainer): fm decide --ask read the stored autonomy and self-decided under a spent budget → effective_autonomy (tested: the ask is queued); degrade() callers passed no project, so optional work ignored risk → all 7 pass p; fm autonomy blamed plans for a risk slowdown → names the risk; the brake is not a guard (approved=true, re-tier, pause still move a task) → documented honestly. Verified clean by the reviewer: fm risk set user-only incl. 'fm risk --day 99 set', no abbreviations, meta writes are state-direct, fm autonomy full can't lift it, memo key correct` → a bad day (destructive blocks, failed closes, reverts) slows Claude a notch until tomorrow [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge, operator, maintainer): fm decide --ask read the stored autonomy and self-decided under a spent budget → effective_autonomy (tested: the ask is queued); degrade() callers passed no project, so optional work ignored risk → all 7 pass p; fm autonomy blamed plans for a risk slowdown → names the risk; the brake is not a guard (approved=true, re-tier, pause still move a task) → documented honestly. Verified clean by the reviewer: fm risk set user-only incl. 'fm risk --day 99 set', no abbreviations, meta writes are state-direct, fm autonomy full can't lift it, memo key correct` → Claude can't move its own brake (guard-tested); it isn't a guard, documented [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (audit edge) `fm-reviewer (intent, adversary, edge, operator, maintainer): fm decide --ask read the stored autonomy and self-decided under a spent budget → effective_autonomy (tested: the ask is queued); degrade() callers passed no project, so optional work ignored risk → all 7 pass p; fm autonomy blamed plans for a risk slowdown → names the risk; the brake is not a guard (approved=true, re-tier, pause still move a task) → documented honestly. Verified clean by the reviewer: fm risk set user-only incl. 'fm risk --day 99 set', no abbreviations, meta writes are state-direct, fm autonomy full can't lift it, memo key correct` → yesterday's events don't count; green closes and routine blocks cost nothing; unreadable ledger fails open (deliberate) [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (audit operator) `fm-reviewer (intent, adversary, edge, operator, maintainer): fm decide --ask read the stored autonomy and self-decided under a spent budget → effective_autonomy (tested: the ask is queued); degrade() callers passed no project, so optional work ignored risk → all 7 pass p; fm autonomy blamed plans for a risk slowdown → names the risk; the brake is not a guard (approved=true, re-tier, pause still move a task) → documented honestly. Verified clean by the reviewer: fm risk set user-only incl. 'fm risk --day 99 set', no abbreviations, meta writes are state-direct, fm autonomy full can't lift it, memo key correct` → fm risk, fm autonomy (now X: why), fm next says why [tree c8faace65e84] (2026-10-16T09:03:36Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge, operator, maintainer): fm decide --ask read the stored autonomy and self-decided under a spent budget → effective_autonomy (tested: the ask is queued); degrade() callers passed no project, so optional work ignored risk → all 7 pass p; fm autonomy blamed plans for a risk slowdown → names the risk; the brake is not a guard (approved=true, re-tier, pause still move a task) → documented honestly. Verified clean by the reviewer: fm risk set user-only incl. 'fm risk --day 99 set', no abbreviations, meta writes are state-direct, fm autonomy full can't lift it, memo key correct` → one module; every autonomy reader goes through effective_autonomy [tree c8faace65e84] (2026-10-16T09:03:36Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:01:22Z set scope=['plugin/lib/fmrisk.py', 'plugin/lib/fmbudget.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_risk.py']
- 2026-10-16T05:01:23Z set tier=L
- 2026-10-16T08:45:39Z set scope=['plugin/lib/fmrisk.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmbudget.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmguard.py', 'plugin/tests/test_risk.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T08:45:40Z focused
- 2026-10-16T08:45:44Z set approved=True
- 2026-10-16T08:51:07Z scope: CHANGELOG.md, MASTER.md — docs
- 2026-10-16T08:52:45Z paused: focus moved to T-1132
- 2026-10-16T08:52:48Z checkpoint: built and green (test_risk + 417 wider tests); waiting on the fm-reviewer pass before finish
- 2026-10-16T08:54:13Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T08:54:13Z focused
- 2026-10-16T08:54:44Z set scope=['plugin/lib/fmrisk.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmbudget.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmguard.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmserve.py', 'plugin/lib/fmnight.py', 'plugin/lib/fmideas.py', 'plugin/tests/test_risk.py', 'plugin/tests/test_guard.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:02:31Z set scope=['plugin/lib/fmrisk.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmbudget.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmguard.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmserve.py', 'plugin/lib/fmnight.py', 'plugin/lib/fmideas.py', 'plugin/tests/test_risk.py', 'plugin/tests/test_guard.py', 'plugin/tests/test_night.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:03:28Z scope: plugin/tests/test_night.py — its process-wide subprocess mock caught the risk read's git log; other commands pass through now. CHANGELOG.md, MASTER.md — docs
- 2026-10-16T09:04:40Z done
- 2026-10-16T09:04:41Z committed 4ead49e (13 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_budget.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-16): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/tests/test_guard.py; re-ground the plan against them before editing
## Build vs reuse
Reuses c.ledger_events (today's guard_block and close_affected events), c.effective_autonomy (the one place autonomy is read, already stepped down by T-1061's plan calibration), fmbudget.degrade (the optional-work brake), the guard's USER_ONLY_FM table, and git log for Revert commits. New: only fmrisk.py (sum, cap, status) and the risk command.
## Lessons
- A brake belongs where every reader of the braked value looks, and only someone other than the braked may release it
## Plan gaps
- failed first: step 1 Failing tests: log 3 weighted events, set a cap of 2, and `fm risk` shows "slowed". `fmbudget.degra…
- failed first: step 3 Hook `slow()` into `degrade()` in `fmbudget.py`.
## Files touched
- plugin/tests/test_guard.py
- plugin/tests/test_risk.py
- plugin/lib/fmrisk.py
- plugin/lib/fmbudget.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmnight.py
- plugin/lib/fmserve.py
- plugin/tests/test_night.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
