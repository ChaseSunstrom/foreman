---
id: T-1490
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/composition.md, plugin/skills/playbooks/references/ui/visual-qa.md, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:10Z
updated: 2026-10-22T18:02:20Z
base: a337171abadbbea754dd22bb07c79836189b5ff6
base_tree: 02b9ac814ab33c5b5da56ac5e9856c935286d39c
plan0_at: 2026-10-22T17:51:03Z
plan0_scope: [plugin/skills/playbooks/references/ui/composition.md]
verified: strong
---
# UI playbook: composition, depth and states
## Raw request
> UI playbook: composition, depth and states
## Interpretation
Brainstorm T-1479 cluster 1: layout that isn't the SaaS-card kit: grids and rhythm, alignment as a choice, hierarchy by scale and space, depth without WebGL (layers, light, shadow that has a source, backdrops), a hero that opens with the subject's most characteristic thing, landing-page structure, and a state atlas (empty, loading, error, partial, offline, overflow) for every screen. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/composition.md covers grid and rhythm, hierarchy, depth without WebGL, hero, landing structure and the state atlas — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/composition.md').read(); miss=[s for s in ['## Grid and rhythm','## Hierarchy','## Depth without WebGL','## The hero','## State atlas',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
Options: component catalogue (that is the generic kit); chosen: principles plus ASCII wireframes comparing three layouts for one brief, and the state atlas as a checklist table.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/composition.md
2. [x] ASCII wireframes for three contrasting layouts
## Resume here
## Docs impact
CHANGELOG.md line; plugin/skills/playbooks/SKILL.md index
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/composition.md').read(); miss=[s for s in ['## Grid and rhythm','## Hierarchy','## Depth without WebGL','## The hero','## State atlas',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 805f8edff445] (2026-10-22T18:00:56Z)
- (step 2) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/check_doc.py plugin/skills/playbooks/references/ui/composition.md /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/probe.js` → exit 0 · json ok, 13 keys / probe ok [ran] [tree 805f8edff445] (2026-10-22T18:00:59Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/composition.md').read(); miss=[s for s in ['## Grid and rhythm','## Hierarchy','## Depth without WebGL','## The hero','## State atlas'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree b05087f2ccf7] (2026-10-22T18:02:07Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/composition.md').read(); miss=[s for s in ['## Grid and rhythm','## Hierarchy','## Depth without WebGL','## The hero','## State atlas'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree b05087f2ccf7] (2026-10-22T18:02:07Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/composition.md').read(); miss=[s for s in ['## Grid and rhythm','## Hierarchy','## Depth without WebGL','## The hero','## State atlas'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree b05087f2ccf7] (2026-10-22T18:02:07Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/composition.md').read(); miss=[s for s in ['## Grid and rhythm','## Hierarchy','## Depth without WebGL','## The hero','## State atlas',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree b05087f2ccf7] (2026-10-22T18:02:17Z)
- (audit intent) `builder ran every embedded piece: the console probe in headless Chromium on a planted page (caught a long centred paragraph, a spilling flex row, a covered button, nested cards, two token shadows, z-index 9999), both greps on good and bad CSS, Intl compact notation in node, the scrim opacities from WCAG luminance; I indexed it, linked visual-qa's empty fixture to its state atlas; a batch reviewer pass over the new UI playbooks follows` → layout beyond the card kit, every rule measurable by the probe or a grep [tree b05087f2ccf7] (2026-10-22T18:02:17Z)
- (audit edge) `builder ran every embedded piece: the console probe in headless Chromium on a planted page (caught a long centred paragraph, a spilling flex row, a covered button, nested cards, two token shadows, z-index 9999), both greps on good and bad CSS, Intl compact notation in node, the scrim opacities from WCAG luminance; I indexed it, linked visual-qa's empty fixture to its state atlas; a batch reviewer pass over the new UI playbooks follows` → the probe reads the first viewport at rest only; the axis limits are judgement, raised by DESIGN.md [tree b05087f2ccf7] (2026-10-22T18:02:17Z)
- (audit maintainer) `builder ran every embedded piece: the console probe in headless Chromium on a planted page (caught a long centred paragraph, a spilling flex row, a covered button, nested cards, two token shadows, z-index 9999), both greps on good and bad CSS, Intl compact notation in node, the scrim opacities from WCAG luminance; I indexed it, linked visual-qa's empty fixture to its state atlas; a batch reviewer pass over the new UI playbooks follows` → points to design-direction, type-and-colour and motion rather than repeating them [tree b05087f2ccf7] (2026-10-22T18:02:17Z)
- (audit operator) `builder ran every embedded piece: the console probe in headless Chromium on a planted page (caught a long centred paragraph, a spilling flex row, a covered button, nested cards, two token shadows, z-index 9999), both greps on good and bad CSS, Intl compact notation in node, the scrim opacities from WCAG luminance; I indexed it, linked visual-qa's empty fixture to its state atlas; a batch reviewer pass over the new UI playbooks follows` → indexed; visual-qa now points at the state atlas [tree b05087f2ccf7] (2026-10-22T18:02:17Z)
## Log
- 2026-10-22T17:36:10Z created
- 2026-10-22T17:50:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1490.builder.md
- 2026-10-22T17:51:02Z focused
- 2026-10-22T18:01:48Z merged worktree-agent-a4b492d51d129e077 (1 file(s))
- 2026-10-22T18:01:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4b492d51d129e077
- 2026-10-22T18:01:49Z focused
- 2026-10-22T18:01:50Z set scope=['plugin/skills/playbooks/references/ui/composition.md', 'plugin/skills/playbooks/references/ui/visual-qa.md', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T18:02:19Z done
- 2026-10-22T18:02:20Z committed 8ecf3742 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1500 [FEATURE S, planned, 1 steps] UI playbook: visual QA with screenshots and receipts
- T-1494 [FEATURE M, done, 2 steps] 3D playbook: scene composition, budget and survival contract — lesson: API facts from memory in a playbook need a reviewer who checks e…
- T-1492 [FEATURE M, done, 2 steps] Motion playbook: choreography, timing and reduced motion — lesson: Sibling playbooks need one stated precedence rule where their number…
- decision 2026-10-15: Pane order: Needs you and waiting plans above the hero (T-0909)
- similar finished tasks took 2–2 steps
## Why not caught
new playbook
## Lessons
- Ship a measuring probe with a layout playbook; prose rules about rhythm are unreviewable without one.
## Files touched
- plugin/skills/playbooks/references/ui/composition.md
- CHANGELOG.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/visual-qa.md
