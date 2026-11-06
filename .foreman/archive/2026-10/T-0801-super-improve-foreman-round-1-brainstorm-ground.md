---
id: T-0801
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-14T16:01:40Z
updated: 2026-10-14T16:01:51Z
base: cfeff7118aeaa168486249a8796b8fe6c9c9cb66
base_tree: 049246abcba9ac7f8823573593c0a932656295f7
verified: strong
---
# Super-improve Foreman round 1: brainstorm, ground and queue (CC-feature integration)
## Raw request
> Super-improve Foreman round 1: brainstorm, ground and queue (CC-feature integration)
## Interpretation
Recreates T-0760/T-0800 (their checks named a missing command and a transient queue entry). Super-mode brainstorm on Foreman weighted to unused Claude Code features plus the user's inbox asks; every cluster grounded; build marks queued; catalogue page published.
## Assumptions (confidence)
## Acceptance criteria
- [x] catalogue recorded and the slate decision logged — verify with `test -s state/projects/foreman-4a056f/research/brainstorm-20261014.md && grep -q 'T-0775..T-0786' state/projects/foreman-4a056f/decisions.md`
## Non-goals
## Approach (options → choice → why)
Options: lens-only brainstorm; grounded CC inventory then fm ideas super mode; hand-pick. Chose inventory + super mode: brainstormers can't see the harness.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Inventory, fan out, cluster, ground, score
2. [x] Record catalogue, intake slate, publish the picks page
## Resume here
## Docs impact
none: research and state only
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261014-103619/ideas.md && grep -c '^## \[' state/projects/foreman-4a056f/research/brainstorm-20261014.md` → exit 0 · 30 [ran] [tree 049246abcba9] (2026-10-14T16:01:46Z)
- (step 2) `grep -c 'Later from T-0760' state/projects/foreman-4a056f/INBOX.md; test -s state/projects/foreman-4a056f/research/claude-code-features-20261014.md` → exit 0 · 13 [ran] [tree 049246abcba9] (2026-10-14T16:01:46Z)
- (ac 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261014.md && grep -q 'T-0775..T-0786' state/projects/foreman-4a056f/decisions.md` → exit 0 · (no output) [ran] [tree 049246abcba9] (2026-10-14T16:01:51Z)
- (audit intent) `self: every one of 609 ideas sits in exactly one of 30 clusters (clusters.py check), each cluster grounded by grep/read with file:line, scored and marked; 12 build briefs intaken, 13 later clusters captured, 3 skips carry reasons; catalogue page published with a picks db (list returned empty, as expected)` → the user asked for better Claude Code integration and more capability; 9 of 12 build briefs adopt a native feature (monitors, PushNotification, ReportFindings, sessionTitle, hook if, updatedToolOutput, agent effort, version check, Artifact page) and the 5 inbox asks were answered or queued [tree 049246abcba9] (2026-10-14T16:01:51Z)
- (audit operator) `self: every one of 609 ideas sits in exactly one of 30 clusters (clusters.py check), each cluster grounded by grep/read with file:line, scored and marked; 12 build briefs intaken, 13 later clusters captured, 3 skips carry reasons; catalogue page published with a picks db (list returned empty, as expected)` → the user sees every idea and can Build/Veto any cluster on the page; picks are read back with ArtifactData list 'picks' [tree 049246abcba9] (2026-10-14T16:01:51Z)
## Log
- 2026-10-14T16:01:40Z created
- 2026-10-14T16:01:40Z focused
- 2026-10-14T16:01:51Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0800 [RESEARCH M, dropped, 2 steps] Super-improve Foreman: brainstorm, ground and queue (CC-feature integration)
- T-0760 [RESEARCH M, dropped, 3 steps] Super-improve Foreman: brainstorm, ground and queue (CC-feature integration)
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
- research mission-20261014-103352: Request: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. …
## Lessons
- a criterion's verify must check something durable (a file, a decision line), never a transient state like queue membership or a command not verified to exist
