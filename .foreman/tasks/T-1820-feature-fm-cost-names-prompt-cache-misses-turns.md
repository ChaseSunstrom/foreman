---
id: T-1820
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:13:24Z
updated: 2026-10-28T08:38:03Z
base: 6cb1c5b221d215d8099db9568f0a3f4a45303b83
base_tree: 69ef25bed2ab5dbfbc44078476d87f8f5256decf
plan0_at: 2026-10-28T08:24:56Z
plan0_scope: []
verified: strong
---
# fm cost judges each cache bust by the session's own cache TTL (1 h when the transcript's cache_creation shows ephemeral_1h, else 5 min) and names each bust's cost
## Raw request
> FEATURE: fm cost names prompt-cache misses: turns that rewrote the whole cache after a gap past its TTL, each with its cost and what to change (from the T-1798 brainstorm)
## Interpretation
fm cost prices every cache write at 1.25× and labels a bust 'ttl' only after 5 min idle. Sessions on the 1-hour cache (cache_creation.ephemeral_1h_input_tokens > 0, this user's) pay 2× per write and keep the cache an hour, so every input-equivalent figure (fm cost, fm digest, fm budget, fm serve) runs ~9% low and 5–60 min gaps are mislabelled 'ttl'. Each bust's cost is also unnamed.
## Assumptions (confidence)
## Acceptance criteria
- [x] 1h cache writes weigh 2× everywhere input-equivalent is summed; a 1h session's 10-min-gap bust is a context edit; each session names its busts' cost — verify with `python3 plugin/tests/run.py -k SessionCost -k test_cost_labels_each_cache_bust`
## Non-goals
## Approach (options → choice → why)
One fmcost.weighted(u) prices a usage row (1h write tokens at 2.0, the rest as WEIGHTS) and every summing site uses it; fmbudget drops its duplicate WEIGHTS. _sessions takes each row's TTL from its cache_creation (3600 s when it shows 1h writes, else 300 s) and adds bust_cost: the re-written tokens' price minus what reading them would have cost. Rejected: a per-session TTL flag (rows already carry it), a config knob for prices (they change with Anthropic's price list, not per user).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: 1h weight, 1h-TTL label, bust cost
2. [x] fmcost.weighted + per-row TTL + bust_cost; fmbudget/fmserve use weighted
3. [x] CHANGELOG, gates, finish
## Resume here
<!-- auto -->
- 2026-10-28T08:33:59Z step 1/3: Failing tests: 1h weight, 1h-TTL label, bust cost
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmbudget.py, plugin/lib/fmcost.py, plugin/lib/fmserve.py, plugin/tests/test_economics.py
- touched since last checkpoint: plugin/lib/fmbudget.py, plugin/lib/fmserve.py, plugin/lib/fmcost.py, plugin/tests/test_economics.py, CHANGELOG.md
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_one_hour_cache_writes` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: SessionCost 0s) / FAILED (1 classes) [ran] [tree b27cfa4fc9e5] (2026-10-28T08:25:18Z)
- (step 2) `python3 plugin/tests/run.py test_economics test_cost test_cost_forecast test_perf_cost test_serve test_ideas test_budget` → exit 0 · Ran 100 tests in 17.9s (27 classes, 16 at a time; slowest: Run 18s, Ideas 9s, SessionStart 8s) / OK [ran] [tree 8cca4b5b8b92] (2026-10-28T08:26:44Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmbudget.py, plugin/lib/fmcost.py, plugin/lib/fmserve.py — commit it through a task, or git checkout it back / fm doc; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.5    41.7     150  [0] / SessionEnd                  35.0    41.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 5dc930ce32e5] (2026-10-28T08:30:38Z)
- (audit intent) `fm-reviewer` → no 'what to change' hint and no unit on bust cost: both fixed (cause hint line, '≈ N lost') [tree 2544579e8da9] (2026-10-28T08:32:48Z)
- (audit edge) `fm-reviewer` → TTL now from the session's last cache write (5m→1h switch reads right); over-1h gap → ttl tested [tree 2544579e8da9] (2026-10-28T08:32:48Z)
- (audit adversary) `fm-reviewer` → local transcript JSON only; non-numeric field fails as before [tree 2544579e8da9] (2026-10-28T08:32:48Z)
- (audit operator) `fm-reviewer` → fmbudget imports fmcost lazily, no cycle; one dict lookup per row [tree 2544579e8da9] (2026-10-28T08:32:48Z)
- (audit maintainer) `fm-reviewer` → one weighted() helper replaces 6 duplicated sums and fmbudget's WEIGHTS copy [tree 2544579e8da9] (2026-10-28T08:32:49Z)
- (step 3) `python3 plugin/tests/run.py test_budget test_cost test_cost_forecast test_economics test_perf_cost test_serve test_ideas` → exit 0 · Ran 100 tests in 18.1s (27 classes, 16 at a time; slowest: Run 18s, Ideas 9s, SessionStart 8s) / OK [ran] [tree 2544579e8da9] (2026-10-28T08:33:07Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmbudget.py, plugin/lib/fmcost.py, plugin/lib/fmserve.py — commit it through a task, or git checkout it back / fm doc; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.2    43.0     150  [0] / SessionEnd                  34.8    37.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 0ef284b04864] (2026-10-28T08:37:03Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_economics` → exit 0 · Ran 5 tests in 1.324s / OK [ran] [tree 0ef284b04864] (2026-10-28T08:37:35Z)
- (ac 1) `python3 plugin/tests/run.py -k SessionCost -k test_cost_labels_each_cache_bust` → exit 0 · Ran 5 tests in 1.2s (2 classes, 16 at a time; slowest: SessionCost 1s, BoardIdeas 0s) / OK [ran] [tree 0ef284b04864] (2026-10-28T08:37:37Z)
- (audit intent) `fm-reviewer pass; 4 findings fixed (bust hint, ≈ lost unit, ttl from the last cache-writing row, a >1 h gap row); 1 low-risk left (budget/serve 1 h rows untested, both route through weighted())` → fm cost now matches what Anthropic bills for 1 h-cache sessions (this session: 13.0M, was 11.7M) and says what a bust cost [tree 0ef284b04864] (2026-10-28T08:37:37Z)
- (audit edge) `fm-reviewer pass; 4 findings fixed (bust hint, ≈ lost unit, ttl from the last cache-writing row, a >1 h gap row); 1 low-risk left (budget/serve 1 h rows untested, both route through weighted())` → a 74-min gap on the 1 h cache is a ttl bust, a 10-min one a context edit; sessions without cache_creation price as before [tree 0ef284b04864] (2026-10-28T08:37:37Z)
## Log
- 2026-10-28T08:13:24Z created
- 2026-10-28T08:14:32Z set title=fm cost judges each cache bust by the session's own cache TTL (1 h when the transcript's cache_creation shows ephemeral_1h, else 5 min) and names each bust's cost
- 2026-10-28T08:14:54Z set status=planned
- 2026-10-28T08:24:54Z set tier=M
- 2026-10-28T08:24:55Z focused
- 2026-10-28T08:38:01Z done
- 2026-10-28T08:38:03Z committed c81cc8e6 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0703 [FEATURE M, done, 4 steps] Frontier 03 — Model routing, effort and cache economics — lesson: Context per turn, not output, drives spend here: thresholds for compa…
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- T-0959 [FEATURE M, done, 3 steps] Brainstorm and cost: keep a child's partial answer, a run manifest, cache-bust causes, friction minutes, unused verbs — lesson: A repor…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
## Lessons
- 1 h-TTL sessions: price writes at 2× and judge a ttl bust by the last write's lifetime, not the bust row's
## Plan gaps
- failed first: step 1 Failing tests: 1h weight, 1h-TTL label, bust cost
## Files touched
- plugin/tests/test_economics.py
- plugin/lib/fmbudget.py
- plugin/lib/fmcost.py
- plugin/lib/fmserve.py
- CHANGELOG.md
