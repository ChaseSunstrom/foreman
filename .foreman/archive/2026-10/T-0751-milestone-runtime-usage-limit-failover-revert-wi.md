---
id: T-0751
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-09T21:33:07Z
updated: 2026-10-09T21:37:12Z
batch: [T-0731, T-0732]
base: c05a8e08d73b48afa2e23e9d90806aa7b6aa0b03
base_tree: bb6cd532bb91c677b619aa4e6a9a76cf7f683414
verified: strong
---
# Milestone: Runtime — usage-limit failover, revert with dependents, budget-fit queue, spike lanes
## Raw request
> T-0731: Usage-limit failover (T-0447 rest, deferred from T-0675): when fm run hits a usage limit with no wait budget left, hand the task to another installed agent via fm session (codex, gemini) with its packet
> T-0732: Planning leftovers (deferred from T-0677): fm task revert ID listing dependents (fm relate) before undoing; fm run ordering the queue to fit the remaining budget; a SPIKE task type that runs in a discarded lane
## Interpretation
Do T-0731, T-0732 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0751. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0731: Usage-limit failover (T-0447 rest, deferred from T-0675): when fm run hits a usage limit w works — verify with `python3 plugin/tests/run.py -p test_serve.py -k Failover`
- [x] T-0732: Planning leftovers (deferred from T-0677): fm task revert ID listing dependents (fm relate works — verify with `python3 plugin/tests/run.py -p test_runtime.py`
## Non-goals
## Approach (options → choice → why)
Failover (T-0731): fm run --failover codex|gemini|opencode, opt-in per run (it sends the task's handoff packet to another provider, so never by default or by setting): when a usage limit outlasts --wait, the task's packet goes to a detached fm session of that agent, logged, and the run stops. Revert (T-0732a): fm task revert ID lists the task's commits (its id in the subject or a Foreman-Task trailer), the open tasks that depend on or name it, and the git revert command; it never reverts by itself. Fit (T-0732b): fm run --fit, or usage ahead of pace, takes S before M before L so more finishes before a limit. Spike (T-0732c): fm lane new ID --spike makes a throwaway lane that fm lane merge refuses; findings go in the brief, then fm lane rm. Options weighed: a SPIKE task type (touches every type table and gate: rejected for a lane flag), automatic reverts (hard to undo across dependents: rejected), a usage-cost model for fit (no per-task cost data yet: tier order instead).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0731: Usage-limit failover (T-0447 rest, deferred from T-0675): when fm run hits a usage limit w
2. [x] T-0732: Planning leftovers (deferred from T-0677): fm task revert ID listing dependents (fm relate
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md (Unreleased: runtime), ~/.claude/foreman/MASTER.md (fmserve), ~/.claude/foreman/plugin/skills/intake/references/planning.md (spike lanes)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_serve.py -p test_runtime.py -k Failover -k Revert -k Fit -k Spike` → ✗ exit 1 · Ran 4 tests in 0.4s (4 classes, 16 at a time; slowest: Revert 0s, Fit 0s, Failover 0s) / FAILED (4 classes) [ran] [tree 524a75dcd427] (2026-10-09T21:34:34Z)
- (step 1) `python3 plugin/tests/run.py -p test_serve.py -k Failover` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Failover 0s) / OK [ran] [tree db5e1719d40b] (2026-10-09T21:35:50Z)
- (step 2) `python3 plugin/tests/run.py -p test_runtime.py` → exit 0 · Ran 3 tests in 0.7s (3 classes, 16 at a time; slowest: Fit 1s, Revert 0s, Spike 0s) / OK [ran] [tree db5e1719d40b] (2026-10-09T21:35:51Z)
- (ac 1) `python3 plugin/tests/run.py -p test_serve.py -k Failover` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Failover 0s) / OK [ran] [tree db5e1719d40b] (2026-10-09T21:37:11Z)
- (ac 2) `python3 plugin/tests/run.py -p test_runtime.py` → exit 0 · Ran 3 tests in 0.7s (3 classes, 16 at a time; slowest: Fit 1s, Revert 0s, Spike 0s) / OK [ran] [tree db5e1719d40b] (2026-10-09T21:37:11Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1252 tests in 73.2s (419 classes, 16 at a time; slowest: Stop 44s, TaskLifecycle 28s, Bench 26s) / OK [ran] [tree db5e1719d40b] (2026-10-09T21:37:11Z)
- (audit intent) `main-thread review of the diff against both members' requests` → all four pieces shipped; revert lists and prints rather than acts, and SPIKE is a lane flag rather than a task type, both recorded in the approach with why [tree db5e1719d40b] (2026-10-09T21:37:11Z)
- (audit adversary) `main-thread review of the diff against both members' requests` → failover sends the task packet to another provider, so it is a per-run flag with no saved setting and no default, and a run without it never calls another agent (tested); the packet is redacted by fm task packet before it leaves [tree db5e1719d40b] (2026-10-09T21:37:11Z)
- (audit edge) `main-thread review of the diff against both members' requests` → fixed: task revert's commit parse was garbled (tested); a failover that can't start reports why and stops; --fit keeps a task waiting on an open dependency out of the order [tree db5e1719d40b] (2026-10-09T21:37:11Z)
## Log
- 2026-10-09T21:33:07Z created
- 2026-10-09T21:34:14Z criterion 1 verify: `` → `python3 plugin/tests/run.py -p test_serve.py -k Failover`
- 2026-10-09T21:34:14Z criterion 2 verify: `` → `python3 plugin/tests/run.py -p test_runtime.py`
- 2026-10-09T21:34:14Z focused
- 2026-10-09T21:37:12Z done
- 2026-10-09T21:37:12Z committed 5895f50 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- T-0677 [FEATURE M, done, 8 steps] Milestone: Features — Planning, briefs and queue — lesson: Seven small first versions fit one milestone when each reuses an existing me…
- decision 2026-10-09: Self-approve T-0691 (planning milestone, L) after the second-plan review: all six objections answered in the brief (independent replan triggers, def…
## Lessons
- Anything that sends a task's contents to another provider stays a per-run flag the user types; a saved setting would make the outward flow silent
## Plan gaps
- failed first: step 1 T-0731: Usage-limit failover (T-0447 rest, deferred from T-0675): when fm run hits a usage limit w
## Files touched
- plugin/tests/test_serve.py
- plugin/tests/test_runtime.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- plugin/lib/fmserve.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/planning.md
