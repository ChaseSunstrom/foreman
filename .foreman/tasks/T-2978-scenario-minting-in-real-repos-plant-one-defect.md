---
id: T-2978
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T14:20:23Z
updated: 2026-11-04T17:45:38Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (624) held on the first finish 98% of the time: 28 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T14:30:59Z
rival_split: true
builder_model: haiku
base: 78122ed04551eb0675258ec322e9736c8b648c5d
base_tree: bd802619e75e6a0ac139b142c87679e8d1906717
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T14:31:29Z
plan0_scope: []
lane_stop: merged 2026-11-04T15:24:26Z
verified: strong
unproven: [docs]
---
# Scenario minting in real repos: plant one defect by mutation in a Sampo project's real…
## Raw request
> FEATURE: Scenario minting in real repos: plant one defect by mutation in a Sampo project's real code inside a throwaway worktree (an off-by-one, a dropped check, a swapped condition), keep it only when the project's own tests catch it, and file it as a Louhi scenario with its language and kind; across every project's languages, so the actor's rejection-sampling loop has verified scenarios at scale
> CONTEXT: from the model brainstorm (research brainstorm-20261104-model, T-2973): Sampo's own models must be generic across every project built with Sampo, trained on outcomes, adopted per slot only where they beat today's path on whole held-out projects.
## Interpretation
Reading 1 (chosen): mint Louhi scenarios from real Sampo projects: in a throwaway worktree of a project's HEAD, apply one small mutation to a source file its tests cover (flip a comparison, drop a guard clause, swap two arguments, off-by-one a range bound, negate a condition), keep it only when the project's own tests go red and the unmutated tree is green, and file it as a scenario (language, kind bug, the request the tests imply, the grading key: the file and symbol) that sampo exam run can serve; mutation is deterministic from a seed, so a scenario can be rebuilt. Reading 2 (ruled out): have a model write the bugs; deterministic mutation needs no model, is reproducible and can't leak a fix into the request.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo exam gen --from-repo PATH --n N mints scenarios in a throwaway worktree: each is one deterministic mutation the project's tests catch on a tree whose tests pass unmutated; a mutation the tests miss is dropped and counted; the main checkout is untouched — verify with `python3 plugin/tests/run.py test_mint`
- [x] minted scenarios run through sampo exam run like seeded ones and are graded by the planted file and symbol — verify with `python3 plugin/tests/run.py test_mint test_exam`
## Non-goals
## Approach (options → choice → why)
1) A mint module (plugin/lib/sampo/mint.py, its fm shim and a map bullet) with operators per language (Python via ast; JS/TS, Rust, C, Ruby by conservative token rewrites of comparison operators and integer bounds), run in a throwaway worktree, the project's test command from fm map's gate detection, keep-if-red, a scenario JSON beside Louhi's seeded ones under the run, reached by `sampo exam gen --from-repo PATH --n N` (an existing verb's flag). Likely outcome: dozens of verified scenarios per project in real code. Fails if: a project's suite is slow; a per-mutation time cap and a sample bound keep it in budget.
2) use what exists: Louhi's templates with more variants. Likely outcome: more of the same toy repos. Fails if: the actor needs real codebases to generalise.
3) do less: Python only via ast. Likely outcome: the safest operators, one language. Fails if: the generic claim needs every language Sampo projects use.
Choice 1 (70%): real code, verified by the project's own tests, reproducible from a seed.
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for plugin/lib/sampo/mint.py.
## Execution prompt
## Steps
1. [x] failing tests: a tiny Python repo with tests; a mutation they catch is kept, one they miss is dropped, HEAD untouched
2. [x] mint.py operators (Python ast, token rewrites for the rest), the worktree runner, the scenario file, the --from-repo flag
3. [x] a live mint on two of this machine's projects in different languages
## Resume here
<!-- auto -->
- 2026-11-04T14:40:38Z step 2/3: mint.py operators (Python ast, token rewrites for the rest), the worktree runner, the scenario file, the --from-repo flag
- git: worktree-agent-afe64527985dea25b; 5 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/lib/fmmint.py, plugin/lib/sampo/mint.py, plugin/tests/test_mint.py
- touched since last checkpoint: plugin/lib/sampo/mint.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/cli.py, plugin/lib/fmmint.py, plugin/tests/test_mint.py
## Docs impact
CHANGELOG line; research T-2978-minting; MASTER bullet and map line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_mint 2>&1 | tail -n 25` → ✗ exit 1 · Ran 5 tests in 5.5s (1 classes, 16 at a time; slowest: MintFromRepo 2s) / FAILED (1 classes: test_mint.MintFromRepo) [ran] [tree 89608a284dc1] [world 2f1906870a] (2026-11-04T14:35:35Z)
- (step 1) `python3 plugin/tests/run.py test_mint` → ✗ exit 1 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: MintFromRepo 1s) / FAILED (1 classes: test_mint.MintFromRepo) [ran] [tree 89608a284dc1] [world 2f1906870a] (2026-11-04T14:39:19Z)
- (ac 1) `python3 plugin/tests/run.py test_mint 2>&1 | tail -n 60` → ✗ exit 1 · Ran 6 tests in 7.1s (1 classes, 16 at a time; slowest: MintFromRepo 6s) / FAILED (1 classes: test_mint.MintFromRepo) [ran] [tree d9b95cfa3291] [world 2f1906870a] (2026-11-04T14:41:21Z)
- (ac 2) `python3 plugin/tests/run.py test_mint test_exam 2>&1 | tail -n 80` → exit 0 · Ran 115 tests in 160.2s (28 classes, 16 at a time; slowest: LeanKind 160s, ExamAuthors 113s, ExamGen 109s) / OK [ran] [tree 6d15acdfad55] [world 2f1906870a] (2026-11-04T14:44:20Z)
- (step 2) `python3 plugin/tests/run.py test_mint test_exam 2>&1 | tail -n 80` → exit 0 · Ran 115 tests in 160.2s (28 classes, 16 at a time; slowest: LeanKind 160s, ExamAuthors 113s, ExamGen 109s) / OK [ran] [tree 6d15acdfad55] [world 2f1906870a] (2026-11-04T14:44:20Z)
- (step 2) `python3 plugin/tests/run.py test_mint test_exam` → exit 0 · Ran 115 tests in 205.3s (28 classes, 16 at a time; slowest: LeanKind 205s, ExamAuthors 114s, ExamGen 97s) / OK [ran] [tree 6cf2e119bba8] [world 2f1906870a] (2026-11-04T14:48:02Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_cli test_code test_core test_design_tokens test_docs test_docsdrift test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_mcp test_mint test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 2022 tests in 262.3s (402 classes, 16 at a time; slowest: Worker 180s, Stop 138s, LeanKind 117s) / FAILED (2 classes: test_docs.PluginFiles, test_docs.MapShards) [ran] [tree 6cf2e119bba8] [world 2f1906870a] (2026-11-04T14:54:01Z)
- (step 3) `python3 plugin/tests/run.py test_docs 2>&1 | tail -n 4` → exit 0 · Ran 112 tests in 13.3s (27 classes, 16 at a time; slowest: Fences 13s, DocsProof 6s, TaskLifecycle 4s) / OK [ran] [tree 880471d416d2] [world 2f1906870a] (2026-11-04T14:54:41Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 112 tests in 9.1s (27 classes, 16 at a time; slowest: Fences 9s, DocsProof 3s, Site 2s) / OK [ran] [tree 880471d416d2] [world 2f1906870a] (2026-11-04T14:57:49Z)
- (step 1) `python3 plugin/tests/run.py test_mint` → exit 0 · Ran 17 tests in 4.8s (2 classes, 16 at a time; slowest: MintWithUntrackedDeps 4s, MintFromRepo 3s) / OK [ran] [tree e56a7f5eb897] [world 2f1906870a] (2026-11-04T17:33:06Z)
- `python3 plugin/tests/run.py test_mint` → ✗ exit 1 · Ran 17 tests in 3.3s (2 classes, 16 at a time; slowest: MintWithUntrackedDeps 2s, MintFromRepo 1s) / FAILED (2 classes: test_mint.MintWithUntrackedDeps, test_mint.MintFromRepo) (start tree + this task's tests) [ran] [tree e56a7f5eb897] [world 2f1906870a] (2026-11-04T17:33:14Z)
- `python3 plugin/tests/run.py test_mint` → exit 0 · Ran 17 tests in 4.4s (2 classes, 16 at a time; slowest: MintWithUntrackedDeps 4s, MintFromRepo 3s) / OK [ran] [tree e56a7f5eb897] [world 2f1906870a] (2026-11-04T17:33:14Z)
- (ac 1) `python3 plugin/tests/run.py test_mint` → exit 0 · Ran 17 tests in 9.8s (2 classes, 16 at a time; slowest: MintWithUntrackedDeps 9s, MintFromRepo 7s) / OK [ran] [tree ce2cddbe1c20] [world 2f1906870a] (2026-11-04T17:37:18Z)
- (ac 2) `python3 plugin/tests/run.py test_mint test_exam` → exit 0 · Ran 126 tests in 202.3s (29 classes, 16 at a time; slowest: LeanKind 201s, ExamAuthors 105s, ExamGen 88s) / OK [ran] [tree ce2cddbe1c20] [world 2f1906870a] (2026-11-04T17:37:18Z)
- (audit adversary) `branch diff read in full before merge (mint gen, _candidates, _scenario; louhi passes/_check_one for origin minted; test_mint); grade cap gap fixed on the branch test-first; live mints on two real projects in two languages (T-2987 did the deps); prove red on the start tree, green now` → the target repo's own test command runs only in throwaway copies under the sandbox env (no forge or cloud credentials); HEAD and the checkout are untouched (tested); linked deps are never written (no bytecode, tested) [tree ce2cddbe1c20] (2026-11-04T17:37:18Z)
- (audit edge) `branch diff read in full before merge (mint gen, _candidates, _scenario; louhi passes/_check_one for origin minted; test_mint); grade cap gap fixed on the branch test-first; live mints on two real projects in two languages (T-2987 did the deps); prove red on the start tree, green now` → red or flaky at HEAD mints nothing (tested); a mutant with no verdict is skipped, never kept; the same seed mints the same list (tested) [tree ce2cddbe1c20] (2026-11-04T17:37:18Z)
- (audit intent) `branch diff read in full before merge (mint gen, _candidates, _scenario; louhi passes/_check_one for origin minted; test_mint); grade cap gap fixed on the branch test-first; live mints on two real projects in two languages (T-2987 did the deps); prove red on the start tree, green now` → real-code scenarios across languages for the generic model (T-2971's farm, T-2977's negatives); numbers in research T-2978-minting [tree ce2cddbe1c20] (2026-11-04T17:37:18Z)
## Log
- 2026-11-04T14:20:23Z created
- 2026-11-04T14:29:04Z planned: it has criteria and steps
- 2026-11-04T14:29:05Z set approved=True
- 2026-11-04T14:31:09Z steer: baseline green twice before minting; dedup by normalized diff hash; scenario shape matches louhi's seeded ones plus origin=minted
- 2026-11-04T14:31:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2978.builder.md
- 2026-11-04T14:31:28Z focused
- 2026-11-04T14:31:29Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T15:24:26Z merged worktree-agent-afe64527985dea25b (7 file(s))
- 2026-11-04T15:24:36Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-afe64527985dea25b
- 2026-11-04T17:32:52Z focused
- 2026-11-04T17:33:42Z scope: MASTER bullet, map line and fmjeffexport shim for T-2970's merged jeffexport module (the repo-wide self-docs gate blocked this close)
- 2026-11-04T17:45:37Z done
- 2026-11-04T17:45:38Z committed a61fe5db (4 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a mutation-based minting pipeline. For a target project, create a throwaway `git worktree`, apply one AST- or regex-level mutation (off-by-one, dropped guard, swapped comparison) to a non-test source file, run the project's own test command, keep it only if a previously green suite goes …
- A library/CLI feature inside Sampo (`plugin/lib/sampo/cli.py`, run as `fm`/`sampo` subcommand, e.g. `sampo mint`) that batches over all registered projects and emits scenarios as the corpus the actor's rejection-sampling loop consumes; the "at scale" part is the throughput, scheduling and dedup lay…
- Narrower: only Sampo's own repo (Python in `plugin/lib/`, TS in `mods/foreman-ui`) as the "real project", using `plugin/tests/test_*.py` → source mapping as the oracle. "Every project's languages" says this is not the intent, but it is the cheapest first slice.
- Unclear what "file it as a Louhi scenario" means: an existing Louhi schema/store I haven't located in the map, or a new one. This changes the output format, so it needs checking in the repo before building.
Approaches:
- Language-pluggable mutator: a registry keyed by language (Python via `ast`, TS/JS via regex or tree-sitter, others via a generic token-level operator-swap fallback) with a few operator classes (`off_by_one`, `drop_check`, `swap_condition`). Each emits a candidate patch. A runner applies it in a wor…
- Reuse the test→source mapping that the project map already derives (e.g. `test_away.py` → `fmaway.py`) to select only the covering tests per mutant instead of the full suite. Cheaper, but a kill under a subset can mean something different from a kill under the full suite, so re-verify survivors aga…
- Put the pipeline in `plugin/lib/sampo/` as a new module with a `cli.py` subcommand, producing Louhi scenario files plus a manifest. Sampling is weighted by (language, kind) for balance, and dedup is by a normalized diff hash, so rejection-sampling gets a diverse corpus, not 1000 variants of one com…
- Baseline gate first: run the suite on the unmutated worktree and abort on red or flaky (run twice). Otherwise every "kill" is just pre-existing failure.
Failure modes:
- Flaky or environment-dependent tests (`plugin/tests/bench_hooks.py`, timing-based or hook tests) read as kills, so scenarios get filed where the defect isn't what fails. Only a baseline-green-twice plus a re-run of the mutant on the failing test set guards this.
- Equivalent or trivially detectable mutants: mutations in docs, strings, `CHANGELOG.md`, templates or dead code, or ones that cause an import/syntax error, are "caught" by the tests without being realistic defects. This yields scenarios the actor solves by reading a traceback, with no training signa…
- Worktree isolation leaks: tests that write to the real repo, `~/.claude`, shared ports or `plugin/tests/fixtures/instruments/repo/app.py`, or that use absolute paths, mean a mutant run mutates shared state or passes or fails because of another run when minting in parallel.
- The corpus is skewed toward Python (the dominant language in `plugin/lib/` and `plugin/tests/`), so the "generic across every project" goal is not met; held-out whole-project evaluation is then contaminated if scenarios from one project end up in both train and eval splits.
## Dissent
- [x] rival reading: Likeliest: a mutation-based minting pipeline. For a target project, create a throwaway `git worktree`, apply one AST- or regex-level mutation (off-by-one, dropped guard, swapped comparison) to a non-test source file, run the project's own test command, keep it only if a previously green suite goes … — answered: agrees with the plan's reading
- [x] rival reading: A library/CLI feature inside Sampo (`plugin/lib/sampo/cli.py`, run as `fm`/`sampo` subcommand, e.g. `sampo mint`) that batches over all registered projects and emits scenarios as the corpus the actor's rejection-sampling loop consumes; the "at scale" part is the throughput, scheduling and dedup lay… — answered: one repo per call keeps it simple; the night job or a loop over sampo's project list batches later
- [x] rival reading: Narrower: only Sampo's own repo (Python in `plugin/lib/`, TS in `mods/foreman-ui`) as the "real project", using `plugin/tests/test_*.py` → source mapping as the oracle. "Every project's languages" says this is not the intent, but it is the cheapest first slice. — answered: ruled out: the model must be generic across Sampo projects, so more than Sampo's own repo
- [x] rival reading: Unclear what "file it as a Louhi scenario" means: an existing Louhi schema/store I haven't located in the map, or a new one. This changes the output format, so it needs checking in the repo before building. — answered: the builder reads louhi.py's seeded scenario shape and writes the same one, adding origin=minted
- [x] rival approach: Language-pluggable mutator: a registry keyed by language (Python via `ast`, TS/JS via regex or tree-sitter, others via a generic token-level operator-swap fallback) with a few operator classes (`off_by_one`, `drop_check`, `swap_condition`). Each emits a candidate patch. A runner applies it in a wor… — answered: adopted as plain per-language functions in one dict, no registry class
- [x] rival approach: Reuse the test→source mapping that the project map already derives (e.g. `test_away.py` → `fmaway.py`) to select only the covering tests per mutant instead of the full suite. Cheaper, but a kill under a subset can mean something different from a kill under the full suite, so re-verify survivors aga… — answered: full suite with a per-mutation time cap; a subset kill means less
- [x] rival approach: Put the pipeline in `plugin/lib/sampo/` as a new module with a `cli.py` subcommand, producing Louhi scenario files plus a manifest. Sampling is weighted by (language, kind) for balance, and dedup is by a normalized diff hash, so rejection-sampling gets a diverse corpus, not 1000 variants of one com… — answered: adopted: dedup by a hash of the normalized diff
- [x] rival approach: Baseline gate first: run the suite on the unmutated worktree and abort on red or flaky (run twice). Otherwise every "kill" is just pre-existing failure. — answered: adopted: the unmutated suite must pass twice or the repo is skipped as flaky
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261104-model: Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than j…
- T-2976 [FEATURE M, planned, 3 steps] Leave-one-project-out measurement and adoption: the model bench holds out whole…
- T-2974 [FEATURE M, active, 3 steps] The training lake: `sampo models export` (under an existing verb, no new top-level verb)…
- decision 2026-11-04: Recommendation: build Sampo's own model family generic across every Sampo project in this order — the training lake (T-2974), a retrieval baseline d…
## Lessons
- Minting from a real project is gated by its test suite's speed and its untracked deps, not by the mutation operators; time the suite in a copy first
## Plan gaps
- failed first: step 1 failing tests: a tiny Python repo with tests; a mutation they catch is kept, one they miss is dropp…
## Files touched
- plugin/tests/test_mint.py
- plugin/lib/sampo/mint.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/cli.py
- plugin/lib/fmmint.py
- docs/map/files-lib-3.md
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmjeffexport.py
- docs/map/files-lib-2.md
