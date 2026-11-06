---
id: T-2348
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T13:59:19Z
updated: 2026-11-01T07:55:47Z
group: Mission 5 inbox items
base: 01de3ebc0fbba93e42a07fc1bfa39cf646cb0089
base_tree: 0dacdea25ef4bc2e221ac41911619314802df459
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-01T07:46:58Z
plan0_scope: []
verified: strong
---
# Decision tape on the site: fm decide rows with their confidence, door and any later reversal on one scrollable timeline page
## Raw request
> Decision tape on the web UI (Mission 5 inbox, tier 2): fm decide rows with confidence, door and later reversal on one scrollable timeline
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the site's Decisions page lists fm decide rows newest first, each with its confidence, its kind (reversible, costly, outward; a door), and the later row that reversed or revisited it, escaped and with no outside hosts — verify with `python3 plugin/tests/run.py test_site`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] site/stats.py decisions block and site/pages.py page
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site -k test_the_decisions_page` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: DecisionTape 0s) / FAILED (1 classes: test_site.DecisionTape) [ran] [tree c62b11c110e4] (2026-11-01T07:47:11Z)
- (step 2) `python3 plugin/tests/run.py test_site test_docs` → exit 0 · Ran 139 tests in 10.7s (44 classes, 16 at a time; slowest: Fences 10s, Header 5s, DocsProof 5s) / OK [ran] [tree 224e20c13dfe] (2026-11-01T07:48:19Z)
- (ac 1) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 36 tests in 6.2s (20 classes, 16 at a time; slowest: Header 6s, Landing 3s, Session 3s) / OK [ran] [tree 224e20c13dfe] (2026-11-01T07:48:26Z)
- `python3 plugin/tests/run.py test_site -k test_the_decisions_page` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: DecisionTape 0s) / FAILED (1 classes: test_site.DecisionTape) (start tree + this task's tests) [ran] [tree 224e20c13dfe] (2026-11-01T07:48:30Z)
- `python3 plugin/tests/run.py test_site -k test_the_decisions_page` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: DecisionTape 0s) / OK [ran] [tree 224e20c13dfe] (2026-11-01T07:48:30Z)
- (ac 1) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 36 tests in 4.7s (20 classes, 16 at a time; slowest: Header 4s, Landing 2s, Session 1s) / OK [ran] [tree 224e20c13dfe] (2026-11-01T07:55:10Z)
- (audit self) `self: fm check exit 0 (5531 tests); red→green test (rows newest first, kind, confidence, the later reversal, escaped text, the empty render); fm task prove proved; the page loads no outside host (inline style, the site's own helpers)` → no findings [tree 224e20c13dfe] (2026-11-01T07:55:10Z)
## Log
- 2026-10-31T13:59:19Z created
- 2026-11-01T07:32:09Z planned from capture
- 2026-11-01T07:46:57Z focused
- 2026-11-01T07:46:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-01T07:48:30Z scope: site/pages.py and site/stats.py (the page and its block), plugin/tests/test_site.py (the test), MASTER.md and CHANGELOG.md (docs)
- 2026-11-01T07:55:45Z done
- 2026-11-01T07:55:47Z committed 605e22a0 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2160 [FEATURE M, done, 3 steps] Write the steer's standing rules (testing cadence, real coverage, long-horizon tier as… — lesson: Two readers of the same rows (steer_c…
- T-0688 [FEATURE L, done, 7 steps] Milestone: Intelligence — Judgment, taste and decisions — lesson: Judgment improves where it's recorded: doors and precedent as rules a…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- decision 2026-10-30: [revisited: long-horizon tier is the deciding end-of-run score] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run]…
## Lessons
- A site page reads the project's own files through stats.py once at build, so the page code stays pure rendering
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_site.py
- site/stats.py
- site/pages.py
- CHANGELOG.md
- MASTER.md
