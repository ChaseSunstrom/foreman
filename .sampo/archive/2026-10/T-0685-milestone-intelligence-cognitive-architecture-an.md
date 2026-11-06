---
id: T-0685
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:16Z
updated: 2026-10-09T19:50:26Z
batch: [T-0663, T-0664, T-0665]
base: b9fd48ab0576206ea0dbb59b99d6953b73c85e4c
base_tree: 5b0075278f6f28f235ea802cb14ebcdd0f97c075
verified: strong
---
# Milestone: Intelligence — Cognitive architecture and wild bets
## Raw request
> T-0663: FEATURE: Memory by activation and episode (I101, value 3/5, effort M, risk low)
>   first version: Add activation to recall: boost hits by recent touch of the same files and repeated failure signatures; keep schema distillation as a night job over lessons. Skip REM recombination and causal model.
>   what it is: Recalls by activation, segments episodes, distils schemas and finds analogues across projects.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0664: FEATURE: Cognitive evaluation (I105, value 3/5, effort M, risk low)
>   first version: Use fm evolve --drop to run lesion tests on each instruction file/skill (is it ever used, does bench drop without it) and report in fm usage; ties to fm usage's never-used list. Skip Common Model audit and K-lines.
>   what it is: Audits Foreman against cognitive models and tests faculties by lesion.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0665: FEATURE: Dream-time and sleep simulation (I106, value 3/5, effort M, risk med)
>   first version: Add a night job that replays the day's surprises/failed steps into a bench case or tripwire candidate (counterfactual: would the new rule have caught it). Skip sandboxed overnight plan dreaming.
>   what it is: Counterfactual simulation, night passes and sleeping on problems.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 2 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0663, T-0664, T-0665 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0685. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0663: Memory by activation and episode (I101, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_cognition.py -k Activation`
- [x] T-0664: Cognitive evaluation (I105, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_cognition.py -k Lesions`
- [x] T-0665: Dream-time and sleep simulation (I106, value 3/5, effort M, risk med) works — verify with `python3 plugin/tests/run.py -p test_cognition.py -k Dream`
## Non-goals
## Approach (options → choice → why)
T-0663 activation: recall's BM25 score is multiplied by an activation — a past brief whose files the active task touched recently (×1.5) or whose failure signatures recurred in the last 7 days (×1.5) — options: a separate memory store (duplicates recall), embeddings (model calls); chosen: two multipliers on data recall already reads. T-0664 lesions: fm usage --lesions joins the evolve ablations already logged (fm evolve --drop: bench held without the file = may not earn its tokens; dropped = earns it) with the never-used skills and playbooks, naming the next lesion to run; options: run the lesions now (bench spend), or only list never-used (exists); chosen: the report, since the runs need budget. T-0665 dream: fm dream (and a free night job) groups the day's failure signatures and guard refusals, and for each repeated one writes a tripwire candidate with its counterfactual (how many later occurrences a rule on it would have caught) into research/dream-DATE.md; options: replay the day in a sandbox with a model (later), or only list failures (exists in the friction digest); chosen: candidates with the counterfactual, model-free.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0663: Memory by activation and episode (I101, value 3/5, effort M, risk low)
2. [x] T-0664: Cognitive evaluation (I105, value 3/5, effort M, risk low)
3. [x] T-0665: Dream-time and sleep simulation (I106, value 3/5, effort M, risk med)
## Resume here
## Docs impact
CHANGELOG; MASTER.md (fmrecall)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_cognition.py` → ✗ exit 1 · Ran 3 tests in 0.5s (3 classes, 16 at a time; slowest: Activation 0s, Dream 0s, Lesions 0s) / FAILED (3 classes) [ran] [tree 37d274e8fb16] (2026-10-09T19:46:50Z)
- (step 1) `python3 plugin/tests/run.py -p test_cognition.py -k Activation` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Activation 0s) / OK [ran] [tree 031fafea07db] (2026-10-09T19:48:00Z)
- (step 2) `python3 plugin/tests/run.py -p test_cognition.py -k Lesions` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Lesions 0s) / OK [ran] [tree 031fafea07db] (2026-10-09T19:48:00Z)
- (step 3) `python3 plugin/tests/run.py -p test_cognition.py -k Dream` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Dream 0s) / OK [ran] [tree 031fafea07db] (2026-10-09T19:48:01Z)
- (ac 1) `python3 plugin/tests/run.py -p test_cognition.py -k Activation` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Activation 0s) / OK [ran] [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
- (ac 2) `python3 plugin/tests/run.py -p test_cognition.py -k Lesions` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Lesions 0s) / OK [ran] [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
- (ac 3) `python3 plugin/tests/run.py -p test_cognition.py -k Dream` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Dream 0s) / OK [ran] [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
- (audit intent) `self review of the three members; full suite (the night dry-run test updated: the free dream job always fits)` → each member's first version shipped as its note asked: activation boosts in recall, lesion reports from existing ablations, a night dream job turning repeated failures into tripwire candidates with their counterfactual [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
- (audit adversary) `self review of the three members; full suite (the night dry-run test updated: the free dream job always fits)` → nothing new leaves the machine; the dream file holds failure signatures already in the project's own folder and is redacted; recall only reorders what it already showed [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
- (audit edge) `self review of the three members; full suite (the night dry-run test updated: the free dream job always fits)` → no active task or no recent failures leaves recall unchanged; one-off failures and the hint records aren't candidates; a lesion that ties counts as held (the file may not earn its tokens), as fm evolve already treats it [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
- (audit operator) `self review of the three members; full suite (the night dry-run test updated: the free dream job always fits)` → fm dream on this project writes one file per day and costs nothing; recall's added work is one ledger and failures read per call, the same files it already reads [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
- (audit maintainer) `self review of the three members; full suite (the night dry-run test updated: the free dream job always fits)` → one multiplier function beside recall, one report beside fm usage's others, one command beside failure memory; the night job list gains a free entry first [tree 0aea665b9b44] (2026-10-09T19:50:26Z)
## Log
- 2026-10-09T15:40:16Z created
- 2026-10-09T19:46:36Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_cognition.py -k Activation`
- 2026-10-09T19:46:36Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_cognition.py -k Lesions`
- 2026-10-09T19:46:36Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_cognition.py -k Dream`
- 2026-10-09T19:46:37Z set approved=True
- 2026-10-09T19:46:37Z focused
- 2026-10-09T19:50:26Z done
- 2026-10-09T19:50:26Z committed 576d51c (8 files)
## Follow-ups captured
## Build vs reuse
Reuse: recall's scoring and _documents (files, id per brief), failures.jsonl signatures, the ledger's touched/evolve/guard_block events, fm usage's skill/playbook counts, fm night's job list. Build: two multipliers, one report flag, one command and one night job. Nothing new is stored except the dream file.
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-intelligence-20261009: 768 ideas from 15 lenses over 4 rounds plus 3 deepened categories, in 106 capabilities; every idea under exactly one capabilit…
- T-0689 [FEATURE M, planned, 7 steps] Milestone: Intelligence — Learning from outcomes
- T-0680 [FEATURE M, done, 4 steps] Milestone: Features — Self-improvement and learning — lesson: Measure what the harness itself injects: notes are tokens too, and a note…
- decision 2026-10-09: Self-approved T-0685 (L): three model-free first versions on existing data (recall multipliers, a lesion report, a dream file); the self-critique fo…
- the similar finished task took 4 steps
## Lessons
- Memory works better weighted by what's active now; a counterfactual line (how many later failures a rule would have caught) is what makes a tripwire candidate worth reading
## Files touched
- plugin/tests/test_cognition.py
- plugin/lib/fmrecall.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- plugin/lib/fmnight.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_night.py
