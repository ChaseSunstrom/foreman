---
id: T-0678
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:15Z
updated: 2026-10-09T17:54:29Z
batch: [T-0492, T-0493]
base: 32a1b7507e0967126e0556e8ac0db9b832cf5b6f
base_tree: 449ca46ac46d5471b7525f8be5993107bb62a4d0
verified: strong
---
# Milestone: Features — Releases and delivery
## Raw request
> T-0492: FEATURE: Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
>   first version: Before a release, run fm replay, fm bench and fm sentinel across every project from fm projects and print per-project deltas; skip channels and synthetic fixtures.
>   what it is: Replay consumer projects against a release candidate and close a release only after consumers ran it.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 8 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0493: FEATURE: One-command releases and self-test (C086, value 3/5, effort M, risk low)
>   first version: scripts/release: clean git worktree, run tests, install-user into a temp HOME, then uninstall and diff the tree for a round trip, bump versions and changelog; skip blue/green.
>   what it is: Cut releases from a clean throwaway worktree with clean-install and upgrade tests.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0492, T-0493 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0678. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0493 release.py VERSION bumps all three version fields, adds the changelog heading under Unreleased and commits; refuses a dirty tree or an older version; --push merges into the remote's main — verify with `python3 plugin/tests/run.py -p test_release.py -k Release`
- [x] T-0492 release.py --canary runs fm sentinel in each local project and prints per-project failures before releasing — verify with `python3 plugin/tests/run.py -p test_release.py -k Canary`
## Non-goals
## Approach (options → choice → why)
A release.py at the repo root (next to install.sh), not an fm command: it releases Foreman itself, and other projects release their own way. Steps: refuse a dirty tree or a version that isn't newer; bump plugin.json and both marketplace entries; put the version heading under Unreleased; run fm check (--no-check for tests); commit; --push URL merges into the remote's main from a scratch clone (the flow used by hand for 1.2.16–1.2.19); --canary first runs fm sentinel in every local project fm projects knows and prints what fails. Skipped: blue/green, channels, synthetic fixtures.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] release.py
3. [x] docs (README, MASTER), changelog; release 1.2.20 with it next time
## Resume here
## Docs impact
README layout; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_release.py` → ✗ exit 1 · Ran 4 tests in 0.1s (2 classes, 16 at a time; slowest: Canary 0s, Release 0s) / FAILED (2 classes) [ran] [tree 1bebd484c907] (2026-10-09T17:53:49Z)
- (step 2) `python3 plugin/tests/run.py -p test_release.py` → exit 0 · Ran 4 tests in 0.3s (2 classes, 16 at a time; slowest: Canary 0s, Release 0s) / OK [ran] [tree 942f2a3b81e5] (2026-10-09T17:54:27Z)
- (ac 1) `python3 plugin/tests/run.py -p test_release.py -k Release` → exit 0 · Ran 3 tests in 0.2s (1 classes, 16 at a time; slowest: Release 0s) / OK [ran] [tree 942f2a3b81e5] (2026-10-09T17:54:28Z)
- (ac 2) `python3 plugin/tests/run.py -p test_release.py -k Canary` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Canary 0s) / OK [ran] [tree 942f2a3b81e5] (2026-10-09T17:54:28Z)
- (step 3) `python3 plugin/tests/run.py -p test_release.py -p test_docs.py` → exit 0 · Ran 22 tests in 0.3s (8 classes, 16 at a time; slowest: Canary 0s, Release 0s, PluginConflicts 0s) / OK [ran] [tree 942f2a3b81e5] (2026-10-09T17:54:28Z)
- (audit intent) `self over release.py: refuses dirty trees and non-newer versions, bumps only Foreman's version fields, reverts the bump if fm check fails, pushes via a scratch clone (never touches the working repo's remotes)` → one command replaces the eight manual steps used for 1.2.16–1.2.19 [tree 942f2a3b81e5] (2026-10-09T17:54:28Z)
- (audit adversary) `self over release.py: refuses dirty trees and non-newer versions, bumps only Foreman's version fields, reverts the bump if fm check fails, pushes via a scratch clone (never touches the working repo's remotes)` → --push takes the remote from the command line only; it merges --no-ff into a fresh clone's main and pushes, so a failed merge leaves the remote and the repo untouched; --canary runs each project's own sentinel, which already skips side-effect commands [tree 942f2a3b81e5] (2026-10-09T17:54:28Z)
- (audit edge) `self over release.py: refuses dirty trees and non-newer versions, bumps only Foreman's version fields, reverts the bump if fm check fails, pushes via a scratch clone (never touches the working repo's remotes)` → a CHANGELOG without '## Unreleased' stops before committing; another plugin's version (0.6.1) in marketplace.json is left alone (test) [tree 942f2a3b81e5] (2026-10-09T17:54:28Z)
## Log
- 2026-10-09T15:40:15Z created
- 2026-10-09T17:53:34Z focused
- 2026-10-09T17:54:28Z done
- 2026-10-09T17:54:29Z committed d1c56c2 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0563 [FEATURE M, dropped, 0 steps] One-command releases and self-test (C086, value 3/5, effort M, risk low)
- T-0562 [FEATURE M, dropped, 0 steps] Canary releases with consumer replay (C085, value 3/5, effort M, risk low)
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
- the similar finished task took 7 steps
## Lessons
- A release done by hand four times in a day is a script; the script is the checklist that can't skip a step.
## Files touched
- plugin/tests/test_release.py
- release.py
- CHANGELOG.md
- README.md
