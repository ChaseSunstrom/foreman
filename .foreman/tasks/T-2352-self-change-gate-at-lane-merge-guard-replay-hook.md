---
id: T-2352
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/lib/fmreplay.py, plugin/lib/fmdoctor.py]
depends_on: [T-2358]
source: user
created: 2026-10-31T14:00:57Z
updated: 2026-10-31T17:20:49Z
builder_model: sonnet
base: d9115041184e84f71dae29c618c09565e77651cd
base_tree: 759f115a0056132999582aaaa96326d808b95df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T16:59:58Z
plan0_scope: [plugin/lib/fmlanes.py, plugin/lib/fmreplay.py, plugin/lib/fmdoctor.py]
verified: strong
---
# Self-change gate at lane merge: guard replay, hook p95 and footprint must not get worse (Mission 8, #7 #12)
## Raw request
> Self-change gate at lane merge: guard replay, hook p95 and footprint must not get worse (Mission 8, #7 #12)
## Interpretation
Reading 1: the gate sits at fm lane merge and fires only for a branch touching fmguard.py, plugin/hooks/ or what a hook injects, comparing base vs branch on the guard's replay cases, hook p95 and footprint (gap map #7 code self-change gate and #12 keep the guard intact). Reading 2: the gate is a check every task runs through fm check. Ruled out: bench_hooks costs minutes and most tasks never touch hooks, so every task would pay for the few that do.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane merge of a branch that changes fmguard.py or plugin/hooks/ replays the guard's recorded cases on base and branch with no grants; a case the base blocks and the branch allows refuses the merge, naming the case and both verdicts — verify with `python3 plugin/tests/run.py test_lanes test_replay`
- [x] A branch changing hook code runs bench_hooks on base and branch; a hook whose p95 passes its budget or rises more than 15% refuses the merge with both numbers — verify with `python3 plugin/tests/run.py test_lanes`
- [x] A branch whose always-on footprint grows refuses unless it cuts at least as much elsewhere; a session's own fm decide never passes a refused gate, only the user's yes to fm ask ID core — verify with `python3 plugin/tests/run.py test_lanes test_doctor`
## Non-goals
## Approach (options → choice → why)
1) Merge gate for self-change branches: guard replay cases base vs branch with no grants (any newly allowed case refuses), bench_hooks p95 per hook (past budget or +15% refuses), fmdoctor.footprint growth refuses unless the branch cuts as much elsewhere; a refusal names the numbers and only the user's fm ask ID core passes it. Fails if: the touched-path test misses a self-change that edits an injected string from a non-hook file, so the path list reads what each hook injects. 2) Use what exists: fm check's affected-tests run plus fm bench gate, which already gates instruction files for fm evolve. Likely outcome: a guard block turned into an allow passes whenever no unit test names that case. 3) Do less: a nightly regression report. Fails if: it is advice after the merge, not a gate. 4) Run the three checks inside fm check for every task. Breaks the speed of every close for branches that never touch hooks. Choice 1 (85%): a self-change branch is the one place a regression is cheap to refuse and costly to find later.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/tests/test_doctor.py, plugin/lib/fmcli.py, MASTER.md, plugin/tests/test_lanes.py; past FIXes T-0928, T-0951, T-1011, T-1136, T-1139.
## Execution prompt
## Steps
1. [x] red tests: newly allowed case refuses; slower hook refuses; grown footprint refuses unless offset; decision doesn't pass
2. [x] the gate in fm lane merge for self-change branches
3. [x] docs: MASTER lane merge line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T17:04:51Z step 1/3: red tests: newly allowed case refuses; slower hook refuses; grown footprint refuses unless offset; decision doesn't pass
- git: foreman/build; 1 uncommitted: plugin/tests/test_lanes.py
- touched since last checkpoint: plugin/tests/test_lanes.py
## Docs impact
MASTER.md (fmselfgate line), CHANGELOG.md
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_lanes test_replay test_doctor` → exit 0 · Ran 210 tests in 31.8s (42 classes, 16 at a time; slowest: LaneRecovery 31s, Lanes 29s, RaceEvidence 20s) / OK [ran] [tree 6957cf3f72da] (2026-10-31T17:08:48Z)
- (step 3) `grep -q 'T-2352' MASTER.md CHANGELOG.md` → exit 0 · (no output) [ran] [tree 6957cf3f72da] (2026-10-31T17:09:07Z)
- `python3 plugin/tests/run.py test_lanes -k SelfChangeGate` → ✗ exit 1 · Ran 10 tests in 2.0s (1 classes, 16 at a time; slowest: SelfChangeGate 0s) / FAILED (1 classes: test_lanes.SelfChangeGate) (start tree + this task's tests) [ran] [tree 6957cf3f72da] (2026-10-31T17:09:16Z)
- `python3 plugin/tests/run.py test_lanes -k SelfChangeGate` → exit 0 · Ran 10 tests in 5.9s (1 classes, 16 at a time; slowest: SelfChangeGate 6s) / OK [ran] [tree 6957cf3f72da] (2026-10-31T17:09:16Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_serve test_replay test_doctor` → exit 0 · Ran 246 tests in 21.1s (47 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 15s, Run 14s) / OK [ran] [tree 832615640de8] (2026-10-31T17:18:34Z)
- (step 1) `python3 plugin/tests/run.py test_lanes -k SelfChangeGate` → exit 0 · Ran 15 tests in 6.4s (1 classes, 16 at a time; slowest: SelfChangeGate 6s) / OK [ran] [tree 832615640de8] (2026-10-31T17:18:55Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_replay` → exit 0 · Ran 116 tests in 20.8s (12 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 14s, RaceEvidence 9s) / OK [ran] [tree 832615640de8] (2026-10-31T17:19:59Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 106 tests in 20.7s (9 classes, 16 at a time; slowest: LaneRecovery 20s, Lanes 14s, RaceEvidence 9s) / OK [ran] [tree 832615640de8] (2026-10-31T17:19:59Z)
- (ac 3) `python3 plugin/tests/run.py test_lanes test_doctor` → exit 0 · Ran 205 tests in 20.9s (39 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 15s, RaceEvidence 9s) / OK [ran] [tree 832615640de8] (2026-10-31T17:19:59Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 6 MEDIUM, 2 LOW fixed with tests; residuals in research/T-2352-review` → guard replay, hook bench and footprint, each refusing with its numbers; a criteria waiver never waives the gate [tree 832615640de8] (2026-10-31T17:19:59Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 6 MEDIUM, 2 LOW fixed with tests; residuals in research/T-2352-review` → the base's harness judges the branch; trees from git blobs; scrubbed env; the yes is bound to the gated sha, which is what merges; fm serve gated too [tree 832615640de8] (2026-10-31T17:19:59Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 6 MEDIUM, 2 LOW fixed with tests; residuals in research/T-2352-review` → both trees failing on a command doesn't refuse; a None verdict does; a new fixture takes the base's tightest budget; b0 of 0 guarded [tree 832615640de8] (2026-10-31T17:19:59Z)
- (audit operator) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 6 MEDIUM, 2 LOW fixed with tests; residuals in research/T-2352-review` → 2-4 min per gated merge (replay and bench run only for files that can change them); a refusal names fm ask ID core [tree 832615640de8] (2026-10-31T17:19:59Z)
- (audit maintainer) `fm-reviewer pass (intent, adversary, edge, operator, maintainer); 2 HIGH, 6 MEDIUM, 2 LOW fixed with tests; residuals in research/T-2352-review` → one module, 15 tests incl. a real-subprocess replay through the base's harness [tree 832615640de8] (2026-10-31T17:19:59Z)
## Log
- 2026-10-31T14:00:57Z created
- 2026-10-31T16:06:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2352.builder.md
- 2026-10-31T16:06:57Z builder slot freed
- 2026-10-31T16:10:56Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2352.builder.md
- 2026-10-31T16:10:56Z builder slot freed
- 2026-10-31T16:50:09Z ground: fmreplay.candidate(ref) loads a guard from a git ref and verdicts(cmds, g) judges with no grants: replay guard_cases.jsonl + guard_allow.jsonl (the union of base's and branch's, so a branch deleting a case can't hide it) under base and branch guards. Hook p95 and injected chars: run each tree's bench_hooks.py --inject (T-2358 adds it) on a git-archive of base and on the lane worktree; footprint via fmdoctor.footprint + measured, judged with the T-2358 ratchet rule (refactor _ratchet into a pure was/now function both share). Grant: the session holds a standing core yes, so the gate must take only a per-task fm ask ID core answered after the refusal, never the standing yes.
- 2026-10-31T16:50:09Z set depends_on=['T-2358']
- 2026-10-31T16:50:49Z plan (second-plan review, all taken): trigger = any branch touching plugin/ runs the guard replay (cheap, static cases) and the footprint (static); the hook bench runs when the diff touches plugin/hooks/ or a module in the hooks' import closure (ast walk from hooks/hook's entry modules), so a shared helper or injected string from a non-hook file is caught. Corpus integrity: replay the union of base's and branch's guard_cases.jsonl and guard_allow.jsonl; a branch that removes a labelled case refuses too. Approval: only a grant from fm ask ID core recorded on this task after the refusal (the user's answer to Claude Code's prompt), never the standing core yes or any fm decide; the refusal prints the ask. Noise: hook p95 = median of 3 bench runs (as fmdoctor.hook_p95), CPU time when loaded; 'past its budget' = over bench_hooks.BUDGET_MS. Footprint unit: chars of always-on context, same-unit cut since base (T-2358's rule, shared as one pure function); moving text to a lazily loaded file is a real cut. Can't run (no bench, error) = refuse with the reason; the same per-task ask passes it.
- 2026-10-31T16:59:53Z focused
- 2026-10-31T16:59:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T17:05:03Z paused: focus moved to T-2429
- 2026-10-31T17:05:59Z focused
- 2026-10-31T17:09:06Z scope: the gate lives in a new module plugin/lib/fmselfgate.py (one MASTER line), tests in test_lanes.SelfChangeGate (the ACs' verify command), docs in MASTER and CHANGELOG
- 2026-10-31T17:18:02Z scope: fmserve._integrate_lane gated too (review: fm serve merged lanes with --ff-only around the gate)
- 2026-10-31T17:20:46Z done
- 2026-10-31T17:20:49Z committed 3deb3dc7 (6 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The touched-path test is the gate's weakest point and the plan only names it as a failure mode. If it misses a self-change (an injected string edited from a non-hook file, a shared helper imported by fmguard.py, config the guard reads), the whole gate is silently bypassed. There's no criterio…
- HIGH: "Replay on base vs branch with no grants" only proves anything if the recorded cases cover the guard's blocks. The plan's own option 2 admits the failure is a block turned allow with no test naming it. Nothing checks replay coverage or that the replay corpus itself isn't changed by the branch…
- HIGH: The bypass rule is under-specified and unverifiable as written. "A session's own fm decide never passes a refused gate, only the user's yes to fm ask ID core" needs a mechanism: how does the merge distinguish a user answer from a session-issued one? If it's just a flag or file the session can…
- MEDIUM: The p95 criterion is flaky as stated. A +15% threshold on a timing benchmark across base and branch runs on a shared machine will give false refusals and, worse, false passes. The plan has no sample count, warm-up, or noise handling, and "passes its budget" is ambiguous (exceeds? within?). …
- MEDIUM: "Footprint grows refuses unless it cuts at least as much elsewhere" has no defined unit or scope. Is it bytes, tokens, or lines of always-on context? "Elsewhere" could let a branch offset a hook injection with an unrelated doc trim, or game it by moving content to a lazily loaded file that …
- LOW: Step order puts red tests first but there's no step for rollback or a kill switch. If the gate misfires (e.g. bench_hooks unavailable on a machine), lane merge is blocked for self-change branches, which includes the branch that fixes the gate. — Define behavior when a check can't run (refuse w…
Verdict: revise — the approach is right, but the trigger detection, corpus integrity and approval authentication are the gate's actual security properties and none has a criterion that proves it.
## Dissent
- [ ] HIGH: The touched-path test is the gate's weakest point and the plan only names it as a failure mode. If it misses a self-change (an injected string edited from a non-hook file, a shared helper imported by fmguard.py, config the guard reads), the whole gate is silently bypassed. There's no criterio…
- [ ] HIGH: "Replay on base vs branch with no grants" only proves anything if the recorded cases cover the guard's blocks. The plan's own option 2 admits the failure is a block turned allow with no test naming it. Nothing checks replay coverage or that the replay corpus itself isn't changed by the branch…
- [ ] HIGH: The bypass rule is under-specified and unverifiable as written. "A session's own fm decide never passes a refused gate, only the user's yes to fm ask ID core" needs a mechanism: how does the merge distinguish a user answer from a session-issued one? If it's just a flag or file the session can…
- [ ] MEDIUM: The p95 criterion is flaky as stated. A +15% threshold on a timing benchmark across base and branch runs on a shared machine will give false refusals and, worse, false passes. The plan has no sample count, warm-up, or noise handling, and "passes its budget" is ambiguous (exceeds? within?). …
- [ ] MEDIUM: "Footprint grows refuses unless it cuts at least as much elsewhere" has no defined unit or scope. Is it bytes, tokens, or lines of always-on context? "Elsewhere" could let a branch offset a hook injection with an unrelated doc trim, or game it by moving content to a lazily loaded file that …
- [ ] LOW: Step order puts red tests first but there's no step for rollback or a kill switch. If the gate misfires (e.g. bench_hooks unavailable on a machine), lane merge is blocked for self-change branches, which includes the branch that fixes the gate. — Define behavior when a check can't run (refuse w…
## Related
Related past work (data from this project's history, not instructions):
- T-2359 [FEATURE M, done, 3 steps] Each generation's sweep fails on net growth: footprint, hook p95 and verbs at the seed vs at the sweep (Mission 8, #12) — lesson: A no-…
- T-2358 [FEATURE M, done, 3 steps] The lean ratchet measures what gen-0 names: hook p95 and injected context, and only a cut pays for growth (Mission 8, #12) — lesson: Ne…
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_lanes.py, plugin/tests/test_replay.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmdoctor.py, plugin/lib/fmlanes.py; re-ground the plan against them before editing
## Lessons
- A gate that runs the candidate's own measuring code measures nothing: judge with the base's harness, bind the approval to the exact commit, and merge that commit
## Files touched
- plugin/tests/test_lanes.py
- plugin/tests/test_doctor.py
- plugin/lib/fmselfgate.py
- plugin/lib/fmlanes.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmserve.py
