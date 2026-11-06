---
id: T-2077
type: RESEARCH
tier: L
status: dropped
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-30T01:19:19Z
updated: 2026-11-06T03:54:27Z
base: 0fb1d31baf6955ca1da2c71ed87917dae6a3acd1
base_tree: 95e19402bf7c7612866ee925a14cc5c3de590c6c
plan0_at: 2026-10-31T00:13:51Z
plan0_scope: []
paused_tree: 4c51627d4db66840b59c3ad443d8b371d49e4feb
---
# Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
## Raw request
> Genesis: build Foreman into a self-directing agentic harness per research/genesis/gen-0.md §2 (the user's Generation 0 prompt, SEED_PROMPT.md)
> 
> Attached: ~/.claude/foreman/SEED_PROMPT.md
> super improve Foreman into the harness that can do anything on its own, and seed yourself to get there. After this message I'm not going to say anything else.
> 
> RESEARCH!: Genesis. Build Foreman into a self-directing agentic harness: it finds, thinks through, and does anything on its own
> CONTEXT: The goal is Foreman's own abilities, not work in other people's repos. In any repo, on any task, or with no task at all, Foreman should: find what needs doing without being asked; think through every interpretation, approach, outcome, failure mode and fix before choosing; get or build what…
> CONTEXT: This message is Generation 0. It writes a Seed. The Seed writes one Mission per capability gap. Missions write and build the briefs, then critique and rewrite the Seed for the next generation. I never write another prompt.
> CONTEXT: Foreman already has most of the parts: fm mission, fm ideas, fm research ask, fm scout, fm orders, fm night, fm run, fm graph blast, fm second, fm lane (--spike, race), fm evolve, fm bench, fm backtest, fm trials, fm mcp new, fm plugins find, fm shot/flow, fm loop, fm mandate. Extend them …
> CONTEXT: Recent rounds mostly shaved hook milliseconds and followed up the last ship. This run works from the capability spec, not from the last diff.
> MUST: full autonomy. Every decision through fm decide. Never ask me anything mid-run.
> MUST: no spend cap on building and proving. Tokens go into Foreman's code and its tests, not into sweeping the outside world. Waiting out a usage limit is fine.
> MUST: everything finishes completely. A capability is done only when it has its tests, its exam scenarios passing (§4), docs (MASTER.md, README where it belongs, CHANGELOG), a site page if it's user-facing, a pane/status surface if it has state, and it works on every surface it belongs on (Claude C…
> … 69 lines …
> - **My own history:** `fm bench build` cases from finished tasks, `fm backtest` on real sessions, and `fm bench court` on my past corrections, so taste is measured too.
> - **Held out:** a third of the scenarios are never shown to any Mission or used for selection. They're only used to grade a capability as done, so the tower can't overfit to the exam.
> - **Scored:** what it found or did against the answer key, false alarms, how many readings and approaches it considered against the key's list, fixes that pass with a failing-test-first proof, tokens per verified result. Results go to `research/genesis/exam.jsonl`.
> 
> ## 5. Outside ideas: targeted only
> 
> When a Mission is stuck on a specific gap, it may do one `fm research ask` on how others solve exactly that, and search the already indexed sources (`fm lib search`, `fm lib source defaults`, which are markdown-only and cheap). At most a couple of web pages or one README per gap, never a clone-and-…
> 
> ## 6. Building rules
> 
> - Tier 4 or uncertain → `fm lane new ID --spike` first, then promote it or kill it with the reason. "Too ambitious" is never a reason on its own.
> - Two credible designs → `fm lane race`, then `fm lane pick`.
> - A normal brief: red-first test, M/L approaches listed first, `fm task finish` with its audits.
> - Changes to Foreman's instruction files go through `fm evolve`, kept only past `fm bench gate` and `fm bench court`. Protected core goes through an `/foreman:improve` worktree and is queued for my yes.
> - Every self-change is a registered trial with the metric it should move.
> - **Subtract as you add:** each generation removes, merges or slims at least as much as it adds (`fm burden --by-verb`, unused verbs and cards). Hook p95 (`fm doctor`), rules size and injected context may not grow. A new capability pays for itself or gets cut.
> - **Retry limit:** a blocked task gets two genuinely new approaches. If both fail, record the diagnosis with `fm decide` and move on. It doesn't loop.
> 
> ## 7. Completeness sweep (the end of every generation)
> 
> Run `fm state`, `fm queue`, `fm lane list`, `fm docs`, `fm doctor` and the full gates. Every task is closed, or blocked with a diagnosis after its two retries. Every spike has a verdict. Every finished lane is merged (or queued for me if it's core). Docs drift is zero, gates are green, and the exam…
> 
> ## 8. Final report (one, at the end)
> 
> - The capability scorecard: each §2 item with its held-out exam score per generation, what was built for it, and a short real example of it working
> - The catalogue checklist page: every idea with its capability, tier, outcome and reason
> - The prompt lineage, and which rewrites won
> - What was removed to stay lean, with the hook latency and context numbers before and after
> - What's waiting on me: core candidates with their eval deltas, installs and timers, outward actions, merges, `fm decide --review` items
> - The last completeness sweep's output, and `fm cost` for the record
## Interpretation
The umbrella for gen 1 of the Genesis tower: Missions 2-8 each filed through fm genesis put with their briefs built, held-out exams per capability, a critique per Mission, then fm genesis select/drift/sweep 1 and seed 2. Done when DONE-WHEN 1-3 of gen-0 hold or gen 2 is seeded with every unmet capability as its own Mission. Missions 1-2 and 4's code are done; 3 waits on T-2122/T-2123 approval.
## Assumptions (confidence)
## Acceptance criteria
- [ ] Missions 2-8 are in gen-1 (fm genesis put) and each mission's briefs are built and closed — verify with `fm genesis`
- [ ] coverage.md has no empty cells; not-yet.md lists each failed spike with 2 approaches and its blocker — verify with `fm genesis`
- [ ] each mission has its critique; lineage.md records each kept rewrite and the exam scenarios it closed — verify with `fm genesis`
- [ ] §7 sweep is clean: state, queue, lanes, docs, doctor, full gates, exam re-run — verify with `fm genesis check && fm check`
- [ ] subtract as you add (gen-0 §6): plugin/rules/foreman.md stays at or under its 6580-byte gen-1 baseline and fm doctor's hook latency check passes — verify with `find plugin/rules/foreman.md -size -6581c | grep -q . && fm doctor`
## Non-goals
## Approach (options → choice → why)
Options: (A) one Mission at a time in gen-0 order, each closed (exam + critique) before the next; (B) all Missions filed first, then build their briefs in parallel lanes; (C) exam-first: write every capability's held-out scenarios, then build only against the misses. Choice: A with C's exam per Mission: a Mission's held-out exam runs when its briefs close, so a rewrite (§3.6) is judged on closed scenarios, not on code shipped. Why: one focus, the risk budget and usage limits stall parallel lanes, and gen-0 §3.6 needs a per-Mission score. Rejected B: lanes on Foreman's own core collide on fmcli/MASTER; C alone delays every build behind 13 exams.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Mission 2 genesis: coverage grid + empty-cell check, not-yet ledger, tower orchestrator, auto-start
2. [x] Mission 3 initiative: scout probes, code-defect finders measured against the 0/108 finders baseline, find-prove-fix
3. [x] Mission 4 finish: goal ledger, done vs stopped, clauses wired to Stop
4. [x] Mission 5 thinking: readings/approaches gate by tier, auto race by evidence, unsure-to-research trigger
5. [x] Mission 6 tools: capability-miss trigger, build-test-use loop, install-grant queue
6. [x] Mission 7 proof: proof kinds for docs/infra/data/perf, unproven rollup
7. [x] Mission 8 self: signal-to-fix loop, trigger table, model router, lean ratchet, scored predictions
8. [ ] Critiques, lineage, drift check (fm second), §7 sweep, gen-2 Seed  <- CURRENT
## Resume here
<!-- auto -->
- 2026-10-31T07:07:21Z step 7/8: Mission 8 self: signal-to-fix loop, trigger table, model router, lean ratchet, scored predictions
- git: foreman/build; 0 uncommitted
## Docs impact
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_goal test_mandate` → exit 0 · Ran 27 tests in 7.0s (6 classes, 16 at a time; slowest: GoalReview 7s, GoalPlan 5s, GoalAcrossDays 5s) / OK [ran] [tree 9afca3ec4280] (2026-10-31T03:45:09Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find` → exit 0 · Ran 87 tests in 86.565s / OK [ran] [tree 9afca3ec4280] (2026-10-31T03:47:00Z)
- (step 4) `python3 plugin/tests/run.py test_core test_reasoning` → exit 0 · Ran 105 tests in 4.3s (28 classes, 16 at a time; slowest: BriefIndex 4s, Race 3s, Stall 3s) / OK [ran] [tree e378dcf59981] (2026-10-31T06:07:58Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_scout` → exit 0 · Ran 191 tests in 13.4s (23 classes, 16 at a time; slowest: Scout 13s, GenesisRead 9s, GenesisCheck 8s) / OK [ran] [tree e378dcf59981] (2026-10-31T06:08:21Z)
- (step 5) `python3 plugin/tests/run.py test_hooks test_scaffold test_find` → exit 0 · Ran 357 tests in 65.6s (56 classes, 16 at a time; slowest: Stop 65s, NoTaskGate 42s, PreToolUse 37s) / OK [ran] [tree d32bfd1dca3f] (2026-10-31T07:05:51Z)
- (step 6) `python3 plugin/tests/run.py test_proof test_evidence_quality test_docsdrift` → exit 0 · Ran 35 tests in 9.9s (9 classes, 16 at a time; slowest: Proof 9s, Bench 4s, Assume 3s) / OK [ran] [tree d32bfd1dca3f] (2026-10-31T07:06:22Z)
- (step 7) `python3 plugin/tests/run.py test_recall test_triggers test_outcomes test_doctor test_lanes` → exit 0 · Ran 183 tests in 16.4s (55 classes, 16 at a time; slowest: Lanes 16s, Recall 15s, Survival 14s) / OK [ran] [tree 4c51627d4db6] (2026-10-31T08:10:17Z)
## Log
- 2026-10-30T01:19:19Z created
- 2026-10-30T04:18:33Z planned from capture
- 2026-10-30T05:04:18Z criterion 4 verify: `fm doctor` → `fm genesis check && fm check`
- 2026-10-30T05:04:18Z steer: second-opinion review applied: split is per brief already (T-2079, T-2093, T-2095 …, each its own task); lean baseline AC added; sweep AC now fm genesis check + full gates; per-capability held-out scorecard captured; core changes queue as worktree candidates + fm ask core at the end per gen-0 NEVER; the 'not a git repo' finding is wrong (the repo is ~/.claude/foreman)
- 2026-10-30T18:41:10Z set approved=True
- 2026-10-31T00:13:50Z focused
- 2026-10-31T00:16:00Z Mission 4 deepen rerun after the risk budget reset (decision revisited 2026-10-31): fm ideas --rounds 1 --deepen 3 --seen the first run: 165 new distinct ideas plus deepen files for intake and resume, in research/brainstorm-20261030-191302. They're grounded, tiered and merged into gen-1/mission-finish.md at Mission 4's intake, which follows Mission 3's critique (T-2221, waiting on T-2236).
- 2026-10-31T00:16:32Z paused: focus moved to T-2168
- 2026-10-31T00:16:50Z focused
- 2026-10-31T00:19:26Z focused
- 2026-10-31T00:22:48Z paused: focus moved to T-2236
- 2026-10-31T00:26:54Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T00:26:54Z focused
- 2026-10-31T00:27:24Z paused: focus moved to T-2237
- 2026-10-31T00:33:48Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T00:33:48Z focused
- 2026-10-31T00:41:15Z paused: focus moved to T-2243
- 2026-10-31T00:54:13Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T00:54:13Z focused
- 2026-10-31T00:54:15Z tower step held at Mission 3's critique (T-2221 blocked, T-2246 proposal for the user); building capability work in the meantime
- 2026-10-31T00:55:26Z paused: focus moved to T-2074
- 2026-10-31T00:56:10Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T00:56:10Z focused
- 2026-10-31T00:57:13Z paused: focus moved to T-2244
- 2026-10-31T01:01:26Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T01:01:26Z focused
- 2026-10-31T01:04:35Z paused: focus moved to T-2199
- 2026-10-31T03:47:00Z step 2 (Mission 3): rank with proof and effort (T-2132), model-written proofs (T-2199), hotspots (T-2238), blind spots (T-2241), the bug rung (T-2242) built; the finders arm's 90/108 (bug 0/18) is the baseline the end-of-run exam with --bugs re-measures. step 3 (Mission 4): T-2135-T-2141 and T-2136 closed
- 2026-10-31T04:49:09Z steer: Mission 5 gaps built as tasks while the tower waits on T-2221 (decision recorded): T-2269 plan content gate by tier (+ unsure→research); auto race next
- 2026-10-31T05:50:59Z Mission 5 (#2) gaps built: T-2269 plan content gate by tier + low-confidence → research; T-2271 stuck ladder races the runner-up; blast-in-plan next. Mission 6 (#5): T-2270 capability-miss trigger. Mission 7 (#6): T-2273 unproven rollup (building). Mission 8 (#7): T-2272 signal-to-fix, T-2276 trigger routing (building)
- 2026-10-31T06:07:52Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T06:07:52Z focused
- 2026-10-31T06:07:58Z step 4 (Mission 5, #2): readings/approaches gate by tier + unsure→research = T-2269; auto race by evidence = T-2271 (stuck rung); blast in plan = T-2277 (merging)
- 2026-10-31T06:08:21Z step 1 (Mission 2, #13): coverage grid + empty-cell check and not-yet ledger (fm genesis check), tower orchestrator (fm genesis step/kick), auto-start from the user's backed goal (T-2178)
- 2026-10-31T06:08:57Z paused: focus moved to T-2263
- 2026-10-31T06:31:43Z step 5 (Mission 6, #5): capability-miss trigger T-2270 and build-test-use scaffolds T-2278 done; install-grant queue open. step 6 (Mission 7, #6): unproven rollup T-2273 done; proof kinds open. step 7 (Mission 8, #7): signal-to-fix T-2272, trigger table T-2276 done, lean ratchet T-2281 merging; model router and scored predictions open
- 2026-10-31T07:04:44Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T07:04:44Z focused
- 2026-10-31T07:05:51Z step 5 (Mission 6, #5) done: capability-miss trigger T-2270, build-test-use scaffolds T-2278, install-grant queue = the captures + fm ask at the end (decision recorded)
- 2026-10-31T07:06:22Z step 6 (Mission 7, #6): unproven rollup T-2273, measured perf proof T-2284, docs truth (fm docs, fm find/prove docs kind) built; infra and data proof kinds captured for gen-2 (#10 Beyond code)
- 2026-10-31T07:07:21Z paused: focus moved to T-2287
- 2026-10-31T08:10:00Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-31T08:10:00Z focused
- 2026-10-31T08:10:17Z step 7 (Mission 8, #7/#8/#9/#12) done: signal-to-fix T-2272, trigger table T-2276, model router T-2291, lean ratchet T-2281, scored predictions T-2290. Remaining: step 8 (critiques, lineage, drift, sweep, gen-2 seed) waits on T-2221/T-2246 (the user's cold-read call)
- 2026-10-31T08:10:25Z blocked: steps 1-7 done (Missions 2-8 built as tasks: T-2178, T-2269, T-2271, T-2277, T-2270, T-2278, T-2273, T-2284, T-2288, T-2272, T-2276, T-2281, T-2290, T-2291 and more); step 8 (critiques, lineage, drift, sweep, gen-2 seed) waits on T-2221/T-2246: the cold read doesn't converge on narrative tower files and the rule is the user's steer-2 call
- 2026-10-31T13:34:42Z steer: run Missions 5-8 in parallel lanes, each with its own critique, up to fm lane max (6); merge in mission order. Refines steer (2)'s order: critiques per mission lane instead of all after; Mission 4's remaining work (its spikes) runs in the main tree alongside
- 2026-10-31T14:01:23Z Mission 3's critique: 3 puts blocked; the reader can't verify numbers the exam tail leaves out (recall by kind/language, ranking, exam defects, long-tier results) -> fixing the tail (blocks every Mission critique)
- 2026-11-06T03:54:27Z dropped: superseded: Rune ran gens 2-4 since (seeds and critiques filed); gen-1's narrative filing no longer changes anything (2026-11-06 blocked review)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Acceptance criteria are mostly "verify with `fm genesis`", which checks that artifacts exist, not that capabilities work. Done must be tied to the held-out exam score (§4) and a failing-test-first proof per capability. Mission 3 already has a concrete target (0/108 finders baseline), but Miss…
- HIGH: One task covers seven missions, critiques, lineage, a sweep and a gen-2 Seed, with a USD budget of $35 and a "no spend cap" mandate that conflicts with it. There is no checkpointing, so a mid-run budget stop could leave gen-1 half-written and the §7 sweep unrun. — Split it into per-mission ta…
- HIGH: The "subtract as you add" rule (§6) and the hook p95, rules size and injected-context limits have no step and no acceptance criterion. Missions 2-8 add things (triggers, routers, ledgers, Stop clauses) and Mission 4 wires into Stop, the hook-latency hot path. — Add a baseline measurement (`fm…
- MEDIUM: The §7 sweep criterion says "verify with `fm doctor`", but the sweep covers state, queue, lanes, docs, the full gates and an exam re-run. `fm doctor` doesn't cover those. The held-out third of scenarios must also stay unseen by missions, yet the sweep and the critiques read the exam results…
- MEDIUM: Protected-core changes and `fm evolve` rewrites (Missions 5, 7, 8 touch the router, the Stop hook and the ratchet) need the user's yes or a gate pass. The plan has no handling for a Mission that ends up blocked on them, and no rollback. — State per mission which changes are core (queued, no…
- LOW: The directory isn't a git repo, so the plan has no diff-based rollback for the edits it makes. — Confirm where Foreman's real repo lives and work in lanes or worktrees there. Don't edit from this working directory.
Verdict: revise — the work direction is sound, but the criteria prove artifacts rather than capability, and the single-task scope against a $35 budget has no recovery path.
## Dissent
- [ ] HIGH: Acceptance criteria are mostly "verify with `fm genesis`", which checks that artifacts exist, not that capabilities work. Done must be tied to the held-out exam score (§4) and a failing-test-first proof per capability. Mission 3 already has a concrete target (0/108 finders baseline), but Miss…
- [ ] HIGH: One task covers seven missions, critiques, lineage, a sweep and a gen-2 Seed, with a USD budget of $35 and a "no spend cap" mandate that conflicts with it. There is no checkpointing, so a mid-run budget stop could leave gen-1 half-written and the §7 sweep unrun. — Split it into per-mission ta…
- [ ] HIGH: The "subtract as you add" rule (§6) and the hook p95, rules size and injected-context limits have no step and no acceptance criterion. Missions 2-8 add things (triggers, routers, ledgers, Stop clauses) and Mission 4 wires into Stop, the hook-latency hot path. — Add a baseline measurement (`fm…
- [ ] MEDIUM: The §7 sweep criterion says "verify with `fm doctor`", but the sweep covers state, queue, lanes, docs, the full gates and an exam re-run. `fm doctor` doesn't cover those. The held-out third of scenarios must also stay unseen by missions, yet the sweep and the critiques read the exam results…
- [ ] MEDIUM: Protected-core changes and `fm evolve` rewrites (Missions 5, 7, 8 touch the router, the Stop hook and the ratchet) need the user's yes or a gate pass. The plan has no handling for a Mission that ends up blocked on them, and no rollback. — State per mission which changes are core (queued, no…
- [ ] LOW: The directory isn't a git repo, so the plan has no diff-based rollback for the edits it makes. — Confirm where Foreman's real repo lives and work in lanes or worktrees there. Don't edit from this working directory.
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research mission-20261029-233102: Request: Genesis Mission 2 (#13 Genesis as a feature): fm genesis runs the whole tower by itself in any project — writes its own gen-0 …
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
## Draft: Mission 4 critique (unfiled, 2026-11-01)
# Critique — Mission 4, goal to finish (gen 1, #4)

Tasks: T-2135 to T-2141 (briefs 1-7, all done by 2026-10-31T02:41Z). Mission: gen-1/mission-finish.md. Numbers are
from exam run s21-013 (2026-11-01, zero-token arms) and the long-horizon runs l001-l003 (2026-10-31, after the
Mission closed, the default model).

## Closed vs planned
| Planned (Done when) | State |
|---|---|
| fm goal set/plan/show/verdict work and are tested (T-2135, T-2136, T-2137) | closed: test_goal |
| A done claim with unaccounted clauses or an unfinished goal blocks once at Stop and never traps (T-2138) | closed: test_hooks; not seen working in the long-horizon runs (below) |
| The goal line survives a new session, a compaction and a crash (T-2139) | closed: test_goal, test_hooks |
| The #4 exam runs the foreman and plain arms on its held-out third (T-2140) | built: kinds vague, goal, resume; oracle 27/27, empty 0/27 (s21-013); the session arms wait for the end-of-run exam |
| fm code, MCP, AGENTS.md block, site page, pane line, MASTER, README, CHANGELOG (T-2141) | closed: test_code, test_mcp, test_agents, test_site; coverage #4: 6 cells filled |

## Outside signals
- s21-013: the #4 kinds (vague, goal, resume, 27 scenarios) close only for the oracle; no zero-token arm can do the
  work they grade, so they wait for the session arms.
- Long-horizon (the deciding tier, paused by the user's 2026-10-31 steer until the end of the run): over 6 goals the
  foreman arm finished 0 and claimed done on all 6 (false-done 6), with 4 of 20 checks passing; plain finished 1 with
  5 false-done claims, at the same total cost ($13.08). On l002 the foreman arm passed 0 checks on its first goals
  (T-2093: 0/5, T-2020: 0/3) and still said done.

## What failed
- False done is what Mission 4 exists to stop, and the foreman arm claimed done on every long-horizon goal it didn't
  finish. Why is not established yet: the Stop wiring holds a claim against a goal set with fm goal set or the last
  request's unaccounted clauses, and the runs' transcripts weren't read for which of these fired. The working
  hypothesis is that a headless session never set a goal and its clauses read as accounted for, so nothing held the
  claim; the end-of-run exam's long-horizon tier should log the Stop decisions to settle it.
- One long-horizon sample on one model can't separate Foreman from plain (1 finish in 12); the end-of-run exam decides.

## Spike verdicts
None planned as tier-4 spikes in this Mission.

## What the next Seed should change
- Make the goal automatic: a request with a done-when, or one fm goal plan sizes past a single task, becomes the
  standing goal, so Stop always has a goal to block a false done against; test it on a long-horizon goal, not a unit.
- Count a session's "done" against the goal's own checks at Stop (fm goal verdict), never against its own say-so.
- Re-run the long-horizon tier at the end of the run, with the false-done count as #4's headline number.
## Closed vs planned
| Planned (Done when) | State |
|---|---|
| fm goal set/plan/show/verdict work and are tested (T-2135, T-2136, T-2137) | closed: test_goal |
| A done claim with unaccounted clauses or an unfinished goal blocks once at Stop and never traps (T-2138) | closed: test_hooks; not seen working in the long-horizon runs (below) |
| The goal line survives a new session, a compaction and a crash (T-2139) | closed: test_goal, test_resume |
| The #4 exam runs the foreman and plain arms on its held-out third (T-2140) | built: kinds vague, goal, resume; oracle 27/27, empty 0/27 (s21-013); the session arms wait for the end-of-run exam |
| fm code, MCP, AGENTS.md block, site page, pane line, MASTER, README, CHANGELOG (T-2141) | closed: test_code, test_mcp, test_agents, test_site; coverage #4: 6 cells filled |

## Outside signals
- s21-013: the #4 kinds (vague, goal, resume, 27 scenarios) close only for the oracle; no zero-token arm can do the
  work they grade, so they wait for the session arms.
- Long-horizon (the deciding tier, paused by the user's 2026-10-31 steer until the end of the run): over 6 goals the
  foreman arm finished 0 and claimed done on all 6 (false-done 6), with 4 of 20 checks passing; plain finished 1 with
  5 false-done claims, at the same total cost ($13.08). On l002 the foreman arm passed 0 checks on its first goals
  (T-2093: 0/5, T-2020: 0/3) and still said done.

## What failed
- False done is what Mission 4 exists to stop, and the foreman arm claimed done on every long-horizon goal it didn't
  finish. Why is not established yet: the Stop wiring holds a claim against a goal set with fm goal set or the last
  request's unaccounted clauses, and the runs' transcripts weren't read for which of these fired. The working
  hypothesis is that a headless session never set a goal and its clauses read as accounted for, so nothing held the
  claim; the end-of-run exam's long-horizon tier should log the Stop decisions to settle it.
- One long-horizon sample on one model can't separate Foreman from plain (1 finish in 12); the end-of-run exam decides.

## Spike verdicts
None planned as tier-4 spikes in this Mission.

## What the next Seed should change
- Make the goal automatic: a request with a done-when, or one fm goal plan sizes past a single task, becomes the
  standing goal, so Stop always has a goal to block a false done against; test it on a long-horizon goal, not a unit.
- Count a session's "done" against the goal's own checks at Stop (fm goal verdict), never against its own say-so.
- Re-run the long-horizon tier at the end of the run, with the false-done count as #4's headline number.
