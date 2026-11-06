---
id: T-0899
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T16:45:27Z
updated: 2026-10-15T18:05:47Z
base: f7a22df80e0231e426808b2430fee7005e0515c9
base_tree: 7437f9fb679f2a26f9ccac2ac6dc21b028868daf
verified: strong
---
# A final reply's own promises (I'll also…, I'll follow up on…) become inbox items so they aren't lost
## Raw request
> FEATURE: The Stop hook captures Claude's own promises in a final reply (I'll also…, next I'll…, I'll follow up…) so they aren't lost
> CONTEXT: round 6 #9
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a promise in a reply that ends the turn is captured once; a reply without one captures nothing — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_hooks Stop, then capture_promises in fmcli called from stop()
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks test_friction` → exit 0 · Ran 162 tests in 28.4s (22 classes, 16 at a time; slowest: Stop 28s, PreToolUse 14s, Approvals 11s) / OK [ran] [tree d99d80115296] (2026-10-15T18:02:11Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 150 tests in 27.9s (20 classes, 16 at a time; slowest: Stop 28s, PreToolUse 14s, Approvals 11s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d99d80115296] (2026-10-15T18:03:07Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 150 tests in 27.5s (20 classes, 16 at a time; slowest: Stop 27s, PreToolUse 14s, Approvals 11s) / OK [ran] [tree d99d80115296] (2026-10-15T18:03:07Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 150 tests in 27.7s (20 classes, 16 at a time; slowest: Stop 28s, PreToolUse 14s, Approvals 11s) / OK [ran] [tree d99d80115296] (2026-10-15T18:05:46Z)
- (audit self) `self review: a narrow regex (I'll / I will + also, later, follow up on|with, come back to, circle back to, get to); only when the turn really ends (no hold, not a one-off session); code blocks ignored; deduped against open briefs' titles; the systemMessage names the captured ids` → no findings [tree d99d80115296] (2026-10-15T18:05:46Z)
## Log
- 2026-10-15T16:45:27Z created
- 2026-10-15T16:45:31Z set tier=S
- 2026-10-15T18:00:24Z planned from capture
- 2026-10-15T18:00:24Z focused
- 2026-10-15T18:05:46Z done
- 2026-10-15T18:05:47Z committed a3ed938 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0383 [FEATURE M, done, 3 steps] Reorganize/reorder tasks that are related/depend/implement things others might need/build — lesson: A builder lane plus one review roun…
- research brainstorm-round6-20261015: Probe: `fm ideas` with user value + bold bets, 2 rounds, past every earlier ideas.md (brainstorm-20261015-113737): 49 new titles, ea…
- research mission-20261015-083935: Request: can you keep going? super super improve? recursively? genuinely, make it THE plugin, everything, etc. [stale: plugin/lib/fmamb…
- decision 2026-10-15: Round 6 slate: 6 builds from 49 grounded ideas (salvage on drop, research closes with a decision, fm spec from the user's examples, fm at, promise c…
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
