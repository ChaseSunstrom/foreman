---
id: T-1488
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/design-direction.md, plugin/skills/playbooks/SKILL.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:09Z
updated: 2026-10-22T17:44:44Z
base: 8172fcf89a55d0b9e4a3f0a5bcd925e5171f5ffc
base_tree: cf434325f22dd63e6571358c6fb6da8e615dff22
plan0_at: 2026-10-22T17:36:58Z
plan0_scope: [plugin/skills/playbooks/references/ui/design-direction.md]
verified: strong
---
# UI playbook: design direction before pixels
## Raw request
> UI playbook: design direction before pixels
## Interpretation
Brainstorm T-1479 cluster 1: Claude's UI work defaults to generic looks. A playbook that makes it choose and write down a point of view first: a bank of distinct directions, a taste-word to knob table ("premium", "playful", "calm" → type, colour, density, motion, radius), a three-question interview for vague asks, an audacity dial (safe/bold/wild), the defaults to avoid, and a DESIGN.md template the choice is saved to. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/design-direction.md has the direction bank, the taste-word table, the interview, the audacity dial, the defaults to avoid and the DESIGN.md template — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/design-direction.md').read(); miss=[s for s in ['## Direction bank','## Taste words','## Interview','## Audacity','## Defaults to avoid','DESIGN.md',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
Options: extend terminal-ui.md (wrong surface); a long essay (unreadable); chosen: one file of tables and numbered rules, 150-250 lines, with an example DESIGN.md filled in for one invented product.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/design-direction.md
2. [x] check each rule is checkable; link frontend/design-systems, frontend/typography
## Resume here
## Docs impact
CHANGELOG.md line; plugin/skills/playbooks/SKILL.md index
## Verification evidence
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/design-direction.md').read(); miss=[s for s in ['## Direction bank','## Taste words','## Interview','## Audacity','## Defaults to avoid','DESIGN.md',] if s not in t]; assert not miss, miss"` → ✗ exit 1 (never ran: no plugin/skills/playbooks/references/ui/design-direction.md) · ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ / FileNotFoundError: [Errno 2] No such file or directory: 'plugin/skills/playbooks/references/ui/design-direction.md' [ran] [tree cf434325f22d] (2026-10-22T17:38:36Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/design-direction.md').read(); miss=[s for s in ['## Direction bank','## Taste words','## Interview','## Audacity','## Defaults to avoid','DESIGN.md',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree 9581979fb82d] (2026-10-22T17:39:53Z)
- (step 2) `grep -c 'fm lib show design-systems\|fm lib show typography' plugin/skills/playbooks/references/ui/design-direction.md` → exit 0 · 3 [ran] [tree 9581979fb82d] (2026-10-22T17:39:55Z)
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/design-direction.md').read(); miss=[s for s in ['## Direction bank','## Taste words','## Interview','## Audacity','## Defaults to avoid','DESIGN.md'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree d3d707304e6e] (2026-10-22T17:44:25Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/design-direction.md').read(); miss=[s for s in ['## Direction bank','## Taste words','## Interview','## Audacity','## Defaults to avoid','DESIGN.md'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree d3d707304e6e] (2026-10-22T17:44:25Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/design-direction.md').read(); miss=[s for s in ['## Direction bank','## Taste words','## Interview','## Audacity','## Defaults to avoid','DESIGN.md'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree d3d707304e6e] (2026-10-22T17:44:26Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/design-direction.md').read(); miss=[s for s in ['## Direction bank','## Taste words','## Interview','## Audacity','## Defaults to avoid','DESIGN.md',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree d3d707304e6e] (2026-10-22T17:44:34Z)
- (audit intent) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → a written point of view before pixels: interview, taste words to five knobs, 12 directions, audacity dial, defaults to avoid, DESIGN.md [tree d3d707304e6e] (2026-10-22T17:44:34Z)
- (audit edge) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → example palette contrast 12.99/5.17/7.62 verified; under full autonomy the interview is answered from the repo and marked assumed [tree d3d707304e6e] (2026-10-22T17:44:34Z)
- (audit maintainer) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → motion values defer to motion.md's tokens and ceiling; scene-3d and terminal-ui don't overlap [tree d3d707304e6e] (2026-10-22T17:44:34Z)
- (audit operator) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → indexed in SKILL.md's UI section (renamed to cover design, motion and 3D) [tree d3d707304e6e] (2026-10-22T17:44:34Z)
- (audit intent) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → a written point of view before pixels: interview, taste words to five knobs, 12 directions, audacity dial, defaults to avoid, DESIGN.md [tree d3d707304e6e] (2026-10-22T17:44:41Z)
- (audit edge) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → example palette contrast 12.99/5.17/7.62 verified; under full autonomy the interview is answered from the repo and marked assumed [tree d3d707304e6e] (2026-10-22T17:44:41Z)
- (audit maintainer) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → motion values defer to motion.md's tokens and ceiling; scene-3d and terminal-ui don't overlap [tree d3d707304e6e] (2026-10-22T17:44:41Z)
- (audit operator) `builder wrote it (218 lines) from the brief; one fm-reviewer pass over the three UI playbooks: contrast figures recomputed correct, cards exist; its nits for this file fixed (Gallery under motion.md's 500 ms ceiling, word-vs-dial precedence, a knobs-in-range check, a concrete token grep); test_docs green with the index lines` → indexed in the playbooks skill's UI section (renamed to cover design, motion and 3D) [tree d3d707304e6e] (2026-10-22T17:44:41Z)
## Log
- 2026-10-22T17:36:09Z created
- 2026-10-22T17:36:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1488.builder.md
- 2026-10-22T17:36:58Z focused
- 2026-10-22T17:40:31Z merged worktree-agent-a2f0de4d2cb8a65f8 (1 file(s))
- 2026-10-22T17:40:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2f0de4d2cb8a65f8
- 2026-10-22T17:40:31Z focused
- 2026-10-22T17:40:57Z set scope=['plugin/skills/playbooks/references/ui/design-direction.md', 'plugin/skills/playbooks/SKILL.md', 'CHANGELOG.md']
- 2026-10-22T17:40:57Z scope: SKILL.md also indexes T-1494's merged scene-3d.md, or test_docs fails on it
- 2026-10-22T17:41:04Z scope: SKILL.md also indexes T-1492's merged motion.md
- 2026-10-22T17:44:20Z steer: review nits (T-1488/92/94 review): Gallery motion capped at motion.md's 500 ms ceiling, taste word vs audacity precedence stated, a knobs-in-range check, the token grep reworded
- 2026-10-22T17:44:43Z done
- 2026-10-22T17:44:44Z committed 329256b6 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1489 [FEATURE M, planned, 2 steps] UI playbook: type and colour
- T-1493 [FEATURE S, planned, 1 steps] Motion playbook: game feel with intensity caps
- T-1492 [FEATURE M, planned, 2 steps] Motion playbook: choreography, timing and reduced motion
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
## Why not caught
new playbook
## Lessons
- A playbook's acceptance check proves headings, not quality: pair every writing task with one reviewer pass on accuracy and cross-file consistency.
## Files touched
- plugin/skills/playbooks/references/ui/design-direction.md
- CHANGELOG.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/ui/scene-3d.md
