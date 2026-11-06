---
id: T-2269
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T04:48:28Z
updated: 2026-10-31T05:40:26Z
base: 5148948fa6c36dc8f96ce0b3142ad9c0ffd4456c
base_tree: 3764f6f58280f043133c0cc3f6e9a7f09c1c3528
plan0_at: 2026-10-31T04:49:02Z
plan0_scope: []
verified: strong
---
# Plan gate checks content by tier (Mission 5, #2): M/L Approach names 3+ options and a choice; L adds 2+ readings and risks; a low-confidence assumption needs a research note or spike first
## Raw request
> Plan gate checks content by tier (Mission 5, #2): M/L Approach names 3+ options and a choice; L adds 2+ readings and risks; a low-confidence assumption needs a research note or spike first
## Interpretation
Gap map #2: the plan gate (fmcore.plan_gaps) checks only that Interpretation and Approach are non-empty, so a one-line approach starts an M task, and the rules' '3+ approaches; choose' is prose only. Readings (one request read two ways) and failure modes are never asked of an L plan, and a low-confidence assumption goes straight to code instead of research.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm focus refuses an M brief whose Approach names fewer than 3 options or no choice, an L brief also without 2+ readings in Interpretation or an empty Risks section, and any brief with a (low) assumption until a research note or spike is linked; existing open tasks keep working (a task already started isn't re-gated) — verify with `python3 plugin/tests/run.py test_core test_cli`
## Non-goals
## Approach (options → choice → why)
1) content checks inside plan_gaps: options counted as numbered '1)'/'2.'/bullets or 'Option' lines in the Approach section, a choice as 'Choice'/'chose'/'→ choice'; L: Interpretation with 2+ readings (numbered or 'Reading'), 'Risks and rollback' non-empty; a line in Assumptions marked '(low)' needs a linked research note (fm research id in the brief) or a spike task id. Each gap names its fix. Gate applies at fm focus and lane brief (both already call plan_gaps); a task already active or done isn't re-gated. 2) a model judging plan quality — rejected: tokens per focus and a judge that can be argued with; counting is deterministic. 3) a warning only — rejected: the rule already exists as prose and is skipped. Choice 1.
## Risks and rollback
Open M/L tasks written before the rule may be refused at focus: the gap names the fix (add options), a minute's work; rollback is reverting plan_gaps' new lines.
## Execution prompt
## Steps
1. [x] red tests: each gap refused with its fix named; a full brief starts; an active task isn't re-gated
2. [x] plan_gaps content checks (options, choice, readings, risks, low assumptions) with the fix in each gap's text
3. [x] docs: MASTER plan gate line, CHANGELOG, intake skill's planning reference names the rule
## Resume here
<!-- auto -->
- 2026-10-31T05:26:33Z step 1/3: red tests: each gap refused with its fix named; a full brief starts; an active task isn't re-gated
- git: worktree-agent-a2f6f547b49b194e2; 2 uncommitted: plugin/tests/test_cli.py, plugin/tests/test_core.py
- touched since last checkpoint: plugin/lib/fmcore.py, plugin/skills/intake/references/planning.md, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/b1.json, plugin/tests/test_builder.py, plugin/tests/test_clean_helpers.py, plugin/tests/test_conflict_history.py, plugin/tests/test_defect_classes.py, plugin/tests/test_evidence_quality.py, plugin/tests/test_lane_stall.py, plugin/tests/test_lanes.py, plugin/tests/test_metacog.py, plugin/tests/test_pass4.py, plugin/tests/test_reasoning.py
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/planning.md
## Verification evidence
- `python3 plugin/tests/run.py test_core test_cli` → ✗ exit 1 · Ran 236 tests in 21.6s (64 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 9s, CaptureAndIntake 9s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 48f7ebb63acb] (2026-10-31T05:37:36Z)
- `python3 plugin/tests/run.py test_core test_cli` → exit 0 · Ran 236 tests in 20.2s (64 classes, 16 at a time; slowest: TaskLifecycle 20s, StateViews 8s, CaptureAndIntake 8s) / OK [ran] [tree 48f7ebb63acb] (2026-10-31T05:37:36Z)
- (step 1) `python3 plugin/tests/run.py test_core test_cli test_lanes` → exit 0 · Ran 280 tests in 19.7s (69 classes, 16 at a time; slowest: TaskLifecycle 19s, Lanes 15s, StateViews 8s) / OK [ran] [tree 48f7ebb63acb] (2026-10-31T05:37:56Z)
- (step 2) `python3 plugin/tests/run.py test_core test_cli test_lanes` → exit 0 · Ran 280 tests in 19.7s (69 classes, 16 at a time; slowest: TaskLifecycle 19s, Lanes 15s, StateViews 8s) / OK [ran] [tree 48f7ebb63acb] (2026-10-31T05:38:15Z)
- (step 3) `grep -c T-2269 MASTER.md CHANGELOG.md plugin/skills/intake/references/planning.md` → exit 0 · CHANGELOG.md:1 / plugin/skills/intake/references/planning.md:1 [ran] [tree 48f7ebb63acb] (2026-10-31T05:38:16Z)
- (ac 1) `python3 plugin/tests/run.py test_core test_cli` → exit 0 · Ran 236 tests in 19.5s (64 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 48f7ebb63acb] (2026-10-31T05:38:47Z)
- (audit intent) `self + one fm-reviewer pass (2 high, 2 medium, 3 low; all but the shared-fixture refactor fixed with tests); full suite green in the lane (4678 tests); the real queue checked after merge: started L tasks T-2077 and T-2185 aren't re-gated` → the rules' '3+ approaches; choose' and an L plan's readings and risks are now checked at focus and lane brief, and a (low) assumption waits for research or a spike (test_core red-to-green) [tree 48f7ebb63acb] (2026-10-31T05:38:47Z)
- (audit adversary) `self + one fm-reviewer pass (2 high, 2 medium, 3 low; all but the shared-fixture refactor fixed with tests); full suite green in the lane (4678 tests); the real queue checked after merge: started L tasks T-2077 and T-2185 aren't re-gated` → the gate counts, it doesn't judge: hollow markers and the pasted hint text don't pass; a (low) line passes by naming research/NAME or a spike id [tree 48f7ebb63acb] (2026-10-31T05:38:47Z)
- (audit edge) `self + one fm-reviewer pass (2 high, 2 medium, 3 low; all but the shared-fixture refactor fixed with tests); full suite green in the lane (4678 tests); the real queue checked after merge: started L tasks T-2077 and T-2185 aren't re-gated` → a task ever started (plan0_at, base, evidence, a done step) is never re-gated even when paused; (1)/(A)/Option A:/bold/heading option forms count; T-2077's and T-2185's real Approach texts count 3 [tree 48f7ebb63acb] (2026-10-31T05:38:47Z)
- (audit maintainer) `self + one fm-reviewer pass (2 high, 2 medium, 3 low; all but the shared-fixture refactor fixed with tests); full suite green in the lane (4678 tests); the real queue checked after merge: started L tasks T-2077 and T-2185 aren't re-gated` → fm code's planner writes 3 options; its L plans still lack readings and risks (T-2274) [tree 48f7ebb63acb] (2026-10-31T05:38:47Z)
## Log
- 2026-10-31T04:48:28Z created
- 2026-10-31T04:48:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2269.builder.md
- 2026-10-31T04:49:01Z focused
- 2026-10-31T05:36:41Z merged worktree-agent-a2f6f547b49b194e2 (30 file(s))
- 2026-10-31T05:36:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2f6f547b49b194e2
- 2026-10-31T05:36:41Z focused
- 2026-10-31T05:38:27Z scope: plugin/lib/fmcore.py (_content_gaps, _count_options, _started), plugin/lib/fmcode.py (_make_task approach), ~25 test files' fixtures to full briefs, plugin/tests/test_core.py, test_cli.py, MASTER.md, CHANGELOG.md, plugin/skills/intake/references/planning.md
- 2026-10-31T05:40:26Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2077 [RESEARCH L, planned, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- research mission-20261029-104513: Request: keep super ultimate recursive brainstorming, and implementing all ideas, super ultimate improve foreman in all ways [stale: de…
- T-1664 [FEATURE M, done, 4 steps] Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner — lesson: a flag a sub-action doesn't r…
- decision 2026-10-31: [revisited: Standing rule from gen 2 on: one Mission per generation is a moonshot] [cites: the user's steer 2026-10-30 (fifth): moonshot Mission fro…
- the similar finished task took 4 steps
## Lessons
- A new gate must exempt by history (was it ever started?), not by status: a pause rewrites status and would re-gate work in flight
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
- plugin/skills/intake/references/planning.md
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_builder.py
- plugin/tests/test_clean_helpers.py
- plugin/tests/test_conflict_history.py
- plugin/tests/test_defect_classes.py
- plugin/tests/test_evidence_quality.py
- plugin/tests/test_lane_stall.py
- plugin/tests/test_lanes.py
- plugin/tests/test_metacog.py
- plugin/tests/test_pass4.py
- plugin/tests/test_reasoning.py
- plugin/tests/test_replan.py
- plugin/tests/test_round_i.py
- plugin/tests/test_runtime.py
- plugin/tests/test_second.py
- plugin/tests/test_splits.py
- plugin/tests/test_backlog.py
- plugin/tests/test_batch.py
- plugin/tests/test_cli.py
- plugin/tests/test_deliberation.py
- plugin/tests/test_diagnosis.py
- plugin/tests/test_edit_cards.py
- plugin/tests/test_hooks.py
- plugin/tests/test_recall.py
- plugin/tests/test_trust.py
- plugin/lib/fmcode.py
