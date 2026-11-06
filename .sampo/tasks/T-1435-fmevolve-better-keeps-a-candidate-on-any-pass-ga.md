---
id: T-1435
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T21:09:22Z
updated: 2026-10-21T23:06:51Z
base: a75870bb5fd0b040a52f7188b96feb4543b54426
base_tree: 22a92920fda3db56370bafae9fc4e61068a1603e
plan0_at: 2026-10-21T22:53:34Z
plan0_scope: []
verified: strong
---
# fm evolve keeps a candidate only for a win outside the bench noise band, and a result's pass rate is read within 0..1
## Raw request
> fmevolve._better keeps a candidate on any pass gain or cost drop, even one inside the bench noise band, so evolve can adopt a noise win; and fmbench._rate trusts pass_rate without a range check (T-1260 builder)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with repeated runs, a candidate one pass ahead inside the pass band, or cheaper inside the cost band, isn't kept as better; one outside either band is; a pass_rate of 5 or -1 counts as 1 or 0 — verify with `python3 plugin/tests/run.py test_bench test_evolve`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in test_evolve (_better on fixtures with runs and attempt costs) and test_bench (_rate range), then share gate's band math as fmbench.pass_band and cost_band, use them in fmevolve._better, and clamp _rate
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_evolve.BetterOutsideNoise` → ✗ exit 1 · Ran 2 tests in 2.7s (1 classes, 16 at a time; slowest: BetterOutsideNoise 0s) / FAILED (1 classes) [ran] [tree 258ea56e8627] (2026-10-21T22:53:59Z)
- (step 1) `python3 plugin/tests/run.py test_evolve test_bench` → ✗ exit 1 · Ran 51 tests in 135.1s (15 classes, 16 at a time; slowest: Bench 134s, Judged 74s, Evolve 59s) / FAILED (5 classes) [ran] [tree 2078effc6985] (2026-10-21T22:56:49Z)
- (step 1) `python3 plugin/tests/run.py test_evolve test_bench` → exit 0 · Ran 51 tests in 97.2s (15 classes, 16 at a time; slowest: Bench 97s, Judged 44s, Evolve 33s) / OK [ran] [tree 2a662b956da0] (2026-10-21T23:01:03Z)
- (ac 1) `python3 plugin/tests/run.py test_bench test_evolve` → exit 0 · Ran 51 tests in 136.5s (15 classes, 16 at a time; slowest: Bench 136s, Judged 80s, Evolve 65s) / OK [ran] [tree a85c83409adf] (2026-10-21T23:03:39Z)
- (audit intent) `self: gate's band math moved unchanged into fmbench.pass_band and cost_band (gate's own tests pass), _better compares each gain to its band (0 without repeats, so single-run behaviour is as before), _rate clamps to 0..1; my refactor first dropped gate's 'repeated' flag, caught by test_bench and fixed (pband is None means single runs)` → a gain inside the band isn't kept, one outside is (test_evolve) [tree a85c83409adf] (2026-10-21T23:03:39Z)
- (audit edge) `self: gate's band math moved unchanged into fmbench.pass_band and cost_band (gate's own tests pass), _better compares each gain to its band (0 without repeats, so single-run behaviour is as before), _rate clamps to 0..1; my refactor first dropped gate's 'repeated' flag, caught by test_bench and fixed (pband is None means single runs)` → results without attempt costs get no cost band and keep the IMPROVED threshold alone; a bool pass_rate reads as 1 or 0 [tree a85c83409adf] (2026-10-21T23:03:39Z)
- (audit self) `self: gate's band math moved unchanged into fmbench.pass_band and cost_band (gate's own tests pass), _better compares each gain to its band (0 without repeats, so single-run behaviour is as before), _rate clamps to 0..1; my refactor first dropped gate's 'repeated' flag, caught by test_bench and fixed (pband is None means single runs)` → no findings [tree a85c83409adf] (2026-10-21T23:03:39Z)
## Log
- 2026-10-21T21:09:22Z created
- 2026-10-21T22:53:31Z planned from capture
- 2026-10-21T22:53:33Z focused
- 2026-10-21T23:06:46Z done
- 2026-10-21T23:06:51Z committed d4aa947b (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0221 [FEATURE S, done, 1 steps] Bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread,
- research T-0224-review-2: HIGH — `plugin/lib/fmevolve.py:84-113`. The two arms differ by more than the proposed edit. [stale: plugin/lib/fmevolve.py, plugin/lib/fmguard.…
- T-0222 [FEATURE S, done, 1 steps] Fm bench build --commits RANGE --verify CMD — bench cases from any repo's history (commits
- decision 2026-10-06: [revisit: after 2026-12-01] Drop T-0356: keep 'fm task new --focus' and the first edit as separate calls
- similar finished tasks took 1–1 steps
## Regression test
test_evolve.BetterOutsideNoise: a pass gain or cost drop inside the band was 'better' before (step 1 red), not after; _rate clamps 5 and -1 and reads 'x' as 0
## Why not caught
T-1260 added the band to the gate only; evolve kept its own comparison
## Lessons
- When extracting shared math from a function, grep the function for every variable the extracted block defined
## Plan gaps
- failed first: step 1 failing tests in test_evolve (_better on fixtures with runs and attempt costs) and test_bench (_rat…
## Files touched
- plugin/tests/test_evolve.py
- plugin/lib/fmbench.py
- plugin/lib/fmevolve.py
- CHANGELOG.md
