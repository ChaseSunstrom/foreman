---
id: T-3279
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/repro.py, plugin/lib/fmrepro.py, plugin/tests/test_repro.py, plugin/lib/sampo/cli.py, MASTER.md, docs/map/files-lib-3.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:28:08Z
updated: 2026-11-06T06:12:23Z
builder_model: haiku
base: 00b285292666f4610b278fc83fe59c924ac22197
base_tree: b7ea42c9d13afdcf0443d2a19c881e825efa8a91
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:28:52Z
plan0_scope: [plugin/lib/sampo/repro.py, plugin/tests/test_repro.py, plugin/lib/sampo/cli.py, CHANGELOG.md]
builder_returned: 2026-11-06T04:32:17Z
lane_stop: merged 2026-11-06T05:44:30Z
---
# Moon C-002103: sampo repro builds site and README figures twice and from the parent commit, names nondeterministic and changed files
## Raw request
> Moon C-002103: sampo repro builds site and README figures twice and from the parent commit, names nondeterministic and changed files
## Interpretation
Reading 1 (chosen): a dev command that builds Sampo's generated artifacts (site via site/build.py, README figures via demo/readme_figures.py) twice from the working tree and once from a REF worktree, and diffs, so timestamps/ordering nondeterminism and unintended output changes are named before a commit. Reading 2 (ruled out): a phone-side release verifier against two independent build machines, because Sampo has no release artifact hosting and that is not about editing Sampo. Partial: test_site_build.py:40 already proves the site is byte-identical twice, but only in the test run, with no figures, no genesis, and no diff against the parent. genesis.json (rune.export) needs the user's state, so it is left out.
## Assumptions (confidence)
## Acceptance criteria
- [x] repro.diff_trees(a,b) returns the added, removed and changed relative paths of two directories, and nondeterministic = diff of two builds of one tree — verify with `python3 plugin/tests/run.py test_repro`
- [x] sampo repro [--ref REF] builds site/build.py and demo/readme_figures.py twice from the working tree and once from a git worktree of REF (default HEAD), prints 'nondeterministic: N file(s)' and 'changed vs REF: N file(s)' with names, exit 1 only when nondeterministic — verify with `python3 plugin/tests/run.py test_repro`
- [x] the verb is registered in cli.py and listed by sampo which — verify with `python3 plugin/tests/run.py test_repro`
## Non-goals
## Approach (options → choice → why)
1. New module repro.py with diff_trees and a verb; builders run as subprocesses into temp dirs; the REF build uses git worktree add on a temp dir. Likely outcome: small, no big-file collisions, works on any commit.
2. Extend test_site_build.py with a parent diff. Likely outcome: only tests, nobody runs it before a commit, no figures.
3. Hash tracked outputs into a manifest committed to the repo. fails if: every source edit then churns the manifest and lanes conflict in it.
4. Do less: only a verb that builds the site twice and diffs. Likely outcome: duplicates the existing test, misses figures and the parent comparison.

