---
id: T-0779
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmlanes.py, plugin/tests/test_lanes.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:29:15Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
group: headless child command budget and effort
base: ac8480359a4b41ebf39457a944ad189d7521a6c0
base_tree: 1b9fa94e43dd2d984f28008b7b7b9b433422ca7d
verified: strong
---
# Lane briefs pass a per-tier effort with the model
## Raw request
> PERF: Lane briefs pass a per-tier effort with the model
> CONTEXT: T-0760, cluster model-routing (T-0755 asked for lower models). fmlanes.py:163-165 passes model "sonnet" for S builders and nothing for M. The Agent tool takes per-call effort (2.1.292). T-0768 set effort in the agents' frontmatter.
> DONE-WHEN: fm lane brief's Agent line names effort (S: medium, M: high) beside the model; test_lanes pins it.
## Interpretation
fmlanes.py:164 tells the main thread to launch an S builder with model sonnet and an M builder with the main model, both at the session's effort. The Agent tool takes a per-call effort (2.1.292). S builders get effort medium (small, well-specified diffs), M builders high; the reviewer and recon already set theirs in frontmatter (T-0768).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane brief's Agent line says effort: "medium" for S and effort: "high" for M — verify with `cd plugin/tests && python3 -m unittest test_lanes`
## Non-goals
## Approach (options → choice → why)
Options: effort in fm-builder's frontmatter (one value for S and M); per-call effort in the lane brief's Agent line (per tier); a learned table (no data yet). Chose per-call by tier.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing lanes test
2. [x] effort in the Agent line
## Resume here
## Docs impact
## Verification evidence
- (step 2) `cd plugin/tests && python3 -m unittest test_lanes test_builder` → exit 0 · Ran 28 tests in 36.544s / OK [ran] [tree 6a3a1dfbaa50] (2026-10-14T16:19:39Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (33 pass, 5 warn, 0 fail) (slower: 17.2 s vs a usual 8.2 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed (slower: 9.0 s vs a usual 3.9 s); python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                35.2    41.7     150  [0] / SessionEnd                  34.2    45.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at [ran] [tree 6a3a1dfbaa50] (2026-10-14T16:23:01Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (32 pass, 6 warn, 0 fail) (slower: 28.1 s vs a usual 8.6 s); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed (slower: 8.3 s vs a usual 3.9 s); python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                56.5   132.7     150  [0] / SessionEnd                  62.5   119.4     150  [0] (slower: 37.2 s vs a usual 13.0 s); claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/fore [ran] [tree 6a3a1dfbaa50] (2026-10-14T16:24:55Z)
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_the_brief_agent_line_names_effort_by_tier` → ✗ exit 1 · Ran 1 test in 0.314s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree d60c5f4b593b] (2026-10-14T16:26:42Z)
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_the_brief_agent_line_names_effort_by_tier` → exit 0 · Ran 1 test in 0.365s / OK [ran] [tree d60c5f4b593b] (2026-10-14T16:26:42Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_the_brief_agent_line_names_effort_by_tier` → exit 0 · Ran 1 test in 0.589s / OK [ran] [tree d60c5f4b593b] (2026-10-14T16:26:46Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_lanes test_builder` → exit 0 · Ran 28 tests in 23.390s / OK [ran] [tree d60c5f4b593b] (2026-10-14T16:27:09Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_lanes` → exit 0 · Ran 11 tests in 6.229s / OK [ran] [tree d60c5f4b593b] (2026-10-14T16:27:16Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_lanes` → exit 0 · Ran 11 tests in 5.056s / OK [ran] [tree d60c5f4b593b] (2026-10-14T16:29:07Z)
- (audit edge) `self: merged diff read (3 lines in fmlanes.py, one test); S keeps model sonnet and gains effort medium, M gets effort high with no model; the builder's missing red run was replaced by fm task prove (fails on the start tree, passes now)` → a lane brief written before this change has no effort and runs at the session's effort, as before [tree d60c5f4b593b] (2026-10-14T16:29:07Z)
- (audit self) `self: merged diff read (3 lines in fmlanes.py, one test); S keeps model sonnet and gains effort medium, M gets effort high with no model; the builder's missing red run was replaced by fm task prove (fails on the start tree, passes now)` → no findings [tree d60c5f4b593b] (2026-10-14T16:29:07Z)
- (audit edge) `self: merged diff read (3 lines in fmlanes.py, one test); S keeps model sonnet and gains effort medium, M gets effort high with no model; the builder's missing red run was replaced by fm task prove (fails on the start tree, passes now)` → a lane brief written before this change has no effort and runs at the session's effort, as before [tree d60c5f4b593b] (2026-10-14T16:29:15Z)
- (audit self) `self: merged diff read (3 lines in fmlanes.py, one test); S keeps model sonnet and gains effort medium, M gets effort high with no model; the builder's missing red run was replaced by fm task prove (fails on the start tree, passes now)` → no findings [tree d60c5f4b593b] (2026-10-14T16:29:15Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:07:09Z planned from capture
- 2026-10-14T16:12:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0779.builder.md
- 2026-10-14T16:12:47Z focused
- 2026-10-14T16:13:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a52ccb113e6aec41a
- 2026-10-14T16:18:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0779.builder.md
- 2026-10-14T16:18:17Z focused
- 2026-10-14T16:26:35Z merged worktree-agent-a2ed7c103ff820138 (2 file(s))
- 2026-10-14T16:26:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2ed7c103ff820138
- 2026-10-14T16:26:35Z focused
- 2026-10-14T16:29:14Z scope: the other files are T-0803's and T-0778's, committed by those tasks while this lane ran; T-0779's own diff is fmlanes.py and test_lanes.py (merge b763f8a)
- 2026-10-14T16:29:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0373 [FEATURE M, done, 2 steps] Model routing: subagents on the cheapest model that can do the job; builder lanes on Sonnet for S tasks — lesson: Most of the routing a…
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research rsi-20261009-review: 1. **Answer.** Two guard-related frictions are grounded in code: the guard misreads remote interpreter code run over `ssh` as local Foreman…
- decision 2026-09-26: Brainstorm subagents get no tools; the main thread builds one context pack and grounds every idea against the code afterwards
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_lanes.py
## Measurements
S builder effort: the session's own (high or above) → medium; M: unchanged → high (explicit). Token effect per lane not measured yet: it shows in fm cost --sessions after the next S lanes (no builder ran at both efforts on the same task)
## Lessons
- a lane's builder should record the failing run before the fix; when it can't, fm task prove on merge gives the red→green
## Files touched
- .claude/worktrees/agent-a2ed7c103ff820138/plugin/tests/test_lanes.py
- .claude/worktrees/agent-a2ed7c103ff820138/plugin/lib/fmlanes.py
- MASTER.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmsetup.py
- plugin/tests/test_doctor.py
- plugin/tests/test_hooks.py
- plugin/tests/test_lanes.py
- plugin/tests/test_setup.py
