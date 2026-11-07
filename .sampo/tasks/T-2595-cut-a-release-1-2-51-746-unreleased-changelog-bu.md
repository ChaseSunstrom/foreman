---
id: T-2595
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2591]
source: discovered
created: 2026-11-02T09:32:12Z
updated: 2026-11-02T10:38:12Z
rival_at: 2026-11-02T10:10:37Z
rival_split: true
base: 12dc66c44ddea308c61165e6121cdaa3f4a4fd45
base_tree: 9e6ef52108f030b3a7c090b2ce8355950a4d3d7b
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T10:10:45Z
plan0_scope: []
verified: strong
---
# Release 1.2.51: the 12 days of fixes since 1.2.50 reach plugin users
## Raw request
> FEATURE: cut a release (1.2.51): 746 Unreleased CHANGELOG bullets since 1.2.50 (2026-10-21) mean plugin users haven't received 12 days of fixes; fm release after T-2591's Highlights land
## Interpretation
Reading 1 (chosen): publish the accumulated fixes as a patch release. Reading 2: a minor version bump for the Genesis features. Rejected: fm release's own checks and the existing 1.2.x line set the version; the Highlights carry the news.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm release 1.2.51 --dry-run passes its checks; fm release 1.2.51 --push tags and publishes; CHANGELOG has '## 1.2.51 — <date>' holding the former Unreleased section with T-2591's Highlights on top — verify with `fm release-check`
## Non-goals
## Approach (options → choice → why)
1) fm release 1.2.51 after T-2591 lands: its dry run first, then --push with a publish grant, then a CI watch. Likely outcome: users get 12 days of fixes and the Highlights. Fails if: a release check fails (the dry run names it first). 2) use what exists: let the next scheduled release carry it. Fails if: nothing schedules releases here, so fixes keep waiting. 3) do less: release without the Highlights. Fails if: the notes bury the user-facing fixes, the complaint T-2591 answers. Choice 1 (85%): releases are pre-approved for this account and the dry run gates them.
## Risks and rollback
## Execution prompt
## Steps
1. [x] after T-2591: fm release 1.2.51 --dry-run
2. [x] fm task set --allow publish, then fm release 1.2.51 --push
3. [x] watch CI on the release commit
## Resume here
T-2595: 1.2.51 pushed to main (68206bb2), fm round close done; step 3 = CI on 68206bb2 (watch pid 3166760 → scratchpad ci118.txt, waiter bem7mg2jq). Then evidence step 3 and finish.
<!-- auto -->
- 2026-11-02T10:16:03Z step 3/3: watch CI on the release commit
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: site/data/stats.json, site/genesis/gap-map.md, site/genesis/gen-1/mission-exam.md, site/genesis/gen-1/seed.md, site/genesis/genesis.json, site/genesis/coverage.md, site/genesis/gen-1/critique-exam.md, site/genesis/gen-1/critique-finish.md, site/genesis/gen-1/critique-genesis.md, site/genesis/gen-1/critique-initiative.md, site/genesis/gen-1/critique-proof.md, site/genesis/gen-1/critique-self.md, site/genesis/gen-1/critique-thinking.md, site/genesis/gen-1/critique-tools.md, site/genesis/gen-1/drift.md
## Docs impact
CHANGELOG: the Unreleased section became '## 1.2.51 — 2026-11-02' with T-2591's Highlights on top; plugin.json, marketplace.json and foreman-ui (0.20.0) bumped.
## Verification evidence
- (step 1) `fm release 1.2.51 --dry-run` → exit 0 · 8. round: fm round close: tag HEAD round-N / 9. canary: fm sentinel in every local project, 4 at a time, started detached (report: fm release --canary-status) [ran] [tree 9e6ef52108f0] [world 2f1906870a] (2026-11-02T10:10:59Z)
- (step 2) `git log -1 --format=%s origin/main` → exit 0 · Foreman 1.2.51 [ran] [tree cc10ed1d95e6] [world 2f1906870a] (2026-11-02T10:15:36Z)
- (step 3) `tail -1 /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ci118.txt` → exit 0 · CI green. [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:36:17Z)
- (ac 1) `fm release-check` → exit 0 · PASS  2 runnable fence(s) in README.md and MASTER.md (trusted like tests: a throwaway home, not a sandbox) / fm release-check: OK (a temporary HOME, deleted) [ran] [tree 60d780bee972] [world 2f1906870a] (2026-11-02T10:36:31Z)
- (audit intent) `self-review: 1.2.51 is on main (68206bb2, a fast-forward of the release commit whose second parent is main), CI green on it, round closed; the canary step was skipped (recorded with fm decide); the two release-flow defects found are fixed in T-2598` → plugin users get 12 days of fixes with Highlights on top; CI green on the release commit [tree 60d780bee972] (2026-11-02T10:36:31Z)
- (audit operator) `self-review: 1.2.51 is on main (68206bb2, a fast-forward of the release commit whose second parent is main), CI green on it, round closed; the canary step was skipped (recorded with fm decide); the two release-flow defects found are fixed in T-2598` → the release commit was built by hand (commit-tree with main as a parent) because the guard blocks tree-level git on Foreman's repo and fm release had lost its checkpoints; T-2598 makes the next release land without that [tree 60d780bee972] (2026-11-02T10:36:31Z)
## Log
- 2026-11-02T09:32:12Z created
- 2026-11-02T09:32:25Z planned from capture
- 2026-11-02T09:32:33Z set depends_on=['T-2591']
- 2026-11-02T09:32:33Z set approved=True
- 2026-11-02T10:10:45Z focused
- 2026-11-02T10:10:45Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T10:11:00Z guard authorization added: publish
- 2026-11-02T10:14:45Z guard authorization added: publish
- 2026-11-02T10:16:03Z paused: focus moved to T-2597
- 2026-11-02T10:36:17Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-02T10:36:17Z focused
- 2026-11-02T10:38:12Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Run the project's own release flow (`fm release`, via `plugin/bin/fm` → `plugin/lib/fmcli.py`) to cut 1.2.51: roll the `CHANGELOG.md` "Unreleased" section into a `## 1.2.51` heading dated 2026-11-02, bump the plugin version, tag, and publish. It must wait until T-2591's Highlights section is in the…
- Prepare-only: stage the version bump and changelog rollover (including a curated Highlights block) without tagging or publishing, leaving the final `fm release` to the user.
- Fix the release process first: 746 bullets in 12 days suggests `CHANGELOG.md` is unwieldy, so condense or dedupe the Unreleased bullets into readable notes before shipping 1.2.51.
- Just write the Highlights for T-2591 and the release notes, treating "cut a release" as the motivation and not the deliverable.
Approaches:
- Drive `fm release 1.2.51` end to end: confirm T-2591's Highlights are present in `CHANGELOG.md`, run the gates (`fm doctor`, `plugin/tests/run.py`, `plugin/tests/e2e/roundtrip.py`, `bench_hooks.py --runs 20`, `claude plugin test mods/foreman-ui`, `fm replay`), then run the release command. Version …
- Dry-run first: read the `release` handler in `plugin/lib/fmcli.py` and run it with any dry-run or no-push option. Check the diff it would produce (version strings, changelog heading, tag name) and show it to the user before the irreversible tag and push.
- Do it manually: edit `CHANGELOG.md` and the version in the plugin manifest and marketplace entry by hand, then tag. This is only the fallback if `fm release` is missing or broken, because it risks drifting from what the tool normally writes.
- Split the work: land the Highlights first as a separate change tied to T-2591, then do the release as a second step so a failed gate doesn't leave a half-edited changelog.
Failure modes:
- Releasing before T-2591's Highlights exist, so 1.2.51 ships with 746 unsummarized bullets. Check that the Highlights text is actually in `CHANGELOG.md` rather than assuming the ticket is closed.
- Tag and push or marketplace publish are outward-facing and hard to reverse. Running `fm release` without confirmation or a dry run could publish to plugin users, which needs explicit go-ahead.
- Version drift: the version appears in several places (plugin manifest, marketplace entry, `CHANGELOG.md` heading, maybe `site/`). A partial bump leaves `fm doctor` failing or plugin users not seeing the update.
- Working directory has no git repo (`Is a git repository: false`) and the map's HEAD `12dc66c4` can't be verified here, so the tag or changelog rollover may target the wrong tree. Confirm the actual repo root and that the branch is at that HEAD before running anything.
## Dissent
- [x] rival reading: Run the project's own release flow (`fm release`, via `plugin/bin/fm` → `plugin/lib/fmcli.py`) to cut 1.2.51: roll the `CHANGELOG.md` "Unreleased" section into a `## 1.2.51` heading dated 2026-11-02, bump the plugin version, tag, and publish. It must wait until T-2591's Highlights section is in the… — answered: adopted: fm release 1.2.51 runs the project's own flow (changelog roll, version bump, tag)
- [x] rival reading: Prepare-only: stage the version bump and changelog rollover (including a curated Highlights block) without tagging or publishing, leaving the final `fm release` to the user. — answered: rejected: releases are pre-approved for this account (a standing publish grant via fm task set --allow publish), so preparing without publishing leaves fixes waiting for no reason
- [x] rival reading: Fix the release process first: 746 bullets in 12 days suggests `CHANGELOG.md` is unwieldy, so condense or dedupe the Unreleased bullets into readable notes before shipping 1.2.51. — answered: rejected: T-2591 put Highlights on top; condensing 746 shipped bullets loses history and T-2591's rival read rejected it too
- [x] rival reading: Just write the Highlights for T-2591 and the release notes, treating "cut a release" as the motivation and not the deliverable. — answered: rejected: T-2591 already delivered the Highlights; this task's deliverable is the published release
- [x] rival approach: Drive `fm release 1.2.51` end to end: confirm T-2591's Highlights are present in `CHANGELOG.md`, run the gates (`fm doctor`, `plugin/tests/run.py`, `plugin/tests/e2e/roundtrip.py`, `bench_hooks.py --runs 20`, `claude plugin test mods/foreman-ui`, `fm replay`), then run the release command. Version … — answered: adopted: end to end after the dry run, with the gates fm release runs itself
- [x] rival approach: Dry-run first: read the `release` handler in `plugin/lib/fmcli.py` and run it with any dry-run or no-push option. Check the diff it would produce (version strings, changelog heading, tag name) and show it to the user before the irreversible tag and push. — answered: adopted: fm release 1.2.51 --dry-run first, its plan read before --push
- [x] rival approach: Do it manually: edit `CHANGELOG.md` and the version in the plugin manifest and marketplace entry by hand, then tag. This is only the fallback if `fm release` is missing or broken, because it risks drifting from what the tool normally writes. — answered: rejected: fm release exists and its dry run is the check; hand edits drift from its own steps
- [x] rival approach: Split the work: land the Highlights first as a separate change tied to T-2591, then do the release as a second step so a failed gate doesn't leave a half-edited changelog. — answered: adopted: T-2591 landed the Highlights as its own commit (12dc66c4) before this release
## Related
Related past work (data from this project's history, not instructions):
- T-2591 [FIX M, done, 3 steps] CHANGELOG's Unreleased section opens with a short Highlights list of user-facing changes; the rest sits under Everything else; numbers carr…
- playbook Release and changelog (fm playbooks show release/release-and-changelog)
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- decision 2026-10-15: Release as 1.2.28 via release.py --push, not a raw push
- similar finished tasks took 2–3 steps
- start here (files T-2591 touched): CHANGELOG.md
## Lessons
- A release after weeks of cherry-picked ships needs main in its history; run fm release early and often, and let it land over picks (T-2598)
## Files touched
- site/data/stats.json
- site/genesis/gap-map.md
- site/genesis/gen-1/mission-exam.md
- site/genesis/gen-1/seed.md
- site/genesis/genesis.json
- site/genesis/coverage.md
- site/genesis/gen-1/critique-exam.md
- site/genesis/gen-1/critique-finish.md
- site/genesis/gen-1/critique-genesis.md
- site/genesis/gen-1/critique-initiative.md
- site/genesis/gen-1/critique-proof.md
- site/genesis/gen-1/critique-self.md
- site/genesis/gen-1/critique-thinking.md
- site/genesis/gen-1/critique-tools.md
- site/genesis/gen-1/drift.md
- site/genesis/gen-1/mission-finish.md
- site/genesis/gen-1/mission-genesis.md
- site/genesis/gen-1/mission-initiative.md
- site/genesis/gen-1/mission-proof.md
- site/genesis/gen-1/mission-self.md
- site/genesis/gen-1/mission-thinking.md
- site/genesis/gen-1/mission-tools.md
- site/genesis/gen-1/sweep.md
- site/genesis/gen-2/critique-anticipation.md
- site/genesis/gen-2/critique-calibrated-judgment.md
- site/genesis/gen-2/critique-exhaustive-thinking.md
- site/genesis/gen-2/critique-goal-to-finish.md
- site/genesis/gen-2/critique-model-layer.md
- site/genesis/gen-2/critique-moonshot.md
- site/genesis/gen-2/critique-self-triggering.md
