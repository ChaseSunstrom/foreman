---
id: T-2879
type: FEATURE
tier: L
status: planned
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:35:16Z
updated: 2026-11-06T03:54:00Z
rival_at: 2026-11-05T01:58:54Z
rival_split: true
base: b3ac10ff49295f54456dfa8a6c32f2b8fa9b9888
base_tree: 106df4e763e5958f49cb49fa89421e20088b6303
predict_minutes: 13
predict_attempts: 1
plan0_at: 2026-11-05T01:59:10Z
plan0_scope: []
paused_tree: ab0d245b6375d38111d3d00152230ace0565424a
---
# Plugin ids to Sampo: marketplace sampo, plugins sampo, sampo-ui, sampo-design, with a renames map so existing foreman@foreman installs move themselves; every /foreman: and foreman:fm- spelling Sampo writes becomes sampo:, every reader takes both
## Raw request
> Plugin ids to Sampo: marketplace sampo, plugins sampo, sampo-ui, sampo-design, with a renames map so existing foreman@foreman installs move themselves; every /foreman: and foreman:fm- spelling Sampo writes becomes sampo:, every reader takes both
## Interpretation
Reading 1 (taken, per the 2026-11-03 decision under SAMPO.md's 'nothing a user already has may break'): inside the existing 'foreman' marketplace the plugins become sampo, sampo-ui and sampo-design; thin foreman, foreman-ui and foreman-design shims stay, list the Sampo plugin as a dependency and forward /foreman: commands, so existing foreman@foreman installs keep working and new installs use sampo@foreman; every /foreman: and foreman:fm- spelling Sampo writes becomes sampo: / sampo:fm-, and every reader (doctor, settings, hooks, the mod) takes both. Renaming the marketplace itself to 'sampo' (sampo@sampo, SAMPO.md's literal id) is prepared but applied only after an empirical test in a scratch Claude config shows existing installs move without breaking, because marketplace renames are undocumented. Reading 2 (ruled out for now): rename marketplace and plugins at once and rely on a renames map: renames map plugin names only within one marketplace (Claude Code docs), so foreman@foreman installs would break.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the marketplace and plugin manifests carry the new names and the renames map, and claude validates them — verify with `~/.local/bin/claude plugin validate .`
- [ ] readers (doctor, settings, hooks, the mod) accept sampo@* and foreman@* ids and both skill namespaces, and the suite passes — verify with `sampo check`
- [ ] No producer still writes a foreman: namespace outside an explicit allowlist of paths in the test (alias readers, CHANGELOG.md, old-name tests); a new producer anywhere else fails it — verify with `python3 plugin/tests/run.py test_rename_scan`
- [ ] An existing install survives and moves itself: in a scratch Claude config (CLAUDE_CONFIG_DIR in the scratchpad) with foreman@foreman installed from a local copy of today's manifests, updating to the new ones keeps every /foreman: command, foreman: skill and hook working once (no double load) and makes sampo:* available; a script runs this and prints each check — verify with `bash scripts/probe-plugin-rename.sh`
- [ ] Marketplace sampo: not reachable without every user re-adding the marketplace (a marketplace's configured name comes from when it was added; probe in research T-2879-probe); the marketplace keeps the name 'foreman' as an id part, and the not-yet is filed with that blocker — verify with `sampo research show T-2879-probe`
## Non-goals
Renaming the GitHub repo or the Desktop app (separate outward steps with their own grants); removing any foreman alias.
## Approach (options → choice → why)
1) use what exists: the plugins' own renames map within the foreman marketplace plus shims for the old names, readers that take both ids (doctor, settings, hooks, the mod), producers respelled in one lane: likely outcome: new names everywhere Sampo writes, nothing an install has breaks. 2) rename the marketplace now: fails if: existing installs can't find their plugin (undocumented). 3) aliases only, no respelling: fails if: Sampo keeps writing the old names forever. 4) do less: rename the plugin.json name fields only: fails if: 42 producer lines and 6 id readers still say foreman. Choice 1 (80%), with the marketplace step gated on the scratch-config probe.
## Risks and rollback
An install loading both a shim and the Sampo plugin double-registers commands or hooks: the probe checks it and the shims ship no command, skill or hook files of their own; settings written under sampo@foreman by a migration: readers keep honoring sampo@* and foreman@* for good, so a manifest revert leaves both working; the marketplace rename waits for the probe.
Blast radius (sampo graph blast): co-changes CHANGELOG.md, INSTALL.md, README.md, plugin/tests/test_setup.py, plugin/lib/fmcode.py.
## Execution prompt
## Steps
1. [x] probe first: in a scratch CLAUDE_CONFIG_DIR, install foreman@foreman from a local marketplace copy; then try (a) a renames map inside the marketplace, (b) shims with dependencies, (c) a marketplace rename; record what loads, what doubles and what breaks (scripts/probe-plugin-rename.sh). Undo: cp -a ~/.claude/foreman/state/projects/foreman-4a056f/door-snapshots/T-2879-step1/. ~/.claude/foreman/
2. [ ] choose the mechanism the probe proved; respell producers in a lane (readers take both, an explicit allowlist in test_rename_scan)  <- CURRENT
3. [ ] manifests, renames map, install.sh, INSTALL and the upgrade note; probe the move in a sandboxed config dir
## Resume here
## Docs impact
## Verification evidence
- (step 1) `INSTALL_AFTER=1 bash scripts/probe-plugin-rename.sh plugin | grep -q 'Successfully installed plugin: sampo@foreman' && SESSION_AFTER=1 bash scripts/probe-plugin-rename.sh plugin | grep -A6 'after one session start' | grep -q 'sampo@foreman' && bash scripts/probe-plugin-rename.sh shim | grep -q 'failed to load' && echo 'renames map moves installs (a session start installs sampo@foreman); shims fail to load; a marketplace rename does not reach installs'` → ✗ exit 1 · (no output) [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:01:07Z)
- (step 1) `INSTALL_AFTER=1 bash scripts/probe-plugin-rename.sh plugin | grep -q 'Successfully installed plugin: sampo@foreman' && SESSION_AFTER=1 bash scripts/probe-plugin-rename.sh plugin | sed -n '/after one session start/,$p' | grep -q 'sampo@foreman' && bash scripts/probe-plugin-rename.sh shim | grep -q 'failed to load' && echo 'renames map moves installs (a session start installs sampo@foreman); shims fail to load'` → exit 0 · renames map moves installs (a session start installs sampo@foreman); shims fail to load [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:01:28Z)
## Log
- 2026-11-04T03:35:16Z created
- 2026-11-04T03:35:40Z criterion 3 verify: `python3 plugin/tests/run.py test_rename_ratchet` → `python3 plugin/tests/run.py test_rename_scan`
- 2026-11-05T00:43:43Z criterion 3 text: no producer still writes a foreman: namespace outside the alias readers, the changelog and old-name tests → No producer still writes a foreman: namespace outside an explicit allowlist of paths in the test (alias readers, CHANGELOG.md, old-name tests); a new producer anywhere else fails it
- 2026-11-05T00:43:44Z step 1 text: ground: list producers and readers of plugin ids and skill namespaces; the T-2847 split lesson → probe first: in a scratch CLAUDE_CONFIG_DIR, install foreman@foreman from a local marketplace copy; then try (a) a renames map inside the marketplace, (b) shims with dependencies, (c) a marketplace rename; record what loads, what doubles and what breaks (scripts/probe-plugin-rename.sh)
- 2026-11-05T00:43:44Z step 2 text: respell producers in a lane after the site lanes merge; readers take both → choose the mechanism the probe proved; respell producers in a lane (readers take both, an explicit allowlist in test_rename_scan)
- 2026-11-05T01:58:36Z step 1 text: probe first: in a scratch CLAUDE_CONFIG_DIR, install foreman@foreman from a local marketplace copy; then try (a) a renames map inside the marketplace, (b) shims with dependencies, (c) a marketplace rename; record what loads, what doubles and what breaks (scripts/probe-plugin-rename.sh) → probe first: in a scratch CLAUDE_CONFIG_DIR, install foreman@foreman from a local marketplace copy; then try (a) a renames map inside the marketplace, (b) shims with dependencies, (c) a marketplace rename; record what loads, what doubles and what breaks (scripts/probe-plugin-rename.sh). Undo: cp -a ~/.claude/foreman/state/projects/foreman-4a056f/door-snapshots/T-2879-step1/. ~/.claude/foreman/
- 2026-11-05T01:59:09Z focused
- 2026-11-05T01:59:10Z predicted from its closes: 13 min, 1 attempt(s)
- 2026-11-05T02:01:34Z criterion 5 verify: `bash scripts/probe-plugin-rename.sh --marketplace` → `sampo research show T-2879-probe`
- 2026-11-05T02:01:34Z criterion 5 text: Marketplace sampo: the marketplace is renamed to sampo when the scratch probe shows a foreman@foreman install survives the rename; if it doesn't, the probe's result is filed as a not-yet with what blocks it and the marketplace stays foreman → Marketplace sampo: not reachable without every user re-adding the marketplace (a marketplace's configured name comes from when it was added; probe in research T-2879-probe); the marketplace keeps the name 'foreman' as an id part, and the not-yet is filed with that blocker
- 2026-11-05T02:01:43Z step 2 not started, so nothing to verify yet: it respells producers and makes readers take both ids in cli.py, hooks.py and the skills, which the queued lanes (T-3083, T-3087's cli guards, T-3047, T-3034, T-3053, T-3055) also touch; it goes to a builder once the merge chain clears
- 2026-11-05T02:01:43Z blocked: step 2 waits for the merge chain to clear (it touches cli.py and hooks.py like the queued lanes); step 1's probe is done and decided
- 2026-11-06T03:54:00Z unblocked
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The plan's central claim, that shims in the same marketplace "list the Sampo plugin as a dependency" and "forward /foreman: commands", rests on mechanisms never verified. Plugin dependencies and command forwarding between plugins may not exist, and a skill namespace is fixed by the plugin nam…
- HIGH: The acceptance criteria never test the property the request exists for, that existing installs keep working and move themselves. `claude plugin validate`, `sampo check` and a grep scan prove the manifests are well-formed and the strings are respelled, not that an install survives. The probe s…
- HIGH: The request says "marketplace sampo", but the plan ships a `foreman` marketplace and calls that Reading 1. The marketplace rename stays gated and is not an acceptance criterion, so the task can close as done without delivering the literal ask. The 2026-11-03 decision may cover this, but the p…
- MEDIUM: Double-load is handled by an assertion, "the shim carries no hooks", and by readers that "dedupe by skill". If the shim lists `sampo` as a dependency, any command or skill files it ships will still collide with sampo's under the same names, and nothing checks it. — Add a test on the shim ma…
- MEDIUM: The `test_rename_scan` criterion allows exceptions for "alias readers, changelog and old-name tests", with no allowlist defined. A broad allowlist lets stray producers through, and a narrow one makes the test flaky. — Define the allowlist as explicit paths in the test, and make it fail on a…
- LOW: Rollback says "manifests revert", but users who already ran the migration have settings and enabled-plugin entries written under `sampo@foreman`. A manifest revert leaves those pointing at plugins that no longer exist. — Say whether readers keep honoring `sampo@*` after a revert, or whether mi…
Verdict: revise — the shim-and-dependency mechanism that carries the whole no-breakage promise is unverified and untested by the criteria; probe it first and add a criterion that proves an existing install survives.
## Dissent
- [x] HIGH: The plan's central claim, that shims in the same marketplace "list the Sampo plugin as a dependency" and "forward /foreman: commands", rests on mechanisms never verified. Plugin dependencies and command forwarding between plugins may not exist, and a skill namespace is fixed by the plugin nam… — answered: Step 1 is now a probe in a scratch Claude config that tries the renames map, shim dependencies and a marketplace rename before anything ships; step 2 builds only what the probe proved
- [x] HIGH: The acceptance criteria never test the property the request exists for, that existing installs keep working and move themselves. `claude plugin validate`, `sampo check` and a grep scan prove the manifests are well-formed and the strings are respelled, not that an install survives. The probe s… — answered: New criterion: an existing foreman@foreman install in a scratch config survives the update with every command, skill and hook working once, checked by scripts/probe-plugin-rename.sh
- [x] HIGH: The request says "marketplace sampo", but the plan ships a `foreman` marketplace and calls that Reading 1. The marketplace rename stays gated and is not an acceptance criterion, so the task can close as done without delivering the literal ask. The 2026-11-03 decision may cover this, but the p… — answered: New criterion: the marketplace becomes sampo when the probe shows installs survive it; otherwise a not-yet with the probe's result
- [x] MEDIUM: Double-load is handled by an assertion, "the shim carries no hooks", and by readers that "dedupe by skill". If the shim lists `sampo` as a dependency, any command or skill files it ships will still collide with sampo's under the same names, and nothing checks it. — Add a test on the shim ma… — answered: The probe checks double-loading; the shims ship no command, skill or hook files of their own
- [x] MEDIUM: The `test_rename_scan` criterion allows exceptions for "alias readers, changelog and old-name tests", with no allowlist defined. A broad allowlist lets stray producers through, and a narrow one makes the test flaky. — Define the allowlist as explicit paths in the test, and make it fail on a… — answered: Criterion 3 now: an explicit allowlist of paths in test_rename_scan; any other producer fails it
- [x] LOW: Rollback says "manifests revert", but users who already ran the migration have settings and enabled-plugin entries written under `sampo@foreman`. A manifest revert leaves those pointing at plugins that no longer exist. — Say whether readers keep honoring `sampo@*` after a revert, or whether mi… — answered: Rollback: readers keep honoring sampo@* and foreman@* for good, so a revert leaves migrated settings working
- [x] rival reading: **Emit-only change:** Only change what Sampo writes (generated skill text, CLI output, templates) and leave the readers and manifests for a later step. This conflicts with "every reader takes both", so it is less likely. — answered: rejected: the request says every reader takes both, so readers change in the same task; producers alone would break nothing but leave old ids read only one way
- [x] rival reading: **Alias layer instead of rename:** Keep `foreman` as the canonical id and register `sampo` as an alias via the renames map in the other direction. The request says ids "to Sampo", so this is unlikely. — answered: rejected as the end state: the request says ids to Sampo; kept as the fallback the probe may force (the shims) if a renames map can't move installs
- [x] rival reading: **Ambiguity on `fm-` prefix:** `foreman:fm-` could become `sampo:fm-` (prefix kept) or `sampo:` with the `fm-` dropped. The request says "becomes `sampo:`", which reads literally as only the namespace changing. Check against the 1396 files in `plugin/skills/` before bulk-editing. — answered: adopted as a decision: foreman:fm- becomes sampo:fm- (the prefix stays: skills and agents named fm-reviewer etc. keep their names, only the namespace changes, as the request reads literally)
- [x] rival approach: **Central normalizer, then mechanical rewrite:** Add one function in `plugin/lib/` (e.g. `plugin/lib/sampo/`) that maps `foreman:`/`/foreman:`/`foreman:fm-` to the canonical `sampo:` form. Route every reader through it. Then bulk-rewrite writers (skills, templates, `cli.py`, `plugin/bin/sampo`) wit… — answered: adopted for readers: one normaliser function in plugin/lib/sampo (core) maps foreman:, /foreman: and foreman:fm- to the sampo forms; every reader routes through it (hooks.py:224, cost.py:127-129 toda…
- [x] rival approach: **Manifest-first, split into stages:** Land the marketplace/plugin manifests and the `renames` map first, verify migration with `claude plugin test mods/foreman-ui` (the directory may need to move to `mods/sampo-ui`). Then do readers-accept-both, and only after that flip writers. Readers ship befor… — answered: adopted in order: the probe first (step 1) decides the manifest mechanism, then readers through the normaliser, then the bulk respelling; mods/foreman-ui's folder stays (a path, not an id) unless the…
- [x] rival approach: **Generate the old spellings from the new:** Make `sampo:` the single source in the skill frontmatter and templates, and generate the `foreman:` compatibility entries (plugin stubs or alias skill files) at build time. This avoids hand-maintained duplicate lists but adds a build step and may double … — answered: rejected for now: generating compatibility entries at build time needs a build step the plugin doesn't have; the normaliser covers readers, and the shims (if the probe needs them) are three small man…
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Full identity rename (likeliest):** Change the marketplace id and plugin ids (`foreman`→`sampo`, plus new `sampo-ui` from `mods/foreman-ui`, new `sampo-design`) in the manifests. Add a `renames` map (`foreman@foreman`→`sampo@sampo`) so existing installs migrate. Every emitted `/foreman:` and `for…
- **Emit-only change:** Only change what Sampo writes (generated skill text, CLI output, templates) and leave the readers and manifests for a later step. This conflicts with "every reader takes both", so it is less likely.
- **Alias layer instead of rename:** Keep `foreman` as the canonical id and register `sampo` as an alias via the renames map in the other direction. The request says ids "to Sampo", so this is unlikely.
- **Ambiguity on `fm-` prefix:** `foreman:fm-` could become `sampo:fm-` (prefix kept) or `sampo:` with the `fm-` dropped. The request says "becomes `sampo:`", which reads literally as only the namespace changing. Check against the 1396 files in `plugin/skills/` before bulk-editing.
Approaches:
- **Central normalizer, then mechanical rewrite:** Add one function in `plugin/lib/` (e.g. `plugin/lib/sampo/`) that maps `foreman:`/`/foreman:`/`foreman:fm-` to the canonical `sampo:` form. Route every reader through it. Then bulk-rewrite writers (skills, templates, `cli.py`, `plugin/bin/sampo`) wit…
- **Manifest-first, split into stages:** Land the marketplace/plugin manifests and the `renames` map first, verify migration with `claude plugin test mods/foreman-ui` (the directory may need to move to `mods/sampo-ui`). Then do readers-accept-both, and only after that flip writers. Readers ship befor…
- **Generate the old spellings from the new:** Make `sampo:` the single source in the skill frontmatter and templates, and generate the `foreman:` compatibility entries (plugin stubs or alias skill files) at build time. This avoids hand-maintained duplicate lists but adds a build step and may double …
Failure modes:
- **Readers miss a spelling:** The patterns are scattered across `fmhooks.py`, `fmguard.py`, `fmcore.py`, `fmcli.py` and the test fixtures. A hook that matches only `foreman:fm-` silently stops firing on `sampo:` commands. `python3 plugin/tests/bench_hooks.py` and `run.py` won't catch it unless the t…
- **Rename map doesn't actually migrate:** If `renames` is in the wrong manifest or keyed on the wrong form (`foreman@foreman` vs. the new marketplace name), installs stay on the old id with a dangling marketplace. Only `fm doctor` and the `e2e/roundtrip.py` flow would show it, and only if they start…
- **Bulk rewrite corrupts history and data:** A blind replace across 2421 files hits `CHANGELOG.md`, `MASTER.md`, recorded `fm replay` logs, `plugin/evals/` and fixtures. These hold old spellings on purpose (readers must still accept them). Rewriting them breaks replay determinism and removes the onl…
- **Persisted state keyed by plugin id:** Settings, enabled-plugin entries, caches, and paths containing `foreman` (e.g. `~/.claude/plugins/foreman`, `mods/foreman-ui`) are not covered by the string rewrite. After the rename they point at nothing, so hooks or the UI mod load nothing despite passing s…
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
