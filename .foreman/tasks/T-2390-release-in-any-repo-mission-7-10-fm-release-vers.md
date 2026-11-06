---
id: T-2390
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: [T-2389]
source: user
created: 2026-10-31T14:03:07Z
updated: 2026-10-31T20:53:23Z
builder_model: sonnet
base: 7110c87ba1d4390c0b10a342c466106deb4306d7
base_tree: 64252a686abcd89c71cb4253045454091ae2598d
predict_minutes: 5
predict_attempts: 1
plan0_at: 2026-10-31T20:46:15Z
plan0_scope: []
verified: strong
---
# Release in any repo (Mission 7, #10): fm release VERSION runs the local ritual in any repo (bump, changelog, release proof, commit, tag), with push and publish behind the task's publish grant
## Raw request
> Release in any repo (Mission 7, #10): fm release VERSION runs the local ritual in any repo (bump, changelog, release proof, commit, tag), with push and publish behind the task's publish grant
## Interpretation
Reading 1: fm release VERSION works in any repo through a generic step list (bump, changelog, release proof, commit, tag), with push and publish behind the task's publish grant. Reading 2: a separate verb for other repos. Rejected: two release machines drift, and fmrelease already has the checkpoint and resume machinery.
## Assumptions (confidence)
## Acceptance criteria
- [x] Outside Foreman's repo, fm release VERSION runs named steps with a checkpoint after each (tree clean, fm check, bump the one detected manifest version in pyproject.toml, package.json, Cargo.toml or a gemspec or version file, CHANGELOG's Unreleased headed VERSION, fm prove --release, commit, local annotated tag) with --dry-run and --resume; a red or unproven release proof stops before the commit; a repo with no manifest gets the files it looked at — verify with `python3 plugin/tests/run.py test_release -k any_repo`
- [x] --push in a repo other than Foreman's needs a publish grant the user gave for that repo's remote (never Foreman's own push grant) and spends it the way fm ship does; without one it stops after the local tag, never pushes or publishes, and names the push for the final report — verify with `python3 plugin/tests/run.py test_release -k any_repo_push`
- [x] The release skill (plugin/skills/release/SKILL.md) runs fm release VERSION for any repo, so a session asked to release uses the ritual by default — verify with `python3 plugin/tests/run.py test_release -k any_repo_skill`
## Non-goals
## Approach (options → choice → why)
1) fmrelease gains a repo-kind switch: Foreman's steps stay as they are; other repos get the generic step list, reusing its checkpoint and resume machine and fm ship's grant path; bump and changelog per manifest; the prove step calls fm prove --release; push behind the publish grant. Fails if: a stub repo's manifest is not recognised, which the Python and npm stubs pin. 2) Use what exists: today's hand release with no checkpoint. Likely outcome: no proof and no resume. 3) Do less: only remove the plugin.json refusal. Fails if: a release elsewhere still has no checkpoint and no proof. 4) Wrap each ecosystem's tool (npm version, cargo release, bump2version) as the only path. Breaks where the tool is absent; the bump step may call one when present. Choice 1 (80%): one machine, one grant path.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py; past FIXes T-0980, T-0985, T-1117, T-1129, T-1138.
## Execution prompt
## Steps
1. [x] failing tests first in a stub Python repo and a stub npm repo
2. [x] a repo-kind switch in fmrelease: Foreman's steps stay as they are; other repos get the generic step list
3. [x] bump and changelog per manifest; the prove step calls fm prove --release
4. [x] push behind the publish grant; MASTER.md, README, CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_release -k any_repo` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: AnyRepo 1s, Release 0s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:19Z)
- (step 2) `python3 plugin/tests/run.py test_release -k any_repo` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: AnyRepo 1s, Release 0s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:21Z)
- (step 3) `python3 plugin/tests/run.py test_release -k any_repo` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: AnyRepo 1s, Release 0s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:23Z)
- (step 4) `python3 plugin/tests/run.py test_release test_docs` → exit 0 · Ran 143 tests in 11.3s (31 classes, 16 at a time; slowest: Release 11s, Fences 8s, BoardVerbs 3s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:35Z)
- (ac 1) `python3 plugin/tests/run.py test_release -k any_repo` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: AnyRepo 1s, Release 0s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:37Z)
- (ac 2) `python3 plugin/tests/run.py test_release -k any_repo_push` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: AnyRepo 1s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:38Z)
- (ac 3) `python3 plugin/tests/run.py test_release -k any_repo_skill` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: AnyRepo 0s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:39Z)
- `python3 plugin/tests/run.py test_release -k any_repo` → ✗ exit 1 · Ran 5 tests in 1.8s (2 classes, 16 at a time; slowest: AnyRepo 1s, Release 0s) / FAILED (2 classes: test_release.AnyRepo, test_release.Release) (start tree + this task's tests) [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:43Z)
- `python3 plugin/tests/run.py test_release -k any_repo` → exit 0 · Ran 5 tests in 1.3s (2 classes, 16 at a time; slowest: AnyRepo 1s, Release 0s) / OK [ran] [tree e4b7c9d751b9] (2026-10-31T20:50:43Z)
- (ac 1) `python3 plugin/tests/run.py test_release -k any_repo` → exit 0 · Ran 5 tests in 2.2s (2 classes, 16 at a time; slowest: AnyRepo 2s, Release 0s) / OK [ran] [tree ee4f01a01c2f] (2026-10-31T20:51:19Z)
- (ac 1) `python3 plugin/tests/run.py test_release -k any_repo` → exit 0 · Ran 5 tests in 2.1s (2 classes, 16 at a time; slowest: AnyRepo 2s, Release 0s) / OK [ran] [tree ee4f01a01c2f] (2026-10-31T20:51:25Z)
- (ac 2) `python3 plugin/tests/run.py test_release -k any_repo_push` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: AnyRepo 1s) / OK [ran] [tree ee4f01a01c2f] (2026-10-31T20:51:25Z)
- (ac 3) `python3 plugin/tests/run.py test_release -k any_repo_skill` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: AnyRepo 0s) / OK [ran] [tree ee4f01a01c2f] (2026-10-31T20:51:25Z)
- (audit intent) `main-thread review (pace gate holds): Foreman's own release path is untouched (run_any only when plugin.json is absent); the any-repo steps reuse the checkpoint file, resume, _grant and _spend, so the push grant is the released repo's own project's (never Foreman's); a red or unproven proof stops before the commit with the reason and, when refused, how the user unlocks it; the commit takes only the manifest and CHANGELOG.md; the tag is annotated and local until the grant` → Python and npm stub repos release end to end; a failed proof stops before the commit and --resume finishes; no manifest names what it read; --push without the grant stops after the tag naming it, with the grant pushes branch and tag and spends it; the skill runs fm release for any repo [tree ee4f01a01c2f] (2026-10-31T20:51:25Z)
- (audit adversary) `main-thread review (pace gate holds): Foreman's own release path is untouched (run_any only when plugin.json is absent); the any-repo steps reuse the checkpoint file, resume, _grant and _spend, so the push grant is the released repo's own project's (never Foreman's); a red or unproven proof stops before the commit with the reason and, when refused, how the user unlocks it; the commit takes only the manifest and CHANGELOG.md; the tag is annotated and local until the grant` → --remote starting with '-' refused; the bump replaces only the manifest's first version line; nothing is published (no registry upload) [tree ee4f01a01c2f] (2026-10-31T20:51:25Z)
- (audit edge) `main-thread review (pace gate holds): Foreman's own release path is untouched (run_any only when plugin.json is absent); the any-repo steps reuse the checkpoint file, resume, _grant and _spend, so the push grant is the released repo's own project's (never Foreman's); a red or unproven proof stops before the commit with the reason and, when refused, how the user unlocks it; the commit takes only the manifest and CHANGELOG.md; the tag is annotated and local until the grant` → two manifests with versions is ambiguous and refused; a version not newer is refused; a resumed run skips done steps [tree ee4f01a01c2f] (2026-10-31T20:51:25Z)
## Log
- 2026-10-31T14:03:07Z created
- 2026-10-31T14:33:23Z criterion 2 text: --push in another repo goes through the active task's publish grant the way fm ship does and spends it; without the grant it stops after the local tag and never pushes or publishes → --push in a repo other than Foreman's needs a publish grant the user gave for that repo's remote (never Foreman's own push grant) and spends it the way fm ship does; without one it stops after the local tag, never pushes or publishes, and names the push for the final report
- 2026-10-31T16:08:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2390.builder.md
- 2026-10-31T16:08:07Z builder slot freed
- 2026-10-31T16:11:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2390.builder.md
- 2026-10-31T16:11:30Z builder slot freed
- 2026-10-31T17:14:07Z plan (second-plan review, taken): (1) the grant is publish on the task, keyed to the remote URL the user saw in the ask (stored with the grant), spent by one push like fm ship; a different remote URL = refused; (2) manifests: zero = refused, one = used, several = refused naming them unless --manifest PATH; a Cargo workspace bumps the root's workspace.version only; (3) partial failure: each step checkpoints; an existing tag or version refuses before any change; a failed tag after the commit leaves the commit and says the resume command; (4) fm prove --release on a repo with no proof configured reads unproven, never pass; (5) changelog: no file = created with Keep a Changelog headings; no or empty Unreleased = refused naming it; the release heading gets the date and a fresh empty Unreleased is left.
- 2026-10-31T20:46:14Z focused
- 2026-10-31T20:46:15Z predicted from its closes: 5 min, 1 attempt(s)
- 2026-10-31T20:51:19Z scope: fmrelease (run_any), the release skill, test_release (the old outside-Foreman refusal test now pins the any-repo path), README (one row, under the caps), MASTER, CHANGELOG
- 2026-10-31T20:53:21Z done
- 2026-10-31T20:53:23Z committed 93b4ae33 (6 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The grant model is underspecified. "A publish grant the user gave for that repo's remote" has no stated storage, matching rule, or expiry, and "spends it the way fm ship does" is undefined for a repo that isn't Foreman's. Without a concrete check (grant keyed to the remote URL, one-shot consu…
- HIGH: "Detect the one manifest" is ambiguous when there are several. Monorepos and mixed repos commonly have both `package.json` and `pyproject.toml`, or a Cargo workspace with member versions. The plan covers only "no manifest". Define the behavior for zero, one, and many matches: stop and name th…
- MEDIUM: There is no rollback or partial-failure story. Checkpoints support resume, but nothing says what happens if the commit succeeds and the tag fails, or the tag exists already, or the user abandons the run after the bump. A tag that already exists or a version that is not greater than the curr…
- MEDIUM: `fm prove --release` is assumed to work in arbitrary repos. If it was written against Foreman's own layout, the generic path will either fail everywhere or pass vacuously. Check what it needs from a repo, and say what "unproven" means for a repo with no proof configuration. Otherwise the "r…
- MEDIUM: The changelog handling covers only the "Unreleased" heading. Say what happens when there's no CHANGELOG, no Unreleased section, or an empty one. Also decide the format convention (Keep a Changelog headings, a date on the heading, and a fresh empty Unreleased section left behind), or the out…
- LOW: The criteria check behavior through test names (`-k any_repo`), but the skill criterion (`any_repo_skill`) can only confirm that the text mentions the command. Fine as a pin, but also keep one end-to-end test that runs the skill's documented command line against a stub repo, so the skill and t…
Verdict: revise — the one-machine approach is sound, but the grant semantics and manifest ambiguity need to be pinned down and tested before code, since they decide whether a push can go to the wrong place.
## Dissent
- [ ] HIGH: The grant model is underspecified. "A publish grant the user gave for that repo's remote" has no stated storage, matching rule, or expiry, and "spends it the way fm ship does" is undefined for a repo that isn't Foreman's. Without a concrete check (grant keyed to the remote URL, one-shot consu…
- [ ] HIGH: "Detect the one manifest" is ambiguous when there are several. Monorepos and mixed repos commonly have both `package.json` and `pyproject.toml`, or a Cargo workspace with member versions. The plan covers only "no manifest". Define the behavior for zero, one, and many matches: stop and name th…
- [ ] MEDIUM: There is no rollback or partial-failure story. Checkpoints support resume, but nothing says what happens if the commit succeeds and the tag fails, or the tag exists already, or the user abandons the run after the bump. A tag that already exists or a version that is not greater than the curr…
- [ ] MEDIUM: `fm prove --release` is assumed to work in arbitrary repos. If it was written against Foreman's own layout, the generic path will either fail everywhere or pass vacuously. Check what it needs from a repo, and say what "unproven" means for a repo with no proof configuration. Otherwise the "r…
- [ ] MEDIUM: The changelog handling covers only the "Unreleased" heading. Say what happens when there's no CHANGELOG, no Unreleased section, or an empty one. Also decide the format convention (Keep a Changelog headings, a date on the heading, and a fresh empty Unreleased section left behind), or the out…
- [ ] LOW: The criteria check behavior through test names (`-k any_repo`), but the skill criterion (`any_repo_skill`) can only confirm that the text mentions the command. Fine as a pin, but also keep one end-to-end test that runs the skill's documented command line against a stub repo, so the skill and t…
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1188 [FEATURE M, done, 3 steps] `fm release VERSION` chains release-check, canary, the release.py steps and `fm round clos — lesson: A deferred step that acts on HEAD …
- playbook Release and changelog (fm playbooks show release/release-and-changelog)
- decision 2026-10-31: Mission 7 (proof, #6 #10) approach A: grow fm prove into the one proof verb with a kind per domain (--docs, --infra, --migration, --data, --release;…
- similar finished tasks took 2–3 steps
## Lessons
- Generalize a ritual by giving the new case its own step list on the same checkpoint and grant machinery, leaving the original path untouched
## Files touched
- plugin/tests/test_release.py
- plugin/lib/fmrelease.py
- plugin/skills/release/SKILL.md
- CHANGELOG.md
- MASTER.md
- README.md
