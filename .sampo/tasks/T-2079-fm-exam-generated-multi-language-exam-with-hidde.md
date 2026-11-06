---
id: T-2079
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T01:33:22Z
updated: 2026-10-30T04:29:33Z
base: aafc340dfdbf473ce86ee7b93b8e6b25cb24ba11
base_tree: 986026a4dba1f5756f202728a601604f4aa2e53d
plan0_at: 2026-10-30T01:33:49Z
plan0_scope: []
verified: ok
---
# fm exam: generated multi-language exam with hidden keys, holdout third, finders and claude arms, scores to exam.jsonl
## Raw request
> fm exam: generated multi-language exam with hidden keys, holdout third, finders and claude arms, scores to exam.jsonl
## Interpretation
Gen-0 §4 and gen-1/mission-exam.md: a seeded generator of throwaway repos in six languages (python, js, ts, rust, ruby, c) with one planted defect per scenario (bug, vuln, untested, slow, docs, flaky, dep) or request-shape scenarios (vague, ambiguous, missing-tool, none), hidden keys and checks outside the repo, a held-out third, a grader and two agent arms (Foreman's free finders, a headless claude session), one exam.jsonl line per graded run.
## Assumptions (confidence)
Toolchains: python3, node 26 (type stripping for .ts), cargo, ruby without minitest, gcc (confidence 5, checked). A grading test per defect is expressible as one function call and expected value per language (4). Matching findings to the key by file basename + symbol is precise enough in tiny generated repos (3; false alarms reported so drift shows).
## Acceptance criteria
- [x] generated repos pass their visible tests and every hidden check fails on the planted repo and passes on the clean one, in python, js, ts, rust, ruby and c — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam`
- [x] an oracle agent scores 100% found with no false alarms and an empty agent 0%; holdout ids never appear in --split train — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam`
## Non-goals
Java and Go (no compiler here). Network-dependent dep checks. Running the claude arm over the whole set in this task: one sample run proves the arm; full paid runs belong to critiques.
## Approach (options → choice → why)
A (chosen): one app API (total, page, dedupe, user_query) described once as cases, rendered per language from small per-language renderers; each defect is a variant of one function or file; seeded choice of language, defect and names; key + hidden checks stored beside the repo, not in it. B: hand-written fixtures in bench/ (memorisable; the holdout leaks). C: LLM-written repos and keys (unreliable keys, costly). D: plant into Foreman's own code (fmbench planted-bug: one language; kept). Why A: keys true by construction, reproducible by seed, six languages from one spec, free to re-run.
## Risks and rollback
New module and verb only; nothing existing changes behaviour. Generated repos live under the project state's exam/ dir (throwaway). Rollback: revert the commit. Cost risk only in the claude arm: it is budgeted per scenario and off by default.
## Execution prompt
## Steps
1. [x] red tests for gen, grade and split
2. [x] generator: one app spec rendered in six languages, defect variants, key and hidden checks outside the repo
3. [x] grader driven only by key.json (commands + checks per scenario); oracle, empty, finders arms; exam.jsonl line per run
4. [x] verb, genesis status shows the last score, docs
5. [x] baseline: finders arm over a full generation recorded in exam.jsonl
6. [x] outside author and head-to-head (standing rule 5): fm exam gen --author child (tool-less child writes scenarios from the format only; kept only if they pass fm exam check); foreman and plain session arms on the same held-out scenarios
## Resume here
<!-- auto -->
- 2026-10-30T04:26:02Z steps 6/6 done
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, site/genesis/genesis.js, site/genesis/index.html, plugin/lib/fmexam.py, plugin/tests/test_exam.py
- touched since last checkpoint: plugin/tests/test_exam.py, plugin/lib/fmexam.py, site/genesis/genesis.js, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md fmexam line, CHANGELOG fm exam entry, site/genesis exam section and table
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam` → red as expected (exit 1) · Ran 11 tests in 0.8s (8 classes, 16 at a time; slowest: ExamGen 1s, Oracle 0s, ExamJs 0s) / FAILED (7 classes) [ran] [tree 967661f7ef8f] (2026-10-30T01:50:15Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_genesis` → exit 0 · Ran 25 tests in 17.2s (11 classes, 16 at a time; slowest: ExamGen 17s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 3ec5fb09087f] (2026-10-30T04:00:55Z)
- (step 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam` → exit 0 · Ran 12 tests in 17.6s (8 classes, 16 at a time; slowest: ExamGen 17s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 2258692a69e9] (2026-10-30T04:03:32Z)
- (step 4) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam test_genesis 2>&1 | tail -4` → exit 0 · Ran 26 tests in 18.1s (11 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 12s, ExamC 12s) / OK [ran] [tree 3d4f752053a6] (2026-10-30T04:06:01Z)
- (step 4) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam test_genesis test_site` → exit 0 · Ran 51 tests in 19.4s (20 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 13s, ExamC 12s) / OK [ran] [tree 3d4f752053a6] (2026-10-30T04:06:24Z)
- (step 5) `fm exam check s0-001` → exit 0 · s0-001: 99 scenarios checked, all sound [ran] [tree 3d4f752053a6] (2026-10-30T04:09:09Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam 2>&1 | tail -25` → exit 0 · Ran 15 tests in 17.7s (9 classes, 16 at a time; slowest: ExamGen 17s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 504f4413874e] (2026-10-30T04:15:16Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam 2>&1 | tail -25` → exit 0 · Ran 15 tests in 17.7s (9 classes, 16 at a time; slowest: ExamGen 17s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 504f4413874e] (2026-10-30T04:15:16Z)
- (step 6) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam 2>&1 | tail -25` → exit 0 · Ran 15 tests in 17.7s (9 classes, 16 at a time; slowest: ExamGen 17s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 504f4413874e] (2026-10-30T04:15:16Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran)|AssertionError" | head` → exit 0 · Ran 15 tests in 18.9s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 12s) / OK [ran] [tree 9779f091ab98] (2026-10-30T04:17:51Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran)|AssertionError" | head` → exit 0 · Ran 15 tests in 18.9s (9 classes, 16 at a time; slowest: ExamGen 19s, ExamRust 12s, ExamC 12s) / OK [ran] [tree 9779f091ab98] (2026-10-30T04:17:51Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran)|Error:" | head -12` → exit 0 · Ran 17 tests in 18.2s (9 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 43b467c6ca95] (2026-10-30T04:23:11Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam 2>&1 | grep -E "^(FAIL|ERROR|OK|Ran)|Error:" | head -12` → exit 0 · Ran 17 tests in 18.2s (9 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 43b467c6ca95] (2026-10-30T04:23:11Z)
- (step 6) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam` → exit 0 · Ran 17 tests in 18.0s (9 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 11s, ExamC 11s) / OK [ran] [tree 5dbdf1d14568] (2026-10-30T04:23:55Z)
- (step 6) `real sample on s0-001 held-out bug (claude sonnet), after moving sessions to a temp dir outside p.dir; child author on s7-003` → foreman 1/1 found 1/1 fixed 1/1 test-first $0.34; plain 1/1 found 1/1 fixed 1/1 test-first $0.11; child: 1 kept, 1 dropped by fm exam check [tree 5dbdf1d14568] (2026-10-30T04:23:55Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam` → exit 0 · Ran 17 tests in 17.4s (9 classes, 16 at a time; slowest: ExamGen 17s, ExamRust 11s, ExamC 11s) / OK [ran] [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_exam` → exit 0 · Ran 17 tests in 17.4s (9 classes, 16 at a time; slowest: ExamGen 17s, ExamRust 11s, ExamC 11s) / OK [ran] [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer, design) over the full diff; each finding checked against the code, fixed test-first or answered; real paid sample run on held-out scenarios` → sessions already ran in a temp dir outside p.dir (test asserts cwd); session samples now interleave kinds; the row records the split and kinds it covered [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer, design) over the full diff; each finding checked against the code, fixed test-first or answered; real paid sample run on held-out scenarios` → model-written code runs with fmbench.CREDENTIALS stripped from its env; the key sits outside the session's temp tree; grade refuses unknown agents; RecursionError in _reply is caught (test) [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer, design) over the full diff; each finding checked against the code, fixed test-first or answered; real paid sample run on held-out scenarios` → an errored session is counted under errors and shown as N errored in fm exam and on the site (test); _authored drops a plant on OSError and SubprocessError too [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer, design) over the full diff; each finding checked against the code, fixed test-first or answered; real paid sample run on held-out scenarios` → session spend goes through fmbudget.check and record under exam-arm, so fm cost and fm budget see it (test) [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer, design) over the full diff; each finding checked against the code, fixed test-first or answered; real paid sample run on held-out scenarios` → tests for _reply, errored sessions, bad agent names; fmsecrets._tree use kept (same package); duplicate rows on regrade are by design (test expects them) [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
- (audit design) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer, design) over the full diff; each finding checked against the code, fixed test-first or answered; real paid sample run on held-out scenarios` → exam table escapes every field; cost and errors guarded by typeof [tree 5dbdf1d14568] (2026-10-30T04:25:38Z)
## Log
- 2026-10-30T01:33:22Z created
- 2026-10-30T01:33:48Z set approved=True
- 2026-10-30T01:33:48Z focused
- 2026-10-30T01:44:49Z steer: tower files (gap map, gen-1/*) live only in fm genesis storage, never the scratchpad; each capability exam >= 9 scenarios, held-out >= 3 (exam gen guarantees quotas per kind); mission 8 overload: if #3 or #11 trigger table lack a full pass, gen-1 critique hands them to gen 2 as own Missions
- 2026-10-30T01:47:23Z steer: standing for the whole run — (1) no idea killed for ambition: failed spike gets ≥2 different approaches, then not-yet.md ledger with blocker, retried each generation; only proven harm or exact duplicate removes, reason recorded; (2) coverage.md grid: areas × surfaces × stages, every cell grounded idea / existing feature path / recorded n/a; empty cells first each generation; run not done while a cell is empty or a not-yet item is untried this generation
- 2026-10-30T01:59:11Z steer: standing — weakness-finding by outside signals only (fm outcomes 30-day survival, fm second cold review, head-to-head vs plain Claude Code on held-out scenarios); exam scenarios authored by a tool-less child that never sees Foreman's code or Missions; self-strong/outside-weak → top gap next Seed. Design change: grader driven only by key.json (commands + checks stored per scenario), so child-authored scenarios plug in; templates stay as the free reference author (author=self), child = --author child; results record author; plain arm beside the foreman arm
- 2026-10-30T01:59:56Z step 3 text: grader, finders and claude arms, exam.jsonl line per run → grader driven only by key.json (commands + checks per scenario); oracle, empty, finders arms; exam.jsonl line per run
- 2026-10-30T02:06:36Z paused: focus moved to T-2080
- 2026-10-30T02:57:29Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-30T02:57:29Z focused
- 2026-10-30T03:14:00Z paused: focus moved to T-2087
- 2026-10-30T03:50:46Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-30T03:50:46Z focused
- 2026-10-30T04:11:49Z hypothesis: child plant via render(plant=) + _check_one gate + session arms over fmbench._session turn the 3 ExamAuthors tests green; rules out needing per-language test harness changes
- 2026-10-30T04:15:21Z result: hypothesis held: test_exam 15/15 green (3 ExamAuthors incl.); rules out a per-language harness change for child plants (the 'child' test key carries them)
- 2026-10-30T04:22:22Z hypothesis: review fixes so far (credential-free _run env, broader _authored except, RecursionError in _reply, kinds interleaved, budget check) keep the existing exam tests green and turn the reply test green; the errors/kinds/spend/grade-validation tests stay red until the grade edits land
- 2026-10-30T04:26:05Z done
- 2026-10-30T04:26:06Z committed c2a66214 (8 files)
- 2026-10-30T04:27:18Z guard authorization added: publish
- 2026-10-30T04:29:33Z publish grant used by fm ship
## Follow-ups captured
## Build vs reuse
Reuses fmbench's headless session helpers (_session, _seed, _env, _result_json) for the claude arm, fmbench.split_of's hash idea for the holdout (own modulus 3), fmeco's adopt finders for the finders arm, fmgenesis.home for exam.jsonl, c.write_atomic/c.lock. Nothing existing generates multi-language repos with keys (gap map #13).
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-30: T-2079 exam design: one app API rendered in six languages with defect variants, keys outside the repo, hash holdout one in three; finders arm free, …
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- research T-2078-review: Verdict:** approve with nits. The three acceptance criteria are met, and `put` refuses gen-0 and every path outside the tower shape. I found one …
- T-1215 [FEATURE M, done, 3 steps] fm code bench: grade any model or worker as a Foreman worker on seeded tasks — lesson: A bench must grade what the harness can check it…
## Lessons
- A claude session that must edit can't run under Foreman's state dir: the guard blocks writes there, so the arm scored 0 fixed; run sessions in a temp copy and copy the tree back
## Plan gaps
- added late: outside author and head-to-head (standing rule 5): fm exam gen --author child (tool-less child writes scenarios from th…
## Files touched
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
- plugin/tests/test_exam.py
- site/genesis/genesis.css
- plugin/lib/fmexam.py
- plugin/lib/fmcli.py
- site/genesis/genesis.js
- site/genesis/index.html
- MASTER.md
- CHANGELOG.md
