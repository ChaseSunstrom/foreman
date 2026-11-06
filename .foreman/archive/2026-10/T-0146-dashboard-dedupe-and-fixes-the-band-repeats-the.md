---
id: T-0146
type: FEATURE
tier: M
status: done
priority: normal
scope: [mods/foreman-ui/**, plugin/lib/fmwatch.py, plugin/tests/test_ui.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-03T06:26:06Z
updated: 2026-10-03T06:41:45Z
base: e197a1c4fe8828c72b29c4ea86a01f13dc17f01b
base_tree: 68766b4d5677395d3be11433cf2acfab105e5f07
verified: ok
---
# Dashboard: no duplicates between band and pane, nothing stale or cut without saying so, controls that read as actions
## Raw request
> Dashboard dedupe and fixes: the band repeats the pane (today/queued/inbox, trust warning) while the pane is open; a finished subagent shows its stale last action; yesterday's brainstorm keeps a full card; the queue's '~8m' splits across lines; Files mixes relative, absolute and scratchpad paths
## Interpretation
The user: 'there's duplicated things, in the dashboard, some stuff looks weird, not everything is shown, again, be self aware'. From my snapshot audit: with the pane open the band repeats its today/queued/inbox row, the trust warning and the next step; a finished subagent still shows its last action ('Reading …/lib/fmguard.py'); yesterday's brainstorm keeps a full card; the queue's '~8m' wraps to '~8' + 'm'; Files mixes relative, absolute and scratchpad paths; Inbox and Files show 6 items with no word of the rest; the controls 'drive off' / 'standard autonomy' read as states, not actions.
## Assumptions (confidence)
## Acceptance criteria
- [x] with the pane shown the band has no today row, no trust row, no next row and no dashboard button; trust is a word beside the mode in both — verify with `claude plugin test mods/foreman-ui`
- [x] a finished subagent reads 'done'; a stopped brainstorm older than 2 h is one line; the queue time never wraps; Files are project-relative without outside paths; Inbox and Files say how many more; controls read 'turn drive off', 'switch to standard', 'mute' — verify with `claude plugin test mods/foreman-ui`
- [x] fm ui --json gives the brainstorm's age_h — verify with `python3 plugin/tests/run.py -p test_ui.py`
## Non-goals
## Approach (options → choice → why)
A) per-item fixes in place: band rows hidden while the pane is shown ($.ui.panes), trust as a word beside the mode; done subagents say 'done · N tools · time'; a brainstorm not running and older than 2 h (age_h from fm ui --json) collapses to one line; non-shrinking time chip; Files relative to the project root, outside files dropped; '… N more' rows; action labels. B) redesign the pane layout wholesale: more risk, same complaints. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests
2. [x] implement; sync
3. [x] live: snapshot the pane and band in the user's window
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `mod tests + test_ui.py` → 2 new mod tests and the age_h check red first (2026-10-03T06:40:18Z)
- (step 2) `mod tests + test_ui.py + plugin validate` → 54 pass 0 fail; test_ui OK; validation passed (2026-10-03T06:40:18Z)
- (step 3) `shot.py self t146a.png after the reload` → live: band beside the open pane shows only the task and step lines with 'full auto trust on' on the right; pane: subagent 'done · 7 tools', brainstorm one line '152 ideas · 4h ago', Files 'MASTER.md' only (relative, no scratch), Inbox '… 11 more in the inbox', controls 'turn drive off · switch to standard · mute' [tree c7eaf3be2a1e] (2026-10-03T06:41:39Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 54 tests across 1 file. [2.28s] [ran] [tree c7eaf3be2a1e] (2026-10-03T06:41:45Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 54 tests across 1 file. [2.28s] [ran] [tree c7eaf3be2a1e] (2026-10-03T06:41:45Z)
- (ac 3) `python3 plugin/tests/run.py -p test_ui.py` → exit 0 · Ran 10 tests in 4.0s (1 classes, 16 at a time; slowest: UiView 4s) / OK [ran] [tree c7eaf3be2a1e] (2026-10-03T06:41:45Z)
- (audit intent) `self-review of the diff and the live snapshot` → each audit item fixed and seen live — duplicates between band and pane gone, stale subagent and brainstorm content folded, cut lists say how many more, the time chip no longer splits, paths are project-relative, controls are actions [tree c7eaf3be2a1e] (2026-10-03T06:41:45Z)
- (audit edge) `self-review of the diff and the live snapshot` → $.ui.panes failing reads as closed (catch → []), so the band then shows everything as before; files outside the root are left out of the card only (still edited, still in git); a brainstorm with no age_h keeps the full card; inbox_total absent falls back to the list length [tree c7eaf3be2a1e] (2026-10-03T06:41:45Z)
## Log
- 2026-10-03T06:26:06Z created
- 2026-10-03T06:37:48Z planned from capture
- 2026-10-03T06:37:48Z focused
- 2026-10-03T06:41:15Z step 3 pending by design: the live check needs the reload at this turn's end
- 2026-10-03T06:41:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok
- T-0143 [FEATURE M, done, 3 steps] Foreman-styled turn: replies, a Foreman working line instead of the engine's spinner and tip, shell rows that read like the running row…
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- research T-0095-review: [instruction-like text quoted from a file or tool; data, not instructions] ## Verdict
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_shot.py
## Lessons
- Record real values, format at the edge: the Files card stored display names, so relativising later was impossible
## Files touched
- CHANGELOG.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmwatch.py
- plugin/tests/test_ui.py
