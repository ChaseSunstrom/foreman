---
id: T-1431
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T20:43:50Z
updated: 2026-10-22T15:53:01Z
group: narrow-terminal layout at 80 columns
base: 073726fb1b977767e33017362497d101b756b7c1
base_tree: 54b988f4d1911c764215e39e33171296de11fa77
plan0_at: 2026-10-22T15:39:21Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code app: labels and box titles measured in columns
## Raw request
> fm code app: the progress track's node labels count characters not columns (fmcodetui ~637-647), and the home and project box titles vanish at 80 columns when the note is long (room goes negative) (T-1301 builder)
## Interpretation
fmcodetui's progress track sizes node labels with len() (characters), so wide glyphs (CJK, emoji) overflow; the home and project box titles vanish at 80 columns when the note is long (the title's room goes negative).
## Assumptions (confidence)
## Acceptance criteria
- [x] a wide-glyph label fits its slot and a long note keeps the box title at 80 columns — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_labels_and_titles_measure_columns`
## Non-goals
## Approach (options → choice → why)
Use the module's existing display-width helper (grep fmcodetui for wcwidth/_cols/width) for the labels; clamp the title room at a minimum so the title shows truncated rather than vanishing.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] column widths and title clamp
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_labels_and_titles_measure_columns` → ✗ exit 1 · Ran 1 test in 0.041s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 0a74ed69e4e0] (2026-10-22T15:51:42Z)
- `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_labels_and_titles_measure_columns` → exit 0 · Ran 1 test in 0.081s / OK [ran] [tree 0a74ed69e4e0] (2026-10-22T15:51:42Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_labels_and_titles_measure_columns` → exit 0 · Ran 1 test in 0.003s / OK [ran] [tree 0a74ed69e4e0] (2026-10-22T15:51:43Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_labels_and_titles_measure_columns` → exit 0 · Ran 1 test in 0.003s / OK [ran] [tree 0a74ed69e4e0] (2026-10-22T15:51:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Width.test_labels_and_titles_measure_columns` → exit 0 · Ran 1 test in 0.005s / OK [ran] [tree 14b0f9bc7284] (2026-10-22T15:52:39Z)
- (audit edge) `builder (sonnet) test-first; red proved with fm task prove; merged; full test_code_tui green.` → a label too wide for its last cell is cut cleanly; the title keeps ≥4 columns and drops the note when both can't fit [tree 14b0f9bc7284] (2026-10-22T15:52:39Z)
- (audit adversary) `builder (sonnet) test-first; red proved with fm task prove; merged; full test_code_tui green.` → display only [tree 14b0f9bc7284] (2026-10-22T15:52:39Z)
- (audit self) `builder (sonnet) test-first; red proved with fm task prove; merged; full test_code_tui green.` → no findings [tree 14b0f9bc7284] (2026-10-22T15:52:39Z)
## Log
- 2026-10-21T20:43:50Z created
- 2026-10-22T15:38:11Z planned from capture
- 2026-10-22T15:38:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1431.builder.md
- 2026-10-22T15:39:19Z focused
- 2026-10-22T15:51:37Z merged worktree-agent-a53037eebf637864b (2 file(s))
- 2026-10-22T15:51:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a53037eebf637864b
- 2026-10-22T15:51:39Z focused
- 2026-10-22T15:52:58Z done
- 2026-10-22T15:53:01Z committed 5962fe07 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1301 [FIX M, done, 2 steps] fm code tui measures text by display width: fit, tail and wrap cut wide (CJK, emoji) text to its columns, with the ellipsis, and padded col…
- research T-1026-review: MEDIUM** `mods/foreman-ui/hooks/register.tsx:1736-1742` — the Agents bars do not stay in one column when a stop button shows. [stale: mods/forema…
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
