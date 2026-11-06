---
id: T-0181
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx,mods/foreman-ui/tests/foreman-ui.test.tsx,CHANGELOG.md,MASTER.md]
depends_on: []
source: user
created: 2026-10-03T18:52:15Z
updated: 2026-10-03T19:05:12Z
base: 505e8438e7148b1d9c778bd0796ac510c28d6313
base_tree: b77eb9dcfefa7fbee6680ee140deb6e0aa717390
verified: strong
---
# Dashboard matches the chat: header and controls in panels, quiet card borders, steps/criteria/audits aligned; the band stays quiet while the dashboard is open
## Raw request
> the dashboard panel looks weird with the AC and audits thing not matching, and then the top of the panels with foreman etc look weird and the buttons aren't pannelled etc. and also the pannels color doesnt matchj the background color of the chat for some reason
## Interpretation
The user: the dashboard's AC and audits rows don't match the steps, its top (Foreman, mode, today) looks off, the buttons aren't panelled, its panel colours don't match the chat's; and (steer) the band at the bottom of the chat repeats the dashboard while the pane is open.
## Assumptions (confidence)
## Acceptance criteria
- [x] the dashboard and band render as described — verify with `cd mods/foreman-ui && claude plugin test .`
## Non-goals
## Approach (options → choice → why)
A: the pane's header (name, mode, today, mascot) and its controls each become a round panel; every card's border is the chat's quiet grey with colour only in its heading (task card accent, needs-you cards warn); the task card lists steps and done-when criteria under small labels in one glyph column, audits as a bar like the steps'; the band, while the pane is shown, draws only alerts (asks, waiting plans, paused hooks, background waits, done since your message) and nothing else. B (rejected): tint each card in its section colour, like the chat's tool panels — the user named the mismatched colours.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] pane header, cards, task card, controls; quiet band
3. [x] sync, reload, screenshot, docs
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (dashboard)
## Verification evidence
- (step 1) `cd mods/foreman-ui && claude plugin test .` → ✗ exit 1 · 3 fail / Ran 58 tests across 1 file. [2.62s] [ran] [tree b77eb9dcfefa] (2026-10-03T19:03:29Z)
- (step 2) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 58 tests across 1 file. [2.56s] [ran] [tree 86095fe334e0] (2026-10-03T19:04:05Z)
- (step 3) `cd mods/foreman-ui && claude plugin test . && diff -rq hooks ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui/hooks` → exit 0 · 0 fail / Ran 58 tests across 1 file. [2.53s] [ran] [tree 3b008ccd1c63] (2026-10-03T19:05:09Z)
- (ac 1) `cd mods/foreman-ui && claude plugin test .` → exit 0 · 0 fail / Ran 58 tests across 1 file. [2.52s] [ran] [tree 3b008ccd1c63] (2026-10-03T19:05:12Z)
- (audit intent) `self: live in the harness after a reload — header and controls panels, quiet grey cards, no band under the chat with the dashboard open; 58 mod tests` → each named issue addressed — AC/audits aligned with steps (labels, one glyph column, audits a bar), the top in a panel, the buttons in a panel, card colours unified with the chat's, and (steer) the band no longer duplicates the open dashboard [tree 3b008ccd1c63] (2026-10-03T19:05:12Z)
- (audit operator) `self: live in the harness after a reload — header and controls panels, quiet grey cards, no band under the chat with the dashboard open; 58 mod tests` → with the dashboard open, alerts (a yes needed, a plan waiting, a paused hook, background waits, done since your message) still show in the band; the band's dashboard button and the task line show only while the dashboard is closed; the pane's fill colour is the engine's frame (no option for it), and in the user's terminal it measured the same as the chat [tree 3b008ccd1c63] (2026-10-03T19:05:12Z)
## Log
- 2026-10-03T18:52:15Z created
- 2026-10-03T19:01:34Z steer: and the dashboard is duplicated at the bottom of the chat even though there's a pannel on the top right, and again, some things arent in pannels so it looks kind of weird
- 2026-10-03T19:03:26Z planned from capture
- 2026-10-03T19:03:26Z focused
- 2026-10-03T19:05:12Z done
- 2026-10-03T19:05:12Z committed 0a46793 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0122 [FEATURE M, done, 4 steps] UI polish from the live render: narrow band, colored type words, quiet controls, human next, cleaner header and footer — lesson: Judge …
- T-0146 [FEATURE M, done, 3 steps] Dashboard: no duplicates between band and pane, nothing stale or cut without saying so, controls that read as actions — lesson: Record …
- T-0179 [FEATURE M, done, 3 steps] Each reply is a panel: a round-bordered box per message, the closing report accented — lesson: Check a layout change in the live render…
- T-0182 [FEATURE M, done, 3 steps] Your own messages are panels too; questions and thinking summaries say why they can't be — lesson: An animation that stops ticking free…
## Lessons
- When the same facts appear in two places, decide which one owns them while both are visible; the band kept the task line 'because it stays useful' and the person read it as duplication.
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
- MASTER.md
