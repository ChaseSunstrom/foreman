---
id: T-0138
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T05:42:50Z
updated: 2026-10-03T05:50:03Z
base: 045fc4ac4a131151515e787092751bba8121ac89
base_tree: ba1ff95fa85e59f3bf32eec40624673ef5978d78
verified: ok
---
# Drive survives a restart: a resumed session with drive on, full autonomy and open work starts its own first turn
## Raw request
> continue, you weren't reprompted when the session just continued: after claude --continue/--resume with drive on and open work, Foreman should restart the turn itself (SessionStart initialUserMessage)
## Interpretation
User: after claude --continue nothing happened until they typed continue. With drive on and full autonomy the work should pick up by itself.
## Assumptions (confidence)
## Acceptance criteria
- [x] resume + drive + full + open work gives an initial message; startup, standard autonomy, drive off or no work give none — verify with `python3 plugin/tests/run.py -p test_hooks.py -k SessionStart`
## Non-goals
## Approach (options → choice → why)
Options: (a) SessionStart with source resume returns hookSpecificOutput.initialUserMessage ('Continue the Foreman drive: <next>') when drive is on, autonomy full, not paused, not a headless fm run, and there is open work; (b) also on startup. Choice (a): a resume is the user's 'carry on'; a fresh start may be for something else, so it waits for them.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests, initialUserMessage on resume
2. [x] live check: claude --continue in the harness starts a turn
## Resume here
<!-- auto -->
- 2026-10-03T05:44:35Z step 1/2: tests, initialUserMessage on resume
- git: foreman/build; 1 uncommitted: plugin/tests/test_hooks.py
- touched since last checkpoint: plugin/tests/test_hooks.py
## Docs impact
CHANGELOG entry; rules/README unchanged (drive behaviour, no new command)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k SessionStart` → OK; red first (initialUserMessage missing), green after (2026-10-03T05:47:17Z)
- (step 2) `plugin/hooks/hook SessionStart on a demo project (full autonomy, active task): resume and startup payloads` → resume -> 'Continue the Foreman drive: T-0001 — Demo work'; startup -> None. Engine contract: claude-code.d.ts lists initialUserMessage for SessionStart. A live claude --continue was skipped: in full autonomy it starts a paid driven run (2026-10-03T05:47:40Z)
- (ac 1) `python3 plugin/tests/run.py -p test_hooks.py -k SessionStart` → exit 0 · Ran 10 tests in 5.8s (1 classes, 16 at a time; slowest: SessionStart 6s) / OK [ran] [tree 87a59a1e9a97] (2026-10-03T05:49:58Z)
- (audit operator) `intent: 'continue, you weren't reprompted when the session just continued' — a resumed session now gets its own first turn (real hook entry point checked on a demo project: resume gives the message, startup none); scope fmhooks.session_start + one test + changelog` → two sessions resuming one project would both drive; found and fixed test-first (another session active <15 min → no auto-turn). fm run (FOREMAN_DRIVE_TASK), paused, drive off, standard autonomy and waiting-only work all start none; the person can still interrupt with Esc [tree 87a59a1e9a97] (2026-10-03T05:49:58Z)
- (audit intent) `self-review of the diff and tests` → 'continue, you weren't reprompted when the session just continued' — a resumed session now gets its own first turn (real hook entry point on a demo project: resume gives the message, startup none); scope fmhooks.session_start + one test + changelog [tree 87a59a1e9a97] (2026-10-03T05:50:03Z)
- (audit operator) `self-review of the diff and tests` → two sessions resuming one project would both drive; found and fixed test-first (another session active <15 min → no auto-turn). fm run, paused, drive off, standard autonomy and waiting-only work start none; Esc still interrupts [tree 87a59a1e9a97] (2026-10-03T05:50:03Z)
## Log
- 2026-10-03T05:42:50Z created
- 2026-10-03T05:44:28Z planned from capture
- 2026-10-03T05:44:29Z focused
- 2026-10-03T05:46:20Z steer: keep screenshotting the live UI while working (Spectacle on the user's window), not only at the end
- 2026-10-03T05:50:03Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- T-0116 [FEATURE M, done, 4 steps] Size words with meaning: typical time per type and size, time on task, gate ETA — lesson: Medians need a floor on samples; with fewer t…
- T-0014 [FEATURE L, done, 4 steps] Headless remote forever mode: fm serve runs Claude Code Remote Control in a repo in the background; fm run works the queue in fresh ses…
- T-0115 [FIX M, done, 3 steps] Drive trusts the Stop hook's background_tasks list over its event scan — lesson: Prefer the engine's authoritative payload fields over reco…
## Lessons
- Check what Claude Code already offers before building: SessionStart initialUserMessage gave restart-survival in 15 lines
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
