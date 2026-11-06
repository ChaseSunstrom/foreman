---
id: T-1491
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/interaction.md, plugin/skills/playbooks/references/ui/INDEX.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:10Z
updated: 2026-10-22T18:15:18Z
base: aea55198d17117bece982141beba404163546b31
base_tree: ce052b1016cdeda9698f7cfd3059568861fc7325
plan0_at: 2026-10-22T18:01:52Z
plan0_scope: [plugin/skills/playbooks/references/ui/interaction.md]
verified: strong
---
# UI playbook: interaction, forms, microcopy and mobile
## Raw request
> UI playbook: interaction, forms, microcopy and mobile
## Interpretation
Brainstorm T-1479 cluster 1: how a UI feels in the hand: feedback within 100 ms, focus and keyboard paths, forms (labels, validation timing, errors that say how to fix), microcopy (verbs, one name per action across the flow), touch targets and thumb zones, and responsive down to 360 px. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/interaction.md covers feedback timing, keyboard and focus, forms, microcopy and mobile — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/interaction.md').read(); miss=[s for s in ['## Feedback','## Keyboard and focus','## Forms','## Microcopy','## Mobile',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
Options: fold into composition (too long); chosen: its own file with a checklist per section and a before/after microcopy table.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/interaction.md
2. [x] a before/after microcopy table
## Resume here
## Docs impact
CHANGELOG.md line; plugin/skills/playbooks/references/ui/INDEX.md
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/interaction.md').read(); miss=[s for s in ['## Feedback','## Keyboard and focus','## Forms','## Microcopy','## Mobile',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 42d3eda9f294] (2026-10-22T18:13:31Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/interaction.md').read(); s=t.split('### Before and after')[1].split('###')[0]; rows=[l for l in s.splitlines() if l.startswith('| ') and not l.startswith('| Where') and not l.startswith('|---')]; assert len(rows)>=10, len(rows)"` → exit 0 · (no output) [ran] [tree 42d3eda9f294] (2026-10-22T18:13:33Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/interaction.md').read(); miss=[s for s in ['## Feedback','## Keyboard and focus','## Forms','## Microcopy','## Mobile'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 05be2257f9f8] (2026-10-22T18:14:50Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/interaction.md').read(); miss=[s for s in ['## Feedback','## Keyboard and focus','## Forms','## Microcopy','## Mobile'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 05be2257f9f8] (2026-10-22T18:14:50Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/interaction.md').read(); miss=[s for s in ['## Feedback','## Keyboard and focus','## Forms','## Microcopy','## Mobile'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 05be2257f9f8] (2026-10-22T18:14:51Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/interaction.md').read(); miss=[s for s in ['## Feedback','## Keyboard and focus','## Forms','## Microcopy','## Mobile',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 05be2257f9f8] (2026-10-22T18:14:59Z)
- (audit intent) `builder ran every embedded script against planted pages (interaction probe caught 22 defects and a focus trap, clean page exit 0; the double-press probe failed an unguarded button and passed a guarded one; the copy grep hit every bad pattern and no good one) and confirmed the doc's copies match what ran; indexed in the UI index; test_docs green` → how a UI behaves in the hand, each rule pass or fail, with probes that can be a verify command in fm code and run from a Claude Code session [tree 05be2257f9f8] (2026-10-22T18:14:59Z)
- (audit edge) `builder ran every embedded script against planted pages (interaction probe caught 22 defects and a focus trap, clean page exit 0; the double-press probe failed an unguarded button and passed a guarded one; the copy grep hit every bad pattern and no good one) and confirmed the doc's copies match what ran; indexed in the UI index; test_docs green` → scripts ran through a Playwright shim (the installed browser revision differs); a late JS focus style may be flagged; the double-press probe writes once, so seeded fixtures only [tree 05be2257f9f8] (2026-10-22T18:14:59Z)
- (audit maintainer) `builder ran every embedded script against planted pages (interaction probe caught 22 defects and a focus trap, clean page exit 0; the double-press probe failed an unguarded button and passed a guarded one; the copy grep hit every bad pattern and no good one) and confirmed the doc's copies match what ran; indexed in the UI index; test_docs green` → states which number wins where it overlaps a sibling playbook [tree 05be2257f9f8] (2026-10-22T18:14:59Z)
- (audit intent) `builder ran every embedded script against planted pages (interaction probe caught 22 defects and a focus trap, clean page exit 0; the double-press probe failed an unguarded button and passed a guarded one; the copy grep hit every bad pattern and no good one) and confirmed the doc's copies match what ran; indexed in the UI index; test_docs green` → how a UI behaves in the hand, each rule pass or fail, with probes that can be a verify command in fm code and run from a Claude Code session [tree 05be2257f9f8] (2026-10-22T18:15:12Z)
- (audit edge) `builder ran every embedded script against planted pages (interaction probe caught 22 defects and a focus trap, clean page exit 0; the double-press probe failed an unguarded button and passed a guarded one; the copy grep hit every bad pattern and no good one) and confirmed the doc's copies match what ran; indexed in the UI index; test_docs green` → scripts ran through a Playwright shim (the installed browser revision differs); a late JS focus style may be flagged; the double-press probe writes once, so seeded fixtures only [tree 05be2257f9f8] (2026-10-22T18:15:12Z)
- (audit maintainer) `builder ran every embedded script against planted pages (interaction probe caught 22 defects and a focus trap, clean page exit 0; the double-press probe failed an unguarded button and passed a guarded one; the copy grep hit every bad pattern and no good one) and confirmed the doc's copies match what ran; indexed in the UI index; test_docs green` → states which number wins where it overlaps a sibling playbook [tree 05be2257f9f8] (2026-10-22T18:15:12Z)
## Log
- 2026-10-22T17:36:10Z created
- 2026-10-22T18:01:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1491.builder.md
- 2026-10-22T18:01:51Z focused
- 2026-10-22T18:14:46Z merged worktree-agent-a111d199cebd64251 (1 file(s))
- 2026-10-22T18:14:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a111d199cebd64251
- 2026-10-22T18:14:47Z focused
- 2026-10-22T18:14:49Z set scope=['plugin/skills/playbooks/references/ui/interaction.md', 'plugin/skills/playbooks/references/ui/INDEX.md', 'CHANGELOG.md']
- 2026-10-22T18:15:15Z done
- 2026-10-22T18:15:18Z committed 16c6cd96 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1492 [FEATURE M, done, 2 steps] Motion playbook: choreography, timing and reduced motion — lesson: Sibling playbooks need one stated precedence rule where their number…
- T-1493 [FEATURE S, planned, 1 steps] Motion playbook: game feel with intensity caps
- T-1502 [FEATURE M, planned, 1 steps] Build playbooks: Go, JVM, Swift, C# and shell
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
- the similar finished task took 2 steps
## Why not caught
new playbook
## Lessons
- Probes in playbooks should print text, so fm code (no image input) can use them as verify commands.
## Files touched
- plugin/skills/playbooks/references/ui/interaction.md
- CHANGELOG.md
- plugin/skills/playbooks/references/ui/INDEX.md
