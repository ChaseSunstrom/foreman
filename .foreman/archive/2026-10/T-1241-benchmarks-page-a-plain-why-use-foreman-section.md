---
id: T-1241
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T19:28:22Z
updated: 2026-10-16T19:45:07Z
base: 8fa85158fc48ec099e9e85a48ef4f3e77f2ab53c
base_tree: 7bbe310de2ac93257a13e9e51bae5925d0ddd0c9
plan0_at: 2026-10-16T19:43:30Z
plan0_scope: []
verified: strong
---
# Benchmarks page: a plain 'Why use Foreman' section that leads with the measured safety res
## Raw request
> Benchmarks page: a plain 'Why use Foreman' section that leads with the measured safety result and says what the quality runs can and can't show
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Benchmarks page opens with a plain 'Why use Foreman' section: safety result first, then what the quality runs can and can't show — verify with `cd plugin/tests && python3 -m unittest test_docs.Site`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Write the section in pages.py; a test that it leads the page
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 35 tests in 1.3s (12 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree 6dd9858c91a7] (2026-10-16T19:44:25Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_docs.Site` → exit 0 · Ran 3 tests in 0.027s / OK [ran] [tree 6dd9858c91a7] (2026-10-16T19:44:26Z)
- (audit intent) `self: claims checked against site/data/bench.json (20 deny, 4 saved, 25 everyday allowed; force-push, ssh key read, npm publish all in the set) and the published duel numbers; screenshot at 1280 px reviewed` → answers the user's 'why would anyone use it' with measured facts and the honest limit [tree 6dd9858c91a7] (2026-10-16T19:44:26Z)
- (audit self) `self: claims checked against site/data/bench.json (20 deny, 4 saved, 25 everyday allowed; force-push, ssh key read, npm publish all in the set) and the published duel numbers; screenshot at 1280 px reviewed` → no findings [tree 6dd9858c91a7] (2026-10-16T19:44:26Z)
## Log
- 2026-10-16T19:28:22Z created
- 2026-10-16T19:43:29Z focused
- 2026-10-16T19:45:06Z done
- 2026-10-16T19:45:07Z committed b6f06e0e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1222 [FEATURE L, done, 3 steps] Benchmarks page: Foreman against plain Claude Code (and other plugins) on real tasks, published with the method — lesson: Validate a be…
- T-1220 [FEATURE L, planned, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history
- T-1231 [PERFORMANCE L, planned, 5 steps] Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time
- decision 2026-09-26: rounds 4-6 slate: 4 safety items, 4 workflow items, 2 measured perf items (research brainstorm-20260926-slate); run inside T-0018 so one core grant …
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
## Regression test
test_docs.Site.test_the_benchmarks_page_opens_with_why_use_foreman: red before the section, green after
## Files touched
- plugin/tests/test_docs.py
- site/pages.py
- CHANGELOG.md
