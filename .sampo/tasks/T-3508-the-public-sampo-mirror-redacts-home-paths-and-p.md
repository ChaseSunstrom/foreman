---
id: T-3508
type: SECURITY
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/ops-1.md, plugin/lib/sampo/core.py, plugin/lib/sampo/sync.py, plugin/tests/test_sync.py]
depends_on: []
source: discovered
created: 2026-11-06T19:06:03Z
updated: 2026-11-07T00:42:51Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T19:12:54Z
plan0_scope: []
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
unproven: [docs]
---
# The public .sampo mirror redacts home paths and private hosts (user@host, 100.x addresses) and its README says sampo sync
## Raw request
> The public .sampo mirror redacts home paths and private hosts (user@host, 100.x addresses) and its README says sampo sync
## Interpretation
Reading 1 (chosen): every text file sync export writes into the committed .sampo mirror shows home directories (the running user's HOME and any /home/<name>) as ~ and user@IP or bare IPs in 10/8, 172.16/12, 192.168/16, 100.64/10 as <host>; the first export after the change rewrites files already mirrored; import stays consistent with redacted copies; the README says sampo sync. Reading 2 (ruled out): redact local state itself (briefs, ledger) so nothing local holds the paths: wrong, local runs need the real paths and only the public mirror leaks.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo sync export writes no /home/<user> path and no user@host or private-range address into .sampo (replaced by ~ and <host>), and .sampo/README.md says sampo sync — verify with `python3 plugin/tests/run.py test_sync`
## Non-goals
IPv6 ULA addresses, non-IP hostnames, the -home-<name>- Claude project slugs; running a real export against the repo.
## Approach (options → choice → why)
1) Extend core.redact itself. Fails if: the ledger and evidence lose local paths that runs need. 2) Do less: a sync-only scrub inline in export. Fails if: import's 'changed here?' check compares unredacted local text with the redacted base, so every brief with a home path reads as a conflict and decisions.md lines duplicate. 3) core.redact_local beside core.redact plus one sync._outgoing(rel, text) used by export and by import's comparisons; a version key in sync-stamps.json makes the first export re-scrub every file and refresh an fm-written README; import expands ~/ scope entries. Likely outcome: mirror clean after one export, import unchanged. Choice 3 (85%): smallest diff that keeps export and import on one transform.
## Risks and rollback
A version string shaped like a private IPv4 is shown as <host> in the mirror (local copy untouched). Rollback: revert the commit; the mirror keeps redacted text, harmless.
## Execution prompt
## Steps
1. [x] redact on export, test-first
2. [x] README wording
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_sync` → ✗ exit 1 · Ran 35 tests in 42.9s (2 jobs, 16 at a time; slowest: Sync 31s, BoardSurfaces 0s) / FAILED (1 classes: test_sync.Sync) [ran] [tree 8e3249d3bc41] [world 2f1906870a] (2026-11-06T19:15:29Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_sync` → exit 0 · Ran 35 tests in 28.6s (35 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 2s, Sync.test_fresh_sync_writes_sampo_and_status_and_readme_name_it 1s, Syn [ran] [tree ed5320c155dc] [world 2f1906870a] (2026-11-06T19:23:15Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_sync.Sync.test_export_mirrors_briefs_decisions_and_research_without_authorization test_sync.Sync.test_the_next_export_cleans_a_mirror_written_before_redaction` → exit 0 · Ran 2 tests in 24.5s (2 jobs, 16 at a time; slowest: Sync.test_export_mirrors_briefs_decisions_and_research_without_authorization 1s, Sync.test_the_next_export_cleans_a_mirror_written_before_redaction [ran] [tree ed5320c155dc] [world 2f1906870a] (2026-11-06T19:23:58Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 0421648bbe78] (2026-11-06T21:47:17Z)
- (ac 1) `python3 plugin/tests/run.py test_sync` → exit 0 · Ran 35 tests in 8.1s (2 jobs, 16 at a time; slowest: Sync 8s, BoardSurfaces 0s) / OK [ran] [tree 0421648bbe78] [world 2f1906870a] (2026-11-06T21:47:28Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 0421648bbe78] (2026-11-06T21:47:28Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 0421648bbe78] (2026-11-06T21:47:28Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 0421648bbe78] (2026-11-06T21:47:28Z)
## Log
- 2026-11-06T19:06:03Z created
- 2026-11-06T19:06:19Z lane: ~/.claude/foreman.lanes/T-3508 on foreman/T-3508
- 2026-11-06T19:12:53Z focused
- 2026-11-06T19:12:54Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T21:46:50Z merged foreman/T-3508 in merge train
- 2026-11-06T21:47:17Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/ops-1.md', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/sync.py', 'plugin/tests/test_sync.py']
- 2026-11-06T21:47:17Z scope: widened at merge to the reviewed lane's own diff (ce45b201a), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T21:53:13Z done
- 2026-11-06T21:53:20Z committed 90a2aec3f (1 file)
- 2026-11-07T00:42:51Z lane removed: ~/.claude/foreman.lanes/T-3508; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
## Lessons
- When an export transforms what it writes, every comparison against the exported copy applies the same transform, or the transform reads as local changes.
## Plan gaps
- failed first: step 1 redact on export, test-first
## Files touched
- CHANGELOG.md
- docs/map/ops-1.md
- plugin/lib/sampo/core.py
- plugin/lib/sampo/sync.py
- plugin/tests/test_sync.py
