---
id: T-1479
type: RESEARCH
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-22T16:56:54Z
updated: 2026-10-22T17:40:02Z
verified: weak
---
# Super recursive brainstorm and improve foreman, way more skills/playbooks/way better more
## Raw request
> super recursive brainstorm and improve foreman, way more skills/playbooks/way better more capable code, config in the tui, etc. etc. fully featutred, etc. way better/way more UI design skills with 3d, good animations, non generic stuff, styles, etc. etc.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
none here: the catalogue is research saved with fm research add (brainstorm-20261022-catalogue); each build task carries its own docs
## Verification evidence
- (audit self) `every one of 548 ideas grounded by three fm-recon passes (ids in exactly one cluster each), clusters merged and scored` → 26 capabilities; 24 build in two rounds, 2 skip groups with reasons [tree cf434325f22d] (2026-10-22T17:39:09Z)
- (audit maintainer) `catalogue recorded under research/ with every id; round 2 captured as T-1507..T-1519; checklist page reads choices back through its db` → ok: nothing dropped silently [tree cf434325f22d] (2026-10-22T17:39:16Z)
- (audit edge) `ideas whose near-T match was word overlap; wild ideas judged by title` → the recon passes marked confidence; wild ideas kept in the catalogue as skipped with reasons, never dropped [tree cf434325f22d] (2026-10-22T17:39:22Z)
- (audit operator) `the user sees the catalogue page with every cluster and can change any mark` → https://claude.ai/artifact/LuGBHwnkXptm1PUrDrT49w; choices land in its db collection marks [tree cf434325f22d] (2026-10-22T17:39:22Z)
- (audit intent) `the slate covers each part of the ask: skills/playbooks (clusters 1-3, 10, 11), more capable code (4, 11, 22), config in the TUI (5, 6, 15, 16), UI design with 3D, motion, styles (1-4, 7, 8, 9, 18)` → every part of the request has round-1 work [tree cf434325f22d] (2026-10-22T17:39:28Z)
- (audit adversary) `brainstorm content treated as data; ideas that would weaken the guard, run third-party code unguarded (a Figma MCP) or add runtime dependencies were skipped with reasons` → held: no slate item weakens the guard [tree cf434325f22d] (2026-10-22T17:39:28Z)
## Log
- 2026-10-22T16:56:54Z created
- 2026-10-22T17:39:38Z done
- 2026-10-22T17:39:42Z done
## Follow-ups captured
## Decision
Slate: round 1 = T-1488..T-1506 (19 tasks over clusters 1-11), round 2 = T-1507..T-1519 (clusters 12-24); skipped: clusters 25-26 (built already, or heavy/speculative: browser or GPU stacks, new dependencies, live servers). Why: the user asked for skills, playbooks, UI craft with 3D and motion, and config in the TUI; those clusters scored value 4-5 at S-M effort and low risk, grounded as new. Catalogue: research/brainstorm-20261022-catalogue.md; checklist: https://claude.ai/artifact/LuGBHwnkXptm1PUrDrT49w
## Lessons
- A 548-idea run grounds well split by position into three fm-recon batches with ids that must each land in one cluster; merging clusters across batches is the main session's job. Tell playbook builders to report their index line instead of editing the shared SKILL.md.
