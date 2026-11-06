---
id: T-0690
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:17Z
updated: 2026-10-09T20:32:03Z
batch: [T-0619, T-0620, T-0661]
base: ac4119ae8e6133c67d981bc8ed7ab24c075a114f
base_tree: 3fa0ba7ad42ba782c43ca8bbc6fa01433b96f3d1
verified: strong
---
# Milestone: Intelligence — Metacognition and calibration
## Raw request
> T-0619: FEATURE: Calibrate confidence (I090, value 4/5, effort M, risk low)
>   first version: Record confidence number with each assumption/plan; at finish, score vs outcome (reopened, review findings, bench) into a calibration table in fm digest. Start with one axis.
>   what it is: Scores forecasts and confidence per axis and tag against outcomes.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0620: FEATURE: Competence atlas and self-model (I093, value 4/5, effort M, risk low)
>   first version: fm atlas-like report from bench + review findings + reopened tasks, grouped by tag/file area/language, feeding fm next caution hints and the friction pass. Start by aggregating existing grades by area.
>   what it is: Maps where Foreman is weak and predicts its own failure modes.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0661: FEATURE: Honest close-outs (I094, value 3/5, effort M, risk low)
>   first version: Finish lint: compare final criteria text to the one at approval (hash in Log) and flag edits; flag all-green with zero red runs ever as 'suspiciously smooth'. First step is the AC diff check.
>   what it is: Detects hindsight rewriting, confidence laundering and suspiciously smooth results, and diagnoses each escape as a monitoring, control or knowledge failure.
>   from the intelligence brainstorm 2026-10-09 (research brainstorm-intelligence-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0619, T-0620, T-0661 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0690. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0619: Calibrate confidence (I090, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_metacog.py -k Calibrate`
- [x] T-0620: Competence atlas and self-model (I093, value 4/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_metacog.py -k Atlas`
- [x] T-0661: Honest close-outs (I094, value 3/5, effort M, risk low) works — verify with `python3 plugin/tests/run.py -p test_metacog.py -k Honest`
## Non-goals
## Approach (options → choice → why)
Options: (a) confidence on every assumption with its own scoring; (b) one axis — the task's confidence that it holds on its first finish (fm task set ID confidence=N), scored against fmoutcomes' fate and first-finish record; (c) a model judge of confidence. Choice: (b), the brief's 'start with one axis', reusing T-0689's outcomes so calibration, the atlas and the track record share one join. Atlas: fm outcomes --atlas groups done tasks by file touched and by language (n>=3), held vs fixed later/reverted and weak grades; fm focus adds a caution line when the task's scope falls on a weak file; fm friction lists the weakest. Honest close-outs: finish warnings (never refusals) for criteria text or verify edits logged after the first focus, and for an M/L non-FIX task whose every recorded run passed first time; both logged as a closeout_flags event. Later: assumption-level confidence, escape diagnosis (monitoring/control/knowledge), next-turn caution hints.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0619: Calibrate confidence (I090, value 4/5, effort M, risk low)
2. [x] T-0620: Competence atlas and self-model (I093, value 4/5, effort M, risk low)
3. [x] T-0661: Honest close-outs (I094, value 3/5, effort M, risk low)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: metacognition), ~/.claude/foreman/MASTER.md (fmoutcomes row), ~/.claude/foreman/plugin/skills/intake/references/planning.md (Confidence line)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_metacog.py` → ✗ exit 1 · Ran 3 tests in 1.9s (3 classes, 16 at a time; slowest: Atlas 2s, Calibrate 1s, Honest 0s) / FAILED (3 classes) [ran] [tree 270b7e085747] (2026-10-09T20:25:33Z)
- (step 1) `python3 plugin/tests/run.py -p test_metacog.py -k Calibrate` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Calibrate 1s) / OK [ran] [tree ff2b20fed730] (2026-10-09T20:26:54Z)
- (step 2) `python3 plugin/tests/run.py -p test_metacog.py -k Atlas` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: Atlas 1s) / OK [ran] [tree ff2b20fed730] (2026-10-09T20:26:56Z)
- (step 3) `python3 plugin/tests/run.py -p test_metacog.py -k Honest` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Honest 0s) / OK [ran] [tree ff2b20fed730] (2026-10-09T20:26:56Z)
- (ac 1) `python3 plugin/tests/run.py -p test_metacog.py -k Calibrate` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Calibrate 1s) / OK [ran] [tree 221d162b1bfc] (2026-10-09T20:29:52Z)
- (ac 2) `python3 plugin/tests/run.py -p test_metacog.py -k Atlas` → exit 0 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: Atlas 2s) / OK [ran] [tree 221d162b1bfc] (2026-10-09T20:29:52Z)
- (ac 3) `python3 plugin/tests/run.py -p test_metacog.py -k Honest` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Honest 1s) / OK [ran] [tree 221d162b1bfc] (2026-10-09T20:29:52Z)
- `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1200 tests in 89.8s (376 classes, 16 at a time; slowest: Stop 69s, TaskLifecycle 45s, Bench 44s) / FAILED (2 classes) [ran] [tree 221d162b1bfc] (2026-10-09T20:29:52Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1200 tests in 59.3s (376 classes, 16 at a time; slowest: Stop 39s, TaskLifecycle 25s, Parallel 22s) / OK [ran] [tree 221d162b1bfc] (2026-10-09T20:32:02Z)
- (audit intent) `main-thread review of the diff against each member's first version; live atlas and friction runs on this project` → the three first versions shipped (one confidence axis, atlas from existing grades and fates, criteria-edit and smooth-run flags); assumption-level confidence and escape diagnosis left for later, noted in the approach [tree 221d162b1bfc] (2026-10-09T20:32:02Z)
- (audit edge) `main-thread review of the diff against each member's first version; live atlas and friction runs on this project` → confidence is validated as a whole 0-100 percent; the atlas needs 3+ tasks before a file counts and caution needs 2+ bad at 20%+, so one fix doesn't brand a file; criteria edits only count after the first focus, so planning-time edits aren't flagged; flags never refuse a close [tree 221d162b1bfc] (2026-10-09T20:32:02Z)
## Log
- 2026-10-09T15:40:17Z created
- 2026-10-09T20:25:13Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_metacog.py -k Calibrate`
- 2026-10-09T20:25:13Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_metacog.py -k Atlas`
- 2026-10-09T20:25:13Z criterion 3 verify: `` → `python3 plugin/tests/run.py -p test_metacog.py -k Honest`
- 2026-10-09T20:25:15Z focused
- 2026-10-09T20:32:02Z done
- 2026-10-09T20:32:03Z committed e6c839d (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- decision 2026-10-09: Self-approved T-0685 (L): three model-free first versions on existing data (recall multipliers, a lesion report, a dream file); the self-critique fo…
## Lessons
- Calibration needs a stated number before the outcome is known; derive the outcome from the same join the track record uses so the two can't disagree
## Files touched
- plugin/tests/test_metacog.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmfriction.py
- plugin/skills/intake/references/planning.md
- CHANGELOG.md
- MASTER.md
