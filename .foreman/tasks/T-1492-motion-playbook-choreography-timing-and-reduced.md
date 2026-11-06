---
id: T-1492
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/skills/playbooks/references/ui/motion.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:11Z
updated: 2026-10-22T17:45:22Z
base: a2d9513e14fbee82919ae5a14a69dc27d311d18e
base_tree: c37ccb6da3929e39121888540f6e38179c0d7e92
plan0_at: 2026-10-22T17:37:02Z
plan0_scope: [plugin/skills/playbooks/references/ui/motion.md]
verified: strong
---
# Motion playbook: choreography, timing and reduced motion
## Raw request
> Motion playbook: choreography, timing and reduced motion
## Interpretation
Brainstorm T-1479 cluster 2: good animation is designed: a timing vocabulary (named durations and easings as tokens), a state-to-motion table (enter, exit, move, change, attention, loading), storyboard before code, one orchestrated moment over scattered effects, motion that answers a person's action, compositor-only properties, loading choreography that never blocks first paint, and reduced motion as its own designed path. Foreman's own original writing (no third-party text copied); every rule checkable (a reader can say pass or fail); link the library cards it builds on (fm lib show NAME); do not edit plugin/skills/playbooks/SKILL.md, put the one index line in your report.
## Assumptions (confidence)
## Acceptance criteria
- [x] ui/motion.md has the token vocabulary, the state-to-motion table, storyboarding, compositor rules, loading choreography and reduced motion — verify with `python3 -c "t=open('plugin/skills/playbooks/references/ui/motion.md').read(); miss=[s for s in ['## Timing vocabulary','## State to motion','## Storyboard','## Compositor','## Loading','## Reduced motion',] if s not in t]; assert not miss, miss"`
## Non-goals
## Approach (options → choice → why)
Options: per-library recipes (framer-motion cards already exist); chosen: library-neutral tokens and tables, linking the frontend/animation and web/framer-motion cards for the code.
## Risks and rollback
## Execution prompt
## Steps
1. [x] write ui/motion.md
2. [x] tokens as CSS custom properties and as a JS object, one worked storyboard
## Resume here
## Docs impact
CHANGELOG.md line
## Verification evidence
- (step 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/motion.md').read(); miss=[s for s in ['## Timing vocabulary','## State to motion','## Storyboard','## Compositor','## Loading','## Reduced motion'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree fb7129be8c08] (2026-10-22T17:44:59Z)
- (step 2) `python3 -c "t=open('plugin/skills/playbooks/references/ui/motion.md').read(); miss=[s for s in ['## Timing vocabulary','## State to motion','## Storyboard','## Compositor','## Loading','## Reduced motion'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree fb7129be8c08] (2026-10-22T17:44:59Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/motion.md').read(); miss=[s for s in ['## Timing vocabulary','## State to motion','## Storyboard','## Compositor','## Loading','## Reduced motion'] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree fb7129be8c08] (2026-10-22T17:45:00Z)
- (ac 1) `python3 -c "t=open('plugin/skills/playbooks/references/ui/motion.md').read(); miss=[s for s in ['## Timing vocabulary','## State to motion','## Storyboard','## Compositor','## Loading','## Reduced motion',] if s not in t]; assert not miss, miss"` → exit 0 · (no output) [ran] [tree b5ff009d0bc9] (2026-10-22T17:45:09Z)
- (audit intent) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → motion designed from a cause: tokens, a state table, storyboard, compositor-only, reduced motion as its own path [tree b5ff009d0bc9] (2026-10-22T17:45:09Z)
- (audit edge) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → the line grep misses multi-line lists and JS animate calls; now said, with a JS grep [tree b5ff009d0bc9] (2026-10-22T17:45:09Z)
- (audit maintainer) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → one rule settles design-direction's motion values against these tokens [tree b5ff009d0bc9] (2026-10-22T17:45:09Z)
- (audit operator) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → indexed in the playbooks skill [tree b5ff009d0bc9] (2026-10-22T17:45:09Z)
- (audit intent) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → motion designed from a cause: tokens, a state table, storyboard, compositor-only, reduced motion as its own path [tree b5ff009d0bc9] (2026-10-22T17:45:18Z)
- (audit edge) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → the line grep misses multi-line lists and JS animate calls; now said, with a JS grep [tree b5ff009d0bc9] (2026-10-22T17:45:18Z)
- (audit maintainer) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → one rule settles design-direction's motion values against these tokens [tree b5ff009d0bc9] (2026-10-22T17:45:18Z)
- (audit operator) `builder wrote it; one fm-reviewer pass over the three UI playbooks verified WCAG 2.2.2/2.3.1, transitionend, Framer conventions and the 9 cards; its nits fixed here (tokens follow DESIGN.md's Motion knob under the 500 ms ceiling, the property grep marked a lower bound with a JS check)` → indexed in the playbooks skill [tree b5ff009d0bc9] (2026-10-22T17:45:18Z)
## Log
- 2026-10-22T17:36:11Z created
- 2026-10-22T17:36:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1492.builder.md
- 2026-10-22T17:37:01Z focused
- 2026-10-22T17:41:04Z merged worktree-agent-acafa33fcf8e5d60a (1 file(s))
- 2026-10-22T17:41:04Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acafa33fcf8e5d60a
- 2026-10-22T17:44:49Z focused
- 2026-10-22T17:44:59Z steer: review: tokens derive from DESIGN.md's Motion knob with the 500 ms ceiling; the property grep is a lower bound (multi-line lists, inset, font-size, JS animate)
- 2026-10-22T17:45:08Z set scope=['plugin/skills/playbooks/references/ui/motion.md', 'CHANGELOG.md']
- 2026-10-22T17:45:17Z scope: SKILL.md and design-direction.md edits were T-1488's, committed in 329256b6 while this task waited
- 2026-10-22T17:45:20Z done
- 2026-10-22T17:45:22Z committed 1bc9953b (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1493 [FEATURE S, planned, 1 steps] Motion playbook: game feel with intensity caps
- T-1494 [FEATURE M, planned, 2 steps] 3D playbook: scene composition, budget and survival contract
- T-1500 [FEATURE S, planned, 1 steps] UI playbook: visual QA with screenshots and receipts
- decision 2026-10-16: Recommendation: build the slate T-1042..T-1053 plus T-1028 widened (recorded in research brainstorm-20261016-catalogue); the user then asked for eve…
## Why not caught
new playbook
## Lessons
- Sibling playbooks need one stated precedence rule where their numbers overlap.
## Files touched
- plugin/skills/playbooks/references/ui/motion.md
- CHANGELOG.md
- plugin/skills/playbooks/SKILL.md
- plugin/skills/playbooks/references/ui/design-direction.md
