---
id: T-1181
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T12:51:51Z
base: db1389ae3ccbf901815b32734cc5080ebc321781
base_tree: 2030243a4e177b24cabdb2728fc02dac9e086c8a
plan0_at: 2026-10-16T12:39:30Z
plan0_scope: []
verified: strong
---
# At SubagentStop for an fm-reviewer, parse its `## lens: ...` sections and ranked findings
## Raw request
> FEATURE: At SubagentStop for an fm-reviewer, parse its `## lens: ...` sections and ranked findings out of last_assistant_message and log one `finding` event per finding for the active task, so reviewer findings are recorded without a hand-typed `fm task finding`.
> DONE-WHEN: a new test in plugin/tests (python3 plugin/tests/run.py -k reviewer_findings) feeds subagent_stop a sample reviewer message and sees one finding event per finding with the right lens and severity, and none for a non-reviewer agent.
## Interpretation
Reviewer findings feed builder briefs (T-1164) only when someone types fm task finding per finding. Record them automatically: when a foreman:fm-reviewer subagent stops, parse its Findings list (severity — path:line — issue — fix — confidence, the format plugin/agents/fm-reviewer.md asks for; also a lens named in a heading or the line) and log one 'finding' event per finding with verdict 'reported' for the task the review was about (the active task, or a T-id the reviewer message names). fm task finding ... confirmed/rejected still marks the verdict; defect classes count confirmed ones and, with this, the reported ones the main thread didn't reject.
## Assumptions (confidence)
## Acceptance criteria
- [x] a sample reviewer message at SubagentStop logs one finding event per finding with its severity and file, none for a non-reviewer agent, and defect_classes counts them unless rejected — verify with `python3 plugin/tests/run.py test_reviewer_findings`
## Non-goals
## Approach (options → choice → why)
Options: (a) in fmhooks.subagent_stop, when the agent type is foreman:fm-reviewer (the payload's agent_type or the transcript's), parse last_assistant_message with a tolerant regex for severity + path:line + text lines and log finding events {lens, severity, file, text, verdict: reported}; defect_classes counts confirmed plus reported-not-rejected; (b) require the main thread to pipe the review into fm task finding --from FILE (still manual); (c) parse at fm task finish from audit text (too late). Choice: (a). Tighten fm-reviewer.md's Findings line to one parseable line per finding ('- SEVERITY — path:line — issue — fix — confidence') and keep the parser tolerant of bold/backticks. Cap at 30 findings per stop; redact text.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_reviewer_findings.py): parse sample messages (plain, bold, backticked), non-reviewer ignored, cap, rejected excluded from classes
2. [x] Parser + logging in subagent_stop; defect_classes reads reported; fm-reviewer.md line format
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_reviewer_findings` → ✗ exit 1 · Ran 4 tests in 2.8s (1 classes, 16 at a time; slowest: ReviewerFindings 2s) / FAILED (1 classes) [ran] [tree 41ef0cdde093] (2026-10-16T12:39:58Z)
- (step 2) `python3 plugin/tests/run.py test_reviewer_findings test_hooks test_agents test_lanes` → ✗ exit 1 · Ran 212 tests in 167.0s (33 classes, 16 at a time; slowest: Stop 167s, PreToolUse 98s, PromptApprovals 68s) / FAILED (1 classes) [ran] [tree a8786112df91] (2026-10-16T12:43:07Z)
- (step 2) `python3 plugin/tests/run.py test_reviewer_findings` → exit 0 · Ran 4 tests in 6.9s (1 classes, 16 at a time; slowest: ReviewerFindings 6s) / OK [ran] [tree 357d036852b4] (2026-10-16T12:43:49Z)
- (ac 1) `python3 plugin/tests/run.py test_reviewer_findings test_defect_classes test_hooks` → exit 0 · Ran 164 tests in 52.2s (22 classes, 16 at a time; slowest: Stop 52s, PreToolUse 34s, SessionStart 26s) / OK [ran] [tree db7047438956] (2026-10-16T12:49:17Z)
- (ac 1) `python3 plugin/tests/run.py test_reviewer_findings` → exit 0 · Ran 4 tests in 5.8s (1 classes, 16 at a time; slowest: ReviewerFindings 6s) / OK [ran] [tree 0f4314c87c5c] (2026-10-16T12:49:35Z)
- (audit intent) `self: reviewed the merged diff: parser tolerant of bold/backticks/numbering, lens from the nearest heading, capped and redacted; logged only for fm-reviewer agent types; defect_classes dedupes by text and drops reported findings a rejected one matches; lens yields read only confirmed/rejected, so reported doesn't skew them` → reviewer findings feed builder briefs with no manual step [tree 0f4314c87c5c] (2026-10-16T12:49:35Z)
- (audit adversary) `self: reviewed the merged diff: parser tolerant of bold/backticks/numbering, lens from the nearest heading, capped and redacted; logged only for fm-reviewer agent types; defect_classes dedupes by text and drops reported findings a rejected one matches; lens yields read only confirmed/rejected, so reported doesn't skew them` → the message is reviewer output; a named T-id is used only with no active task; text redacted [tree 0f4314c87c5c] (2026-10-16T12:49:35Z)
- (audit edge) `self: reviewed the merged diff: parser tolerant of bold/backticks/numbering, lens from the nearest heading, capped and redacted; logged only for fm-reviewer agent types; defect_classes dedupes by text and drops reported findings a rejected one matches; lens yields read only confirmed/rejected, so reported doesn't skew them` → no lens heading -> self; a repeated stop is deduped by text in the classes [tree 0f4314c87c5c] (2026-10-16T12:49:35Z)
- (audit operator) `self: reviewed the merged diff: parser tolerant of bold/backticks/numbering, lens from the nearest heading, capped and redacted; logged only for fm-reviewer agent types; defect_classes dedupes by text and drops reported findings a rejected one matches; lens yields read only confirmed/rejected, so reported doesn't skew them` → nothing new to type [tree 0f4314c87c5c] (2026-10-16T12:49:35Z)
- (audit maintainer) `self: reviewed the merged diff: parser tolerant of bold/backticks/numbering, lens from the nearest heading, capped and redacted; logged only for fm-reviewer agent types; defect_classes dedupes by text and drops reported findings a rejected one matches; lens yields read only confirmed/rejected, so reported doesn't skew them` → one parser in fmlanes, the reviewer agent's output format documents it [tree 0f4314c87c5c] (2026-10-16T12:49:35Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T12:39:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1181.builder.md
- 2026-10-16T12:39:30Z focused
- 2026-10-16T12:48:17Z merged worktree-agent-a9fe682ac56c79c77 (4 file(s))
- 2026-10-16T12:48:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9fe682ac56c79c77
- 2026-10-16T12:48:23Z focused
- 2026-10-16T12:49:28Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T12:51:49Z done
- 2026-10-16T12:51:51Z committed a42fb552 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-1164 [FEATURE M, done, 2 steps] Feed a task's brief with the defect classes confirmed by reviewers in the last 30 days (`f — lesson: preview a classifier on the real d…
- research brainstorm-20261016-round4: 195 ideas, 46 clusters, each grounded against plugin/lib, hooks, skills, workflows, mods/foreman-ui and CHANGELOG.md. Paths are rela…
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
## Lessons
- when a feature depends on a manual record, make the producer emit it in a parseable form and log it at the hook
## Plan gaps
- failed first: step 1 Failing tests (test_reviewer_findings.py): parse sample messages (plain, bold, backticked), non-rev…
- failed first: step 2 Parser + logging in subagent_stop; defect_classes reads reported; fm-reviewer.md line format
## Files touched
- plugin/tests/test_reviewer_findings.py
- plugin/lib/fmlanes.py
- plugin/lib/fmhooks.py
- plugin/agents/fm-reviewer.md
- MASTER.md
- CHANGELOG.md
