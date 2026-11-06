---
id: T-2488
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T17:10:19Z
updated: 2026-11-01T18:15:34Z
base: 71d9a8abc07ec6723bb6734c75597a9893f2bc32
base_tree: 00f843f1f4e21b5dd3b7a00469f7d509c39eef6b
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T18:01:35Z
plan0_scope: []
verified: strong
---
# The first uses in shadow mode: intake type and tier, fm find lead triage, embedding…
## Raw request
> FEATURE: the first uses in shadow mode: intake type and tier, fm find lead triage, embedding dedupe of captures, each logged beside the path it would replace
## Interpretation
Readings: (a) shadow mode means the path's own decision is recorded inline as a labelled row (cheap, no model), and a batch shadow pass replays those rows through decide() with local backends only on the night run, booking the model's answer beside the path's for the exam arms (T-2487) to compare; (b) call decide() inline on every capture and lead. (a): inline calls would slow fm capture and spend tokens per capture, and the user's rule keeps every use advisory until its exam wins, so nothing needs the model's answer at once.
## Assumptions (confidence)
## Acceptance criteria
- [x] capture, intake, find --rank and capture dedupe log the path's decision; the night tick's shadow pass books a local model's answer per row and spends nothing without a local backend — verify with `python3 plugin/tests/run.py test_models`
## Non-goals
## Approach (options → choice → why)
1) A shadow log (state/shadow.jsonl): fm capture and fm intake write {use: intake-type, input, path: the type chosen}; fm find --rank writes {use: lead-triage, input, path: kept or dropped}; capture_once's dedupe writes {use: dedupe, pair, path: same or different}; the night tick's shadow pass runs decide() on unscored rows with local backends only (a cap per night), booking each answer with its row id. Fails if: no local backend exists (the pass records 'no local backend' and spends nothing). 2) Inline decide() calls. Fails if: capture latency and token spend grow per call, before any exam says the use is worth it. 3) Use what exists: fmnight's tick, decide()'s booking, the prediction book, fmmodels.live() for the switch. Likely outcome: ~70 lines. 4) Do less: log the path rows only. Fails if: no model answer exists for the exam arms to compare. Choice 1 on 3 (80%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] the shadow log at each use and the night shadow pass
3. [x] docs
## Resume here
## Docs impact
MASTER (fmmodels entry), CHANGELOG Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k Shadow test_models test_cli` → ✗ exit 1 · Ran 3 tests in 0.9s (2 classes, 16 at a time; slowest: ShadowRows 0s, Shadow 0s) / FAILED (2 classes: test_models.Shadow, test_cli.ShadowRows) [ran] [tree 0ff1056ff957] (2026-11-01T18:02:36Z)
- `python3 plugin/tests/run.py -k Shadow test_models test_cli` → ✗ exit 1 · Ran 3 tests in 1.6s (2 classes, 16 at a time; slowest: ShadowRows 0s, Shadow 0s) / FAILED (2 classes: test_models.Shadow, test_cli.ShadowRows) (start tree + this task's tests) [ran] [tree 018cad281e46] (2026-11-01T18:03:32Z)
- `python3 plugin/tests/run.py -k Shadow test_models test_cli` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: ShadowRows 0s, Shadow 0s) / OK [ran] [tree 018cad281e46] (2026-11-01T18:03:32Z)
- (step 2) `python3 plugin/tests/run.py test_models test_cli test_find test_night test_recall test_backlog` → exit 0 · Ran 426 tests in 23.4s (101 classes, 16 at a time; slowest: TaskLifecycle 23s, Recall 17s, FindBlindSpots 13s) / OK [ran] [tree 018cad281e46] (2026-11-01T18:03:55Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.2s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 24e974782871] (2026-11-01T18:04:18Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 65 tests in 2.3s (11 classes, 16 at a time; slowest: Bench 2s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree 24e974782871] (2026-11-01T18:04:21Z)
- (ac 1) `python3 plugin/tests/run.py test_models` → exit 0 · Ran 65 tests in 2.2s (11 classes, 16 at a time; slowest: Bench 2s, RunRoute 1s, OpenAIShape 1s) / OK [ran] [tree 24e974782871] (2026-11-01T18:09:50Z)
- (audit intent) `main-thread lens pass over shadow/shadow_pass, the four hooks and the night tick call, with the three tests` → each first use (intake type and tier, dedupe, lead triage) records the rule's decision inline with no model call, and the night tick's shadow pass answers those rows with local backends only, booking each answer (or miss) by row id, so the exam can compare model and rule before any use goes live [tree 24e974782871] (2026-11-01T18:09:50Z)
- (audit adversary) `main-thread lens pass over shadow/shadow_pass, the four hooks and the night tick call, with the three tests` → shadow inputs are plain'd and redacted before they're stored; the pass never reaches a cloud backend, so a sensitive repo's text stays local; shadow() swallows its own errors, so logging can't break a capture or scan [tree 24e974782871] (2026-11-01T18:09:50Z)
- (audit edge) `main-thread lens pass over shadow/shadow_pass, the four hooks and the night tick call, with the three tests` → no local backend means nothing runs and nothing is spent; a row answered once (or missed) is never asked again; find logs only its top 20 leads a scan [tree 24e974782871] (2026-11-01T18:09:50Z)
- (audit operator) `main-thread lens pass over shadow/shadow_pass, the four hooks and the night tick call, with the three tests` → the tick's notes name a shadow-pass failure; MASTER lists every hook [tree 24e974782871] (2026-11-01T18:09:50Z)
- (audit maintainer) `main-thread lens pass over shadow/shadow_pass, the four hooks and the night tick call, with the three tests` → one shadow() helper and one pass in fmmodels; hooks are one line at each decision point [tree 24e974782871] (2026-11-01T18:09:50Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 24e974782871] (2026-11-01T18:10:57Z)
## Log
- 2026-11-01T17:10:19Z created
- 2026-11-01T17:36:36Z planned: it has criteria and steps
- 2026-11-01T17:36:41Z set approved=True
- 2026-11-01T18:01:34Z focused
- 2026-11-01T18:01:35Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T18:04:18Z scope: plugin/lib/fmmodels.py (shadow, shadow_pass, decide ref), fmcli.py (capture, intake, _near hooks), fmfind.py (rank hook), fmnight.py (tick), tests test_models and test_cli, MASTER.md, CHANGELOG.md
- 2026-11-01T18:10:28Z done
- 2026-11-01T18:10:30Z committed 4ffc19f1 (8 files)
- 2026-11-01T18:10:57Z guard authorization added: publish
- 2026-11-01T18:15:34Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2437 [FEATURE L, done, 5 steps] Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A… — lesson: A user's next-generation request has to reach the n…
- T-2485 [FEATURE M, done, 2 steps] decide() on fmmodels: a kind and an input return choice, score and probability from a… — lesson: A model call returns data, not decisio…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
## Lessons
- Shadow mode is cheapest as a log plus a batch pass: inline model calls tax every capture before any exam says they're worth it
## Plan gaps
- failed first: step 1 red tests
## Files touched
- plugin/tests/test_models.py
- plugin/tests/test_cli.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcli.py
- plugin/lib/fmfind.py
- plugin/lib/fmnight.py
- CHANGELOG.md
- MASTER.md
