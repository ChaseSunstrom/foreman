---
id: T-2291
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T07:15:16Z
updated: 2026-10-31T07:37:49Z
base: 62d86c2edbd3189591e4ad6807627b2ffd7486f6
base_tree: 085f66905b7c4557813c25ad0290aacd66bb6e7a
plan0_at: 2026-10-31T07:15:37Z
plan0_scope: []
verified: strong
---
# History-based model router (Mission 8, #9): fm lane brief picks the builder model from how past lanes' tasks held up per tier and model (re-fixed, reverted, red after merge), escalating where the cheaper model's lanes keep needing rework
## Raw request
> History-based model router (Mission 8, #9): fm lane brief picks the builder model from how past lanes' tasks held up per tier and model (re-fixed, reverted, red after merge), escalating where the cheaper model's lanes keep needing rework
## Interpretation
Gap map #9: 'history-based model router with escalation'. fm lane brief hardcodes model sonnet (fmlanes.py:730) for every builder; nothing learns whether sonnet's lanes in some tier keep needing rework that a stronger model would avoid, or whether a cheaper one would do.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief records the model it names on the brief; its suggestion is sonnet unless, over the last 20 lane-built closed tasks of that tier, sonnet's rework rate (a later FIX naming the task, a baseline red after its merge, or a lost outcome) is 0.3+ above opus's with 5+ samples each, then opus with the numbers; fm lane brief --model overrides; with too little history it says so — verify with `python3 plugin/tests/run.py test_lanes test_outcomes`
## Non-goals
## Approach (options → choice → why)
1) record the named model on the brief at lane brief (meta builder_model), and compute per tier and model a rework rate over lane-built closed tasks: a later FIX that names the task, a baseline-red task whose fix touched its files after its merge, or an outcomes 'lost'; suggest opus when sonnet's rate exceeds opus's by 0.3 with 5+ samples each, else sonnet, printing the numbers; --model overrides. 2) escalate on every review with changes — rejected: Foreman can't see review rounds, and outcomes are the honest signal. 3) per-file-area routing — later: too few samples per area now. Choice 1.
## Risks and rollback
Cost: opus costs more; escalation needs a measured gap with samples on both sides, never a hunch. Rollback: the suggestion is a line; the default stays sonnet.
## Execution prompt
## Steps
1. [x] red tests: seeded lane outcomes escalate; too few keep sonnet; --model overrides; the model recorded
2. [x] record the model; the rework join from outcomes and baseline links; the suggestion line
3. [x] docs lines in the report
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lanes test_outcomes 2>&1 | tail -25` → exit 0 · Ran 63 tests in 39.5s (15 classes, 16 at a time; slowest: Lanes 39s, Survival 28s, ModelRouter 15s) / OK [ran] [tree 28b32bbd95df] (2026-10-31T07:18:30Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_outcomes 2>&1 | tail -25` → exit 0 · Ran 63 tests in 39.5s (15 classes, 16 at a time; slowest: Lanes 39s, Survival 28s, ModelRouter 15s) / OK [ran] [tree 28b32bbd95df] (2026-10-31T07:18:30Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_outcomes` → exit 0 · Ran 63 tests in 40.8s (15 classes, 16 at a time; slowest: Lanes 40s, Survival 33s, ModelRouter 17s) / OK [ran] [tree 28b32bbd95df] (2026-10-31T07:19:13Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_builder test_cli test_guard_cases test_lanes test_outcomes test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 263 tests in 39.5s (68 classes, 16 at a time; slowest: TaskLifecycle 39s, Lanes 36s, Survival 31s) / FAILED (1 classes) [ran] [tree 28b32bbd95df] (2026-10-31T07:19:54Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_builder test_cli test_guard_cases test_lanes test_outcomes test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 2 fail / Ran 154 tests across 4 files. [31.64s] [ran] [tree a6cb0419f9b8] (2026-10-31T07:22:20Z)
- `cd plugin/tests && python3 -m unittest -q test_outcomes test_lanes` → ✗ exit 1 · Ran 68 tests in 42.963s / FAILED (failures=1, errors=2) (start tree + this task's tests) [ran] [tree e1ef079446e8] (2026-10-31T07:35:28Z)
- `cd plugin/tests && python3 -m unittest -q test_outcomes test_lanes` → exit 0 · Ran 68 tests in 42.716s / OK [ran] [tree e1ef079446e8] (2026-10-31T07:35:28Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_outcomes test_builder` → exit 0 · Ran 93 tests in 15.0s (24 classes, 16 at a time; slowest: Lanes 15s, Survival 12s, ModelRouter 7s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:35:43Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_outcomes test_builder` → exit 0 · Ran 93 tests in 15.0s (24 classes, 16 at a time; slowest: Lanes 15s, Survival 12s, ModelRouter 7s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:35:59Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_outcomes test_builder` → exit 0 · Ran 93 tests in 15.0s (24 classes, 16 at a time; slowest: Lanes 15s, Survival 12s, ModelRouter 7s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:36:14Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_outcomes` → exit 0 · Ran 69 tests in 14.5s (16 classes, 16 at a time; slowest: Lanes 14s, Survival 12s, ModelRouter 7s) / OK [ran] [tree e1ef079446e8] (2026-10-31T07:36:30Z)
- (audit intent) `self-review of the diff: one suggestion line from closed briefs and outcomes; sonnet stays the default until a measured gap with 5+ samples on each side; --model overrides; the baseline link is a task id in a baseline brief (weaker than a file join, noted)` → #9's router: the builder model follows how past lanes held up, not a constant (test_outcomes red-to-green) [tree e1ef079446e8] (2026-10-31T07:36:30Z)
- (audit edge) `self-review of the diff: one suggestion line from closed briefs and outcomes; sonnet stays the default until a measured gap with 5+ samples on each side; --model overrides; the baseline link is a task id in a baseline brief (weaker than a file join, noted)` → too little history keeps sonnet and says so; history starts with lanes briefed after this change [tree e1ef079446e8] (2026-10-31T07:36:30Z)
## Log
- 2026-10-31T07:15:16Z created
- 2026-10-31T07:15:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2291.builder.md
- 2026-10-31T07:15:36Z focused
- 2026-10-31T07:26:00Z merged worktree-agent-a582c808d79d08894 (5 file(s))
- 2026-10-31T07:27:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a582c808d79d08894
- 2026-10-31T07:34:02Z focused
- 2026-10-31T07:36:14Z scope: plugin/lib/fmlanes.py (model_route, builder_brief), plugin/lib/fmcli.py (--model), plugin/tests/test_outcomes.py, test_lanes.py, test_builder.py, MASTER.md, CHANGELOG.md
- 2026-10-31T07:37:49Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2077 [RESEARCH L, planned, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- decision 2026-10-30: [cites: user steer 2026-10-30] Standing rule (user steer): weakness-finding uses signals Foreman didn't author — outcome survival (fm outcomes: reve…
- the similar finished task took 2 steps
## Lessons
- Escalate on outcomes Foreman can see (re-fixes, reverts, lost survival), never on a hunch about difficulty
## Files touched
- plugin/tests/test_outcomes.py
- plugin/tests/test_lanes.py
- .fm-scratch/e.json
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- plugin/tests/test_builder.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmbudget.py
- plugin/lib/fmexam.py
- plugin/lib/fmlong.py
- plugin/tests/test_exam.py
- plugin/tests/test_long.py
