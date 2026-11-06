---
id: T-0903
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T18:05:18Z
updated: 2026-10-15T18:25:17Z
base: a3ed9382aae01c1aa63120b1c532ad9ea9a1cc24
base_tree: d99d80115296ac68e3580a6c196665bc8463fcd0
verified: strong
---
# Showcase: a recording of the real Claude Code UI with the foreman-ui mod fixing a seeded bug through Foreman
## Raw request
> Showcase demo shows the real Claude Code UI with the foreman-ui mod (band, tool rows, step bar), not just the fm demo CLI (user, 2026-10-15: 'I want the demo to show the CC ui with the mod')
## Interpretation
The user wants the showcase to show Claude Code itself with the foreman-ui mod: the band/card above the prompt, animated tool rows, the step bar, the status line, while Claude fixes a bug through Foreman. Record a real session (a cheap model, a throwaway repo and Foreman state so it starts at T-0001 and touches nothing of the user's), turn the screen captures into an inline animation for the README and a shareable MP4, with personal strings scrubbed.
## Assumptions (confidence)
## Acceptance criteria
- [x] the recording shows the mod's band and a closed task, with no personal strings — verify with `python3 -c "import json,os; ev=[json.loads(l) for l in open('demo/live.cast')][1:]; t=''.join(e[2] for e in ev); assert 'T-0001' in t and os.path.getsize('demo/live.mp4')>100000; import getpass; assert getpass.getuser() not in t and 'passmail' not in t; print('ok', len(ev), 'frames')"`
## Non-goals
## Approach (options → choice → why)
1) Drive real Claude Code in an isolated tmux (shot.py's harness, own socket), capture the coloured screen as it works, build a cast (each capture a full redraw, idle gaps squeezed) rendered to SVG with svg-term and to MP4 with shot.py's own PNG renderer + ffmpeg (chosen: real UI, no screen-grabbing of the user's desktop, reuses tested tools). 2) Screen-record a visible Konsole on the desktop with Spectacle (the user's screen, intrusive, not repeatable). 3) A pty asciinema recording of claude directly (Ink's cursor-addressed redraws are harder to replay faithfully than tmux's rendered screen). 4) Static screenshots only (no motion). Complete version: demo/record_live.py (seed repo, isolated FOREMAN_STATE, Sonnet, types the request, waits for the task's close, scrubs home/user/email), demo/live.svg in the README hero with demo.svg kept for the guard story, demo/live.mp4 to share; size checked; frames inspected before publishing.
## Risks and rollback
## Execution prompt
## Steps
1. [x] shot.py: a reusable render(raw, out)
2. [x] demo/record_live.py and one recording
3. [x] inspect frames, README hero, docs
## Resume here
## Docs impact
README hero and Development; MASTER demo/ row; CHANGELOG
## Verification evidence
- (step 1) `python3 mods/foreman-ui/tools/shot.py selftest` → exit 0 · started fmui (80x24) in . / ok: FOREMAN_* only in the harness session, never the server [ran] [tree 55ff689e05cf] (2026-10-15T18:12:20Z)
- (step 2) `python3 -c "import json,os; ev=[json.loads(l) for l in open('demo/live.cast')][1:]; t=''.join(e[2] for e in ev); assert 'T-0001' in t and os.path.getsize('demo/live.mp4')>100000; import getpass; assert getpass.getuser() not in t and 'passmail' not in t; print('ok', len(ev), 'frames')"` → exit 0 · ok 76 frames [ran] [tree 55ff689e05cf] (2026-10-15T18:12:20Z)
- (step 3) `python3 -c "import sys; t=open('README.md').read(); need=['demo/live.svg','demo/live.mp4','demo/demo.svg','record_live.py']; m=[x for x in need if x not in t]; sys.exit(print(m) or 1) if m else print('readme ok')" && fm doctor` → exit 0 · WARN  briefs               foreman-desktop-d33873: STATE.md differs from the briefs (fm tidy --apply regenerates it); foreman-improve-20260927-4cffe6: STATE.md differs from the briefs (fm tidy --apply [ran] [tree f3b34eb3f342] (2026-10-15T18:23:32Z)
- (step 2) `python3 -c "import json,os; ev=[json.loads(l) for l in open('demo/live.cast')][1:]; t=''.join(e[2] for e in ev); assert 'T-0001' in t and os.path.getsize('demo/live.mp4')>100000; import getpass; assert getpass.getuser() not in t and 'passmail' not in t and 'auto-update' not in t.lower(); print('ok', len(ev), 'frames')"` → exit 0 · ok 82 frames [ran] [tree f3b34eb3f342] (2026-10-15T18:23:32Z)
- (ac 1) `python3 -c "import json,os; ev=[json.loads(l) for l in open('demo/live.cast')][1:]; t=''.join(e[2] for e in ev); assert 'T-0001' in t and os.path.getsize('demo/live.mp4')>100000; import getpass; assert getpass.getuser() not in t and 'passmail' not in t; print('ok', len(ev), 'frames')"` → exit 0 · ok 82 frames [ran] [tree f3b34eb3f342] (2026-10-15T18:25:16Z)
- (audit intent) `self review plus frame checks: MP4 frames at 3, 14 and 27 s and an SVG still at 20 s show the real UI (Foreman card with stages, tool rows, files/fleet/queue/inbox/activity cards, status line); a squashed-video bug found and fixed (hypothesis logged, confirmed by frame heights 339 vs 890 px); the second take drops this machine's auto-update banner; cast scanned for the user name, home path and account e-mail: none` → the user wanted the demo to show Claude Code's UI with the mod: the README hero is now Claude Code + foreman-ui fixing a bug through Foreman (one typed request; Foreman refuses the close until red→green is proved, Claude proves it, closes and commits), with the CLI demo kept below as the no-model try-it-yourself; demo/live.mp4 is the shareable video [tree f3b34eb3f342] (2026-10-15T18:25:16Z)
- (audit operator) `self review plus frame checks: MP4 frames at 3, 14 and 27 s and an SVG still at 20 s show the real UI (Foreman card with stages, tool rows, files/fleet/queue/inbox/activity cards, status line); a squashed-video bug found and fixed (hypothesis logged, confirmed by frame heights 339 vs 890 px); the second take drops this machine's auto-update banner; cast scanned for the user name, home path and account e-mail: none` → record_live.py costs one Sonnet turn (about $0.15 here), runs in its own tmux server with an isolated FOREMAN_STATE under /tmp and none of this session's CLAUDE_*/FOREMAN_* variables; --from-cast re-renders without a new session; the trust dialog's default is 'No, exit', so it selects Yes first [tree f3b34eb3f342] (2026-10-15T18:25:16Z)
- (audit adversary) `self review plus frame checks: MP4 frames at 3, 14 and 27 s and an SVG still at 20 s show the real UI (Foreman card with stages, tool rows, files/fleet/queue/inbox/activity cards, status line); a squashed-video bug found and fixed (hypothesis logged, confirmed by frame heights 339 vs 890 px); the second take drops this machine's auto-update banner; cast scanned for the user name, home path and account e-mail: none` → a published recording could leak who recorded it: the home path, user and real name and the account's e-mail/display names are replaced in every capture before anything is written (whole words only), and the cast was scanned after; the harness no longer hands this session's messaging socket or session id to the recorded Claude Code [tree f3b34eb3f342] (2026-10-15T18:25:16Z)
## Log
- 2026-10-15T18:05:18Z created
- 2026-10-15T18:07:08Z planned from capture
- 2026-10-15T18:07:09Z focused
- 2026-10-15T18:11:40Z hypothesis: live.mp4 frames look squashed because render() sizes each PNG by its own row count (capture-pane drops trailing blank lines), and ffmpeg scales every frame to the first one's smaller size; test: render the cast's first and a middle screen without rows= and compare heights
- 2026-10-15T18:11:44Z confirmed: frame 0 renders 17 rows (1546x339), frame 40 46 rows (1546x890); rows=46 makes both 1546x890
- 2026-10-15T18:25:16Z done
- 2026-10-15T18:25:17Z committed c83c73e (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0902 [FEATURE M, done, 4 steps] Showcase: a recorded demo of Foreman at work in the README, and a README that reads well — lesson: Showcase with the deterministic path…
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Lessons
- Record the product's real UI from a harness that owns its terminal (tmux capture-pane), not a screen grab: frames are exact text, scrubbable before they're written, and re-renderable from the cast without paying for another session
## Files touched
- mods/foreman-ui/tools/shot.py
- demo/record_live.py
- demo/live.mp4
- README.md
- CHANGELOG.md
- MASTER.md
- demo/live.cast
- demo/live.svg
