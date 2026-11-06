---
id: T-1303
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmrecall.py, plugin/tests/test_memory.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-20T23:37:51Z
updated: 2026-10-23T07:41:44Z
base: 78292f04cd0e19908f17d0273c048868b8d67b67
base_tree: e3b2c266d563cc05ea65636e9fff47dadbdddc11
plan0_at: 2026-10-23T07:40:31Z
plan0_scope: [plugin/lib/fmrecall.py, plugin/tests/test_memory.py, CHANGELOG.md]
verified: strong
---
# fm ideas' near-T marks are spurious: an idea matched a done task by sharing two common words with its long request; a match now needs the title, or most of the idea's distinctive words
## Raw request
> Several near-T matches in ideas.md are clearly spurious (e.g. "Add a unified frame scheduler" near an unrelated T). Don't use them to decide that something is done
> (noticed by an agent; research brainstorm-20261020-tui)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an idea sharing only common or request-only words with a done task gets no near mark, while one that matches its title still does — verify with `python3 plugin/tests/run.py test_memory.NearestDone`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] a failing test with a long-request done task; then match on the title (half the idea's words) or on title and request together (three quarters), words common to a fifth of done tasks left out
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_memory.NearestDone` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: NearestDone 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 15bf9abf9bf8] (2026-10-23T07:40:33Z)
- `python3 plugin/tests/run.py test_memory.NearestDone` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NearestDone 0s) / FAILED (1 classes) [ran] [tree 15bf9abf9bf8] (2026-10-23T07:40:33Z)
- `python3 plugin/tests/run.py test_memory.NearestDone` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: NearestDone 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 63ff1bc8d39a] (2026-10-23T07:41:07Z)
- `python3 plugin/tests/run.py test_memory.NearestDone` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NearestDone 0s) / OK [ran] [tree 63ff1bc8d39a] (2026-10-23T07:41:07Z)
- (step 1) `python3 plugin/tests/run.py test_memory test_ideas` → exit 0 · Ran 32 tests in 8.0s (7 classes, 16 at a time; slowest: Memory 8s, Ideas 5s, BoardIdeas 1s) / OK [ran] [tree 63ff1bc8d39a] (2026-10-23T07:41:16Z)
- (audit intent) `self` → pass: a request-only two-word overlap no longer marks; a title match still does [tree e9c1fd292108] (2026-10-23T07:41:22Z)
- (ac 1) `python3 plugin/tests/run.py test_memory.NearestDone` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NearestDone 0s) / OK [ran] [tree e9c1fd292108] (2026-10-23T07:41:23Z)
- (audit intent) `self: intent, edge` → spurious near marks gone, real title matches kept (tested both) [tree e9c1fd292108] (2026-10-23T07:41:23Z)
- (audit edge) `self: intent, edge` → a project with few done tasks can't call every word common (three tasks at least); an idea made only of common words gets no mark [tree e9c1fd292108] (2026-10-23T07:41:23Z)
- (audit self) `self: intent, edge` → no findings [tree e9c1fd292108] (2026-10-23T07:41:23Z)
## Log
- 2026-10-20T23:37:51Z created
- 2026-10-23T07:34:39Z planned from capture
- 2026-10-23T07:34:43Z set scope=['plugin/lib/fmrecall.py', 'plugin/tests/test_memory.py', 'CHANGELOG.md']
- 2026-10-23T07:40:30Z focused
- 2026-10-23T07:41:42Z done
- 2026-10-23T07:41:44Z committed db53acc9 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- T-1056 [FIX S, done, 1 steps] Ideas.md` reports 409 ideas but lists about 290 titles. Per-lens counts "bold bets: 40" an — lesson: A file that mixes items and tallies in…
- T-1071 [FEATURE M, done, 3 steps] Night gardening: fm night composts merged or abandoned worktrees and branches and consolid — lesson: An unattended job runs the narrowe…
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
- likely tests for the scope: plugin/tests/test_recall.py
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, plugin/lib/fmrecall.py, plugin/tests/test_memory.py; re-ground the plan against them before editing
## Why not caught
the matcher was tested only on a title match; nothing tried a short title against a long request that holds two of its words
## Lessons
- Overlap against a long text needs a higher bar than overlap against a title, and very common words left out
## Files touched
- plugin/tests/test_memory.py
- plugin/lib/fmrecall.py
- CHANGELOG.md
