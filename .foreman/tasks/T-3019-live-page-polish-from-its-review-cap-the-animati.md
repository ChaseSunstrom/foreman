---
id: T-3019
type: PERFORMANCE
tier: S
status: blocked
priority: normal
scope: [plugin/web/live/live.js, plugin/web/live/live.css, plugin/tests/test_live_page.py]
depends_on: [T-3055, T-3092]
source: discovered
created: 2026-11-04T20:31:43Z
updated: 2026-11-05T02:09:35Z
group: live page polish and charts
---
# Live page polish from its review: cap the animation loop near 30 fps when nothing moves…
## Raw request
> Live page polish from its review: cap the animation loop near 30 fps when nothing moves (an always-open tab burns CPU) and record a frame-time measurement; raise the 9-10.5px labels to 11px; keep the focus plaque off Jeff's towers below 1400px
## Interpretation
Reading 1 (taken): three polish items from the live page's review, now for the forge theme (opt-in since T-3055) and anything still animating in the modern one: the scene's loop drops to about 30 fps when nothing moves and a frame-time measurement is recorded; labels under 11px become 11px; the focus plaque stays off Jeff's towers below 1400px. Reading 2 (ruled out): drop the forge scene: the user kept it as a setting.
## Assumptions (confidence)
## Acceptance criteria
- [ ] The forge scene's loop runs at about 30 fps or less when nothing moves, and a test records frame times (median and p95) with the page idle — verify with `python3 plugin/tests/run.py test_live_page`
- [ ] No label on the live page is under 11px in either theme — verify with `python3 plugin/tests/run.py test_live_page`
- [ ] Below 1400px the focus plaque never covers Jeff's towers — verify with `python3 plugin/tests/run.py test_live_page`
## Non-goals
## Approach (options → choice → why)
1) use what exists: the idle-redraw rule T-3034 gave the Network view, applied to the forge scene's loop; a frame-time probe in the page tests; a CSS floor for label sizes; the plaque's layout rule at 1400px: likely outcome: a small diff after the redesign lands. 2) do less: labels only: fails if: an always-open forge tab keeps burning CPU. Choice 1 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] idle frame cap with a frame-time test, label floor, plaque rule (tests first)  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T20:31:43Z created
- 2026-11-05T02:09:33Z set depends_on=['T-3055', 'T-3092'], scope=['plugin/web/live/live.js', 'plugin/web/live/live.css', 'plugin/tests/test_live_page.py']
- 2026-11-05T02:09:35Z planned: it has criteria and steps
- 2026-11-05T02:09:35Z set approved=True
- 2026-11-05T02:09:35Z blocked: after T-3055 (merging) and T-3092 (modern charts), which rewrite the same live.js and live.css
## Follow-ups captured
