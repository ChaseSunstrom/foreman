---
id: T-2849
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T22:17:21Z
updated: 2026-11-03T22:47:49Z
rival_at: 2026-11-03T22:32:06Z
base: 363b6c3fc2514131dc51df5d37eeab7ada83e6cb
base_tree: 8136bffa2548af31aa06242d309cec9d6cb452f7
predict_minutes: 1
predict_attempts: 1
plan0_at: 2026-11-03T22:32:12Z
plan0_scope: []
verified: strong
---
# Ship the landed commits to main: T-2834 through T-2846 on foreman/build (user: push to main any time)
## Raw request
> Ship the landed commits to main: T-2834 through T-2846 on foreman/build (user: push to main any time)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin main has every landed commit — verify with `fm ship --check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] full gates, then fm ship under a publish grant
## Resume here
<!-- auto -->
- 2026-11-03T22:41:59Z step 1/1: full gates, then fm ship under a publish grant
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/12-forge-illustrated/_review/r3/extra_r3.py, /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/picker/watch.sh
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check` → exit 0 · nothing to ship: origin main already has HEAD's changes after the last shipped commit 363b6c3f [ran] [tree 8136bffa2548] [world 2f1906870a] (2026-11-03T22:47:48Z)
- (step 1) `fm ship --check` → exit 0 · nothing to ship: origin main already has HEAD's changes after the last shipped commit 363b6c3f [ran] [tree 8136bffa2548] [world 2f1906870a] (2026-11-03T22:47:48Z)
- (audit edge) `shipped 11 commits to origin main at 1e906ee after fm check exit 0 and the 6007-test affected run` → post-merge reds fixed in T-2855 before the ship [tree 8136bffa2548] (2026-11-03T22:47:48Z)
- (audit self) `shipped 11 commits to origin main at 1e906ee after fm check exit 0 and the 6007-test affected run` → no findings [tree 8136bffa2548] (2026-11-03T22:47:48Z)
## Log
- 2026-11-03T22:17:21Z created
- 2026-11-03T22:32:12Z focused
- 2026-11-03T22:32:12Z predicted from its closes: 1 min, 1 attempt(s)
- 2026-11-03T22:37:49Z guard authorization added: publish
- 2026-11-03T22:47:37Z publish grant used by fm ship
- 2026-11-03T22:47:49Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: fast-forward/merge into `main` the already-committed work for tickets T-2834..T-2846 that sits on branch `foreman/build`, then `git push origin main`. The user explicitly authorized pushing to main, so no confirmation is needed. "Landed" implies the commits are already on `foreman/build`…
- Only the commits whose messages reference T-2834..T-2846 are meant to ship. If `foreman/build` contains other commits interleaved (or tickets in the range missing, e.g. T-2840 never landed), the request means cherry-pick the matching ones rather than the whole branch.
- "Ship" could mean a release: bump the version, update `CHANGELOG.md`, and tag, in addition to the push. The request only says "push to main", so this is less likely.
- Possibly the work is meant to go through a PR or the repo's own landing flow (an `fm` subcommand in `plugin/lib/fmcli.py`) rather than a raw `git push`.
Approaches:
- Plain git: in the repo (the working directory here is not a git repo, so first locate the real one), run `git fetch`, then `git log main..foreman/build --grep 'T-28'` to list the ticket commits. If they're exactly the branch's new commits and `main` is an ancestor, run `git push origin foreman/buil…
- Rebase-then-push when `main` has moved: rebase `foreman/build` onto `origin/main`, run the gates (`fm doctor`, `python3 plugin/tests/run.py`, `roundtrip.py`), then push. Rebased SHAs differ from the "landed" ones, so report this.
- Cherry-pick path when the range is mixed: create a temp branch off `origin/main`, cherry-pick only the T-2834..T-2846 commits in order, run the gates, and push that branch to `main`.
- Check `plugin/lib/fmcli.py` for an existing ship/land subcommand and use it if it exists, since it may enforce the hooks and guards in `plugin/lib/fmguard.py` that a raw push would bypass.
Failure modes:
- The current directory `/run/user/1000/fm-children-1000` is not a git repo, so running git there fails or hits the wrong repo. The real repo (HEAD `363b6c3f`) has to be found before any push, or the push goes nowhere.
- A non-fast-forward rejection because `main` advanced. The tempting fix is `--force`, which would overwrite others' commits. The correct response is to rebase and rerun the gates, never force.
- The ticket range is not contiguous on the branch: a commit for one ticket is missing, reverted, or tagged differently (e.g. `T-2840` in a body rather than the subject), so a `--grep` silently ships too few or too many commits.
- Skipping the gates (`fm doctor`, `bench_hooks.py`, `claude plugin test mods/foreman-ui`) after a rebase or cherry-pick means a broken `main` ships. A `fmguard.py`/`fmhooks.py` pre-push hook rejecting the push should be read as feedback, not bypassed with `--no-verify`.
## Dissent
- [x] rival reading: Likeliest: fast-forward/merge into `main` the already-committed work for tickets T-2834..T-2846 that sits on branch `foreman/build`, then `git push origin main`. The user explicitly authorized pushing to main, so no confirmation is needed. "Landed" implies the commits are already on `foreman/build`… — answered: adopted: fm ship pushes foreman/build's landed commits to origin main
- [x] rival reading: Only the commits whose messages reference T-2834..T-2846 are meant to ship. If `foreman/build` contains other commits interleaved (or tickets in the range missing, e.g. T-2840 never landed), the request means cherry-pick the matching ones rather than the whole branch. — answered: rejected: every commit on foreman/build since the last push ships, as fm ship's range is defined; the held-for-T-2742 commit rule is fm ship's own
- [x] rival reading: "Ship" could mean a release: bump the version, update `CHANGELOG.md`, and tag, in addition to the push. The request only says "push to main", so this is less likely. — answered: rejected: no release; a push to main as the standing grant says
- [x] rival reading: Possibly the work is meant to go through a PR or the repo's own landing flow (an `fm` subcommand in `plugin/lib/fmcli.py`) rather than a raw `git push`. — answered: adopted: fm ship is the repo's landing flow (full gates, publish grant)
- [x] rival approach: Plain git: in the repo (the working directory here is not a git repo, so first locate the real one), run `git fetch`, then `git log main..foreman/build --grep 'T-28'` to list the ticket commits. If they're exactly the branch's new commits and `main` is an ancestor, run `git push origin foreman/buil… — answered: rejected: fm ship, not raw git
- [x] rival approach: Rebase-then-push when `main` has moved: rebase `foreman/build` onto `origin/main`, run the gates (`fm doctor`, `python3 plugin/tests/run.py`, `roundtrip.py`), then push. Rebased SHAs differ from the "landed" ones, so report this. — answered: rejected: fm ship refuses a moved main rather than rebasing
- [x] rival approach: Cherry-pick path when the range is mixed: create a temp branch off `origin/main`, cherry-pick only the T-2834..T-2846 commits in order, run the gates, and push that branch to `main`. — answered: rejected: the range isn't mixed
- [x] rival approach: Check `plugin/lib/fmcli.py` for an existing ship/land subcommand and use it if it exists, since it may enforce the hooks and guards in `plugin/lib/fmguard.py` that a raw push would bypass. — answered: adopted: fm ship
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2813 [CLEAN S, done, 1 steps] Ship the held commits to main: the Sampo rename steps 4-5, the closes and fixes landed on foreman/build since the last push (user: 'feel …
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- decision 2026-10-30: [revisited: feel free to push to main] [cites: user steer 2026-10-29: push to main without asking] [check: python3 plugin/tests/run.py test_ship.Shi…
