---
id: T-2974
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T14:20:23Z
updated: 2026-11-04T15:23:32Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (624) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T14:23:42Z
rival_split: true
builder_model: haiku
base: 84095a2934007313b449cee0f353f6879b2a6063
base_tree: 0b4e6b97fc4f9ab8395d856c2fdd42d69a7627dd
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T14:24:18Z
plan0_scope: []
lane_stop: merged 2026-11-04T15:15:53Z
verified: strong
unproven: [docs]
---
# The training lake: `sampo models export` (under an existing verb, no new top-level verb)…
## Raw request
> FEATURE: The training lake: `sampo models export` (under an existing verb, no new top-level verb) writes one flat, provenance-tagged table across every Sampo project on the machine — briefs (raw request, interpretation, options and choice, criteria, steps, type, tier), ledger decisions and outcomes, Smith journals, exam grades — labelled from outcomes (done-and-held, reverted, later-fixed as regret), with project ids and names stripped, a time split and dedupe, per-project opt-out and sensitive repos excluded by real path, Claude-written text refused (user, tool and local-model text only), tool-result text quarantined, null-tolerant rows, per-project weights, old names canonicalised and a poisoned-row canary; reproducible from a content hash
> CONTEXT: from the model brainstorm (research brainstorm-20261104-model, T-2973): Sampo's own models must be generic across every project built with Sampo, trained on outcomes, adopted per slot only where they beat today's path on whole held-out projects.
## Interpretation
Reading 1 (chosen): one reproducible export of training rows across every Sampo project on the machine, under the existing 'sampo exam models' family (no new top-level verb: the self-change gate counts verbs), each row with provenance (project hash, source file, task id hash, time), an outcome label (held, reverted, later-fixed), project names and paths stripped, sensitive and opted-out projects excluded by real path, Claude-written text refused, tool-result text quarantined into its own field, old Foreman names canonicalised, a time split and dedupe, and a canary row; the content hash names the export. Reading 2 (ruled out): train anything here; this task is the data only.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo exam models --export DIR writes rows across every Sampo project on the machine with provenance, an outcome label, names and paths stripped, sensitive and opted-out projects excluded by real path, author marked per field (user, tool, agent) with agent text excluded by default, and a manifest with per-project counts, exclusions, a canary and a content hash; a rerun on unchanged state writes the same hash — verify with `python3 plugin/tests/run.py test_lake`
- [x] a live export on this machine writes its manifest (rows per project, exclusions) into research — verify with `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/models/lake-manifest.json`
## Non-goals
## Approach (options → choice → why)
1) A lake module (plugin/lib/sampo/lake.py, its fm shim and MASTER bullet) with collect(projects) -> rows and write(dir) -> manifest, reached by `sampo exam models --export DIR`; rows from load_briefs(include_archive=True) per project, outcome labels from the ledger (done, then a revert or a later fix naming the task within 30 days = regret), the brief's text fields only (raw request, interpretation, approach, criteria texts, steps, lessons), a provenance block per row, and a manifest with counts per project, exclusions, the canary and the content hash. Likely outcome: one command gives a clean, reproducible table of ~4,000 rows. Fails if: briefs embed Claude-written prose (interpretations and approaches are often written by the agent); the row marks author=agent for those fields and the trainer's policy decides, defaulting to exclude.
2) use what exists: sampo export (AGENTS.md) and the bench's _bench_data. Likely outcome: per-project, label-only data. Fails if: neither crosses projects nor carries provenance.
3) do less: export only raw requests with type and tier labels. Likely outcome: enough for the decider heads. Fails if: the verifier and actor need outcomes and journals.
Choice 1 (75%): every later model in the slate reads the same table.
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for plugin/lib/sampo/lake.py.
## Execution prompt
## Steps
1. [x] failing tests: two fake projects (one sensitive), briefs with outcomes, a revert and a later fix, an agent-written field; the hash stable on rerun
2. [x] lake.py collect/write, the --export flag, the shim and MASTER bullet
3. [x] a live export; the manifest in research
## Resume here
<!-- auto -->
- 2026-11-04T14:30:22Z step 3/3: a live export; the manifest in research
- git: worktree-agent-aaf530a2941068a71; 2 uncommitted: plugin/lib/sampo/lake.py, plugin/tests/test_lake.py
- touched since last checkpoint: plugin/lib/fmlake.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, docs/map/files-lib-2.md, MASTER.md, plugin/tests/test_dbg.py, plugin/lib/sampo/lake.py, plugin/tests/test_lake.py
## Docs impact
CHANGELOG line; MASTER.md bullet; files-lib-2 map line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lake` → exit 0 · Ran 5 tests in 6.5s (1 classes, 16 at a time; slowest: Lake 6s) / OK [ran] [tree d3473280b8a4] [world 2f1906870a] (2026-11-04T14:29:28Z)
- (step 2) `python3 plugin/tests/run.py test_lake test_louhi_models test_rename_aliases test_docs test_left_out` → exit 0 · Ran 136 tests in 12.5s (31 classes, 16 at a time; slowest: LouhiModels 12s, Fences 9s, Lake 7s) / OK [ran] [tree d3473280b8a4] [world 2f1906870a] (2026-11-04T14:29:40Z)
- (step 3) `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/models/lake-manifest.json` → exit 0 · (no output) [ran] [tree 0e09bb350663] [world 2f1906870a] (2026-11-04T14:31:04Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_lake test_left_out test_library test_mcp test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2020 tests in 276.8s (402 classes, 16 at a time; slowest: Worker 160s, LeanKind 142s, Stop 127s) / FAILED (2 classes: test_rename_scan.RenameScan, test_bookkeeping.FinishGaps) [ran] [tree 8c52b3764505] [world 2f1906870a] (2026-11-04T14:35:42Z)
- `python3 plugin/tests/run.py test_lake` → ✗ exit 1 · Ran 0 tests in 1.5s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) (start tree + this task's tests) [ran] [tree afd4145501d0] [world 2f1906870a] (2026-11-04T15:16:18Z)
- `python3 plugin/tests/run.py test_lake` → exit 0 · Ran 5 tests in 7.2s (1 classes, 16 at a time; slowest: Lake 7s) / OK [ran] [tree afd4145501d0] [world 2f1906870a] (2026-11-04T15:16:18Z)
- (ac 1) `python3 plugin/tests/run.py test_lake` → exit 0 · Ran 5 tests in 16.7s (1 classes, 16 at a time; slowest: Lake 16s) / OK [ran] [tree bd802619e75e] [world 2f1906870a] (2026-11-04T15:16:44Z)
- (ac 2) `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/models/lake-manifest.json` → exit 0 · (no output) [ran] [tree bd802619e75e] [world 2f1906870a] (2026-11-04T15:16:44Z)
- (audit adversary) `branch diff read in full (lake.py, test_lake, cli/louhi wiring); two live exports grepped for the user name, GitHub owner, email and home paths (0 hits after the fixes); prove red on the start tree, green now` → the lake is a privacy surface. A first live export leaked the OS user from ls -l output and a GitHub owner in remote URLs and bare Owner/repo forms; now stripped (getpass user, home basename, forge URL owners, each project's github owner and git user.name) and asserted in test_lake. Secrets go through core.redact; sensitive projects judged by real path (a symlink can't sneak one in, tested); agent text is off by default [tree bd802619e75e] (2026-11-04T15:16:44Z)
- (audit edge) `branch diff read in full (lake.py, test_lake, cli/louhi wiring); two live exports grepped for the user name, GitHub owner, email and home paths (0 hits after the fixes); prove red on the start tree, green now` → names under 3 characters are not stripped (accepted: too many false hits); common-word project names are over-stripped to <project> (safe direction); a rerun on unchanged state gives the same hash (tested) [tree bd802619e75e] (2026-11-04T15:16:44Z)
- (audit intent) `branch diff read in full (lake.py, test_lake, cli/louhi wiring); two live exports grepped for the user name, GitHub owner, email and home paths (0 hits after the fixes); prove red on the start tree, green now` → one outcome-labelled table across every project, the base for the decider, verifier and actor tasks (T-2970, T-2977, T-2971) [tree bd802619e75e] (2026-11-04T15:16:44Z)
## Log
- 2026-11-04T14:20:23Z created
- 2026-11-04T14:22:45Z set approved=True
- 2026-11-04T14:23:29Z planned: it has criteria and steps
- 2026-11-04T14:24:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2974.builder.md
- 2026-11-04T14:24:17Z focused
- 2026-11-04T14:24:18Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T14:39:14Z hypothesis: the two branch-only failures are the lake's own text: lake.py string literals naming the old product (rename scan 18 vs 16) and --with-agent's help listing 'interpretation' (outranks task set in sampo which); rewording both should turn them green
- 2026-11-04T14:39:28Z ruled out: any failure from files the lane didn't touch; both were the lake's own text, green after rewording
- 2026-11-04T15:15:05Z criterion 2 verify: `test -s state/projects/foreman-4a056f/research/models/lake-manifest.json` → `test -s ~/.claude/foreman/state/projects/foreman-4a056f/research/models/lake-manifest.json`
- 2026-11-04T15:15:53Z merged worktree-agent-aaf530a2941068a71 (7 file(s))
- 2026-11-04T15:15:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aaf530a2941068a71
- 2026-11-04T15:15:57Z focused
- 2026-11-04T15:23:30Z done
- 2026-11-04T15:23:32Z committed 78122ed0 (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a new `models` noun with an `export` verb in the `plugin/lib/sampo/cli.py` dispatcher, exposed via `plugin/bin/sampo`. It reads every project's stores (briefs, ledger, Smith journals, exam grades) and writes one flat table (e.g. JSONL/Parquet) with a manifest holding the content hash. Th…
- Narrower reading: only the training-data builder is wanted, as a library function (labelling, split, dedupe, filters) with the CLI as a thin wrapper. Training and slot adoption are out of scope, since the brainstorm treats them as later work.
- Broader reading: the export is the first piece of the whole pipeline (held-out whole-project evaluation, per-slot adoption). The request lists only the export, so this is a context note, not a deliverable.
- Privacy-first reading: the exclusion and redaction rules (opt-out, real-path sensitive repos, Claude-text refusal, quarantine, stripped ids) are the core, and the table schema is secondary.
Approaches:
- New module `plugin/lib/sampo/models_export.py` as a pipeline of stages: discover projects, per-project extract, provenance-tag, filter (opt-out, realpath exclusion, authorship), label from outcomes, strip ids, dedupe, time split, weights, serialise. The `cli.py` entry only parses flags and calls it…
- Use an allow-list of authorship per field. A row's text is kept only if its provenance is user, tool or local-model, and anything else is dropped at extraction. Tool-result text goes to a separate quarantine column or file, never into the training text. This makes Claude-text refusal structural rat…
- Make reproducibility explicit. Sort rows canonically, hash the normalised content plus the config (split cutoff, weights, exclusions) into a manifest ID, and write output atomically to a path keyed by that hash. Rerunning on unchanged inputs is then byte-identical.
- Put the old-name canonicalisation in one alias map (retired verb/field names to current ones) applied at read time. Missing fields become explicit nulls in a fixed schema rather than being skipped.
Failure modes:
- Project discovery follows symlinks or relative paths, so a sensitive repo is not matched by its real path (needs `os.path.realpath` before comparing), or the same project is counted twice under two paths and double-weighted.
- Stripping project ids and names only from the id columns leaves them in free text (raw request, journals, file paths), so the table still identifies projects. The canary row can also be deduped or filtered away before it reaches the output, so it never tests anything.
- Outcome labels leak through the time split: a brief labelled "later-fixed" depends on events after the split cutoff. Dedupe that runs before the split can also put near-duplicates on both sides, which inflates held-out scores.
- The content hash covers rows but not config or the alias map, or it includes timestamps or an iteration order that varies, so the same inputs give different hashes. An opt-out added later silently changes the output without changing the hash.
## Dissent
- [x] rival reading: Likeliest: a new `models` noun with an `export` verb in the `plugin/lib/sampo/cli.py` dispatcher, exposed via `plugin/bin/sampo`. It reads every project's stores (briefs, ledger, Smith journals, exam grades) and writes one flat table (e.g. JSONL/Parquet) with a manifest holding the content hash. Th… — answered: ruled out: a new top-level noun grows the verb count the self-change gate holds; the export rides 'sampo exam models --export'
- [x] rival reading: Narrower reading: only the training-data builder is wanted, as a library function (labelling, split, dedupe, filters) with the CLI as a thin wrapper. Training and slot adoption are out of scope, since the brainstorm treats them as later work. — answered: adopted in part: the library function (lake.collect/write) is the core and the flag is thin
- [x] rival reading: Broader reading: the export is the first piece of the whole pipeline (held-out whole-project evaluation, per-slot adoption). The request lists only the export, so this is a context note, not a deliverable. — answered: adopted as order, not scope: this is the first piece; LOO measurement is T-2976
- [x] rival reading: Privacy-first reading: the exclusion and redaction rules (opt-out, real-path sensitive repos, Claude-text refusal, quarantine, stripped ids) are the core, and the table schema is secondary. — answered: adopted: the exclusions and redaction are criteria, tested with a sensitive fake project
- [x] rival approach: New module `plugin/lib/sampo/models_export.py` as a pipeline of stages: discover projects, per-project extract, provenance-tag, filter (opt-out, realpath exclusion, authorship), label from outcomes, strip ids, dedupe, time split, weights, serialise. The `cli.py` entry only parses flags and calls it… — answered: adopted: one module (lake.py) whose collect runs discover, extract, tag, filter in order
- [x] rival approach: Use an allow-list of authorship per field. A row's text is kept only if its provenance is user, tool or local-model, and anything else is dropped at extraction. Tool-result text goes to a separate quarantine column or file, never into the training text. This makes Claude-text refusal structural rat… — answered: adopted: author is recorded per field and agent text is excluded by default
- [x] rival approach: Make reproducibility explicit. Sort rows canonically, hash the normalised content plus the config (split cutoff, weights, exclusions) into a manifest ID, and write output atomically to a path keyed by that hash. Rerunning on unchanged inputs is then byte-identical. — answered: adopted: canonical sort plus a hash over rows and config names the export
- [x] rival approach: Put the old-name canonicalisation in one alias map (retired verb/field names to current ones) applied at read time. Missing fields become explicit nulls in a fixed schema rather than being skipped. — answered: adopted: one alias map for old names, applied at read time, missing fields null-tolerant
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- T-2975 [FEATURE M, planned, 3 steps] A retrieval baseline decider: for a new brief, the k nearest closed briefs by bge-m3…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
- similar past tasks were L: consider --tier L
## Lessons
- Grep a live export for the user's own identifiers (OS user, forge handle, email, home path) before trusting a privacy strip; a fixture only finds the leaks someone thought of
## Files touched
- plugin/tests/test_lake.py
- plugin/lib/sampo/lake.py
- plugin/lib/fmlake.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/louhi.py
- docs/map/files-lib-2.md
- MASTER.md
- plugin/tests/test_dbg.py
- CHANGELOG.md
