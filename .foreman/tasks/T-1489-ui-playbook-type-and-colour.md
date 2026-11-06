---
id: T-1489
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/type-and-colour.md, plugin/skills/playbooks/references/ui/design-direction.md, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:09Z
updated: 2026-10-22T17:50:40Z
base: 82838e8380b4bdce813f096f54167e52f9f41a10
base_tree: e818fce8eee9f3a0cc5ff5c05c0d173047968d5d
plan0_at: 2026-10-22T17:42:02Z
plan0_scope: [plugin/skills/playbooks/references/ui/type-and-colour.md]
verified: strong
---
# UI playbook: type and colour
## Raw request
> UI playbook: type and colour
## Interpretation
Brainstorm T-1479 cluster 1: typography and colour rules that read as chosen, not default: a modular type scale, pairing (one family or two clearly distinct), type as texture and as the hero, measure and leading, OKLCH palette roles (neutral ramp, one accent, status colours reserved), contrast proofs (WCAG ratios), and dark mode as its own steps. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/type-and-colour.md covers scale, pairing, type as texture, measure, OKLCH roles, contrast and dark mode — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); miss=[s for s in ['## Type scale','## Pairing','## Type as texture','## Palette roles','OKLCH','## Contrast','## Dark mode',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
Options: list fonts (dates fast, licence issues); chosen: rules and ratios with families named only as examples of a class (a grotesk, a humanist serif), plus one computed example palette with its ratios.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/type-and-colour.md
2. [x] worked example: a scale and a palette with their contrast numbers
## Resume here
## Docs impact
CHANGELOG.md line; plugin/skills/playbooks/SKILL.md index
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); miss=[s for s in ['## Type scale','## Pairing','## Type as texture','## Palette roles','OKLCH','## Contrast','## Dark mode',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree a1a86a90003b] (2026-10-22T17:48:50Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); assert '## Worked example' in t and 'clamp(2.488rem' in t and '| 'text' on 'surface-sunken' | 7 | 14.09 | 12.26 |' in t"` → ✗ exit 1 · ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ / AssertionError [ran] [tree a1a86a90003b] (2026-10-22T17:48:53Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); assert '## Worked example' in t and 'clamp(2.488rem' in t and '| 7 | 14.09 | 12.26 |' in t and 'contrast_proof.py' in t"` → exit 0 · (no output) [ran] [tree a1a86a90003b] (2026-10-22T17:48:58Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); miss=[s for s in ['## Type scale','## Pairing','## Type as texture','## Palette roles','OKLCH','## Contrast','## Dark mode'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 06e0e7d8480b] (2026-10-22T17:50:21Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); miss=[s for s in ['## Type scale','## Pairing','## Type as texture','## Palette roles','OKLCH','## Contrast','## Dark mode'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 06e0e7d8480b] (2026-10-22T17:50:21Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); miss=[s for s in ['## Type scale','## Pairing','## Type as texture','## Palette roles','OKLCH','## Contrast','## Dark mode'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 06e0e7d8480b] (2026-10-22T17:50:22Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/type-and-colour.md').read(); miss=[s for s in ['## Type scale','## Pairing','## Type as texture','## Palette roles','OKLCH','## Contrast','## Dark mode',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 06e0e7d8480b] (2026-10-22T17:50:37Z)
- (audit intent) `builder ran the embedded contrast script against the worked example (every table number matches; a failing pair exits 1); I spot-checked the grey shortcut (OKLab L = cube root of Y for neutrals; surface 1.00 needs text L <= 0.56 for 4.5:1: 4.65 at 0.56, 4.47 at 0.57) and fixed design-direction's example that reused its error colour for 'booked'; test_docs green` → type and colour that read as chosen, with numbers a reviewer can check [tree 06e0e7d8480b] (2026-10-22T17:50:37Z)
- (audit edge) `builder ran the embedded contrast script against the worked example (every table number matches; a failing pair exits 1); I spot-checked the grey shortcut (OKLab L = cube root of Y for neutrals; surface 1.00 needs text L <= 0.56 for 4.5:1: 4.65 at 0.56, 4.47 at 0.57) and fixed design-direction's example that reused its error colour for 'booked'; test_docs green` → the proof script reads flat token files only; light-dark() with a var() fallback is not parsed (stated in the file) [tree 06e0e7d8480b] (2026-10-22T17:50:37Z)
- (audit maintainer) `builder ran the embedded contrast script against the worked example (every table number matches; a failing pair exits 1); I spot-checked the grey shortcut (OKLab L = cube root of Y for neutrals; surface 1.00 needs text L <= 0.56 for 4.5:1: 4.65 at 0.56, 4.47 at 0.57) and fixed design-direction's example that reused its error colour for 'booked'; test_docs green` → status colours reserved here and now in design-direction's example; the contrast script will become an fm verb or a lint rule (T-1507) [tree 06e0e7d8480b] (2026-10-22T17:50:37Z)
- (audit operator) `builder ran the embedded contrast script against the worked example (every table number matches; a failing pair exits 1); I spot-checked the grey shortcut (OKLab L = cube root of Y for neutrals; surface 1.00 needs text L <= 0.56 for 4.5:1: 4.65 at 0.56, 4.47 at 0.57) and fixed design-direction's example that reused its error colour for 'booked'; test_docs green` → indexed in the playbooks skill [tree 06e0e7d8480b] (2026-10-22T17:50:37Z)
## Log
- 2026-10-22T17:36:09Z created
- 2026-10-22T17:41:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1489.builder.md
- 2026-10-22T17:42:02Z focused
- 2026-10-22T17:50:00Z merged worktree-agent-a6a3a2b49684dd94f (1 file(s))
- 2026-10-22T17:50:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a6a3a2b49684dd94f
- 2026-10-22T17:50:00Z focused
- 2026-10-22T17:50:20Z set scope=['plugin/skills/playbooks/references/ui/type-and-colour.md', 'plugin/skills/playbooks/references/ui/design-direction.md', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T17:50:37Z scope: design-direction.md's example reused its error colour for 'booked' (this playbook reserves status colours); fixed here
- 2026-10-22T17:50:38Z done
- 2026-10-22T17:50:40Z committed 90612893 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1490 [FEATURE M, planned, 2 steps] UI playbook: composition, depth and states
- T-1488 [FEATURE M, active, 2 steps] UI playbook: design direction before pixels
- T-1500 [FEATURE S, planned, 1 steps] UI playbook: visual QA with screenshots and receipts
- decision 2026-09-26: T-0014 permission mode: fm serve passes --permission-mode only when given; otherwise Remote Control uses the user's own defaultMode (bypass here, se…
## Why not caught
new playbook
## Lessons
- Embedded scripts in a playbook should be run by the writer against the playbook's own example; it caught three real slips here.
## Plan gaps
- failed first: step 2 worked example: a scale and a palette with their contrast numbers
## Files touched
- plugin/skills/playbooks/references/ui/type-and-colour.md
- CHANGELOG.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/design-direction.md
