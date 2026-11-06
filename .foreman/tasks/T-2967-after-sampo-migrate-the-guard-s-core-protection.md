---
id: T-2967
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T13:36:45Z
updated: 2026-11-04T13:43:30Z
builder_model: haiku
base: befd80f03ebb40e5375235787f3ac5ecca68ae2b
base_tree: eacc37c27e48b8da00147fe240fc36134c7b9315
plan0_at: 2026-11-04T13:37:04Z
plan0_scope: []
lane_stop: merged 2026-11-04T13:41:18Z
verified: strong
---
# After sampo migrate the guard's core protection misses the new real path: ~/.claude/foreman becomes a symlink to ~/.claude/sampo and _is_core, _protected_roots, _standing_covers and classify_write compare literal paths, so an Edit or redirect to ~/.claude/sampo/plugin/lib/fmguard.py is not core (T-2742 audit, blocking); also migrate --undo sticks when the state changed since migrate (homemove._undo raises on tree_hash after renaming back), the deprecation line says 'sampo is now sampo', and homemove reads a SAMPO_HOME mirror_env already popped
## Raw request
> After sampo migrate the guard's core protection misses the new real path: ~/.claude/foreman becomes a symlink to ~/.claude/sampo and _is_core, _protected_roots, _standing_covers and classify_write compare literal paths, so an Edit or redirect to ~/.claude/sampo/plugin/lib/fmguard.py is not core (T-2742 audit, blocking); also migrate --undo sticks when the state changed since migrate (homemove._undo raises on tree_hash after renaming back), the deprecation line says 'sampo is now sampo', and homemove reads a SAMPO_HOME mirror_env already popped
## Interpretation
Reading 1 (chosen): core protection must hold on the home's real path after the migration's symlink, in every check that decides core (classify, protected roots, the standing yes), and the migration's undo must not strand a used home; the two Lows ride along. Reading 2 (ruled out): resolve every path through realpath at the guard's entry; that changes what every other category sees (a lane's confine, state-direct) and widens the change past this gap.
## Assumptions (confidence)
## Acceptance criteria
- [x] with the home migrated (the old path a symlink to the new), every core path written through either the old or the new real path is core, and the standing yes still covers it — verify with `python3 plugin/tests/run.py test_guard test_migrate`
- [x] --undo after the state changed since migrate restores the folders, records undone and warns about the changed hash; a second --undo answers nothing to undo — verify with `python3 plugin/tests/run.py test_migrate`
- [x] fm's deprecation line reads 'fm is now sampo … (fm stays as its alias)' and the test asserts the whole line — verify with `python3 plugin/tests/run.py test_rename_cli`
## Non-goals
## Approach (options → choice → why)
1) Carry realpath(foreman_home) as a second root beside the literal one in the four core checks; tests write through both paths on a migrated temp home. Likely outcome: the bypass closes with a narrow diff. Fails if: another check compares the literal home, which the test through the new path finds.
2) use what exists: state_dirs already realpaths; reuse its helper for the core roots. Likely outcome: the same fix sharing one helper. Fails if: the helper's shape differs; then option 1's second root.
3) do less: refuse a migration until the guard is fixed. Likely outcome: no exposure. Fails if: users who already migrated stay exposed.
Choice 1 (85%): the audit traced the four sites; a second root closes all of them.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: the guard on a migrated home through both paths; undo after a write; the full deprecation line
2. [x] fmguard: the home's realpath as a second root in _is_core, _protected_roots, _standing_covers, classify_write; homemove: undone before the hash check, the check a warning; cli: the line's wording; drop the dead SAMPO_HOME read
## Resume here
## Docs impact
CHANGELOG line (T-2967); the deprecation line's wording
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard test_migrate test_rename_cli test_left_out` → exit 0 · Ran 349 tests in 18.4s (99 classes, 16 at a time; slowest: Migrate 18s, Mutation 10s, GuardAgainstBash 6s) / OK [ran] [tree 00305ec3cb2e] [world 2f1906870a] (2026-11-04T13:39:15Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_migrate test_rename_cli test_left_out` → exit 0 · Ran 349 tests in 18.4s (99 classes, 16 at a time; slowest: Migrate 18s, Mutation 10s, GuardAgainstBash 7s) / OK [ran] [tree 00305ec3cb2e] [world 2f1906870a] (2026-11-04T13:39:33Z)
- `python3 plugin/tests/run.py test_migrate test_rename_cli` → ✗ exit 1 · Ran 17 tests in 18.3s (2 classes, 16 at a time; slowest: Migrate 17s, RenameCli 2s) / FAILED (2 classes: test_migrate.Migrate, test_rename_cli.RenameCli) (start tree + this task's tests) [ran] [tree 00305ec3cb2e] [world 2f1906870a] (2026-11-04T13:41:59Z)
- `python3 plugin/tests/run.py test_migrate test_rename_cli` → exit 0 · Ran 17 tests in 17.1s (2 classes, 16 at a time; slowest: Migrate 17s, RenameCli 2s) / OK [ran] [tree 00305ec3cb2e] [world 2f1906870a] (2026-11-04T13:41:59Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_migrate` → exit 0 · Ran 339 tests in 22.9s (97 classes, 16 at a time; slowest: Migrate 22s, Mutation 14s, GuardAgainstBash 11s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:42:52Z)
- (ac 2) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 10 tests in 17.1s (1 classes, 16 at a time; slowest: Migrate 17s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:42:52Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_cli` → exit 0 · Ran 7 tests in 1.9s (1 classes, 16 at a time; slowest: RenameCli 2s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:42:52Z)
- (audit intent) `the T-2742 five-lens audit found it (adversary, blocking); the builder's test migrates a temp home with the real helper and writes through both paths; I checked the guard's other literal-home sites (a hint message, realpath'd bins, its own state files) and none decides core` → after the move every core path written through the old or the new real path is core, and the standing yes covers plain edits through either but not the guard file or a tree write [tree f99cb9b3d28d] (2026-11-04T13:42:52Z)
- (audit adversary) `the T-2742 five-lens audit found it (adversary, blocking); the builder's test migrates a temp home with the real helper and writes through both paths; I checked the guard's other literal-home sites (a hint message, realpath'd bins, its own state files) and none decides core` → the bypass was a write to ~/.claude/sampo/plugin/... after migration; _homes adds the realpath as a second root in _is_core and _protected_roots, and _standing_covers resolves the written path, so a symlink inside core pointing out now asks rather than passing [tree f99cb9b3d28d] (2026-11-04T13:42:52Z)
- (audit edge) `the T-2742 five-lens audit found it (adversary, blocking); the builder's test migrates a temp home with the real helper and writes through both paths; I checked the guard's other literal-home sites (a hint message, realpath'd bins, its own state files) and none decides core` → --undo after the state changed restores the folders, records undone and warns; a second --undo says nothing to undo [tree f99cb9b3d28d] (2026-11-04T13:42:52Z)
## Log
- 2026-11-04T13:36:45Z created
- 2026-11-04T13:36:54Z set approved=True
- 2026-11-04T13:36:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2967.builder.md
- 2026-11-04T13:37:04Z focused
- 2026-11-04T13:41:18Z merged worktree-agent-a9afcf613c4609662 (5 file(s))
- 2026-11-04T13:41:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9afcf613c4609662
- 2026-11-04T13:41:22Z focused
- 2026-11-04T13:42:08Z scope: fmguard.py (_homes, _is_core, _protected_roots, _standing_covers), homemove.py (_undo, _parent), cli.py's deprecation line, test_migrate, test_rename_cli
- 2026-11-04T13:43:28Z done
- 2026-11-04T13:43:30Z committed a5cd1486 (1 file)
## Follow-ups captured
## Scope
plugin/lib/fmguard.py, plugin/lib/sampo/homemove.py, plugin/lib/sampo/cli.py, plugin/tests/test_guard.py, plugin/tests/test_migrate.py, plugin/tests/test_rename_cli.py
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- decision 2026-10-31: [costly] Parked T-2357 at a one-way, ambiguous step: red tests: staging writes nothing outside state; guard category; install after the yes; uninsta…
## Why not caught
test_migrate checked the move and the undo but never ran the guard on a migrated home; it now writes through both paths
## Lessons
- A migration that leaves a symlink makes every literal path comparison in a guard a bypass: compare realpaths wherever protection is decided
## Files touched
- plugin/tests/test_migrate.py
- plugin/tests/test_rename_cli.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/homemove.py
- plugin/lib/fmguard.py
- CHANGELOG.md
