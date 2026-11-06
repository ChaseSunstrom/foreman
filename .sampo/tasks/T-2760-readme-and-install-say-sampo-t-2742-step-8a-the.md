---
id: T-2760
type: FEATURE
tier: M
status: done
priority: normal
scope: [README.md, INSTALL.md, plugin/tests/test_rename_scan.py, plugin/tests/test_docs.py, plugin/tests/test_readme*.py]
depends_on: []
source: user
created: 2026-11-03T03:31:09Z
updated: 2026-11-03T03:42:58Z
builder_model: sonnet
base: 80045ce37958766acc2236443f3e2f43eb71bbe4
base_tree: 029e559af46be3aa36ce01b1f43c2fd6b94592e8
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-03T03:31:54Z
plan0_scope: [README.md, INSTALL.md, plugin/tests/test_rename_scan.py, plugin/tests/test_docs.py, plugin/tests/test_readme*.py]
lane_stop: merged 2026-11-03T03:39:33Z
paused_tree: 2517e1ebe605b56f5c432841775e0c20e23eb07c
verified: strong
unproven: [docs]
---
# README and INSTALL say Sampo (T-2742 step 8a): the Runestone README header (dark and light), every Foreman name and command in the Sampo names (sampo, Smith, Rune, Moons, Louhi, Underworld, Ward), the Kalevala myth paragraph once, an upgrade note naming the kept aliases (fm, foreman@foreman, /foreman:, FOREMAN_*, Foreman-Task, ~/.claude/foreman) and sampo migrate
## Raw request
> README and INSTALL say Sampo (T-2742 step 8a): the Runestone README header (dark and light), every Foreman name and command in the Sampo names (sampo, Smith, Rune, Moons, Louhi, Underworld, Ward), the Kalevala myth paragraph once, an upgrade note naming the kept aliases (fm, foreman@foreman, /foreman:, FOREMAN_*, Foreman-Task, ~/.claude/foreman) and sampo migrate
## Interpretation
Reading 1 (chosen): SAMPO.md's Docs line for the two front-door docs: README and INSTALL rewritten in the Sampo names with the new header and the myth paragraph once (SAMPO.md: once on the site and in the README); MASTER.md waits for T-2748 (it names modules that are moving) and the CHANGELOG top entry comes at the end. Reading 2: a find-and-replace of Foreman to Sampo; rejected: commands change shape (fm genesis → sampo rune) and the alias forms must stay.
## Assumptions (confidence)
## Acceptance criteria
- [x] README.md and INSTALL.md name Foreman only in the kept alias forms and one 'formerly Foreman' line, and the rename ratchet's BASELINE drops by what they removed — verify with `python3 plugin/tests/run.py test_rename_scan`
- [x] the myth paragraph appears once in README.md, the header uses design/sampo/logo/readme-header-dark.svg and -light.svg through a picture element, and every command the docs show parses (sampo verbs included) — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
1. Rewrite by hand, section by section, with the CLI's own help as the source for verbs; the alias forms kept verbatim in one upgrade note. Likely outcome: readable docs, exact commands. Fails if: a renamed verb isn't in the CLI yet (step 2 lands sampo rune etc. before this merges; the doc test parses each command).
2. fm sub (regex codemod) over README for the names, then a hand pass. Likely outcome: faster. Fails if: the codemod rewrites kept forms (foreman@foreman) or history lines.
3. Use what exists: test_docs already parses the fm commands docs show, test_rename_scan counts leftovers, design/sampo/logo has both README headers, SAMPO.md has the myth's content. Likely outcome: no new tooling. Fails if: test_docs only knows the fm program name (extend it to sampo).
4. Do less: header and myth only. Fails if: Done-when says no user-visible Foreman remains.
Choice 1 with 3 (80%).
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, site/pages.py, plugin/lib/fmcode.py; past FIXes T-1209, T-1239, T-1371, T-1569, T-1714.
## Execution prompt
## Steps
1. [x] red: extend test_docs (or a test_readme_sampo) for the header, the one myth paragraph, the upgrade note and that every shown sampo command parses
2. [x] rewrite README.md's names, header and command examples; add the myth paragraph and the upgrade note; INSTALL.md the same
3. [x] lower BASELINE; check the README renders on GitHub's light and dark (picture with prefers-color-scheme sources)
## Resume here
<!-- auto -->
- 2026-11-03T03:34:59Z step 2/3: rewrite README.md's names, header and command examples; add the myth paragraph and the upgrade note; INSTALL.md the same
- git: worktree-agent-ab6a8e7e714156f83; 5 uncommitted: INSTALL.md, README.md, plugin/tests/test_board_surfaces.py, plugin/tests/test_demo.py, plugin/tests/test_docs.py
- touched since last checkpoint: plugin/tests/test_docs.py, plugin/tests/test_demo.py, plugin/tests/test_board_surfaces.py, .fm-scratch/codemod.py, .fm-scratch/prose.py, README.md, INSTALL.md
## Docs impact
README.md; INSTALL.md; CHANGELOG.md
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_docs 2>&1 | grep -B2 -A12 -E "^FAIL" | head -90` → ✗ exit 1 · ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ / AssertionError: 'src="site/assets/foreman.svg"' not found in '<p align="center"><picture>\n  <source me [ran] [tree a0fa88b2d7bb] [world 2f1906870a] (2026-11-03T03:35:50Z)
- (step 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 107 tests in 10.6s (25 classes, 16 at a time; slowest: Fences 10s, DocsProof 5s, TaskLifecycle 2s) / OK [ran] [tree fda8da4f04a6] [world 2f1906870a] (2026-11-03T03:37:51Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_board_surfaces test_demo` → exit 0 · Ran 118 tests in 11.6s (27 classes, 16 at a time; slowest: Fences 11s, Demo 8s, DocsProof 5s) / OK [ran] [tree fda8da4f04a6] [world 2f1906870a] (2026-11-03T03:38:03Z)
- (step 3) `python3 .fm-scratch/left.py` → exit 0 · README.md | [The site](https://chasesunstrom.github.io/foreman/) | A page per feature, with recorded runs. | / README.md **Upgrading.** Sampo was formerly Foreman, and nothing you have breaks: `fm` st [ran] [tree fda8da4f04a6] [world 2f1906870a] (2026-11-03T03:38:04Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_board_surfaces test_demo test_docs test_mcp test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.82s] [ran] [tree fda8da4f04a6] [world 2f1906870a] (2026-11-03T03:38:44Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 54b9ca9ca4a6] [world 2f1906870a] (2026-11-03T03:40:04Z)
- (ac 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 107 tests in 10.4s (25 classes, 16 at a time; slowest: Fences 10s, DocsProof 4s, TaskLifecycle 2s) / OK [ran] [tree 54b9ca9ca4a6] [world 2f1906870a] (2026-11-03T03:40:15Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 2 tests in 0.6s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 2517e1ebe605] [world 2f1906870a] (2026-11-03T03:40:31Z)
- (ac 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 107 tests in 12.2s (25 classes, 16 at a time; slowest: Fences 12s, DocsProof 5s, TaskLifecycle 3s) / OK [ran] [tree 2517e1ebe605] [world 2f1906870a] (2026-11-03T03:40:31Z)
- (audit intent) `reviewed fb4f7a6a: header is a picture with dark and light sources from design/sampo/logo, the myth paragraph appears once (in a details block, to keep the README under its 2000-word limit), the upgrade note lists every kept form; fixed one wrong path (.sampo/fixes.md → .foreman/fixes.md, what fm sync writes today); KEPT gains the repo address so correct install URLs aren't counted` → SAMPO.md Docs (README, INSTALL) and the myth once in the README; MASTER waits for T-2748, the CHANGELOG top entry for the end [tree 2517e1ebe605] (2026-11-03T03:40:31Z)
- (audit edge) `reviewed fb4f7a6a: header is a picture with dark and light sources from design/sampo/logo, the myth paragraph appears once (in a details block, to keep the README under its 2000-word limit), the upgrade note lists every kept form; fixed one wrong path (.sampo/fixes.md → .foreman/fixes.md, what fm sync writes today); KEPT gains the repo address so correct install URLs aren't counted` → the renamed verbs the docs show parse through test_docs' temporary map until step 2 adds them; install URLs stay on ChaseSunstrom/foreman until the user renames the repo [tree 2517e1ebe605] (2026-11-03T03:40:31Z)
- (audit maintainer) `reviewed fb4f7a6a: header is a picture with dark and light sources from design/sampo/logo, the myth paragraph appears once (in a details block, to keep the README under its 2000-word limit), the upgrade note lists every kept form; fixed one wrong path (.sampo/fixes.md → .foreman/fixes.md, what fm sync writes today); KEPT gains the repo address so correct install URLs aren't counted` → test_docs' SAMPO_OLD/SAMPO_NEW map is marked to drop at step 2 (logged on T-2742) [tree 2517e1ebe605] (2026-11-03T03:40:31Z)
- (audit intent) `reviewed fb4f7a6a: header is a picture with dark and light sources from design/sampo/logo, the myth paragraph appears once (in a details block, to keep the README under its 2000-word limit), the upgrade note lists every kept form; fixed one wrong path (.sampo/fixes.md → .foreman/fixes.md, what fm sync writes today); KEPT gains the repo address so correct install URLs aren't counted` → SAMPO.md Docs (README, INSTALL) and the myth once in the README; MASTER waits for T-2748, the CHANGELOG top entry for the end [tree 2517e1ebe605] (2026-11-03T03:41:44Z)
- (audit edge) `reviewed fb4f7a6a: header is a picture with dark and light sources from design/sampo/logo, the myth paragraph appears once (in a details block, to keep the README under its 2000-word limit), the upgrade note lists every kept form; fixed one wrong path (.sampo/fixes.md → .foreman/fixes.md, what fm sync writes today); KEPT gains the repo address so correct install URLs aren't counted` → the renamed verbs the docs show parse through test_docs' temporary map until step 2 adds them; install URLs stay on ChaseSunstrom/foreman until the user renames the repo [tree 2517e1ebe605] (2026-11-03T03:41:44Z)
- (audit maintainer) `reviewed fb4f7a6a: header is a picture with dark and light sources from design/sampo/logo, the myth paragraph appears once (in a details block, to keep the README under its 2000-word limit), the upgrade note lists every kept form; fixed one wrong path (.sampo/fixes.md → .foreman/fixes.md, what fm sync writes today); KEPT gains the repo address so correct install URLs aren't counted` → test_docs' SAMPO_OLD/SAMPO_NEW map is marked to drop at step 2 (logged on T-2742) [tree 2517e1ebe605] (2026-11-03T03:41:44Z)
## Log
- 2026-11-03T03:31:09Z created
- 2026-11-03T03:31:27Z set approved=True
- 2026-11-03T03:31:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2760.builder.md
- 2026-11-03T03:31:48Z focused
- 2026-11-03T03:31:54Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-03T03:39:33Z merged worktree-agent-ab6a8e7e714156f83 (5 file(s))
- 2026-11-03T03:39:33Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab6a8e7e714156f83
- 2026-11-03T03:40:01Z focused
- 2026-11-03T03:40:15Z scope: test_demo.py and test_board_surfaces.py asserted fm commands in the README (builder); CHANGELOG line; KEPT gains the repo address (ChaseSunstrom/foreman and its Pages URL move only with the outward repo rename)
- 2026-11-03T03:41:18Z paused: focus moved to T-2742
- 2026-11-03T03:41:44Z scope: plugin/tests/test_demo.py and plugin/tests/test_board_surfaces.py asserted fm commands in the README (builder's lane); .fm-scratch/codemod.py and .fm-scratch/prose.py are the lane's uncommitted scratch; CHANGELOG.md takes the task's line
- 2026-11-03T03:42:50Z done
- 2026-11-03T03:42:58Z committed c7401633 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2748 [CLEAN M, active, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py…
- T-2759 [FEATURE M, active, 4 steps] The landing page in the forge world (T-2742 step 7b): a hero where the Sampo mill turns and runes write themselves into the headline …
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Lessons
- A docs lane renaming paths must check each path against the code that writes it: the per-repo mirror is still .foreman/
## Files touched
- plugin/tests/test_docs.py
- plugin/tests/test_demo.py
- plugin/tests/test_board_surfaces.py
- .fm-scratch/codemod.py
- INSTALL.md
- README.md
- .fm-scratch/prose.py
- CHANGELOG.md
- plugin/tests/test_rename_scan.py
