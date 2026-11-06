---
id: T-1962
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T10:17:49Z
updated: 2026-10-29T10:26:36Z
batch: [T-1959, T-1960, T-1961]
base: 735fb29e30d45955e24a32e343cfb7f866c5225d
base_tree: e13fd27ddd437fa4e3a1ba742154ae6f3ee8d988
plan0_at: 2026-10-29T10:18:00Z
plan0_scope: []
verified: strong
---
# round 11: fm task step edit/rm, fm ship --check, fm gates ID in focus
## Raw request
> T-1959: FEATURE: fm task step ID edit N "<text>" and fm task step ID rm N, like fm task ac ID edit, so a batch's copied member steps or a stale plan change without rewriting the whole Steps section by hand
> DONE-WHEN: fm task step ID edit 2 "x" renames step 2 and fm task step ID rm 3 removes step 3, renumbering the rest
> T-1960: FEATURE: fm ship --check [shas] exits 0 when the remote's main holds those commits' changes (by patch, as the default pick does) and 1 naming the ones it lacks, so a ship task verifies without a git log -n3 | grep that a later ship pushes out of view
> DONE-WHEN: fm ship --check exits 0 after a ship and 1 before it, without the publish grant
> T-1961: FEATURE: fm focus's "Done needs: … (fm gates)" line names the task (fm gates T-1234), now that fm gates takes an id
> DONE-WHEN: fm focus prints fm gates with the focused id
## Interpretation
Three small CLI gaps hit in use this session; tier S each: mirror task ac edit for steps, reuse ship's git cherry for --check, and fill the id into one focus line.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task step ID edit 2 "x" renames step 2 and rm 3 removes step 3, renumbering the rest — verify with `python3 plugin/tests/run.py test_cli_ergonomics`
- [x] fm ship --check exits 0 after a ship and 1 before it, without the publish grant — verify with `python3 plugin/tests/run.py test_ship`
- [x] fm focus prints fm gates with the focused id — verify with `python3 plugin/tests/run.py test_cli_ergonomics -k gates`
## Non-goals
## Approach (options → choice → why)
Chosen: Brief.edit_step/remove_step in fmcore (refuse when evidence exists at or after the step, since evidence is keyed by step number); ship --check returns before the grant; focus line interpolates target.id. Rejected: step rm that remaps evidence (more code, no need); a separate fm verb for the remote check (fm ship already computes the picks).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: step edit/rm, ship --check, focus names fm gates ID
2. [x] Brief.edit_step/remove_step + fm task step edit|rm
3. [x] fm ship --check [shas]
4. [x] focus Done needs line names the id; docs
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_cli_ergonomics test_ship` → ✗ exit 1 · Ran 17 tests in 9.4s (2 classes, 16 at a time; slowest: Ship 8s, CliErgonomics 2s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 0e515bb5478d] (2026-10-29T10:18:41Z)
- `python3 plugin/tests/run.py test_cli_ergonomics test_ship` → ✗ exit 1 · Ran 17 tests in 8.6s (2 classes, 16 at a time; slowest: Ship 8s, CliErgonomics 2s) / FAILED (2 classes) [ran] [tree 0e515bb5478d] (2026-10-29T10:18:41Z)
- (step 1) `python3 plugin/tests/run.py test_cli_ergonomics test_ship` → exit 0 · Ran 17 tests in 8.9s (2 classes, 16 at a time; slowest: Ship 9s, CliErgonomics 2s) / OK [ran] [tree cf3563789290] (2026-10-29T10:19:47Z)
- (step 2) `python3 plugin/tests/run.py test_cli_ergonomics -k step` → exit 0 · Ran 83 tests in 12.9s (54 classes, 16 at a time; slowest: Stories 8s, Stop 6s, CaptureAndIntake 5s) / OK [ran] [tree cf3563789290] (2026-10-29T10:20:00Z)
- (step 3) `python3 plugin/tests/run.py test_ship -k check` → exit 0 · Ran 207 tests in 13.5s (132 classes, 16 at a time; slowest: Ship 13s, CheckSkip 11s, Bench 8s) / OK [ran] [tree cf3563789290] (2026-10-29T10:20:14Z)
- (step 4) `python3 plugin/tests/run.py test_cli_ergonomics -k gates` → exit 0 · Ran 68 tests in 15.6s (24 classes, 16 at a time; slowest: CloseGates 15s, DiffGates 10s, VerifyStrength 4s) / OK [ran] [tree cf3563789290] (2026-10-29T10:20:30Z)
- (ac 1) `python3 plugin/tests/run.py test_cli_ergonomics` → exit 0 · Ran 4 tests in 2.3s (1 classes, 16 at a time; slowest: CliErgonomics 2s) / OK [ran] [tree e85e4d01927f] (2026-10-29T10:26:06Z)
- (ac 2) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 13 tests in 8.9s (1 classes, 16 at a time; slowest: Ship 9s) / OK [ran] [tree e85e4d01927f] (2026-10-29T10:26:06Z)
- (ac 3) `python3 plugin/tests/run.py test_cli_ergonomics -k gates` → exit 0 · Ran 68 tests in 15.5s (24 classes, 16 at a time; slowest: CloseGates 15s, DiffGates 10s, VerifyStrength 4s) / OK [ran] [tree e85e4d01927f] (2026-10-29T10:26:06Z)
- `python3 plugin/tests/run.py test_cli_ergonomics test_ship` → exit 0 · Ran 17 tests in 8.8s (2 classes, 16 at a time; slowest: Ship 9s, CliErgonomics 2s) / OK [ran] [tree e85e4d01927f] (2026-10-29T10:26:06Z)
- (audit edge) `self: read the diff; step rm rewrites lines in place with the old order matching steps(); edit/rm refused once evidence sits at or after the step (evidence is keyed by step number); ship --check returns before the grant and passes only rev-parsed shas to git cherry; renamed the step events off step_edit, which the hook counts as file edits` → rm of the current step moves CURRENT to the next undone one; rm 9 is a usage error; edit of a done step is refused (done steps carry evidence) [tree e85e4d01927f] (2026-10-29T10:26:06Z)
- (audit adversary) `self: read the diff; step rm rewrites lines in place with the old order matching steps(); edit/rm refused once evidence sits at or after the step (evidence is keyed by step number); ship --check returns before the grant and passes only rev-parsed shas to git cherry; renamed the step events off step_edit, which the hook counts as file edits` → commit subjects go through c.plain and c.fit; --remote reading as an option is still refused before --check [tree e85e4d01927f] (2026-10-29T10:26:06Z)
- (audit self) `self: read the diff; step rm rewrites lines in place with the old order matching steps(); edit/rm refused once evidence sits at or after the step (evidence is keyed by step number); ship --check returns before the grant and passes only rev-parsed shas to git cherry; renamed the step events off step_edit, which the hook counts as file edits` → no findings [tree e85e4d01927f] (2026-10-29T10:26:06Z)
## Log
- 2026-10-29T10:17:49Z created
- 2026-10-29T10:17:58Z set tier=S
- 2026-10-29T10:17:59Z focused
- 2026-10-29T10:26:35Z done
- 2026-10-29T10:26:36Z committed ea0663cd (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1957 [FEATURE S, done, 4 steps] fm CLI round 10: task new --json --focus, fm gates ID, finish --numbers
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- similar finished tasks took 2–4 steps
## Files touched
- plugin/tests/test_cli_ergonomics.py
- plugin/tests/test_ship.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmrecall.py
