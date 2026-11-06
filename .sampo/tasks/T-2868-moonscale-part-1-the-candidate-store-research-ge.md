---
id: T-2868
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T01:46:55Z
updated: 2026-11-04T02:10:57Z
rival_at: 2026-11-04T01:47:23Z
rival_split: true
builder_model: haiku
base: 3d1776caed881060d8c0ecb7c4716037ddbe5f5b
base_tree: 87abb155a866e2befc8ceb6feacc30cbdc1c7a99
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T01:48:01Z
plan0_scope: []
lane_stop: merged 2026-11-04T02:09:15Z
verified: strong
unproven: [docs, meaning]
---
# Moonscale part 1: the candidate store (research/genesis/moons/candidates.jsonl plus an append-only funnel log), write-time rules (the 'Today you can't / With this, you can' line required; internal-only payoff and missing or unfalsifiable kill tests rejected with a reason), the grid (problem x kind x mechanism x scale x surface) with coverage and thin cells first, and generation routed to the local llama-swap profile or Haiku, resumable and budget-capped (sampo moons grow, sampo moons coverage)
## Raw request
> Moonscale part 1: the candidate store (research/genesis/moons/candidates.jsonl plus an append-only funnel log), write-time rules (the 'Today you can't / With this, you can' line required; internal-only payoff and missing or unfalsifiable kill tests rejected with a reason), the grid (problem x kind x mechanism x scale x surface) with coverage and thin cells first, and generation routed to the local llama-swap profile or Haiku, resumable and budget-capped (sampo moons grow, sampo moons coverage)
## Interpretation
Reading 1 (chosen): the part of T-2865's plan its title names, built as T-2865's Interpretation, Approach and Build vs reuse describe (sampo/moonscale.py beside moons.py; candidates in research/genesis/moons/; no new dependency). Reading 2 (ruled out): scaling moonshot.md itself; T-2865 rules it out on cost and the cold read's size.
## Assumptions (confidence)
## Acceptance criteria
- [x] admit() keeps a moon with the line and a falsifiable kill test and rejects an internal-only or untestable one with its reason; the grid picks the thinnest cells first; grow appends batches routed local-first then Haiku, stops at --target or the budget, and resumes — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
1. Use what exists, as T-2865's Build vs reuse lists (moons.py, ideas.run_child, models.resolve/complete, budget.check, rune.put/export). Likely outcome: one module section and its tests. Fails if a model call can't be mocked; every call goes through one routing function the tests patch.
2. A separate service or vector store. Fails: a new dependency for stdlib work.
3. Do less: skip the routing and call Haiku only. Fails the steer's cost rule (local models first).
Choice 1 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: admit, grid coverage and thin-first, routing and resume with mocked models
2. [x] moonscale.py store, admit, grid, coverage, grow; the CLI verbs
## Resume here
<!-- auto -->
- 2026-11-04T02:01:06Z step 2/2: moonscale.py store, admit, grid, coverage, grow; the CLI verbs
- git: worktree-agent-a834dc4b3e1c6f1f5; 3 uncommitted: plugin/lib/fmmoonscale.py, plugin/lib/sampo/moonscale.py, plugin/tests/test_moons_scale.py
- touched since last checkpoint: plugin/tests/test_moons_scale.py, plugin/lib/sampo/moonscale.py, plugin/lib/fmmoonscale.py
## Docs impact
MASTER.md: the fmmoonscale entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -8` → ✗ exit 1 · Ran 16 tests in 1.5s (5 classes, 16 at a time; slowest: Grow 0s, Admit 0s, Route 0s) / FAILED (5 classes: test_moons_scale.Admit, test_moons_scale.Grow, test_moons_scale.Route, test_moons_scale.Store, [ran] [tree aa668809ba08] [world 2f1906870a] (2026-11-04T01:57:57Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 16 tests in 0.6s (5 classes, 16 at a time; slowest: Admit 0s, Route 0s, Grow 0s) / FAILED (5 classes: test_moons_scale.Admit, test_moons_scale.Grow, test_moons_scale.Route, test_moons_scale.Store, [ran] [tree aa668809ba08] [world 2f1906870a] (2026-11-04T01:58:00Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -60` → ✗ exit 1 · Ran 16 tests in 1.0s (5 classes, 16 at a time; slowest: Cli 1s, Route 1s, Store 1s) / FAILED (1 classes: test_moons_scale.Grow) [ran] [tree 952c217782fd] [world 2f1906870a] (2026-11-04T02:03:11Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -E "^(FAIL|ERROR):|Error:|Ran |OK|FAILED" | head -20` → ✗ exit 1 · Ran 19 tests in 0.9s (5 classes, 16 at a time; slowest: Grow 1s, Route 1s, Cli 1s) / FAILED (2 classes: test_moons_scale.Grow, test_moons_scale.Route) [ran] [tree edbc7dc66601] [world 2f1906870a] (2026-11-04T02:04:35Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -E "^(FAIL|ERROR):|Error:|Ran |OK|FAILED" | head -20` → exit 0 · Ran 19 tests in 0.8s (5 classes, 16 at a time; slowest: Grow 1s, Route 1s, Cli 0s) / OK [ran] [tree 903c763912fe] [world 2f1906870a] (2026-11-04T02:04:54Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -E "^(FAIL|ERROR):|Error:|Ran |OK|FAILED" | head -20` → exit 0 · Ran 19 tests in 0.8s (5 classes, 16 at a time; slowest: Grow 1s, Route 1s, Cli 0s) / OK [ran] [tree 903c763912fe] [world 2f1906870a] (2026-11-04T02:04:54Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 19 tests in 0.8s (5 classes, 16 at a time; slowest: Grow 1s, Route 1s, Cli 0s) / OK [ran] [tree 903c763912fe] [world 2f1906870a] (2026-11-04T02:05:03Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_moons_scale test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.66s] [ran] [tree 903c763912fe] [world 2f1906870a] (2026-11-04T02:05:44Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 19 tests in 0.8s (5 classes, 16 at a time; slowest: Grow 1s, Route 0s, Cli 0s) / OK [ran] [tree 8115e58c8ef1] [world 2f1906870a] (2026-11-04T02:10:07Z)
- `python3 plugin/tests/run.py test_moons_scale test_moonshot` → exit 0 · Ran 34 tests in 0.9s (12 classes, 16 at a time; slowest: Climb 1s, Grow 1s, Route 1s) / OK [ran] [tree 8115e58c8ef1] [world 2f1906870a] (2026-11-04T02:10:07Z)
- (audit intent) `builder self-review (two holes fixed test-first: a run-wide paid cap so many small calls can't dodge the per-command cap; wrapped JSON replies parsed) plus my read of admit and the prompt: the four write rules (line, internal-only payoff, falsifiable kill, plain English) reject with a headed reason and are stored, so the funnel counts them` → the steer's write-time rules hold at write; the grid fills thin cells first; generation goes local-first then Haiku [tree 8115e58c8ef1] (2026-11-04T02:10:07Z)
- (audit edge) `builder self-review (two holes fixed test-first: a run-wide paid cap so many small calls can't dodge the per-command cap; wrapped JSON replies parsed) plus my read of admit and the prompt: the four write rules (line, internal-only payoff, falsifiable kill, plain English) reject with a headed reason and are stored, so the funnel counts them` → resume replays ids and batch numbers; stops at target, max-calls, budget or 3 failed calls in a row; open: two concurrent grows can share a batch number (ids are lock-safe), --target counts rejected rows [tree 8115e58c8ef1] (2026-11-04T02:10:07Z)
- (audit adversary) `builder self-review (two holes fixed test-first: a run-wide paid cap so many small calls can't dodge the per-command cap; wrapped JSON replies parsed) plus my read of admit and the prompt: the four write rules (line, internal-only payoff, falsifiable kill, plain English) reject with a headed reason and are stored, so the funnel counts them` → every model reply is data: parsed as JSON and admitted field by field, never run; the local profile's key is read only from its env var by the model layer [tree 8115e58c8ef1] (2026-11-04T02:10:07Z)
## Log
- 2026-11-04T01:46:55Z created
- 2026-11-04T01:47:32Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2868.builder.md
- 2026-11-04T01:48:00Z focused
- 2026-11-04T01:48:01Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T02:09:15Z merged worktree-agent-a834dc4b3e1c6f1f5 (5 file(s))
- 2026-11-04T02:09:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a834dc4b3e1c6f1f5
- 2026-11-04T02:09:23Z focused
- 2026-11-04T02:10:56Z done
- 2026-11-04T02:10:57Z committed 5570d538 (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a new `sampo moons` subcommand group (`grow`, `coverage`) in `plugin/lib/sampo/cli.py`, backed by a new module (e.g. `plugin/lib/sampo/moons.py` or `fmmoons.py`, following the `fmX.py` / `sampo/X.py` pairing seen in `fmambient.py` / `sampo/ambient.py`). It owns the candidate store `resea…
- Narrower: only the store and write-time validator ship now (a library plus tests), and `grow`/`coverage` are stubs. "Part 1" could mean the grid and generation come in later parts, but the request names the commands explicitly, so this reading is less likely.
- Alternative: moons are an extension of the existing genesis system (`plugin/lib/fmgenesis.py`, `site/genesis/index.html`) and should reuse its candidate or idea schema and its rendering, rather than being a separate store.
- Alternative: "grid" means a persisted, user-editable config of axis values (problem, kind, mechanism, scale, surface), as opposed to one derived from the candidates already stored. This changes where coverage gets its denominator.
Approaches:
- Pure-function core plus thin CLI: `validate_candidate(dict) -> (ok, reason)` enforces the "Today you can't / With this, you can" line, rejects internal-only payoff, and rejects a missing or unfalsifiable kill test. `append_candidate` writes to the JSONL and also logs accepted or rejected-with-reaso…
- Grid as the cross product of axis enums defined in one module. `coverage` counts candidates per cell by reading the store, sorts ascending, and `grow` picks the thinnest cells first. A cell is the tuple key, so the sort is stable and deterministic for tests.
- Generation behind a small backend interface with two implementations: the local llama-swap profile (an HTTP call to an OpenAI-compatible endpoint, with the profile name from config) and Haiku (`claude-haiku-5-5`). Selection is by flag or config, with fallback when llama-swap is unreachable.
- Resumability and budget cap come from the funnel log rather than a separate state file. On start, `grow` replays the log to learn which cells are already done and how much has been spent. It appends a cost record per call and stops once the cap is reached. A `--budget` flag defaults from config.
Failure modes:
- The unfalsifiable kill-test check is semantic. A regex or keyword heuristic will either pass vague tests ("it works well") or reject good ones. The rule needs concrete structure (a metric, threshold, or observable event) and a fixture of both good and bad examples, or the reason text will be unreli…
- An interrupted run can leave the JSONL and funnel log inconsistent (a candidate written but not logged, or the reverse), and a torn last line breaks resume. Appends need to be a single write per line with a newline, and the reader must tolerate a truncated final line. Otherwise resume double-counts…
- Budget accounting for llama-swap has no dollar cost, and Haiku costs come from token usage that may be missing from a failed or streamed response. If the cap counts only Haiku calls, or the local cost is treated as zero with no call limit, a loop in a thin cell can run unbounded. The cap needs a ca…
- Models will emit near-duplicate candidates, and the thin-cells-first rule keeps hitting the same cell if rejections never add to coverage. Without dedup on the store and a per-cell attempt cap in the funnel log, `grow` loops on a cell whose output keeps failing validation and burns budget without r…
## Dissent
- [x] rival reading: Likeliest: a new `sampo moons` subcommand group (`grow`, `coverage`) in `plugin/lib/sampo/cli.py`, backed by a new module (e.g. `plugin/lib/sampo/moons.py` or `fmmoons.py`, following the `fmX.py` / `sampo/X.py` pairing seen in `fmambient.py` / `sampo/ambient.py`). It owns the candidate store `resea… — answered: adopted: sampo moons grow and coverage as genesis moonshot verbs (the moons alias), backed by a new sampo/moonscale.py
- [x] rival reading: Narrower: only the store and write-time validator ship now (a library plus tests), and `grow`/`coverage` are stubs. "Part 1" could mean the grid and generation come in later parts, but the request names the commands explicitly, so this reading is less likely. — answered: rejected: part 1 ships grow and coverage working end to end; part 2 adds the funnel
- [x] rival reading: Alternative: moons are an extension of the existing genesis system (`plugin/lib/fmgenesis.py`, `site/genesis/index.html`) and should reuse its candidate or idea schema and its rendering, rather than being a separate store. — answered: adopted in part: moons live in the Rune tower (rune.home), beside moonshot.md, and reuse its fields' names (Domain, Lens, Kill, Prior art) where they mean the same
- [x] rival reading: Alternative: "grid" means a persisted, user-editable config of axis values (problem, kind, mechanism, scale, surface), as opposed to one derived from the candidates already stored. This changes where coverage gets its denominator. — answered: adopted in part: the axes are constants in moonscale.py except problems, read from Sampo's own records (friction, steers, escapes, blocked tasks, the user's projects); no user-edited config
- [x] rival approach: Pure-function core plus thin CLI: `validate_candidate(dict) -> (ok, reason)` enforces the "Today you can't / With this, you can" line, rejects internal-only payoff, and rejects a missing or unfalsifiable kill test. `append_candidate` writes to the JSONL and also logs accepted or rejected-with-reaso… — answered: adopted: admit(row) -> (ok, reason) is a pure function
- [x] rival approach: Grid as the cross product of axis enums defined in one module. `coverage` counts candidates per cell by reading the store, sorts ascending, and `grow` picks the thinnest cells first. A cell is the tuple key, so the sort is stable and deterministic for tests. — answered: adopted: the cross product of the axes; coverage counts per cell from the store; grow picks the thinnest
- [x] rival approach: Generation behind a small backend interface with two implementations: the local llama-swap profile (an HTTP call to an OpenAI-compatible endpoint, with the profile name from config) and Haiku (`claude-haiku-5-5`). Selection is by flag or config, with fallback when llama-swap is unreachable. — answered: adopted in part: one routing function (local profile when keyed and answering, else Haiku through ideas.run_child) the tests patch, not a class hierarchy
- [x] rival approach: Resumability and budget cap come from the funnel log rather than a separate state file. On start, `grow` replays the log to learn which cells are already done and how much has been spent. It appends a cost record per call and stops once the cap is reached. A `--budget` flag defaults from config. — answered: adopted: grow replays candidates.jsonl to know what exists; the budget comes from budget.check per call, not a separate state file
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, planned, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-fi…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- T-2869 [FEATURE M, planned, 2 steps] Moonscale part 2: the funnel over candidates, cheapest first (exact then embedding dedupe through a new models.embed on the OpenAI e…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
## Why not caught
none: a new feature
## Lessons
- a per-call budget cap is dodged by a loop of small calls: cap the run's total too
## Plan gaps
- failed first: step 1 red tests: admit, grid coverage and thin-first, routing and resume with mocked models
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/fmmoonscale.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/cli.py
- MASTER.md
