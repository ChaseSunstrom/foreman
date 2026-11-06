---
id: T-1209
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T15:09:38Z
updated: 2026-10-16T15:27:54Z
base: 6d4d43b85bc351e5f30bcfbdf87b2f84fd98ca2e
base_tree: 569f8ad2177f7d6cfda59d7e56cfc0f65ee3a768
plan0_at: 2026-10-16T15:09:39Z
plan0_scope: []
verified: ok
---
# The live demo records in true color, so the pane's charts don't turn into gray blocks
## Raw request
> The live demo records in true color, so the pane's charts don't turn into gray blocks
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a capture of Claude Code in shot.py's tmux harness carries true-color codes (38;2/48;2), not only 256-color ones, so chart wells keep their blue-gray tint against the terminal background — verify with `python3 plugin/tests/run.py -k test_the_harness_keeps_true_color`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Find which layer quantizes to 256 colors (Claude Code's color detection in the harness, or the capture) with a direct probe
2. [x] Fix the harness env or capture, with a test
3. [x] Re-record demo/live.* and the site poster, then check frames
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_the_harness_keeps_true_color` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: OneOff 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree e4ffd5f00129] (2026-10-16T15:11:26Z)
- `python3 plugin/tests/run.py -k test_the_harness_keeps_true_color` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: OneOff 0s) / OK [ran] [tree e4ffd5f00129] (2026-10-16T15:11:26Z)
- (step 1) `bash scratchpad/ccprobe.sh: Claude Code in a private tmux server, first screen captured` → COLORTERM alone: 0 true-color codes, 14 256-color; FORCE_COLOR=3 and TERM=xterm-256color/xterm-direct: same; with CLAUDE_CODE_TMUX_TRUECOLOR=1: 14 true-color, 0 256-color. Claude Code's ae(): if TMUX is set and level>2 it drops to level 2 unless CLAUDE_CODE_TMUX_TRUECOLOR [tree e4ffd5f00129] (2026-10-16T15:12:43Z)
- (step 2) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 6 tests in 0.3s (3 classes, 16 at a time; slowest: Harness 0s, Trust 0s, OneOff 0s) / OK [ran] [tree e4ffd5f00129] (2026-10-16T15:12:44Z)
- (step 3) `python3 -c "import re;t=open('demo/live.cast').read();a=len(re.findall(r'[34]8;2;',t));b=len(re.findall(r'[34]8;5;',t));print('truecolor',a,'256',b);assert a and not b"` → exit 0 · truecolor 176418 256 0 [ran] [tree 263236ccc4c2] (2026-10-16T15:26:29Z)
- (ac 1) `python3 plugin/tests/run.py -k test_the_harness_keeps_true_color` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: OneOff 0s) / OK [ran] [tree 263236ccc4c2] (2026-10-16T15:26:31Z)
- `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 6 tests in 0.3s (3 classes, 16 at a time; slowest: Harness 0s, Trust 0s, OneOff 0s) / OK [ran] [tree 263236ccc4c2] (2026-10-16T15:26:31Z)
- (audit self) `self: probe showed Claude Code's tmux downgrade (ae(): TMUX set and level>2 → level 2 unless CLAUDE_CODE_TMUX_TRUECOLOR); harness env fixed and tested; re-recorded: 176k true-color codes, 0 256-color; frames read; captions match the new session; the remaining pane patchwork (CC's #262626 pane background vs the charts' default background) captured as T-1217` → no findings [tree 263236ccc4c2] (2026-10-16T15:26:31Z)
## Log
- 2026-10-16T15:09:38Z created
- 2026-10-16T15:09:38Z focused
- 2026-10-16T15:16:20Z paused: focus moved to T-1203
- 2026-10-16T15:19:53Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T15:19:53Z focused
- 2026-10-16T15:23:47Z paused: focus moved to T-1213
- 2026-10-16T15:26:00Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T15:26:00Z focused
- 2026-10-16T15:26:30Z scope: demo/live.* re-recorded, site poster and captions, README caption and alt, MASTER demo row, CHANGELOG
- 2026-10-16T15:27:51Z done
- 2026-10-16T15:27:54Z committed 33ea5f47 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1035 [FEATURE M, done, 2 steps] Re-record the README demo video and refresh the README's pictures with the new UI (chat se — lesson: Record the demo after the UI work …
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-0998 [FEATURE S, done, 2 steps] Re-record the README demo with the remade pane
- decision 2026-10-09: Added JARVIS (<user>@<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
- similar finished tasks took 2–5 steps
## Files touched
- plugin/tests/test_shot.py
- mods/foreman-ui/tools/shot.py
- demo/live.mp4
- site/assets/poster.jpg
- README.md
- site/index.html
- MASTER.md
- CHANGELOG.md
- demo/live.cast
- demo/live.svg
