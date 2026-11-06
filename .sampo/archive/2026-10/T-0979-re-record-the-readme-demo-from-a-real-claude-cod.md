---
id: T-0979
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T22:20:26Z
updated: 2026-10-15T22:46:42Z
base: 70e4b37be070ccc08d25aa015d1c00261770506e
base_tree: f3abbe26ccd947dc091a84389c19c56c19790c0a
verified: strong
---
# Re-record the README demo from a real Claude Code session with the current pane: record_li
## Raw request
> Re-record the README demo from a real Claude Code session with the current pane: record_live.py gains --repo/--request to record a session working a small real Foreman task in a scratch clone of this repo (scrubbed); replace live.svg/live.mp4 if it reads well
## Interpretation
The README's live demo shows an older pane on a seeded calc bug. Record a fresh one with the current Claude Code (2.1.301) and mod: Claude working a real, small Foreman task in a scratch clone of this repo, scrubbed of names and paths, and replace live.svg/live.mp4 if it reads well.
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 demo/record_live.py --repo . --request '…' --dry prints the clone, the request and the claude it will run, and changes nothing — verify with `python3 demo/record_live.py --repo . --request 'FIX: x' --dry`
- [x] demo/live.cast and live.svg come from a session on a real Foreman task in a clone, scrubbed (no home path, user or account e-mail in them) — verify with `! grep -q -i -e chase -e passmail demo/live.cast`
## Non-goals
## Approach (options → choice → why)
Options: record_live.py gains --repo (a local clone into the scratch folder) and --request, recording a session on a real queued task (chosen: real work, same scrubbing and rendering, the recorder stays one script); screen-record the user's own terminal (captures their whole screen and this conversation, can't be scrubbed); re-run the seeded calc demo (current pane, but not real work).
## Risks and rollback
## Execution prompt
## Steps
1. [x] --repo/--request/--dry in record_live.py
2. [x] Record, check frames, swap the README asset and caption if it reads well
## Resume here
<!-- auto -->
- 2026-10-15T22:31:57Z step 2/2: Record, check frames, swap the README asset and caption if it reads well
- git: foreman/build; 1 uncommitted: demo/record_live.py
- touched since last checkpoint: demo/record_live.py
## Docs impact
README, CHANGELOG
## Verification evidence
- (step 1) `python3 demo/record_live.py --repo . --request 'FIX: x' --dry` → exit 0 · request: FIX: x / claude: 2.1.299 (Claude Code) · model sonnet · up to 600 s [ran] [tree 300fa0527f5d] (2026-10-15T22:27:06Z)
- (step 2) `! grep -q -i -e chase -e passmail -e sunstrom demo/live.cast && python3 demo/record_live.py --repo . --request 'FIX: x' --dry` → ✗ exit 1 · raise child_exception_type(errno_num, err_msg, err_filename) / FileNotFoundError: [Errno 2] No such file or directory: 'claude' [ran] [tree 837959f8270f] (2026-10-15T22:46:25Z)
- (step 2) `! grep -q -i -e chase -e passmail -e sunstrom demo/live.cast && python3 demo/record_live.py --repo . --request 'FIX: x' --dry` → exit 0 · request: FIX: x / claude: not on PATH · model sonnet · up to 600 s [ran] [tree 907ad5336e9e] (2026-10-15T22:46:31Z)
- (ac 1) `python3 demo/record_live.py --repo . --request 'FIX: x' --dry` → exit 0 · request: FIX: x / claude: not on PATH · model sonnet · up to 600 s [ran] [tree 8478f786db97] (2026-10-15T22:46:38Z)
- (ac 2) `! grep -q -i -e chase -e passmail demo/live.cast` → exit 0 · (no output) [ran] [tree 8478f786db97] (2026-10-15T22:46:38Z)
- (audit intent) `self: three rendered frames checked by eye (pane, plan, Skills card, pulse charts, the close and commit); cast grepped for names and e-mails; dry run works` → the README demo now shows a real session on a real Foreman task with the current UI [tree 8478f786db97] (2026-10-15T22:46:38Z)
- (audit adversary) `self: three rendered frames checked by eye (pane, plan, Skills card, pulse charts, the close and commit); cast grepped for names and e-mails; dry run works` → the user's names, account and git e-mails and home path are scrubbed before anything is written; the clone has no remote; the user's terminal is never recorded [tree 8478f786db97] (2026-10-15T22:46:38Z)
- (audit operator) `self: three rendered frames checked by eye (pane, plan, Skills card, pulse charts, the close and commit); cast grepped for names and e-mails; dry run works` → --max-frames keeps the SVG near 3 MB for GitHub; --dry says what would run [tree 8478f786db97] (2026-10-15T22:46:38Z)
## Log
- 2026-10-15T22:20:26Z created
- 2026-10-15T22:26:47Z focused
- 2026-10-15T22:27:33Z paused: focus moved to T-0981
- 2026-10-15T22:31:36Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T22:31:36Z focused
- 2026-10-15T22:31:58Z paused: focus moved to T-0984
- 2026-10-15T22:44:24Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T22:44:24Z focused
- 2026-10-15T22:46:40Z done
- 2026-10-15T22:46:42Z committed 3fe7abd (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0903 [FEATURE M, done, 3 steps] Showcase: a recording of the real Claude Code UI with the foreman-ui mod fixing a seeded bug through Foreman — lesson: Record the produ…
- T-0902 [FEATURE M, done, 4 steps] Showcase: a recorded demo of Foreman at work in the README, and a README that reads well — lesson: Showcase with the deterministic path…
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
## Lessons
- A recorder that waits for T-0001 misses a session that drops and redoes its first brief: watch for any task closing
## Plan gaps
- failed first: step 2 Record, check frames, swap the README asset and caption if it reads well
## Files touched
- demo/record_live.py
- demo/live.cast
- demo/live.mp4
- demo/live.svg
- README.md
- CHANGELOG.md
