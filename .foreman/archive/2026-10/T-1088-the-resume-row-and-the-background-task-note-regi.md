---
id: T-1088
type: FEATURE
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx]
depends_on: []
source: discovered
created: 2026-10-16T04:05:38Z
updated: 2026-10-16T07:55:56Z
base: 1e5f2309d4091d1afff82cede84f65a2db187a34
base_tree: f6a34924c730021f96f7deb02fc0629c8565b970
plan0_at: 2026-10-16T07:53:45Z
plan0_scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx]
verified: ok
---
# The `↻` resume row and the background-task note (`register.tsx:791`, `:822`) are not part
## Raw request
> The `↻` resume row and the background-task note (`register.tsx:791`, `:822`) are not part of the tree, so the rail breaks at them
> (noticed by an agent; research T-1040-review)
## Interpretation
In the chat tree (T-1040), the ↻ resume row (a foreman-ui message) and the background-task note (a task-notification UserMessage) are drawn without branch(), so the rail breaks at them.
## Assumptions (confidence)
## Acceptance criteria
- [x] with the tree on, the ↻ row and the background-task note each draw a ├─ branch and the rail; with chat full they draw no branch — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Wrap both rows in branch() like every other row (head marker, rail beside); off the tree (chat full, desktop) branch returns the row unchanged.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then wrap both rows in branch()
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 117 tests across 1 file. [11.13s] [ran] [tree 88426cce1e6b] (2026-10-16T07:54:55Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 117 tests across 1 file. [11.26s] [ran] [tree 068738d1e7d3] (2026-10-16T07:55:07Z)
- (audit self) `self: both rows go through branch(), which returns the row unchanged off the tree (chat full, desktop), so only the tree view changes; mod suite 117/117` → no findings [tree 068738d1e7d3] (2026-10-16T07:55:07Z)
## Log
- 2026-10-16T04:05:38Z created
- 2026-10-16T07:53:41Z set tier=S
- 2026-10-16T07:53:42Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx']
- 2026-10-16T07:53:44Z focused
- 2026-10-16T07:54:55Z scope: CHANGELOG.md — release note
- 2026-10-16T07:55:56Z done
- 2026-10-16T07:55:56Z committed b679927 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1040-review: Verdict: approve with nits.** I found no HIGH or CRITICAL defects. I read the diff and the surrounding code but ran nothing, so the `claude plugi…
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- decision 2026-10-16: T-1040 self-approved under full autonomy: per-row branches with a rail and compact finished calls, chat setting tree\
- similar past tasks were M: consider --tier M
## Preflight
Changed in scope since this was planned (2026-10-16): mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx; re-ground the plan against them before editing
## Lessons
- Every row the chat tree can show must go through branch(); grep the renderers for a bare return when adding one
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
