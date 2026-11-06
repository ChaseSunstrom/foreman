---
id: T-0164
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_bash_touch.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T08:14:17Z
updated: 2026-10-03T08:17:48Z
base: 622d5265ce7f05ac73afac393144fee132adf7ab
base_tree: a694a211304336ecdc00318191dad5cb0edd55ed
verified: strong
---
# A Bash touch is timed by the file's mtime, so a scope reason logged in the same command covers it
## Raw request
> Scope refusal: a logged 'scope: <why>' only counts when it names the file, but the message doesn't say so (T-0087 needed a second log); say 'scope: <file> — <why>' or accept a reason logged after the edit
## Interpretation
Root cause (not the message): T-0086's async PostToolUse hook logs a Bash-changed file's touch when the hook runs, after the whole command, so a 'scope:' reason that command logged reads as older than the edit and the finish is refused.
## Assumptions (confidence)
## Acceptance criteria
- [x] A scope reason logged in the same command as the edit covers it at finish — verify with `python3 plugin/tests/run.py -k test_bash_touch`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test
2. [x] Record the file's mtime with the touch and prefer it in task_touches
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bash_touch` → ✗ exit 1 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: BashTouches 2s) / FAILED (1 classes) [ran] [tree 3356abc734a1] (2026-10-03T08:16:41Z)
- (step 2) `python3 plugin/tests/run.py -k test_bash_touch` → exit 0 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: BashTouches 2s) / OK [ran] [tree 6f77b689cef7] (2026-10-03T08:16:50Z)
- (step 3) `grep -q T-0164 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 29fdc5ba7500] (2026-10-03T08:17:38Z)
- (step 1) `python3 plugin/tests/run.py -k test_bash_touch` → exit 0 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: BashTouches 2s) / OK [ran] [tree 29fdc5ba7500] (2026-10-03T08:17:46Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bash_touch` → exit 0 · Ran 2 tests in 1.6s (1 classes, 16 at a time; slowest: BashTouches 2s) / OK [ran] [tree 29fdc5ba7500] (2026-10-03T08:17:48Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:17 UTC); cached (fm check --fresh reruns) [ran] [tree 29fdc5ba7500] (2026-10-03T08:17:48Z)
- (audit self) `self: red→green on the same test command (the touch logged after the reason, then timed by mtime); Edit/Write touches keep their event time (no 'at'); older ledger lines without 'at' read as before` → no findings [tree 29fdc5ba7500] (2026-10-03T08:17:48Z)
## Log
- 2026-10-03T08:14:17Z created
- 2026-10-03T08:16:35Z planned from capture
- 2026-10-03T08:16:35Z focused
- 2026-10-03T08:17:48Z done
- 2026-10-03T08:17:48Z committed 17ed9d1 (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0086 [FEATURE S, done, 3 steps] Bash-edit attribution: files a Bash command changed count as the task's touches, with a live scope note — lesson: Attribution by mtime …
- research t0071-fg-review: Each piece does what it claims end-to-end (verified by reading each call site): the mtime union in `fm task done` (fmcli.py:219-226), `--fail-f…
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW.
- research t0071-de-review: MEDIUM — `plugin/lib/fmcost.py:546` — `cmd_usage`'s Next-follow regex `\bfm [a-z-]+(?: (?:prep|step|done|new|evidence|ac|audit|finish|prove))?`…
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Lessons
- An async hook's own clock is the wrong timestamp for what it observed: record when the thing happened (the file's mtime), not when the hook ran.
## Files touched
- plugin/tests/test_bash_touch.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcore.py
- CHANGELOG.md
