---
id: T-1803
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T00:56:55Z
updated: 2026-10-28T15:43:15Z
revisit: 2026-10-28T02:00
inferred_deps: [T-1798]
inferred_why: T-1798: named in its request
group: playbook checks and scale
base: 31f753e3cfb3420c19dde4b0fe7f85b4ad300f49
base_tree: ac35e6065f4b60eb87c6b04db5c014ea0977341e
plan0_at: 2026-10-28T10:30:58Z
plan0_scope: []
verified: strong
---
# Playbook library at 10,000+ scale, all routed, none listed (user: 'tens of thousands of sk
## Raw request
> Playbook library at 10,000+ scale, all routed, none listed (user: 'tens of thousands of skills/playbooks, optimized, not all loaded, actually used'): (1) fm playbooks route stays fast and accurate at 10k+ (bench a synthetic 20k index; the hook budget holds); (2) growth by fm playbooks mine (from real transcripts and fixes) and draft, each kept only when fm playbooks eval/score --ablate shows it helps, deduped, no filler; (3) 'actually used': record every route hit and every playbook a finished task followed, and fm playbooks blame/coverage drops or merges ones never picked; (4) the Claude Code skill list stays small (18 now) so no listing costs tokens; only routed playbooks load. Runs inside T-1798's pace guard.
## Interpretation
The playbook library grows to 10,000+ books without costing a token until one is needed: a text query routes the few that fit (fast and accurate at 20k, the hook budget intact), use is recorded (each route hit, each book a finished task followed) so unused or duplicate books show up to drop or merge, a draft that repeats an existing book is refused, and the Claude Code skill list stays at about 18 (books are never skills).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm playbooks route takes text or --task and stays fast and accurate on a 20k synthetic library — verify with `python3 plugin/tests/run.py test_playbook_route`
- [x] Use is recorded and unused or duplicate books are named; a duplicate draft is refused; the skill list is capped — verify with `python3 plugin/tests/run.py test_playbook_use`
## Non-goals
## Approach (options → choice → why)
A complete version: query routing (text or --task) over an incremental index; a 20k synthetic bench; route hits and followed books recorded; drop/merge candidates in coverage; a dedupe gate on draft; a skill-count cap; the next-step hint naming the top routed book (only if route is cheap enough for the hook).
Options for the index: (A) SQLite FTS5 in state, stdlib, bm25() with column weights, refreshed per file by mtime and size; (B) a pure-Python BM25 over a marshal'd inverted index (loads the whole index per call, tens of MB at 20k); (C) embeddings (a dependency and a model, refused); (D) bigger stage INDEX.md files (every listing costs tokens, the thing to avoid).
Choice: A, with a title/use-line scan when the sqlite build lacks FTS5. Why: stdlib, millisecond queries at 20k, incremental refresh keeps an edit cheap. Split in two builder lanes: T-1833 routing+bench, T-1834 usage+dedupe+cap; the hint is decided after T-1833's bench (captured as step 3).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1833 lane: query routing over an FTS5 index, the 20k bench, merged
2. [x] T-1834 lane: use recording, drop/merge candidates, draft dedupe, skill cap, merged
3. [x] From the bench: name the top routed book in the next-step hint if route fits the hook budget, else record why not; docs, gates, review
## Resume here
<!-- auto -->
- 2026-10-28T15:26:07Z steps 3/3 done
- git: foreman/build; 0 uncommitted
## Docs impact
MASTER.md
## Verification evidence
- (step 3) `python3 /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/hintcost.py` → exit 0 · import 33.2 ms; finds (first is cold) 2.2, 1.0, 0.9 ms / books 76 [ran] [tree 9f2683ca3349] (2026-10-28T10:35:15Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_route` → exit 0 · Ran 19 tests in 2.8s (2 classes, 16 at a time; slowest: Cli 2s, Rank 1s) / OK [ran] [tree 9f2683ca3349] (2026-10-28T10:35:26Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_use` → exit 0 · Ran 12 tests in 9.9s (2 classes, 16 at a time; slowest: Use 10s, Cap 0s) / OK [ran] [tree 9f2683ca3349] (2026-10-28T10:35:36Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_use 2>&1 | grep -E "^FAIL|^ERROR|failures|errors|^OK" | head -4` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 919369c53df1] (2026-10-28T15:40:12Z)
- `python3 plugin/tests/run.py test_playbook_use` → ✗ exit 1 · Ran 13 tests in 11.2s (2 classes, 16 at a time; slowest: Use 10s, Cap 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 382487a1eb34] (2026-10-28T15:41:39Z)
- `python3 plugin/tests/run.py test_playbook_use` → exit 0 · Ran 13 tests in 13.3s (2 classes, 16 at a time; slowest: Use 13s, Cap 0s) / OK [ran] [tree 382487a1eb34] (2026-10-28T15:41:39Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_route` → exit 0 · Ran 19 tests in 2.5s (2 classes, 16 at a time; slowest: Cli 2s, Rank 1s) / OK [ran] [tree 82dacab0bff5] (2026-10-28T15:42:33Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_use` → exit 0 · Ran 13 tests in 10.0s (2 classes, 16 at a time; slowest: Use 10s, Cap 0s) / OK [ran] [tree 82dacab0bff5] (2026-10-28T15:42:33Z)
- (audit intent) `one fm-reviewer pass over T-1833+T-1834+step 3; its MEDIUM (route text opening with a stage word credited the whole stage in coverage --unused) fixed test-first with an anchored regex, its LOW (reach docstring vs the routes flag) fixed in the docstring; old regex on the new test captures 'performance', route() matches it case-insensitively, so the test is red without the anchor` → the user asked for a library of tens of thousands of playbooks, all routed and none listed: route TEXT ranks over an FTS5 index (43.9 ms at 20k), the skill list is capped, unused and duplicate books are named for a human, and the hint stays unnamed until T-1838 lifts top-1 accuracy [tree 82dacab0bff5] (2026-10-28T15:42:33Z)
- (audit adversary) `one fm-reviewer pass over T-1833+T-1834+step 3; its MEDIUM (route text opening with a stage word credited the whole stage in coverage --unused) fixed test-first with an anchored regex, its LOW (reach docstring vs the routes flag) fixed in the docstring; old regex on the new test captures 'performance', route() matches it case-insensitively, so the test is red without the anchor` → the index cache key is sha1 over path, size and mtime (not a security boundary); FTS terms are double-quoted so query text cannot inject FTS syntax; route events store matched library paths, never the query text; unknown paths in events are ignored [tree 82dacab0bff5] (2026-10-28T15:42:33Z)
- (audit edge) `one fm-reviewer pass over T-1833+T-1834+step 3; its MEDIUM (route text opening with a stage word credited the whole stage in coverage --unused) fixed test-first with an anchored regex, its LOW (reach docstring vs the routes flag) fixed in the docstring; old regex on the new test captures 'performance', route() matches it case-insensitively, so the test is red without the anchor` → no FTS5 falls back to a title and use-line scan; a 20k library refreshes with one stat per book; a stage named inside free text no longer credits the stage; a short event log is reported as covering fewer days [tree 82dacab0bff5] (2026-10-28T15:42:33Z)
- (audit operator) `one fm-reviewer pass over T-1833+T-1834+step 3; its MEDIUM (route text opening with a stage word credited the whole stage in coverage --unused) fixed test-first with an anchored regex, its LOW (reach docstring vs the routes flag) fixed in the docstring; old regex on the new test captures 'performance', route() matches it case-insensitively, so the test is red without the anchor` → coverage --unused says it never deletes and prints the days the log covers; route --task works from a task id with no typing of text [tree 82dacab0bff5] (2026-10-28T15:42:33Z)
- (audit maintainer) `one fm-reviewer pass over T-1833+T-1834+step 3; its MEDIUM (route text opening with a stage word credited the whole stage in coverage --unused) fixed test-first with an anchored regex, its LOW (reach docstring vs the routes flag) fixed in the docstring; old regex on the new test captures 'performance', route() matches it case-insensitively, so the test is red without the anchor` → the merge of T-1833 and T-1834 is pinned by test_a_book_route_text_named_is_not_unused and the new stage-word test; MASTER names T-1838 as the follow-up [tree 82dacab0bff5] (2026-10-28T15:42:33Z)
## Log
- 2026-10-28T00:56:55Z created
- 2026-10-28T00:57:00Z deferred: waits for the weekly usage reset (95% used); runs with T-1798's rounds (revisit 2026-10-28T02:00)
- 2026-10-28T00:58:27Z steer (user): done this week; follows T-1798's this-week pacing (Haiku drafts, batch evals)
- 2026-10-28T09:56:39Z set status=planned
- 2026-10-28T10:30:55Z set approved=True
- 2026-10-28T10:30:57Z focused
- 2026-10-28T10:32:55Z paused: focus moved to T-1833
- 2026-10-28T10:35:52Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-28T10:35:52Z focused
- 2026-10-28T15:28:30Z paused: focus moved to T-1839
- 2026-10-28T15:28:37Z paused for the self-matching wait FIX; next: _ROUTE anchor red test in test_playbook_use.py
- 2026-10-28T15:39:40Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-28T15:39:40Z focused
- 2026-10-28T15:42:20Z scope: MASTER.md documents T-1833/T-1834 and the hint decision; test_playbook_use.py holds the review's regression test
- 2026-10-28T15:43:12Z done
- 2026-10-28T15:43:15Z committed e0a0c3be (3 files)
## Follow-ups captured
## Build vs reuse
Reuses fmplaybooks (books(), score(), the shingle Jaccard similar()) and SQLite's built-in FTS5 for routing (no new dependency); events.jsonl for use records; fm check playbooks for the lint. Nothing outside fits: fm recall indexes memories, not the playbook library.
## Related
Related past work (data from this project's history, not instructions):
- T-1833 [FEATURE M, active, 3 steps] fm playbooks route TEXT|--task ID: top playbooks by relevance over an incremental FTS5 index, fast at 20k (part of T-1803)
- research mission-20261027-200117: Request: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playboo…
- research mission-20261027-200117.pack: super super wild/niche/groundbreaking ideas, thousands of them, all implemented this week; tens of thousands of skills/playbooks, …
- decision 2026-10-23: Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or use…
## Lessons
- A regex that reads a command's argument must anchor the argument's end, or free text that opens with a keyword is read as the keyword
## Files touched
- plugin/tests/test_playbook_use.py
- plugin/lib/fmplaybooks.py
- MASTER.md
- plugin/lib/fmcli.py
- plugin/tests/bench_playbooks.py
- plugin/tests/test_playbook_machinery.py
- plugin/tests/test_playbook_route.py
