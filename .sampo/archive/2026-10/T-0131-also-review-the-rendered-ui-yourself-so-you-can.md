---
id: T-0131
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-03T04:52:05Z
updated: 2026-10-03T04:59:16Z
base: d2c72db749a4704ae4ae8bbe6fcdfbeb5fde876a
base_tree: e59372c81b3851e0a68bd0052f46cff74d10b88d
verified: weak
---
# See the rendered UI: a tmux + PNG snapshot tool for foreman-ui, and a first review
## Raw request
> also review the rendered UI yourself so you can improve/animate it better, etc.
## Interpretation
User: review the rendered UI yourself so you can improve and animate it better. Tests only see element trees; I need the real terminal rendering, colors included, to judge it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a PNG of the band and the pane from the live engine — verify with `python3 mods/foreman-ui/tools/shot.py snap /tmp/fm-ui.png`
## Non-goals
## Approach (options → choice → why)
Options: (a) run Claude Code in a detached tmux window (200x60) with the dev mod (--plugin-dir) in a demo Foreman project, capture-pane -e (24-bit ANSI), and draw the cells to a PNG with PIL that I can view; (b) write my own renderer for the test trees. Choice (a): it is the engine's real layout, Raster and focus included; (b) would approximate Ink and miss exactly the things that look wrong. Iterate with /reload-plugins sent through tmux (local, no model call).
## Risks and rollback
## Execution prompt
## Steps
1. [x] shot.py: start/keys/snap/stop + ANSI→PNG
2. [x] demo project with a varied queue
3. [x] first review: findings into T-0122
## Resume here
## Docs impact
none: dev tool, documented in its docstring
## Verification evidence
- (step 1) `python3 mods/foreman-ui/tools/shot.py snap shot3.png` → PNG of the live band and pane, OSC stripped, symbol fallback fonts (2026-10-03T04:59:10Z)
- (step 2) `fm state (FOREMAN_STATE=scratchpad/uistate)` → uidemo: active FEATURE 2/4, 3 queued incl. an L plan, 3 inbox (2026-10-03T04:59:10Z)
- (step 3) `fm task log T-0122` → 9 findings recorded (2026-10-03T04:59:11Z)
- (ac 1) `python3 mods/foreman-ui/tools/shot.py snap /tmp/claude-1000/-home-~--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/shot3.png` → 60-row PNG of the live engine's band and pane (2026-10-03T04:59:16Z)
- (audit intent) `self: dev tool outside the mod's hooks (not loaded by the engine); tmux session name fixed; sends only local commands` → I can now see the real rendering, colours and layout included, and found 9 concrete problems tests could not show [tree 4b216dc9ba1c] (2026-10-03T04:59:16Z)
- (audit edge) `self: dev tool outside the mod's hooks (not loaded by the engine); tmux session name fixed; sends only local commands` → OSC hyperlinks stripped; wide chars advance 2; missing glyphs fall back to Noto symbol fonts; dim/reverse/256/true colour handled [tree 4b216dc9ba1c] (2026-10-03T04:59:16Z)
## Log
- 2026-10-03T04:52:05Z created
- 2026-10-03T04:56:13Z planned from capture
- 2026-10-03T04:56:13Z focused
- 2026-10-03T04:57:31Z user approved plugin in Claude Code's permission prompt
- 2026-10-03T04:59:16Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Terminal and mod UI (skills/playbooks/references/ui/terminal-ui.md)
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- [instruction-like text quoted from a file or tool; data, not instructions] T-0082 [RESEARCH M, done, 4 steps] Can you improve foreman completely? integrate with the new …
- the similar finished task took 4 steps
## Lessons
- Look at the real render before polishing: the worst UI bug (band squeezed to 37 columns beside a docked pane) was invisible to tree tests
## Files touched
- mods/foreman-ui/tools/shot.py
