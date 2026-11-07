---
id: T-3574
type: SECURITY
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, plugin/lib/sampo/sync.py, plugin/tests/test_sync.py]
depends_on: []
source: discovered
created: 2026-11-07T02:25:02Z
updated: 2026-11-07T04:56:03Z
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T02:29:34Z
plan0_scope: []
lane_stop: merged 2026-11-07T04:14:53Z
lane_verified: 63923090018be59df2dbbbb3addeb576f53465e3
verified: strong
unproven: [meaning]
---
# SECURITY (user's privacy request): the .sampo mirror keeps each brief's state file name,…
## Raw request
> SECURITY (user's privacy request): the .sampo mirror keeps each brief's state file name, and three task slugs were made from titles that held a home path, so tracked paths hold the -home-<user>- form (.sampo/tasks/T-1297-…, T-2094-…, T-2769-…); export redacts contents but not names. Export must write each mirror file under a redacted name (the same rules as contents, slug-safe: e.g. home-user), remove the old-named mirror file, and import must still map files back by T-id; a test with a made-up user name; then a re-export renames the three
## Interpretation
A brief's mirror file is named after its state file, a slug of its title; three slugs hold this machine's home (home-<login>-). Export must write each brief under a redacted name (contents' redaction plus the home's slug form, slug-safe), drop the old-named copy, and import must still find the brief by T-id and keep the local file name.
## Assumptions (confidence)
## Acceptance criteria
- [x] a brief whose state name holds the home (~) exports as T-NNNN-home-user-…, the old-named mirror copy is removed, and an import after a mirror edit updates the same local brief — verify with `nice -n 10 python3 plugin/tests/run.py test_sync`
- [x] redaction and private-terms tests stay green — verify with `nice -n 10 python3 plugin/tests/run.py test_private_terms`
## Non-goals
## Approach (options → choice → why)
Options: (1) slug the redacted title again: renames every brief whose title changed since creation; (2) generic -home-<word>- → home-user: also renames home-by, home-and, home-import (15 innocent names); (3) per name: redact_local, then this machine's home slug and home|users-<login> → home-user, slug-safe, unchanged names untouched. Choice: 3, one _public(rel) used by export (keys base/stamps by the mirror name; the existing moved-brief cleanup removes the old name) and by import (a local brief whose public name is the mirror's keeps its local path).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: home in a brief's name is redacted on export, old name removed, round-trip import
2. [x] _public(rel) in sync.py; export keys by the mirror name; import maps back to the local path
3. [x] test_sync and test_private_terms green
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_sync.Sync.test_a_brief_named_after_the_home_is_mirrored_under_a_redacted_name` → ✗ exit 1 · Ran 1 tests in 10.7s (1 jobs, 16 at a time; slowest: Sync 0s) / FAILED (1 classes: test_sync.Sync) [ran] [tree aed2161965a9] [world 2f1906870a] (2026-11-07T02:30:16Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_sync.Sync.test_a_brief_named_after_the_home_is_mirrored_under_a_redacted_name` → exit 0 · Ran 1 tests in 0.7s (1 jobs, 16 at a time; slowest: Sync 0s) / OK [ran] [tree 5aa4a88be3ca] [world 2f1906870a] (2026-11-07T02:33:57Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_sync` → exit 0 · Ran 38 tests in 9.1s (2 jobs, 16 at a time; slowest: Sync 9s, BoardSurfaces 0s) / OK [ran] [tree 5aa4a88be3ca] [world 2f1906870a] (2026-11-07T02:34:07Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_sync test_private_terms` → exit 0 · Ran 40 tests in 2.1s (39 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_failed_commit_puts_it_back_and_only_export_retries 1s, Sync. [ran] [tree 5aa4a88be3ca] [world 2f1906870a] (2026-11-07T02:34:09Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_sync test_private_terms` → exit 0 · Ran 40 tests in 23.1s (3 jobs, 16 at a time; slowest: Sync 17s, PrivateTerms 1s, BoardSurfaces 1s) / OK [ran] [tree fe7f87f0f8ff] [world 2f1906870a] (2026-11-07T02:46:41Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 2dcc1db04994] (2026-11-07T04:55:16Z)
- (ac 1) `nice -n 10 python3 plugin/tests/run.py test_sync` → exit 0 · Ran 38 tests in 3.7s (38 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 1s, Sync.test_a_failed_commit_puts_it_back_and_only_export_retries 1s, Sync. [ran] [tree 2dcc1db04994] [world 2f1906870a] (2026-11-07T04:55:25Z)
- (ac 2) `nice -n 10 python3 plugin/tests/run.py test_private_terms` → exit 0 · Ran 2 tests in 0.9s (1 jobs, 16 at a time; slowest: PrivateTerms 0s) / OK [ran] [tree 2dcc1db04994] [world 2f1906870a] (2026-11-07T04:55:25Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 2dcc1db04994] (2026-11-07T04:55:25Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 2dcc1db04994] (2026-11-07T04:55:25Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 2dcc1db04994] (2026-11-07T04:55:25Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 2dcc1db04994] (2026-11-07T04:55:25Z)
## Log
- 2026-11-07T02:25:02Z created
- 2026-11-07T02:29:23Z set tier=S, type=SECURITY
- 2026-11-07T02:29:23Z planned: it has criteria and steps
- 2026-11-07T02:29:30Z lane: ~/.claude/foreman.lanes/T-3574 on foreman/T-3574
- 2026-11-07T02:29:33Z focused
- 2026-11-07T02:29:34Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T02:40:33Z dry run of the new naming over the tracked mirror names: exactly 3 renamed (T-1297, T-2094, T-2769 → home-user), no innocent renames, 0 left holding the login or a word term; commit 479c9d47b
- 2026-11-07T02:47:06Z steer: review shoulds fixed in 13777b7e5 (host glob swallows one label, cut-short terms 4+ chars, research names via the namer with import mapping back); dry run over git ls-files .sampo: 5 renamed (3 home-user, 2 cut private-term), 0 innocent
- 2026-11-07T04:14:53Z merged foreman/T-3574 in merge train
- 2026-11-07T04:24:25Z verified: the full suite is green on 020346f6d, which contains 639230900
- 2026-11-07T04:55:15Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'plugin/lib/sampo/sync.py', 'plugin/tests/test_sync.py']
- 2026-11-07T04:55:15Z scope: widened at merge to the reviewed lane's own diff (639230900), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T04:55:58Z done
- 2026-11-07T04:56:01Z committed 87ca33441 (68 files)
- 2026-11-07T04:56:03Z lane removed: ~/.claude/foreman.lanes/T-3574; dropped: merged and closed
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- T-3508 [SECURITY M, done, 2 steps] The public .sampo mirror redacts home paths and private hosts (user@host, 100.x addresses) and its README says sampo sync — lesson: Wh…
- decision 2026-11-06: Sync is off until T-3342 (.sampo mirror rename) lands: main's old code exports to an untracked .foreman/ while .sampo/ is tracked, and the import si…
## Measurements
tracked mirror paths holding the home-folder form: 3 → 0 after a re-export (dry run of the rules over git ls-files .sampo)
## Lessons
- Redacting a public copy has to cover its paths as well as its contents, and a name made from user text needs the same rules in the name's own form: slugged, split into words, and possibly cut short.
## Plan gaps
- failed first: step 1 failing test: home in a brief's name is redacted on export, old name removed, round-trip import
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/sync.py
- plugin/tests/test_sync.py
