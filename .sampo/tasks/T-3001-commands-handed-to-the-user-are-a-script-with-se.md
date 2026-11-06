---
id: T-3001
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks]
depends_on: []
source: discovered
created: 2026-11-04T18:52:01Z
updated: 2026-11-06T13:15:18Z
base: 4a071f512dd1846d1eef4d166677386001c96bfd
base_tree: 60cc54bf87559a732fc623eea93ed0ed81b84ed2
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T11:18:13Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
builder_returned: 2026-11-06T11:37:59Z
lane_stop: merged 2026-11-06T13:05:40Z
verified: strong
---
# A reply that hands the user a shell block with an irreversible step is held once unless it is a set -euo pipefail script with a check before that step
## Raw request
> Commands handed to the user are a script with set -euo pipefail and a check before every irreversible step, never a paste block that ends in rm: the Ollama move's paste block ran with rsync missing, moved the store aside and its last line deleted it (72 GB of models lost, re-pullable); a lesson for the firewall (T-2992's classes) and a Ward-style lint on suggested commands
## Interpretation
Stop hook gate beside _claims_gate: a fenced sh/bash block in the last reply with an irreversible line lacking set -euo pipefail or a prior guard is held once per reply.
## Assumptions (confidence)
## Acceptance criteria
- [x] the Stop hook holds once (per reply) a reply whose fenced shell block has an irreversible step (rm, a mv or rsync --delete of a directory, dd, mkfs, git reset --hard, git clean, DROP) without set -euo pipefail at its top or without a test/check line before that step, naming the step and the script shape; a block that is that script, or has no irreversible step, passes — verify with `python3 plugin/tests/run.py test_hooks`
- [x] the lesson is a standing rule: decisions.md carries 'commands handed to the user are a script with set -euo pipefail and a check before every irreversible step, never a paste block that ends in rm' (T-3001) — verify with `grep -q 'never a paste block that ends in rm' ~/.claude/foreman/state/projects/foreman-4a056f/decisions.md`
## Non-goals
## Approach (options → choice → why)
Regex gate _paste_gate(pl,g), key in g['paste'] like claims; no transcript needed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the Ollama-move block (rsync then rm -rf) held; the same as a set -euo pipefail script with a test -d check passes; a block with no irreversible step passes; held once
2. [x] the paste gate in hooks.py beside _claims_gate, and the standing decision
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop.test_a_paste_block_with_an_irreversible_step_is_held_once_unless_a_guarded_script` → ✗ exit 1 · Ran 1 tests in 1.7s (1 jobs, 16 at a time; slowest: Stop 0s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 2a11e70cd932] [world 2f1906870a] (2026-11-06T11:19:00Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 71 tests in 41.0s (1 jobs, 16 at a time; slowest: Stop 41s) / OK [ran] [tree 75170ccdfc71] [world 2f1906870a] (2026-11-06T11:19:44Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 635 tests in 22.1s (245 jobs, 16 at a time; slowest: Approvals 16s, UserPromptSubmit 13s, NoTaskGateMulti 11s) / FAILED (2 classes: test_core.LazyPatterns, test_left_out.LeftOut) [ran] [tree 75170ccdfc71] [world 2f1906870a] (2026-11-06T11:20:12Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.30s] [ran] [tree f3a5c26c5c74] [world 2f1906870a] (2026-11-06T11:21:24Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Stop test_core.LazyPatterns test_left_out` → exit 0 · Ran 77 tests in 5.2s (73 jobs, 16 at a time; slowest: Stop.test_a_tests_pass_claim_needs_a_passing_run_after_the_last_edit 4s, Stop.test_side_work_respects_lane_capacity_and_plan_reviews 2s, Stop.test [ran] [tree f3a5c26c5c74] [world 2f1906870a] (2026-11-06T11:21:34Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Stop test_core.LazyPatterns test_left_out` → exit 0 · Ran 78 tests in 18.6s (74 jobs, 16 at a time; slowest: Stop.test_a_tests_pass_claim_needs_a_passing_run_after_the_last_edit 3s, Stop.test_a_paste_block_false_holds_and_variants 2s, Stop.test_side_work [ran] [tree 11c20d0d8778] [world 2f1906870a] (2026-11-06T11:36:57Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.20s] [ran] [tree 11c20d0d8778] [world 2f1906870a] (2026-11-06T11:37:48Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 1fb5d53a9f8b] (2026-11-06T13:05:48Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 262 tests in 117.0s (185 jobs, 16 at a time; slowest: PreToolUse 17s, CapabilityMiss 14s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_takes_0_4_s 7s) / OK [ran] [tree 1fb5d53a9f8b] [world 2f1906870a] (2026-11-06T13:07:50Z)
- (ac 2) `grep -q 'never a paste block that ends in rm' ~/.claude/foreman/state/projects/foreman-4a056f/decisions.md` → exit 0 · (no output) [ran] [tree 1fb5d53a9f8b] [world 2f1906870a] (2026-11-06T13:07:50Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 1fb5d53a9f8b] (2026-11-06T13:07:50Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 1fb5d53a9f8b] (2026-11-06T13:07:50Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 1fb5d53a9f8b] (2026-11-06T13:07:50Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 1fb5d53a9f8b] (2026-11-06T13:07:50Z)
## Log
- 2026-11-04T18:52:01Z created
- 2026-11-05T02:41:07Z planned from capture
- 2026-11-05T02:41:08Z set approved=True
- 2026-11-05T02:41:08Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-11-05T02:41:08Z blocked: planned and approved; waits for a builder slot
- 2026-11-06T03:53:05Z unblocked
- 2026-11-06T11:18:12Z focused
- 2026-11-06T11:18:13Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T13:05:40Z merged worktree-agent-a78c981b8ad740e0d (2 file(s))
- 2026-11-06T13:05:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a78c981b8ad740e0d
- 2026-11-06T13:05:42Z focused
- 2026-11-06T13:05:47Z set scope=['plugin/lib/sampo/hooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks']
- 2026-11-06T13:05:47Z scope: widened at merge to the reviewed lane's own diff (e8524dd52), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T13:15:14Z done
- 2026-11-06T13:15:18Z committed da5255104 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-05: standing (T-3001): commands handed to the user are a script with set -euo pipefail and a check before every irreversible step, never a paste block t…
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- playbook Shell script errors (bash -n, ShellCheck, bats) (fm playbooks show build/shell-build)
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing tests: the Ollama-move block (rsync then rm -rf) held; the same as a set -euo pipefail scri…
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