Choice 1 (85%): smallest new surface, covers both generated artifacts and the parent diff. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [x] Write plugin/tests/test_repro.py first: diff_trees on temp dirs, and repro.run on a tiny temp git repo with a fake builder command
2. [x] Add plugin/lib/sampo/repro.py: diff_trees, build(root,out) running the two builders, run(ref); cmd(args)
3. [x] Register 'repro' with lazy('sampo.repro','cmd') beside which in cli.py; CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-06T02:46:31Z step 3/3: Register 'repro' with lazy('sampo.repro','cmd') beside which in cli.py; CHANGELOG line
- git: worktree-agent-a43cfbb02f63ce9c4; 6 uncommitted: MASTER.md, docs/map/files-lib-3.md, plugin/lib/sampo/cli.py, plugin/lib/fmrepro.py, plugin/lib/sampo/repro.py, plugin/tests/test_repro.py
- touched since last checkpoint: plugin/lib/sampo/repro.py, plugin/lib/fmrepro.py, plugin/lib/sampo/cli.py, plugin/tests/test_repro.py, MASTER.md, docs/map/files-lib-3.md
## Docs impact
MASTER.md bullet and docs/map/files-lib-3.md line added by the builder; the verb's help names its cost
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_repro` → ✗ exit 1 (never ran: no tests ran) · Ran 1 tests in 49.4s (2 jobs, 16 at a time; slowest: Repro 44s, loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (ran] (tree 3542fd3cabf3] (world 2f1906870a] (2026-11-06T02:35:21Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_repro` → ✗ exit 1 · Ran 17 tests in 125.9s (5 jobs, 16 at a time; slowest: Repro 109s, Run 20s, Cmd 14s) / FAILED (2 classes: test_repro.Cmd, test_repro.Verb) (ran] (tree 474a41f945c5] (world 2f1906870a] (2026-11-06T02:40:03Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_repro` → ✗ exit 1 · Ran 17 tests in 165.4s (15 jobs, 16 at a time; slowest: Repro 156s, Verb.test_the_verb_is_registered_and_sampo_which_lists_it 13s, Run.test_a_deterministic_build_names_what_differs_from_the_parent_com (ran] (tree 634d5c6d0198] (world 2f1906870a] (2026-11-06T02:43:04Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_repro` → ✗ exit 1 · Ran 17 tests in 128.0s (15 jobs, 16 at a time; slowest: Repro 120s, Run.test_a_deterministic_build_names_what_differs_from_the_parent_commit 15s, Cmd.test_a_change_against_ref_alone_exits_0_and_names_ (ran] (tree 9257f3d3ab17] (world 2f1906870a] (2026-11-06T02:46:04Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_repro` → exit 0 · Ran 18 tests in 242.2s (18 jobs, 16 at a time; slowest: Repro 225s, Verb.test_the_verb_is_registered_and_sampo_which_lists_it 24s, Cmd.test_a_change_against_ref_alone_exits_0_and_names_the_ref 16s) / (ran] (tree 591d4e820be0] (world 2f1906870a] (2026-11-06T02:58:30Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_design_tokens test_design_works test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_kalevala test_left_out test_library test_louhi_models test_mcp test_mint test_models test_moons_scale test_parallel test_proof test_rename_scan test_repro test_scaffold test_self_aware test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2394 tests in 1236.8s (718 jobs, 16 at a time; slowest: Proof 338s, TaskLifecycle 335s, LeanKindGateHookDelay 277s) / FAILED (3 classes: test_design_works.StaticGates, test_hooks.NoTaskGateMulti, (ran] (tree 591d4e820be0] (world 2f1906870a] (2026-11-06T03:19:25Z)
- (step 3) `PYTHON_CPU_COUNT=2 nice -n 10 python3 plugin/tests/run.py test_repro` → exit 0 · Ran 22 tests in 34.6s (16 jobs, 2 at a time; slowest: Repro 24s, Smoke 18s, Cmd 5s) / OK (ran] (tree bb65f7f815e0] (world 2f1906870a] (2026-11-06T04:32:11Z)
- (audit self, imported) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings (tree 32cd4bb50aec] (2026-11-06T05:44:36Z)
- (ac 1) `python3 plugin/tests/run.py test_repro` → exit 0 · Ran 22 tests in 51.4s (7 jobs, 16 at a time; slowest: Smoke 7s, Repro 4s, Run 1s) / OK (ran] (tree 32cd4bb50aec] (world 2f1906870a] (2026-11-06T05:45:46Z)
- (ac 2) `python3 plugin/tests/run.py test_repro` → exit 0 · Ran 22 tests in 51.4s (7 jobs, 16 at a time; slowest: Smoke 7s, Repro 4s, Run 1s) / OK (ran] (tree 32cd4bb50aec] (world 2f1906870a] (2026-11-06T05:45:46Z)
- (ac 3) `python3 plugin/tests/run.py test_repro` → exit 0 · Ran 22 tests in 51.4s (7 jobs, 16 at a time; slowest: Smoke 7s, Repro 4s, Run 1s) / OK (ran] (tree 32cd4bb50aec] (world 2f1906870a] (2026-11-06T05:45:46Z)
- (audit intent, imported) `lane review before merge (fm-reviewer, FIX FIRST), findings fixed in round 2 (8dfea91); self audit after the merge` → reviewer checked each criterion against its test; the JSON flag and real-builder smoke test were added in round 2 (tree 32cd4bb50aec] (2026-11-06T05:45:46Z)
- (audit edge, imported) `lane review before merge (fm-reviewer, FIX FIRST), findings fixed in round 2 (8dfea91); self audit after the merge` → a hung git is now ReproError (exit 2), not nondeterminism; cleanup still runs with check=False (tree 32cd4bb50aec] (2026-11-06T05:45:46Z)
- (audit self, imported) `the only change since the merge: two '# not a list:' notes on repro.py's git error lines (the silent-cut scan); test_left_out and test_repro pass` → no findings (tree cf8b91a753d4] (2026-11-06T06:12:19Z)
- (audit intent, imported) `lane review before merge (fm-reviewer, FIX FIRST), findings fixed in round 2; self audit after the last change` → reviewer checked each criterion against its test; the JSON flag and real-builder smoke test were added in round 2 (tree cf8b91a753d4] (2026-11-06T06:12:23Z)
- (audit edge, imported) `lane review before merge (fm-reviewer, FIX FIRST), findings fixed in round 2; self audit after the last change` → a hung git is now ReproError (exit 2), not nondeterminism; cleanup still runs with check=False (tree cf8b91a753d4] (2026-11-06T06:12:23Z)
## Log
- 2026-11-06T02:28:08Z created
- 2026-11-06T02:28:15Z set scope=['plugin/lib/sampo/repro.py', 'plugin/tests/test_repro.py', 'plugin/lib/sampo/cli.py', 'CHANGELOG.md']
- 2026-11-06T02:28:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3279.builder.md
- 2026-11-06T02:28:51Z focused
- 2026-11-06T02:28:52Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-06T02:37:41Z set scope=['plugin/lib/sampo/repro.py', 'plugin/lib/fmrepro.py', 'plugin/tests/test_repro.py', 'plugin/lib/sampo/cli.py', 'MASTER.md', 'docs/map/files-lib-3.md', 'CHANGELOG.md']
- 2026-11-06T02:37:44Z scope widened: the standing rule for a new plugin/lib module needs its fm shim (fmrepro.py), a MASTER.md bullet and a docs/map line
- 2026-11-06T05:44:30Z merged worktree-agent-a43cfbb02f63ce9c4 (6 file(s))
- 2026-11-06T05:44:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a43cfbb02f63ce9c4
- 2026-11-06T05:44:32Z focused
- 2026-11-06T06:10:18Z focused
- 2026-11-06T06:12:13Z scope: repro.py's two git error lines get '# not a list:' notes (test_left_out's silent-cut scan flagged ' '.join(args[:2]))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- decision 2026-11-05: [costly] Parked T-3006 at a one-way, ambiguous step: failing tests with a fake model: the state message, the deliberate trigger, the check-before-ed…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
## Preflight
Changed in scope since this was planned (2026-11-06): CHANGELOG.md, MASTER.md, docs/map/files-lib-3.md, plugin/lib/fmrepro.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/repro.py, plugin/tests/test_repro.py; re-ground the plan against them before editing
