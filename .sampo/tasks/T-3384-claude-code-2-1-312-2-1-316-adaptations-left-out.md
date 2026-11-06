---
id: T-3384
type: FEATURE
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/doctor.py, plugin/tests/test_doctor.py]
depends_on: []
source: discovered
created: 2026-11-06T06:41:43Z
updated: 2026-11-06T11:13:05Z
base: 019c4c4cfde0468d58e407ecb302cc1efcb28c9d
base_tree: d9b1fcb5d9c62c98583101806fc081c72a3bbcf6
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:59:11Z
plan0_scope: []
builder_returned: 2026-11-06T09:26:36Z
lane_stop: merged 2026-11-06T11:12:35Z
verified: strong
---
# Claude Code 2.1.312-2.1.316 adaptations left out of T-3341: per-lane-class subagent…
## Raw request
> FEATURE: Claude Code 2.1.312-2.1.316 adaptations left out of T-3341: per-lane-class subagent effort (CLAUDE_CODE_SUBAGENT_EFFORT), the 24-concurrent-hooks cap warning, safety_event ingestion, group budgets, the worktree-lifetime gate (see T-3341's raw request)
## Interpretation
Two items survive the T-3341 review: doctor shows the per-lane-class subagent effort (builder, reviewer, scout) and warns when CLAUDE_CODE_SUBAGENT_EFFORT (2.1.316) overrides them all; doctor gates fm-builder's worktree-lifetime reliance on Claude Code 2.1.311.
## Assumptions (confidence)
## Acceptance criteria
- [x] doctor names each lane class's effort, warns when CLAUDE_CODE_SUBAGENT_EFFORT overrides it, and CC_FEATURES gates fm-builder's worktree on 2.1.311 — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
Option A: new env per class (impossible: one global var). B: doctor check reading the agents' effort: frontmatter per class plus the env override. C: also CC_FEATURES row for worktree lifetime 2.1.311 on agents/fm-builder.md. Choose B and C: no new API invented. Items 2-4 moot per the 06:42 log (hook cap prompt/agent only, safety_event stopped in 2.1.312, group budgets gateway-only); Sampo ingests no OTel stream. Row placed away from T-3341's SubagentStop row to avoid a merge conflict.
## Risks and rollback
A wrong version number gives a false WARN on old CC only; revert the commit.
## Execution prompt
## Steps
1. [x] failing tests
2. [x] check_subagent_effort and CC_FEATURES row
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 116 tests in 480.7s (44 jobs, 16 at a time; slowest: ViewsRepair 6s, LockProbe 3s, Timing 2s) / FAILED (1 classes: test_doctor.Checks) [ran] [tree acea0ae13cc9] [world 2f1906870a] (2026-11-06T09:07:33Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 116 tests in 605.0s (44 jobs, 16 at a time; slowest: Timing 16s, ViewsRepair 3s, LockProbe 3s) / OK [ran] [tree acea0ae13cc9] [world 2f1906870a] (2026-11-06T09:11:57Z)
- (step 2) `python3 plugin/tests/run.py test_doctor.Checks` → exit 0 · Ran 34 tests in 157.9s (1 jobs, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 517936faa23a] [world 2f1906870a] (2026-11-06T09:24:15Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [17.98s] [ran] [tree 517936faa23a] [world 2f1906870a] (2026-11-06T09:26:20Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 357e887063e0] (2026-11-06T11:12:37Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 117 tests in 3.3s (44 jobs, 16 at a time; slowest: ViewsRepair 3s, LockProbe 2s, Timing 2s) / OK [ran] [tree 357e887063e0] [world 2f1906870a] (2026-11-06T11:12:43Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 357e887063e0] (2026-11-06T11:12:43Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 357e887063e0] (2026-11-06T11:12:43Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 357e887063e0] (2026-11-06T11:12:43Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 357e887063e0] (2026-11-06T11:12:43Z)
## Log
- 2026-11-06T06:41:43Z created
- 2026-11-06T06:42:28Z scope after T-3341 review: keep CLAUDE_CODE_SUBAGENT_EFFORT per lane class (2.1.316) and the subagent worktree-lifetime doctor gate (2.1.311); drop as moot: 24-hook cap (prompt/agent hooks only, Sampo has none), safety_event (CC stopped sending it in 2.1.312), pooled group budgets (gateway admin only)
- 2026-11-06T08:59:03Z set tier=S
- 2026-11-06T08:59:08Z planned: it has criteria and steps
- 2026-11-06T08:59:10Z focused
- 2026-11-06T08:59:11Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T11:12:35Z merged worktree-agent-ab09de40662e4ac86 (2 file(s))
- 2026-11-06T11:12:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab09de40662e4ac86
- 2026-11-06T11:12:35Z focused
- 2026-11-06T11:12:36Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/doctor.py', 'plugin/tests/test_doctor.py']
- 2026-11-06T11:12:36Z scope: widened at merge to the reviewed lane's own diff (777427b01), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T11:13:03Z done
- 2026-11-06T11:13:05Z committed 5ddaa3e49 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3341 [FEATURE S, planned, 2 steps] Claude Code 2.1.311-2.1.318 adaptation: doctor gate for SubagentStop firing once per subagent (2.1.311; older versions overcount bud…
- research mission-20261029-104513: Request: keep super ultimate recursive brainstorming, and implementing all ideas, super ultimate improve foreman in all ways [stale: de…
- research mission-20261029-104513.pack: keep super ultimate recursive brainstorming, and implementing all ideas, super ultimate improve foreman in all ways [stale: demo/l…
- decision 2026-10-30: Home's 5-open scout cap is shared by doctor items routed from every project
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/sampo/doctor.py
- CHANGELOG.md
