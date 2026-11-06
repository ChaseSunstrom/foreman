---
id: T-2742
type: FEATURE
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-11-03T00:54:33Z
updated: 2026-11-04T13:55:40Z
base_note: Calibration: this plan states Choice 75% where FEATURE L closes (78) held on the first finish 96% of the time: 21 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T00:55:05Z
rival_split: true
base: 4f7973362e021347d30fb396a1e42e647e6c2066
base_tree: 6e9781b841afcc4c314d46e11c3cac7827d18278
predict_minutes: 14
predict_attempts: 1
plan0_at: 2026-11-03T00:55:28Z
plan0_scope: []
verified: ok
unproven: [data, meaning, typed]
---
# Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a one-time move of ~/.claude/foreman with backup and undo; the plugin, internals and env renamed; a new design system, logo and site
## Raw request
> Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a one-time move of ~/.claude/foreman with backup and undo; the plugin, internals and env renamed; a new design system, logo and site

Also asked (T-2772, done here):
> Sampo reimagined: a new logo and a completely redesigned site (user steer 2026-11-03): four rendered directions (logo, animated hero, sections) to choose from, then the chosen one carried through every page, the logo's variants, the README header and the design tokens, with far richer animation and detail, the site matching the logo's world completely
## Interpretation
Reading 1 (chosen): SAMPO.md, verbatim at the repo root, is the spec. Rename every Foreman name (product, CLI, plugin, internals, env, paths, state, installs, docs, identity, site) to Sampo and its role names, keep every old name working as an alias (fm for at least two releases with one deprecation line a day; FOREMAN_* read; Foreman-Task read forever; old import paths as shims), migrate ~/.claude/foreman to ~/.claude/sampo once on first launch with backup, manifest and undo, keep tower history verbatim (gen-0 never edited), rebuild the identity and site in the forge-meets-machine design system with a cold design review, and queue protected core and outward steps for the user. Reading 2 (ruled out): a display-only rebrand that leaves internals, paths and env as foreman. Ruled out: SAMPO.md says internals included, and paths and env move with fallbacks.
Inventory (2026-11-03): 733 tracked files and 7,851 mentions of foreman; 157 tracked paths named foreman or fm (122 in plugin/lib); 72 FOREMAN_* variables; plugin ids foreman@foreman and foreman-ui@foreman in ~/.claude/settings.json; ~/.local/bin/fm links into the repo; ~/.claude/foreman is both this git checkout and the install home (state 3.4 GB, 23 projects), with siblings foreman.draft, foreman.evolve and foreman.lanes. Classes: rename (CLI, verbs, modules, ids, env, paths, docs, site); alias (fm, old verbs, fm* imports, FOREMAN_*, Foreman-Task, foreman@foreman, /foreman:*, foreman:* agents, ~/.claude/foreman symlink); history (CHANGELOG past entries, gen-0 and past tower records, commit messages, ledgers).
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo runs every verb, the six renamed verbs (smith, rune, moons, louhi, underworld, ward) work, and fm and every old verb still work, printing one deprecation line a day — verify with `python3 plugin/tests/run.py test_rename_cli`
- [x] a copy of this machine's real Foreman home migrates in place (move, symlink at the old path, manifest, backup), a rerun changes nothing, sampo migrate --undo restores it byte for byte, a half-migrated crash resumes, and a sensitive repo stays sensitive — verify with `python3 plugin/tests/run.py test_migrate`
- [x] SAMPO_* variables are read with FOREMAN_* as fallbacks, and the Sampo-Task and Foreman-Task trailers are both read — verify with `python3 plugin/tests/run.py test_rename_env`
- [x] the old fm* module import paths and the plugin ids foreman@foreman and foreman-ui@foreman, the /foreman: commands and the foreman: agents still resolve, as thin aliases — verify with `python3 plugin/tests/run.py test_rename_aliases`
- [x] no user-visible 'Foreman' remains outside history and the alias list (the rename's automatic check) — verify with `python3 plugin/tests/run.py test_rename_scan`
- [x] the Rune tower, exam runs, lineage and every project's ledger read back intact through the new paths after migration — verify with `python3 plugin/tests/run.py test_migrate`
- [x] the full gates pass and the lean check holds: hook latency and injected context are no larger than before — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
1. Aliases first, then staged renames (SAMPO.md's Order): add the sampo entry point, one alias table (verbs, plugin ids, commands, agents, env, trailers) and SAMPO_* with FOREMAN_* fallbacks while every name still works; then the migration with tests on a copy of a real home; then internals module by module with fm sub and a history denylist, each step green and old fm* imports kept as shims; then visible surfaces (protected core built in a worktree and queued); then design tokens, logo, site and docs in parallel lanes. Likely outcome: many commits, each green, nothing broken at any point. Fails if: a module rename misses a dynamic import (lazy('fmx', ...), importlib) and only shows at run time; the answer is a scan test for string module names.
2. Big bang: one fm sub codemod over the tree and one commit. Fails if: 7,851 mentions in 733 files change at once, so a red suite has no bisectable cause and the live session's own plugin breaks mid-change.
3. Use what exists: fm sub (regex codemod with per-file counts), fm edit, fmrollback's snapshot and manifest pattern for the migration's backup, fm install-user's manifest for the undo, fm drill --restore's temp home for testing on a copy, fm looks and the directions skill for the logo, fm shot, fm flow and fm critique for the site. Likely outcome: no new tooling beyond sampo migrate and the alias table.
4. Do less: a display-only rebrand (names on surfaces; internals, env and paths unchanged). Fails if: SAMPO.md requires internals, env and paths renamed with fallbacks.
5. Fork a new Sampo repo and freeze Foreman. Fails if: the user's state, history and installs must carry over in place.
Choice 1 on 3 (75%). The 25% doubt: renaming 122 modules and 419 tests mechanically while the plugin this session runs from is the same tree; each stage runs its affected tests, and the live install keeps working through the shims until the migration moves it. A cold rival read agreed on aliases first, one alias table, a denylist codemod and a separate design track.
## Risks and rollback
The migration moves the folder this repo and 3.4 GB of state live in: it runs only on first launch of the renamed build, keeps a backup (fmrollback's tar pattern) and a manifest, leaves a symlink at ~/.claude/foreman, and sampo migrate --undo restores it exactly; it is tested on a copy of this machine's home before it can run here. A missed rename shows as a red affected test at its own stage; each stage is a separate commit, so git revert undoes one stage alone. Protected core (the guard, hooks.json, rules, evals, BUILD_PROMPT.md, settings) is built in a worktree and queued with fm ask core, never applied unasked; outward steps (the GitHub repo, Pages URL, marketplace listing, Desktop app) are only prepared and listed.
Blast radius (fm graph blast): unknown, no co-change history for SAMPO.md.
## Execution prompt
## Steps
1. [x] Plan: the inventory, each occurrence classified (rename, alias, history), approaches, fm decide
2. [x] Aliases first: the sampo entry point, verb aliases, SAMPO_* with FOREMAN_* fallbacks, trailers; nothing breaks
3. [x] Migration (sampo migrate, --undo) with its tests on a copy of a real home
4. [x] Internals: modules, files, tests renamed mechanically, with old import paths as shims
5. [x] Visible surfaces: plugin ids, commands, skills, agents, output style, rules, statusline, the sampo-ui mod, installers and adapters (protected core built in a worktree, then queued with fm ask core)
6. [x] Design system and three logo directions, cold design review, the chosen logo and every variant
7. [x] The site rebuilt in the design system, every page, with shots at desktop, tablet and phone and the quality bar: carried by T-2788 (the Kirjokansi + forge rebuild, after the user's pick in T-2772)
8. [x] Docs: README, MASTER, INSTALL, CHANGELOG top entry, the one myth paragraph
9. [x] Full fm check, lean check, cold review for any leftover Foreman, outward steps prepared and listed
## Resume here
<!-- auto -->
- 2026-11-04T13:36:44Z steps 9/9 done
- git: foreman/build; 0 uncommitted
- failures met: keyerror: slice(none, 0, none); assertionerror: 0.0 not less than 0 : stopped at its init line, not after the sleep; <img src="live.svg" width="0" alt="claude code 0.0.0 with the sampo-ui mod, working a rea…
## Docs impact
README, INSTALL, MASTER (and its docs/map shards), the CHANGELOG's Highlights, the skills, commands, agents and rules teach sampo spellings; the old names are listed as aliases; the Kalevala paragraph explains the names once
## Verification evidence
- (step 1) `fm task show T-2742 (Interpretation with the inventory, Approach with 5 options, Risks and rollback, rival read resolved, decision recorded)` → planned [tree f2b13010631b] (2026-11-03T00:56:08Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_cli 2>&1 | grep -E "^(FAIL|ERROR|OK|FAILED|Ran)" | head -10` → ✗ exit 1 · FAILED (failures=7) / Ran 6 tests in 2.8s (1 classes, 16 at a time; slowest: RenameCli 2s) [ran] [tree 5af3d96b9e79] [world 2f1906870a] (2026-11-03T02:42:37Z)
- (step 2) `python3 plugin/tests/run.py test_sampo_design 2>&1 | tail -2` → exit 0 · OK [ran] [tree 83b5c05c4dc5] [world 2f1906870a] (2026-11-03T02:43:02Z)
- (step 3) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 8 tests in 35.0s (1 classes, 16 at a time; slowest: Migrate 34s) / OK [ran] [tree 2517e1ebe605] [world 2f1906870a] (2026-11-03T03:45:44Z)
- (step 6) `python3 plugin/tests/run.py test_sampo_design` → exit 0 · Ran 29 tests in 1.7s (4 classes, 16 at a time; slowest: Logo 1s, Directions 0s, Tokens 0s) / OK [ran] [tree 0495ab3d29c2] [world 2f1906870a] (2026-11-03T03:46:51Z)
- (step 4) `T-2748 closed: the library is the sampo package, every fmX import path a shim; its close ran the full suite` → T-2748 done (commit 5ea1ab3b's tree), full suite green at its close [tree 9963cd4d79ca] (2026-11-03T19:56:49Z)
- (step 5) `T-2779, T-2807, T-2808, T-2809, T-2810, T-2768 and T-2775 closed: hook notes, library messages, the UI mod, descriptions, rules, MASTER, skills and completion say Sampo` → all done; their closes ran their tests [tree 9963cd4d79ca] (2026-11-03T19:56:49Z)
- (step 7) `python3 plugin/tests/run.py test_hooks test_board_hooks test_friction 2>&1 | tail -1` → exit 0 · OK [ran] [tree c0f51f67c42f] [world 2f1906870a] (2026-11-04T05:51:03Z)
- (step 8) `python3 plugin/tests/run.py test_docs test_rename_scan` → exit 0 · Ran 121 tests in 11.0s (27 classes, 16 at a time; slowest: Fences 10s, RenameScan 7s, DocsProof 5s) / OK [ran] [tree 2eacbd5fecd0] [world 2f1906870a] (2026-11-04T09:23:51Z)
- (step 7) `python3 plugin/tests/run.py test_site test_site_landing test_site_hero test_site_sections test_genesis test_site_sampo test_site_build` → exit 0 · Ran 292 tests in 19.6s (50 classes, 16 at a time; slowest: GenerationReview 19s, GenesisRead 15s, GenesisSweep 14s) / OK [ran] [tree 4563dfdc5760] [world 2f1906870a] (2026-11-04T12:39:54Z)
- (step 9) `sampo check` → exit 0 · ✓ fm replay → exit 0 · skipped: nothing under plugin/lib/fmguard.py changed since its pass at 11:07 UTC (0.0 s) / ! changed during the gates: CHANGELOG.md, plugin/tests/test_site_hero.py, site/forge.c [ran] [tree eacc37c27e48] [world 2f1906870a] (2026-11-04T13:31:20Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_cli` → exit 0 · Ran 7 tests in 1.9s (1 classes, 16 at a time; slowest: RenameCli 2s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:50:39Z)
- (ac 2) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 10 tests in 18.1s (1 classes, 16 at a time; slowest: Migrate 18s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:50:39Z)
- (ac 3) `python3 plugin/tests/run.py test_rename_env` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: RenameEnv 0s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:50:39Z)
- (ac 4) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 3.8s (1 classes, 16 at a time; slowest: RenameAliases 3s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:50:39Z)
- (ac 5) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 10 tests in 3.7s (1 classes, 16 at a time; slowest: RenameScan 3s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:50:39Z)
- (ac 6) `python3 plugin/tests/run.py test_migrate` → exit 0 · Ran 10 tests in 18.1s (1 classes, 16 at a time; slowest: Migrate 18s) / OK [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:50:39Z)
- (ac 7) `fm check` → exit 0 · gate lock held by sampo check (pid 2004007); waiting / ✓ all 6 gates passed on this exact tree already (run at 13:50 UTC); cached (sampo check --fresh reruns) [ran] [tree f99cb9b3d28d] [world 2f1906870a] (2026-11-04T13:50:39Z)
- (audit intent) `a five-lens fm-reviewer pass over the rename's cross-cutting promises (aliases, migration, the guard text, user-visible leftovers); its one blocking finding (core protection on the migrated real path) fixed test-first in T-2967 with the undo and deprecation-line findings; the step-9 cold review's leftovers fixed in T-2946; two cold design reviews (T-2788)` → sampo and the six renamed verbs work; fm, every old verb, foreman@foreman, /foreman:, foreman: agents, FOREMAN_* and Foreman-Task keep working; the one-time move has a manifest, backup, symlink and undo; README, site and tower say Sampo [tree f99cb9b3d28d] (2026-11-04T13:50:39Z)
- (audit adversary) `a five-lens fm-reviewer pass over the rename's cross-cutting promises (aliases, migration, the guard text, user-visible leftovers); its one blocking finding (core protection on the migrated real path) fixed test-first in T-2967 with the undo and deprecation-line findings; the step-9 cold review's leftovers fixed in T-2946; two cold design reviews (T-2788)` → after the move the guard judged a write through ~/.claude/sampo not core; fixed (T-2967): both paths are core and the standing yes covers both the same way; every reader of the guard's refusal text matches 'Ward: blocked' and 'Foreman guard: blocked' [tree f99cb9b3d28d] (2026-11-04T13:50:39Z)
- (audit edge) `a five-lens fm-reviewer pass over the rename's cross-cutting promises (aliases, migration, the guard text, user-visible leftovers); its one blocking finding (core protection on the migrated real path) fixed test-first in T-2967 with the undo and deprecation-line findings; the step-9 cold review's leftovers fixed in T-2946; two cold design reviews (T-2788)` → a half-migrated crash resumes from its manifest, a rerun changes nothing, a sensitive repo stays sensitive, and --undo after the home was used restores it and warns (T-2967) [tree f99cb9b3d28d] (2026-11-04T13:50:39Z)
- (audit operator) `a five-lens fm-reviewer pass over the rename's cross-cutting promises (aliases, migration, the guard text, user-visible leftovers); its one blocking finding (core protection on the migrated real path) fixed test-first in T-2967 with the undo and deprecation-line findings; the step-9 cold review's leftovers fixed in T-2946; two cold design reviews (T-2788)` → hook latency and injected context held through the rename (sampo check's bench and lean ratchet green; burden 41-77 chars a turn); the migration's tarball and hash are a one-time cost not yet measured at 3.4 GB [tree f99cb9b3d28d] (2026-11-04T13:50:39Z)
- (audit maintainer) `a five-lens fm-reviewer pass over the rename's cross-cutting promises (aliases, migration, the guard text, user-visible leftovers); its one blocking finding (core protection on the migrated real path) fixed test-first in T-2967 with the undo and deprecation-line findings; the step-9 cold review's leftovers fixed in T-2946; two cold design reviews (T-2788)` → one alias table (RENAMES/_alias) feeds the CLI, hooks and scan; test_rename_scan's surface list now covers the guard and READMEs (BASELINE 16, each a reader or a kept protocol string); the release subject stays 'Foreman {v}' on purpose [tree f99cb9b3d28d] (2026-11-04T13:50:39Z)
## Log
- 2026-11-03T00:54:33Z created
- 2026-11-03T00:54:42Z set priority=urgent
- 2026-11-03T00:55:27Z focused
- 2026-11-03T00:55:28Z predicted from its closes: 14 min, 1 attempt(s)
- 2026-11-03T00:56:13Z set approved=True
- 2026-11-03T00:56:58Z plan (ordering, security): the guard matches fm by name; a sampo executable, SAMPO_* variables or new verb names it doesn't know would let an agent reach what it refuses under fm (prove --yes-run, --allow, ask --standing, a FOREMAN_STATE override). So: (a) the guard learns sampo, the new verbs and SAMPO_* first, built in a worktree and queued with fm ask T-2742 core (SAMPO.md: protected core); (b) until the guard says it knows them (a KNOWS_SAMPO constant), plugin/bin/sampo refuses inside an agent session, and SAMPO_* are not read; (c) meanwhile the parts that widen nothing proceed: the migration (tested on a copy), internals with sys.modules shims, the design system, logo and site lanes, docs
- 2026-11-03T00:59:22Z plan (step 4, internals map): a package plugin/lib/sampo/; fmX.py → sampo/X.py, except the roles: fmguard → sampo/ward.py, fmgenesis → rune.py, fmexam → louhi.py, fmmoonshot → moons.py, fmcode → smith.py (and codebench/codemod/codeterm/codetui → smithbench/smithmod/smithterm/smithtui). Each old plugin/lib/fmX.py becomes a two-line shim (import sys; from sampo import X as _m; sys.modules[__name__] = _m) so old imports, private names and mock.patch('fmX.y') hit the same module object. lazy('fmX', ...) strings and importlib names are rewritten too; a scan test finds any string module name left. ForemanTestCase → SampoTestCase with the old name kept. Starts after the T-2745, T-2746 and T-2747 lanes merge (they edit files this moves).
- 2026-11-03T00:59:56Z the rename's check: plugin/tests/test_rename_scan.py, a ratchet over user-visible surfaces (876 lines say Foreman today outside kept aliases); each stage lowers BASELINE; done at 0. The decision's --check names it.
- 2026-11-03T01:01:58Z plan (step 5, plugin ids; claude-code-guide, docs code.claude.com/docs/en/plugins/host-marketplace.md, loading.md, manifest-reference.md): a plugin id is name@marketplace and is the enabledPlugins key; marketplace.json's 'renames' maps old plugin names to new only within one marketplace, so renaming the marketplace breaks foreman@foreman. Shape: the repo's marketplace becomes 'sampo' (sampo, sampo-ui, sampo-design); a second, thin 'foreman' marketplace in its own folder lists shim plugins foreman and foreman-ui that declare dependencies ['sampo@sampo'] (allowCrossMarketplaceDependenciesOn: ['sampo']) and whose commands and agents forward to /sampo:* by instruction (no alias field exists); hooks live only in sampo, so nothing runs twice. Switching a user's enabledPlugins and extraKnownMarketplaces is a settings change: built and queued with fm ask core. Directory-source plugins load in place, so the ~/.claude/foreman symlink keeps a live install working until then (to be tested).
- 2026-11-03T01:03:49Z paused: focus moved to T-2746
- 2026-11-03T01:38:27Z focused
- 2026-11-03T01:39:52Z paused: focus moved to T-2746
- 2026-11-03T02:17:05Z plan (step 2, after T-2748 merges, on the sampo/ layout): plugin/bin/sampo (fm's launcher; prog name from argv[0]); fm prints one deprecation line a day to stderr; argparse aliases for the renamed verbs (rune=genesis, louhi=exam, ward=guard, smith=code), silent word maps for moons=genesis moonshot and underworld=genesis underworld (a new genesis action that prints not-yet.md's items and blockers, so no verb is added); a c.env(NAME) helper reads SAMPO_NAME then FOREMAN_NAME at every FOREMAN_* read; the Foreman-Task trailer readers (fmgraph.py:68, fmcli.py:1136, 5294, 5351) accept Sampo-Task too, and new commits write Sampo-Task; ~/.local/bin/sampo link via install-user (installs step). Tests: test_rename_cli, test_rename_env.
- 2026-11-03T02:17:22Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T02:17:22Z focused
- 2026-11-03T02:17:39Z focused
- 2026-11-03T02:37:12Z paused: focus moved to T-2751
- 2026-11-03T02:42:21Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T02:42:21Z focused
- 2026-11-03T02:46:38Z steer (found end to end): plugin/bin/sampo sets SAMPO_PROG but nothing reads it, so sampo's usage line and errors still say 'fm' (sampo nosuchverb → 'usage: fm …', 'fm help lists them'); step 2 makes the parser's prog and its messages follow what was typed
- 2026-11-03T03:07:46Z paused: focus moved to T-2756
- 2026-11-03T03:09:13Z step 2 red tests written: test_rename_cli (6 tests, 7 fail: new verbs, moons/underworld, no '(ran' line, once-a-day tty notice) and test_rename_env (3 fail: SAMPO_HOME, SAMPO wins over FOREMAN twin, Sampo-Task read by fm task revert). Plan: one env mirror at fmcore import (SAMPO_X overrides FOREMAN_X, FOREMAN_X fills SAMPO_X) covers all 118 readers; trailer readers → (?:Sampo|Foreman)-Task, writers (fmcli finish, fmrelease, fmstack) → Sampo-Task, git --grep with -E; test_secrets:84 asserts Sampo-Task
- 2026-11-03T03:25:12Z from T-2753 (for steps 5 and 8): README and MASTER headers still show the hard hat; site/assets/diagrams/architecture.svg says Foreman; gallery pages and plugin/skills playbooks name Foreman; fmcodetui's key map says 'every Foreman project'; the localStorage key fm-theme and genesis.json's 'foreman' key keep old names (rename with a read of the old); layout() pages lack a theme-color meta
- 2026-11-03T03:32:00Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T03:32:00Z focused
- 2026-11-03T03:32:51Z paused: focus moved to T-2757
- 2026-11-03T03:33:43Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T03:33:43Z focused
- 2026-11-03T03:33:53Z paused: focus moved to T-2757
- 2026-11-03T03:36:06Z focused
- 2026-11-03T03:40:01Z paused: focus moved to T-2760
- 2026-11-03T03:40:16Z from T-2760: test_docs maps sampo smith/rune/louhi/ward to the old verbs (SAMPO_OLD/SAMPO_NEW) until step 2; drop that map once the CLI has them. The per-repo mirror .foreman/ (fm sync) still needs its rename to .sampo/ with .foreman read (step 5 paths)
- 2026-11-03T03:41:18Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T03:41:18Z focused
- 2026-11-03T03:43:03Z focused
- 2026-11-03T03:46:20Z scope: plugin/tests/test_site.py — the lacks-page test required 'fm which' in README; README now says 'sampo which' (T-2760), so it accepts either name
- 2026-11-03T04:04:01Z paused: focus moved to T-2759
- 2026-11-03T04:44:31Z steer: the user isn't a fan of the website and logo: wants it nicer, way better animations, more detail, a better logo, the site matching the logo's vibe completely, completely redesigned/reimagined (T-2770 redoes steps 6 and 7)
- 2026-11-03T05:35:46Z step 7 text: The site rebuilt in the design system, every page, with shots at desktop, tablet and phone and the quality bar → The site rebuilt in the design system, every page, with shots at desktop, tablet and phone and the quality bar: carried by T-2788 (the Kirjokansi + forge rebuild, after the user's pick in T-2772)
- 2026-11-03T05:35:46Z steer: the user rejected the T-2759 site and Runestone logo (2026-11-03); T-2772 showed four directions, the user picked Kirjokansi and said they like the forge too; T-2788 rebuilds the logo system and every page in the fused direction, so step 7 closes when T-2788 does
- 2026-11-03T05:36:22Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T05:36:22Z focused
- 2026-11-03T05:37:54Z paused: focus moved to T-2763
- 2026-11-03T15:21:12Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T15:21:12Z focused
- 2026-11-03T16:00:23Z focused
- 2026-11-03T16:07:31Z paused: focus moved to T-2812
- 2026-11-03T16:09:07Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T16:09:07Z focused
- 2026-11-03T16:24:56Z paused: focus moved to T-2767
- 2026-11-03T16:40:47Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T16:40:47Z focused
- 2026-11-03T16:40:48Z step 7 waits on T-2788's fiery-forge build (designer running); step 5 lanes merged (T-2779, T-2807, T-2808, T-2809, T-2810); ship and closes running in the background (T-2813)
- 2026-11-03T16:41:12Z paused: focus moved to T-2767
- 2026-11-03T17:07:12Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:07:12Z focused
- 2026-11-03T17:13:01Z paused: focus moved to T-2768
- 2026-11-03T18:47:24Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T18:47:24Z focused
- 2026-11-03T19:14:37Z step 7 not verifiable yet: the site rebuild waits on the design pick between 11 (photoreal) and 12 (illustrated), both still being built and shown live on the picker artifact; T-2788 carries it
- 2026-11-03T19:26:42Z paused: focus moved to T-2822
- 2026-11-03T19:56:44Z focused
- 2026-11-03T20:12:18Z paused: focus moved to T-2834
- 2026-11-03T20:13:30Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T20:13:30Z focused
- 2026-11-03T20:13:58Z paused: focus moved to T-2835
- 2026-11-03T20:23:01Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T20:23:01Z focused
- 2026-11-03T20:24:36Z includes T-2772: Sampo reimagined: a new logo and a completely redesigned site (user steer 2026-11-03): four rendered directions (logo, animated hero, sections) to choose from, then the chosen one carried through every page, the logo's variants, the README header and the design tokens, with far richer animation and detail, the site matching the logo's world completely
- 2026-11-03T20:26:02Z paused: focus moved to T-2818
- 2026-11-03T20:28:25Z focused
- 2026-11-03T20:28:27Z paused: focus moved to T-2818
- 2026-11-03T20:59:43Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T20:59:43Z focused
- 2026-11-03T20:59:58Z paused: focus moved to T-2839
- 2026-11-03T21:01:40Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T21:01:40Z focused
- 2026-11-03T21:02:06Z paused: focus moved to T-2838
- 2026-11-03T21:04:41Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T21:04:41Z focused
- 2026-11-03T21:07:47Z includes T-2795: Breakage ahead: bced376 changed plugin/skills/genesis/SKILL.md without CHANGELOG.md,…
- 2026-11-03T21:07:54Z includes T-2803: Where are the screenshots at? or can I run the website locally or something to see it
- 2026-11-03T21:07:54Z includes T-2804: Super imrove the fuse completely, combined/animated logos, beautiful, better…
- 2026-11-03T21:07:54Z includes T-2832: Adopt the fully animated variant as the project's single canonical theme: choose it as…
- 2026-11-03T21:08:45Z includes T-2805: Work autonomously by default: when the next step is clear, take it instead of pausing to…
- 2026-11-03T21:08:45Z includes T-2831: Publish the current state of the work's artifacts (reports, outputs, proofs, test…
- 2026-11-03T21:08:46Z includes T-2817: Treat visual and interactive work (UI, web pages, games, graphics, demos) as held to a…
- 2026-11-03T21:08:46Z includes T-2824: Treat the user's visual preference as standing for all Sampo-facing design work: a…
- 2026-11-03T21:11:06Z includes T-2802: Consolidate near-duplicate lessons
- 2026-11-03T21:18:52Z paused: focus moved to T-2798
- 2026-11-03T21:39:13Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T21:39:13Z focused
- 2026-11-03T21:52:22Z paused: focus moved to T-2778
- 2026-11-03T22:01:38Z focused
- 2026-11-03T22:05:56Z paused: focus moved to T-2843
- 2026-11-03T22:17:15Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T22:17:15Z focused
- 2026-11-03T22:30:15Z paused: focus moved to T-2855
- 2026-11-04T00:28:44Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T00:28:44Z focused
- 2026-11-04T00:29:25Z step 8 (docs): 47 staged changelog lines landed under Unreleased (1a723cfb); the top entry and the Runestone-line rewrite wait for the theme port (T-2851/T-2852); scratchpad changelog-lines.md emptied for new lines
- 2026-11-04T00:31:17Z paused: focus moved to T-2857
- 2026-11-04T00:32:48Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T00:32:48Z focused
- 2026-11-04T00:35:04Z paused: focus moved to T-2863
- 2026-11-04T00:52:23Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T00:52:23Z focused
- 2026-11-04T00:53:09Z paused: focus moved to T-2864
- 2026-11-04T01:15:30Z focused
- 2026-11-04T01:31:20Z paused: focus moved to T-2847
- 2026-11-04T01:49:56Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T01:49:56Z focused
- 2026-11-04T02:02:05Z paused: focus moved to T-2861
- 2026-11-04T02:14:55Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T02:14:55Z focused
- 2026-11-04T02:15:22Z paused: focus moved to T-2871
- 2026-11-04T02:18:21Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T02:18:21Z focused
- 2026-11-04T02:57:42Z paused: focus moved to T-2872
- 2026-11-04T03:03:07Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T03:03:07Z focused
- 2026-11-04T03:04:03Z paused: focus moved to T-2873
- 2026-11-04T03:10:34Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T03:10:34Z focused
- 2026-11-04T03:12:28Z paused: focus moved to T-2874
- 2026-11-04T03:19:12Z focused
- 2026-11-04T03:34:45Z marketplace probe (CC 2.1.317, sandboxed CLAUDE_CONFIG_DIR): json name foreman->sampo keeps an existing registration keyed foreman; a top-level renames map {foreman: sampo} rewrites enabledPlugins foreman@foreman -> sampo@foreman on the next CLI run and startup installs it; new adds register as sampo, so sampo@sampo. Old /foreman: slash commands become /sampo:. Code must accept sampo@* and foreman@* ids
- 2026-11-04T03:45:46Z paused: focus moved to T-2883
- 2026-11-04T03:53:57Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T03:53:57Z focused
- 2026-11-04T04:02:59Z paused: focus moved to T-2887
- 2026-11-04T04:08:13Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-04T04:08:13Z focused
- 2026-11-04T04:21:47Z focused
- 2026-11-04T04:36:01Z paused: focus moved to T-2894
- 2026-11-04T04:54:42Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T04:54:42Z focused
- 2026-11-04T05:22:31Z paused: focus moved to T-2900
- 2026-11-04T05:26:22Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T05:26:22Z focused
- 2026-11-04T05:43:42Z paused: focus moved to T-2901
- 2026-11-04T05:48:04Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T05:48:04Z focused
- 2026-11-04T05:51:07Z paused: focus moved to T-2901
- 2026-11-04T05:58:45Z focused
- 2026-11-04T06:14:02Z paused: focus moved to T-2851
- 2026-11-04T06:37:22Z focused
- 2026-11-04T06:37:23Z step 7 reopened: it was checked by an ambient run of the drive tests (test_hooks test_board_hooks test_friction) recorded as its evidence while T-2742 was focused; the site still waits on critique 6 and round 7's re-sync
- 2026-11-04T06:43:32Z paused: focus moved to T-2909
- 2026-11-04T06:47:25Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T06:47:25Z focused
- 2026-11-04T07:02:41Z paused: focus moved to T-2919
- 2026-11-04T07:40:14Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T07:40:14Z focused
- 2026-11-04T07:42:25Z paused: focus moved to T-2922
- 2026-11-04T09:19:05Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T09:19:05Z focused
- 2026-11-04T09:28:16Z paused: focus moved to T-2926
- 2026-11-04T11:28:23Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T11:28:23Z focused
- 2026-11-04T11:35:12Z guard authorization added: publish
- 2026-11-04T11:47:09Z paused: focus moved to T-2955
- 2026-11-04T11:49:42Z guard authorization added: publish
- 2026-11-04T11:51:27Z focused
- 2026-11-04T11:57:24Z paused: focus moved to T-2958
- 2026-11-04T12:01:03Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T12:01:03Z focused
- 2026-11-04T12:01:23Z paused: focus moved to T-2959
- 2026-11-04T12:10:07Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T12:10:07Z focused
- 2026-11-04T12:10:09Z guard authorization added: publish
- 2026-11-04T12:19:38Z paused: focus moved to T-2960
- 2026-11-04T12:23:08Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T12:23:08Z focused
- 2026-11-04T12:23:09Z guard authorization added: publish
- 2026-11-04T12:29:26Z paused: focus moved to T-2957
- 2026-11-04T12:39:30Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T12:39:30Z focused
- 2026-11-04T12:39:30Z guard authorization added: publish
- 2026-11-04T12:39:34Z step 7: the site carries critique 7's converged forge (T-2957); shots at 320/390/768/1440 in both themes in the scratchpad's directions-v2/12-forge-illustrated/_review/site-sync/ (looked at landing-dark-1440, how-dark-1440: no box behind the hero's italic line, the lamp-lit station matching its row); critique 7 final.md: nothing above Low on the landing or the tower
- 2026-11-04T12:41:56Z paused: focus moved to T-2947
- 2026-11-04T12:44:32Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T12:44:32Z focused
- 2026-11-04T12:47:50Z paused: focus moved to T-2948
- 2026-11-04T13:09:53Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T13:09:53Z focused
- 2026-11-04T13:09:53Z guard authorization added: publish
- 2026-11-04T13:22:31Z publish grant used by fm ship
- 2026-11-04T13:22:51Z focused
- 2026-11-04T13:26:20Z paused: focus moved to T-2964
- 2026-11-04T13:33:15Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T13:33:15Z focused
- 2026-11-04T13:35:17Z paused: focus moved to T-2788
- 2026-11-04T13:35:52Z focused
- 2026-11-04T13:41:22Z paused: focus moved to T-2967
- 2026-11-04T13:43:45Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T13:43:45Z focused
- 2026-11-04T13:43:46Z scope: the rename spans the whole repo by design (SAMPO.md: product, CLI, plugin, internals, env, paths, state, installs, docs, identity, site); each part landed through its own sub-task with its own audits
- 2026-11-04T13:55:40Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Full product rebrand, staged (likeliest):** SAMPO.md is the spec. Introduce `sampo` as the primary CLI (`plugin/bin/fm` → `plugin/bin/sampo`), rename the concepts (Smith, Rune, Moons, Louhi, Underworld, Ward) across `plugin/skills/` (1388 files), `plugin/lib/fm*.py`, docs, and the plugin manifest…
- **User-facing rename only:** the CLI, docs, plugin name and site change, while internal module names (`fmcore`, `fmhooks`) and the on-disk layout stay. This contradicts "internals and env renamed", so it is less likely.
- **Alias-first compatibility layer:** land only the `sampo` entry point, the alias table and the migration now, and treat the visual work (design system, logo, site) as a separate follow-up. The request bundles both, so this is a possible staging of the first reading.
- **Ambiguous mapping:** SAMPO.md may not say which old concept maps to which new name (e.g. which of Smith, Rune or Moons replaces which existing subsystem). A build that guesses would be wrong, and one that reads SAMPO.md first would not be.
Approaches:
- **Central alias registry first:** a single table (old name → new name) in `plugin/lib/` consumed by the CLI dispatcher in `plugin/bin/fm`, the skill and command resolver, and the env-var reader. Rename in layers after that, with `fm doctor` and `plugin/tests/run.py` green at each layer.
- **Migration as a standalone module:** a `sampo migrate` command that copies `~/.claude/foreman` to the new directory, writes a manifest and a timestamped backup, and provides `sampo migrate --undo`. Leave a compatibility symlink or fallback read path so hooks that run mid-migration (`plugin/lib/fmh…
- **Scripted mechanical rename with a denylist:** a codemod over `plugin/skills/`, `plugin/tests/` and `plugin/lib/` that rewrites identifiers and strings. It skips `CHANGELOG.md`, fixtures under `plugin/tests/fixtures/`, and historical records. Review the diff by category (code, docs, skill descript…
- **Site and design system separately:** treat `site/` (64 files), `plugin/templates/web/index.html` and `mods/foreman-ui` as an independent track. Build design tokens once (tailwind config) and have both the site and the web template consume them, so the visual work doesn't block the code rename.
Failure modes:
- **Hook latency or breakage:** `plugin/lib/fmhooks.py` and `fmguard.py` read the state path and env vars on every hook call. Renaming them without a fallback silently disables guards for existing installs, and an alias lookup on the hot path can regress `plugin/tests/bench_hooks.py --runs 20`.
- **Migration data loss:** moving `~/.claude/foreman` while a session is live, or running it twice, can clobber state. Undo that restores from a stale backup loses writes made after the move, and the move is hard to reverse, so it needs a confirmation gate.
- **Blind global replace corrupts text:** "Ward", "Moons", "Rune" and "Smith" are common words, and "foreman" appears in fixtures, CHANGELOG history, skill descriptions that drive triggering, and git URLs. A naive replace breaks `plugin/tests/fixtures/`, trigger phrases in `plugin/skills/` descriptio…
- **Plugin identity change breaks upgrades:** renaming the plugin id in the manifest or marketplace entry makes installed users see a new plugin rather than an update, which orphans their settings and enabled hooks. `fm replay` and the e2e roundtrip may pass locally while real installs break.
## Dissent
- [x] rival reading: **Alias-first compatibility layer:** land only the `sampo` entry point, the alias table and the migration now, and treat the visual work (design system, logo, site) as a separate follow-up. The request bundles both, so this is a possible staging of the first reading. — answered: adopted in order, not in scope: aliases and migration land first (steps 2 and 3); SAMPO.md's Done-when includes the logo, site and design review, so they stay in this task as later steps run in paral…
- [x] rival reading: **Ambiguous mapping:** SAMPO.md may not say which old concept maps to which new name (e.g. which of Smith, Rune or Moons replaces which existing subsystem). A build that guesses would be wrong, and one that reads SAMPO.md first would not be. — answered: ruled out: SAMPO.md's table maps each name exactly (Foreman→Sampo, the task loop→Smith, Genesis→Rune, moonshots→Moons, exam and Inspector→Louhi, not-yet→Underworld, guard→Ward)
- [x] rival approach: **Central alias registry first:** a single table (old name → new name) in `plugin/lib/` consumed by the CLI dispatcher in `plugin/bin/fm`, the skill and command resolver, and the env-var reader. Rename in layers after that, with `fm doctor` and `plugin/tests/run.py` green at each layer. — answered: adopted: one alias table (old → new: verbs, plugin ids, commands, agents, env, trailers) read by the CLI dispatcher, the hooks and the scan test, so an alias exists in one place
- [x] rival approach: **Scripted mechanical rename with a denylist:** a codemod over `plugin/skills/`, `plugin/tests/` and `plugin/lib/` that rewrites identifiers and strings. It skips `CHANGELOG.md`, fixtures under `plugin/tests/fixtures/`, and historical records. Review the diff by category (code, docs, skill descript… — answered: adopted: fm sub with a denylist (CHANGELOG past entries, research/genesis history, gen-0, ledgers, commit trailers' old form); the scan test holds the same allowlist
- [x] rival approach: **Site and design system separately:** treat `site/` (64 files), `plugin/templates/web/index.html` and `mods/foreman-ui` as an independent track. Build design tokens once (tailwind config) and have both the site and the web template consume them, so the visual work doesn't block the code rename. — answered: adopted: design tokens once, read by the site, the web page, the ui mod, the TUI theme and the statusline; built in parallel lanes after the aliases land
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- research mission-20261029-233102: Request: Genesis Mission 2 (#13 Genesis as a feature): fm genesis runs the whole tower by itself in any project — writes its own gen-0 …
## Build vs reuse
Reuses: the CLI's own parser (fmcli._Parser, FOLDED and TOMBSTONES already map old words to new), fm sub for the mechanical renames, fmrollback's tar snapshot and manifest for the migration backup, fm install-user's manifest for undo, fm drill --restore's temp home for the migration test, fm looks and the directions skill for the logo directions, fm shot, fm flow, fm critique and fm design lint for the site. New: one alias table, the sampo entry point, sampo migrate (--undo), and module shims (sys.modules aliasing so old fm* imports return the same module object).
## Outward steps
Prepared, never applied unasked (SAMPO.md "Protected core and outward actions"):
1. GitHub repo: origin is already git@github.com:ChaseSunstrom/sampo.git; install.sh, README and the site clone that URL. Nothing left to apply; GitHub's redirect keeps the old URL working.
2. Desktop repo and app: rename ChaseSunstrom/foreman-desktop to ChaseSunstrom/sampo-desktop (GitHub redirects the old name), then change install.sh's FOREMAN_DESKTOP_REPO default, the "Foreman Desktop" menu entry and the binary name to Sampo Desktop (T-2818 keeps them until the repo moves). Needs the user's `gh auth login` on this box.
3. Pages URL: point the Pages site at the sampo repo and add a redirect page at the old Pages path. Needs `gh auth login`.
4. Marketplace and plugin ids: foreman@foreman to sampo@sampo with the old id kept as an alias; planned as T-2879 (L), approval before the build.
5. Protected core built in worktrees and merged under the standing core yes: the guard's refusal text (T-2946), hooks.json's description (T-2946); rules/foreman.md keeps its path as an alias.
## Lessons
- A rename is a security change wherever a path is compared: audit every literal path check before the migration that changes the path
## Files touched
- plugin/tests/test_rename_scan.py
- CHANGELOG.md
- plugin/bin/sampo
- design/sampo/logo/build.py
- plugin/tests/test_rename_cli.py
- plugin/tests/test_site.py
- plugin/skills/playbooks/ratchet.json
- plugin/lib/sampo/hooks.py
- plugin/tests/test_hooks.py
- models.json
- research/models/bench.jsonl
- plugin/tests/test_ship.py
- plugin/lib/sampo/release.py
