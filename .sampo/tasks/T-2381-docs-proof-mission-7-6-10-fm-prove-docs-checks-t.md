---
id: T-2381
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T14:02:21Z
updated: 2026-10-31T14:54:46Z
builder_model: sonnet
base: 82f270baef458d2a455b4c982a5be090b7b1062b
base_tree: 995a4ec41c7beb99ae37fad2630dfcdb9bab5880
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T14:14:22Z
plan0_scope: []
verified: strong
---
# Docs proof (Mission 7, #6/#10): fm prove --docs checks the repo's own CLI flags, subcommands, paths and fenced examples in its docs against the code: static in any tree, run in a trusted throwaway copy
## Raw request
> Docs proof (Mission 7, #6/#10): fm prove --docs checks the repo's own CLI flags, subcommands, paths and fenced examples in its docs against the code: static in any tree, run in a trusted throwaway copy
## Interpretation
Gap map #6/#10 docs truth (3): fm docs checks paths and npm/make targets, fmfind's docs finder checks function names; nothing checks the flags, subcommands and examples the docs give for the repo's own CLI, so docs that lie about the code pass. On Foreman's own docs the static rung finds 0 of 345 flags missing (T-1011's self-docs check covers Foreman), so its value is measured on other repos and the exam's docs and beyond kinds.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove --docs [FILE...] lists each docs claim (a path, a make or npm target, a flag or subcommand of the repo's own CLI, a fenced command) as proven, failed or unproven; a flag or subcommand the docs name that no tracked non-doc file contains fails in any tree; in a trusted tree each fenced command of the repo's CLI runs in a throwaway copy with fm prove's environment and a flag missing from its --help fails; exit 0 none failed, 1 a failure, 2 nothing checkable — verify with `python3 plugin/tests/run.py test_prove -k docs_proof`
- [x] fm task finish's docs check (fmdocs.task_docs) runs the static rung on the lines the task added to the docs it names, so a renamed flag left in the README blocks the close, while a prose-only addition such as a CHANGELOG line checks nothing — verify with `python3 plugin/tests/run.py test_docsdrift -k docs_proof`
- [x] A flag or subcommand the static rung finds only as text in a tracked file is unproven, not proven (text in a file isn't a working flag); a flag is proven only by a run of a documented command that uses it and exits 0, and one its subcommand's --help doesn't list fails — verify with `python3 plugin/tests/run.py test_prove -k docs_proof_static`
- [x] A fenced command whose docs show its output (lines after the command in the same block, or an output block right after it) is proven only when the run's output contains those lines; a mismatch fails, so a command that exits 0 while doing something other than what the docs show isn't proven — verify with `python3 plugin/tests/run.py test_prove -k docs_proof_output`
## Non-goals
## Approach (options → choice → why)
1) grow fm prove with a --docs kind: a static rung (git grep, any tree) and a run rung (trusted throwaway copy, --help and fenced commands), reusing fmdocs' scanner and fm prove's copy, environment and consent. 2) a model reads docs and code and judges drift: rejected as proof, a model judging a model is labelled model-judged. 3) per-language CLI parsers (argparse, click, commander, clap) read statically: rejected, hand-written per language against standing intent 5; the CLI's own --help is the runtime signal. Choice 1: one verb, ecosystem-agnostic, its static half free in any tree.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first: a stub repo whose README names a flag its CLI lacks, a correct README, and a prose-only doc
2. [x] static rung: claims from fm docs' detectors plus the repo's CLI found from its manifest (pyproject scripts, package.json bin, Cargo bin targets, bin/), checked with git grep over tracked non-doc files
3. [x] run rung: trusted trees only, fm prove's throwaway copy and scrubbed environment, each fenced command under a timeout, documented flags checked against the subcommand's --help
4. [x] finish reach through task_docs; MASTER.md, README, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T14:44:23Z steps 4/4 done
- git: worktree-agent-a701b6b5afd673f6f; 0 uncommitted
- touched since last checkpoint: plugin/tests/test_prove.py, plugin/lib/fmdocs.py, plugin/lib/fmcli.py, MASTER.md, plugin/lib/fmprove.py
## Docs impact
README.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove -k docs_proof` → ✗ exit 1 · Ran 5 tests in 8.9s (1 classes, 16 at a time; slowest: DocsProof 3s) / FAILED (1 classes: test_prove.DocsProof) [ran] [tree 0817718a4342] (2026-10-31T14:17:13Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k docs_proof 2>&1 | tail -40` → exit 0 · Ran 5 tests in 4.2s (1 classes, 16 at a time; slowest: DocsProof 3s) / OK [ran] [tree 70c99a6fb17f] (2026-10-31T14:20:18Z)
- (step 2) `python3 plugin/tests/run.py test_prove -k docs_proof` → exit 0 · Ran 5 tests in 2.0s (1 classes, 16 at a time; slowest: DocsProof 2s) / OK [ran] [tree 69f4b475c7e7] (2026-10-31T14:22:21Z)
- (step 3) `python3 plugin/tests/run.py test_docsdrift -k docs_proof` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: TaskDocsDrift 0s) / OK [ran] [tree 69f4b475c7e7] (2026-10-31T14:22:22Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_docsdrift test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 423 tests in 60.2s (93 classes, 16 at a time; slowest: TaskLifecycle 60s, VerifyStrength 38s, BoardVerbs 37s) / FAILED (1 classes: test_docs.ReadmeShape) [ran] [tree 69f4b475c7e7] (2026-10-31T14:23:24Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_docsdrift test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 423 tests in 61.2s (93 classes, 16 at a time; slowest: TaskLifecycle 61s, BoardVerbs 46s, VerifyStrength 45s) / FAILED (1 classes: test_docs.ReadmeShape) [ran] [tree c5f7d60dfb05] (2026-10-31T14:24:41Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_docsdrift test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 423 tests in 38.4s (93 classes, 16 at a time; slowest: TaskLifecycle 38s, VerifyStrength 23s, BoardVerbs 21s) / FAILED (1 classes: test_docs.ReadmeShape) [ran] [tree 1a71a5c42ad0] (2026-10-31T14:25:39Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_docsdrift test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.39s] [ran] [tree 37ea3264d0e6] (2026-10-31T14:28:04Z)
- (step 4) `python3 plugin/tests/run.py test_docsdrift -k docs_proof` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: TaskDocsDrift 0s) / OK [ran] [tree 37ea3264d0e6] (2026-10-31T14:28:10Z)
- (step 1) `python3 plugin/tests/run.py test_prove -k docs_proof_static` → exit 0 · Ran 6 tests in 1.8s (1 classes, 16 at a time; slowest: DocsProof 1s) / OK [ran] [tree d3b0525eb753] (2026-10-31T14:36:56Z)
- (step 4) `python3 plugin/tests/run.py test_prove test_docsdrift` → exit 0 · Ran 39 tests in 3.7s (7 classes, 16 at a time; slowest: DocsProof 3s, VerifyStrength 3s, Migration 2s) / OK [ran] [tree d3b0525eb753] (2026-10-31T14:37:00Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_docsdrift test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [17.95s] [ran] [tree d3b0525eb753] (2026-10-31T14:38:11Z)
- (step 1) `python3 plugin/tests/run.py test_prove -k docs_proof_output` → red as expected (exit 1) · Ran 6 tests in 1.8s (1 classes, 16 at a time; slowest: DocsProof 1s) / FAILED (1 classes: test_prove.DocsProof) [ran] [tree 90a1a4d678dc] (2026-10-31T14:46:02Z)
- (step 2) `python3 plugin/tests/run.py test_prove -k docs_proof_output` → exit 0 · Ran 6 tests in 4.3s (1 classes, 16 at a time; slowest: DocsProof 4s) / OK [ran] [tree 9d061d3b182d] (2026-10-31T14:46:59Z)
- (step 3) `python3 plugin/tests/run.py test_prove test_docsdrift` → exit 0 · Ran 45 tests in 7.7s (7 classes, 16 at a time; slowest: DocsProof 7s, VerifyStrength 3s, Migration 2s) / OK [ran] [tree 9d061d3b182d] (2026-10-31T14:47:07Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_docsdrift test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 436 tests in 60.6s (93 classes, 16 at a time; slowest: TaskLifecycle 60s, BoardVerbs 36s, VerifyStrength 35s) / FAILED (1 classes: test_board_verbs.BoardVerbs) [ran] [tree 9d061d3b182d] (2026-10-31T14:48:11Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_docsdrift test_find test_guard_cases test_paused test_prove test_robustness test_statusline_ui test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [25.19s] [ran] [tree 9d061d3b182d] (2026-10-31T14:50:54Z)
- (step 3) `python3 plugin/tests/run.py test_prove test_docsdrift` → exit 0 · Ran 45 tests in 2.3s (7 classes, 16 at a time; slowest: DocsProof 2s, Migration 1s, FindReview 1s) / OK [ran] [tree d69b84b1678f] (2026-10-31T14:53:29Z)
- (ac 1) `python3 plugin/tests/run.py test_prove -k docs_proof` → exit 0 · Ran 18 tests in 2.3s (1 classes, 16 at a time; slowest: DocsProof 2s) / OK [ran] [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (ac 2) `python3 plugin/tests/run.py test_docsdrift -k docs_proof` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: TaskDocsDrift 0s) / OK [ran] [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (ac 3) `python3 plugin/tests/run.py test_prove -k docs_proof_static` → exit 0 · Ran 6 tests in 0.7s (1 classes, 16 at a time; slowest: DocsProof 0s) / OK [ran] [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (ac 4) `python3 plugin/tests/run.py test_prove -k docs_proof_output` → exit 0 · Ran 6 tests in 1.1s (1 classes, 16 at a time; slowest: DocsProof 1s) / OK [ran] [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (audit intent) `one fm-reviewer pass (all five lenses): changes needed, all fixed on the branch: text in a file is unproven, only a trusted run that exits 0 proves a flag (criterion 3), documented output must match the run (criterion 4, red then green), trust and copy use the named folder not the git root, -- ends flag parsing, py parameter-derived flags count, bin shims stay unproven, absolute/~/.. args skipped in the run rung; 45 tests OK after merge` → four criteria met: static rung disproves only, run rung proves, task_docs blocks a renamed flag on added lines, output the docs show must match (tested) [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): changes needed, all fixed on the branch: text in a file is unproven, only a trusted run that exits 0 proves a flag (criterion 3), documented output must match the run (criterion 4, red then green), trust and copy use the named folder not the git root, -- ends flag parsing, py parameter-derived flags count, bin shims stay unproven, absolute/~/.. args skipped in the run rung; 45 tests OK after merge` → the run rung runs only in a trusted tree, on a throwaway copy with a scrubbed env, never with absolute or home paths; the trust record never widens past the named folder (tested) [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (audit edge) `one fm-reviewer pass (all five lenses): changes needed, all fixed on the branch: text in a file is unproven, only a trusted run that exits 0 proves a flag (criterion 3), documented output must match the run (criterion 4, red then green), trust and copy use the named folder not the git root, -- ends flag parsing, py parameter-derived flags count, bin shims stay unproven, absolute/~/.. args skipped in the run rung; 45 tests OK after merge` → a single-file check can't judge subcommand typos (one-subcommand rule); a timestamp in documented output would false-fail (no wildcard beyond ... and <x>) [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (audit operator) `one fm-reviewer pass (all five lenses): changes needed, all fixed on the branch: text in a file is unproven, only a trusted run that exits 0 proves a flag (criterion 3), documented output must match the run (criterion 4, red then green), trust and copy use the named folder not the git root, -- ends flag parsing, py parameter-derived flags count, bin shims stay unproven, absolute/~/.. args skipped in the run rung; 45 tests OK after merge` → bounded: 30 commands, 20 s each, 300 s per run; corpus capped at 4000 files and 8 MB per M/L close [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
- (audit maintainer) `one fm-reviewer pass (all five lenses): changes needed, all fixed on the branch: text in a file is unproven, only a trusted run that exits 0 proves a flag (criterion 3), documented output must match the run (criterion 4, red then green), trust and copy use the named folder not the git root, -- ends flag parsing, py parameter-derived flags count, bin shims stay unproven, absolute/~/.. args skipped in the run rung; 45 tests OK after merge` → regular() public; dict-based dedupe [tree 4962ef3f09d1] (2026-10-31T14:53:55Z)
## Log
- 2026-10-31T14:02:21Z created
- 2026-10-31T14:14:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2381.builder.md
- 2026-10-31T14:14:22Z focused
- 2026-10-31T14:14:22Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T14:28:51Z criterion 3 text: A flag or subcommand the static rung finds only as text in a tracked file is unproven, not proven (text in a file isn't a working flag); only the run rung's --help listing or a run that exits 0 proves it → A flag or subcommand the static rung finds only as text in a tracked file is unproven, not proven (text in a file isn't a working flag); a flag is proven only by a run of a documented command that uses it and exits 0, and one its subcommand's --help doesn't list fails
- 2026-10-31T14:53:26Z merged worktree-agent-a701b6b5afd673f6f (7 file(s))
- 2026-10-31T14:53:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a701b6b5afd673f6f
- 2026-10-31T14:53:26Z focused
- 2026-10-31T14:53:49Z scope: plugin/lib/fmdocs.py, plugin/lib/fmprove.py, plugin/lib/fmcli.py, plugin/tests/test_prove.py, plugin/tests/test_docsdrift.py, README.md, MASTER.md, CHANGELOG.md
- 2026-10-31T14:54:44Z done
- 2026-10-31T14:54:46Z committed db16058c (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
- the similar finished task took 2 steps
## Lessons
- A presence check can only disprove; proof needs a run that could have failed
## Plan gaps
- failed first: step 1 failing tests first: a stub repo whose README names a flag its CLI lacks, a correct README, and a p…
## Files touched
- plugin/tests/test_prove.py
- plugin/tests/test_docsdrift.py
- plugin/lib/fmdocs.py
- plugin/lib/fmprove.py
- plugin/lib/fmcli.py
- MASTER.md
- README.md
- plugin/lib/.fm-nothing
- CHANGELOG.md
