---
id: T-2502
type: FEATURE
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-11-01T19:16:31Z
updated: 2026-11-01T20:31:25Z
rival_at: 2026-11-01T19:47:21Z
base: 9530de63b787d65481dcf93fc9f24a06952e459c
base_tree: 79afa843aa2ec0b853e0170f248370943db55217
plan0_at: 2026-11-01T20:11:45Z
plan0_scope: []
verified: strong
---
# Redraw the gap map each generation against current code (one recon per capability) and…
## Raw request
> FEATURE!: redraw the gap map each generation against current code (one recon per capability) and rank the next Seed's Missions by expected value from that map, the exam scorecard, outcome survival and the cross-cutting review; empty coverage cells only break ties; fm genesis sweep goes red when the gap map predates the generation's last commit or the seed's order ignores the value scores
> DONE-WHEN: the seed writer's rank key is expected value with empty cells last, and the sweep row checks the gap map's date and the seed's order
## Interpretation
Readings: (a) likeliest: a gap-map stage after the review and before the sweep: the session runs one recon per capability against the current code and files gen-N/gap-map.md as a table (capability, tier 1-4, evidence path, what is missing); the next seed ranks Missions by an expected-value score built from that tier, the exam scorecard's verdict, outcome survival losses and the review's gap rows, with empty coverage cells only a tiebreaker; the sweep goes red when the map is missing, older than the review, or skips a gen-0 capability. (b) Redraw the root gap-map.md in place: rejected, a per-generation file keeps each map beside the generation it ranked. Fails if: recon subagents are paused (economy); then the session redraws from targeted reads, and the map records how each row was grounded.
## Assumptions (confidence)
## Acceptance criteria
- [x] the seed ranks Missions by an expected-value score from gen-N/gap-map.md's tier, the exam verdict, survival losses and review gap rows, printing each score's parts, empty cells only a tiebreaker; the sweep row is red when gen-N/gap-map.md is missing, older than the review, or skips a gen-0 capability; step names the redraw after the review — verify with `python3 plugin/tests/run.py test_genesis.GapMapValue`
## Non-goals
## Approach (options → choice → why)
1) gen-N/gap-map.md table + _ev(p, n, area) = tier + exam (fail 3, ungraded 2, pass 0) + 3 x survival-lost share of the area's Mission tasks + 2 x review gap rows naming it; the seed's rank key becomes (-ev, -empty, -open) and the seed prints each Mission's score parts; step() and the sweep check the map. Fails if: the score's weights are arbitrary (they are printed with each rank, so a critique can argue them). 2) A model ranks the Missions from the four inputs. Fails if: an unscored opinion orders the generation, and it can't be checked mechanically. 3) use what exists: keep the coverage rank and add the scorecard as a first key. Fails if: empty cells still decide every tie and the gap map never enters. 4) do less: rank by exam verdict alone. Fails if: survival and review findings, which the user named, are dropped. Choice 1 (80%): every input the user named enters one printed score; empty cells only break ties.
## Risks and rollback
A capability with no exam yet scores 2 on exam, so ungraded areas outrank passing ones: intended (unknown is a gap). The weights live in one tuple, printed in each seed. Rollback: revert; old seeds stay as written.
## Execution prompt
## Steps
1. [x] red tests: GapMapValue (table parse, _ev parts, seed order with a tie broken by empty cells, sweep row, step stage)
2. [x] gap-map table parser + _ev + seed rank key and printed parts + sweep row + step stage
3. [x] docs: genesis skill, MASTER, README, CHANGELOG
4. [x] spike: coverage areas, scorecard rows and gap-map rows match by the lowercased bare capability name (_seed's caps dict already keys that way), so no new naming layer
## Resume here
## Docs impact
plugin/skills/genesis/SKILL.md, README.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 194 tests in 23.1s (20 classes, 16 at a time; slowest: GenesisRead 23s, GenerationReview 20s, GenesisCheck 18s) / OK [ran] [tree cd7bd3e7804a] (2026-11-01T20:15:32Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 194 tests in 22.0s (20 classes, 16 at a time; slowest: GenesisRead 22s, GenerationReview 19s, GenesisCheck 17s) / OK [ran] [tree cd7bd3e7804a] (2026-11-01T20:15:55Z)
- `python3 plugin/tests/run.py test_genesis.GapMapValue` → ✗ exit 1 · Ran 4 tests in 2.6s (1 classes, 16 at a time; slowest: GapMapValue 1s) / FAILED (1 classes: test_genesis.GapMapValue) (start tree + this task's tests) [ran] [tree cd7bd3e7804a] (2026-11-01T20:15:59Z)
- `python3 plugin/tests/run.py test_genesis.GapMapValue` → exit 0 · Ran 4 tests in 1.1s (1 classes, 16 at a time; slowest: GapMapValue 1s) / OK [ran] [tree cd7bd3e7804a] (2026-11-01T20:15:59Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_skills` → exit 0 · Ran 104 tests in 11.7s (25 classes, 16 at a time; slowest: Fences 11s, DocsProof 6s, TaskLifecycle 3s) / OK [ran] [tree fded83ca6f46] (2026-11-01T20:16:31Z)
- (step 4) `python3 plugin/tests/run.py test_genesis.GapMapValue` → exit 0 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: GapMapValue 1s) / OK [ran] [tree fded83ca6f46] (2026-11-01T20:16:33Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GapMapValue` → exit 0 · Ran 4 tests in 0.6s (1 classes, 16 at a time; slowest: GapMapValue 0s) / OK [ran] [tree fded83ca6f46] (2026-11-01T20:23:05Z)
- (audit intent) `main-thread five-lens review of the diff (subagents paused); one finding captured as T-2509` → the user's part 2 holds: a per-generation gap map drawn after the review and stamped with its commit; the next seed ranks Missions by a printed expected-value score from the map's tier, the scorecard, survival and review gaps; empty cells only break ties; the sweep and step enforce the map [tree fded83ca6f46] (2026-11-01T20:23:05Z)
- (audit adversary) `main-thread five-lens review of the diff (subagents paused); one finding captured as T-2509` → the gap map is a put tower doc, so it passes the same cold read as the others; its Drawn at must be a real commit at or after the review's, so a stale or invented stamp turns the row red [tree fded83ca6f46] (2026-11-01T20:23:05Z)
- (audit edge) `main-thread five-lens review of the diff (subagents paused); one finding captured as T-2509` → a gen-0 with no numbered §2 has no scorecard and still ranks on the other inputs; a review without a commit stamp skips the order check; review gaps are counted by substring (T-2509 captured) [tree fded83ca6f46] (2026-11-01T20:23:05Z)
- (audit operator) `main-thread five-lens review of the diff (subagents paused); one finding captured as T-2509` → the redraw is session work (one recon per capability when subagents are allowed, targeted reads otherwise); step names it with its exact put command [tree fded83ca6f46] (2026-11-01T20:23:05Z)
- (audit maintainer) `main-thread five-lens review of the diff (subagents paused); one finding captured as T-2509` → the rank lives in one function (_mission_rank) with one weights table (EV_WEIGHTS) printed in each seed; T-2482's capability-first and T-2474's empty-first keys are retired in one place, and selected()/mapped() keep older fixtures valid [tree fded83ca6f46] (2026-11-01T20:23:05Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree fded83ca6f46] (2026-11-01T20:25:17Z)
## Log
- 2026-11-01T19:16:31Z created
- 2026-11-01T19:47:06Z planned: it has criteria and steps
- 2026-11-01T20:11:44Z set approved=True
- 2026-11-01T20:11:45Z focused
- 2026-11-01T20:16:00Z scope: fmgenesis gap map (SHAPE, _gap_rows, _mission_rank, EV_WEIGHTS, _gapmap_row, seed rank and section, review Drawn at, step stage), test_genesis GapMapValue + selected()/mapped()/reviewed() helpers, genesis SKILL.md, README, MASTER, CHANGELOG
- 2026-11-01T20:24:46Z done
- 2026-11-01T20:24:49Z committed fbb6e81d (6 files)
- 2026-11-01T20:25:17Z guard authorization added: publish
- 2026-11-01T20:31:25Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuse: scorecard() for exam verdicts, fmoutcomes.outcomes for survival, _review_gaps, coverage() for the tiebreak, the seed's table. Build: the gap-map table parser, _ev, one sweep row, one step stage.
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Full pipeline change (likeliest):** per-generation gap-map redraw (one recon per capability against current code), a seed writer that ranks Missions by expected value (EV) computed from gap map + exam scorecard + outcome survival + cross-cutting review (empty coverage cells only as tiebreak, sort…
- **Narrow reading (DONE-WHEN literal):** only change the seed writer's sort key (EV desc, empty cells last) and add the sweep check; assume the gap map, scorecard, survival and review inputs already exist and the recon-per-capability redraw is already implemented or out of scope.
- **Redraw-only reading:** the headline is the gap map regeneration step per generation, with ranking and sweep as downstream consequences.
- **Ordering semantic ambiguity:** "empty cells only break ties" could mean empty coverage is a secondary key among equal EV, versus "empty last" in DONE-WHEN meaning a hard partition (all non-empty before any empty). These differ when an empty-cell Mission has higher EV.
Approaches:
- **Locate and extend existing genesis code:** find the seed writer and the `genesis sweep` rows in `plugin/lib/fmcli.py` / `plugin/lib/fmcore.py` (and any `fmgenesis*` module, plus `plugin/skills/` genesis skill text); replace the seed writer's sort with `key=(-ev, is_empty, name)` where `ev` is a p…
- **Sweep row via recompute:** the new row re-derives EV from the persisted inputs, re-sorts, compares with the seed's Mission order, and compares the gap map's recorded date/commit against the generation's last commit (`git log -1` of the generation range); red on either mismatch with a message nami…
- **Gap map stamp:** have the redraw write the HEAD sha and timestamp into the gap map header, and have the sweep compare the sha (not mtime) to the generation's last commit, to avoid file-touch false greens.
- **Skill/doc-driven redraw:** if the recon is run by a skill (one subagent per capability) rather than Python, encode the "redraw each generation" rule in the genesis skill under `plugin/skills/` and add the stamp requirement there, with Python only validating.
Failure modes:
- **Tie/empty semantics wrong:** implementing empty cells as an EV bonus/penalty or as a pure tiebreak, when DONE-WHEN says "empty last"; the sweep and writer then agree with each other but not with the spec, and the order differs for a high-EV empty-cell Mission.
- **Writer and sweep use different EV code:** a duplicated formula means sweep passes or fails spuriously; float EV ties and unstable sort make the order nondeterministic, so the sweep goes red on a seed the writer just produced.
- **Staleness compared by mtime or wrong "last commit":** checking file date instead of recorded sha, or using repo HEAD instead of the generation's last commit, flags a fresh map red after any unrelated commit (or misses staleness after a rebase); also newly-red sweep breaks `fm doctor`/`plugin/test…
- **Missing inputs treated as zero:** a capability lacking an exam score, survival outcome, or review entry silently gets EV 0 and sinks to the bottom, indistinguishable from "empty cell", so the sweep goes green on a seed that ignores real value.
## Dissent
- [x] rival reading: **Narrow reading (DONE-WHEN literal):** only change the seed writer's sort key (EV desc, empty cells last) and add the sweep check; assume the gap map, scorecard, survival and review inputs already exist and the recon-per-capability redraw is already implemented or out of scope. — answered: rejected: the user asked for the map to be redrawn each generation; a sort key over a stale map would rank on old evidence
- [x] rival reading: **Redraw-only reading:** the headline is the gap map regeneration step per generation, with ranking and sweep as downstream consequences. — answered: rejected: the user named the ranking and the tiebreak as the point; the redraw is its input, built in the same task
- [x] rival reading: **Ordering semantic ambiguity:** "empty cells only break ties" could mean empty coverage is a secondary key among equal EV, versus "empty last" in DONE-WHEN meaning a hard partition (all non-empty before any empty). These differ when an empty-cell Mission has higher EV. — answered: adopted: empty cells are a secondary key among equal scores only (the user: a tiebreaker, never the ranking), not a partition; the test pins a tie broken by empty cells
- [x] rival approach: **Locate and extend existing genesis code:** find the seed writer and the `genesis sweep` rows in `plugin/lib/fmcli.py` / `plugin/lib/fmcore.py` (and any `fmgenesis*` module, plus `plugin/skills/` genesis skill text); replace the seed writer's sort with `key=(-ev, is_empty, name)` where `ev` is a p… — answered: adopted: it extends fmgenesis's _seed rank key and sweep() rows, where the coverage rank lives today
- [x] rival approach: **Sweep row via recompute:** the new row re-derives EV from the persisted inputs, re-sorts, compares with the seed's Mission order, and compares the gap map's recorded date/commit against the generation's last commit (`git log -1` of the generation range); red on either mismatch with a message nami… — answered: adopted: the sweep row recomputes the scores and checks the seed's Mission order against them
- [x] rival approach: **Gap map stamp:** have the redraw write the HEAD sha and timestamp into the gap map header, and have the sweep compare the sha (not mtime) to the generation's last commit, to avoid file-touch false greens. — answered: adopted: gap-map.md carries a 'Drawn at: <HEAD sha>' line; the sweep compares it with the review's inputs, never the file's mtime
- [x] rival approach: **Skill/doc-driven redraw:** if the recon is run by a skill (one subagent per capability) rather than Python, encode the "redraw each generation" rule in the genesis skill under `plugin/skills/` and add the stamp requirement there, with Python only validating. — answered: adopted in part: the genesis skill names the per-capability recon (a subagent when budget allows, targeted reads otherwise); the code checks the file, not who drew it
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- T-2501 [FEATURE L, done, 4 steps] Generation cross-cutting review: after the Mission critiques, one cold reviewer on a… — lesson: a new genesis stage needs the shared te…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
## Lessons
- a ranking a reader can't check is an opinion: printing each score's parts in the seed makes the order arguable in a critique
## Plan gaps
- added late: spike: coverage areas, scorecard rows and gap-map rows match by the lowercased bare capability name (_seed's caps dict …
## Files touched
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/skills/genesis/SKILL.md
