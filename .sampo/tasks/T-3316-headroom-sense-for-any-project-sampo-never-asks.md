---
id: T-3316
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/headroom.py, plugin/tests/test_headroom.py, plugin/lib/fmheadroom.py, MASTER.md, docs/map]
depends_on: []
source: user
created: 2026-11-06T04:20:48Z
updated: 2026-11-06T06:11:34Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a116c672c4b27d347
lane_branch: worktree-agent-a116c672c4b27d347
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T05:53:17Z
plan0_scope: [plugin/lib/sampo/headroom.py, plugin/tests/test_headroom.py, plugin/lib/fmheadroom.py, MASTER.md, docs/map]
---
# Headroom part 1: census of a project's fixed sets and caps, plus caps raised by hand (T-3316)
## Raw request
> Headroom sense, for any project: Sampo never asks 'do we want more than this?'. Kalevala's 26 towers are coverage.md's open rows (written once by a gen-1 seed) plus 3 fixed; nothing ever proposes a new aspect, so the set can only shrink. Same shape everywhere: missions <=8, 5 audit lenses, ideas lenses, moon areas, K slots, BUILDERS_MAX, budgets, card targets. Build a general headroom pass: (1) census of every bounded set and cap the project works with, found from code and data (constants, fixed tuples, slices, grid rows), not a hand list; (2) per set, measure binding (how often the cap is hit) and orphans (captures, steers, failures, ideas, user messages that map to no member); (3) a 'what would a complete version have that this lacks' pass against the goal, local model first; (4) when a cap binds or orphans cluster, propose growth as a task, and for Kalevala open the new tower itself (gen N chooses the tower set: births as well as keeps); (5) the turn-end self-checks (T-3123) gain 'closed set / binding cap'. Works in any repo Sampo runs in. User: 'why are you not able to recognize/come up with improvements to the framework... only 26 tower ideas... fully self aware, and again, not specific to Sampo'
## Interpretation
Reading 1: library functions census and raised, no CLI. Reading 2: also a CLI verb; ruled out, part 4 (T-3328) adds it.
## Assumptions (confidence)
## Acceptance criteria
- [ ] census(root) lists module-level UPPER_CASE ints >=2 used as caps (compared, min/max, slice bound) and UPPER tuples/lists of >=3 strings, via ast for .py and a one-line regex for other languages; raised(root) reads one git log -p -U0 over 180 days and counts how often each cap's value went up; a fixture repo's raised cap shows raised=2, its name tuple is listed, a bare TIMEOUT used only in sleep() is not — verify with `python3 plugin/tests/run.py test_headroom`
- [ ] runs in under 3 s on this repo and never in a hook — verify with `python3 plugin/tests/run.py test_headroom`
- [ ] Non-Python names and the 3 s bound: regex fallback lists a JS cap, and census+raised on this repo finish under 3 s — verify with `python3 plugin/tests/run.py test_headroom`
## Non-goals
Left out (later parts, T-3328 etc): raising caps, the CLI verb, binding and orphan measurement, the model pass, growth tasks, turn-end self-checks. Not here: 'Headroom sense, for any project: Sampo never asks do we want more than this' (the asking is part 3+); 'nothing ever proposes a new aspect, so the set can only shrink' (Kalevala towers, part 5); 'Same shape everywhere: missions <=8, 5 audit lenses, ideas lenses, moon areas' (this part only finds them); 'Works in any repo Sampo runs in.' (covered by the fixture repo); 'User: why are you not able to recognize/come up with improvements to the framework' (the motive, not a criterion).
## Approach (options → choice → why)
1) ast scan + one git log: exact, cheap; fails if non-Python repos need more than regex. 2) model reads repo: costly, unrepeatable; fails on cost. 3) hand registry: goes stale; fails as the user rejected it. 4) use what exists: ast and git are used elsewhere but no census exists; likely outcome a new module. 5) do less: census only, no raised; fails to show binding. Choice 1 (80%): exact, cheap, general.
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmexam.py; past FIXes T-1817, T-1828, T-1839, T-1865, T-1886.
## Execution prompt
## Steps
1. [x] fixture repo test, red
2. [x] census via ast plus regex fallback
3. [x] raised caps from one git log
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_headroom` → exit 0 · Ran 3 tests in 165.5s (3 jobs, 16 at a time; slowest: HeadroomTest.test_fast_on_this_repo 28s, HeadroomTest.test_raised_counts_value_increases 0s, HeadroomTest.test_census_lists_caps_and_sets_not_bare [ran] [tree b7a33b5f728d] [world 2f1906870a] (2026-11-06T06:08:19Z)
- (step 2) `python3 plugin/tests/run.py test_headroom` → exit 0 · Ran 3 tests in 64.7s (3 jobs, 16 at a time; slowest: HeadroomTest.test_fast_on_this_repo 11s, HeadroomTest.test_census_lists_caps_and_sets_not_bare_timeout 0s, HeadroomTest.test_raised_counts_value_in [ran] [tree b7a33b5f728d] [world 2f1906870a] (2026-11-06T06:09:33Z)
- (step 3) `python3 plugin/tests/run.py test_headroom` → exit 0 · Ran 3 tests in 113.3s (3 jobs, 16 at a time; slowest: HeadroomTest.test_fast_on_this_repo 8s, HeadroomTest.test_raised_counts_value_increases 0s, HeadroomTest.test_census_lists_caps_and_sets_not_bare_ [ran] [tree b7a33b5f728d] [world 2f1906870a] (2026-11-06T06:11:34Z)
## Log
- 2026-11-06T04:20:48Z created
- 2026-11-06T04:31:02Z planned from capture
- 2026-11-06T05:52:45Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_headroom`
- 2026-11-06T05:52:45Z criterion 3 text: ignore → Non-Python names and the 3 s bound: regex fallback lists a JS cap, and census+raised on this repo finish under 3 s
- 2026-11-06T05:53:15Z focused
- 2026-11-06T05:53:17Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3050 [FEATURE L, blocked, 6 steps] Kalevala: many Rune towers at once on every aspect of Sampo, overseen by Väinämöinen, and evolving its own setup
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_code.py, plug…
## Preflight
Changed in scope since this was planned (2026-11-06): docs/map/ops-1.md; re-ground the plan against them before editing
