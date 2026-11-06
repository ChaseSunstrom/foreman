---
id: T-0179
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/kit.ts, mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-03T18:42:20Z
updated: 2026-10-03T18:48:22Z
base: 83b91e8d178f5d52dc02a8e5fc7ed5c7904635e5
base_tree: 0b3f4555925c0af53518532e53f3733fa0056d18
verified: strong
---
# Each reply is a panel: a round-bordered box per message, the closing report accented
## Raw request
> a lot of your output still doesn't look right to me, can we have each message be formatted and look like a panel or something? and better formatting or whatever?
## Interpretation
The user: 'a lot of your output still doesn't look right … can we have each message be formatted and look like a panel or something? and better formatting'. Screenshots (this session and the user's volt window) show replies as bare ● lines in the same grey as the tool rows, so a message doesn't read as one.
## Assumptions (confidence)
## Acceptance criteria
- [x] a reply block renders as a round-bordered panel, accented when it is the closing report — verify with `cd mods/foreman-ui && claude plugin test .`
## Non-goals
## Approach (options → choice → why)
A: the AssistantMessage hook wraps each block in a round-bordered Box (the band's style, paddingX 1), the mark inside on the reply's first block; border dim grey, accent for the closing report (a block with Foreman's Changed:/✓/✗/Next: lines), pulsing accent while live. B (rejected): a left accent bar per line, compact, but it doesn't read as a panel, which is what was asked. A titled top border (╭─ Foreman ──╮) would need a hand-drawn border, since Box has no per-side border, and costs a line per message.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test the panel (red)
2. [x] panel in the AssistantMessage hook
3. [x] sync dev-mods, reload, screenshot, docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (foreman-ui panels)
## Verification evidence
- (step 1) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 1 fail / Ran 57 tests across 1 file. [2.48s] [ran] [tree 420d175c3467] (2026-10-03T18:44:19Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.56s] [ran] [tree d3c2dc79bfae] (2026-10-03T18:44:32Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.70s] [ran] [tree d371497922b1] (2026-10-03T18:46:31Z)
- (step 3) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.53s] [ran] [tree 1a49dea8a404] (2026-10-03T18:47:32Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 57 tests across 1 file. [2.48s] [ran] [tree 99b6361665d2] (2026-10-03T18:48:14Z)
- (audit intent) `self: three live screenshots of this session after each reload (shot.py self), 57 mod tests with panel, colour and width checks, plugin validate` → both asks met as screenshotted — each reply is a panel (grey; the closing report teal; the live one pulsing) and, per the steer, commands, edits and agent runs are panels in their own toned-down colour, red on failure, pulsing while running; reads and searches stay one line so the transcript isn't all boxes; all full width after the live check caught short command panels hugging their text [tree 99b6361665d2] (2026-10-03T18:48:14Z)
- (audit operator) `self: three live screenshots of this session after each reload (shot.py self), 57 mod tests with panel, colour and width checks, plugin validate` → each panel costs two lines, so a turn grows taller; a reply over 9000 characters or with control characters still falls back to the engine's own drawing, without a panel; other sessions get panels only when the mod is released (installed 0.4.0) [tree 99b6361665d2] (2026-10-03T18:48:14Z)
- (audit intent) `self: three live screenshots of this session after each reload (shot.py self), 57 mod tests with panel, colour and width checks, plugin validate` → both asks met as screenshotted — each reply is a panel (grey; the closing report teal; the live one pulsing) and, per the steer, commands, edits and agent runs are panels in their own toned-down colour, red on failure, pulsing while running; reads and searches stay one line so the transcript isn't all boxes; all full width after the live check caught short command panels hugging their text [tree 99b6361665d2] (2026-10-03T18:48:22Z)
- (audit operator) `self: three live screenshots of this session after each reload (shot.py self), 57 mod tests with panel, colour and width checks, plugin validate` → each panel costs two lines, so a turn grows taller; a reply over 9000 characters or with control characters still falls back to the engine's own drawing, without a panel; other sessions get panels only when the mod is released (installed 0.4.0) [tree 99b6361665d2] (2026-10-03T18:48:22Z)
## Log
- 2026-10-03T18:42:20Z created
- 2026-10-03T18:44:08Z planned from capture
- 2026-10-03T18:44:08Z focused
- 2026-10-03T18:44:42Z synced to dev-mods; ending the turn so the mod reloads, then screenshot this session's replies
- 2026-10-03T18:45:23Z steer: and the command changes or whatever I want in panels or something too
- 2026-10-03T18:46:05Z scope: mods/foreman-ui/hooks/rows.tsx and hooks/kit.ts — the steer puts commands, edits and agent rows in panels: their row renderers live in rows.tsx and the shared tint colour helper in kit.ts
- 2026-10-03T18:46:38Z steer applied: shell, edit and agent rows are panels tinted with their colour (red on failure), running ones pulse; synced; reloading to screenshot
- 2026-10-03T18:48:22Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/hooks/rows.tsx', 'mods/foreman-ui/hooks/kit.ts', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-03T18:48:22Z done
- 2026-10-03T18:48:22Z committed ed25a90 (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0143 [FEATURE M, done, 3 steps] Foreman-styled turn: replies, a Foreman working line instead of the engine's spinner and tip, shell rows that read like the running row…
- T-0137 [FEATURE M, done, 3 steps] Everything in the chat: shell rows with their output formatted inline, folded command groups unfolded, the pane's Output card gone — le…
- T-0141 [FEATURE M, done, 3 steps] Clean tool rows: Edit/Write results as Foreman rows with a compact coloured diff; shell commands wrap under themselves — lesson: Snapsh…
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
## Lessons
- Check a layout change in the live render, not only in tests: the unit tests saw a bordered box, the screenshot showed short panels hugging their text while long ones filled the row.
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/rows.tsx
- MASTER.md
- CHANGELOG.md
