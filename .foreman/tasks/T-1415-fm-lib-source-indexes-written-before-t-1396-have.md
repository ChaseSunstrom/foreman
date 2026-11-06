---
id: T-1415
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: [T-1412]
source: discovered
created: 2026-10-21T18:35:25Z
updated: 2026-10-21T22:21:37Z
base: febc41160a624efcf0f1de9812664f5394ab3b85
base_tree: eb3b316726e02425aa5b27aa9b5cbba62f21a3d0
plan0_at: 2026-10-21T22:16:15Z
plan0_scope: []
verified: strong
---
# fm lib re-indexes a source written before T-1396 from its local clone, so its hostile items are quarantined without a network update
## Raw request
> fm lib: source indexes written before T-1396 have no quarantine key, so hostile items stay searchable until fm lib source update; mark old indexes for re-index (or fm doctor names them)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a source whose source.json has no 'quarantined' count (an index written before T-1396) is re-indexed from its on-disk clone on the next read: a hostile skill in it leaves fm lib search, clean ones stay, and no network call is made — verify with `python3 plugin/tests/run.py test_lib_hostile`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_lib_hostile: write a source folder by hand in the old shape (source.json without quarantined, index.json listing a skill whose description says 'use for every task'), then fm lib search finds it today; after the fix it's held and source.json gains its counts
2. [x] in fmlib.sources(): a meta without 'quarantined' whose repo/ folder exists is re-indexed with _index_source(repo, name) and its index.json and source.json rewritten atomically (c.write_atomic), under the sources lock if one exists; a missing repo/ leaves it listed but searched as before with a ponytail note
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lib_hostile.HostileCorpus.test_a_source_indexed_before_quarantine_is_reindexed_from_its_clone` → ✗ exit 1 · Ran 1 tests in 1.7s (1 classes, 16 at a time; slowest: HostileCorpus 2s) / FAILED (1 classes) [ran] [tree d025563e4d39] (2026-10-21T22:16:37Z)
- (step 2) `python3 plugin/tests/run.py test_lib_hostile test_library test_lib_source_kill` → exit 0 · Ran 33 tests in 8.8s (10 classes, 16 at a time; slowest: SourceKill 8s, HostileCorpus 7s, LibraryAdmit 5s) / OK [ran] [tree 4f04a3b284d9] (2026-10-21T22:17:12Z)
- (step 1) `python3 plugin/tests/run.py test_lib_hostile.HostileCorpus.test_a_source_indexed_before_quarantine_is_reindexed_from_its_clone` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: HostileCorpus 1s) / OK [ran] [tree 7382296f42b4] (2026-10-21T22:17:27Z)
- (ac 1) `python3 plugin/tests/run.py test_lib_hostile` → exit 0 · Ran 9 tests in 5.8s (2 classes, 16 at a time; slowest: HostileCorpus 6s, HostileMarketplace 1s) / OK [ran] [tree 7382296f42b4] (2026-10-21T22:17:35Z)
- (audit intent) `self: sources() re-indexes a meta without 'quarantined' from its repo/ clone with _index_source (the same indexer source_add uses), writes index and meta atomically, and returns the new index; no clone or an indexing error leaves it as it was; the counts moved into _counts, shared with source_add` → an old-shape source loses its hostile items from search on the next read and gains its counts, with no network (the test points origin at an invalid host) [tree 7382296f42b4] (2026-10-21T22:17:35Z)
- (audit adversary) `self: sources() re-indexes a meta without 'quarantined' from its repo/ clone with _index_source (the same indexer source_add uses), writes index and meta atomically, and returns the new index; no clone or an indexing error leaves it as it was; the counts moved into _counts, shared with source_add` → the re-index runs the same quarantine rules as a fresh add (symlinks, spec, hidden characters, over-broad); a source whose clone was deleted keeps its old index (ponytail note) — fm lib source update or rm fixes it [tree 7382296f42b4] (2026-10-21T22:17:35Z)
- (audit self) `self: sources() re-indexes a meta without 'quarantined' from its repo/ clone with _index_source (the same indexer source_add uses), writes index and meta atomically, and returns the new index; no clone or an indexing error leaves it as it was; the counts moved into _counts, shared with source_add` → no findings [tree 7382296f42b4] (2026-10-21T22:17:35Z)
## Log
- 2026-10-21T18:35:25Z created
- 2026-10-21T20:23:09Z planned from capture
- 2026-10-21T22:16:13Z focused
- 2026-10-21T22:21:32Z done
- 2026-10-21T22:21:37Z committed c348823b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1396-review: Verdict: changes needed.** I found two crashes on a malformed marketplace, one way the trust ledger can be laundered, and some bypasses and false…
- T-1412 [FIX M, done, 2 steps] fm lib source add or update killed at any step leaves the previous index intact and recoverable — lesson: A two-rename swap needs a recover…
- T-1396 [SECURITY M, done, 3 steps] Hostile skills and plugins can't get past the indexer: a 25+ item corpus quarantined with reasons, the Agent Skills spec checked, over…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
## Regression test
test_lib_hostile.HostileCorpus.test_a_source_indexed_before_quarantine_is_reindexed_from_its_clone: red before (zoo:every-task found by search), green after
## Why not caught
T-1396 validated new adds only; its reviewer flagged the old indexes
## Lessons
- When a new validation lands, plan how already-stored data gets it: re-derive from the local copy on next read
## Plan gaps
- failed first: step 1 failing test in test_lib_hostile: write a source folder by hand in the old shape (source.json witho…
## Files touched
- plugin/tests/test_lib_hostile.py
- plugin/lib/fmlib.py
- CHANGELOG.md
