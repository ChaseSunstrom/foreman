---
id: T-1493
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/game-feel.md, plugin/skills/playbooks/references/ui/INDEX.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:11Z
updated: 2026-10-22T18:12:40Z
base: 181fc4d050742e2b0bdaeeb523b994925d950c3f
base_tree: ec8cd1dfbc81881d9b3e350c3520aecf59f517b0
plan0_at: 2026-10-22T18:06:02Z
plan0_scope: [plugin/skills/playbooks/references/ui/game-feel.md]
verified: strong
---
# Motion playbook: game feel with intensity caps
## Raw request
> Motion playbook: game feel with intensity caps
## Interpretation
Brainstorm T-1479 cluster 2: juice for games and playful UI (anticipation, squash and stretch, hit-stop, screen shake, particles, easing curves, sound cues off by default) with caps so it never harms: a shake amplitude and duration ceiling, flash under 3 per second, reduced-motion fallbacks. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/game-feel.md lists each technique with its cap and its reduced-motion fallback — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/game-feel.md').read(); miss=[s for s in ['## Techniques','## Caps','## Reduced motion','hit-stop',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/game-feel.md
## Resume here
## Docs impact
CHANGELOG.md line; references/ui/INDEX.md
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/game-feel.md').read(); miss=[s for s in ['## Techniques','## Caps','## Reduced motion','hit-stop',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 681771659bb8] (2026-10-22T18:11:25Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/game-feel.md').read(); miss=[s for s in ['## Techniques','## Caps','## Reduced motion','hit-stop'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree ce052b1016cd] (2026-10-22T18:12:23Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/game-feel.md').read(); miss=[s for s in ['## Techniques','## Caps','## Reduced motion','hit-stop'] if s not in t]; assert not miss, miss" && python3 -I /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/check_juice.py` → ✗ exit 1 · ~~~~~~~~^^^ / IndexError: list index out of range [ran] [tree ce052b1016cd] (2026-10-22T18:12:23Z)
- (step 1) `python3 -c "import re; t=open('plugin/skills/playbooks/references/ui/game-feel.md').read(); exec(compile(re.search(r'\x60\x60\x60python\n(.*?)\x60\x60\x60', t, re.S).group(1), 'juice.py', 'exec'), {'__name__': '__main__'})"` → exit 0 · juice caps hold [ran] [tree ce052b1016cd] (2026-10-22T18:12:30Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/game-feel.md').read(); miss=[s for s in ['## Techniques','## Caps','## Reduced motion','hit-stop',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree ce052b1016cd] (2026-10-22T18:12:38Z)
- (audit intent) `self: the embedded juice.py runs from the playbook and prints 'juice caps hold'; the builder mutated each of 12 caps in a copy and the asserts caught all 12, and fixed a NaN shake and a 1-frame restart that defeated the 1 s cap; indexed in the UI index; test_docs green` → juice for games and playful UI with hard caps and a reduced-motion fallback for every technique [tree ce052b1016cd] (2026-10-22T18:12:38Z)
- (audit edge) `self: the embedded juice.py runs from the playbook and prints 'juice caps hold'; the builder mutated each of 12 caps in a copy and the asserts caught all 12, and fixed a NaN shake and a 1-frame restart that defeated the 1 s cap; indexed in the UI index; test_docs green` → engine API notes (Phaser shake default, Godot timers, Unity WaitForSecondsRealtime) are from memory and marked as such; kick plus shake within 2% is a reviewer check, not code [tree ce052b1016cd] (2026-10-22T18:12:38Z)
- (audit maintainer) `self: the embedded juice.py runs from the playbook and prints 'juice caps hold'; the builder mutated each of 12 caps in a copy and the asserts caught all 12, and fixed a NaN shake and a 1-frame restart that defeated the 1 s cap; indexed in the UI index; test_docs green` → points to motion.md for tokens and reduced motion; T-1505 will run embedded python blocks so this one can't rot [tree ce052b1016cd] (2026-10-22T18:12:38Z)
- (audit self) `self: the embedded juice.py runs from the playbook and prints 'juice caps hold'; the builder mutated each of 12 caps in a copy and the asserts caught all 12, and fixed a NaN shake and a 1-frame restart that defeated the 1 s cap; indexed in the UI index; test_docs green` → no findings [tree ce052b1016cd] (2026-10-22T18:12:38Z)
## Log
- 2026-10-22T17:36:11Z created
- 2026-10-22T18:05:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1493.builder.md
- 2026-10-22T18:06:01Z focused
- 2026-10-22T18:12:21Z merged worktree-agent-ad6a44cdb622f0659 (1 file(s))
- 2026-10-22T18:12:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad6a44cdb622f0659
- 2026-10-22T18:12:21Z focused
- 2026-10-22T18:12:22Z set scope=['plugin/skills/playbooks/references/ui/game-feel.md', 'plugin/skills/playbooks/references/ui/INDEX.md', 'CHANGELOG.md']
- 2026-10-22T18:12:37Z scope: the earlier failed evidence run called the builder's checker without its file argument; the embedded juice.py then ran green
- 2026-10-22T18:12:39Z done
- 2026-10-22T18:12:40Z committed aea55198 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1492 [FEATURE M, done, 2 steps] Motion playbook: choreography, timing and reduced motion — lesson: Sibling playbooks need one stated precedence rule where their number…
- T-1504 [FEATURE M, planned, 1 steps] Communication and ops playbooks: incidents, observability, data-viz, docs, decks, scrollytelling, demos, sound
- T-1500 [FEATURE S, done, 1 steps] UI playbook: visual QA with screenshots and receipts — lesson: A playbook that ships a script should be run against a clean and a broke…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- similar finished tasks took 1–2 steps
## Why not caught
new playbook
## Lessons
- Asserts in an embedded snippet should check the playbook's table, not the snippet's own constants, or a drift passes.
## Files touched
- plugin/skills/playbooks/references/ui/game-feel.md
- CHANGELOG.md
- plugin/skills/playbooks/references/ui/INDEX.md
