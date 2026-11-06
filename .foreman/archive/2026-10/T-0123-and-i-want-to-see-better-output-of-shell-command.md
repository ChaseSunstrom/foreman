---
id: T-0123
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:14:20Z
updated: 2026-10-03T05:29:00Z
base: 9a25f5019f8182786755105f7bb8f29ea87a4507
base_tree: b10f4fd1c7ff892a0335521ab56530c01fb3e9ac
verified: strong
---
# Shell output as a Foreman summary, full formatted output in the pane
## Raw request
> and I want to see better output of shell commands/claude messages etc, instead of having the regular claude code panel, can you have it show a summary of that, and also able to see nice formatted output of commands and stuff, etc.
## Interpretation
User: instead of Claude Code's regular output panel for shell commands, a summary; and nicely formatted output of commands to look at.
## Assumptions (confidence)
## Acceptance criteria
- [x] a long Bash result draws as summary + key lines + more; the pane shows the last output formatted; errored calls stay the engine's — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) hook ui.render ToolResult for Bash: draw status, line count and up to 6 key lines (failures and errors first, else the tail), each coloured by meaning, with '… N more lines (/fm → Output)'; keep the engine's view for errored calls; the pane gains an Output card with the last command's full output (200 lines, coloured); (b) rewrite the ToolUse header row too. Choice (a): ToolResult is the output panel exactly, the header stays Claude Code's; errors keep the engine's full text where it matters most.
## Risks and rollback
## Execution prompt
## Steps
1. [x] kit: outputSummary + tone (tests)
2. [x] ToolResult hook + outputs atom + pane card
3. [x] live render check, docs
## Resume here
<!-- auto -->
- 2026-10-03T05:25:17Z step 1/3: kit: outputSummary + tone (tests)
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG.md: shell output summary
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 39 tests across 1 file. [1.88s] [ran] [tree c456ea8dd85d] (2026-10-03T05:28:03Z)
- (step 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 39 tests across 1 file. [1.86s] [ran] [tree c456ea8dd85d] (2026-10-03T05:28:05Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 39 tests across 1 file. [1.82s] [ran] [tree c456ea8dd85d] (2026-10-03T05:28:07Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 39 tests across 1 file. [1.81s] [ran] [tree c456ea8dd85d] (2026-10-03T05:28:49Z)
- (audit intent) `self-review + 39 mod tests; validate; tsc` → shell output is a summary with the key lines coloured; the full formatted output is in the pane's Output card [tree c456ea8dd85d] (2026-10-03T05:28:49Z)
- (audit edge) `self-review + 39 mod tests; validate; tsc` → errors keep the engine's text; empty output, interrupted and backgrounded calls each one line; '0 failed' reads as ok; colour codes stripped; fm commands keep their quiet row; subagent calls don't replace the Output card [tree c456ea8dd85d] (2026-10-03T05:28:49Z)
- (audit intent) `self-review + 39 mod tests; validate; tsc` → shell output is a summary with the key lines coloured; the full formatted output is in the pane's Output card [tree c456ea8dd85d] (2026-10-03T05:29:00Z)
- (audit edge) `self-review + 39 mod tests; validate; tsc` → errors keep the engine's text; empty output, interrupted and backgrounded calls each one line; '0 failed' reads as ok; colour codes stripped; fm commands keep their quiet row; subagent calls don't replace the Output card [tree c456ea8dd85d] (2026-10-03T05:29:00Z)
- (audit adversary) `self-review + 39 mod tests; validate; tsc` → fmguard.py and test_guard.py in this diff are T-0135's (reviewed and committed in 19db140 while this task was paused); this task's own change renders command output as text only [tree c456ea8dd85d] (2026-10-03T05:29:00Z)
## Log
- 2026-10-03T04:14:20Z created
- 2026-10-03T05:24:53Z planned from capture
- 2026-10-03T05:24:53Z focused
- 2026-10-03T05:25:17Z paused: focus moved to T-0135
- 2026-10-03T05:26:42Z focused
- 2026-10-03T05:29:00Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0108 [FEATURE L, done, 7 steps] foreman-ui 0.4.0: mascot, whole-queue progress, size words, clean permission notes, quieter finished rows — lesson: When a note summari…
- T-0131 [FEATURE M, done, 3 steps] See the rendered UI: a tmux + PNG snapshot tool for foreman-ui, and a first review — lesson: Look at the real render before polishing: …
- T-0122 [FEATURE M, done, 4 steps] UI polish from the live render: narrow band, colored type words, quiet controls, human next, cleaner header and footer — lesson: Judge …
- T-0015 [FEATURE L, done, 5 steps] Foreman-aware conversation view: output style, richer badge and statusline, pending-approval display, live step tracking
- similar finished tasks took 3–7 steps
## Lessons
- Replace only the part of a row you can do better (ToolResult), keep the engine's where it matters most (errors)
## Files touched
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
