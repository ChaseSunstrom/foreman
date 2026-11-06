---
id: T-2192
type: FIX
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: discovered
created: 2026-10-30T16:52:59Z
updated: 2026-10-30T17:37:16Z
base: 46e8661e91c83f1988457252d6e4d726dbabc9c1
base_tree: 056f656c5c33065f201855c91adc712b40cb1e2d
plan0_at: 2026-10-30T17:00:42Z
plan0_scope: []
verified: strong
---
# The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18…
## Raw request
> FIX!: the foreman arm still trails the free finders on s31-006 with session-start leads: 10/18 found vs 16/18 (Haiku smoke). Read the 9 answers against the leads each session was shown: which leads were dropped, which found defects weren't in the leads, whether 8 leads per scenario is the cap that cost them; close the gap so the session finds at least what the finders find (standing intent #2: a built tool a session doesn't use is a top gap)
## Interpretation
The foreman arm's 0/9 on the three Rust scenarios is a lost answer, not a detection miss: in none-rust-65ff1a the session fixed the SQL splice and the README's wrong name (its work tree shows both), but its final reply had no findings object, so the grade counted nothing. Exam answers keep no reply text, so a miss like this can't be read back. The arms must be graded on what the session found, with the reply shape never the deciding factor, and the remaining gap to the finders (if any) read per scenario against the leads.
## Assumptions (confidence)
## Acceptance criteria
- [x] a session whose reply has no findings object gets one resumed turn for the JSON, both turns' cost counted, the answer keeps the reply tail and whether it re-asked — verify with `python3 plugin/tests/run.py test_exam`
- [x] Haiku smoke foreman arm on s31-006 held out: every Rust scenario answers with a findings object; found and the per-scenario leads-vs-findings diff recorded — verify with `fm exam`
- [x] every Stop-hook hold in claude -p mode tells the session to end with its whole answer (the caller sees only the last message); interactive holds don't — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
Options: (a) when a session's reply carries no findings object, resume that session for one turn asking only for the JSON, and keep the reply's tail in the answer (chosen: general, costs a turn only when the answer is lost, same rule for every arm); (b) infer findings from the diff the session left (rejected: the grader would author the answer); (c) push the JSON ask into a system prompt or the Stop hook for the foreman arm only (rejected: arms must get the same ask); (d) parse findings out of prose (rejected: fragile). Then re-run the Haiku smoke foreman arm on s31-006's 9 held-out scenarios and diff each answer against the leads its session was shown.
## Risks and rollback
Sessions now persist (keep) so the resume can find them: a transcript per exam session in Claude Code's projects folder, cleaned on its schedule. Rollback: revert the commit.
## Execution prompt
## Steps
1. [x] red test: a no-JSON reply gets one resumed turn; the answer keeps said and reasked
2. [x] implement the resume turn in the session arm
3. [x] Haiku smoke re-run on s31-006 held out (foreman arm), diff answers against leads
4. [x] fm check, docs, audit, finish
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/rules/foreman.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors.test_a_reply_with_no_findings_object_gets_one_more_turn_for_it` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: ExamAuthors 1s) / FAILED (1 classes) [ran] [tree 8e99bc13423a] (2026-10-30T17:01:03Z)
- (ac 1) `python3 plugin/tests/run.py test_exam 2>&1 | grep -B 3 -A 25 "^FAIL:\|^ERROR:" | head -n 50` → ✗ exit 1 · Ran 27 tests in 25.8s (10 classes, 16 at a time; slowest: ExamGen 25s, ExamAuthors 18s, ExamRust 13s) / FAILED (1 classes) [ran] [tree 544c049de01f] (2026-10-30T17:02:20Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_bench` → exit 0 · Ran 77 tests in 55.5s (28 classes, 16 at a time; slowest: Bench 55s, Judged 39s, Duel 26s) / OK [ran] [tree f831124976b4] (2026-10-30T17:03:51Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.NoTaskGate.test_a_bench_replay_never_asks_for_a_push_notification test_hooks.NoTaskGate.test_a_failing_suite_leaves_the_task_open_and_says_so_once` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: NoTaskGate 1s) / FAILED (1 classes) [ran] [tree ad194e9c50b1] (2026-10-30T17:15:51Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_hooks test_core test_docs` → exit 0 · Ran 410 tests in 43.0s (80 classes, 16 at a time; slowest: Stop 43s, NoTaskGate 34s, PreToolUse 28s) / OK [ran] [tree 3406c52b283a] (2026-10-30T17:18:30Z)
- (step 3) `fm exam` → exit 0 · foreman s31-006: 10/18 found, 3 false alarms, 17/18 fixed, 5/6 test-first, 2/3 ranked, held out 10/18 found, $0.58 / foreman s31-006: 15/18 found, 4 false alarms, 17/18 fixed, 6/6 test-first, 2/3 rank [ran] [tree 3406c52b283a] (2026-10-30T17:18:30Z)
- (step 2) `python3 plugin/tests/run.py test_exam.ExamAuthors` → ✗ exit 1 · Ran 9 tests in 6.1s (1 classes, 16 at a time; slowest: ExamAuthors 6s) / FAILED (1 classes) [ran] [tree a354940ae2f3] (2026-10-30T17:21:34Z)
- (audit intent) `foreman:fm-reviewer` → 15/18 vs finders 16/18 stated, not called closed; LEADS cap cost nothing (≤3 leads a scenario), logged [tree 25ebc1f4ee88] (2026-10-30T17:22:44Z)
- (audit edge) `foreman:fm-reviewer` → re-ask trigger now the shared parser (_answer): broken JSON re-asks; errored turn not re-asked, tested [tree 25ebc1f4ee88] (2026-10-30T17:22:44Z)
- (audit operator) `foreman:fm-reviewer` → 2x budget ceiling and kept transcripts documented; rules hint cut for the cap, cue kept on line 14 [tree 25ebc1f4ee88] (2026-10-30T17:22:44Z)
- (audit adversary) `foreman:fm-reviewer` → ok: constants only; said redacted, capped, never fed to a model; lead rows JSON-quoted [tree 25ebc1f4ee88] (2026-10-30T17:22:44Z)
- (audit maintainer) `foreman:fm-reviewer` → print-mode check reuses _headless(); re-asked count on the exam line [tree 25ebc1f4ee88] (2026-10-30T17:22:44Z)
- (step 2) `python3 plugin/tests/run.py test_exam test_hooks.NoTaskGate test_hooks.Stop test_hooks.SessionStart` → exit 0 · Ran 123 tests in 38.4s (13 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 29s, ExamGen 22s) / OK [ran] [tree 25ebc1f4ee88] (2026-10-30T17:23:29Z)
- (step 4) `fm check` → ✗ exit 1 · AssertionError: 18 != 17 : Evidence, gates and verification: the map table's count / ✓ fm replay → exit 0 · skipped: nothing under plugin/lib/fmguard.py changed since its pass at 15:52 UTC (0.0 s) [ran] [tree 25ebc1f4ee88] (2026-10-30T17:27:11Z)
- (step 4) `fm check` → exit 0 · ✓ python3 plugin/tests/run.py → exit 0 · Ran 4454 tests in 171.7s (1038 classes, 16 at a time; slowest: Worker 80s, Stop 46s, Fakes 42s) / OK (171.8 s) / ✓ fm replay → exit 0 · skipped: nothing under [ran] [tree cf4fa6c76654] (2026-10-30T17:31:03Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 27 tests in 22.0s (10 classes, 16 at a time; slowest: ExamGen 22s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree cf4fa6c76654] (2026-10-30T17:32:26Z)
- (ac 2) `fm exam` → exit 0 · foreman s31-006: 10/18 found, 3 false alarms, 17/18 fixed, 5/6 test-first, 2/3 ranked, held out 10/18 found, $0.58 / foreman s31-006: 15/18 found, 4 false alarms, 17/18 fixed, 6/6 test-first, 2/3 rank [ran] [tree cf4fa6c76654] (2026-10-30T17:32:26Z)
- (ac 3) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 213 tests in 32.3s (28 classes, 16 at a time; slowest: Stop 32s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree cf4fa6c76654] (2026-10-30T17:32:26Z)
- (step 1) `python3 plugin/tests/run.py test_exam.ExamAuthors test_hooks.NoTaskGate.test_a_failing_suite_leaves_the_task_open_and_says_so_once test_hooks.SessionStart` → exit 0 · Ran 28 tests in 11.8s (3 classes, 16 at a time; slowest: SessionStart 12s, ExamAuthors 6s, NoTaskGate 1s) / OK [ran] [tree cf4fa6c76654] (2026-10-30T17:32:26Z)
- (audit intent) `one foreman:fm-reviewer pass over five lenses; 2 findings fixed test-first (parsed re-ask trigger, _headless reuse), the rest answered in the brief` → 15/18 vs finders 16/18 stated as such; the 3 misses were untested leads shown and dropped, now worded per kind [tree cf4fa6c76654] (2026-10-30T17:32:26Z)
- (audit edge) `one foreman:fm-reviewer pass over five lenses; 2 findings fixed test-first (parsed re-ask trigger, _headless reuse), the rest answered in the brief` → broken JSON re-asks; an errored first turn isn't re-asked; interactive holds get no print-mode line [tree cf4fa6c76654] (2026-10-30T17:32:26Z)
- (audit adversary) `one foreman:fm-reviewer pass over five lenses; 2 findings fixed test-first (parsed re-ask trigger, _headless reuse), the rest answered in the brief` → new strings are constants; said is redacted, capped and never fed to a model [tree cf4fa6c76654] (2026-10-30T17:32:26Z)
## Log
- 2026-10-30T16:52:59Z created
- 2026-10-30T16:56:21Z grounding: in the smoke run every Rust scenario (none-rust-65ff1a, rank-rust-981449, clean-rust-6bacb3) answered 0 findings with done=false and no error, while the Python and JS ones answered 2-3 each; start there (a timeout or cargo cost eating the turn, or a reply with no JSON object), then the leads-vs-findings diff per scenario
- 2026-10-30T17:00:41Z planned: it has criteria and steps
- 2026-10-30T17:00:42Z focused
- 2026-10-30T17:18:30Z smoke (Haiku, foreman arm, s31-006 held out, after the resumed turn): 15/18 found (was 10/18; finders 16/18), 4 false alarms, 17/18 fixed, $0.38; all 3 Rust scenarios answered (4 reasked: none-rust, rank-rust, clean-rust, none-python-37ffb1). clean-rust's first reply said its JSON was 'at the end of my previous reply': a Stop-hook hold made one more message and claude -p returns only the last, the root cause; fixed in the Stop hook for every print-mode user. Leads vs findings: every lead shown was a keyed defect; all 3 misses were untested leads the session was shown and dropped (none-rust bound, rank-rust clamp; none-python-37ffb1 named its new test class AppTests instead of limit_to), so the leads note, fm next and the rules now say how an untested lead closes (a test that calls it) and to report each under its own symbol. The false alarms: clean-rust's overflow and CJK-width notes (unkeyed edge observations), rank-js's duplicate lookup_sql rows. No third Haiku smoke this generation (steer 1: at most one per generation; the steer-3 rerun and this one are spent): the wording change is checked by unit tests and rides into the end-of-run exam.
- 2026-10-30T17:22:25Z review: the rules lost '(long: fm outline it or Read with an offset)' to fit the 6400-char rules cap; line 14's targeted reads (grep, fm outline PATH, line ranges) keep the cue. Exam sessions now persist (keep) so the re-ask can resume; transcripts age out on Claude Code's cleanup and are what showed T-2194's cost gap. LEADS stays 8: no s31-006 scenario had more than 3 leads, so the cap cost nothing.
- 2026-10-30T17:23:30Z scope: plugin/rules/foreman.md and the 5 synced eval prompts (leads wording), fmcore fm next line, MASTER/CHANGELOG docs
- 2026-10-30T17:33:23Z done
- 2026-10-30T17:33:25Z committed 0073b9b0 (13 files)
- 2026-10-30T17:34:49Z guard authorization added: publish
- 2026-10-30T17:37:16Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2184 [FEATURE M, done, 5 steps] Foreman sessions use fm find by default (steer 2026-10-30 #3): the exam shows a Foreman… — lesson: a capability the session never hears…
- research draft-mission-exam-gen1: Task: T-2079 (fm exam). Site: T-2080 (this tower on the site).
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: [revisited: testing cadence] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pending T-2158] Testing ca…
- similar finished tasks took 4–5 steps
## Why not caught
exam answers kept no reply text and the stubbed claude always ended on JSON; the nojson stub and the kept tail now catch it
## Lessons
- A grade that reads one reply object scores the reply's shape: claude -p returns only the last message, so a Stop-hook hold after the answer zeroed sessions that had fixed every planted bug. Read the answer across the session and keep the raw tail so a zero can be read back; and price a suspected cost gap at the model's own rates before calling it one (T-2194 was a false alarm).
## Plan gaps
- failed first: step 1 red test: a no-JSON reply gets one resumed turn; the answer keeps said and reasked
- failed first: step 4 fm check, docs, audit, finish
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- MASTER.md
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/lib/fmcore.py
- plugin/rules/foreman.md
- CHANGELOG.md
