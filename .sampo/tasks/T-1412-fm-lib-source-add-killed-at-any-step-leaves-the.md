---
id: T-1412
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T20:55:57Z
base: 0b8f3bdae8ff1e214bc32e4abde117ea6acc2e6b
base_tree: ad2821b97468eb3b799d8e10d4a0c96f69575638
plan0_at: 2026-10-21T20:04:42Z
plan0_scope: []
verified: strong
---
# fm lib source add or update killed at any step leaves the previous index intact and recoverable
## Raw request
> FIX: fm lib source add killed at any step leaves the previous index intact (S25, A15)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a test killing source_add at each step of a fixture finds the previous index unchanged
## Interpretation
source_add swaps the new clone in with two renames (final→final.old-PID, tmp→final). A kill between them leaves no NAME at all, only NAME.old-PID, so the source vanishes from search until re-added; a kill earlier leaves .tmp- folders forever.
## Assumptions (confidence)
## Acceptance criteria
- [x] a test that stops source_add at each step of a fixture (clone, index, the move of the old index aside, the move of the new one in) finds the previous source listed and searchable afterwards, and no .tmp- or .old- folder listed as a source — verify with `python3 plugin/tests/run.py test_lib_source_kill`
## Non-goals
## Approach (options → choice → why)
Options: (A) recover on next use: restore an orphaned .old- when its NAME is missing, sweep stale temp folders by dead pid (chosen: two renames stay, recovery is a few lines, covers every kill point); (B) a symlink swap (one atomic rename of a link; changes the on-disk layout every reader knows); (C) a journal file (more moving parts than the problem). 
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_lib_source_kill.py: patch os.replace / _index_source / _git_src to raise (or SIGKILL a child doing the add) at each step, then check fmlib.sources() and fm lib search
2. [x] fmlib: recover at the start of sources() and source_add — a NAME.old-PID with no NAME is moved back; stale .tmp-*/.old-* folders whose pid is gone are removed; sources() never lists dot or .old- folders
## Resume here
<!-- auto -->
- 2026-10-21T20:40:44Z steps 2/2 done
- git: foreman/build; 1 uncommitted: CHANGELOG.md
- touched since last checkpoint: .claude/worktrees/agent-a7afe76b862cc1b21/plugin/lib/fmlib.py, .claude/worktrees/agent-a7afe76b862cc1b21/plugin/tests/test_lib_source_kill.py, CHANGELOG.md
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lib_source_kill 2>&1 | tail -40` → ✗ exit 1 · Ran 3 tests in 4.0s (1 classes, 16 at a time; slowest: SourceKill 3s) / FAILED (1 classes) [ran] [tree 36d77ad47540] (2026-10-21T20:06:04Z)
- (step 1) `python3 plugin/tests/run.py test_lib_source_kill` → ✗ exit 1 · Ran 3 tests in 3.3s (1 classes, 16 at a time; slowest: SourceKill 3s) / FAILED (1 classes) [ran] [tree 36d77ad47540] (2026-10-21T20:06:10Z)
- (ac 1) `python3 plugin/tests/run.py test_lib_source_kill 2>&1 | tail -4` → exit 0 · Ran 3 tests in 10.5s (1 classes, 16 at a time; slowest: SourceKill 10s) / OK [ran] [tree ff6cbcb70d90] (2026-10-21T20:07:49Z)
- (step 2) `python3 plugin/tests/run.py test_lib_source_kill` → exit 0 · Ran 3 tests in 10.3s (1 classes, 16 at a time; slowest: SourceKill 10s) / OK [ran] [tree ad13b63eabaf] (2026-10-21T20:08:06Z)
- (step 1) `python3 plugin/tests/run.py test_lib_source_kill test_lib_hostile` → exit 0 · Ran 11 tests in 10.3s (3 classes, 16 at a time; slowest: SourceKill 10s, HostileCorpus 7s, HostileMarketplace 1s) / OK [ran] [tree cb037914127b] (2026-10-21T20:29:39Z)
- (step 2) `python3 plugin/tests/run.py test_lib_source_kill test_lib_hostile` → exit 0 · Ran 11 tests in 10.0s (3 classes, 16 at a time; slowest: SourceKill 9s, HostileCorpus 8s, HostileMarketplace 1s) / OK [ran] [tree cb037914127b] (2026-10-21T20:29:51Z)
- (ac 1) `python3 plugin/tests/run.py test_lib_source_kill` → exit 0 · Ran 3 tests in 8.7s (1 classes, 16 at a time; slowest: SourceKill 8s) / OK [ran] [tree 20b908bb01e4] (2026-10-21T20:30:10Z)
- (audit intent) `self: read _recover_sources, sources() and source_add — recovery touches only leftovers of dead pids (a set-aside .old- moved back when NAME is missing, else removed; .tmp- removed); sources() skips dot and .old- folders; a failed move-in restores the old index before raising` → a SIGKILL at each of five points (clone, index, before and after the old index moves aside, after the new one moves in) leaves the previous source listed and searchable and no temp folder listed (test_lib_source_kill) [tree 20b908bb01e4] (2026-10-21T20:30:10Z)
- (audit edge) `self: read _recover_sources, sources() and source_add — recovery touches only leftovers of dead pids (a set-aside .old- moved back when NAME is missing, else removed; .tmp- removed); sources() skips dot and .old- folders; a failed move-in restores the old index before raising` → a live process's folders are left alone; a reused pid delays cleanup (ponytail note); two concurrent updates of one name still race (captured T-1428) [tree 20b908bb01e4] (2026-10-21T20:30:10Z)
- (audit intent) `self: read _recover_sources, sources() and source_add — recovery touches only leftovers of dead pids (a set-aside .old- moved back when NAME is missing, else removed; .tmp- removed); sources() skips dot and .old- folders; a failed move-in restores the old index before raising` → a SIGKILL at each of five points (clone, index, before and after the old index moves aside, after the new one moves in) leaves the previous source listed and searchable and no temp folder listed (test_lib_source_kill) [tree 009d2f12e9ff] (2026-10-21T20:50:13Z)
- (audit edge) `self: read _recover_sources, sources() and source_add — recovery touches only leftovers of dead pids (a set-aside .old- moved back when NAME is missing, else removed; .tmp- removed); sources() skips dot and .old- folders; a failed move-in restores the old index before raising` → a live process's folders are left alone; a reused pid delays cleanup (ponytail note); two concurrent updates of one name still race (captured T-1428) [tree 009d2f12e9ff] (2026-10-21T20:50:13Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T20:04:19Z planned from capture
- 2026-10-21T20:04:21Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1412.builder.md
- 2026-10-21T20:04:41Z focused
- 2026-10-21T20:28:52Z merged worktree-agent-a7afe76b862cc1b21 (2 file(s))
- 2026-10-21T20:29:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7afe76b862cc1b21
- 2026-10-21T20:29:27Z focused
- 2026-10-21T20:40:45Z paused: focus moved to T-1379
- 2026-10-21T20:50:11Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-21T20:50:11Z focused
- 2026-10-21T20:55:52Z done
- 2026-10-21T20:55:57Z committed d89420bd (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1396 [SECURITY M, done, 3 steps] Hostile skills and plugins can't get past the indexer: a 25+ item corpus quarantined with reasons, the Agent Skills spec checked, over…
- T-1410 [FEATURE S, done, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it — lesson: A record the user can create should…
- decision 2026-10-16: Recommendation: build the 9 grounded items T-1180..T-1188 with builders; the worktree-fm re-exec idea is skipped (unreviewed lane code would write r…
## Why not caught
no test killed source_add mid-way before
## Lessons
- A two-rename swap needs a recovery pass on the next read; atomicity of each rename isn't atomicity of the pair
## Plan gaps
- failed first: step 1 failing tests in plugin/tests/test_lib_source_kill.py: patch os.replace / _index_source / _git_src …
## Files touched
- plugin/tests/test_lib_source_kill.py
- plugin/lib/fmlib.py
- CHANGELOG.md
- README.md
- plugin/lib/fmcode.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmmodels.py
- plugin/lib/fmplugins.py
- plugin/tests/helpers.py
- plugin/tests/test_doctor.py
- plugin/tests/test_retired_models.py
- plugin/tests/test_safety.py
- plugin/tests/test_supply_delta.py
