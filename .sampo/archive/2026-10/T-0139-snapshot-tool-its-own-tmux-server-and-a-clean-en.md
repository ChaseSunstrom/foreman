---
id: T-0139
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T05:42:50Z
updated: 2026-10-03T05:44:04Z
base: 97f860d33ae5f97933d3ab51dbe651e6045b24c4
base_tree: 2c43a8cd3f24c2b57fa4f4ad606c3e5ec1d124fa
verified: ok
---
# Snapshot tool: its own tmux server and a clean environment, so FOREMAN_STATE can't leak into the user's tmux
## Raw request
> Snapshot tool: its own tmux server and a clean environment, so FOREMAN_STATE can't leak into the user's tmux
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the harness runs on its own tmux socket and its server env carries no FOREMAN_* — verify with `python3 mods/foreman-ui/tools/shot.py selftest`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] own socket (-L), env without FOREMAN_* for the server, -e only for the session; selftest
## Resume here
## Docs impact
none: the harness docstring says it
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_shot.py` → ✗ exit 1 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Harness 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ba1ff95fa85e] (2026-10-03T05:43:16Z)
- (step 1) `python3 plugin/tests/run.py -p test_shot.py` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Harness 0s) / OK [ran] [tree ba1ff95fa85e] (2026-10-03T05:43:16Z)
- (ac 1) `python3 mods/foreman-ui/tools/shot.py selftest` → exit 0 · started fmui (80x24) in . / ok: FOREMAN_* only in the harness session, never the server [ran] [tree ba1ff95fa85e] (2026-10-03T05:43:24Z)
- (step 1) `python3 plugin/tests/run.py -p test_shot.py` → red on the old harness, green now (2026-10-03T05:43:24Z)
- (ac 1) `python3 mods/foreman-ui/tools/shot.py selftest` → exit 0 · started fmui (80x24) in . / ok: FOREMAN_* only in the harness session, never the server [ran] [tree ba1ff95fa85e] (2026-10-03T05:44:04Z)
- (audit adversary) `self: harness server started from an environment without FOREMAN_*; the session alone gets FOREMAN_STATE (-e); own socket, so the user's tmux is never touched; selftest checks both` → the leaked variables also included a stale FOREMAN_SESSION_ID that would have mis-attributed ledger events; both cleaned from the user's tmux global env by hand, and the harness can no longer write there [tree ba1ff95fa85e] (2026-10-03T05:44:04Z)
- (audit self) `self: harness server started from an environment without FOREMAN_*; the session alone gets FOREMAN_STATE (-e); own socket, so the user's tmux is never touched; selftest checks both` → no findings [tree ba1ff95fa85e] (2026-10-03T05:44:04Z)
## Log
- 2026-10-03T05:42:50Z created
- 2026-10-03T05:42:51Z focused
- 2026-10-03T05:44:04Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- T-0131 [FEATURE M, done, 3 steps] See the rendered UI: a tmux + PNG snapshot tool for foreman-ui, and a first review — lesson: Look at the real render before polishing: …
- research T-0120-review: Verdict
- decision 2026-09-26: T-0014 supervisor: systemd user unit only (no tmux-only fallback); the unit runs tmux on a private socket (foreman-<slug>) for the TTY Remote Contro…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- start here (files T-0131 touched): mods/foreman-ui/tools/shot.py
## Lessons
- A helper that starts a long-lived server (tmux) hands it the caller's whole environment: start it from a clean one
## Files touched
- mods/foreman-ui/tools/shot.py
- plugin/tests/test_shot.py
