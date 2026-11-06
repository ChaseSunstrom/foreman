---
id: T-1838
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T10:35:22Z
updated: 2026-10-28T16:06:33Z
base: cd12a7d5b4875b883d655f1e44870faa042895f3
base_tree: 68f1b355bd9eed227dd2dd3fe1abf16180fa0ca4
plan0_at: 2026-10-28T15:57:22Z
plan0_scope: []
verified: strong
---
# Fm playbooks route: top-1 missed on 3 of 3 real task titles (e.g. a stop-hook bug → strate
## Raw request
> fm playbooks route: top-1 missed on 3 of 3 real task titles (e.g. a stop-hook bug → strategic-compact); build a small labelled set of real titles → expected book and tune weights/terms until top-3 hits most, then revisit naming it in the hint (T-1803 decision)
## Interpretation
fm playbooks route/find ranks the playbook library by FTS5 bm25 over title/use/heads/body. On real task titles it often misses the right book. Build a small labelled set of real titles → expected book, measure top-1/top-3, and tune the index columns, weights and query terms so the expected book lands in the top 3 for most. Then decide whether the route hint should name its top book.
## Assumptions (confidence)
## Acceptance criteria
- [x] 24 labelled real task titles (16 tuned on, 8 held out) put the expected book in the top 3 for at least 17 (was 15) and at the top for at least 9 (was 7) — verify with `python3 plugin/tests/run.py test_playbook_route`
## Non-goals
No embeddings, no synonyms table unless the grid fails, no change to fm which ranking.
## Approach (options → choice → why)
Options: (a) weight grid only over WEIGHTS; (b) add an indexed name column built from the book's path words (terminal ui, silent failures) with an INDEX_VERSION bump, plus a grid; (c) shorter query terms (4+ letters) so words like 'flaky' and 'test' count; (d) a synonyms table. Choice: measure (a)-(c) in memory with a scratch grid against 16 labelled real titles, ship the best simple combination; (d) only if the rest leave most misses. Why: smallest change measured on real titles.
## Risks and rollback
## Execution prompt
## Steps
1. [x] grid-search columns, weights and term length in memory against the labelled titles
2. [x] red test with the labelled set, then the index/query change, INDEX_VERSION bumped
3. [x] decide naming the top book in the hint (fm decide)
## Resume here
<!-- auto -->
- 2026-10-28T16:03:06Z steps 3/3 done
- git: foreman/build; 3 uncommitted: MASTER.md, plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_route.py
- touched since last checkpoint: plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_route.py, MASTER.md
## Docs impact
MASTER.md playbook routing line; CHANGELOG Unreleased
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_playbook_route test_which test_playbook_machinery` → exit 0 · Ran 60 tests in 3.9s (10 classes, 16 at a time; slowest: Load 4s, Verbs 2s, Cli 2s) / OK [ran] [tree d7b9cf45fd4f] (2026-10-28T16:02:33Z)
- (step 1) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/routetune5.py` → exit 0 · 1 24 1 (4, 11) (1, 1) (12, 5) / 1 24 1.5 (4, 10) (2, 3) (13, 6) [ran] [tree d7b9cf45fd4f] (2026-10-28T16:02:40Z)
- (step 3) `grep -n 'T-1838 step 3' state/projects/foreman-4a056f/decisions.md` → exit 0 · 202:| 2026-10-28 | T-1838 step 3: the per-turn hint still does not name the top routed book | after tuning, the top 1 is right on 9 of 24 real titles: a wrong book named every turn costs 22-33 ms and [ran] [tree d7b9cf45fd4f] (2026-10-28T16:02:40Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_route 2>&1 | grep -B2 -A12 "^ERROR\|Traceback" | head -30` → ✗ exit 1 · FAILED (errors=1) / Ran 23 tests in 2.2s (2 classes, 16 at a time; slowest: Cli 2s, Rank 1s) [ran] [tree 04dc4a0f7aa8] (2026-10-28T16:05:02Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_route` → exit 0 · Ran 23 tests in 2.3s (2 classes, 16 at a time; slowest: Cli 2s, Rank 1s) / OK [ran] [tree 4d41fc8eba91] (2026-10-28T16:06:23Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 2 MEDIUM + 4 LOW; 5 fixed test-first (type normalised, red on old code), 1 accepted and noted` → route --task now uses the normalised type; tuned 13/8 and held-out 4/1 asserted separately; hint still names no book (decided) [tree 4d41fc8eba91] (2026-10-28T16:06:23Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 2 MEDIUM + 4 LOW; 5 fixed test-first (type normalised, red on old code), 1 accepted and noted` → no FTS5 skips; hand-edited lowercase type boosts; fm which past BIG queries 8 words, noted [tree 4d41fc8eba91] (2026-10-28T16:06:23Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 2 MEDIUM + 4 LOW; 5 fixed test-first (type normalised, red on old code), 1 accepted and noted` → the live-library test names missed titles and checks each labelled book exists [tree 4d41fc8eba91] (2026-10-28T16:06:23Z)
## Log
- 2026-10-28T10:35:22Z created
- 2026-10-28T15:57:17Z set tier=M
- 2026-10-28T15:57:21Z focused
- 2026-10-28T16:01:56Z hypothesis: the kiln test scores 0 because FTS5 clamps IDF when a term is in half the books or more (2 of 3); with 3 unrelated books (2 of 5) the scores are nonzero and the boost shows
- 2026-10-28T16:02:29Z criterion 1 text: the labelled real-title set puts the expected book in the top 3 for at least 12 of 16 and top 1 for more than today's 7 → 24 labelled real task titles (16 tuned on, 8 held out) put the expected book in the top 3 for at least 17 (was 15) and at the top for at least 9 (was 7)
- 2026-10-28T16:06:32Z done
- 2026-10-28T16:06:33Z committed 14ed36ef (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-28: T-1803 step 3: the next-step hint does not name the top routed book
- T-1835 [FEATURE S, done, 1 steps] Fm which ranks playbooks by reading every header; at 10k+ books call fmplaybooks.find (FTS
- T-1833 [FEATURE M, done, 3 steps] fm playbooks route TEXT|--task ID: top playbooks by relevance over an incremental FTS5 index, fast at 20k (part of T-1803) — lesson: Tw…
- T-1803 [FEATURE L, done, 3 steps] Playbook library at 10,000+ scale, all routed, none listed (user: 'tens of thousands of sk — lesson: A regex that reads a command's arg…
- similar finished tasks took 1–3 steps
- start here (files T-1835 touched): plugin/tests/test_which.py, plugin/lib/fmwhich.py
## Lessons
- bm25 in FTS5 scores 0 for a word in half the docs or more: a tiny test library needs filler books or every score ties
## Files touched
- plugin/tests/test_playbook_route.py
- plugin/lib/fmplaybooks.py
- MASTER.md
- CHANGELOG.md
