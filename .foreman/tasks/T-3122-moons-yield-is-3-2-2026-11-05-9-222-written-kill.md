---
id: T-3122
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T03:14:57Z
updated: 2026-11-05T13:20:14Z
rival_at: 2026-11-05T04:50:37Z
rival_split: true
builder_model: haiku
base: 2b19d1a0be4d0d6cee82d0b4049f650b8ccc48a7
base_tree: 92b5e82582290f38115258afcfddc35b10a114ab
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T04:51:13Z
plan0_scope: []
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (640) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
lane_stop: merged 2026-11-05T13:15:39Z
verified: strong
unproven: [ui-unshot]
---
# Moons yield from 3.2% toward 10,000 kept: a 'go wilder' rewrite of medium-tier moons, cell prompts seeded with the cell's kept wild moons, a kept-per-call writer bench, and the fill's projected finish on the live page
## Raw request
> Moons yield is 3.2% (2026-11-05: 9,222 written, kill keeps 2,775 (30%), tier keeps 328 of 2,596 (87% rejected as low or medium wildness), novelty 292): 10,000 kept needs about 310,000 candidates at this rate. Raise yield: a 'go wilder' rewrite of each medium-tier moon (one child row, as kill's repair does), cell prompts seeded with that cell's kept high-tier moons, a kept-per-call bench of the writers (27B, 35B, Haiku, Sonnet) choosing the writer per stage, and the fill's projected finish date on the live page
## Interpretation
Reading 1 (chosen): measured 2026-11-05: of 9,222 written, kill keeps 30%, tier keeps 13% (87% of what reaches it rejected as low or medium wildness, the user's bar), novelty 89%: 3.2% overall, so 10,000 kept needs ~310,000 candidates; raise yield where it is lost: each medium-tier moon gets one 'go wilder' rewrite as a child row (as kill's repair does) judged again by tier, each cell's write prompt carries that cell's kept high-tier moons as exemplars, a bench of writers (27B, 35B, Haiku, Sonnet) on kept per call picks the writer per stage, and the live page shows kept per hour and the projected date for 10,000. Reading 2: lower the tier bar; rejected, the bar is the user's wild-moon standard.
## Assumptions (confidence)
## Acceptance criteria
- [x] a medium-tier moon gets one 'go wilder' rewrite as a child row with its parent, judged by tier again; a rewrite is never rewritten — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] a cell's write prompt carries up to 2 of that cell's kept high-tier moons as exemplars, never a rejected one — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] sampo moons bench-writers runs each writer on the same cells and reports kept per call per stage; the fill uses the best per stage; numbers in research — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] the live page shows kept moons per hour and the projected date for 10,000 — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: _repair's child-row pattern for the rewrite, _hints for exemplars, the funnel's per-row model field for the bench, T-3083's progress rows for the projection; likely outcome: tier yield up several fold. 2. Do less: exemplars only; fails if: the 2,255 medium rejects stay dead. 3. Generate far more with the same yield; fails if: 310,000 candidates take weeks of Jarvis. Choice 1 (75%)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: rewrite rows, exemplars, the writer bench, the projection
2. [x] the four changes
## Resume here
<!-- auto -->
- 2026-11-05T05:05:16Z step 1/3: failing tests: rewrite rows, exemplars, the writer bench, the projection
- git: worktree-agent-a22e97981c4c45d2f; 3 uncommitted: plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/tests/test_moons_scale.py
- touched since last checkpoint: plugin/tests/test_moons_scale.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/moonscale.py
## Docs impact
CHANGELOG line; bench-writers in genesis moonshot's help; load_picks and bench_writers docstrings say only the writer is taken
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -15` → ✗ exit 1 · Ran 99 tests in 11.6s (19 classes, 16 at a time; slowest: StoreLock 8s, KeepGrow 7s, Yield 7s) / FAILED (8 classes: test_moons_scale.Yield, test_moons_scale.Writers, test_moons_scale.Funnel, test_moon [ran] [tree b3cdadcb73ac] [world 2f1906870a] (2026-11-05T04:59:01Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -15` → ✗ exit 1 · Ran 99 tests in 11.6s (19 classes, 16 at a time; slowest: StoreLock 8s, KeepGrow 7s, Yield 7s) / FAILED (8 classes: test_moons_scale.Yield, test_moons_scale.Writers, test_moons_scale.Funnel, test_moon [ran] [tree b3cdadcb73ac] [world 2f1906870a] (2026-11-05T04:59:01Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -15` → ✗ exit 1 · Ran 99 tests in 11.6s (19 classes, 16 at a time; slowest: StoreLock 8s, KeepGrow 7s, Yield 7s) / FAILED (8 classes: test_moons_scale.Yield, test_moons_scale.Writers, test_moons_scale.Funnel, test_moon [ran] [tree b3cdadcb73ac] [world 2f1906870a] (2026-11-05T04:59:01Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 99 tests in 3.1s (19 classes, 16 at a time; slowest: Yield 3s, Grow 3s, StoreLock 2s) / FAILED (12 classes: test_moons_scale.Yield, test_moons_scale.Grow, test_moons_scale.Writers, test_moons_scal [ran] [tree 0ca9ff77179b] [world 2f1906870a] (2026-11-05T05:04:07Z)
- (step 2) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 86 tests in 144.6s (11 classes, 16 at a time; slowest: Page 144s, Serve 17s, Act 16s) / OK [ran] [tree c25d71113079] [world 2f1906870a] (2026-11-05T05:11:46Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_guard test_instruments test_left_out test_library test_live test_live_page test_models test_moons_scale test_motion_verify test_playbook_check test_playbook_machinery test_rename_scan test_scaffold test_small_cards test_smoke test_smoke_profiles test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [27.50s] [ran] [tree c25d71113079] [world 2f1906870a] (2026-11-05T05:14:45Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale test_live` → exit 0 · Ran 198 tests in 23.0s (114 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 23s, Page.test_the_network_view_draws_three_columns_and_pulse [ran] [tree 4b9b2e6e5e23] [world 2f1906870a] (2026-11-05T13:16:22Z)
- `python3 plugin/tests/run.py test_moons_scale.Writers` → ✗ exit 1 · Ran 10 tests in 3.1s (10 jobs, 16 at a time; slowest: Writers.test_the_fill_uses_the_picked_writer_for_the_write_and_each_judge_stage 2s, Writers.test_the_best_per_stage_wins_a_tie_goes_to_the_free_wr [ran] [tree 9f9ee5e90275] [world 2f1906870a] (2026-11-05T13:17:18Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale test_live` → exit 0 · Ran 199 tests in 31.2s (146 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 31s, Page.test_the_network_view_draws_three_columns_and_pulse [ran] [tree c6117d0642e0] [world 2f1906870a] (2026-11-05T13:18:06Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 113 tests in 6.0s (65 jobs, 16 at a time; slowest: KeepGrow.test_a_model_whose_rows_all_fail_admit_stalls_with_no_max_calls 5s, Wilder.test_a_rewrite_is_never_rewritten_and_a_parent_never_twice 5s [ran] [tree 308b40164580] [world 2f1906870a] (2026-11-05T13:19:02Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 113 tests in 6.0s (65 jobs, 16 at a time; slowest: KeepGrow.test_a_model_whose_rows_all_fail_admit_stalls_with_no_max_calls 5s, Wilder.test_a_rewrite_is_never_rewritten_and_a_parent_never_twice 5s [ran] [tree 308b40164580] [world 2f1906870a] (2026-11-05T13:19:02Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 113 tests in 6.0s (65 jobs, 16 at a time; slowest: KeepGrow.test_a_model_whose_rows_all_fail_admit_stalls_with_no_max_calls 5s, Wilder.test_a_rewrite_is_never_rewritten_and_a_parent_never_twice 5s [ran] [tree 308b40164580] [world 2f1906870a] (2026-11-05T13:19:02Z)
- (ac 4) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 86 tests in 21.5s (75 jobs, 16 at a time; slowest: Page.test_the_charts_are_drawn_from_one_kit_labelled_and_readable_in_both_schemes 21s, Page.test_the_network_view_draws_three_columns_and_pulses_ [ran] [tree 308b40164580] [world 2f1906870a] (2026-11-05T13:19:02Z)
- (audit intent) `re-ran test_moons_scale + test_live on main after the merge (199 OK); read bench_writers and load_picks; found that the fill adopted each judge stage's best kept-per-call, i.e. its laxest judge, and narrowed load_picks to the write stage (tests updated red-first, a new test pins it)` → AC1 rewrite once per medium moon (never a rewrite of a rewrite), AC2 exemplars only from the cell's kept high-tier moons, AC4 kept per hour and the 10,000 projection on the live page all hold; AC3's 'the fill uses the best per stage' is now the best writer only, a deliberate narrowing so the bench can't lower the bar for a kept moon; the live yield round moved to T-3202 [tree 308b40164580] (2026-11-05T13:19:02Z)
- (audit adversary) `re-ran test_moons_scale + test_live on main after the merge (199 OK); read bench_writers and load_picks; found that the fill adopted each judge stage's best kept-per-call, i.e. its laxest judge, and narrowed load_picks to the write stage (tests updated red-first, a new test pins it)` → Goodhart on the metric: a judge that keeps more is laxer, so letting kept-per-call pick judges would let the funnel grade itself easier; now a bench can only change who writes, while kill, tier and novelty keep the fill's own judges; a hand-edited writers.json naming judges is ignored (tested) [tree 308b40164580] (2026-11-05T13:19:02Z)
- (audit edge) `re-ran test_moons_scale + test_live on main after the merge (199 OK); read bench_writers and load_picks; found that the fill adopted each judge stage's best kept-per-call, i.e. its laxest judge, and narrowed load_picks to the write stage (tests updated red-first, a new test pins it)` → no writers.json or an unreadable one gives {} (default writer); a paid writer pick is still dropped for --local-only or a sensitive project [tree 308b40164580] (2026-11-05T13:19:02Z)
## Log
- 2026-11-05T03:14:57Z created
- 2026-11-05T04:46:50Z planned from capture
- 2026-11-05T04:46:50Z set approved=True
- 2026-11-05T04:50:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3122.builder.md
- 2026-11-05T04:51:12Z focused
- 2026-11-05T04:51:13Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T13:15:39Z merged worktree-agent-a22e97981c4c45d2f (7 file(s))
- 2026-11-05T13:15:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a22e97981c4c45d2f
- 2026-11-05T13:15:58Z focused
- 2026-11-05T13:18:19Z step 3 removed: a live round: yield before and after, in research
- 2026-11-05T13:20:12Z done
- 2026-11-05T13:20:14Z committed 76bebce4 (3 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a four-part change to the "moons" generation pipeline (write → kill → tier → novelty). (1) A "go wilder" rewrite stage for medium-tier moons that emits one child row per medium parent, the way kill's repair does. (2) Per-cell prompt seeding from that cell's kept high-tier moons. (3) A ke…
- Narrower: only the yield levers (rewrite, seeding, writer choice) are wanted, and the projected finish date is a side display. The 3.2% figure and the 310,000-candidate estimate would then be the success metric, not a deliverable.
- Bench-first: run the bench (`bench/`) before building anything, and let it decide which stages get which writer. Rewrite and seeding would then be built against the winning writers.
- Different yield definition: "kept" could mean surviving all stages (3.2% = 292/9,222 after novelty), or it could mean tier-kept only. The projection depends on which one, because 10,000 / 0.032 ≈ 312,500 only holds for the end-to-end definition.
Approaches:
- Add the rewrite as a new stage after tier. Medium-tier rows get a child row with a parent id, and the child re-enters tier and novelty. Reuse kill's repair code path for child-row creation so the lineage schema stays the same. Cap it at one generation of children so rewrites can't loop.
- Seed prompts by querying kept high-tier moons grouped by cell at prompt-build time and sampling a few as exemplars. Fall back to the unseeded prompt when a cell has no kept highs. Keep the seed sample small and rotating to limit homogeneity, since novelty is already a gate.
- Build the bench as a script in `bench/` that runs a fixed candidate batch through each writer at the same stage, then records kept-per-call (and cost) from the real kill/tier/novelty outcomes. Write the result to a config file that stage dispatch reads, so choosing a writer is data rather than code.
- Compute the projection from the rolling kept-per-day rate and the remaining gap to 10,000, and write it to a JSON status file. `plugin/web/live/index.html` reads that file. Show a range, not a single date, until the rate stabilizes.
Failure modes:
- Rewritten children inflate the "kept" count with near-duplicates of their parents. Novelty is the only guard, so it must compare children against their parent and siblings. Otherwise yield rises while real diversity falls.
- Seeding on kept high-tier moons creates a feedback loop. Cells converge on their own past output, and novelty rejections climb enough to cancel the tier gains.
- The bench measures kept-per-call on a small sample, so the writer choice is noise. It also ignores per-call cost and latency (Sonnet vs 27B), which can make the "best" writer the wrong one under the $200 budget.
- The projected date is wrong because the rate changes after the new stages ship. The old 3.2% would be mixed with the new rate, and the live page would show a confident date that moves daily. The projection must use only post-change data and show uncertainty.
## Dissent
- [x] rival reading: Narrower: only the yield levers (rewrite, seeding, writer choice) are wanted, and the projected finish date is a side display. The 3.2% figure and the 310,000-candidate estimate would then be the success metric, not a deliverable. — answered: rejected: the projection is part of the user's ask (10,000 kept and used, progress on the website); it is the smallest part and stays
- [x] rival reading: Bench-first: run the bench (`bench/`) before building anything, and let it decide which stages get which writer. Rewrite and seeding would then be built against the winning writers. — answered: rejected as an order: the bench runs inside the build (criterion 3), and rewrite and seeding don't depend on which writer wins
- [x] rival reading: Different yield definition: "kept" could mean surviving all stages (3.2% = 292/9,222 after novelty), or it could mean tier-kept only. The projection depends on which one, because 10,000 / 0.032 ≈ 312,500 only holds for the end-to-end definition. — answered: adopted: kept means surviving novelty (292 of 9,222 = 3.2%), the count the user's 10,000 is about; the research states both
- [x] rival approach: Add the rewrite as a new stage after tier. Medium-tier rows get a child row with a parent id, and the child re-enters tier and novelty. Reuse kill's repair code path for child-row creation so the lineage schema stays the same. Cap it at one generation of children so rewrites can't loop. — answered: adopted: the rewrite is a child row with a parent id through kill's repair path, re-entering tier and novelty; never rewritten twice
- [x] rival approach: Seed prompts by querying kept high-tier moons grouped by cell at prompt-build time and sampling a few as exemplars. Fall back to the unseeded prompt when a cell has no kept highs. Keep the seed sample small and rotating to limit homogeneity, since novelty is already a gate. — answered: adopted: exemplars come from that cell's kept high-tier moons at prompt-build time, up to 2, rotating, none when the cell has none
- [x] rival approach: Build the bench as a script in `bench/` that runs a fixed candidate batch through each writer at the same stage, then records kept-per-call (and cost) from the real kill/tier/novelty outcomes. Write the result to a config file that stage dispatch reads, so choosing a writer is data rather than code. — answered: adopted in part: a fixed candidate batch per writer recording kept per call from real stage outcomes, as a sampo verb (moons bench-writers) not a bench/ script, result in research
- [x] rival approach: Compute the projection from the rolling kept-per-day rate and the remaining gap to 10,000, and write it to a JSON status file. `plugin/web/live/index.html` reads that file. Show a range, not a single date, until the rate stabilizes. — answered: adopted: a rolling kept-per-hour rate gives a range until it steadies, shown on the live page from the snapshot
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- research T-2865-review: Verdict:** approve with nits. This covers only T-2865's own code, which in this diff is two later patches to moonscale.py, one hunk in rune.py an…
- T-2878 [FEATURE L, blocked, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- similar past tasks were L: consider --tier L
## Lessons
- A yield bench must hold the judge fixed: ranking judges by how much they keep selects the most lenient one
## Plan gaps
- failed first: step 1 failing tests: rewrite rows, exemplars, the writer bench, the projection
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/live.py
- plugin/web/live/index.html
- plugin/web/live/live.js
- plugin/tests/test_live.py
- CHANGELOG.md
- plugin/agents/fm-builder.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/doctor.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/night.py
- plugin/lib/sampo/which.py
- plugin/skills/next/SKILL.md
- plugin/tests/genesis_page.js
- plugin/tests/helpers.py
- plugin/tests/test_batch_edit.py
- plugin/tests/test_builder.py
- plugin/tests/test_cli.py
- plugin/tests/test_contract.py
- plugin/tests/test_docs.py
- plugin/tests/test_genesis.py
- plugin/tests/test_handoff.py
- plugin/tests/test_helpers_env.py
- plugin/tests/test_hooks.py
- plugin/tests/test_hunks.py
- plugin/tests/test_integrity.py
