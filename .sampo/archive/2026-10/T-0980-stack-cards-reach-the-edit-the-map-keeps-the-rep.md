---
id: T-0980
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T22:20:40Z
updated: 2026-10-15T22:21:21Z
base: bbd5ee15da9a281321712b4533ce3d59e06bf76e
base_tree: f97681da396bfcf9bd8d0c3f184ed91f909e0f54
verified: strong
---
# Stack cards reach the edit: the map keeps the repo's language cards beyond the top 8
## Raw request
> Stack cards reach the edit: the map keeps the repo's language cards beyond the top 8
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm map's lib_cards keep every language card the repo's files match even when 8 framework/tool cards outrank them, so a .py edit in a repo whose top 8 are tool cards injects the python card — verify with `python3 plugin/tests/run.py -k LangCardsKept`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing LangCardsKept test
2. [x] for_map keeps language cards; map VERSION bump
## Resume here
## Docs impact
MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k LangCardsKept` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: LangCardsKept 0s) / FAILED (1 classes) [ran] [tree c432b3564e5e] (2026-10-15T22:20:55Z)
- (step 2) `python3 plugin/tests/run.py test_edit_cards test_library test_map` → exit 0 · Ran 32 tests in 4.5s (14 classes, 16 at a time; slowest: EditCards 4s, Map 2s, EditCardsReview 2s) / OK [ran] [tree 9ef7ac80ffa3] (2026-10-15T22:21:19Z)
- (ac 1) `python3 plugin/tests/run.py -k LangCardsKept` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: LangCardsKept 0s) / OK [ran] [tree 34abfbd139ae] (2026-10-15T22:21:20Z)
- (step 1) `python3 plugin/tests/run.py -k LangCardsKept` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: LangCardsKept 0s) / OK [ran] [tree 34abfbd139ae] (2026-10-15T22:21:20Z)
- (audit self) `self: red then green on LangCardsKept; the rebuilt live map now holds bash and python` → language cards survive a crowded top 8; map VERSION 7 rebuilds old maps [tree 34abfbd139ae] (2026-10-15T22:21:20Z)
## Log
- 2026-10-15T22:20:40Z created
- 2026-10-15T22:20:45Z focused
- 2026-10-15T22:21:20Z done
- 2026-10-15T22:21:21Z committed 02c5c26 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0976 [FIX S, dropped, 0 steps] Stack cards reach the edit: the map's lib_cards always keep the repo's language cards (bey
- T-0949 [FEATURE M, done, 4 steps] Enforce: the right stack card's pitfalls injected at edit time, and a compliance count — lesson: A ranking rule (framework before langu…
- T-0939 [FEATURE M, done, 3 steps] Pane shows skill use: skills invoked, stack cards read, and this repo's suggested cards — lesson: A mechanical sed over JSX props must …
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar past tasks were M: consider --tier M
## Plan gaps
- failed first: step 1 Failing LangCardsKept test
## Files touched
- plugin/tests/test_edit_cards.py
- plugin/lib/fmlib.py
- plugin/lib/fmmap.py
- MASTER.md
