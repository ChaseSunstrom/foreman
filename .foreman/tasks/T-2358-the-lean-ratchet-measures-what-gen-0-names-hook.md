---
id: T-2358
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/lib/fmrelease.py]
depends_on: []
source: user
created: 2026-10-31T14:01:02Z
updated: 2026-10-31T16:59:19Z
builder_model: sonnet
base: 29838df1224c78cb4bc23af46456bc6d31e53196
base_tree: 504a23ee207f3674d641dc0b868c0badbdfe9ae3
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:23:13Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/lib/fmrelease.py]
verified: strong
---
# The lean ratchet measures what gen-0 names: hook p95 and injected context, and only a cut pays for growth (Mission 8, #12)
## Raw request
> The lean ratchet measures what gen-0 names: hook p95 and injected context, and only a cut pays for growth (Mission 8, #12)
## Interpretation
Reading 1: the lean ratchet's footprint() measures what gen-0 section 6 names (hook p95 and injected context from SessionStart and UserPromptSubmit) and a grown metric clears only on a recorded always-on cut of at least its size (gap map #12). Reading 2: only add the metrics and keep the decision waiver. Rejected: any fm decide naming a grown metric clears its warning today, so a session can waive its own lean gate.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship's footprint record and fm doctor's ratchet include SessionStart and UserPromptSubmit injected chars and each hook's p95 when measured, latency with a 15% band — verify with `python3 plugin/tests/run.py test_doctor test_ship`
- [x] A grown metric's warning clears only when an always-on cut of at least that size since the same ship is on record; an fm decide naming the metric no longer clears it — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
1) Extend footprint(): add SessionStart and UserPromptSubmit injected chars from the doctor's hook bench and each hook's p95 when measured (FOREMAN_DOCTOR_BENCH), latency with a 15% band; a grown metric clears only when an always-on cut of at least its size since the same ship is on record. Fails if: a noisy bench trips the band, which the 15% band and measured-only rule absorb. 2) Use what exists: footprint() as T-2281 shipped it (rules, descriptions, the largest SKILL body), with the decision waiver. Likely outcome: the two named metrics stay unmeasured and the waiver stays self-granted. 3) Do less: hard-fail fm ship on any growth. Fails later, not now: the per-branch self-change gate and the generation sweep do the blocking, so this is left for them. Choice 1 (85%): the smallest change that closes both holes and is testable offline.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_doctor.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_supply_delta.py; past FIXes T-0928, T-0951, T-1011, T-1139, T-1219.
## Execution prompt
## Steps
1. [x] red tests: the new metrics; latency band; the cut clears and the decision doesn't
2. [x] footprint metrics and the ratchet's clearing rule
3. [x] docs: MASTER doctor line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T16:29:59Z step 3/3: docs: MASTER doctor line, CHANGELOG
- git: foreman/build; 4 uncommitted: plugin/lib/fmdoctor.py, plugin/tests/bench_hooks.py, plugin/tests/test_doctor.py, plugin/tests/test_ship.py
- touched since last checkpoint: plugin/tests/test_ship.py, plugin/tests/test_doctor.py, plugin/tests/bench_hooks.py, plugin/lib/fmdoctor.py
## Docs impact
MASTER.md (fmdoctor and fm ship lines), CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor -k FootprintRatchet` → ✗ exit 1 · Ran 9 tests in 0.7s (1 classes, 16 at a time; slowest: FootprintRatchet 0s) / FAILED (1 classes: test_doctor.FootprintRatchet) [ran] [tree 373b527f69b4] (2026-10-31T16:26:31Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 125 tests in 24.9s (31 classes, 16 at a time; slowest: Ship 25s, ViewsRepair 5s, LockProbe 4s) / OK [ran] [tree e7e6af292a2a] (2026-10-31T16:29:37Z)
- (step 3) `grep -q 'T-2358' MASTER.md CHANGELOG.md` → exit 0 · (no output) [ran] [tree 4ffa0b05d0c4] (2026-10-31T16:48:52Z)
- `python3 plugin/tests/run.py test_doctor -k FootprintRatchet` → ✗ exit 1 · Ran 9 tests in 1.9s (1 classes, 16 at a time; slowest: FootprintRatchet 0s) / FAILED (1 classes: test_doctor.FootprintRatchet) (start tree + this task's tests) [ran] [tree 4ffa0b05d0c4] (2026-10-31T16:48:55Z)
- `python3 plugin/tests/run.py test_doctor -k FootprintRatchet` → exit 0 · Ran 9 tests in 0.5s (1 classes, 16 at a time; slowest: FootprintRatchet 0s) / OK [ran] [tree 4ffa0b05d0c4] (2026-10-31T16:48:55Z)
- (step 2) `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 127 tests in 33.5s (31 classes, 16 at a time; slowest: Ship 33s, ViewsRepair 7s, LockProbe 6s) / OK [ran] [tree da1d06a8c69c] (2026-10-31T16:54:11Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor test_ship` → exit 0 · Ran 127 tests in 37.6s (31 classes, 16 at a time; slowest: Ship 37s, ViewsRepair 7s, LockProbe 6s) / OK [ran] [tree 759f115a0056] (2026-10-31T16:55:22Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 99 tests in 8.1s (30 classes, 16 at a time; slowest: ViewsRepair 7s, LockProbe 6s, Command 4s) / OK [ran] [tree 759f115a0056] (2026-10-31T16:55:22Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 3 LOW and one noticed hole (ship absorbing growth) fixed test-first` → injected chars and each hook's p95 in the ship record and the doctor's ratchet; a decision no longer waives growth [tree 759f115a0056] (2026-10-31T16:55:22Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 3 LOW and one noticed hole (ship absorbing growth) fixed test-first` → no cross-hook or SKILL-trim offsets; a failed hook's 0 isn't a cut; the record ratchets so a ship can't absorb growth [tree 759f115a0056] (2026-10-31T16:55:22Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 3 LOW and one noticed hole (ship absorbing growth) fixed test-first` → loaded runs and 0 sizes aren't measured; a metric not measured now isn't judged; a hook that hangs measures 0 [tree 759f115a0056] (2026-10-31T16:55:22Z)
- (audit operator) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 4 MEDIUM, 3 LOW and one noticed hole (ship absorbing growth) fixed test-first` → ship bench at 5 runs, 180 s timeout, skipped under FOREMAN_DOCTOR_BENCH=0 [tree 759f115a0056] (2026-10-31T16:55:22Z)
## Log
- 2026-10-31T14:01:02Z created
- 2026-10-31T16:07:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2358.builder.md
- 2026-10-31T16:07:14Z builder slot freed
- 2026-10-31T16:11:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2358.builder.md
- 2026-10-31T16:11:04Z builder slot freed
- 2026-10-31T16:23:11Z focused
- 2026-10-31T16:23:13Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T16:26:30Z scope: tests live in plugin/tests/test_doctor.py and test_ship.py (the ACs' verify commands name them); bench_hooks.py gains --inject so fm ship can measure the shipped tree's hooks
- 2026-10-31T16:30:32Z paused: focus moved to T-2338
- 2026-10-31T16:48:41Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T16:48:41Z focused
- 2026-10-31T16:54:19Z scope: tests in test_doctor/test_ship (the ACs' verify commands), bench_hooks.py gains injection_sizes and --inject so fm ship measures the shipped tree, MASTER and CHANGELOG lines
- 2026-10-31T16:59:14Z done
- 2026-10-31T16:59:19Z committed d9115041 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2359 [FEATURE M, done, 3 steps] Each generation's sweep fails on net growth: footprint, hook p95 and verbs at the seed vs at the sweep (Mission 8, #12) — lesson: A no-…
- T-2281 [FEATURE M, done, 3 steps] Lean ratchet (Mission 8/#12): each ship records the always-on footprint (rules chars, descriptions chars, SKILL bodies, hook p50) and f…
- research T-2359-review: Verdict: changes needed.** Nothing is wrong with the ratchet's core logic. But the hook p95 leg can turn the sweep red on an unchanged tree, a fa…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_release.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmdoctor.py; re-ground the plan against them before editing
## Lessons
- Net accounting across a unit leaks: pool only metrics that are truly interchangeable (always-on chars), judge the rest alone, and compare measurements taken with one estimator on one basis
## Plan gaps
- failed first: step 1 red tests: the new metrics; latency band; the cut clears and the decision doesn't
## Files touched
- plugin/tests/test_doctor.py
- plugin/tests/test_ship.py
- plugin/tests/bench_hooks.py
- plugin/lib/fmdoctor.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmlanes.py
- plugin/lib/fmmcp.py
- plugin/lib/fmnew.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmtoolproof.py
- plugin/lib/fmwhich.py
- plugin/skills/intake/references/planning.md
- plugin/tests/helpers.py
- plugin/tests/test_backlog.py
- plugin/tests/test_builder.py
- plugin/tests/test_clean_helpers.py
- plugin/tests/test_cli.py
- plugin/tests/test_conflict_history.py
- plugin/tests/test_core.py
- plugin/tests/test_defect_classes.py
- plugin/tests/test_deliberation.py
- plugin/tests/test_diagnosis.py
- plugin/tests/test_edit_cards.py
- plugin/tests/test_evidence_quality.py
- plugin/tests/test_graph.py
- plugin/tests/test_hooks.py
- plugin/tests/test_judgment.py
