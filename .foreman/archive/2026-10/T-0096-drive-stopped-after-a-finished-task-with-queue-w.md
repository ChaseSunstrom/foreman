---
id: T-0096
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-02T20:09:43Z
updated: 2026-10-02T20:25:58Z
base: 9beae1a127c961267a4f30b99def4ecb113114cc
verified: ok
---
# Drive resumes when background work finished mid-turn
## Raw request
> FIX!: drive stopped after a finished task with queue work left: a 5-day Volt session ended its turn on 'Next: back to the queue, starting with T-0176' and didn't continue
> CONTEXT: user report from a long-running Volt session; Foreman should keep driving the queue unattended
## Interpretation
Volt (full autonomy, drive on, M task queued) stopped after T-0187: drive saw 5 background commands as still running because their completion notices arrived inside running turns (never via UserPromptSubmit), and the 6 h stale window kept drive silent.
## Assumptions (confidence)
## Acceptance criteria
- [x] a completion notice that arrived mid-turn, a stopped task and a >2 h stale start no longer hold drive — verify with `python3 -m unittest discover -s plugin/tests -p test_hooks.py -q`
## Non-goals
## Approach (options → choice → why)
Options: (a) at Stop, scan the transcript's new bytes for task-notification ids (incremental offset in gate.json), record TaskStop/KillShell as done, cut the stale window to 2 h, and log why drive declined; (b) drop the background wait entirely. Choice: (a). Why: keeps the no-busywork rule for genuinely running work while every finished one is seen; the window is only a backstop.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests
2. [x] transcript scan + TaskStop + 2 h backstop + drive_idle reason
3. [x] docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_hooks.py -q` → ✗ exit 1 · Ran 108 tests in 46.491s / FAILED (failures=3) (start tree + this task's tests) [ran] [tree a0407435034a] (2026-10-02T20:24:35Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_hooks.py -q` → exit 0 · Ran 108 tests in 46.347s / OK [ran] [tree a0407435034a] (2026-10-02T20:24:35Z)
- (step 2) `python3 plugin/tests/bench_hooks.py --runs 20` → Stop                        32.5    35.3     150  [0] (2026-10-02T20:24:45Z)
- (step 1) `fm task prove` → start tree 3 failures, current tree 108 OK (2026-10-02T20:25:02Z)
- (step 3) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree d57ccb8489f4] (2026-10-02T20:25:02Z)
- (ac 1) `python3 -m unittest discover -s plugin/tests -p test_hooks.py -q` → exit 0 · Ran 108 tests in 46.650s / OK [ran] [tree d57ccb8489f4] (2026-10-02T20:25:58Z)
- (audit intent) `checked against the Volt ledger: full autonomy, drive on, T-0176 queued, 5 unmatched bg_start ids (newest 16:57) held drive at 19:51; all three paths now free it` → pass: the reported stop is explained and fixed [tree d57ccb8489f4] (2026-10-02T20:25:58Z)
- (audit edge) `transcript scan: offset per session, reset when the file shrinks, 8 MB per Stop cap, ids only from <task-id> tags (the start message has none); TaskStop/KillShell ids; 2 h backstop; Stop p95 36 ms` → pass: a stray tag in text could free drive early, which only means a continuation, never a lost wait on the user [tree d57ccb8489f4] (2026-10-02T20:25:58Z)
## Log
- 2026-10-02T20:09:43Z created
- 2026-10-02T20:21:13Z planned from capture
- 2026-10-02T20:21:13Z focused
- 2026-10-02T20:21:48Z user approved core in Claude Code's permission prompt
- 2026-10-02T20:25:58Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0014 [FEATURE L, done, 4 steps] Headless remote forever mode: fm serve runs Claude Code Remote Control in a repo in the background; fm run works the queue in fresh ses…
- playbook Strategic Compact Skill (skills/playbooks/references/context/strategic-compact.md)
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- research brainstorm-20260926-super-slate: Built under T-0071, in rounds (inbox items folded in):
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
## Lessons
- A wait that depends on an event the hook might never see needs a second signal (transcript) and a short backstop; log every decline so a silent stop can be explained.
## Files touched
- CHANGELOG.md
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
