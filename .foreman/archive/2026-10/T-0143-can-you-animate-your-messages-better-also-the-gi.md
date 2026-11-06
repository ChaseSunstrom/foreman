---
id: T-0143
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/**, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T06:03:42Z
updated: 2026-10-03T06:36:52Z
base: e609225479975a43339b943c04d61d342810767b
base_tree: b86b615f8e6535671f63862f89f48c0c88dd152f
verified: ok
---
# Foreman-styled turn: replies, a Foreman working line instead of the engine's spinner and tip, shell rows that read like the running row, softer diff colours, a live snapshot loop
## Raw request
> can you animate your messages better? also the git diffs with the green/red are weird in contrast, and the $ in the shell commands or wahtever, that isn't animated like the Running, is weird, and the long commands/whatever don't look right, etc.? and can we get rid of the extra stuff below that? like the "Seasoning" thing for yourself? and have it be a foreman thing? idk, make it look better, add a hook to screenshot every few seconds so you can see first hand, etc.
## Interpretation
The user wants the whole turn to look like Foreman: their words — animate messages better; the red/green diff contrast is weird; the $ in finished shell rows doesn't match the animated Running row; long commands don't look right; get rid of the 'Seasoning…' line and the tip under it and make it a Foreman thing; my plain replies look out of place beside the Foreman rows; screenshot every few seconds to see it first hand. Replies keep the engine's markdown (a Markdown element), only the Foreman reply-format lines get Foreman colours.
## Assumptions (confidence)
## Acceptance criteria
- [x] the working line is Foreman's (animated mark, task and step, what the turn is doing, elapsed) with no engine word or tip — verify with `claude plugin test mods/foreman-ui`
- [x] a reply's first block opens with a Foreman mark that animates while the turn runs; Foreman reply lines (Changed:, ✓/✗, ⚑ Captured, ◆ Decided, Next:, ⚠ Needs you) are coloured like the rows; other text stays the engine's markdown — verify with `claude plugin test mods/foreman-ui`
- [x] a finished shell row reads like the running one: mark, its description, time and lines, the command under it dim (whole, up to 3 lines) with no $ prompt; diff lines use softer colours — verify with `claude plugin test mods/foreman-ui`
- [x] shot.py watch snapshots the session's own pane every few seconds — verify with `python3 plugin/tests/run.py -p test_shot.py`
- [x] under a shell row Claude Code's result block is replaced: no second copy of the output or the timeout; files the command changed, a git commit and an auto-background timeout appear as Foreman lines in the row — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Working line: A) keep the engine's spinner and add a suffix (today: the user calls it out), B) draw a Foreman tree in its place: mark animated from the shared frame, task id and step, a word for the mode (thinking, writing, running tools), elapsed from turn.start. Choice B; tokens are not offered to a tree, the band's context meter covers it. Replies: A) Markdown element for the whole block with a Foreman mark column, B) parse every line ourselves. Choice A plus line-level colouring only for the known Foreman reply lines (each drawn as a Text row); everything else stays one Markdown element. Shell row: description as the title like the running row, command under it dim without $. Snapshots: shot.py watch OUT --every 5 loop (the background loop already running proves it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests: spinner, reply rows, shell row shape, diff colours, watch
2. [x] implement; sync dev-mods
3. [x] live check: harness Haiku turn and own-pane snapshots
## Resume here
## Docs impact
CHANGELOG entry; shot.py docstring
## Verification evidence
- (step 1) `mod tests + test_shot.py` → 7 new/changed mod tests red first, then 51 pass; watch test red then OK (2026-10-03T06:32:45Z)
- (step 2) `mod tests + plugin validate` → 51 pass 0 fail; validation passed; dev copy synced (2026-10-03T06:32:45Z)
- (step 3) `shot.py self t143a.png --back 30 after the reload` → live in the user's window: '✓ ❯ Ran Print two lines… · 0.1s · 3 lines' with the command dim under it and the output once (no ⎿ copy); the working line '✳ T-0143 step 3/3 … · running tools · 6.0s' replaced 'Seasoning…' and its Tip; replies open with the accent mark and report lines are coloured (✎ changed, ✓, ⚑ captured, → next). Three follow-ups seen there (blank lines between groups, the 4-line plugin prompt, 'Cogitated' turn word) fixed test-first and synced for the next reload [tree 68766b4d5677] (2026-10-03T06:35:46Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 52 tests across 1 file. [2.41s] [ran] [tree 68766b4d5677] (2026-10-03T06:36:45Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 52 tests across 1 file. [2.41s] [ran] [tree 68766b4d5677] (2026-10-03T06:36:45Z)
- (ac 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 52 tests across 1 file. [2.41s] [ran] [tree 68766b4d5677] (2026-10-03T06:36:45Z)
- (ac 4) `python3 plugin/tests/run.py -p test_shot.py` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: Harness 0s) / OK [ran] [tree 68766b4d5677] (2026-10-03T06:36:45Z)
- (ac 5) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 52 tests across 1 file. [2.41s] [ran] [tree 68766b4d5677] (2026-10-03T06:36:45Z)
- (audit intent) `self-review of the diff and two live snapshots of the user's window` → each of the user's points maps to a change seen live — messages animated/Foreman-styled, softer diff colours, no $ and a Running-like finished row, long commands under the title (≤3 lines + count), the Seasoning line and tip replaced, plain replies matching the rows, snapshots every few seconds (shot.py watch, detached); duplicate shell output removed [tree 68766b4d5677] (2026-10-03T06:36:45Z)
- (audit edge) `self-review of the diff and two live snapshots of the user's window` → replies over 9000 chars or with control characters keep the engine's rendering (Markdown limits, test); report lines inside code fences stay markdown; bashEditDiff/gitOperation are read defensively (untyped); a command is never cut silently (3 lines + '… N more command lines'); errors and refused trees fall back to the engine's row [tree 68766b4d5677] (2026-10-03T06:36:45Z)
- (audit intent) `self-review of the diff and two live snapshots of the user's window` → each of the user's points maps to a change seen live — messages animated/Foreman-styled, softer diff colours, no $ and a Running-like finished row, long commands under the title (≤3 lines + count), the Seasoning line and tip replaced, plain replies matching the rows, snapshots every few seconds (shot.py watch, detached); duplicate shell output removed [tree 68766b4d5677] (2026-10-03T06:36:52Z)
- (audit edge) `self-review of the diff and two live snapshots of the user's window` → replies over 9000 chars or with control characters keep the engine's rendering (Markdown limits, test); report lines inside code fences stay markdown; bashEditDiff/gitOperation are read defensively (untyped); a command is never cut silently (3 lines + '… N more command lines'); errors and refused trees fall back to the engine's row [tree 68766b4d5677] (2026-10-03T06:36:52Z)
## Log
- 2026-10-03T06:03:42Z created
- 2026-10-03T06:04:03Z steer: 'and just your normal text output looks weird with everything else as well' — the assistant's own replies must match the Foreman rows
- 2026-10-03T06:08:50Z planned from capture
- 2026-10-03T06:23:55Z steer: 'a lot of the bash/task/diff stuff, basically everything still doesn't match foreman that well, and there's duplicated things, in the dashboard, some stuff looks weird, not everything is shown, again, be self aware' — start from a screenshot audit listing every mismatch, duplicate and missing item
- 2026-10-03T06:24:47Z focused
- 2026-10-03T06:36:52Z scope: plugin/tests/test_shot.py — the shot.py watch test lives with the other harness tests
- 2026-10-03T06:36:52Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0141 [FEATURE M, done, 3 steps] Clean tool rows: Edit/Write results as Foreman rows with a compact coloured diff; shell commands wrap under themselves — lesson: Snapsh…
- T-0137 [FEATURE M, done, 3 steps] Everything in the chat: shell rows with their output formatted inline, folded command groups unfolded, the pane's Output card gone — le…
- playbook Loop Design + Review (skills/playbooks/references/evals/loop-design-check.md)
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- similar finished tasks took 3–8 steps
- likely tests for the scope: plugin/tests/test_shot.py
## Lessons
- Snapshot the user's real window after each reload: the duplicate ⎿ block, the lost blank lines and the 4-line plugin prompt only showed there
## Files touched
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/tools/shot.py
- plugin/tests/test_shot.py
