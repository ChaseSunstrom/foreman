---
id: T-1260
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-20T14:01:25Z
updated: 2026-10-21T21:31:05Z
group: bench rigor and reporting
base: 06253578b4b3a02c6ab97d393f8379903beb0f3c
base_tree: ccc07cb8afdaa6e4d5831c89e5a339e164b4a169
plan0_at: 2026-10-21T20:46:20Z
plan0_scope: []
verified: strong
---
# fm bench's gate shows each delta with its noise band from repeated runs, and calls a change inside it noise, not a win or a loss
## Raw request
> Bench rigor: noise bands before a delta is published, hook-feature ablation in the duel, an equal-dollar-cap duel, a false-done benchmark on impossible tasks (brainstorm-20261020 C5)
## Interpretation
A bench delta (passes, cost per case) is published as if exact, though one run of a case can flip. With --runs N the attempts give a spread: show each delta with its band and say when it's inside noise, so no change is proposed or rejected on noise alone. The other three ideas in this capture (hook-feature ablation, an equal-dollar duel, a false-done benchmark) are separate captures.
## Assumptions (confidence)
## Acceptance criteria
- [x] with repeated runs, the gate prints passes and cost per case each with a ± band, and a drop inside the band reads 'within noise' and doesn't fail the gate, while one outside it still does — verify with `python3 plugin/tests/run.py test_bench test_evolve`
- [x] with single runs the gate is unchanged and still says a flipped case may be noise — verify with `python3 plugin/tests/run.py test_bench test_evolve`
## Non-goals
## Approach (options → choice → why)
Options: (A) per-case binomial standard error from attempts, summed for the pass total, and the cost spread as 2 x the standard error of the mean cost; a delta within its band is 'within noise' (chosen: stdlib statistics, no new runs needed); (B) bootstrap over attempts (more code, same answer at these sizes); (C) require --runs 3 for every gate (costly, blocks single-run use). Single runs keep today's note; a loss outside the band still fails the gate.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: gate on repeated results inside and outside the band; single runs unchanged
2. [x] fmbench.gate: bands from attempts; within-noise wording; docs
## Resume here
## Docs impact
CHANGELOG line; plugin/skills/improve/SKILL.md gate description
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench -k gate -k old_repeated` → exit 0 · Ran 117 tests in 106.8s (50 classes, 16 at a time; slowest: Bench 107s, Judged 60s, CloseGates 58s) / OK [ran] [tree f8d833047e69] (2026-10-21T20:56:07Z)
- (step 2) `python3 plugin/tests/run.py test_bench test_evolve` → exit 0 · Ran 49 tests in 90.1s (14 classes, 16 at a time; slowest: Bench 90s, Judged 48s, Evolve 43s) / OK [ran] [tree f8d833047e69] (2026-10-21T20:57:41Z)
- (step 1) `python3 plugin/tests/run.py test_bench test_evolve` → exit 0 · Ran 49 tests in 89.6s (14 classes, 16 at a time; slowest: Bench 89s, Judged 45s, Evolve 36s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:26:47Z)
- (step 2) `python3 plugin/tests/run.py test_bench test_evolve` → exit 0 · Ran 49 tests in 87.6s (14 classes, 16 at a time; slowest: Bench 87s, Judged 42s, Evolve 32s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:28:16Z)
- (ac 1) `python3 plugin/tests/run.py test_bench test_evolve` → exit 0 · Ran 49 tests in 94.0s (14 classes, 16 at a time; slowest: Bench 93s, Judged 47s, Evolve 38s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:30:50Z)
- (ac 2) `python3 plugin/tests/run.py test_bench test_evolve` → exit 0 · Ran 49 tests in 94.0s (14 classes, 16 at a time; slowest: Bench 93s, Judged 47s, Evolve 38s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:30:50Z)
- (audit intent) `self: read gate, _runs, _cost_se — the band is 2 SE of the difference; pass SE from each case's rate and runs (a single run has zero variance, so it's judged as strictly as before); cost SE from per-attempt costs, which run_case_n already stores, else no cost band and the 15% tolerance decides alone` → with repeated runs both deltas print with ± bands; a drop inside reads 'within noise' and passes, one outside fails; single runs unchanged with the 'may be noise' line (test_bench, test_evolve) [tree 44850c6e72aa] (2026-10-21T21:30:50Z)
- (audit edge) `self: read gate, _runs, _cost_se — the band is 2 SE of the difference; pass SE from each case's rate and runs (a single run has zero variance, so it's judged as strictly as before); cost SE from per-attempt costs, which run_case_n already stores, else no cost band and the 15% tolerance decides alone` → non-numeric runs count as 1, rates clamped, boolean or non-numeric attempt costs skipped; evolve's _better can still adopt a gain inside the band (T-1435) [tree 44850c6e72aa] (2026-10-21T21:30:50Z)
- (audit intent) `self: read gate, _runs, _cost_se — the band is 2 SE of the difference; pass SE from each case's rate and runs (a single run has zero variance, so it's judged as strictly as before); cost SE from per-attempt costs, which run_case_n already stores, else no cost band and the 15% tolerance decides alone` → with repeated runs both deltas print with ± bands; a drop inside reads 'within noise' and passes, one outside fails; single runs unchanged with the 'may be noise' line (test_bench, test_evolve) [tree 44850c6e72aa] (2026-10-21T21:31:01Z)
- (audit edge) `self: read gate, _runs, _cost_se — the band is 2 SE of the difference; pass SE from each case's rate and runs (a single run has zero variance, so it's judged as strictly as before); cost SE from per-attempt costs, which run_case_n already stores, else no cost band and the 15% tolerance decides alone` → non-numeric runs count as 1, rates clamped, boolean or non-numeric attempt costs skipped; evolve's _better can still adopt a gain inside the band (T-1435) [tree 44850c6e72aa] (2026-10-21T21:31:01Z)
## Log
- 2026-10-20T14:01:25Z created
- 2026-10-21T13:42:05Z planned from capture
- 2026-10-21T15:27:33Z criterion 1 verify: `python3 plugin/tests/run.py test_evolve` → `python3 plugin/tests/run.py test_bench test_evolve`
- 2026-10-21T15:27:34Z criterion 2 verify: `python3 plugin/tests/run.py test_evolve` → `python3 plugin/tests/run.py test_bench test_evolve`
- 2026-10-21T15:27:34Z grounded: fmbench.gate (line ~480) is called by fmevolve (the improve loop's candidate vs live); each case result carries attempts [{pass, cost_usd, …}] and runs/pass_rate when --runs > 1, so bands come from data already kept; tests go in test_bench calling fmbench.gate directly (verify widened to test_bench test_evolve). Second plan skipped: the math is small and local.
- 2026-10-21T20:22:34Z grounded 2026-10-21: fmbench.gate (line 473) compares sum(_rate) per shared case and mean cost_usd; a case keeps runs and its pass rate but only one cost_usd, so the cost band needs per-attempt costs kept (or the band covers passes only, cost still gated by the 15% tolerance). Pass band: per case p(1-p)/n summed for each side, difference SE = sqrt(SEa^2+SEb^2), band = 2 SE; a pass drop within the band reads 'within noise' and doesn't fail; single runs keep today's line.
- 2026-10-21T20:45:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1260.builder.md
- 2026-10-21T20:46:19Z focused
- 2026-10-21T21:24:14Z merged worktree-agent-a7953a69066cadf6e (3 file(s))
- 2026-10-21T21:24:14Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7953a69066cadf6e
- 2026-10-21T21:29:14Z focused
- 2026-10-21T21:30:51Z affected tests waived: UI mod JS subagent-row test times out at 5 s under load (T-1427, blocked with diagnosis)
- 2026-10-21T21:31:02Z affected tests waived: UI mod JS subagent-row test times out at 5 s under load (T-1427, blocked with diagnosis)
- 2026-10-21T21:31:05Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- T-0221 [FEATURE S, done, 1 steps] Bench rigor — fm bench run --runs N reports per-case pass fraction and cost/turns spread,
- T-1231 [PERFORMANCE L, deferred, 5 steps] Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- the similar finished task took 1 steps
## Why not caught
none: new reporting
## Lessons
- Before calling a delta a regression, show its noise band; with repeats the data to compute it is usually already stored
## Files touched
- plugin/tests/test_bench.py
- plugin/lib/fmbench.py
- plugin/skills/improve/SKILL.md
- CHANGELOG.md
- plugin/lib/fmcode.py
- plugin/tests/test_code_hardening.py
