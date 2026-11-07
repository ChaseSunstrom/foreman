---
id: T-0760
type: RESEARCH
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T15:33:49Z
updated: 2026-10-14T15:57:05Z
base: 4a9bf49a329a62d797e24dacdb67306687aa8570
base_tree: 9fbf7df9dd3f3f007b3ac68a2b68b13199490a6d
---
# Super-improve Foreman: brainstorm, ground and queue (CC-feature integration)
## Raw request
> super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. etc.
## Interpretation
Super-mode brainstorm on Foreman itself, weighted to Claude Code features Foreman doesn't use yet (Artifact pages, Monitor/ScheduleWakeup/Cron, PushNotification, agent effort/model/worktree isolation, ReportFindings, plugin eval, mods) plus the 5 inbox items the user already asked; ground every cluster, turn build marks into briefs.
## Assumptions (confidence)
## Acceptance criteria
- [ ] catalogue recorded and slate queued — verify with `fm research list | grep -q brainstorm-2026101`
## Non-goals
## Approach (options → choice → why)
Options: (a) brainstorm only from lenses; (b) grounded CC-feature inventory first, then fm ideas super mode; (c) skip brainstorm, hand-pick. Choice: b — the user named new CC features, and brainstormers can't see the harness, so the pack must list them.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Inventory CC features vs Foreman use; extend the pack
2. [x] Fan out fm ideas (super mode)
3. [x] Cluster, ground, score; record; intake the slate
## Resume here
<!-- auto -->
- 2026-10-14T15:37:14Z step 1/3: Inventory CC features vs Foreman use; extend the pack
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/cc-features.md
## Docs impact
## Verification evidence
- (step 1) `grep -rl 'ScheduleWakeup\|PushNotification\|ReportFindings\|EnterWorktree' plugin/ | wc -l` → exit 0 · 0 [ran] [tree 82c6f888d49e] (2026-10-14T15:47:38Z)
- (step 1) `grep -rn 'Monitor\|CronCreate' plugin/lib plugin/hooks 2>/dev/null | wc -l` → exit 0 · 1 [ran] [tree 82c6f888d49e] (2026-10-14T15:47:39Z)
- (step 2) `ls state/projects/foreman-4a056f/research/brainstorm-20261014-104747/r2-*.md | wc -l` → exit 0 · 8 [ran] [tree 82c6f888d49e] (2026-10-14T15:49:06Z)
- (step 3) `grep -c '^- ' state/projects/foreman-4a056f/research/brainstorm-20261014-104747/ideas.md && fm task show T-0769 >/dev/null && echo captured` → exit 0 · 306 / captured [ran] [tree 82c6f888d49e] (2026-10-14T15:49:20Z)
- (ac 1) `fm research list | grep -q brainstorm-2026101` → ✗ exit 1 · usage: fm research [-h] [--json] [-p PROJECT] {add,ask} ... / fm research: error: argument research_cmd: invalid choice: 'list' (choose from 'add', 'ask') [ran] [tree 82c6f888d49e] (2026-10-14T15:49:24Z)
- (ac 1) `fm research list | grep -q brainstorm-2026101` → ✗ exit 1 · usage: fm research [-h] [--json] [-p PROJECT] {add,ask} ... / fm research: error: argument research_cmd: invalid choice: 'list' (choose from 'add', 'ask') [ran] [tree 82c6f888d49e] (2026-10-14T15:49:32Z)
- (ac 1) `fm research list | grep -q brainstorm-2026101` → ✗ exit 1 · usage: fm research [-h] [--json] [-p PROJECT] {add,ask} ... / fm research: error: argument research_cmd: invalid choice: 'list' (choose from 'add', 'ask') [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:56:57Z)
## Log
- 2026-10-14T15:33:49Z created
- 2026-10-14T15:34:22Z planned from capture
- 2026-10-14T15:34:22Z focused
- 2026-10-14T15:39:20Z paused: focus moved to T-0761
- 2026-10-14T15:47:28Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-14T15:47:28Z focused
- 2026-10-14T15:49:36Z blocked: AC 1 uses 'fm research list', which doesn't exist (fm research has add|ask), and its evidence can't be edited. Step 3 is done: slate T-0769..T-0772 captured. Fix: add a corrected criterion or drop and recreate T-0760.
- 2026-10-14T15:54:04Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-14T15:54:04Z focused
- 2026-10-14T15:57:05Z dropped: criterion 1's verify named 'fm research list', which doesn't exist (T-0765's lint would have caught it); recreated with a working check
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- research mission-20261014-103352: Request: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. …
- research mission-20261014-103352.pack: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. etc.
- decision 2026-10-09: [costly] Build all 70 'build' capabilities from the Foreman brainstorm in value-for-effort rounds (security first); the user's ticks on the punch li…
