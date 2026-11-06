---
id: T-1500
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/visual-qa.md, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:14Z
updated: 2026-10-22T18:01:35Z
base: d62a3d329728b893367660a02e1e3114366d5024
base_tree: 0fa5aaf5400efa09bec7028ae5cf3dc7c61d4963
plan0_at: 2026-10-22T17:54:44Z
plan0_scope: [plugin/skills/playbooks/references/ui/visual-qa.md]
verified: ok
---
# UI playbook: visual QA with screenshots and receipts
## Raw request
> UI playbook: visual QA with screenshots and receipts
## Interpretation
Brainstorm T-1479 cluster 8: UI work is proven by looking: fm smoke web at three viewports (360, 768, 1440), light and dark, reduced motion, a seeded fixture so frames are stable, an eyeball checklist (overlap, overflow, contrast, alignment, empty states), and a receipt in the task's evidence (the screenshot paths and what was checked). Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/visual-qa.md gives the fm smoke commands, the viewports, the eyeball checklist and the receipt format — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/visual-qa.md').read(); miss=[s for s in ['fm smoke','360','1440','## Eyeball checklist','## Receipt',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/visual-qa.md
## Resume here
## Docs impact
CHANGELOG.md line; plugin/skills/playbooks/SKILL.md index
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/visual-qa.md').read(); miss=[s for s in ['fm smoke','360','1440','## Eyeball checklist','## Receipt',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree d00784cf0e5e] (2026-10-22T17:59:49Z)
- (step 1) `node frames.mjs (the playbook's script, extracted; launch given QA_CHROME for the local 1243 shell) on a clean page and a broken page via python http.server` → clean: 7 frames, exit 0, identical hashes over two runs, Date frozen at 2026-01-15T10:00Z, reduce-still ok; broken: overflow 556/148 px, NaN, reduce-still MOVING, exit 1; no args: usage, exit 2 [tree d00784cf0e5e] (2026-10-22T17:59:54Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/visual-qa.md').read(); miss=[s for s in ['fm smoke','360','1440','## Eyeball checklist','## Receipt'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 02b9ac814ab3] (2026-10-22T18:01:13Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/visual-qa.md').read(); miss=[s for s in ['fm smoke','360','1440','## Eyeball checklist','## Receipt'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 02b9ac814ab3] (2026-10-22T18:01:14Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/visual-qa.md').read(); miss=[s for s in ['fm smoke','360','1440','## Eyeball checklist','## Receipt',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 02b9ac814ab3] (2026-10-22T18:01:24Z)
- (audit intent) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → a UI change is proven by looking at a seeded frame matrix, recorded as a receipt [tree 02b9ac814ab3] (2026-10-22T18:01:24Z)
- (audit edge) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → fm smoke covers only 1440 and 390 today (T-1565 captured to extend it); the script needs the project's own Playwright [tree 02b9ac814ab3] (2026-10-22T18:01:24Z)
- (audit operator) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → works from Claude Code (Read shows PNGs) and fm code (frames as a verify, the eyeball line pending) [tree 02b9ac814ab3] (2026-10-22T18:01:24Z)
- (audit self) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → no findings [tree 02b9ac814ab3] (2026-10-22T18:01:24Z)
- (audit intent) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → a UI change is proven by looking at a seeded frame matrix, recorded as a receipt [tree 02b9ac814ab3] (2026-10-22T18:01:32Z)
- (audit edge) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → fm smoke covers only 1440 and 390 today (T-1565 captured to extend it); the script needs the project's own Playwright [tree 02b9ac814ab3] (2026-10-22T18:01:32Z)
- (audit operator) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → works from Claude Code (Read shows PNGs) and fm code (frames as a verify, the eyeball line pending) [tree 02b9ac814ab3] (2026-10-22T18:01:32Z)
- (audit self) `self: read the structure and receipt; the builder ran the embedded frame script on a clean and a broken page (identical hashes twice, frozen date, reduced-motion check; overflow, NaN and motion caught, exit 1; usage exit 2) and viewed a frame through the Read tool as a Claude Code session would; test_docs green with the index line` → no findings [tree 02b9ac814ab3] (2026-10-22T18:01:32Z)
## Log
- 2026-10-22T17:36:14Z created
- 2026-10-22T17:54:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1500.builder.md
- 2026-10-22T17:54:44Z focused
- 2026-10-22T18:01:11Z merged worktree-agent-a5dca2251b929b015 (1 file(s))
- 2026-10-22T18:01:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5dca2251b929b015
- 2026-10-22T18:01:12Z focused
- 2026-10-22T18:01:13Z set scope=['plugin/skills/playbooks/references/ui/visual-qa.md', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T18:01:32Z scope: .qa/frames/* were the builder's trial frames from running the playbook's script in its worktree; never committed, not in the main checkout
- 2026-10-22T18:01:34Z done
- 2026-10-22T18:01:35Z committed a337171a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- T-1490 [FEATURE M, active, 2 steps] UI playbook: composition, depth and states
- T-1492 [FEATURE M, done, 2 steps] Motion playbook: choreography, timing and reduced motion — lesson: Sibling playbooks need one stated precedence rule where their number…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–2 steps
## Why not caught
new playbook
## Lessons
- A playbook that ships a script should be run against a clean and a broken fixture before it lands.
## Files touched
- plugin/skills/playbooks/references/ui/visual-qa.md
- .qa/frames/412c63d8-full/index-html-1440-dark.png
- .qa/frames/412c63d8-full/index-html-1440-light.png
- .qa/frames/412c63d8-full/index-html-360-dark.png
- .qa/frames/412c63d8-full/index-html-360-light.png
- .qa/frames/412c63d8-full/index-html-360-reduce.png
- .qa/frames/412c63d8-full/index-html-768-dark.png
- .qa/frames/412c63d8-full/index-html-768-light.png
- .qa/frames/412c63d8-full/broken-html-1440-dark.png
- .qa/frames/412c63d8-full/broken-html-1440-light.png
- .qa/frames/412c63d8-full/broken-html-360-dark.png
- .qa/frames/412c63d8-full/broken-html-360-light.png
- .qa/frames/412c63d8-full/broken-html-360-reduce.png
- .qa/frames/412c63d8-full/broken-html-768-dark.png
- .qa/frames/412c63d8-full/broken-html-768-light.png
- CHANGELOG.md
- plugin/skills/playbooks/SKILL.md
