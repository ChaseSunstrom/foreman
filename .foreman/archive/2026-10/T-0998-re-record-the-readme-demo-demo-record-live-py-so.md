---
id: T-0998
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T00:03:49Z
updated: 2026-10-16T01:31:12Z
inferred_deps: [T-1002]
inferred_why: T-1002: re-record the demo after the pane layout changes
group: foreman-ui pane work
base: 75d559b8c152621da758e33659335e77ab1aa6fa
base_tree: 8387d0e34f9f9f58dc9d275158d64c25d9479928
verified: strong
---
# Re-record the README demo with the remade pane
## Raw request
> Re-record the README demo (demo/record_live.py) so it shows the one-panel pane from T-0989, not the old bordered cards
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] demo/live.svg and demo/live.mp4 re-rendered from a new real session showing the 0.11 pane; README caption matches — verify with `test demo/live.svg -nt mods/foreman-ui/hooks/register.tsx`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] record a real session on a small task in a scratch clone
2. [x] check frames read well; README caption
## Resume here
## Docs impact
README.md
## Verification evidence
- (step 1) `test -s demo/live.mp4 && test -s demo/live.svg && test -s demo/live.cast` → exit 0 · (no output) [ran] [tree 65d4891208e4] (2026-10-16T01:31:03Z)
- (step 2) `grep -q 'T-1009' README.md` → exit 0 · (no output) [ran] [tree 65d4891208e4] (2026-10-16T01:31:04Z)
- (ac 1) `test demo/live.svg -nt mods/foreman-ui/hooks/register.tsx` → exit 0 · (no output) [ran] [tree 65d4891208e4] (2026-10-16T01:31:04Z)
- (audit operator) `self` → frames at 10/30/50/65 s read well: plan → test-first → red/green → close with the done strip; scrubbed (home path shown as /tmp clone only); caption and alt match [tree 65d4891208e4] (2026-10-16T01:31:04Z)
- (ac 1) `test demo/live.svg -nt mods/foreman-ui/hooks/register.tsx` → exit 0 · (no output) [ran] [tree 65d4891208e4] (2026-10-16T01:31:11Z)
- (audit operator) `frames reviewed; no name, e-mail or home path in the cast (grep); caption and alt rewritten` → the README shows the 0.11 pane doing a real task end to end [tree 65d4891208e4] (2026-10-16T01:31:11Z)
- (audit self) `frames reviewed; no name, e-mail or home path in the cast (grep); caption and alt rewritten` → no findings [tree 65d4891208e4] (2026-10-16T01:31:11Z)
## Log
- 2026-10-16T00:03:49Z created
- 2026-10-16T01:12:17Z planned from capture
- 2026-10-16T01:12:18Z focused
- 2026-10-16T01:18:52Z paused: focus moved to T-1010
- 2026-10-16T01:25:35Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T01:25:35Z focused
- 2026-10-16T01:26:01Z paused: focus moved to T-1011
- 2026-10-16T01:29:54Z demo files (live.cast/svg/mp4) landed in T-1011's commit 9fab934: its close swept the recorder's output; history left as is
- 2026-10-16T01:30:51Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T01:30:51Z focused
- 2026-10-16T01:31:11Z done
- 2026-10-16T01:31:12Z committed e171ab0 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0999 [FEATURE M, dropped, 0 steps] Demo/live.svg` still draws the old bordered cards, and the README caption now misdescribes
- research T-0989-review: Verdict:** changes needed. The row budget holds. There is one functional regression (plan approval) and two housekeeping misses (version, types).…
- T-0938 [FIX M, done, 3 steps] Pane stays put: volatile cards hold their height and linger instead of popping in and out — lesson: Layout stability is a time property: te…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar past tasks were M: consider --tier M
## Files touched
- README.md
