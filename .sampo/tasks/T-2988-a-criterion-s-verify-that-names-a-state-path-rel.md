---
id: T-2988
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T15:15:05Z
updated: 2026-11-04T15:33:19Z
base: 2b6c237a3d332aef55de66319465a61751ee94c6
base_tree: 70a53290b4931005ff407592d1d41f132444a097
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T15:31:40Z
plan0_scope: []
verified: strong
---
# A criterion's verify that names a state/ path relative to the repo always fails in a…
## Raw request
> A criterion's verify that names a state/ path relative to the repo always fails in a lane (state is git-ignored, the lane has none); lane merge should run such a verify from the main checkout, or task ac add should warn when a verify names a relative state/ path (T-2974 and T-2975 both refused on it)
## Interpretation
Reading 1 (chosen): lint_verify warns when a verify names Sampo's state by a repo-relative path (state/projects/...): state is git-ignored, so in a builder lane the file is never there and lane merge reads the criterion red (T-2974 and T-2975 both refused on it); the warning says to use the absolute path. Reading 2 (ruled out): have lane merge rewrite the path; a silent rewrite hides a wrong criterion.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo task ac add with a verify naming state/projects/... relative warns that a lane has no state and to give the absolute path; an absolute path or tests/state stays quiet — verify with `python3 plugin/tests/run.py test_board_posture`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then the lint rule
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_board_posture` → ✗ exit 1 · Ran 10 tests in 8.8s (2 classes, 16 at a time; slowest: BoardPostureBench 8s, BoardPosture 1s) / FAILED (1 classes: test_board_posture.BoardPosture) [ran] [tree aef559b22b61] [world 2f1906870a] (2026-11-04T15:31:56Z)
- (step 1) `python3 plugin/tests/run.py test_board_posture` → exit 0 · Ran 10 tests in 9.1s (2 classes, 16 at a time; slowest: BoardPostureBench 9s, BoardPosture 1s) / OK [ran] [tree 8ea2dc2d1e2e] [world 2f1906870a] (2026-11-04T15:32:21Z)
- `python3 plugin/tests/run.py test_board_posture` → ✗ exit 1 · Ran 10 tests in 10.6s (2 classes, 16 at a time; slowest: BoardPostureBench 9s, BoardPosture 1s) / FAILED (1 classes: test_board_posture.BoardPosture) (start tree + this task's tests) [ran] [tree cca669af9579] [world 2f1906870a] (2026-11-04T15:32:49Z)
- `python3 plugin/tests/run.py test_board_posture` → exit 0 · Ran 10 tests in 9.0s (2 classes, 16 at a time; slowest: BoardPostureBench 9s, BoardPosture 1s) / OK [ran] [tree cca669af9579] [world 2f1906870a] (2026-11-04T15:32:49Z)
- (ac 1) `python3 plugin/tests/run.py test_board_posture` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T15:32:49Z [ran] [tree cca669af9579] [world 2f1906870a] (2026-11-04T15:32:50Z)
- (audit edge) `diff read: one lint rule in core.lint_verify and its test; prove red on the start tree, green now` → an absolute path to state, ~/.claude/foreman/state and a repo's own tests/state stay quiet (tested); the rule only warns, never refuses [tree cca669af9579] (2026-11-04T15:32:50Z)
- (audit self) `diff read: one lint rule in core.lint_verify and its test; prove red on the start tree, green now` → no findings [tree cca669af9579] (2026-11-04T15:32:50Z)
## Log
- 2026-11-04T15:15:05Z created
- 2026-11-04T15:31:39Z planned: it has criteria and steps
- 2026-11-04T15:31:39Z set approved=True
- 2026-11-04T15:31:40Z focused
- 2026-11-04T15:31:40Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T15:33:17Z done
- 2026-11-04T15:33:19Z committed 5b436d78 (3 files)
## Follow-ups captured
## Regression test
test_board_posture: lint_verify flags 'test -s state/projects/x/research/models/lake-manifest.json' and passes the same with an absolute path and 'pytest tests/state'.
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
## Lessons
- When the same refusal hits twice from one cause, lint the cause where it's written (ac add), not where it bites (lane merge)
## Plan gaps
- failed first: step 1 failing test, then the lint rule
## Files touched
- plugin/tests/test_board_posture.py
- plugin/lib/sampo/core.py
- CHANGELOG.md
