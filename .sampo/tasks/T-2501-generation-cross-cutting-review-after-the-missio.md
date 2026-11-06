---
id: T-2501
type: FEATURE
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-11-01T19:16:31Z
updated: 2026-11-01T19:49:58Z
rival_at: 2026-11-01T19:20:53Z
rival_split: true
base: 8df00388e8e7236e07a2c2780b7c1260b680771a
base_tree: e731dbac6bc8ac3da45fd6acc1366648861a3e67
plan0_at: 2026-11-01T19:21:41Z
plan0_scope: []
verified: strong
---
# Generation cross-cutting review: after the Mission critiques, one cold reviewer on a…
## Raw request
> FEATURE!: generation cross-cutting review: after the Mission critiques, one cold reviewer on a stronger model than the Missions use, blind to the Missions and critiques, reads only the generation's repo diff, exam lines, fm outcomes and fm friction and answers what got worse, what grew without earning it, what is measured wrong, what is presented ahead of its proof and what a demanding user would complain about first; each finding is grounded in a file or a number and becomes a fix task or a top gap in the next Seed, a dismissal needs a recorded reason; fm genesis sweep goes red without the review file or with an unhandled finding
> DONE-WHEN: gen-N/review.md exists from a stronger-model cold read with grounded findings, each linked to a task, a seed gap or a recorded dismissal; the sweep row checks it
## Interpretation
Readings: (a) likeliest: a new genesis stage between the critiques and the sweep: fm genesis review N builds the inputs (the generation's git diff from its lean start commit: stat, log and a capped patch; its exam lines; fm outcomes' track and survival lines plus the judgment summary; fm friction's digest), sends them to one cold child on a model ranked above the Missions' (Fable over this session's Opus), keeps only findings grounded in a path or number the inputs hold, writes gen-N/review.md, files a task per finding unless the file marks it a seed gap or dismissed with a reason; the seed lists review gaps first; the sweep goes red without the file, with a weaker model, or with an unhandled finding. (b) The review runs inside the sweep itself: rejected, the sweep must stay zero-token and repeatable; the review is one model call per generation, cached by its inputs' hash. Fails if: the stronger model isn't reachable (then the review is unread and the sweep says so, never a silent pass).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis review N writes gen-N/review.md from a child on a model ranked above the Missions', keeps only findings grounded in the inputs, files a task per unhandled finding; the sweep row is red without the file, with a weaker model or an unhandled finding, green when each finding has a task, a seed gap or a dismissal with a reason — verify with `python3 plugin/tests/run.py test_genesis.GenerationReview`
## Non-goals
## Approach (options → choice → why)
1) fmgenesis.review(p, n, model) on fmideas.run_child (no tools, budget-capped): REVIEW_CHILD asks the five questions as 'FINDING: key | ground | claim' lines; a finding counts only when its ground (a path or number) occurs in the inputs; gen-N/review.md holds the model, the inputs' sha256 and each finding with a Handled column; a FIX is filed per unhandled finding (source genesis-review); step() runs review after critiques, drift and selection; the sweep row checks it. Fails if: findings come back vague (the filter drops them and the file counts the drops). 2) Spawn a reviewer subagent from the session. Fails if: the session's context leaks in (it saw the Missions), breaking the blind rule. 3) use what exists: fm audit prep's reviewer brief over the generation's range. Fails if: it reviews a task diff with no exam, outcomes or friction, so three of the five questions have no input. 4) do less: no model at all, a mechanical report (diff stat against exam deltas and friction counts). Fails if: 'what would a demanding user complain about first' needs judgment a count can't give. Reused in 1: run_child, _exam_tail, fmoutcomes track/survival lines, fmfriction digest/render, _lean_at_seed for the start commit, _sweep_fixes' filing shape. Choice 1 (85%): blind by construction (a fresh child sees only the four inputs), grounded by a mechanical filter, and every finding lands where the sweep can count it.
## Risks and rollback
Cost: one large-context call per generation on the top model, inputs capped (patch cut at 60k chars, largest files' hunks first). A model reply is untrusted: only FINDING lines whose ground occurs in the inputs enter review.md, plain'd and fit. The child gets no tools. Rollback: revert; review.md files stay as tower data and the sweep row goes away with the code.
## Execution prompt
## Steps
1. [x] red tests: GenerationReview (inputs, grounding filter, review.md, filed tasks, sweep row, step order)
2. [x] fmgenesis.review + REVIEW_CHILD + the sweep row + the step stage + the seed's review gaps
3. [x] docs: genesis skill, MASTER, README, CHANGELOG
4. [x] spike: claude -p --model fable runs (claude-fable-5-1; a one-word reply cost $0.29 with a 0.5 cap, failed under a 0.05 cap): the review must fit the per-run cap
## Resume here
## Docs impact
plugin/skills/genesis/SKILL.md (the review stage and --handle), README.md (the Genesis bullet), MASTER.md (fmgenesis entry), CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenerationReview` → exit 0 · Ran 5 tests in 12.0s (1 classes, 16 at a time; slowest: GenerationReview 12s) / OK [ran] [tree 7b0d625f8219] (2026-11-01T19:33:47Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_docs test_skills` → exit 0 · Ran 294 tests in 14.7s (44 classes, 16 at a time; slowest: GenerationReview 13s, GenesisRead 12s, GenesisCheck 9s) / OK [ran] [tree 44e93240554d] (2026-11-01T19:35:17Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_docs test_skills` → exit 0 · Ran 294 tests in 14.9s (44 classes, 16 at a time; slowest: GenerationReview 14s, GenesisRead 12s, GenesisCheck 9s) / OK [ran] [tree 44e93240554d] (2026-11-01T19:35:33Z)
- (step 4) `python3 plugin/tests/run.py test_genesis test_docs test_skills` → exit 0 · Ran 294 tests in 14.9s (44 classes, 16 at a time; slowest: GenerationReview 14s, GenesisRead 12s, GenesisCheck 9s) / OK [ran] [tree 44e93240554d] (2026-11-01T19:35:48Z)
- `python3 plugin/tests/run.py test_genesis.GenerationReview` → ✗ exit 1 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: GenerationReview 0s) / FAILED (1 classes: test_genesis.GenerationReview) (start tree + this task's tests) [ran] [tree 44e93240554d] (2026-11-01T19:36:03Z)
- `python3 plugin/tests/run.py test_genesis.GenerationReview` → exit 0 · Ran 5 tests in 12.1s (1 classes, 16 at a time; slowest: GenerationReview 12s) / OK [ran] [tree 44e93240554d] (2026-11-01T19:36:03Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenerationReview` → exit 0 · Ran 5 tests in 8.9s (1 classes, 16 at a time; slowest: GenerationReview 9s) / OK [ran] [tree 44e93240554d] (2026-11-01T19:41:57Z)
- (audit intent) `main-thread five-lens review of the diff (subagents paused: usage ahead of pace); one finding captured as T-2506` → the user's part 1 holds end to end: after critiques/drift/select and before the sweep, a cold child on the family above the Missions' (task_done models) sees only the diff, exam, outcomes and friction; findings become tasks, gap rows or dismissals with reasons; the sweep row and the step stage enforce it; gaps lead the next seed [tree 44e93240554d] (2026-11-01T19:41:57Z)
- (audit adversary) `main-thread five-lens review of the diff (subagents paused: usage ahead of pace); one finding captured as T-2506` → the reply is untrusted: only FINDING lines with a listed key and a ground that occurs in the inputs enter review.md, plain'd, pipe-escaped and cut; the child runs tool-less under the per-run budget cap; review.md is OWNED (put refuses it), so a hand-written row can't pass the stage [tree 44e93240554d] (2026-11-01T19:41:57Z)
- (audit edge) `main-thread five-lens review of the diff (subagents paused: usage ahead of pace); one finding captured as T-2506` → no start commit falls back to the last 50 commits; an unavailable input says so instead of losing the review; a rerun on an existing file makes no model call; --handle refuses a dismissal without a reason; a weak 2-character numeric ground still passes (T-2506 captured) [tree 44e93240554d] (2026-11-01T19:41:57Z)
- (audit operator) `main-thread five-lens review of the diff (subagents paused: usage ahead of pace); one finding captured as T-2506` → one top-model call per generation (a one-word fable call cost $0.29; the inputs are capped at a 60k-char patch); a failed call leaves no file, so step stays on review and the CLI says why [tree 44e93240554d] (2026-11-01T19:41:57Z)
- (audit maintainer) `main-thread five-lens review of the diff (subagents paused: usage ahead of pace); one finding captured as T-2506` → the review lives in fmgenesis beside the sweep it feeds, reuses run_child, _exam_tail, fmoutcomes, fmfriction and capture_once; the selected() test helper now also writes a clean review so fixtures past selection stay valid [tree 44e93240554d] (2026-11-01T19:41:57Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 44e93240554d] (2026-11-01T19:44:10Z)
## Log
- 2026-11-01T19:16:31Z created
- 2026-11-01T19:20:12Z planned: it has criteria and steps
- 2026-11-01T19:20:30Z set approved=True
- 2026-11-01T19:21:40Z focused
- 2026-11-01T19:36:03Z scope: fmgenesis review stage (review, _review_inputs, _review_row, review_fixes, review_handle, _review_gaps, step, seed, CLI), fmcli genesis --handle, test_genesis GenerationReview + reviewed() helper, genesis SKILL.md, README, MASTER, CHANGELOG
- 2026-11-01T19:43:40Z done
- 2026-11-01T19:43:43Z committed fbd3e499 (7 files)
- 2026-11-01T19:44:10Z guard authorization added: publish
- 2026-11-01T19:49:58Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuse: fmideas.run_child (child runner), fmgenesis._exam_tail, fmoutcomes, fmfriction, _sweep_fixes' shape, _file/_doc for tower files. Build: the REVIEW_CHILD prompt, the grounding filter, review.md's format, one sweep row, one step stage. No dependency.
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: a new pipeline stage in the genesis loop.** After Mission critiques, `fm genesis` spawns one reviewer agent on a stronger model, giving it only four inputs (git diff of the generation, exam lines, fm outcomes, fm friction). The reviewer writes `gen-N/review.md` with five fixed sections…
- **Narrower: only the sweep gate.** Add the review-file and finding-handled checks to the sweep and leave review production manual or agent-driven by convention. This fits the DONE-WHEN "the sweep row checks it", but the "one cold reviewer on a stronger model" wording says the spawning belongs in sc…
- **Broader: a generic cross-cutting review primitive.** A reusable "cold reviewer" mechanism (blind input bundle, model override, findings schema) that genesis is the first consumer of. It would be reused for other reviews later, and the request names only genesis.
- **Alternate: the reviewer's output is the Seed.** Findings feed straight into the next Seed's gap list automatically instead of being linked by hand. This is a stretch, since the request says "becomes a fix task or a top gap" and also allows dismissals, which implies a human or agent decision step.
Approaches:
- **Extend the existing genesis code.** Add a `review` step in `plugin/lib/fmcli.py` (or the genesis module it dispatches to) that builds a blind input bundle in a temp dir, runs a new `plugin/agents/` reviewer definition pinned to a stronger model, and writes `gen-N/review.md`. Add a sweep row besid…
- **Findings as structured front matter or a table.** Each finding gets an id, section, evidence ref and a `handled:` field (`task:<id>`, `seed-gap:<id>`, or `dismissed: <reason>`). The sweep parses that, which is more reliable than prose heuristics. The cost is that the reviewer must be prompted int…
- **Bundle builder as a pure function, tested alone.** A function takes a generation id and returns exactly the four inputs (diff, exam lines, outcomes, friction). Blindness is then enforced by construction, because the Mission and critique files are never read. A test in `plugin/tests/` asserts the …
- **Two-phase: review, then triage.** The reviewer produces ungrounded-checked findings. A separate triage step creates the tasks or Seed gaps or records dismissals, and writes the links back into `review.md`. The sweep checks the links. This separates judgement from bookkeeping, at the price of one …
Failure modes:
- **Blindness leaks.** The repo diff for a generation can include Mission files, critique files or `gen-N` artifacts, so the "blind" reviewer sees what it shouldn't. The bundle builder needs a path exclusion, and a test has to prove it on a real generation diff.
- **"Stronger model" isn't enforced.** If the model is resolved from config or a default and the Missions' model is also configurable, the reviewer can silently end up the same or weaker. The sweep or the review header should record both model ids and fail when the reviewer is not strictly stronger.
- **Grounding is checked loosely.** A sweep that only greps for a path-like or numeric token accepts findings citing files that don't exist in the diff or numbers that aren't in the exam lines. Validate that each cited file is in the diff and each cited number appears in the provided inputs.
- **The gate breaks existing generations.** Adding a red sweep row makes every past `gen-N` without a `review.md` fail `fm genesis sweep`, and the `fm doctor` and `fm replay` gates may exercise it. It needs a cutoff generation or a legacy exemption, and the fixtures in `plugin/tests/` that run sweeps…
## Dissent
- [x] rival reading: **Narrower: only the sweep gate.** Add the review-file and finding-handled checks to the sweep and leave review production manual or agent-driven by convention. This fits the DONE-WHEN "the sweep row checks it", but the "one cold reviewer on a stronger model" wording says the spawning belongs in sc… — answered: rejected: the user asked for the review itself every generation; a gate over a manual file would let it be skipped
- [x] rival reading: **Broader: a generic cross-cutting review primitive.** A reusable "cold reviewer" mechanism (blind input bundle, model override, findings schema) that genesis is the first consumer of. It would be reused for other reviews later, and the request names only genesis. — answered: rejected: one consumer today; review() takes its inputs as text so a later caller can reuse it without a framework now
- [x] rival reading: **Alternate: the reviewer's output is the Seed.** Findings feed straight into the next Seed's gap list automatically instead of being linked by hand. This is a stretch, since the request says "becomes a fix task or a top gap" and also allows dismissals, which implies a human or agent decision step. — answered: rejected: the user allows dismissals with a reason; findings become tasks by default and only a marked 'gap' row goes to the seed's top gaps
- [x] rival approach: **Extend the existing genesis code.** Add a `review` step in `plugin/lib/fmcli.py` (or the genesis module it dispatches to) that builds a blind input bundle in a temp dir, runs a new `plugin/agents/` reviewer definition pinned to a stronger model, and writes `gen-N/review.md`. Add a sweep row besid… — answered: adopted: it lives in fmgenesis as fm genesis review N, dispatched like the other genesis subcommands; no agent definition, the child runner keeps it tool-less
- [x] rival approach: **Findings as structured front matter or a table.** Each finding gets an id, section, evidence ref and a `handled:` field (`task:<id>`, `seed-gap:<id>`, or `dismissed: <reason>`). The sweep parses that, which is more reliable than prose heuristics. The cost is that the reviewer must be prompted int… — answered: adopted: review.md is a table with an id, the question key, the ground, the claim and a Handled column (T-NNNN, gap, or dismissed: reason) that the sweep parses
- [x] rival approach: **Bundle builder as a pure function, tested alone.** A function takes a generation id and returns exactly the four inputs (diff, exam lines, outcomes, friction). Blindness is then enforced by construction, because the Mission and critique files are never read. A test in `plugin/tests/` asserts the … — answered: adopted: _review_inputs(p, n) returns the four inputs as text and reads no tower file, tested alone for blindness
- [x] rival approach: **Two-phase: review, then triage.** The reviewer produces ungrounded-checked findings. A separate triage step creates the tasks or Seed gaps or records dismissals, and writes the links back into `review.md`. The sweep checks the links. This separates judgement from bookkeeping, at the price of one … — answered: adopted in part: the review call writes findings; filing tasks for unhandled rows is a separate pass the sweep and step run, so a re-run never refiles
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
## Lessons
- a new genesis stage needs the shared test fixtures (selected()) to cover it, or every older step test starts failing at the new stage
## Plan gaps
- added late: spike: claude -p --model fable runs (claude-fable-5-1; a one-word reply cost $0.29 with a 0.5 cap, failed under a 0.05 …
## Files touched
- plugin/lib/fmgenesis.py
- plugin/lib/fmcli.py
- plugin/tests/test_genesis.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/skills/genesis/SKILL.md
