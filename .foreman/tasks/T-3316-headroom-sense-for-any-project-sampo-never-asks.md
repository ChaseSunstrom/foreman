---
id: T-3316
type: FEATURE
tier: M
status: planned
priority: normal
scope: [plugin/lib/sampo/headroom.py, plugin/tests/test_headroom.py, plugin/lib/fmheadroom.py, MASTER.md, docs/map]
depends_on: []
source: user
created: 2026-11-06T04:20:48Z
updated: 2026-11-06T04:31:03Z
---
# Headroom part 1: census of a project's fixed sets and caps, plus caps raised by hand (T-3316)
## Raw request
> Headroom sense, for any project: Sampo never asks 'do we want more than this?'. Kalevala's 26 towers are coverage.md's open rows (written once by a gen-1 seed) plus 3 fixed; nothing ever proposes a new aspect, so the set can only shrink. Same shape everywhere: missions <=8, 5 audit lenses, ideas lenses, moon areas, K slots, BUILDERS_MAX, budgets, card targets. Build a general headroom pass: (1) census of every bounded set and cap the project works with, found from code and data (constants, fixed tuples, slices, grid rows), not a hand list; (2) per set, measure binding (how often the cap is hit) and orphans (captures, steers, failures, ideas, user messages that map to no member); (3) a 'what would a complete version have that this lacks' pass against the goal, local model first; (4) when a cap binds or orphans cluster, propose growth as a task, and for Kalevala open the new tower itself (gen N chooses the tower set: births as well as keeps); (5) the turn-end self-checks (T-3123) gain 'closed set / binding cap'. Works in any repo Sampo runs in. User: 'why are you not able to recognize/come up with improvements to the framework... only 26 tower ideas... fully self aware, and again, not specific to Sampo'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] census(root) lists module-level UPPER_CASE ints >=2 used as caps (compared, min/max, slice bound) and UPPER tuples/lists of >=3 strings, via ast for .py and a one-line regex for other languages; raised(root) reads one git log -p -U0 over 180 days and counts how often each cap's value went up; a fixture repo's raised cap shows raised=2, its name tuple is listed, a bare TIMEOUT used only in sleep() is not — verify with `python3 plugin/tests/run.py test_headroom`
- [ ] runs in under 3 s on this repo and never in a hook — verify with `python3 plugin/tests/run.py test_headroom`
## Non-goals
## Approach (options → choice → why)
1) ast scan + one git log: exact, cheap, works on any Python repo, regex fallback for others. 2) model reads the repo: costly, unrepeatable. 3) hand registry: goes stale, the user rejected hand lists. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fixture repo test, red  <- CURRENT
2. [ ] census via ast plus regex fallback
3. [ ] raised caps from one git log
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:20:48Z created
- 2026-11-06T04:31:02Z planned from capture
## Follow-ups captured
