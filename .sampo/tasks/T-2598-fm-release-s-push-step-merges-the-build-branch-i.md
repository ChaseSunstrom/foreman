---
id: T-2598
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T10:13:20Z
updated: 2026-11-02T10:47:08Z
rival_at: 2026-11-02T10:23:58Z
rival_split: true
base: 6276aa3d97a762341c056abbc1acc728b837e945
base_tree: 42d21710ff8b8459bfa08914cd5e6fa74bbb7456
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T10:24:23Z
plan0_scope: []
verified: strong
---
# fm release's push lands on a main that fm ship fed by cherry-pick: a conflicting merge falls back to a merge commit of the release tree plus main's CI-ignored data, when main holds nothing the branch lacks
## Raw request
> FIX: fm release's push step merges the build branch into main with --no-ff, but fm ship lands each commit on main as a cherry-pick, so after a release cycle of ships the histories diverge (merge base 2026-10-27) and the merge conflicts on files whose content already matches (1.2.51); release should first merge origin/main into the branch (taking the branch's code and main's paths-ignore data) or land unshipped commits the way ship does
## Interpretation
Reading 1 (chosen): fm release must land on a main whose history diverged only because ships cherry-picked; content-equal is safe to merge by construction. Reading 2: stop cherry-picking in fm ship. Rejected: ship's re-picking onto a moved main is its core safety (T-2511, T-2572).
## Assumptions (confidence)
## Acceptance criteria
- [x] when git merge --no-ff conflicts, _push checks each file that differs between main and the release outside main's paths-ignore globs: if main's version of every such file occurs in the release branch's history, it commits tree = release tree with main's ignored files overlaid, parents (main, release), and pushes; any file whose main version the branch never had refuses as before — verify with `python3 plugin/tests/run.py test_release`
- [x] fm release VERSION with plugin.json already at VERSION and HEAD 'Foreman VERSION' (a release commit not yet pushed, checkpoints abandoned) continues from that commit instead of refusing 'isn't newer' — verify with `python3 plugin/tests/run.py test_release`
- [x] after a landed release, the build branch fast-forwards to the landed commit when its tree is clean, so the next release merges from main's history — verify with `python3 plugin/tests/run.py test_release`
## Non-goals
## Approach (options → choice → why)
1) On a conflicting merge, verify main is only behind (each non-data file main differs in has its main blob somewhere in the release's history), then commit-tree the release tree with main's paths-ignore files overlaid, parents (main, release). Likely outcome: releases land after weeks of ships. Fails if: main holds a change the branch never had (then it refuses, as now). 2) use what exists: land the release the way fm ship does (cherry-pick onto main). Fails if: release's tag and round expect a merge commit naming the version; and the branch would still diverge. 3) do less: tell the user to merge origin/main into the branch first. Fails if: Foreman's guard blocks tree-level git on its own repo, so a session can't, and every release would stop. Choice 1 (75%): it encodes exactly the hand fix of 1.2.51 with a check that it's safe.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_release: a cherry-picked history conflicts and still lands; a real divergence refuses; an abandoned bumped release continues
2. [x] fallback in fmrelease._push using _ci_ignored
3. [x] version check accepts an unpushed release commit of the same version
4. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG (Unreleased); the release skill's steps are unchanged (the fallback and the follow are inside step 7).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_release.LandAfterShips` → ✗ exit 1 · Ran 3 tests in 2.0s (1 classes, 16 at a time; slowest: LandAfterShips 2s) / FAILED (1 classes: test_release.LandAfterShips) [ran] [tree 45842685ac54] [world 2f1906870a] (2026-11-02T10:25:29Z)
- (step 2) `python3 plugin/tests/run.py test_release test_ship` → exit 0 · Ran 79 tests in 28.4s (10 classes, 16 at a time; slowest: Ship 28s, Release 11s, BoardVerbs 3s) / OK [ran] [tree 53e6c38666cc] [world 2f1906870a] (2026-11-02T10:27:16Z)
- (step 3) `python3 plugin/tests/run.py test_release test_ship` → exit 0 · Ran 79 tests in 28.1s (10 classes, 16 at a time; slowest: Ship 28s, Release 11s, BoardVerbs 3s) / OK [ran] [tree 53e6c38666cc] [world 2f1906870a] (2026-11-02T10:27:45Z)
- (step 4) `head -5 CHANGELOG.md` → exit 0 · ## Unreleased / - `fm release --push` now lands on a main that `fm ship` has been feeding by cherry-pick. When the release merge conflicts only because the histories split, it commits the release with [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:27:45Z)
- `python3 plugin/tests/run.py test_release.LandAfterShips` → ✗ exit 1 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: LandAfterShips 2s) / FAILED (1 classes: test_release.LandAfterShips) (start tree + this task's tests) [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:33:34Z)
- `python3 plugin/tests/run.py test_release.LandAfterShips` → exit 0 · Ran 3 tests in 2.3s (1 classes, 16 at a time; slowest: LandAfterShips 2s) / OK [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:33:34Z)
- (ac 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 44 tests in 11.2s (9 classes, 16 at a time; slowest: Release 11s, BoardVerbs 3s, ReleaseProof 3s) / OK [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:33:46Z)
- (ac 2) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 44 tests in 11.2s (9 classes, 16 at a time; slowest: Release 11s, BoardVerbs 3s, ReleaseProof 3s) / OK [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:33:46Z)
- (ac 3) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 44 tests in 11.2s (9 classes, 16 at a time; slowest: Release 11s, BoardVerbs 3s, ReleaseProof 3s) / OK [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:33:46Z)
- (audit intent) `self-review: on a conflicting merge _push aborts and calls _land_over_picks, which refuses unless main's version of each non-data differing file appears in the release branch's raw history, then builds tree = release tree with main's CI-ignored files overlaid and commits it with parents (main, release); after the push the clean branch fast-forwards to the landed commit when HEAD is its ancestor; a fresh fm release VERSION on an unpushed 'Foreman VERSION' commit continues from it` → a cherry-pick-fed main takes the release with main's data kept and the branch follows (test); a change main has that the branch never had refuses and pushes nothing (test); an abandoned committed release continues (test) [tree 60d780bee972] (2026-11-02T10:33:46Z)
- (audit adversary) `self-review: on a conflicting merge _push aborts and calls _land_over_picks, which refuses unless main's version of each non-data differing file appears in the release branch's raw history, then builds tree = release tree with main's CI-ignored files overlaid and commits it with parents (main, release); after the push the clean branch fast-forwards to the landed commit when HEAD is its ancestor; a fresh fm release VERSION on an unpushed 'Foreman VERSION' commit continues from it` → the data set comes from main's own committed workflow, so widening paths-ignore needs push access to main, and the overlay only restores main's content; the safety check compares exact blob ids, so a near-identical edit on main still refuses [tree 60d780bee972] (2026-11-02T10:33:46Z)
- (audit edge) `self-review: on a conflicting merge _push aborts and calls _land_over_picks, which refuses unless main's version of each non-data differing file appears in the release branch's raw history, then builds tree = release tree with main's CI-ignored files overlaid and commits it with parents (main, release); after the push the clean branch fast-forwards to the landed commit when HEAD is its ancestor; a fresh fm release VERSION on an unpushed 'Foreman VERSION' commit continues from it` → a file the branch added (absent on main) passes; a data file main removed is removed; later work committed after the release commit stops the branch from following (HEAD isn't an ancestor), and a dirty tree never moves [tree 60d780bee972] (2026-11-02T10:33:46Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:41:56Z)
## Log
- 2026-11-02T10:13:20Z created
- 2026-11-02T10:17:37Z planned from capture
- 2026-11-02T10:24:18Z set approved=True
- 2026-11-02T10:24:23Z focused
- 2026-11-02T10:24:23Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T10:34:28Z done
- 2026-11-02T10:34:31Z committed d2f4f18a (3 files)
- 2026-11-02T10:41:56Z guard authorization added: publish
- 2026-11-02T10:47:08Z publish grant used by fm ship
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Release pre-merge sync (likeliest):** In `fm release`'s push step (likely `plugin/lib/fmcli.py`, with git helpers in `fmcore.py`), merge `origin/main` into the build branch before the `--no-ff` merge into main. Conflicts resolve as: branch wins for code, main wins for `paths-ignore` data (CHANGEL…
- **Release lands commits like ship:** Replace the `--no-ff` merge with the same cherry-pick path `fm ship` uses, so release only picks commits not yet on main and no merge base is involved.
- **Ship/release unification:** Extract the shared "land commits on main" routine so both commands use one implementation, fixing divergence at the root (larger refactor than the request names).
- **Conflict-tolerant merge only:** Use `-X ours/theirs` or a patch-id-aware strategy on the existing merge. This is a narrow reading that treats the symptom and hides real conflicts.
Approaches:
- **Sync-then-merge:** Before the push-step merge, run `git merge origin/main` on the branch with `-X ours`, then restore main's versions of the paths-ignore files via `git checkout origin/main -- <paths>`. The final `--no-ff` merge to main then fast-resolves. The paths-ignore list must come from the…
- **Cherry-pick unshipped:** Compute unshipped commits with `git cherry origin/main <branch>` (patch-id based, which skips ones ship already picked), then reuse ship's landing function on each. Keeps main linear but drops the merge commit that release may record.
- **Shared lander:** Factor ship's cherry-pick logic into one function in `fmcore.py` that release calls with a commit range. Tests in `plugin/tests/` for ship and release both go through it.
- **Merge strategy via temp worktree:** Perform the sync merge in a throwaway worktree so a failed conflict never leaves the user's build branch mid-merge, then fast-forward the branch on success.
Failure modes:
- **`-X ours` is too broad:** It silently takes the branch side for hunks in non-code files that main legitimately changed (CHANGELOG.md, MASTER.md, `site/genesis/genesis.json`) unless the explicit restore of paths-ignore files runs afterward and its path list is complete.
- **Cherry-pick loses semantics:** `git cherry` misses commits that ship amended or conflict-resolved (patch-id differs), so release re-lands content already on main and conflicts again, or double-applies it.
- **Failure leaves state behind:** If the sync merge conflicts partway, the build branch stays in a merging state and the release step aborts after partially mutating the branch; there is no `merge --abort` or rollback on the error path.
- **Push races and remote drift:** `origin/main` is stale unless `git fetch` runs immediately before the sync, so the new merge can still conflict with a ship that landed between fetch and push, and a non-fast-forward push is rejected with no retry.
## Dissent
- [x] rival reading: **Release pre-merge sync (likeliest):** In `fm release`'s push step (likely `plugin/lib/fmcli.py`, with git helpers in `fmcore.py`), merge `origin/main` into the build branch before the `--no-ff` merge into main. Conflicts resolve as: branch wins for code, main wins for `paths-ignore` data (CHANGEL… — answered: adopted in part: after the push lands, the branch fast-forwards to the landed merge so the next release starts from main's history; the merge itself is built at push time in the temp worktree with th…
- [x] rival reading: **Ship/release unification:** Extract the shared "land commits on main" routine so both commands use one implementation, fixing divergence at the root (larger refactor than the request names). — answered: rejected: a larger refactor; ship tests and lands each commit, release lands one commit naming the version
- [x] rival reading: **Conflict-tolerant merge only:** Use `-X ours/theirs` or a patch-id-aware strategy on the existing merge. This is a narrow reading that treats the symptom and hides real conflicts. — answered: rejected: -X strategies resolve real conflicts silently; the fallback refuses any file whose main version the branch never had
- [x] rival approach: **Sync-then-merge:** Before the push-step merge, run `git merge origin/main` on the branch with `-X ours`, then restore main's versions of the paths-ignore files via `git checkout origin/main -- <paths>`. The final `--no-ff` merge to main then fast-resolves. The paths-ignore list must come from the… — answered: adopted in part: main's paths-ignore files win in the overlay; rejected -X ours for the reason in 3
- [x] rival approach: **Cherry-pick unshipped:** Compute unshipped commits with `git cherry origin/main <branch>` (patch-id based, which skips ones ship already picked), then reuse ship's landing function on each. Keeps main linear but drops the merge commit that release may record. — answered: rejected: a release must be one commit naming the version for its tag and round, and patch-id matching misses cherry-picked merges (312 such on main today)
- [x] rival approach: **Shared lander:** Factor ship's cherry-pick logic into one function in `fmcore.py` that release calls with a commit range. Tests in `plugin/tests/` for ship and release both go through it. — answered: rejected: as 2
- [x] rival approach: **Merge strategy via temp worktree:** Perform the sync merge in a throwaway worktree so a failed conflict never leaves the user's build branch mid-merge, then fast-forward the branch on success. — answered: adopted: _push already merges in a temp worktree; the fallback runs there and the branch moves only after the push succeeds
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2212 [FEATURE M, done, 1 steps] fm ship can't ship a lane merged after a conflict resolution: it cherry-picks the lane's… — lesson: Replay a merged branch by its first…
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- T-2572 [FIX M, done, 3 steps] fm ship re-picks onto a moved main without a retest only when every file main gained is one CI itself ignores (the workflow's paths-ignore)…
## Why not caught
release tests always pushed to a main that only ever received release merges; none fed main by cherry-pick, the way fm ship does every day
## Lessons
- Two landing paths into one branch (ship cherry-picks, release merges) must be tested together: each path's tests passed alone while their combination failed on the first real release
## Plan gaps
- failed first: step 1 red tests in test_release: a cherry-picked history conflicts and still lands; a real divergence ref…
## Files touched
- plugin/tests/test_release.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
