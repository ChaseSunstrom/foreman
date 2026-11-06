---
id: T-1013
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T01:23:47Z
updated: 2026-10-16T01:24:16Z
base: faa7b2bed1c4d2dc067adf7d9940b43c3a56d890
base_tree: 887bcb6f3a0c538f4ec3768903c4406ddad2328f
verified: strong
---
# shot.py: a harness session with its own FOREMAN_STATE is a working session, not a one-off
## Raw request
> shot.py: a harness session with its own FOREMAN_STATE is a working session, not a one-off
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] shot.start sets FOREMAN_ONEOFF=1 only without FOREMAN_STATE; with it, the session gets FOREMAN_STATE and no FOREMAN_ONEOFF — verify with `python3 plugin/tests/run.py test_shot`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: shot.start's tmux env with and without FOREMAN_STATE
2. [x] shot.start: one-off only when sharing the real state
3. [x] docs: CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_shot` → ✗ exit 1 · Ran 3 tests in 0.2s (2 classes, 16 at a time; slowest: Harness 0s, OneOff 0s) / FAILED (1 classes) [ran] [tree cf50a84201a4] (2026-10-16T01:23:58Z)
- (step 2) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 3 tests in 0.2s (2 classes, 16 at a time; slowest: Harness 0s, OneOff 0s) / OK [ran] [tree 80332ababd56] (2026-10-16T01:24:04Z)
- (step 3) `grep -q 'T-1013' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 63e4952f1cb9] (2026-10-16T01:24:14Z)
- (ac 1) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 3 tests in 0.2s (2 classes, 16 at a time; slowest: Harness 0s, OneOff 0s) / OK [ran] [tree 63e4952f1cb9] (2026-10-16T01:24:14Z)
- (audit edge) `self` → isolated state: FOREMAN_STATE passed, no one-off; user's state: one-off as T-0995 wanted; the selftest still proves no FOREMAN_* leaks into the tmux server [tree 63e4952f1cb9] (2026-10-16T01:24:14Z)
- (ac 1) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 3 tests in 0.2s (2 classes, 16 at a time; slowest: Harness 0s, OneOff 0s) / OK [ran] [tree 63e4952f1cb9] (2026-10-16T01:24:15Z)
- (audit edge) `unit test on shot.start's tmux env both ways; red→green` → the harness on the user's state stays a one-off (T-0995) [tree 63e4952f1cb9] (2026-10-16T01:24:15Z)
- (audit self) `unit test on shot.start's tmux env both ways; red→green` → no findings [tree 63e4952f1cb9] (2026-10-16T01:24:15Z)
## Log
- 2026-10-16T01:23:47Z created
- 2026-10-16T01:23:47Z focused
- 2026-10-16T01:24:15Z done
- 2026-10-16T01:24:16Z committed 049461f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1004 [FIX S, done, 3 steps] A one-off session records no evidence on another session's task
- T-0996 [FEATURE S, dropped, 0 steps] Catch it earlier: the harness had only been used with local commands (/fm) or single promp
- T-0995 [FIX S, done, 2 steps] The UI harness's interactive session (shot.py) was driven by the Stop hook into the queue: it planned three tasks and took focus from the w…
- decision 2026-09-26: T-0014 fm run: minimal one-shot worker (fresh claude -p per task, drive scoped to that task via FOREMAN_DRIVE_TASK, per-task timeout, stop on no pro…
- similar finished tasks took 2–3 steps
## Why not caught
T-0995 changed the harness for the screenshot use and no test covered the recorder's isolated-state use
## Plan gaps
- failed first: step 1 red test: shot.start's tmux env with and without FOREMAN_STATE
## Files touched
- plugin/tests/test_shot.py
- mods/foreman-ui/tools/shot.py
- CHANGELOG.md
