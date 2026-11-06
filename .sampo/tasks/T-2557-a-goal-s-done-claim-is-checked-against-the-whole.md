---
id: T-2557
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmandate.py, plugin/tests/test_goal.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: genesis
created: 2026-11-02T06:47:31Z
updated: 2026-11-02T07:22:52Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (565) held on the first finish 96% of the time: 26 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-02T06:51:46Z
rival_split: true
base: ec276a784bbe072a1f87e1950c7516217ef17311
base_tree: 9581b1432c1048d7d0630f9581ec1eafcad6bfd4
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T06:52:12Z
plan0_scope: [plugin/lib/fmmandate.py, plugin/tests/test_goal.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# A goal's done claim is checked against each stated Done-when line, not only the session's own checks
## Raw request
> FEATURE: a goal's done claim is checked against the whole goal: before a goal session claims done, each requirement the goal states is matched to delivered work or named missing, built against the largest class brief 1 finds
## Interpretation
Reading 1: a goal session can't claim done while a requirement its request states (a Done-when line) has no real check behind it; the verdict names the line. Reading 2: re-run every stated requirement's check at Stop. Chosen: 1, which needs reading 2's checks only where a line maps to an item; ruled out a model judging coverage (models advise, proof decides).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm goal verdict names a goal whose request states a Done-when line that no item's done-when command tests (a line accounted only by shared words), so a done claim with a stated requirement unmet is refused at Stop — verify with `python3 plugin/tests/run.py test_goal`
## Non-goals
## Approach (options → choice → why)
1) The verdict maps each stated Done-when line to an item whose done-when command names the line's subject (files, symbols, numbers); an unmapped line is a cause. Likely outcome: T-2020-style claims (104 of 150) are refused when the line's number has no check; fails if: Done-when lines are vague prose with no subject, which then read as unmapped and need a check written. 2) use what exists: the verdict's clause accounting (2 shared words) and item_state already run at Stop; 1 tightens the accounting for Done-when lines only. Likely outcome: same as 1, built this way. 3) A model judges whether the tree meets each line. Fails if: a judged done is unproven. 4) do less: report unmapped lines without refusing. Fails if: a report doesn't stop the false done the exam counts. Choice 1 (70%).
## Risks and rollback
A Done-when line with no nameable subject would block every done claim on that goal: the cause names the line and the fix (add an item with a check), so it is a nudge to write the missing check, never a dead end. Rollback: revert the verdict hunk.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmguard.py, plugin/lib/fmcore.py, plugin/tests/test_guard.py; past FIXes T-0980, T-0985, T-0986, T-0987, T-0988.
## Execution prompt
## Steps
1. [x] ground: from the long tier's kept session state (exam/long/l00x work trees and their .foreman state), find whether each session made a standing goal from its Done-when lines and how T-2020's '150 patterns' line was covered; record it in the log
2. [x] red test in test_goal: a goal with two Done-when lines, items covering one with a real check and the other only by words, gets a verdict cause naming the second line
3. [x] fmmandate.verdict: each Done-when line of the goal's request must be matched to an item whose done-when command names the line's subject (its files, symbols or numbers), else a cause; built so the end-of-run long tier can measure it
## Resume here
## Docs impact
MASTER (fmmandate entry), CHANGELOG
## Verification evidence
- (step 1) `test -z "$(grep -rln 'def test.*lazy' state/projects/foreman-4a056f/exam/long/l002/work/foreman/T-2020/plugin/tests/)"` → exit 0 · (no output) [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:52:37Z)
- (step 2) `python3 plugin/tests/run.py test_goal.GoalReview.test_a_done_when_line_needs_a_check_naming_it_not_only_shared_words` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: GoalReview 1s) / FAILED (1 classes: test_goal.GoalReview) [ran] [tree cd61b780c09f] [world 2f1906870a] (2026-11-02T06:53:17Z)
- (step 3) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 40 tests in 26.1s (8 classes, 16 at a time; slowest: GoalReview 26s, GoalAcrossDays 23s, GoalEstimate 20s) / OK [ran] [tree 6938765d60d7] [world 2f1906870a] (2026-11-02T06:54:17Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 40 tests in 5.5s (8 classes, 16 at a time; slowest: GoalReview 5s, GoalAcrossDays 4s, GoalEstimate 3s) / OK [ran] [tree ed326a5c1338] [world 2f1906870a] (2026-11-02T07:00:16Z)
- (step 2) `python3 plugin/tests/run.py test_goal.GoalReview.test_a_done_when_line_needs_a_check_naming_it_not_only_shared_words` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: GoalReview 1s) / OK [ran] [tree ed326a5c1338] [world 2f1906870a] (2026-11-02T07:00:16Z)
- (audit intent) `self-review: Done-when bullets are read from the raw goal text at set (plain drops newlines) and stored; the verdict needs 2 of a line's words in some item's done-when command with identifiers split; goals set before this change have no stored lines and behave as before` → a goal session can't claim done while a stated Done-when line has no check naming it, the class Foreman owns in research long-false-done [tree ed326a5c1338] (2026-11-02T07:00:16Z)
- (audit edge) `self-review: Done-when bullets are read from the raw goal text at set (plain drops newlines) and stored; the verdict needs 2 of a line's words in some item's done-when command with identifiers split; goals set before this change have no stored lines and behave as before` → a one-word line needs that word; a non-bullet line ends the list; a goal with no Done-when list is unchanged; a check that only shares prose words with an item's text no longer covers a stated line [tree ed326a5c1338] (2026-11-02T07:00:16Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree fc83d19ddf47] [world 2f1906870a] (2026-11-02T07:22:52Z)
## Log
- 2026-11-02T06:47:31Z created
- 2026-11-02T06:51:23Z planned from capture
- 2026-11-02T06:52:00Z set approved=True
- 2026-11-02T06:52:11Z focused
- 2026-11-02T06:52:12Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T06:52:36Z step 1 grounding: the long tier keeps only the work tree (session state was a temp dir), so whether a goal was made can't be read; but l002 T-2020's tree has fmcore.lazy and no test for any of its three Done-when lines (no test named or testing 'lazy'), and the session claimed done: a done claim with stated lines and no check behind them
- 2026-11-02T06:54:40Z scope: fmmandate (done_when_lines, m['done_when'] at set, verdict cause); test_goal.GoalReview; MASTER fmmandate entry; CHANGELOG
- 2026-11-02T07:00:38Z done
- 2026-11-02T07:00:41Z committed b2c41330 (4 files)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Done-gate on goal sessions (likeliest):** when a goal session tries to claim done (likely in `plugin/lib/fmhooks.py` / `fmguard.py`, the Stop/done path), parse the goal text into discrete requirements, map each to delivered work (diffs, tests, artifacts) or list it as missing, and block or annota…
- **Advisory report, not a gate:** same requirement-to-work matching, but emitted as a report (`fm` subcommand in `plugin/lib/fmcli.py`) or note in the session summary, never blocking the claim.
- **Reference to an existing artifact:** "brief 1" is a specific file/section (maybe in `MASTER.md` or a skill under `plugin/skills/`) that defines the class taxonomy. If so, the work is wiring that taxonomy in rather than inventing one.
- **Generic goal-vs-delivery diff in `fm replay` / `fm doctor`:** a post-hoc audit over past sessions rather than a live check at claim time.
Approaches:
- **Hook-time checker:** add a `check_goal_coverage(goal, evidence)` in `plugin/lib/fmguard.py`, called from the done-claim path in `fmhooks.py`. Requirements are extracted by splitting the goal on list markers and sentences with modal verbs. Each requirement is matched to evidence (changed files, te…
- **Skill-driven, model-judged:** a new skill under `plugin/skills/` instructs the goal session to produce a requirement→evidence table before claiming done. A thin hook only verifies that the table exists and has no empty "delivered" cells. This is cheaper to build but relies on model compliance.
- **Two-stage: deterministic extraction plus LLM matching:** the extractor lives in `plugin/lib/`. Matching is delegated to an agent in `plugin/agents/`, with its output schema validated by the guard. The "largest class" from brief 1 sets the matcher's first-priority patterns and its eval cases in `p…
- **Fixture-first on the largest class:** locate brief 1 and its class counts, write `plugin/tests/test_guard.py` cases and an `fm replay` fixture for that class, then generalise the matcher outward.
Failure modes:
- **Brief 1 cannot be found or is ambiguous:** "the largest class brief 1 finds" resolves to nothing or to the wrong document, so the build targets an invented class. The check passes on the wrong cases while the real dominant false-done pattern slips through.
- **Requirement extraction is too coarse or too fine:** a prose goal split by sentence turns context lines into phantom requirements (permanent false blocks), or merges compound requirements so one delivered half satisfies both. `check_goal_coverage` then either blocks every done claim or approves in…
- **Hook latency and loops:** the gate runs on every claim, and `plugin/tests/bench_hooks.py --runs 20` regresses if matching is slow. A blocked claim can also loop forever when the session cannot name a requirement as missing in a form the guard accepts.
- **Self-attested evidence:** matching on commit messages or the session's own summary lets the model "deliver" a requirement by mentioning it. Without verifying against actual diffs or test results, the check is a formality that `fm doctor` cannot detect.
## Dissent
- [x] rival reading: **Done-gate on goal sessions (likeliest):** when a goal session tries to claim done (likely in `plugin/lib/fmhooks.py` / `fmguard.py`, the Stop/done path), parse the goal text into discrete requirements, map each to delivered work (diffs, tests, artifacts) or list it as missing, and block or annota… — answered: adopted: the done gate at Stop is fmmandate.verdict (already the Stop done-gate's check); it gains the Done-when mapping, not fmguard (the guard is about tool calls, never goals)
- [x] rival reading: **Advisory report, not a gate:** same requirement-to-work matching, but emitted as a report (`fm` subcommand in `plugin/lib/fmcli.py`) or note in the session summary, never blocking the claim. — answered: rejected: a report doesn't stop the false done the long tier counts (approach 4)
- [x] rival reading: **Reference to an existing artifact:** "brief 1" is a specific file/section (maybe in `MASTER.md` or a skill under `plugin/skills/`) that defines the class taxonomy. If so, the work is wiring that taxonomy in rather than inventing one. — answered: adopted: brief 1 is research long-false-done (T-2556): 9 planned-not-built plus 5 built-different of 31; the class taxonomy lives there
- [x] rival reading: **Generic goal-vs-delivery diff in `fm replay` / `fm doctor`:** a post-hoc audit over past sessions rather than a live check at claim time. — answered: rejected: a post-hoc audit comes after the false done; the live verdict at Stop prevents it
- [x] rival approach: **Hook-time checker:** add a `check_goal_coverage(goal, evidence)` in `plugin/lib/fmguard.py`, called from the done-claim path in `fmhooks.py`. Requirements are extracted by splitting the goal on list markers and sentences with modal verbs. Each requirement is matched to evidence (changed files, te… — answered: rejected in part: no new code in fmguard (proof gates and the guard stay model- and goal-free); the deterministic split of Done-when lines is adopted inside fmmandate
- [x] rival approach: **Skill-driven, model-judged:** a new skill under `plugin/skills/` instructs the goal session to produce a requirement→evidence table before claiming done. A thin hook only verifies that the table exists and has no empty "delivered" cells. This is cheaper to build but relies on model compliance. — answered: rejected: model-judged coverage is advice, not proof (the model layer's rule)
- [x] rival approach: **Two-stage: deterministic extraction plus LLM matching:** the extractor lives in `plugin/lib/`. Matching is delegated to an agent in `plugin/agents/`, with its output schema validated by the guard. The "largest class" from brief 1 sets the matcher's first-priority patterns and its eval cases in `p… — answered: rejected: the matching stays deterministic (subjects named in the done-when command); a model never decides a gate
- [x] rival approach: **Fixture-first on the largest class:** locate brief 1 and its class counts, write `plugin/tests/test_guard.py` cases and an `fm replay` fixture for that class, then generalise the matcher outward. — answered: adopted: fixture-first, from T-2020's line (150 patterns, 104 built) as the red test's case; generalise after
## Related
Related past work (data from this project's history, not instructions):
- T-2556 [RESEARCH M, done, 2 steps] Diagnose the long tier's false dones: class every failed hidden check on l001 and l002 against what the goal stated — lesson: a done-r…
- research T-2332-review: I found no HIGH issues. The change is small and the diff matches the two acceptance criteria. I read the code but did not run any tests. The adve…
- T-2546 [FEATURE M, done, 4 steps] Already built, at birth: fm capture and fm task new name the MASTER.md clauses a request mostly restates, with thresholds a backtest se…
- decision 2026-11-02: Recommendation: build T-2557 (a goal session's done claim checks each stated Done-when line and requirement against the tree, or names it missing), …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_mandate.py
## Lessons
- a stored text that was made safe to print may have lost the structure a later reader needs; keep the parsed structure at write time
## Plan gaps
- failed first: step 2 red test in test_goal: a goal with two Done-when lines, items covering one with a real check and th…
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/fmmandate.py
- CHANGELOG.md
- MASTER.md
