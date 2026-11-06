---
id: T-0908
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T18:42:19Z
updated: 2026-10-15T19:06:40Z
base: d289d774b347849c248bf9f76fbbd1acb3fedbd6
base_tree: 91ec9e838e09afe5aab780e63c6d6738700d309d
verified: strong
---
# Promise capture: offers ('if you want, I'll also…'), idioms ('I'll get to the bottom of…') and narration ('I'll also note…') aren't promises; at most 3 per reply; the Stop hook skips fmcli's import when no 'I'll' is said
## Raw request
> Promise capture: offers ('if you want, I'll also…'), idioms ('I'll get to the bottom of…') and narration ('I'll also note…') aren't promises; at most 3 per reply; the Stop hook skips fmcli's import when no 'I'll' is said
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the reviewer's reproducers capture nothing; T-0899's case still captures two — verify with `python3 plugin/tests/run.py -k Stop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing cases in test_hooks Stop, then narrow _PROMISE and its caller
## Resume here
<!-- auto -->
- 2026-10-15T18:43:44Z step 1/1: failing cases in test_hooks Stop, then narrow _PROMISE and its caller
- git: foreman/build; 3 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py
- touched since last checkpoint: plugin/tests/test_hooks.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k Stop` → ✗ exit 1 · Ran 40 tests in 28.2s (1 classes, 16 at a time; slowest: Stop 28s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 658557949162] (2026-10-15T19:06:11Z)
- `python3 plugin/tests/run.py -k Stop` → exit 0 · Ran 40 tests in 27.5s (1 classes, 16 at a time; slowest: Stop 27s) / OK [ran] [tree 658557949162] (2026-10-15T19:06:11Z)
- (ac 1) `python3 plugin/tests/run.py -k Stop` → exit 0 · Ran 40 tests in 27.2s (1 classes, 16 at a time; slowest: Stop 27s) / OK [ran] [tree 658557949162] (2026-10-15T19:06:39Z)
- (step 1) `python3 plugin/tests/run.py -k Stop` → exit 0 · Ran 40 tests in 27.2s (1 classes, 16 at a time; slowest: Stop 27s) / OK [ran] [tree 658557949162] (2026-10-15T19:06:39Z)
- (audit edge) `self: the reviewer's reproducers (get to the bottom, if-you-want offers, would-also, also note, mention…if you like) capture nothing; T-0899's two promises still captured; the Stop hook imports fmcli only when the reply says I'll/I will; lock wait 1 s in the Stop path` → an offer split across sentences ('Want more? I'll also add X.') still counts — the sentence before isn't read; accepted (rare, and the inbox item is visible) [tree 658557949162] (2026-10-15T19:06:39Z)
- (audit self) `self: the reviewer's reproducers (get to the bottom, if-you-want offers, would-also, also note, mention…if you like) capture nothing; T-0899's two promises still captured; the Stop hook imports fmcli only when the reply says I'll/I will; lock wait 1 s in the Stop path` → no findings [tree 658557949162] (2026-10-15T19:06:39Z)
## Log
- 2026-10-15T18:42:19Z created
- 2026-10-15T18:42:19Z focused
- 2026-10-15T18:47:53Z paused: focus moved to T-0909
- 2026-10-15T19:04:42Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T19:04:42Z focused
- 2026-10-15T19:06:39Z done
- 2026-10-15T19:06:40Z committed 34ebe51 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0899 [FEATURE S, done, 1 steps] A final reply's own promises (I'll also…, I'll follow up on…) become inbox items so they aren't lost
- playbook typescript (skills/playbooks/references/review/typescript.md)
- T-0588 [RESEARCH L, done, 3 steps] And maybe a knowledge graph if we dont have it already, and also, better intuition/reasoni — lesson: grounding brainstormers in today'…
- decision 2026-10-15: Round 6 slate: 6 builds from 49 grounded ideas (salvage on drop, research closes with a decision, fm spec from the user's examples, fm at, promise c…
- similar finished tasks took 1–3 steps
- start here (files T-0899 touched): plugin/tests/test_hooks.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
