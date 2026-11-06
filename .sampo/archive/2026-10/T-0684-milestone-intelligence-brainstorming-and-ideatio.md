---
id: T-0684
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:16Z
updated: 2026-10-09T19:45:45Z
batch: [T-0605, T-0606, T-0607, T-0627, T-0628]
base: 0fb22eacbe05843baf3bc4fcbd402248fe8bbecd
base_tree: cbb8faf0c5d25380f1275cc129597a3e28714281
verified: strong
---
# Milestone: Intelligence — Brainstorming and ideation
## Raw request
> T-0605: FEATURE: Know when to stop brainstorming (I025, value 4/5, effort M, risk low)
>   first version: Add a coverage map (cluster counts by capability axis, from the category tags ideas already carry) and a 'holes' pack line listing empty or thin categories fed to the next --rounds pass; reuse the existing category regex.
>   what it is: Detects saturation, maps coverage and feeds holes back into the next round.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 6 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0606: FEATURE: Rank and triage ideas (I026, value 4/5, effort M, risk low)
>   first version: First version: a tool-less 'kill it fast' child (via fmsecond-style _child) that gets each cluster's one-line claim and returns a one-line falsifier, stored beside the grounding; tournament and novelty score skipped as lower value than the falsifier.
>   what it is: Ranks by tournament, falsifies in one line, clusters duplicates and measures novelty.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 9 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0607: FEATURE: Learn which ideas the user keeps (I027, value 4/5, effort M, risk low)
>   first version: Record each brainstorm catalogue's cluster->lens->mark, then on later turns join to briefs that were actually built/kept/dropped to produce per-lens keep rates in fm taste; use it to choose default lenses and --deepen. Needs the catalogue stored structurally (research add already holds it).
>   what it is: Backtests the ideator and lenses against what the user kept and dropped.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0627: FEATURE: Reframe before ideating (I023, value 3/5, effort S, risk low)
>   first version: First version: a 'flip assumptions' lens plus a 'reframe' lens added to fm ideas lenses and an assumption-flip bullet in R1 of intake/planning.md (Assumptions section already exists to flip).
>   what it is: Climbs the abstraction ladder, flips assumptions and distils insights as reframings.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0628: FEATURE: Wild idea generators (I028, value 3/5, effort S, risk low)
>   first version: First step: 3 extra optional lenses (oblique provocation from fm recall of past lessons and failures, devil's idea, worst-bugs persona) as prompt text only; cross-breeding as a final fm ideas round that combines top ideas. Cheap since lens infra exists.
>   what it is: Provocations, cross-breeding, devil's ideas and persona-driven brainstorms.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0605, T-0606, T-0607, T-0627, T-0628 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0684. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0605: Know when to stop brainstorming (I025, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_ideation.py -k Coverage`
- [x] T-0606: Rank and triage ideas (I026, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_ideation.py -k Falsify`
- [x] T-0607: Learn which ideas the user keeps (I027, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_ideation.py -k KeepRates`
- [x] T-0627: Reframe before ideating (I023, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_ideation.py -k Lenses`
- [x] T-0628: Wild idea generators (I028, value 3/5, effort S, risk low) works — verify with `python3 plugin/tests/run.py -p test_ideation.py -k Crossbreed`
## Non-goals
## Approach (options → choice → why)
All inside fm ideas and fm taste, children stubbed in tests. T-0605: ideas.md gains a coverage map (ideas per category, from the category tags lenses already return) and the thin categories among a fixed capability axis list; later rounds' pack names them as holes to fill. T-0606: --falsify runs one tool-less child over every title and stores a one-line kill-it-fast test beside each idea (one call, not one per cluster). T-0607: each brainstorm writes ideas.json (lens → titles); fm taste joins titles to briefs by shared words and shows per-lens built/dropped/open rates. T-0627/T-0628: lenses 'reframe', 'flip assumptions', 'oblique provocation' (its pack gets the latest lessons), 'devil's idea', 'worst-bugs persona', each with a one-line note in the child prompt; --crossbreed adds one child that combines the top ideas; planning.md gets an assumption-flip bullet. Options: a tournament per cluster or novelty scoring — more calls for less than the falsifier.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0605: Know when to stop brainstorming (I025, value 4/5, effort M, risk low)
2. [x] T-0606: Rank and triage ideas (I026, value 4/5, effort M, risk low)
3. [x] T-0607: Learn which ideas the user keeps (I027, value 4/5, effort M, risk low)
4. [x] T-0627: Reframe before ideating (I023, value 3/5, effort S, risk low)
5. [x] T-0628: Wild idea generators (I028, value 3/5, effort S, risk low)
## Resume here
## Docs impact
CHANGELOG; MASTER.md fmideas; intake planning R1
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_ideation.py` → ✗ exit 1 · Ran 5 tests in 0.2s (5 classes, 16 at a time; slowest: Coverage 0s, KeepRates 0s, Falsify 0s) / FAILED (5 classes) [ran] [tree e34629335a80] (2026-10-09T19:42:12Z)
- (step 1) `python3 plugin/tests/run.py -p test_ideation.py -k Coverage` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Coverage 0s) / OK [ran] [tree cd2491a682a7] (2026-10-09T19:43:23Z)
- (step 2) `python3 plugin/tests/run.py -p test_ideation.py -k Falsify` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Falsify 0s) / OK [ran] [tree cd2491a682a7] (2026-10-09T19:43:24Z)
- (step 3) `python3 plugin/tests/run.py -p test_ideation.py -k KeepRates` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: KeepRates 1s) / OK [ran] [tree cd2491a682a7] (2026-10-09T19:43:25Z)
- (step 4) `python3 plugin/tests/run.py -p test_ideation.py -k Lenses` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Lenses 0s) / OK [ran] [tree cd2491a682a7] (2026-10-09T19:43:25Z)
- (step 5) `python3 plugin/tests/run.py -p test_ideation.py -k Crossbreed` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Crossbreed 0s) / OK [ran] [tree cd2491a682a7] (2026-10-09T19:43:26Z)
- (ac 1) `python3 plugin/tests/run.py -p test_ideation.py -k Coverage` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Coverage 0s) / OK [ran] [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
- (ac 2) `python3 plugin/tests/run.py -p test_ideation.py -k Falsify` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Falsify 0s) / OK [ran] [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
- (ac 3) `python3 plugin/tests/run.py -p test_ideation.py -k KeepRates` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: KeepRates 1s) / OK [ran] [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
- (ac 4) `python3 plugin/tests/run.py -p test_ideation.py -k Lenses` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Lenses 0s) / OK [ran] [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
- (ac 5) `python3 plugin/tests/run.py -p test_ideation.py -k Crossbreed` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Crossbreed 0s) / OK [ran] [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
- (audit intent) `self review of the five members in fmideas, fm taste and planning; full suite` → each member's first version shipped as its note asked: coverage map and holes, one falsifier child, per-lens keep rates from structured catalogues, reframing lenses with the planning flip, wild lenses and a cross-breed round [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
- (audit edge) `self review of the five members in fmideas, fm taste and planning; full suite` → repeated ideas across rounds count once in coverage; --falsify and --crossbreed are optional passes whose failure leaves the catalogue intact; an idea matches a brief when most of its words are in the title; lenses without notes keep the old prompt so cached prefixes stay the same [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
- (audit operator) `self review of the five members in fmideas, fm taste and planning; full suite` → the two optional passes are one child call each, budget-checked like every lens; nothing runs unless asked [tree 32f5e0433dfd] (2026-10-09T19:43:40Z)
## Log
- 2026-10-09T15:40:16Z created
- 2026-10-09T19:41:55Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_ideation.py -k Coverage`
- 2026-10-09T19:41:55Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_ideation.py -k Falsify`
- 2026-10-09T19:41:55Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_ideation.py -k KeepRates`
- 2026-10-09T19:41:55Z criterion 4 verify: `` → `python3 plugin/tests/run.py -p test_ideation.py -k Lenses`
- 2026-10-09T19:41:55Z criterion 5 verify: `` → `python3 plugin/tests/run.py -p test_ideation.py -k Crossbreed`
- 2026-10-09T19:41:55Z focused
- 2026-10-09T19:43:40Z done
- 2026-10-09T19:43:41Z committed e3d6b64 (4 files)
- 2026-10-09T19:45:45Z committed b9fd48a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-intelligence-20261009: 768 ideas from 15 lenses over 4 rounds plus 3 deepened categories, in 106 capabilities; every idea under exactly one capabilit…
- T-0688 [FEATURE L, planned, 7 steps] Milestone: Intelligence — Judgment, taste and decisions
- T-0693 [FEATURE M, planned, 4 steps] Milestone: Intelligence — Reasoning and thought process
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- Brainstorm quality needs feedback the catalogue can carry: store it structurally (lens → ideas) so later choices can be joined back to it
## Files touched
- plugin/tests/test_ideation.py
- plugin/lib/fmideas.py
- plugin/lib/fmcli.py
- plugin/skills/intake/references/planning.md
- CHANGELOG.md
- MASTER.md
