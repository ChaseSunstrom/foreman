---
id: T-2121
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:47Z
updated: 2026-10-30T09:19:47Z
base: b4f9e0e21b8873eef93e663c258d4a92bcf6312d
base_tree: 37674d932d1b15bca6979d256c9fc86f026bb2b6
plan0_at: 2026-10-30T08:35:44Z
plan0_scope: []
verified: strong
---
# fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (Mission 3 brief 2)
## Raw request
> fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (Mission 3 brief 2)
## Interpretation
A new verb fm find [PATH] [--json] runs deterministic, language-agnostic finders over a tree (py, js, ts, rb, rs, c): untested public functions, SQL built from a bare parameter, membership tests on a list inside a loop, unseeded randomness in tests, imports no stdlib or manifest has, docs drift (fmdocs.scan) and committed secrets (fmsecrets). Precision first: zero findings on every clean exam render. The exam's finders arm runs it.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find reports 0 on every clean exam render and finds each planted kind it covers — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
Proving findings (T-2122), ranking (T-2125), the failing-gates finder (needs the run machinery of T-2122), logic bugs (no deterministic finder can tell an off-by-one from intent).
## Approach (options → choice → why)
A. Chosen: one module of small regex/line finders per kind, each returning {finder, kind, file, symbol, line, says}; tuned to report nothing on the clean renders of all six languages, measured by the exam renders in test_find. B. Per-language AST (python ast, tree-sitter): exact but one language each and tree-sitter is a dependency; Python ast could later back the py finders. C. External analysers (semgrep, bandit, clippy): needs installs, that's capability #5 (Mission 6). Gates finder (rerun a failing suite) deferred to the prove gate T-2122, which already runs tests; listed here as a non-goal.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fmfind.py finders + fm find verb
2. [x] exam finders arm runs fm find
## Resume here
<!-- auto -->
- 2026-10-30T09:10:30Z steps 2/2 done
- git: foreman/build; 9 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmdocs.py, plugin/lib/fmexam.py, plugin/lib/fmtidy.py, plugin/lib/fmfind.py, plugin/tests/test_find.py
- touched since last checkpoint: MASTER.md, README.md, CHANGELOG.md, plugin/lib/fmdocs.py, plugin/lib/fmfind.py, plugin/lib/fmtidy.py, plugin/tests/test_find.py
- failures met: json.decoder.jsondecodeerror: expecting value: line 0 column 0 (char 0)
## Docs impact
MASTER.md, README.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find.FindRenders test_find.FindPrecision` → exit 0 · Ran 2 tests in 1.6s (2 classes, 16 at a time; slowest: FindRenders 1s, FindPrecision 0s) / OK [ran] [tree 4730cfbe5ab0] (2026-10-30T08:51:28Z)
- (step 2) `python3 plugin/tests/run.py test_find test_exam` → exit 0 · Ran 31 tests in 19.9s (18 classes, 16 at a time; slowest: ExamGen 20s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 6ee1ac488c12] (2026-10-30T08:52:36Z)
- (step 2) `python3 plugin/tests/run.py test_find test_exam` → exit 0 · Ran 33 tests in 20.0s (18 classes, 16 at a time; slowest: ExamGen 20s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 472062af818f] (2026-10-30T09:03:09Z)
- (step 2) `python3 plugin/tests/run.py test_find test_exam test_docs test_tidy` → exit 0 · Ran 151 tests in 19.0s (52 classes, 16 at a time; slowest: ExamGen 19s, DeferredTriage 15s, StalePlans 14s) / OK [ran] [tree 459e10711816] (2026-10-30T09:12:31Z)
- (step 2) `python3 plugin/tests/run.py test_find test_exam test_docs test_tidy` → exit 0 · Ran 152 tests in 23.1s (52 classes, 16 at a time; slowest: ExamGen 22s, DeferredTriage 19s, StalePlans 18s) / OK [ran] [tree b07c737989cc] (2026-10-30T09:14:27Z)
- (audit adversary) `hostile tree: symlinks to /dev/zero and outside creds, FIFO, surrogate names, fsmonitor config, 350 KB SQL line, star-run C line` → all fixed test-first; FindHostile passes with and without git; no read outside the tree [tree b07c737989cc] (2026-10-30T09:14:27Z)
- (audit edge) `empty dir, git-ignored subdir, malformed manifests (toml str, json list, latin-1), generated file with a key, crash path` → walk fallback, 'No files' message, manifests skipped, secret found, crash exits 2 [tree b07c737989cc] (2026-10-30T09:14:27Z)
- (audit intent) `every clean exam render in 6 langs x 11 kinds; exam s7-004 finders arm` → 0 findings on every clean render; 20/24 found, 0 false alarms; misses are uncovered kinds [tree b07c737989cc] (2026-10-30T09:14:27Z)
- (audit maintainer) `one module, finders as plain functions, ceilings named in MASTER and ponytail comments` → substring dep match marked as a ceiling; stale_commands hardened in place [tree b07c737989cc] (2026-10-30T09:14:28Z)
- (audit operator) `self-scan of Foreman (1893 files)` → 42 candidates in 3 s; exit 1/0/2 documented [tree b07c737989cc] (2026-10-30T09:14:28Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 18 tests in 5.8s (11 classes, 16 at a time; slowest: FindCli 6s, FindRenders 2s, DryRun 1s) / OK [ran] [tree 392acaf554ae] (2026-10-30T09:14:51Z)
- (audit edge) `fm-reviewer pass (saved as research T-2121-review); 9 findings verified and fixed test-first; FindHostile + crash-exit tests; self-scan and exam s7-004 re-run` → empty, ignored, malformed manifests, generated secrets, crash → all handled, tested [tree 392acaf554ae] (2026-10-30T09:14:51Z)
- (audit adversary) `fm-reviewer pass (saved as research T-2121-review); 9 findings verified and fixed test-first; FindHostile + crash-exit tests; self-scan and exam s7-004 re-run` → links, FIFOs, odd names, fsmonitor, regex blowups → regular files only, git config off, line cap [tree 392acaf554ae] (2026-10-30T09:14:51Z)
- (audit edge) `fm-reviewer pass (saved as research T-2121-review); 9 findings verified and fixed test-first; FindHostile + crash-exit tests; self-scan and exam s7-004 re-run` → empty, ignored, malformed manifests, generated secrets, crash → all handled, tested [tree c92ba2d07975] (2026-10-30T09:16:17Z)
- (audit adversary) `fm-reviewer pass (saved as research T-2121-review); 9 findings verified and fixed test-first; FindHostile + crash-exit tests; self-scan and exam s7-004 re-run` → links, FIFOs, odd names, fsmonitor, regex blowups → regular files only, git config off, line cap [tree c92ba2d07975] (2026-10-30T09:16:17Z)
- (audit intent) `every clean exam render in 6 langs x 11 kinds; exam s7-004 finders arm; help slot moved to 457` → 0 findings on every clean render; 20/24 found, 0 false alarms [tree c92ba2d07975] (2026-10-30T09:16:53Z)
- (audit maintainer) `one module, finders as plain functions, ceilings in MASTER and ponytail comments; own help position` → HelpRegistrations green [tree c92ba2d07975] (2026-10-30T09:16:53Z)
- (audit operator) `self-scan of Foreman (1893 files); exit 0/1/2 documented` → 42 candidates in 3 s [tree c92ba2d07975] (2026-10-30T09:16:53Z)
- (audit edge) `fm-reviewer pass (saved as research T-2121-review); 9 findings verified and fixed test-first; FindHostile + crash-exit tests; self-scan and exam s7-004 re-run` → empty, ignored, malformed manifests, generated secrets, crash → all handled, tested [tree c92ba2d07975] (2026-10-30T09:16:54Z)
- (audit adversary) `fm-reviewer pass (saved as research T-2121-review); 9 findings verified and fixed test-first; FindHostile + crash-exit tests; self-scan and exam s7-004 re-run` → links, FIFOs, odd names, fsmonitor, regex blowups → regular files only, git config off, line cap [tree c92ba2d07975] (2026-10-30T09:16:54Z)
## Log
- 2026-10-30T08:06:47Z created
- 2026-10-30T08:35:44Z focused
- 2026-10-30T09:02:49Z hypothesis: a module with any reached public function is tested (black-box via its entry point); module rule now fires only when none is reached. Confirmed: test_find+test_exam 33 OK, real-repo shape case passes.
- 2026-10-30T09:04:23Z exam s7-004 (22 scenarios, all langs): finders 20/24 found, 0 false alarms; empty 0/24; oracle 24/24 fixed. Misses are kinds no finder covers (bug, vague, ambiguous, missing-tool).
- 2026-10-30T09:17:22Z done
- 2026-10-30T09:17:24Z committed 6a4e7c18 (9 files)
- 2026-10-30T09:17:31Z guard authorization added: publish
- 2026-10-30T09:19:47Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2120-review: Verdict:** changes needed. One MEDIUM finding: the exam-defect proof can be satisfied without any exam defect. [stale: plugin/lib/fmexam.py, plug…
- T-2120 [FIX M, done, 3 steps] Exam contract repair: README run command, an edge contract every clean app follows, a proven unkeyed finding counts as an exam defect (Miss…
- T-2079 [FEATURE L, done, 6 steps] fm exam: generated multi-language exam with hidden keys, holdout third, finders and claude arms, scores to exam.jsonl — lesson: A claud…
- decision 2026-10-30: [revisit: when plugin/lib/fmexam.py changes @ecf3a72d8dff] Exam baseline: the finders arm (fmdocs.scan + fmsecrets, no session) scores 0/108 on s0-0…
## Why not caught
the first tests used only clean exam renders and Foreman's own tree; none was hostile
## Lessons
- A tool that reads untrusted trees needs a hostile-tree test from the start: lstat + S_ISREG, byte-safe git output, neutralized git config, capped line length.
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmfind.py
- plugin/lib/fmcli.py
- plugin/lib/fmexam.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmdocs.py
- plugin/lib/fmtidy.py
