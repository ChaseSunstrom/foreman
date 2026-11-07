---
id: T-1833
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_route.py, plugin/tests/bench_playbooks.py]
depends_on: []
source: discovered
created: 2026-10-28T09:59:19Z
updated: 2026-10-28T10:34:06Z
base: 31f753e3cfb3420c19dde4b0fe7f85b4ad300f49
base_tree: fe2139b2cffa4c77929c7003f280028a97ead3a7
plan0_at: 2026-10-28T09:59:45Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_route.py, plugin/tests/bench_playbooks.py]
verified: strong
---
# fm playbooks route TEXT|--task ID: top playbooks by relevance over an incremental FTS5 index, fast at 20k (part of T-1803)
## Raw request
> fm playbooks route TEXT|--task ID: top playbooks by relevance over an incremental FTS5 index, fast at 20k (part of T-1803)
## Interpretation
Routing by meaning instead of by stage, so a library of tens of thousands of books costs nothing until a query picks a few. The index lives in Foreman's state, never in the plugin tree (an installed plugin is read-only).
## Assumptions (confidence)
## Acceptance criteria
- [x] route with text that isn't a stage key, or --task ID (the task's title, interpretation and criteria), prints the top -k N (default 5) books with score and Use-when line; a stage key keeps today's behaviour; on a 2k synthetic library each planted book is top-1 for its query; the index refreshes after a book is added, edited or removed; without FTS5 a title/use-line scan answers — verify with `python3 plugin/tests/run.py test_playbook_route`
- [x] bench_playbooks.py builds a 20k synthetic library in a temp dir and reports index build, one-edit refresh, and route p50/p95 wall and CPU; exits 1 when warm route CPU p95 > 50 ms or refresh > 2 s or planted accuracy < 95% — verify with `python3 plugin/tests/bench_playbooks.py --books 20000`
## Non-goals
## Approach (options → choice → why)
sqlite3 FTS5 table (path UNINDEXED, title, use, heads, body) with bm25() weights about 10/5/2/1, built under c.state_dir() keyed by the playbooks root; a files table of (path, mtime_ns, size) so each call stats the tree once (os.scandir) and re-indexes only changed rows, deletes removed ones. Index body text capped (first ~4 KB) so 20k books stay small. Query: the text's words (5+ letters, not _COMMON, OR-joined, quoted to dodge FTS5 syntax). Each explicit route call appends one event (kind 'playbook', action 'route', paths) to events.jsonl via the existing event writer so reach() can count it. Fallback when 'create virtual table … using fts5' raises: score title+use word overlap. Rejected: pure-Python BM25 (loads the whole index per call), embeddings (a dependency), bigger INDEX.md listings (cost tokens).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests for text and --task routing, refresh and fallback
2. [x] FTS5 index and route, green
3. [x] bench_playbooks.py at 20k, numbers in the report
## Resume here
<!-- auto -->
- 2026-10-28T10:14:37Z steps 3/3 done
- git: worktree-agent-ac9c5d6b51b4d1564; 3 uncommitted: plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_machinery.py, plugin/tests/test_playbook_route.py
- touched since last checkpoint: plugin/tests/bench_playbooks.py, plugin/lib/fmcli.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/prof.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/micro.py, MASTER.md, plugin/tests/test_playbook_route.py, plugin/tests/test_playbook_machinery.py, plugin/lib/fmplaybooks.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p 'test_playbook_route.py' 2>&1 | tail -5; true` → ✗ exit 1 · FAILED (2 classes) / fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hides the exit), so it counts as a failure [ran] [tree 651eb6e24197] (2026-10-28T10:01:52Z)
- (step 1) `python3 plugin/tests/run.py -p test_playbook_route.py` → exit 0 · Ran 15 tests in 1.3s (2 classes, 16 at a time; slowest: Cli 1s, Rank 0s) / OK [ran] [tree f27f34ccc1fe] (2026-10-28T10:06:21Z)
- (step 3) `python3 plugin/tests/bench_playbooks.py --books 20000` → exit 0 · route_wall: p50 40.8 ms, p95 44.3 ms / route_cpu: p50 40.3 ms, p95 43.9 ms [ran] [tree f27f34ccc1fe] (2026-10-28T10:06:27Z)
- (step 2) `python3 plugin/tests/run.py -p test_playbook_route.py` → exit 0 · Ran 15 tests in 1.3s (2 classes, 16 at a time; slowest: Cli 1s, Rank 0s) / OK [ran] [tree f27f34ccc1fe] (2026-10-28T10:06:30Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_playbook_check test_playbook_route` → exit 0 · Ran 171 tests in 23.7s (48 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / OK [ran] [tree f27f34ccc1fe] (2026-10-28T10:06:54Z)
- (step 1) `python3 plugin/tests/run.py -p 'test_playbook*.py'` → exit 0 · Ran 98 tests in 8.7s (20 classes, 16 at a time; slowest: FromThisRepo 9s, Load 8s, Verbs 5s) / OK [ran] [tree 2152c2608058] (2026-10-28T10:16:20Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_playbook_check test_playbook_machinery test_playbook_route` → exit 0 · Ran 200 tests in 50.0s (53 classes, 16 at a time; slowest: TaskLifecycle 50s, AuditPrep 26s, StateViews 26s) / OK [ran] [tree 2152c2608058] (2026-10-28T10:17:12Z)
- (step 2) `python3 plugin/tests/run.py -p test_playbook*.py` → exit 0 · Ran 111 tests in 6.9s (22 classes, 16 at a time; slowest: Use 7s, Load 4s, FromThisRepo 4s) / OK [ran] [tree c514690e662b] (2026-10-28T10:33:06Z)
- (step 3) `python3 plugin/tests/bench_playbooks.py --books 20000` → exit 0 · route_wall: p50 40.5 ms, p95 44.0 ms / route_cpu: p50 39.5 ms, p95 42.8 ms [ran] [tree c514690e662b] (2026-10-28T10:33:13Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_route` → exit 0 · Ran 19 tests in 1.8s (2 classes, 16 at a time; slowest: Cli 2s, Rank 0s) / OK [ran] [tree 9f2683ca3349] (2026-10-28T10:33:39Z)
- (ac 2) `python3 plugin/tests/bench_playbooks.py --books 20000` → exit 0 · route_wall: p50 38.7 ms, p95 41.7 ms / route_cpu: p50 38.6 ms, p95 41.6 ms [ran] [tree 9f2683ca3349] (2026-10-28T10:33:39Z)
- (audit intent) `Lead review of the builder's diff; nits fixed on the branch; the merge with T-1834 resolved by hand (_scan now counts route events once for reach and unused) with a seam test` → route TEXT or --task ranks books over an FTS5 index with score and Use-when line; stage keys keep the old table; bench at 20k: build 0.65 s, refresh 0.1 s, warm route CPU p95 43 ms [tree 9f2683ca3349] (2026-10-28T10:33:39Z)
- (audit adversary) `Lead review of the builder's diff; nits fixed on the branch; the merge with T-1834 resolved by hand (_scan now counts route events once for reach and unused) with a seam test` → the route event stores paths, never the query text; FTS5 query terms are quoted tokens, so user text can't inject FTS syntax; a corrupt index is rebuilt [tree 9f2683ca3349] (2026-10-28T10:33:39Z)
- (audit edge) `Lead review of the builder's diff; nits fixed on the branch; the merge with T-1834 resolved by hand (_scan now counts route events once for reach and unused) with a seam test` → no FTS5 falls back to a title/use-line scan; a mistyped one-word stage is a usage error; an index whose library is gone is pruned; the bench misses its limit under heavy load (T-1836) [tree 9f2683ca3349] (2026-10-28T10:33:39Z)
- (audit maintainer) `Lead review of the builder's diff; nits fixed on the branch; the merge with T-1834 resolved by hand (_scan now counts route events once for reach and unused) with a seam test` → one _scan pass serves reach and unused; routed is {book: routes} in both [tree 9f2683ca3349] (2026-10-28T10:33:39Z)
## Log
- 2026-10-28T09:59:19Z created
- 2026-10-28T09:59:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1833.builder.md
- 2026-10-28T09:59:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1833.builder.md
- 2026-10-28T09:59:45Z focused
- 2026-10-28T10:07:38Z scope: test_playbook_machinery.py edited, its route-nosuch case now asks for words, not an error (T-1833)
- 2026-10-28T10:32:49Z merged worktree-agent-ac9c5d6b51b4d1564 (7 file(s))
- 2026-10-28T10:32:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac9c5d6b51b4d1564
- 2026-10-28T10:32:55Z focused
- 2026-10-28T10:33:20Z scope: CHANGELOG.md takes the release line; test_playbook_use.py and the _scan merge are the T-1834 seam (route TEXT hits count as use)
- 2026-10-28T10:34:04Z done
- 2026-10-28T10:34:06Z committed f275832d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1803 [FEATURE L, planned, 3 steps] Playbook library at 10,000+ scale, all routed, none listed (user: 'tens of thousands of sk
- T-1834 [FEATURE M, planned, 2 steps] Playbook use: followed books recorded at finish, unused and near-duplicate books named, duplicate drafts refused, the skill list cap…
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- decision 2026-10-28: T-1822: route map lives in test_plugin_parity, not fmcodetui — nothing at runtime reads it and the help view shows terminal lines (CLI), not Claude …
- the similar finished task took 1 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- Two lanes changing the same reader of the event log conflict at the seam: resolve into one pass and add a test that crosses both features
## Plan gaps
- failed first: step 1 Red tests for text and --task routing, refresh and fallback
## Files touched
- plugin/tests/bench_playbooks.py
- plugin/tests/test_playbook_route.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmcli.py
- plugin/tests/test_playbook_machinery.py
- MASTER.md
- CHANGELOG.md
- plugin/skills/playbooks/references/ui/INDEX.md
- plugin/skills/playbooks/references/ui/composition.md
- plugin/skills/playbooks/references/ui/data-viz.md
- plugin/skills/playbooks/references/ui/design-direction.md
- plugin/skills/playbooks/references/ui/examples/composition.html
- plugin/skills/playbooks/references/ui/examples/data-viz.html
- plugin/skills/playbooks/references/ui/examples/design-direction.html
- plugin/skills/playbooks/references/ui/examples/game-feel.html
- plugin/skills/playbooks/references/ui/examples/interaction.html
- plugin/skills/playbooks/references/ui/examples/motion.html
- plugin/skills/playbooks/references/ui/examples/scrollytelling.html
- plugin/skills/playbooks/references/ui/examples/sound-design.html
- plugin/skills/playbooks/references/ui/examples/terminal-ui.html
- plugin/skills/playbooks/references/ui/examples/type-and-colour.html
- plugin/skills/playbooks/references/ui/examples/visual-qa.html
- plugin/skills/playbooks/references/ui/game-feel.md
- plugin/skills/playbooks/references/ui/interaction.md
- plugin/skills/playbooks/references/ui/motion.md
- plugin/skills/playbooks/references/ui/scene-3d.md
- plugin/skills/playbooks/references/ui/scrollytelling.md
- plugin/skills/playbooks/references/ui/sound-design.md
- plugin/skills/playbooks/references/ui/terminal-ui.md
- plugin/skills/playbooks/references/ui/type-and-colour.md
