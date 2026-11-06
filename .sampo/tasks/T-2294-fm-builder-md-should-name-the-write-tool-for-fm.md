---
id: T-2294
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T08:15:21Z
updated: 2026-10-31T08:43:25Z
builder_model: sonnet
base: 899b26cf41a13cc4800fee21675e1350460b5f02
base_tree: 2e48a5bdf5f662741ece42c8908c650c128c7fc7
plan0_at: 2026-10-31T08:22:21Z
plan0_scope: []
verified: strong
---
# fm-builder.md: scratch and batch files are written with the Write tool, never a heredoc
## Raw request
> fm-builder.md should name the Write tool for .fm-scratch batch files: builders still hit heredoc refusals (10x); assert the wording in test_builder.py
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm-builder.md says to create .fm-scratch/ files (an fm edit batch, notes, drafts) with the Write tool and names heredocs and cat > as refused there; test_builder asserts both phrases — verify with `python3 plugin/tests/run.py test_builder`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reword fm-builder.md's scratch rule to name the Write tool; assert it in test_builder's worktree-contract test
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_builder 2>&1 | tail -5` → ✗ exit 1 · Ran 26 tests in 54.5s (9 classes, 16 at a time; slowest: Contract 48s, Brief 22s, LaneMergeGate 12s) / FAILED (1 classes) [ran] [tree 210fed6aef04] (2026-10-31T08:23:34Z)
- (step 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 26 tests in 59.0s (9 classes, 16 at a time; slowest: Contract 57s, Brief 20s, LaneMergeGate 12s) / OK [ran] [tree 9fa1266e9996] (2026-10-31T08:24:41Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_builder test_claude test_debug test_diagnosis test_docs test_doctor test_export test_foresight test_genesis test_handoff test_judgment test_lanes test_lib_hostile test_onwrite test_roles test_session test_session_fixes test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 2 fail / Ran 154 tests across 4 files. [120.17s] [ran] [tree 9fa1266e9996] (2026-10-31T08:30:00Z)
- (step 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 26 tests in 18.0s (9 classes, 16 at a time; slowest: Contract 17s, Brief 8s, LaneMergeGate 4s) / OK [ran] [tree 9fa1266e9996] (2026-10-31T08:41:13Z)
- (ac 1) `python3 plugin/tests/run.py test_builder` → exit 0 · Ran 26 tests in 17.2s (9 classes, 16 at a time; slowest: Contract 17s, Brief 6s, LaneMergeGate 4s) / OK [ran] [tree 7d9717ff9e89] (2026-10-31T08:41:47Z)
- (audit intent) `self-review of the merged diff: wording only in the builder contract, plus a whitespace-flattened assertion of both phrases in test_builder` → builders read that .fm-scratch files are made with the Write tool and that heredocs and cat > are refused, the cause of 10 refused heredocs in the friction digest [tree 7d9717ff9e89] (2026-10-31T08:41:47Z)
- (audit edge) `self-review of the merged diff: wording only in the builder contract, plus a whitespace-flattened assertion of both phrases in test_builder` → the test flattens whitespace so a rewrap doesn't break it; it proves the words are there, not that builders comply [tree 7d9717ff9e89] (2026-10-31T08:41:47Z)
- (audit self) `self-review of the merged diff: wording only in the builder contract, plus a whitespace-flattened assertion of both phrases in test_builder` → no findings [tree 7d9717ff9e89] (2026-10-31T08:41:47Z)
## Log
- 2026-10-31T08:15:21Z created
- 2026-10-31T08:19:56Z planned from capture
- 2026-10-31T08:21:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2294.builder.md
- 2026-10-31T08:22:18Z focused
- 2026-10-31T08:40:42Z merged worktree-agent-ab86eb7bb8f9e7ec7 (2 file(s))
- 2026-10-31T08:40:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab86eb7bb8f9e7ec7
- 2026-10-31T08:40:53Z focused
- 2026-10-31T08:41:26Z scope: plugin/agents/fm-builder.md, plugin/tests/test_builder.py, CHANGELOG.md
- 2026-10-31T08:43:19Z done
- 2026-10-31T08:43:25Z committed fea468ec (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2259 [FEATURE S, done, 1 steps] Builders write scratch files with cat > /tmp/claude-… heredocs and get 'isolated in the… — lesson: An instruction to write a file must …
- T-1917 [FIX M, done, 2 steps] Guard lets a quoted heredoc write a scratch draft that fm edit or an on-disk script reads — lesson: A guard exemption keyed on a filename m…
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
## Lessons
- A rule a builder keeps breaking needs the tool named in the rule (the Write tool), not the action (write the batch)
## Files touched
- plugin/tests/test_builder.py
- plugin/agents/fm-builder.md
- CHANGELOG.md
