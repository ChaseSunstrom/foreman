---
id: T-1875
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrisk.py, plugin/lib/fmhooks.py, plugin/tests/test_risk.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-29T02:40:58Z
base: df225336aa51246d370a3e8a786ac7d2dd0e639f
base_tree: 6b9ebb9acb147124510d81f29d4ad6b3028f70c2
plan0_at: 2026-10-29T02:28:22Z
plan0_scope: [plugin/lib/fmrisk.py, plugin/lib/fmhooks.py, plugin/tests/test_risk.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Fm risk lists the week's guard collisions by rule with the rewrite that passes, and Sessio
## Raw request
> FEATURE: fm risk lists the week's guard collisions by rule with the rewrite that passes, and SessionStart names a rule hit 3+ times in 7 days in one short line
> CONTEXT: forever loop round 5 ("Prime each session with the model's own top collisions", "Count self-collisions apart from real risk, and show the rewrite"). The cap and its weights stay as they are: a brake the braked can't lift.
## Interpretation
fm risk lists the last 7 days' guard blocks by rule with the guard's own rewrite, marking the ones that spend risk; SessionStart names a rule hit 3+ times in one bounded line. Report only (tier M, not L: no cap, weight or guard change).
## Assumptions (confidence)
## Acceptance criteria
- [x] collisions in fm risk (text and JSON) and a SessionStart line at 3+ hits, nothing at 2 — verify with `python3 plugin/tests/run.py test_risk`
## Non-goals
## Approach (options → choice → why)
Complete version: grouped by rule, newest detail redacted, rewrite from fmguard._hint, spends flag, JSON, a session line, no budget change. Options: (a) reuse fmfriction's events.jsonl counts — global, not per project, 30k tail; (b) a new cache file written by the guard — extra writes on every block; (c) ledger_events with the byte filter, 7 days (20 ms measured). Choice: (c). Captured: none.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test red: fm risk collisions and the SessionStart line
2. [x] collisions, collision_line, cmd_risk rows, hooks part; green
3. [x] CHANGELOG and MASTER
## Resume here
<!-- auto -->
- 2026-10-29T02:35:25Z steps 3/3 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmhooks.py, plugin/lib/fmrisk.py, plugin/tests/test_risk.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, plugin/lib/fmhooks.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/imp.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1875r.txt, plugin/lib/fmrisk.py, plugin/tests/test_risk.py
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_risk` → red as expected (exit 1) · Ran 7 tests in 5.2s (1 classes, 16 at a time; slowest: Risk 5s) / FAILED (1 classes) [ran] [tree 17bea9cf9806] (2026-10-29T02:28:28Z)
- (step 2) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 7 tests in 5.4s (1 classes, 16 at a time; slowest: Risk 5s) / OK [ran] [tree 181000a9ae3b] (2026-10-29T02:28:40Z)
- (step 3) `grep -c T-1875 CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:1 [ran] [tree 6fe360752362] (2026-10-29T02:28:41Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py, plugin/lib/fmrisk.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.3    41.2     150  [0] / SessionEnd                  35.7    40.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 6fe360752362] (2026-10-29T02:35:11Z)
- (step 2) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 7 tests in 3.2s (1 classes, 16 at a time; slowest: Risk 3s) / OK [ran] [tree f514cce4598f] (2026-10-29T02:35:19Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py, plugin/lib/fmrisk.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.1    44.5     150  [0] / SessionEnd                  34.5    40.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree f514cce4598f] (2026-10-29T02:39:40Z)
- (ac 1) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 7 tests in 3.2s (1 classes, 16 at a time; slowest: Risk 3s) / OK [ran] [tree f514cce4598f] (2026-10-29T02:40:10Z)
- (audit intent) `one fm-reviewer pass (5 lenses); 3 MEDIUM + 2 LOW fixed test-first, 1 LOW (_hint on detail[:200]) skipped: no reproducer` → rows with no hint now show what was blocked [tree f514cce4598f] (2026-10-29T02:40:10Z)
- (audit operator) `one fm-reviewer pass (5 lenses); 3 MEDIUM + 2 LOW fixed test-first, 1 LOW (_hint on detail[:200]) skipped: no reproducer` → SessionStart line capped at 240, first hint sentence only; fmguard import measured at ~12 ms [tree f514cce4598f] (2026-10-29T02:40:10Z)
- (audit maintainer) `one fm-reviewer pass (5 lenses); 3 MEDIUM + 2 LOW fixed test-first, 1 LOW (_hint on detail[:200]) skipped: no reproducer` → 7-day window and rule-less fallback tested, real rule names [tree f514cce4598f] (2026-10-29T02:40:10Z)
- (audit adversary) `one fm-reviewer pass (5 lenses); 3 MEDIUM + 2 LOW fixed test-first, 1 LOW (_hint on detail[:200]) skipped: no reproducer` → ok, detail redacted/defanged/fitted, rule from [a-z] words [tree f514cce4598f] (2026-10-29T02:40:10Z)
- (audit edge) `one fm-reviewer pass (5 lenses); 3 MEDIUM + 2 LOW fixed test-first, 1 LOW (_hint on detail[:200]) skipped: no reproducer` → ok, 2 hits stay silent, 3 speak [tree f514cce4598f] (2026-10-29T02:40:10Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-29T00:40:41Z set tier=M, scope=['plugin/lib/fmrisk.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_risk.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T00:53:52Z set status=planned
- 2026-10-29T01:18:54Z plan re-read: only CHANGELOG.md moved; drafts re-applied clean in a trial tree with all queued drafts, tests green
- 2026-10-29T02:28:20Z focused
- 2026-10-29T02:40:56Z done
- 2026-10-29T02:40:58Z committed fc8b9322 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1080 [FEATURE L, done, 3 steps] Risk budget: one daily autonomy budget (destructive asks, reverts, failed closes) that slo — lesson: A brake belongs where every reader…
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_risk.py
## Preflight
Changed in scope since this was planned (2026-10-28): CHANGELOG.md, MASTER.md, plugin/lib/fmhooks.py; re-ground the plan against them before editing
## Lessons
- A new SessionStart line has to earn its share of the 2000-char budget: cap it near 240 and keep only the first sentence of any hint
## Files touched
- plugin/tests/test_risk.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmhooks.py
- plugin/lib/fmrisk.py
