---
id: T-2572
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:21Z
updated: 2026-11-02T09:29:33Z
trigger: genesis-review
trigger_key: fd634cb4c9da5481
base: a60940fdfd474f57e53f94b97efc70f4e833a27e
base_tree: 6c06d2c01180ca7bd520b578adb5b60713522a5d
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T09:15:20Z
plan0_scope: []
verified: strong
---
# fm ship re-picks onto a moved main without a retest only when every file main gained is one CI itself ignores (the workflow's paths-ignore); any other move refuses so the next ship retests
## Raw request
> FIX: cross-cutting review gen-2 #3 (what got worse): fm ship now re-picks onto a moved main and pushes up to 3 tries with no retest; the pushed commit has never had the suite run on it, and ad98d29a already shipped the same re-pick a second way. [ec276a78]
> genesis-review 2:3
## Interpretation
Reading 1 (chosen): the risk is a combined tree nobody tested; narrow the no-retest re-pick to moves CI itself never tests (tower data). Reading 2: the review's 'second way' claim means T-2555 duplicated T-2511. Rejected after reading fmrelease.py:474-496: T-2555 only loops T-2511's re-pick for a push race; one mechanism.
## Assumptions (confidence)
## Acceptance criteria
- [x] a main that moved only in files matching the repo's .github/workflows paths-ignore globs is re-picked onto and pushed without a retest; a move touching any other file, even one the shipped commits don't touch, refuses with 'run fm ship again'; a repo with no paths-ignore refuses every move — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
1) Read the repo's .github/workflows/*.yml paths-ignore globs and allow the no-retest re-pick only when every file main gained matches one; otherwise refuse (the next fm ship tests the new main). Likely outcome: tower publishes still re-pick; a code move refuses. Fails if: a workflow's paths-ignore is wider than data (then CI also never tests those files, so nothing is lost). 2) use what exists: rerun the suite on the re-picked tree before the push. Likely outcome: always safe. Fails if: a 5-minute retest lets main move again (tower publishes come every few minutes), so ship rarely lands. 3) do less: keep the disjoint-files rule and rely on the post-push CI watch. Fails if: a broken main lands before CI says so. 4) Refuse every move (revert T-2511). Fails if: each tower publish fails the ship, the reason T-2511 exists. Choice 1 (85%): CI's own ignore list is the exact set a retest would never cover.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_ship (data-only move re-picks; code move in an untouched file refuses; no workflow refuses)
2. [x] _ci_ignored(wt) reads paths-ignore globs; the re-pick condition requires every new file to match
3. [x] CHANGELOG/MASTER
## Resume here
## Docs impact
CHANGELOG (Unreleased). MASTER's fmrelease entry is unchanged in shape; the re-pick rule is in the CHANGELOG and the code comment.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 35 tests in 28.5s (1 classes, 16 at a time; slowest: Ship 28s) / FAILED (1 classes: test_ship.Ship) [ran] [tree 6e93e16aabfa] [world 2f1906870a] (2026-11-02T09:16:02Z)
- (step 2) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 35 tests in 38.0s (1 classes, 16 at a time; slowest: Ship 38s) / OK [ran] [tree 773b6e126ee1] [world 2f1906870a] (2026-11-02T09:17:50Z)
- (step 3) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 35 tests in 40.1s (1 classes, 16 at a time; slowest: Ship 40s) / OK [ran] [tree 773b6e126ee1] [world 2f1906870a] (2026-11-02T09:18:30Z)
- `python3 plugin/tests/run.py test_ship` → ✗ exit 1 · Ran 35 tests in 29.4s (1 classes, 16 at a time; slowest: Ship 28s) / FAILED (1 classes: test_ship.Ship) (start tree + this task's tests) [ran] [tree 27ba8fb9df49] [world 2f1906870a] (2026-11-02T09:28:09Z)
- `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 35 tests in 28.5s (1 classes, 16 at a time; slowest: Ship 28s) / OK [ran] [tree 27ba8fb9df49] [world 2f1906870a] (2026-11-02T09:28:09Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 35 tests in 28.5s (1 classes, 16 at a time; slowest: Ship 28s) / OK [ran] [tree 27ba8fb9df49] [world 2f1906870a] (2026-11-02T09:28:47Z)
- (audit intent) `self-review: the post-test re-pick now refuses unless every file main gained matches a paths-ignore glob read from the moved main's own workflows; globs follow GitHub's ** and * rules; the shared-file refusal and the T-2555 push-race retry are unchanged; empty-commit moves still re-pick (no files gained); 40 real tower publishes all fall inside the real workflow's globs` → a data-only move re-picks (T-2511 test with ci_ignores); a code move in an untouched file refuses with 'files CI tests' and keeps the grant; no workflow refuses every file move (tests) [tree 27ba8fb9df49] (2026-11-02T09:28:47Z)
- (audit adversary) `self-review: the post-test re-pick now refuses unless every file main gained matches a paths-ignore glob read from the moved main's own workflows; globs follow GitHub's ** and * rules; the shared-file refusal and the T-2555 push-race retry are unchanged; empty-commit moves still re-pick (no files gained); 40 real tower publishes all fall inside the real workflow's globs` → the globs come from the moved main's own committed workflow, so a pusher could widen paths-ignore to sneak an untested file past ship; but then CI also never tests that file, and the workflow change itself is a moved file that must match a glob to pass, so widening needs a commit to main that already passed review [tree 27ba8fb9df49] (2026-11-02T09:28:47Z)
- (audit edge) `self-review: the post-test re-pick now refuses unless every file main gained matches a paths-ignore glob read from the moved main's own workflows; globs follow GitHub's ** and * rules; the shared-file refusal and the T-2555 push-race retry are unchanged; empty-commit moves still re-pick (no files gained); 40 real tower publishes all fall inside the real workflow's globs` → quoted globs and trailing comments are stripped; a missing .github/workflows gives no globs; ls-tree or show failures give none (refuse, the safe side) [tree 27ba8fb9df49] (2026-11-02T09:28:47Z)
## Log
- 2026-11-02T08:23:21Z created
- 2026-11-02T08:26:53Z planned from capture
- 2026-11-02T09:15:20Z set approved=True
- 2026-11-02T09:15:20Z focused
- 2026-11-02T09:15:20Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T09:29:30Z done
- 2026-11-02T09:29:33Z committed e51d82b0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2555 [FEATURE S, done, 2 steps] fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries — lesson: a…
- T-2511 [FIX M, done, 2 steps] fm ship re-picks onto a main that moved only in files the shipped commits never touch — lesson: A ship race with an automated publisher is …
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Why not caught
T-2511's test only moved a data file, so 'disjoint files' and 'files CI never tests' looked the same; no test moved a code file the ship didn't touch
## Lessons
- A shortcut justified by one kind of input (tower data) must be keyed to that kind, not to a broader property (disjoint files) that happened to cover it
## Plan gaps
- failed first: step 1 red tests in test_ship (data-only move re-picks; code move in an untouched file refuses; no workflo…
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
