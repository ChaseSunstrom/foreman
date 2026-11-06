---
id: T-2185
type: FEATURE
tier: L
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-30T16:35:39Z
updated: 2026-10-31T06:57:25Z
base: c824fc3883d84816d32eaf24e4cc36fa3a5fad97
base_tree: e721d00cc39495aa1584ea72342d099f463cfc6f
plan0_at: 2026-10-31T06:50:25Z
plan0_scope: []
verified: strong
---
# Initiative detection ladder (steer 2026-10-30 #4, capability #1): fm find stays the free…
## Raw request
> FEATURE!: Initiative detection ladder (steer 2026-10-30 #4, capability #1): fm find stays the free first pass; detection beyond it is never hand-written per language. In order: (1) the repo's own and the ecosystem's standard tools, discovered from manifests and stack cards (compilers, type checkers, linters, test and coverage runners, OSV-Scanner, gitleaks, Semgrep rule packs), missing tools queued through #5 (fm plugins find / fm ask); (2) tree-sitter for structural, language-agnostic rules; (3) dynamic signals: tests, coverage, fuzz and property tests, mutation testing, running the app, git bug-fix hotspots; (4) AI review aimed at those hotspots for semantic bugs, every finding proven by fm find prove (T-2122) or dropped; (5) every bug found by another path that no finder caught is a blind spot that becomes a new rule, tool or check. Exam recall reported per language and per bug type, with child-authored scenarios in languages and kinds fm find wasn't written for
## Interpretation
Steer 2026-10-30 #4, a standing rule for capability #1. fm find stays the free, code-free first pass; recall beyond it comes from a ladder, never from hand-written per-language finders: (1) the repo's own and the ecosystem's standard tools, discovered from manifests and stack cards (fm lib), installed ones run, missing ones queued through #5 (fm plugins find, then fm ask ID plugin); (2) tree-sitter structural rules, one query set across languages; (3) dynamic signals: the test runner, coverage, fuzz and property tests, mutation testing, running the app, and git bug-fix hotspots; (4) AI review aimed only at those hotspots, each finding proven by fm find prove (T-2122) or dropped; (5) any bug another path found that no finder caught is recorded as a blind spot and becomes a rule, tool or check task. The exam reports recall per language and per bug type, and the child author writes scenarios in languages and kinds fm find wasn't written for. Constraint carried from fm find: it never runs a scanned repo's code. Rungs 1 and 3 run the repo's own code (builds, tests, the app), so they run only where T-2124's consent holds (the user's own commits) or inside an exam sandbox, never on a clone by default.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find --ladder runs the stack's standard tools found from manifests and stack cards (no per-language Python), each as a named finder with learned precision, and queues a missing tool through #5 — verify with `python3 plugin/tests/run.py test_find`
- [x] rungs that run the repo's code (tools that build or test, coverage, mutation, the app) run only in a tree fmprove.trusted() accepts (the user's own fm prove --yes-run, kept per tree; Foreman's home) or in an exam sandbox, never on an author-email claim (T-2202); fm find itself still never runs repo code — verify with `python3 plugin/tests/run.py test_find test_scout`
- [x] tree-sitter rules run from .scm data when the binding is present, and are queued as a #5 plugin when not — verify with `python3 plugin/tests/run.py test_find`
- [x] git bug-fix hotspots rank files; a hotspot review files only findings fm find prove (T-2122) shows red, the rest dropped — verify with `python3 plugin/tests/run.py test_find`
- [x] a closed FIX whose lines no finder flagged becomes a blind-spot record, and fm find blindspots files a rule, tool or check task for each — verify with `python3 plugin/tests/run.py test_find`
- [x] exam grade lines and fm exam scorecard report recall per language and per bug type, with child-authored held-out scenarios in languages and kinds fm find wasn't written for — verify with `python3 plugin/tests/run.py test_exam test_genesis`
## Non-goals
## Approach (options → choice → why)
Revised after fm second plan (verdict revise) and the T-2233 re-grade (s0-001 finders: bug 0/18, all other kinds full; by language the misses are those bugs). Options: (1) one batch across all rungs (rejected: too big, boundaries untestable); (2) rung by rung, ordered by measured blind spot; (3) tools first because they're free (rejected: tools don't catch the logic bugs the exam shows missed). Choice 2: (a) bug rung: T-2199 extended to bug, a cheap child reviews the top-ranked files and each finding needs a failing test that fm prove runs on a trusted or exam-sandbox copy (stub control kept); (b) git bug-fix hotspots rank files for (a), reading only git log with fsmonitor and hooks off; (c) tool rung: argv only from Foreman's own registry (stack cards), repo manifests only select entries and never supply argv, run only in a trusted tree or exam sandbox; (d) tree-sitter rules from .scm data behind an optional import; (e) blind-spot records: store what each finder flagged at capture time, map a closed FIX's lines to it, file at most one rule task a day. Recall per language and kind landed (T-2233); the scorecard reading it is part of (a)'s exam check.
## Risks and rollback
Rungs that run tools execute repo-influenced code: the tool rung runs only in a tree the user trusted (fmprove.trusted, T-2202) with argv from Foreman's registry (T-2239); tree-sitter parses only (T-2240). A noisy rung is muted by per-finder precision. Each rung is opt-in behind --ladder, so rollback is not passing it; each landed as its own task (T-2233, T-2238, T-2239, T-2240, T-2241, T-2242).
## Execution prompt
## Steps
1. [x] red tests for every rung, the consent gate and the per-language/per-kind recall
2. [x] tool rung: registry from stack cards and manifests, SARIF/text normalizing, #5 queueing
3. [x] tree-sitter rung behind an optional import, .scm rules as data
4. [x] hotspots from git log; hotspot review behind fm find prove (after T-2122)
5. [x] blind-spot records and fm find blindspots
6. [x] exam: per-language/per-kind recall, wider CHILD_KINDS and languages; the two steer 4 rules get their checks
7. [x] docs: MASTER, README, CHANGELOG, site; zero-token arms on the new scenarios (Haiku smoke only at the end-of-run exam)
## Resume here
## Docs impact
site/pages.py, MASTER.md, README.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 129 tests in 13.9s (25 classes, 16 at a time; slowest: FindBlindSpots 13s, FindRenders 8s, FindProve 8s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:50:57Z)
- (step 2) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 129 tests in 13.2s (25 classes, 16 at a time; slowest: FindBlindSpots 13s, FindProve 8s, FindRenders 8s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:51:11Z)
- (step 3) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 129 tests in 10.4s (25 classes, 16 at a time; slowest: FindBlindSpots 10s, FindProve 7s, FindRenders 7s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:51:21Z)
- (step 4) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 129 tests in 12.7s (25 classes, 16 at a time; slowest: FindBlindSpots 12s, FindRenders 7s, FindProve 7s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:51:34Z)
- (step 5) `python3 plugin/tests/run.py test_find test_prove` → exit 0 · Ran 129 tests in 10.0s (25 classes, 16 at a time; slowest: FindBlindSpots 10s, FindCli 6s, FindProve 6s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:51:45Z)
- (step 6) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 193 tests in 78.2s (28 classes, 16 at a time; slowest: ExamAuthors 78s, ExamGen 59s, GenesisRead 25s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:53:03Z)
- (step 7) `python3 plugin/tests/run.py test_site_build test_docs` → exit 0 · Ran 97 tests in 10.2s (30 classes, 16 at a time; slowest: Fences 10s, Landing 3s, TaskLifecycle 3s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:53:14Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 10.4s (23 classes, 16 at a time; slowest: FindBlindSpots 10s, FindProve 7s, FindCli 7s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (ac 2) `python3 plugin/tests/run.py test_find test_scout` → exit 0 · Ran 163 tests in 15.9s (29 classes, 16 at a time; slowest: Scout 16s, FindBlindSpots 8s, FindCli 6s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (ac 3) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 10.4s (23 classes, 16 at a time; slowest: FindBlindSpots 10s, FindProve 7s, FindCli 7s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (ac 4) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 10.4s (23 classes, 16 at a time; slowest: FindBlindSpots 10s, FindProve 7s, FindCli 7s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (ac 5) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 125 tests in 10.4s (23 classes, 16 at a time; slowest: FindBlindSpots 10s, FindProve 7s, FindCli 7s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (ac 6) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 193 tests in 68.6s (28 classes, 16 at a time; slowest: ExamAuthors 68s, ExamGen 53s, GenesisRead 18s) / OK [ran] [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (audit intent) `umbrella close: every rung landed as its own reviewed task with red-to-green proof; this close adds the site's Initiative bullet; evidence re-run per step (test_find, test_prove, test_exam, test_genesis, test_site_build, test_docs)` → steer 4's ladder is in fm find: stack tools (trusted only), tree-sitter rules (optional binding), git hotspots, blind spots to rules, per-language and per-kind recall on the exam [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (audit adversary) `umbrella close: every rung landed as its own reviewed task with red-to-green proof; this close adds the site's Initiative bullet; evidence re-run per step (test_find, test_prove, test_exam, test_genesis, test_site_build, test_docs)` → the only rung that runs code is the tool rung, gated on the user's own trust by realpath and argv from Foreman's registry (T-2239's adversary review); tree-sitter parses only [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (audit edge) `umbrella close: every rung landed as its own reviewed task with red-to-green proof; this close adds the site's Initiative bullet; evidence re-run per step (test_find, test_prove, test_exam, test_genesis, test_site_build, test_docs)` → every rung is opt-in behind --ladder; a missing tool or binding files one capability miss [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (audit operator) `umbrella close: every rung landed as its own reviewed task with red-to-green proof; this close adds the site's Initiative bullet; evidence re-run per step (test_find, test_prove, test_exam, test_genesis, test_site_build, test_docs)` → a noisy rung is muted by per-finder precision; recall per language shows where finders are blind [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
- (audit maintainer) `umbrella close: every rung landed as its own reviewed task with red-to-green proof; this close adds the site's Initiative bullet; evidence re-run per step (test_find, test_prove, test_exam, test_genesis, test_site_build, test_docs)` → rules and the tool registry are data; each rung has its own test class [tree 6db54b1165f6] (2026-10-31T06:56:46Z)
## Log
- 2026-10-30T16:35:39Z created
- 2026-10-30T16:42:34Z set depends_on=['T-2122']
- 2026-10-30T16:42:43Z set depends_on=[]
- 2026-10-30T16:42:48Z planned: it has criteria and steps
- 2026-10-30T18:59:37Z step 7 text: docs: MASTER, README, CHANGELOG, site; Haiku smoke on the new scenarios → docs: MASTER, README, CHANGELOG, site; zero-token arms on the new scenarios (Haiku smoke only at the end-of-run exam)
- 2026-10-30T18:59:37Z set approved=True
- 2026-10-30T18:59:37Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T19:33:38Z criterion 2 text: rungs that run the repo's code (tools that build or test, coverage, mutation, the app) run only with T-2124's consent or in an exam sandbox; fm find itself still never runs repo code → rungs that run the repo's code (tools that build or test, coverage, mutation, the app) run only in a tree fmprove.trusted() accepts (the user's own fm prove --yes-run, kept per tree; Foreman's home) or in an exam sandbox, never on an author-email claim (T-2202); fm find itself still never runs repo code
- 2026-10-30T19:33:38Z replan: rung consent is T-2202's per-tree trust, not T-2124's author-email check (anyone can write the user's email into a commit)
- 2026-10-30T23:56:54Z T-2233 landed recall per language and kind. Re-graded s0-001 finders (zero tokens): by kind bug 0/18, dep 9/9, docs 18/18, flaky 9/9, slow 18/18, untested 18/18, vuln 18/18; by language c 11/15, js 19/24, python 13/15, ruby 14/16, rust 20/23, ts 13/15. The blind spot is the bug kind (no bug finder), not a language: the ladder's next rung should target bugs (tree-sitter rules, git bug-fix hotspots).
- 2026-10-31T00:06:08Z fm second plan: revise (scope too big for one plan; consent and command boundaries untestable as written; T-2122 dependency; blind-spot records need a stored flag map). Grounding: s0-001 re-grade shows the blind spot is bugs (0/18), every other kind full; the planted bug is a logic error (a paging guard), which only a dynamic signal or a review proven by a failing test can catch. Revised: T-2185 becomes the umbrella; rungs split into their own tasks, the bug rung first (T-2199 extended to bug: a child reviews the ranked files and each finding needs a failing test fm prove runs on a trusted or exam-sandbox copy).
- 2026-10-31T06:50:24Z focused
- 2026-10-31T06:55:10Z scope: site/pages.py (initiative page bullet); the rungs landed as T-2233, T-2238, T-2239, T-2240, T-2241, T-2242
- 2026-10-31T06:57:23Z done
- 2026-10-31T06:57:25Z committed ad6fc381 (1 file)
## Follow-ups captured
## Build vs reuse
Reuses: fmfind's finder registry and learned per-finder precision (each tool becomes a named finder), fm lib stack cards' verify sections and the manifests fm find already reads for tool discovery, fm plugins find / fm ask ID plugin (#5) for missing tools, T-2124's consent gate for rungs that run repo code, fmmap's git fix/revert hotspot counts (fmmap.py:671) for the hotspot rank, T-2122's fm find prove for proving hotspot-review findings, and fmexam's grade lines for recall. New: a tool runner that normalizes SARIF or text output into fm find's finding shape (stdlib json/re, shell=False, timeouts), .scm rule files as data behind an optional tree-sitter import, and blind-spot records. No per-language Python finders.
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Scope is far too large for one plan. Six deliverables (tool registry, tree-sitter, hotspots/dynamic signals, AI review, blind-spot loop, exam changes) are labeled "a batch of M tasks" but there is one step list, and the task is typed L. Step 1 writes red tests for everything up front, which k…
- HIGH: The consent boundary is unverifiable as written. Criterion 2 says "verify with test_find test_scout", but those tests can't prove that no repo code ran. Tools like compilers, linters with plugins, and Semgrep or test runners all execute repo-controlled code (build scripts, conftest, eslint co…
- HIGH: Discovering and invoking tools "from stack cards' verify sections and manifests" means turning free-form text and repo-controlled manifests (package.json scripts, Makefile targets) into commands. Even with shell=False, the repo chooses the argv. — Use a fixed allow-list of tool names with fix…
- MEDIUM: Criterion 4 and rung 4 depend on T-2122 (fm find prove), which is only noted as a dependency, and step 4 says "after T-2122" with no fallback. The tests would fail or have to be stubbed if it isn't landed. — State T-2122's status. If it isn't done, block rung 4 explicitly, or test against a…
- MEDIUM: Exam criterion is weakly checkable. "Child-authored held-out scenarios in languages and kinds fm find wasn't written for" can't be proven by test_exam/test_genesis if the scenarios are authored by a child at exam time (non-deterministic, costs tokens). Per-language recall also has tiny deno…
- MEDIUM: Blind-spot detection ("a closed FIX whose lines no finder flagged") needs a stored record of what finders flagged at the time, plus line mapping across later edits. Neither exists in the plan, and auto-filing a task per blind spot could flood the queue. — Specify the persisted finder-output…
Verdict: revise — the direction is sound, but the plan needs to be split by rung and the consent and command-injection boundaries must be made testable before any code is written.
## Dissent
- [ ] HIGH: Scope is far too large for one plan. Six deliverables (tool registry, tree-sitter, hotspots/dynamic signals, AI review, blind-spot loop, exam changes) are labeled "a batch of M tasks" but there is one step list, and the task is typed L. Step 1 writes red tests for everything up front, which k…
- [ ] HIGH: The consent boundary is unverifiable as written. Criterion 2 says "verify with test_find test_scout", but those tests can't prove that no repo code ran. Tools like compilers, linters with plugins, and Semgrep or test runners all execute repo-controlled code (build scripts, conftest, eslint co…
- [ ] HIGH: Discovering and invoking tools "from stack cards' verify sections and manifests" means turning free-form text and repo-controlled manifests (package.json scripts, Makefile targets) into commands. Even with shell=False, the repo chooses the argv. — Use a fixed allow-list of tool names with fix…
- [ ] MEDIUM: Criterion 4 and rung 4 depend on T-2122 (fm find prove), which is only noted as a dependency, and step 4 says "after T-2122" with no fallback. The tests would fail or have to be stubbed if it isn't landed. — State T-2122's status. If it isn't done, block rung 4 explicitly, or test against a…
- [ ] MEDIUM: Exam criterion is weakly checkable. "Child-authored held-out scenarios in languages and kinds fm find wasn't written for" can't be proven by test_exam/test_genesis if the scenarios are authored by a child at exam time (non-deterministic, costs tokens). Per-language recall also has tiny deno…
- [ ] MEDIUM: Blind-spot detection ("a closed FIX whose lines no finder flagged") needs a stored record of what finders flagged at the time, plus line mapping across later edits. Neither exists in the plan, and auto-filing a task per blind spot could flood the queue. — Specify the persisted finder-output…
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-2239 [FEATURE M, done, 3 steps] fm find --ladder tool rung: run stack tools whose argv comes only from Foreman's… — lesson: An rlimit on a tool is inherited by everyth…
- the similar finished task took 3 steps
## Regression test
none at the umbrella: each rung landed with its own red-to-green proof (T-2233, T-2238, T-2239, T-2240, T-2241, T-2242); this close adds the site bullet
## Lessons
- An L umbrella closes cleanly when each rung is its own M task with its own review; the umbrella then only adds the surfaces
## Files touched
- site/pages.py
