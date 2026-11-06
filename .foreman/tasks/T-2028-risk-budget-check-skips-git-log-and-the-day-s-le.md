---
id: T-2028
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T18:40:41Z
updated: 2026-10-29T18:51:40Z
base: 95d49e8b6f881b73a65bb6699b215feb15631f59
base_tree: 991c2892cb18346eb72d5bd6995df878f2601cd0
plan0_at: 2026-10-29T18:43:35Z
plan0_scope: []
verified: strong
---
# Risk budget check skips git log and the day's ledger rescan when nothing moved
## Raw request
> Risk budget check skips git log and the day's ledger rescan when nothing moved
## Interpretation
fmrisk.status runs in every Stop, UserPromptSubmit and SessionStart process (effective_autonomy, next_action, state_dict): it rescans the day's ledger lines (2.4 ms best, today ~1,500 lines) and runs git log for reverts (1.8 ms best; 10-16 ms under load in the Stop profile). Its per-process memo can't help a new process.
## Assumptions (confidence)
## Acceptance criteria
- [x] status reuses a cached revert count while the reflog is unchanged, and counts only ledger lines appended since its last read — verify with `python3 plugin/tests/run.py test_risk`
## Non-goals
## Approach (options → choice → why)
Options: (a) a cache file with the day's counts, the ledger offset read up to (checked by the 64 bytes of the last line read, which start with its unique chain hash) and the revert count keyed by .git/logs/HEAD's size and mtime; (b) key everything on the ledger size (useless: every hook appends); (c) drop the git log (would weaken the budget: no). Chose (a): a new process reads only lines appended since, a rolled ledger fails the check and rescans, a missing reflog or cache falls back to today's full path. Written only when counts, the git key or 64 KB of offset moved, so most calls are read-only.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests: no git subprocess on a second process call with an unchanged reflog; new guard_block lines counted from the saved offset; a rolled (rewritten) ledger rescans
2. [x] Implement in fmrisk.status with a small risk.json cache in the project dir; CHANGELOG with numbers
## Resume here
<!-- auto -->
- 2026-10-29T18:44:50Z step 1/2: Red tests: no git subprocess on a second process call with an unchanged reflog; new guard_block lines counted from the saved offset; a rolled (rewritten) ledger rescans
- git: foreman/build; 1 uncommitted: plugin/tests/test_risk.py
- touched since last checkpoint: plugin/tests/test_risk.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/edit28.json
## Docs impact
CHANGELOG line added; no user-facing docs change (internal cache)
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_risk 2>&1 | grep -E "^(FAIL|ERROR):|Error:|^OK|FAILED" | head` → ✗ exit 1 · FAILED (failures=1, errors=1) / FAILED (1 classes) [ran] [tree 2f694fc788d5] (2026-10-29T18:43:47Z)
- (step 1) `python3 plugin/tests/run.py test_risk` → ✗ exit 1 · Ran 11 tests in 3.0s (1 classes, 16 at a time; slowest: Risk 3s) / FAILED (1 classes) [ran] [tree 2f694fc788d5] (2026-10-29T18:43:56Z)
- (ac 1) `python3 plugin/tests/run.py test_risk 2>&1 | tail -15` → exit 0 · Ran 11 tests in 3.0s (1 classes, 16 at a time; slowest: Risk 3s) / OK [ran] [tree 9463673e1f59] (2026-10-29T18:46:37Z)
- (step 2) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 11 tests in 3.0s (1 classes, 16 at a time; slowest: Risk 3s) / OK [ran] [tree 75a95f977da0] (2026-10-29T18:47:24Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmrisk.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.4    31.2     150  [0] / SessionEnd                  25.6    28.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree 75a95f977da0] (2026-10-29T18:51:12Z)
- (ac 1) `python3 plugin/tests/run.py test_risk` → exit 0 · Ran 11 tests in 2.9s (1 classes, 16 at a time; slowest: Risk 3s) / OK [ran] [tree 75a95f977da0] (2026-10-29T18:51:36Z)
- (audit intent) `self-review (risk budget spent: no subagents): traced status -> _counts for a fresh, unchanged, appended, rolled, broken-cache, missing-ledger and new-day case; the state dir is state-direct (never authorizable), so the cache is as guarded as the ledger` → a new hook process reads only ledger lines appended since the cached offset and runs git log only when .git/logs/HEAD moved; counts and return shape unchanged; WEIGHTS, CAP and DESTRUCTIVE untouched [tree 75a95f977da0] (2026-10-29T18:51:36Z)
- (audit edge) `self-review (risk budget spent: no subagents): traced status -> _counts for a fresh, unchanged, appended, rolled, broken-cache, missing-ledger and new-day case; the state dir is state-direct (never authorizable), so the cache is as guarded as the ledger` → a rolled ledger fails the 64-byte mark (unique chain hash) and rescans; a half-written last line is left for the next read; a broken or non-dict cache or another day counts afresh; a worktree (.git file) has no reflog key so git log runs each time; concurrent writers are atomic, last wins with a self-consistent snapshot [tree 75a95f977da0] (2026-10-29T18:51:36Z)
## Log
- 2026-10-29T18:40:41Z created
- 2026-10-29T18:43:34Z focused
- 2026-10-29T18:51:38Z done
- 2026-10-29T18:51:40Z committed 4d76875b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- research brainstorm-pass-1: Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, …
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- decision 2026-10-23: fm code's spend counts toward fm budget's day cap like any other Foreman spend
- the similar finished task took 2 steps
## Measurements
fmrisk.status in Stop (profiled) 9-10 ms -> <0.5 ms; Stop hook median 60 -> 55 ms; UserPromptSubmit 98 -> 92 ms (hook_t, 15 runs, same state)
## Lessons
- A per-process memo doesn't help hooks: each event is a new process. Persist the scan's offset with a content mark of the last line read, so an in-place rewrite fails the check instead of returning stale counts.
## Plan gaps
- failed first: step 1 Red tests: no git subprocess on a second process call with an unchanged reflog; new guard_block lin…
## Files touched
- plugin/tests/test_risk.py
- plugin/lib/fmrisk.py
- CHANGELOG.md
