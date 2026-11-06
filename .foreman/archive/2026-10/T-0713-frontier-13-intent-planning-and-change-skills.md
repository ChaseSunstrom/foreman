---
id: T-0713
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T19:33:08Z
base: 991f827aec22f4d889a861dab9bec94a2ad4c15a
base_tree: 93c0781f351179363175101111a54396efe9c7d5
verified: strong
---
# Frontier 13 — Intent, planning and change skills
## Raw request
> FEATURE: Frontier 13 — Intent, planning and change skills
> CONTEXT: A wish becomes an executable spec and a priced plan, and large mechanical changes are done as one rule, not hundreds of edits.
> CONTEXT: first slice: Intent compiler that turns a one-liner into a red spec, plus structural rewrite with cheap converter for leftovers.
> CONTEXT: proof at close: A rename/migration across a fixture repo done by one rule with zero residual sites, and a one-line wish yields a red spec.
> CONTEXT: members (15, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Mechanical pre-mortem: the beliefs a plan silently rests on, compiled to probes; Prediction ledger and confusion meter; Intent compiler: a one-line wish becomes a red, executable spec, and ambiguity is resolved by picking between concrete outputs; User twin: answers on your behalf where your own history proves it would, and pre-builds your next ask; Metric hunt: state a number, and Foreman runs an overnight evolutionary search on your code against it, with statistical proof; One rule instead of a hundred edits; Cheap converter for the sites a rule couldn't match; Upgrade everything at once; group testing isolates the few that break; Migrations as a burndown whose contract step can't run early; Schema changes checked against real data shape before they run; Public-surface diff with a check of every consumer repo on this machine; Record real HTTP traffic once, replay it as a contract test forever; Semver from the surface diff, notes from the briefs, an install round-trip; Docs tested like code: runnable blocks run, every mentioned flag must exist; Do likewise: Foreman generalises the agent's own last two edits into a rule and finds the rest
## Interpretation
First slice of Frontier 13. Intent compiler: fm spec "<wish>" --module M asks one tool-less child (no code, no repo) for concrete assertions about M, keeps only safe ones (comparisons over calls into M and literals; no imports, dunders, eval, open, os), writes them as a unittest file and runs it once to show it red. Structural change: fm rewrite OLD NEW [--glob G] [--apply] renames an identifier in one rule — Python by tokens, so code changes and strings/comments are left as residual sites; other code files by whole word — and lists every residual site (strings, comments, case and separator variants such as OldName, OLD_NAME, old-name); --convert hands the residual lines to a cheap child and applies the lines it returns when they no longer hold the old name.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm spec writes a red unittest from a one-line wish, keeping only safe assertions — verify with `python3 plugin/tests/run.py -p test_intent.py -k Spec`
- [x] fm rewrite renames code sites in one rule, leaves and lists strings/comments/variants as residuals, and --convert clears them to zero — verify with `python3 plugin/tests/run.py -p test_intent.py -k Rewrite`
## Non-goals
## Approach (options → choice → why)
Spec: (a) a model writes the whole test file — runs arbitrary code when executed; (b) the child returns one assert per line, validated by an AST allowlist before it's written or run — chosen; (c) a template with placeholders — not executable. Rewrite: (a) sed over the tree — renames inside strings and unrelated words; (b) tokenize-based rename for Python plus whole-word for other code, residuals listed — chosen: stdlib, exact for code; (c) ast-grep or comby — not installed here. Converter: Haiku via the existing tool-less child runner, budget-checked; only lines that lose the old name are applied. Deferred: pre-mortem probes, user twin, metric hunt, group-tested upgrades, surface diffs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fm spec with the assertion allowlist
3. [x] fm rewrite with residuals and --convert
4. [x] proof runs, docs, CHANGELOG, full suite
## Resume here
## Docs impact
CHANGELOG; MASTER.md module list (fmchange)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_intent.py` → ✗ exit 1 · Ran 3 tests in 0.3s (2 classes, 16 at a time; slowest: Rewrite 0s, Spec 0s) / FAILED (2 classes) [ran] [tree f02745df2dce] (2026-10-09T19:29:25Z)
- (step 2) `python3 plugin/tests/run.py -p test_intent.py -k Spec` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Spec 0s) / OK [ran] [tree afd0f90d0155] (2026-10-09T19:32:00Z)
- (step 3) `python3 plugin/tests/run.py -p test_intent.py -k Rewrite` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Rewrite 0s) / OK [ran] [tree afd0f90d0155] (2026-10-09T19:32:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_intent.py` → exit 0 · Ran 3 tests in 0.4s (2 classes, 16 at a time; slowest: Rewrite 0s, Spec 0s) / OK [ran] [tree afd0f90d0155] (2026-10-09T19:32:01Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1159 tests in 58.9s (336 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree dae7b9b59e59] (2026-10-09T19:33:00Z)
- (ac 1) `python3 plugin/tests/run.py -p test_intent.py -k Spec` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Spec 0s) / OK [ran] [tree dae7b9b59e59] (2026-10-09T19:33:07Z)
- (ac 2) `python3 plugin/tests/run.py -p test_intent.py -k Rewrite` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Rewrite 0s) / OK [ran] [tree dae7b9b59e59] (2026-10-09T19:33:07Z)
- (audit intent) `self review of fmchange, the AST allowlist and the rename; real runs: a Haiku spec and a converted rename on a copy of Foreman's library` → the first slice asked for an intent compiler turning a one-liner into a red spec and a structural rewrite with a cheap converter for leftovers; both shipped and were proven on real runs (7 red assertions; 38 sites, 2 residuals converted to 0) [tree dae7b9b59e59] (2026-10-09T19:33:07Z)
- (audit adversary) `self review of fmchange, the AST allowlist and the rename; real runs: a Haiku spec and a converted rename on a copy of Foreman's library` → model output is written as code only after an AST allowlist (comparisons over calls into the named module and literals, no underscores, imports, eval, open), and runs once in the project like any test; the converter's lines are applied only when they drop every spelling of the old name, and only to lines the rule flagged; children are tool-less and budget-checked [tree dae7b9b59e59] (2026-10-09T19:33:07Z)
- (audit edge) `self review of fmchange, the AST allowlist and the rename; real runs: a Haiku spec and a converted rename on a copy of Foreman's library` → a file that doesn't tokenize is left untouched rather than half-renamed; non-code files only report residuals; an identifier with no residual skips the child; a spec with no safe assertion refuses; dry run is the default [tree dae7b9b59e59] (2026-10-09T19:33:07Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T19:29:11Z focused
- 2026-10-09T19:33:07Z done
- 2026-10-09T19:33:08Z committed a81dfda (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0712 [FEATURE M, done, 4 steps] Frontier 12 — Self-improvement flywheel — lesson: Self-improvement needs an objective before candidates: measure the burden per version…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar finished tasks took 3–4 steps
## Lessons
- Generated code is safe to run only through an allowlist of AST shapes; a rename rule should own the code sites and hand the strings and other spellings to review or a cheap converter, never sed them
## Files touched
- plugin/tests/test_intent.py
- plugin/lib/fmchange.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
