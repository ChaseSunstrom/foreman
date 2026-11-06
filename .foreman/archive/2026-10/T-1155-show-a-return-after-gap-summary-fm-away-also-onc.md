---
id: T-1155
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:19:38Z
base: 41972ca335372d973f8d8c8a4dd70b249013efea
base_tree: fd5f0476fbe03785c8a0216d46958f5ca38ef4ba
plan0_at: 2026-10-16T10:48:09Z
plan0_scope: []
verified: strong
---
# Show a return-after-gap summary (`fm away`, also once at session start) of what closed, bl
## Raw request
> FEATURE: Show a return-after-gap summary (`fm away`, also once at session start) of what closed, blocked, was asked, or was reverted since the user last spoke.
> DONE-WHEN: a test seeds a ledger with events before and after a simulated gap and `fm away` lists the closed, blocked, pending-ask and reverted items after the gap and nothing before it
## Interpretation
After a gap (the user's last prompt more than 2 h ago, or on demand), one short summary of what happened since they last spoke: tasks closed, tasks blocked (with why), asks still pending, and anything reverted or rolled back, each one line with its id. Nothing from before the gap.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm away lists closed, blocked, pending-ask and reverted items after the gap and nothing before it; a session start after a 2 h gap carries one away line, a short gap none — verify with `python3 plugin/tests/run.py test_away`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new fm away verb over the ledger events since the last user-prompt event, plus one line injected at SessionStart/UserPromptSubmit when the gap exceeds 2 h; (b) fm digest --since; (c) a pane-only line. Choice: (a), reusing the ledger readers fm digest uses; why: digest is a weekly cost screen and the pane isn't seen headless. Register the verb next to digest's registration in fmcli (tier Reports).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_away.py): seeded ledger before/after a gap; pending ask listed; nothing before; session-start line only after a long gap
2. [x] fm away (where the last user-prompt time comes from, the ledger readers digest uses) and the one-line session-start injection
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_away` → exit 0 · Ran 3 tests in 4.3s (1 classes, 16 at a time; slowest: Away 4s) / OK [ran] [tree ac6d6bcc1841] (2026-10-16T10:49:33Z)
- (step 2) `python3 plugin/tests/run.py test_away` → exit 0 · Ran 3 tests in 4.8s (1 classes, 16 at a time; slowest: Away 4s) / OK [ran] [tree ac6d6bcc1841] (2026-10-16T10:49:41Z)
- (step 2) `python3 plugin/tests/run.py test_away` → exit 0 · Ran 6 tests in 1.0s (1 classes, 16 at a time; slowest: Away 1s) / OK [ran] [tree 245f0f0246a9] (2026-10-16T11:14:25Z)
- (ac 1) `python3 plugin/tests/run.py test_away test_hooks` → exit 0 · Ran 163 tests in 74.3s (21 classes, 16 at a time; slowest: Stop 74s, PreToolUse 40s, SessionStart 29s) / OK [ran] [tree 925a29fad84d] (2026-10-16T11:16:06Z)
- (ac 1) `python3 plugin/tests/run.py test_away` → exit 0 · Ran 6 tests in 2.1s (1 classes, 16 at a time; slowest: Away 2s) / OK [ran] [tree c37cfbfee70a] (2026-10-16T11:16:20Z)
- (audit intent) `self review of the merged diff: added on every SessionStart incl. compact, 150 ms from per-row brief lookups, oldest ids shown, untested git Revert path; builder fixed all four test-first (the Revert test caught a real %cI parse bug); measured 35 ms on this repo's ledger, SessionStart bench median 55.6 -> 55.7 ms` → a returning user sees what changed while away in one line, details on demand [tree c37cfbfee70a] (2026-10-16T11:16:20Z)
- (audit adversary) `self review of the merged diff: added on every SessionStart incl. compact, 150 ms from per-row brief lookups, oldest ids shown, untested git Revert path; builder fixed all four test-first (the Revert test caught a real %cI parse bug); measured 35 ms on this repo's ledger, SessionStart bench median 55.6 -> 55.7 ms` → block reasons and ask text are the project's own, cut to 100 chars; nothing executed [tree c37cfbfee70a] (2026-10-16T11:16:20Z)
- (audit edge) `self review of the merged diff: added on every SessionStart incl. compact, 150 ms from per-row brief lookups, oldest ids shown, untested git Revert path; builder fixed all four test-first (the Revert test caught a real %cI parse bug); measured 35 ms on this repo's ledger, SessionStart bench median 55.6 -> 55.7 ms` → sensitive projects log no prompts, so no gap and no line; compact/clear starts add nothing [tree c37cfbfee70a] (2026-10-16T11:16:20Z)
- (audit operator) `self review of the merged diff: added on every SessionStart incl. compact, 150 ms from per-row brief lookups, oldest ids shown, untested git Revert path; builder fixed all four test-first (the Revert test caught a real %cI parse bug); measured 35 ms on this repo's ledger, SessionStart bench median 55.6 -> 55.7 ms` → line names counts and the newest ids, fm away lists by kind [tree c37cfbfee70a] (2026-10-16T11:16:20Z)
- (audit maintainer) `self review of the merged diff: added on every SessionStart incl. compact, 150 ms from per-row brief lookups, oldest ids shown, untested git Revert path; builder fixed all four test-first (the Revert test caught a real %cI parse bug); measured 35 ms on this repo's ledger, SessionStart bench median 55.6 -> 55.7 ms` → reuses ledger_events and fmoutcomes.reverts; one new module [tree c37cfbfee70a] (2026-10-16T11:16:20Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T10:47:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1155.builder.md
- 2026-10-16T10:48:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1155.builder.md
- 2026-10-16T10:48:08Z focused
- 2026-10-16T11:14:47Z merged worktree-agent-ab097e6feab5445f8 (4 file(s))
- 2026-10-16T11:14:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab097e6feab5445f8
- 2026-10-16T11:14:51Z focused
- 2026-10-16T11:16:17Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T11:19:37Z done
- 2026-10-16T11:19:38Z committed ea0244a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar finished tasks took 2–2 steps
## Lessons
- a session-start addition must be timed on the real ledger, not the bench fixture, which had no gap
## Files touched
- plugin/tests/test_away.py
- plugin/lib/fmaway.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- MASTER.md
- CHANGELOG.md
