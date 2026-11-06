---
id: T-1027
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T02:08:47Z
updated: 2026-10-16T02:56:52Z
---
# Multiple panes: a full-width pane across the top of Claude Code, not only the right-hand d
## Raw request
> Multiple panes: a full-width pane across the top of Claude Code, not only the right-hand dock
## Interpretation
Use more of the screen than the right-hand dock. Claude Code gives a mod no surface at the top of the screen: a pane docks beside the transcript (fullscreen) or sits inline above the prompt, a second pane is a tab in the same dock, and the band above the prompt is the only other surface (the transcript column's width, under the transcript). So: put Activity in that band, full transcript width while the pane is open, and give its rows in the pane to History.
## Assumptions (confidence)
## Acceptance criteria
- [ ] With the pane docked, the band above the prompt draws the Activity lanes across the transcript column and the pane has no Activity section (its rows go to the others); with the pane closed the band is as before — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Options: (a) a second pane: a tab, never shown beside the first; (b) the band above the prompt with a copy of the head: redundant (the one-panel request, T-0989); (c) the band carries the Activity lanes, wide, and the pane drops them: two surfaces, no repeats, the transcript column's empty bottom used. Choice (c); off the terminal, or with the pane closed, things stay as they are.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing mod tests: band draws lanes beside a docked pane; the pane drops Activity then  <- CURRENT
2. [ ] Move the lanes into a shared builder; band renders it while the pane is docked; pane layout without Activity
3. [ ] Live look in the harness; README, CHANGELOG, foreman-ui version
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-16T02:08:47Z created
- 2026-10-16T02:54:05Z steer (T-1033): the band beside the pane should be the live session/agent tree, not only the Activity lanes; build them as one
- 2026-10-16T02:56:52Z dropped: merged into T-1033: the band beside the docked pane becomes the live tree (the user's later ask), not the Activity lanes
## Follow-ups captured
