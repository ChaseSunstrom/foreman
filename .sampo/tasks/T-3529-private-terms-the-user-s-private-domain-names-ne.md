---
id: T-3529
type: SECURITY
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, README.md, docs/map/ops-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/doctor.py, plugin/lib/sampo/models.py, plugin/lib/sampo/release.py, plugin/lib/sampo/sync.py, plugin/tests/helpers.py, plugin/tests/test_doctor.py, plugin/tests/test_louhi_models.py, plugin/tests/test_models_systemone.py, plugin/tests/test_private_terms.py, plugin/tests/test_ship.py, plugin/tests/test_sync.py]
depends_on: []
source: user
created: 2026-11-06T19:33:25Z
updated: 2026-11-07T00:42:53Z
base: 483ea8c998fcabcdbad613d057b6da06eed34146
base_tree: 8d82ac7ab38937b5a64f2ab3af4b2c2fdfd175da
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T19:42:33Z
plan0_scope: []
lane_stop: merged 2026-11-07T00:04:53Z
verified: strong
unproven: [docs]
---
# Private terms: the user's private domain names never reach the repo: sampo private add TERM (kept in state, outside git), the mirror export redacts them, and sampo ship refuses a push that carries one
## Raw request
> Private terms: the user's private domain names never reach the repo: sampo private add TERM (kept in state, outside git), the mirror export redacts them, and sampo ship refuses a push that carries one
## Interpretation
Reading 1 (chosen): the user registers private terms locally; every path out of the machine (mirror export, ship push) redacts or refuses them, and tests check configured terms rather than naming one. Reading 2 (ruled out): scrub only today's three occurrences by hand — leaves future leaks unguarded, which the user explicitly asked against.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a private term configured (a host glob like *.home.example.test or a word), sync export writes <host> or <private> in its place and rewrites already-mirrored files once when the terms change, sampo ship refuses a push whose commits or tree carry a term (naming the files, never the term), the term itself is stored only in the state folder and never logged in clear, and no test or code file in the repo contains the user's real term — verify with `python3 plugin/tests/run.py test_private_terms test_sync`
## Non-goals
## Approach (options → choice → why)
1) terms in a git-ignored repo file — fails if: someone force-adds it or the ignore rule drifts; the term ends up committed. 2) terms in an env var — likely outcome: lost between shells, ship and export disagree. 3) use what exists: T-3508's core.redact_local (the mirror's last pass), sync's stamp version, models.secrets_path for the secret env, and core.state_dir() (state/ is git-ignored) — one JSON file there behind sampo private add|rm|list; likely outcome: one loader shared by the export and the ship guard. 4) do less: delete the three literals by hand — fails if: the next brief quotes the endpoint again; nothing stops it. Choice 3 (85%): smallest durable fix, reuses what T-3508 built and release.py's push path.
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for release.py.
## Execution prompt
## Steps
1. [x] sampo private add/rm/list and the redaction in export, test-first
2. [x] ship refuses a push that carries a term
3. [x] the two tests that name the term check the configured terms instead
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_private_terms test_sync` → ✗ exit 1 · ^^^^^^^^^^^^^^^^^^^ / AttributeError: module 'sampo.core' has no attribute 'private_terms' [ran] [tree 8e3bdb87b904] [world 2f1906870a] (2026-11-06T19:42:46Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_private_terms test_sync` → exit 0 · Ran 38 tests in 26.3s (37 jobs, 16 at a time; slowest: Sync.test_explicit_off_is_respected_and_checkpoints_ignore_the_mirror 2s, Sync.test_a_failed_move_commit_keeps_uncommitted_mirror_edits 1s, Sync. [ran] [tree fe90196db69e] [world 2f1906870a] (2026-11-06T19:44:53Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k test_a_private_term_or_a_secret_value test_ship` → ✗ exit 1 · Ran 1 tests in 17.5s (1 jobs, 16 at a time; slowest: Ship 2s) / FAILED (1 classes: test_ship.Ship) [ran] [tree fe90196db69e] [world 2f1906870a] (2026-11-06T19:45:15Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_ship test_release` → exit 0 · Ran 103 tests in 6.5s (81 jobs, 16 at a time; slowest: BoardVerbs 5s, Release.test_the_canary_runs_detached_and_its_failure_lands_in_the_inbox_and_the_notify_hook 4s, ReleaseProof 3s) / OK [ran] [tree 9c6aa7741a60] [world 2f1906870a] (2026-11-06T19:48:57Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_louhi_models test_models_systemone test_models test_secrets` → exit 0 · Ran 130 tests in 4.8s (38 jobs, 16 at a time; slowest: Bench 4s, ModelBenchVisible 4s, LouhiModels.test_a_failing_backend_counts_errors_and_a_second_run_appends_a_new_run 3s) / OK [ran] [tree 9c6aa7741a60] [world 2f1906870a] (2026-11-06T19:49:02Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py -k test_the_private_scan_never_puts test_ship` → ✗ exit 1 · Ran 1 tests in 0.7s (1 jobs, 16 at a time; slowest: Ship 0s) / FAILED (1 classes: test_ship.Ship) [ran] [tree d802bdd29574] [world 2f1906870a] (2026-11-06T19:56:41Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_private_terms test_ship test_release` → exit 0 · Ran 106 tests in 6.0s (84 jobs, 16 at a time; slowest: BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home 4s, Release.test_the_canary_runs_detached_and_its_failure_lands_in_the_inb [ran] [tree 422817a199a4] [world 2f1906870a] (2026-11-06T19:57:22Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -k test_self_docs_and_the_file_map_read test_doctor` → ✗ exit 1 · Ran 1 tests in 16.5s (1 jobs, 16 at a time; slowest: CodeTreeDocs 0s) / FAILED (1 classes: test_doctor.CodeTreeDocs) [ran] [tree 0aae99098e8b] [world 2f1906870a] (2026-11-06T21:52:05Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py -k test_self_docs_and_the_file_map_read test_doctor` → exit 0 · Ran 1 tests in 133.4s (1 jobs, 16 at a time; slowest: CodeTreeDocs 1s) / OK [ran] [tree b2fde73cb8dd] [world 2f1906870a] (2026-11-06T22:02:18Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 6f488664b88c] (2026-11-07T00:04:55Z)
- (ac 1) `python3 plugin/tests/run.py test_private_terms test_sync` → exit 0 · Ran 38 tests in 8.8s (3 jobs, 16 at a time; slowest: Sync 8s, PrivateTerms 0s, BoardSurfaces 0s) / OK [ran] [tree 6f488664b88c] [world 2f1906870a] (2026-11-07T00:05:06Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 6f488664b88c] (2026-11-07T00:05:06Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 6f488664b88c] (2026-11-07T00:05:06Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 6f488664b88c] (2026-11-07T00:05:06Z)
## Log
- 2026-11-06T19:33:25Z created
- 2026-11-06T19:34:39Z lane: ~/.claude/foreman.lanes/T-3529 on foreman/T-3529
- 2026-11-06T19:42:31Z focused
- 2026-11-06T19:42:33Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-07T00:04:53Z merged foreman/T-3529 in merge train
- 2026-11-07T00:04:55Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'README.md', 'docs/map/ops-1.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/doctor.py', 'plugin/lib/sampo/models.py', 'plugin/lib/sampo/release.py', 'plugin/lib/sampo/sync.py', 'plugin/tests/helpers.py', 'plugin/tests/test_doctor.py', 'plugin/tests/test_louhi_models.py', 'plugin/tests/test_models_systemone.py', 'plugin/tests/test_private_terms.py', 'plugin/tests/test_ship.py', 'plugin/tests/test_sync.py']
- 2026-11-07T00:04:55Z scope: widened at merge to the reviewed lane's own diff (78884c114), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-07T00:10:20Z done
- 2026-11-07T00:10:23Z committed 781b3e69f (1 file)
- 2026-11-07T00:42:53Z lane removed: ~/.claude/foreman.lanes/T-3529; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3508 [SECURITY M, active, 2 steps] The public .sampo mirror redacts home paths and private hosts (user@host, 100.x addresses) and its README says sampo sync
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- similar past tasks were L: consider --tier L
## Measurements
tracked files holding the private domain: 3 → 1 (git grep -l -F over the lane tree; the last is the mirror brief, rewritten by the next export once the term is added)
## Lessons
- A test proving a refusal must assert the refusal's own message, not just a non-zero exit.
## Plan gaps
- failed first: step 1 sampo private add/rm/list and the redaction in export, test-first
- failed first: step 2 ship refuses a push that carries a term
## Files touched
- CHANGELOG.md
- README.md
- docs/map/ops-1.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/doctor.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/release.py
- plugin/lib/sampo/sync.py
- plugin/tests/helpers.py
- plugin/tests/test_doctor.py
- plugin/tests/test_louhi_models.py
- plugin/tests/test_models_systemone.py
- plugin/tests/test_private_terms.py
- plugin/tests/test_ship.py
- plugin/tests/test_sync.py
