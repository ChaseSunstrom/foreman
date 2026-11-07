---
id: T-1001
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbus.py, plugin/hooks/statusline, plugin/tests/test_bus.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T00:17:08Z
updated: 2026-10-16T00:19:39Z
base: 880fac15923377bd1535f0f8015c3ed9aad6bfae
base_tree: b1b0ce6f8ca7e133f2ec09a42c307afc19103538
verified: strong
---
# Fleet lists ended and one-off sessions (dead UI-harness sessions show as '?%' rows in the
## Raw request
> Fleet lists ended and one-off sessions (dead UI-harness sessions show as '?%' rows in the pane and crowd out the More lines): drop sessions that ended or went silent, and never list FOREMAN_ONEOFF ones
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a session whose recorded claude process is gone drops out of the fleet at once; a one-off session (FOREMAN_ONEOFF=1) writes no snapshot — verify with `python3 plugin/tests/run.py -k Conductor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing Conductor test
2. [x] live() drops dead sessions; statusline skips one-offs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k Conductor` → ✗ exit 1 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Conductor 1s) / FAILED (1 classes) [ran] [tree 41887942337b] (2026-10-16T00:18:48Z)
- (step 2) `python3 plugin/tests/run.py -k Conductor` → ✗ exit 1 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Conductor 1s) / FAILED (1 classes) [ran] [tree c45a74c1fa87] (2026-10-16T00:18:59Z)
- (step 2) `python3 plugin/tests/run.py -k Conductor` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Conductor 1s) / OK [ran] [tree d975c629f35b] (2026-10-16T00:19:16Z)
- `python3 plugin/tests/run.py -k Conductor` → ✗ exit 1 · Ran 2 tests in 1.9s (1 classes, 16 at a time; slowest: Conductor 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d975c629f35b] (2026-10-16T00:19:24Z)
- `python3 plugin/tests/run.py -k Conductor` → exit 0 · Ran 2 tests in 1.5s (1 classes, 16 at a time; slowest: Conductor 1s) / OK [ran] [tree d975c629f35b] (2026-10-16T00:19:24Z)
- (ac 1) `python3 plugin/tests/run.py -k Conductor` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Conductor 1s) / OK [ran] [tree ac3634d2ba78] (2026-10-16T00:19:38Z)
- (audit edge) `self: live() now drops sessions whose every recorded pid is gone or reused (start time differs); sessions with no pid record (older, or another machine's) keep the 15-minute rule; the statusline writes no snapshot for FOREMAN_ONEOFF=1; proved red on the start tree` → a session with one live and one dead recorded pid stays (any alive counts); a reused pid with a different start time counts as gone [tree ac3634d2ba78] (2026-10-16T00:19:38Z)
- (audit self) `self: live() now drops sessions whose every recorded pid is gone or reused (start time differs); sessions with no pid record (older, or another machine's) keep the 15-minute rule; the statusline writes no snapshot for FOREMAN_ONEOFF=1; proved red on the start tree` → no findings [tree ac3634d2ba78] (2026-10-16T00:19:38Z)
## Log
- 2026-10-16T00:17:08Z created
- 2026-10-16T00:18:20Z set scope=['plugin/lib/fmbus.py', 'plugin/hooks/statusline', 'plugin/tests/test_bus.py', 'CHANGELOG.md']
- 2026-10-16T00:18:20Z focused
- 2026-10-16T00:19:39Z done
- 2026-10-16T00:19:39Z committed 0ed7835 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0777 [FEATURE M, done, 3 steps] Never idle without tmux: a plugin monitor streams this session's Foreman mail, and fm bus --wake prefers it over typing into tmux — les…
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-09: Added JARVIS (<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
- likely tests for the scope: plugin/tests/test_bus.py
## Plan gaps
- failed first: step 1 failing Conductor test
- failed first: step 2 live() drops dead sessions; statusline skips one-offs
## Files touched
- plugin/tests/test_bus.py
- plugin/hooks/statusline
- plugin/lib/fmbus.py
- CHANGELOG.md
