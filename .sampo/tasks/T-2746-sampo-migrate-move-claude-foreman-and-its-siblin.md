---
id: T-2746
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T00:58:09Z
updated: 2026-11-03T01:42:40Z
builder_model: sonnet
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-03T00:58:31Z
plan0_scope: []
lane_stop: merged 2026-11-03T01:39:40Z
inferred_deps: [T-2742]
inferred_why: T-2742: named in its request
group: Sampo rename and its steps
base: c4b45466d72df6af7ff14c65701f61d03aa086de
base_tree: de2380a15cdadc8376d8fc1ebbd2e7d770dc9151
verified: strong
unproven: [docs]
---
# sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave symlinks at the old paths, keep a backup of the record and a manifest, rerun safely, resume a half-done move, and undo exactly with --undo (T-2742 step 3)
## Raw request
> sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave symlinks at the old paths, keep a backup of the record and a manifest, rerun safely, resume a half-done move, and undo exactly with --undo (T-2742 step 3)
## Interpretation
Reading 1 (chosen): SAMPO.md's Paths and state: on first launch of the renamed build, move (not copy) the Foreman home to ~/.claude/sampo with its siblings, symlink the old paths so every absolute path in settings, links, worktrees' gitdir files and state still resolves, back up the record first (fmrollback._tar_record's pattern: ledgers, briefs, research, meta, not exam work copies), record a manifest with hashes, be idempotent, resume a crash mid-way, and undo exactly. This task builds the verb and its tests; wiring it to first launch comes with the visible surfaces. Reading 2 (ruled out): copy state to the new home and leave the old one. Ruled out: SAMPO.md says move, and two homes would split new writes.
## Assumptions (confidence)
## Acceptance criteria
- [x] on a temp home laid from a real upgrade snapshot (or a synthetic one when none exists), migrate moves the home and siblings, leaves symlinks, writes the manifest and a backup, and the restore drill's checks (ledger chain, fsck, state, outcomes) pass through the new path — verify with `python3 plugin/tests/run.py test_migrate`
- [x] a second run changes nothing; a run killed after the move but before the symlink finishes on rerun; --undo restores the old layout byte for byte (hashes in the manifest) and removes the symlinks; a sensitive project is still sensitive after migrating — verify with `python3 plugin/tests/run.py test_migrate`
## Non-goals
## Approach (options → choice → why)
1. fmmigrate.py with phases recorded in the manifest before each one (backup, move each folder with os.rename, symlink, done); a rerun reads the manifest and resumes at the first unfinished phase; --undo reverses the phases from the manifest and checks the hashes; HOME-relative paths so tests run in a temp home. Likely outcome: one module, one verb, one test file. Fails if: source and destination are on different filesystems (os.rename fails); then it refuses and says why rather than copying 3.4 GB.
2. Copy with shutil.copytree, then remove the source. Fails if: 3.4 GB copies slowly and a crash mid-copy leaves two partial homes.
3. Use what exists: fmrollback._tar_record for the backup, fmdrill.restore's checks for the readback, fm drill --restore's temp-home pattern for the test. Likely outcome: no new backup or check code.
4. Do less: only a symlink ~/.claude/sampo -> ~/.claude/foreman. Fails if: SAMPO.md asks for a move with the symlink at the old path, so new installs are pure Sampo.
Choice 1 on 3 (80%).
## Risks and rollback
It moves the folder this repo and the live state live in; it never runs here until the user's first launch of the renamed build, and only after a backup; --undo restores from the manifest. Tests run only in temp homes. Different filesystems: refuse, never copy.
Blast radius (fm graph blast): unknown, no co-change history for SAMPO.md.
## Execution prompt
## Steps
1. [x] red tests on a temp home
2. [x] fmmigrate.py: plan, backup, move, symlink, manifest, resume, undo
3. [x] the fm migrate verb (sampo migrate once T-2745 lands)
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_migrate` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.3s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree 23a44265d686] [world 2f1906870a] (2026-11-03T00:59:43Z)
- (ac 1) `python3 plugin/tests/run.py test_migrate 2>&1 | tail -25` → ✗ exit 1 · Ran 8 tests in 13.3s (1 classes, 16 at a time; slowest: Migrate 13s) / FAILED (1 classes: test_migrate.Migrate) [ran] [tree f5e50a2163d9] [world 2f1906870a] (2026-11-03T01:00:16Z)
- (ac 2) `python3 plugin/tests/run.py test_migrate 2>&1 | tail -25` → ✗ exit 1 · Ran 8 tests in 13.3s (1 classes, 16 at a time; slowest: Migrate 13s) / FAILED (1 classes: test_migrate.Migrate) [ran] [tree f5e50a2163d9] [world 2f1906870a] (2026-11-03T01:00:16Z)
- (step 2) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 14.7s (1 classes, 16 at a time; slowest: Migrate 14s) / OK [ran] [tree 3f593ed71e6c] [world 2f1906870a] (2026-11-03T01:00:48Z)
- (step 3) `python3 plugin/bin/fm migrate --help` → exit 0 · manifest's hashes / --dry-run             show the steps; change nothing [ran] [tree 3f593ed71e6c] [world 2f1906870a] (2026-11-03T01:00:49Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_migrate test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 211 tests in 23.4s (52 classes, 16 at a time; slowest: TaskLifecycle 23s, Migrate 16s, VerifyStrength 15s) / FAILED (1 classes: test_board_verbs.BoardVerbs) [ran] [tree 3f593ed71e6c] [world 2f1906870a] (2026-11-03T01:01:12Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_guard_cases test_migrate test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.43s] [ran] [tree 0283a76613a8] [world 2f1906870a] (2026-11-03T01:02:13Z)
- (ac 1) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 16.1s (1 classes, 16 at a time; slowest: Migrate 16s) / OK [ran] [tree 5da01c9c8bc6] [world 2f1906870a] (2026-11-03T01:40:10Z)
- (ac 2) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 14.1s (1 classes, 16 at a time; slowest: Migrate 14s) / OK [ran] [tree 5da01c9c8bc6] [world 2f1906870a] (2026-11-03T01:40:25Z)
- (step 1) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 14.3s (1 classes, 16 at a time; slowest: Migrate 14s) / OK [ran] [tree 5da01c9c8bc6] [world 2f1906870a] (2026-11-03T01:40:40Z)
- (step 2) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 13.5s (1 classes, 16 at a time; slowest: Migrate 13s) / OK [ran] [tree 5da01c9c8bc6] [world 2f1906870a] (2026-11-03T01:40:54Z)
- (step 3) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 13.3s (1 classes, 16 at a time; slowest: Migrate 13s) / OK [ran] [tree 5da01c9c8bc6] [world 2f1906870a] (2026-11-03T01:41:07Z)
- (ac 1) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 13.9s (1 classes, 16 at a time; slowest: Migrate 14s) / OK [ran] [tree fd1ccc3fce88] [world 2f1906870a] (2026-11-03T01:41:56Z)
- (ac 2) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 13.9s (1 classes, 16 at a time; slowest: Migrate 14s) / OK [ran] [tree fd1ccc3fce88] [world 2f1906870a] (2026-11-03T01:41:56Z)
- `python3 plugin/tests/run.py test_migrate test_rename_scan` → exit 0 · Ran 10 tests in 13.6s (2 classes, 16 at a time; slowest: Migrate 13s, RenameScan 0s) / OK [ran] [tree fd1ccc3fce88] [world 2f1906870a] (2026-11-03T01:41:56Z)
- (audit adversary) `read fmhomemove: steps are decided from disk, so a kill at any point resumes; os.rename only, a cross-filesystem OSError refuses; tree_hash per folder in the manifest makes --undo verifiable; the user approved the new verb (fm ask core); review added the agent-session refusal (only --dry-run when harness() isn't a person's shell), tested` → an agent can't move the home: cmd_migrate refuses any non-dry run under claude-code, fm-code or exam, and unsetting CLAUDECODE is already a guard refusal (self-authorize) [tree fd1ccc3fce88] (2026-11-03T01:41:56Z)
- (audit edge) `read fmhomemove: steps are decided from disk, so a kill at any point resumes; os.rename only, a cross-filesystem OSError refuses; tree_hash per folder in the manifest makes --undo verifiable; the user approved the new verb (fm ask core); review added the agent-session refusal (only --dry-run when harness() isn't a person's shell), tested` → files written during a migration could fail undo's hash check (no lock; noted); the backup covers the record, not the draft, evolve and lanes siblings, which are moved, not changed [tree fd1ccc3fce88] (2026-11-03T01:41:56Z)
- (audit intent) `read fmhomemove: steps are decided from disk, so a kill at any point resumes; os.rename only, a cross-filesystem OSError refuses; tree_hash per folder in the manifest makes --undo verifiable; the user approved the new verb (fm ask core); review added the agent-session refusal (only --dry-run when harness() isn't a person's shell), tested` → SAMPO.md's Paths and state: move not copy, symlink at the old path, idempotent, a backup, a manifest the way install-user keeps one, undone by --undo; first-launch wiring comes with the visible surfaces [tree fd1ccc3fce88] (2026-11-03T01:41:56Z)
## Log
- 2026-11-03T00:58:09Z created
- 2026-11-03T00:58:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2746.builder.md
- 2026-11-03T00:58:30Z focused
- 2026-11-03T00:58:31Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-03T01:03:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7e54ff36c381475e (branch worktree-agent-a7e54ff36c381475e kept: not merged)
- 2026-11-03T01:03:49Z focused
- 2026-11-03T01:38:17Z user approved core in Claude Code's permission prompt
- 2026-11-03T01:38:27Z paused: focus moved to T-2742
- 2026-11-03T01:38:28Z lane: ~/.claude/foreman.lanes/T-2746 on foreman/T-2746
- 2026-11-03T01:39:40Z merged worktree-agent-a7e54ff36c381475e (4 file(s))
- 2026-11-03T01:39:51Z lane removed: ~/.claude/foreman.lanes/T-2746 (branch foreman/T-2746 kept: not merged)
- 2026-11-03T01:39:52Z focused
- 2026-11-03T01:41:08Z scope: MASTER.md (fmhomemove's entry, the doctor's self-docs check), CHANGELOG.md; the module is fmhomemove.py since fmmigrate.py holds fm prove --migration's runners
- 2026-11-03T01:41:27Z scope: MASTER.md (the entry reworded so the rename ratchet doesn't rise)
- 2026-11-03T01:42:37Z done
- 2026-11-03T01:42:40Z committed 70f2b836 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, active, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; …
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- T-2568 [FEATURE M, done, 4 steps] fm tidy --apply prunes graded exam runs' work copies past 14 days, keeping the newest run per tier and agent, answers, grades and keys …
- T-2745 [SECURITY M, active, 3 steps] Ward knows Sampo: the guard treats sampo (and plugin/bin/sampo) exactly as fm, sampo* modules as fm* ones, SAMPO_STATE, SAMPO_HOME a…
## Lessons
- A verb that moves or deletes the user's own files refuses inside an agent session except as a dry run; a new verb also passes the self-change gate, so ask for the core yes before the lane is removed
## Plan gaps
- failed first: step 1 red tests on a temp home
## Files touched
- plugin/tests/test_migrate.py
- plugin/lib/fmhomemove.py
- plugin/lib/fmcli.py
- MASTER.md
