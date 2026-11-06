---
id: T-1301
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T23:37:51Z
updated: 2026-10-21T21:31:53Z
base: f0548424dcb549cded464acf9511af7db252e2a7
base_tree: 2ba9ac908f50e0dac2fa5032650d52e208175d07
plan0_at: 2026-10-21T20:21:13Z
plan0_scope: []
verified: strong
---
# fm code tui measures text by display width: fit, tail and wrap cut wide (CJK, emoji) text to its columns, with the ellipsis, and padded columns stay aligned
## Raw request
> Canvas `fit`/`put` use character count rather than display width (CJK/emoji will overflow boxes) — worth its own task
> (noticed by an agent; research brainstorm-20261020-tui)
## Interpretation
Canvas.put already draws a wide character in two cells and clips it, but fit, tail and wrap count characters, so a CJK or emoji title is cut by put without its ellipsis and padded columns (the history and project rows) drift. Measure display width everywhere text is cut or padded.
## Assumptions (confidence)
## Acceptance criteria
- [x] fit, tail and wrap return text whose display width is at most n, ending in … when cut, for CJK, emoji and accented text; plain ASCII results are unchanged — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] a history or project row with a CJK title draws with its later columns aligned and the box's right border intact at 80 and 120 columns — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options: (A) one width(s) from unicodedata (W/F = 2, combining = 0, else 1) used by fit, tail, wrap and a pad(s, n) for the f-string column widths in the list rows (chosen: stdlib, one rule, the same one put draws by); (B) wcwidth-style tables (a dependency, more exact for emoji presentation sequences; later if needed); (C) only clip in put (today: loses the ellipsis and alignment). Emoji ZWJ sequences count by their parts (a known ceiling, noted).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: fit/tail/wrap on wide text; a CJK row's alignment and border
2. [x] width() and pad(); fit, tail, wrap and the list rows use them
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_code_tui 2>&1 | tail -40` → ✗ exit 1 · Ran 102 tests in 60.3s (15 classes, 16 at a time; slowest: Fuzz 55s, Command 50s, Events 17s) / FAILED (1 classes) [ran] [tree 2f9ca0acba9b] (2026-10-21T20:24:03Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui 2>&1 | tail -40` → ✗ exit 1 · Ran 102 tests in 60.3s (15 classes, 16 at a time; slowest: Fuzz 55s, Command 50s, Events 17s) / FAILED (1 classes) [ran] [tree 2f9ca0acba9b] (2026-10-21T20:24:03Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 102 tests in 26.3s (15 classes, 16 at a time; slowest: Fuzz 25s, Command 24s, Events 11s) / FAILED (1 classes) [ran] [tree 89cc40f86c90] (2026-10-21T20:25:32Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 102 tests in 36.4s (15 classes, 16 at a time; slowest: Fuzz 36s, Command 34s, Events 15s) / OK [ran] [tree 4f8eb28fe69b] (2026-10-21T20:40:43Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 102 tests in 23.2s (15 classes, 16 at a time; slowest: Fuzz 22s, Command 20s, Events 8s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:28:40Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 102 tests in 18.5s (15 classes, 16 at a time; slowest: Command 18s, Fuzz 17s, Events 7s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:28:59Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 102 tests in 25.6s (15 classes, 16 at a time; slowest: Fuzz 25s, Command 18s, Events 7s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:31:50Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 102 tests in 25.6s (15 classes, 16 at a time; slowest: Fuzz 25s, Command 18s, Events 7s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:31:50Z)
- (audit intent) `self: read _cells, width, _take, pad, fit, tail and the row builders — one width rule (combining 0, East Asian W/F 2, else 1) shared with put; fit/tail stop counting at n columns (a 5 MB line costs ~3 ms); tail(n=0) now returns nothing` → fit, tail and wrap stay within n columns ending in … for CJK, emoji and accented text, ASCII unchanged; history and project rows with a CJK title keep columns aligned and the right border intact at 80 and 120 columns (test_code_tui Width) [tree 44850c6e72aa] (2026-10-21T21:31:50Z)
- (audit edge) `self: read _cells, width, _take, pad, fit, tail and the row builders — one width rule (combining 0, East Asian W/F 2, else 1) shared with put; fit/tail stop counting at n columns (a 5 MB line costs ~3 ms); tail(n=0) now returns nothing` → ZWJ emoji sequences count by their parts (ponytail note); progress-track labels and long box titles at 80 columns captured (T-1431); the app-opens test's raw-byte check flakes on cell-diff redraws (T-1430) [tree 44850c6e72aa] (2026-10-21T21:31:50Z)
## Log
- 2026-10-20T23:37:51Z created
- 2026-10-21T13:42:42Z planned from capture
- 2026-10-21T15:27:15Z grounded: Canvas.put already draws W/F as two cells and clips; fit (line 363), tail and wrap (373) count len(); 15 fit/tail/wrap calls and 18 padded spots (:<N, ljust) in fmcodetui, most padding ASCII ids and counts; user text sits last in rows (titles, requests) except _project_row's name:<24 and the selected row's ljust(iw). So width() in fit/tail/wrap fixes the cut and ellipsis; pad() is needed only where user text is followed by more columns. Second plan skipped: low-risk display fix, cause read in code.
- 2026-10-21T20:20:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1301.builder.md
- 2026-10-21T20:21:12Z focused
- 2026-10-21T20:57:15Z merged worktree-agent-a3a27d02c6ae7eced (2 file(s))
- 2026-10-21T20:57:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3a27d02c6ae7eced
- 2026-10-21T21:31:23Z focused
- 2026-10-21T21:31:50Z affected tests waived: UI mod JS subagent-row test times out at 5 s under load (T-1427, blocked with diagnosis)
- 2026-10-21T21:31:53Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1026-review: MEDIUM** `mods/foreman-ui/hooks/register.tsx:1736-1742` — the Agents bars do not stay in one column when a stop button shows. [stale: mods/forema…
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- decision 2026-10-21: T-1300 ships the renderer, motion, gradients, recording and round 1 of the TUI brainstorm; round 2 is queued as T-1305..T-1315 (with T-1301 wide cha…
## Why not caught
tests used ASCII titles only
## Lessons
- Measure terminal text by display columns everywhere it's cut or padded, with the same rule the canvas draws by
## Plan gaps
- failed first: step 1 Failing tests: fit/tail/wrap on wide text; a CJK row's alignment and border
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmmodels.py
- plugin/skills/improve/SKILL.md
- plugin/tests/test_bench.py
- plugin/tests/test_code_hardening.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_runner_lint.py
- plugin/tests/test_supply_delta.py
