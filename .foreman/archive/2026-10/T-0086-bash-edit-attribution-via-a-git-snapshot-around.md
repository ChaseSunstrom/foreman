---
id: T-0086
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_bash_touch.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-02T18:35:16Z
updated: 2026-10-03T08:05:40Z
base: 494308d65f0cd2b4f277fc37341132b53abe45ab
base_tree: 662c6e47003e03e101ce44de839cfaa8209043dd
verified: ok
---
# Bash-edit attribution: files a Bash command changed count as the task's touches, with a live scope note
## Raw request
> Bash-edit attribution via a git snapshot around Bash calls (scope, tripwires)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] After a Bash call, a file it changed outside the task's scope gets a scope note, one in scope is a touch without a note, and a file changed before the call isn't counted — verify with `python3 plugin/tests/run.py -k test_bash_touch`
- [x] Hook latency stays in budget and all gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] git status by mtime in PostToolUse(Bash)
3. [x] MASTER (edit attribution line) and CHANGELOG
## Resume here
## Docs impact
MASTER (edit attribution limits) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bash_touch` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: BashTouches 0s) / OK [ran] [tree 31389981072f] (2026-10-03T08:05:34Z)
- (step 2) `python3 plugin/tests/run.py -k test_bash_touch` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BashTouches 0s) / OK [ran] [tree 31389981072f] (2026-10-03T08:05:35Z)
- (step 3) `grep -q T-0086 MASTER.md && grep -q T-0086 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 31389981072f] (2026-10-03T08:05:35Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bash_touch` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BashTouches 0s) / OK [ran] [tree 31389981072f] (2026-10-03T08:05:40Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:05 UTC); cached (fm check --fresh reruns) [ran] [tree 31389981072f] (2026-10-03T08:05:40Z)
- (audit self) `self: the test covers an in-scope file (touch, no note), an out-of-scope one (touch + note), one changed before the call (not counted) and a repeat (no second note); PostToolUse stays at ~31 ms median in the bench (async anyway); only runs with an active task in a git checkout; .foreman/ and paths outside the project are skipped` → no findings [tree 31389981072f] (2026-10-03T08:05:40Z)
## Log
- 2026-10-02T18:35:16Z created
- 2026-10-03T08:04:07Z planned from capture
- 2026-10-03T08:04:07Z focused
- 2026-10-03T08:05:40Z done
- 2026-10-03T08:05:40Z committed 5817b9e (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research t0018-r3-operator: 3","isSidechain":true,"agentId":"a8c97e63300d81c73","message":{"model":"claude-sonnet-5","id":"msg_011CfSRu7Xczh871gZj2Mqhv","type":"message"…
- T-0136 [FIX M, done, 3 steps] Work done while a task was paused isn't its own change — lesson: When several callers read the same derived value (task_base), fix the valu…
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-02): CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; re-ground the plan against them before editing
## Lessons
- Attribution by mtime inside the call's window needs no snapshot: git status already lists every candidate, and the window rules out older edits.
## Files touched
- plugin/tests/test_bash_touch.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcore.py
