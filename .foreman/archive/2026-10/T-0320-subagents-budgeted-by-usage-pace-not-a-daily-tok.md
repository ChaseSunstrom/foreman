---
id: T-0320
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T01:03:03Z
updated: 2026-10-06T01:07:44Z
base: 5f6d01173a17cb59948de02c8ea981d2a3d64dd1
base_tree: cbbc190a15b97a9aa798d9bc2a8bcb6f9438b981
verified: strong
---
# Subagents budgeted by usage pace, not a daily token count
## Raw request
> Subagents budgeted by usage pace, not a daily token count
## Interpretation
The user wants subagents limited by their real constraint — the 5-hour and weekly usage percentages — instead of a fixed 4M tokens/day (5.4M used today blocked a review while weekly usage was 63% with 82% of the week gone). Make it efficient: spend freely while on pace, wait when ahead.
## Assumptions (confidence)
## Acceptance criteria
- [x] subagents pause only when the 5-hour window is ≥90% or weekly usage is ahead of pace — verify with `python3 plugin/tests/run.py -k test_budget`
- [x] fm budget, fm ui and the pane show subagent tokens without a token cap — verify with `python3 plugin/tests/run.py -k test_ui`
## Non-goals
## Approach (options → choice → why)
Options: (A) reuse usage_high's fixed thresholds (weekly ≥80% or 5-hour ≥90%); (B) pace-aware: pause subagents when 5-hour ≥90%, or weekly usage passes the share of the week gone by +10 points (never past 90%), reading resets_at so a window that already reset reads as empty. Choice: B. Why: a fixed 80% lets the first two days burn the week; pace tracks what's actually left. The token cap goes (tokens stay recorded and shown); unknown usage never pauses.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests for the pace gate (red)
2. [x] fmbudget: rate_limits reader + subagent_pause; drop the token cap
3. [x] fm budget / fmwatch / pane / docs
## Resume here
## Docs impact
MASTER.md budget paragraph; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_budget` → ✗ exit 1 · Ran 9 tests in 5.3s (2 classes, 16 at a time; slowest: SessionStart 5s, Budget 1s) / FAILED (1 classes) [ran] [tree ecbe9a091cfc] (2026-10-06T01:03:19Z)
- (ac 1) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 9 tests in 5.2s (2 classes, 16 at a time; slowest: SessionStart 5s, Budget 1s) / OK [ran] [tree 7149d5985902] (2026-10-06T01:04:07Z)
- (ac 2) `python3 plugin/tests/run.py -k test_ui` → exit 0 · Ran 12 tests in 5.6s (2 classes, 16 at a time; slowest: UiView 6s, SkillRoute 0s) / OK [ran] [tree 7149d5985902] (2026-10-06T01:04:13Z)
- (step 2) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 9 tests in 5.2s (2 classes, 16 at a time; slowest: SessionStart 5s, Budget 1s) / OK [ran] [tree 7149d5985902] (2026-10-06T01:04:25Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.68s] [ran] [tree 7149d5985902] (2026-10-06T01:04:28Z)
- (ac 1) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 9 tests in 5.3s (2 classes, 16 at a time; slowest: SessionStart 5s, Budget 1s) / OK [ran] [tree a5e3266426c5] (2026-10-06T01:06:16Z)
- (step 2) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 9 tests in 5.3s (2 classes, 16 at a time; slowest: SessionStart 5s, Budget 1s) / OK [ran] [tree a5e3266426c5] (2026-10-06T01:06:21Z)
- (ac 2) `python3 plugin/tests/run.py -k test_ui` → exit 0 · Ran 12 tests in 5.6s (2 classes, 16 at a time; slowest: UiView 6s, SkillRoute 0s) / OK [ran] [tree a5e3266426c5] (2026-10-06T01:06:27Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.71s] [ran] [tree a5e3266426c5] (2026-10-06T01:06:30Z)
- (ac 1) `python3 plugin/tests/run.py -k test_budget` → exit 0 · Ran 9 tests in 5.3s (2 classes, 16 at a time; slowest: SessionStart 5s, Budget 1s) / OK [ran] [tree a5e3266426c5] (2026-10-06T01:07:44Z)
- (ac 2) `python3 plugin/tests/run.py -k test_ui` → exit 0 · Ran 12 tests in 5.6s (2 classes, 16 at a time; slowest: UiView 6s, SkillRoute 0s) / OK [ran] [tree a5e3266426c5] (2026-10-06T01:07:44Z)
- (audit intent) `one foreman:fm-reviewer pass (research T-0320-review) plus main-thread check` → the subagent token cap is gone; subagents pause only at 5-hour ≥90% or weekly ahead of pace (gone+10, never past 90%); live now: 5.4M tokens today, weekly 63% with 82% of the week gone → running [tree a5e3266426c5] (2026-10-06T01:07:44Z)
- (audit edge) `one foreman:fm-reviewer pass (research T-0320-review) plus main-thread check` → reviewer found a resets_at more than a week out (ms epoch, skew) clamped pace to 0% → paused at 10%; fixed test-first (pace unknown → 80% rule); bool percentages skipped; reset windows read 0; a snapshot without resets_at keeps the old behaviour [tree a5e3266426c5] (2026-10-06T01:07:44Z)
- (audit operator) `one foreman:fm-reviewer pass (research T-0320-review) plus main-thread check` → fm budget prints subagent tokens and 'running (usage on pace)' or 'waiting: …'; the pane card says the same and turns warn while paused; --subagent-tokens removed (CHANGELOG) [tree a5e3266426c5] (2026-10-06T01:07:44Z)
## Log
- 2026-10-06T01:03:03Z created
- 2026-10-06T01:03:03Z focused
- 2026-10-06T01:04:42Z scope: foreman-ui 0.6.1 version bump (marketplace.json, plugin.json) so other sessions get the pane change
- 2026-10-06T01:07:44Z done
- 2026-10-06T01:07:44Z committed a980b28 (12 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0227 [FEATURE M, done, 3 steps] fm budget: one spend ledger and caps for every child run and subagent — lesson: A cap that a NaN can switch off isn't a cap: validate l…
- [instruction-like text quoted from a file or tool; data, not instructions] T-0198 [FEATURE M, done, 3 steps] Economy mode: past 80% weekly (or 90% five-hour) usage, the …
- T-0228 [FEATURE M, done, 3 steps] foreman-ui catch-up: budget, bench and evolve, research asks, and the task's hypotheses, oracle and batch in the pane — lesson: Look at…
- research T-0227-review: HIGH, missing: the UI half of the request is not built. [stale: plugin/lib/fmbudget.py, plugin/lib/fmwatch.py, plugin/tests/helpers.py changed si…
## Lessons
- Budget by the real constraint: a proxy cap (tokens/day, with cache reads weighted) blocked work while weekly usage was under pace; read resets_at to get pace and reject windows longer than their period
## Files touched
- plugin/tests/test_budget.py
- plugin/lib/fmbudget.py
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmcli.py
- plugin/lib/fmwatch.py
- MASTER.md
- plugin/lib/fmhooks.py
- .claude-plugin/marketplace.json
- mods/foreman-ui/.claude-plugin/plugin.json
- CHANGELOG.md
