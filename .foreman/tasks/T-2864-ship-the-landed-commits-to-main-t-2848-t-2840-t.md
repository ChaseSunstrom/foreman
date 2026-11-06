---
id: T-2864
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T00:52:37Z
updated: 2026-11-04T01:15:22Z
rival_at: 2026-11-04T00:52:59Z
rival_split: true
base: 3e621c938fcb4912768844484f16aae0d08268e1
base_tree: 7668d90bd4352efeabe10800118dcaf2565d6ccb
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T00:53:11Z
plan0_scope: []
verified: strong
---
# Ship the landed commits to main: T-2848, T-2840, T-2850, T-2853, T-2844, T-2857, T-2863, T-2858 and the CHANGELOG (user: push to main any time)
## Raw request
> Ship the landed commits to main: T-2848, T-2840, T-2850, T-2853, T-2844, T-2857, T-2863, T-2858 and the CHANGELOG (user: push to main any time)
## Interpretation
Reading 1 (chosen): push foreman/build's landed, closed work to origin main through fm ship after full gates, as the user's standing 'push to main any time' allows. Reading 2 (ruled out): a release (version bump and tag); the user granted pushes, and a release waits for the rename to finish (T-2742 step 9).
## Assumptions (confidence)
## Acceptance criteria
- [x] the landed commits are on origin main after full gates — verify with `fm ship --check`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: fm ship --task T-2864 under fm task set --allow publish, after fm check at low load. Likely outcome: pushed, CI watched. Fails if a gate is red; then the red one becomes its own fix first.
2. git push by hand. Fails: skips the gates and the ship ledger.
3. Do less: wait for T-2847 to land first. Fails: holds 9 landed fixes back for an unrelated lane.
Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] full gates, then fm ship under a publish grant
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `fm ship --check` → exit 0 · nothing to ship: origin main already has HEAD's changes after the last shipped commit 3e621c93 [ran] [tree 7668d90bd435] [world 2f1906870a] (2026-11-04T01:15:20Z)
- (step 1) `fm ship --check` → exit 0 · nothing to ship: origin main already has HEAD's changes after the last shipped commit 3e621c93 [ran] [tree 7668d90bd435] [world 2f1906870a] (2026-11-04T01:15:20Z)
- (audit edge) `shipped 10 commits to origin main at 8114656 after fm check exit 0 (6017 tests) and fm ship's own run on the pushed commits` → T-2847's lane is unmerged and stays off main until its review fixes and full check land [tree 7668d90bd435] (2026-11-04T01:15:20Z)
- (audit self) `shipped 10 commits to origin main at 8114656 after fm check exit 0 (6017 tests) and fm ship's own run on the pushed commits` → no findings [tree 7668d90bd435] (2026-11-04T01:15:20Z)
## Log
- 2026-11-04T00:52:37Z created
- 2026-11-04T00:53:10Z focused
- 2026-11-04T00:53:11Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T01:04:55Z guard authorization added: publish
- 2026-11-04T01:15:04Z publish grant used by fm ship
- 2026-11-04T01:15:22Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: cherry-pick or merge the commits for tickets T-2848, T-2840, T-2850, T-2853, T-2844, T-2857, T-2863 and T-2858 (landed on some other branch or worktree) onto `main`, then add or update `CHANGELOG.md` entries for them, and `git push origin main`. The user's "push to main any time" is stan…
- "Landed" could mean already merged into an integration branch, so the job is a fast-forward or merge of that branch into `main`. That would also bring along any unlisted commits that sit between the listed ones.
- "The CHANGELOG" could mean the CHANGELOG commit already exists and just needs shipping with the rest, not a fresh edit.
- The working directory `/run/user/1000/fm-children-1000` is not a git repository, so the real repo (HEAD 3e621c93) may be elsewhere, such as the parent foreman checkout. The request may be aimed at that checkout and not at this directory.
Approaches:
- Locate the repo first. Run `git log --all --grep 'T-28'` to map each ticket ID to its commit(s) and to the branch they sit on. Check for missing tickets, since all eight must be found. Then run the gates (`fm doctor`, `python3 plugin/tests/run.py`) on a temporary branch off `main` before pushing.
- Cherry-pick the commits in original topological order (`git rev-list --reverse`) onto an up-to-date `main`. Resolve `CHANGELOG.md` conflicts by hand, since it is the most-changed file. Then push.
- If all eight sit on one clean branch ahead of `main`, merge it with `--ff-only` and skip the cherry-picks. Check `git log main..branch` for extra commits first, and ship only what the user listed.
- Build the CHANGELOG entries from the commit subjects, in the file's existing format, as one final commit, so the changelog matches exactly what shipped.
Failure modes:
- A ticket ID matches several commits (fixups, reverts, or a mention in another ticket's message), so the wrong commits get picked, or one is left out while the push still succeeds.
- Cherry-picking out of order, or leaving out a dependency commit, produces conflicts or a tree that builds differently from where it was tested. This is most likely in `plugin/lib/fmcli.py`, `plugin/lib/fmcore.py` and `plugin/lib/fmhooks.py`, which many tickets touch. The gates (`plugin/tests/run.py…
- `CHANGELOG.md` conflicts get resolved by taking one side wholesale, which silently drops other tickets' entries. Or the entries are written for commits that were not shipped.
- Running in `/run/user/1000/fm-children-1000`, which is not a git repo, so git commands fail or hit an unintended parent repo. Pushing from the wrong checkout or branch would publish unrelated work.
## Dissent
- [x] rival reading: Likeliest: cherry-pick or merge the commits for tickets T-2848, T-2840, T-2850, T-2853, T-2844, T-2857, T-2863 and T-2858 (landed on some other branch or worktree) onto `main`, then add or update `CHANGELOG.md` entries for them, and `git push origin main`. The user's "push to main any time" is stan… — answered: rejected: no cherry-picks; fm ship pushes foreman/build's history to origin main as every earlier ship did
- [x] rival reading: "Landed" could mean already merged into an integration branch, so the job is a fast-forward or merge of that branch into `main`. That would also bring along any unlisted commits that sit between the listed ones. — answered: adopted: foreman/build is the integration branch; fm ship pushes it whole, unlisted landed commits included, all closed and gated
- [x] rival reading: "The CHANGELOG" could mean the CHANGELOG commit already exists and just needs shipping with the rest, not a fresh edit. — answered: adopted: the CHANGELOG commits (1a723cfb, 3e621c93) exist and ship with the rest
- [x] rival reading: The working directory `/run/user/1000/fm-children-1000` is not a git repository, so the real repo (HEAD 3e621c93) may be elsewhere, such as the parent foreman checkout. The request may be aimed at that checkout and not at this directory. — answered: rejected: the repo is ~/.claude/foreman (HEAD 3e621c93); the rival ran from a scratch dir
- [x] rival approach: Locate the repo first. Run `git log --all --grep 'T-28'` to map each ticket ID to its commit(s) and to the branch they sit on. Check for missing tickets, since all eight must be found. Then run the gates (`fm doctor`, `python3 plugin/tests/run.py`) on a temporary branch off `main` before pushing. — answered: rejected: fm ship reads the commits itself; every landed task here is closed by its own finish
- [x] rival approach: Cherry-pick the commits in original topological order (`git rev-list --reverse`) onto an up-to-date `main`. Resolve `CHANGELOG.md` conflicts by hand, since it is the most-changed file. Then push. — answered: rejected: cherry-picking rewrites history the next ship would diverge from
- [x] rival approach: If all eight sit on one clean branch ahead of `main`, merge it with `--ff-only` and skip the cherry-picks. Check `git log main..branch` for extra commits first, and ship only what the user listed. — answered: adopted in effect: fm ship fast-forwards origin main from foreman/build after the gates
- [x] rival approach: Build the CHANGELOG entries from the commit subjects, in the file's existing format, as one final commit, so the changelog matches exactly what shipped. — answered: rejected: each task's line is already in the CHANGELOG, written as it closed
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2390 [FEATURE M, done, 4 steps] Release in any repo (Mission 7, #10): fm release VERSION runs the local ritual in any repo (bump, changelog, release proof, commit, tag…
- playbook Release and changelog (fm playbooks show release/release-and-changelog)
- decision 2026-11-02: [outward] Release 1.2.51 finished by hand after fm release refused a fresh run (version already bumped) and its checkpoints were abandoned: pushed t…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–4 steps
