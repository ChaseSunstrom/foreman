---
id: T-0915
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T19:21:17Z
updated: 2026-10-15T19:24:51Z
base: b6e32590e051558beda54340d4255ad656827266
base_tree: 78a06cab5156da0050db23356bcfa25fdecfb821
verified: ok
---
# Re-record the README live demo with the redesigned pane
## Raw request
> Re-record the README live demo with the redesigned pane
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] demo/live.cast, live.svg and live.mp4 are re-recorded and free of personal strings — verify with `grep -ciE 'chase|passmail|/home/' demo/live.cast demo/live.svg | grep -q ':0' && test -s demo/live.mp4`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] python3 demo/record_live.py; check the frames; scan for personal strings
## Resume here
<!-- auto -->
- 2026-10-15T19:22:31Z step 1/1: python3 demo/record_live.py; check the frames; scan for personal strings
- git: foreman/build; 3 uncommitted: demo/live.cast, demo/live.mp4, demo/live.svg
- touched since last checkpoint: demo/live.mp4
## Docs impact
## Verification evidence
- (step 1) `test -s demo/live.mp4 && grep -c 'T-0001 done' demo/live.cast` → exit 0 · 19 [ran] [tree 7baa257ed696] (2026-10-15T19:24:44Z)
- (ac 1) `grep -ciE 'chase|passmail|/home/' demo/live.cast demo/live.svg | grep -q ':0' && test -s demo/live.mp4` → exit 0 · (no output) [ran] [tree 7baa257ed696] (2026-10-15T19:24:44Z)
- (audit self) `self: two takes (the first showed the audits row wrapping at 70 columns, fixed in T-0916); frames at 12 s, 16.8 s and 27 s checked by eye: rail with comet, Now, Plan, Pulse lanes, the done card with sweep, grade and proof; personal strings: 0 in cast and svg` → no findings [tree 7baa257ed696] (2026-10-15T19:24:44Z)
- `grep -ciE 'chase|passmail|/home/' demo/live.cast demo/live.svg | grep -q ':0' && test -s demo/live.mp4` → exit 0 · (no output) [ran] [tree 7baa257ed696] (2026-10-15T19:24:49Z)
- (audit self) `self: two takes (the first showed the audits row wrapping at 70 columns, fixed in T-0916); frames at 12 s, 16.8 s and 27 s checked by eye: rail with comet, Now, Plan, Pulse lanes, the done card with sweep, grade and proof; personal strings: 0 in cast and svg` → no findings [tree 7baa257ed696] (2026-10-15T19:24:49Z)
## Log
- 2026-10-15T19:21:17Z created
- 2026-10-15T19:21:18Z focused
- 2026-10-15T19:22:32Z paused: focus moved to T-0916
- 2026-10-15T19:23:31Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T19:23:31Z focused
- 2026-10-15T19:23:55Z scope: README's pane description rewritten to match the redesign (T-0909, T-0912..T-0914) alongside the new recording
- 2026-10-15T19:24:50Z done
- 2026-10-15T19:24:51Z committed bc99c72 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0902 [FEATURE M, done, 4 steps] Showcase: a recorded demo of Foreman at work in the README, and a README that reads well — lesson: Showcase with the deterministic path…
- T-0903 [FEATURE M, done, 3 steps] Showcase: a recording of the real Claude Code UI with the foreman-ui mod fixing a seeded bug through Foreman — lesson: Record the produ…
- T-0909 [FEATURE L, done, 6 steps] Can you super improve the UI, better animations/visuals for graphs/tasks things going on? — lesson: In the mod test harness a Text elem…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Behaviour lock
none: no code changed; recordings and README prose only
## Files touched
- demo/live.mp4
- README.md
- demo/live.cast
- demo/live.svg
