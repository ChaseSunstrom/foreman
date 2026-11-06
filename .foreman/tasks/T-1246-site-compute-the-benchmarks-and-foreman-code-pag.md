---
id: T-1246
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T21:06:17Z
updated: 2026-10-20T13:55:17Z
group: theme applied before first paint
base: 61306fef779fec15b15236e53cc840462ab575d2
base_tree: 3fea8d053ada0489e52606a7717831b7dfff926a
plan0_at: 2026-10-20T13:52:38Z
plan0_scope: []
verified: strong
---
# Site: prose figures computed from stats.json, and the saved theme applied before first paint
## Raw request
> Site: compute the Benchmarks and Foreman Code pages' prose figures (24/20/4/25, 10%/29%, 52/9) from stats.json, or pin them in a test, so they can't drift from the charts; and apply the stored theme before first paint (a stored light theme flashes dark)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the why-section and Foreman Code figures come from the data (a changed stats.json changes the text), and the theme is set in <head> — verify with `cd plugin/tests && python3 -m unittest test_docs.Site`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Callable text blocks; _why(s) from safety and the duels (long runs over every long duel); Foreman Code counts in stats.py; theme script in head
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_docs.Site` → exit 0 · Ran 11 tests in 0.055s / OK [ran] [tree ca867906271e] (2026-10-20T13:54:31Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_docs.Site` → exit 0 · Ran 11 tests in 0.054s / OK [ran] [tree ca867906271e] (2026-10-20T13:54:32Z)
- (audit intent) `self: _why tested on synthetic stats (every figure moves with the data) and on the real stats; theme script checked in the rendered head` → figures can no longer drift from the charts; the one that had drifted (52) now reads 51 [tree ca867906271e] (2026-10-20T13:54:32Z)
- (audit self) `self: _why tested on synthetic stats (every figure moves with the data) and on the real stats; theme script checked in the rendered head` → no findings [tree ca867906271e] (2026-10-20T13:54:32Z)
## Log
- 2026-10-16T21:06:17Z created
- 2026-10-20T13:52:36Z planned from capture
- 2026-10-20T13:52:37Z focused
- 2026-10-20T13:55:16Z done
- 2026-10-20T13:55:17Z committed ba12f467 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1220-review: Changes needed. Nothing is critical. Three MEDIUM defects are worth fixing before the next publish. I read the code and the data files and did no…
- T-1206 [FEATURE M, done, 3 steps] A GitHub Pages site for Foreman: one modern page with the real demo, the loop, the guard and install — lesson: A marketing page for a d…
- research T-1242-review: Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported. [stale: plugin/lib/fmc…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
## Behaviour lock
test_docs.Site ran green before the first edit; the existing why-section words (24 dangerous, both sides pass, 6 of 6, 3 of 6, compact) still hold, now computed from site/data
## Files touched
- plugin/tests/test_docs.py
- site/build.py
- site/pages.py
- site/stats.py
- site/data/stats.json
- CHANGELOG.md
