---
id: T-2811
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T15:04:24Z
updated: 2026-11-03T18:30:17Z
builder_model: sonnet
base: feab53acf6e697e70b8e3ac76180e0dd92488d16
base_tree: 398b4aa61509921a11428be75074f63572b46454
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T16:41:33Z
plan0_scope: []
lane_stop: merged 2026-11-03T17:07:11Z
verified: strong
unproven: [docs, infra, ui-unshot]
---
# FIX: links point at the renamed repo: chasesunstrom.github.io/foreman now 404s since the repo became ChaseSunstrom/sampo, so README, site, install.sh, INSTALL and templates link to the sampo Pages URL, repo and raw install URL; the scan stops keeping the old address
## Raw request
> FIX: links point at the renamed repo: chasesunstrom.github.io/foreman now 404s since the repo became ChaseSunstrom/sampo, so README, site, install.sh, INSTALL and templates link to the sampo Pages URL, repo and raw install URL; the scan stops keeping the old address
## Interpretation
1. Point links at the new address (chosen): the repo is renamed (github.com/ChaseSunstrom/foreman 301s to sampo) and project Pages don't follow a rename (the old Pages URL 404s), so every tracked link moves to sampo and the scan stops excusing the old address.
2. Keep the old links and restore the old Pages URL instead: needs an outward user-site redirect (prepared in the outward steps, not applied); the in-repo links should be right regardless.
3. Only the Pages links: ruled out; the repo and raw URLs redirect today but would break if a repo named foreman were ever created.
## Assumptions (confidence)
## Acceptance criteria
- [x] no tracked file outside history links chasesunstrom.github.io/foreman, github.com/ChaseSunstrom/foreman or raw.githubusercontent.com/ChaseSunstrom/foreman; each says sampo — verify with `python3 plugin/tests/run.py test_docs test_setup test_doctor test_site_build test_foresight`
- [x] the rename scan's KEPT regex no longer keeps the old repo address, so a new old-address link counts — verify with `python3 plugin/tests/run.py test_rename_scan`
## Non-goals
## Approach (options → choice → why)
1. fm sub over the three address forms, history left alone (chosen). Likely outcome: one small green commit. Fails if: a test pins an old address; the targeted tests catch it.
2. Hand edits per file. Likely outcome: same, slower. Fails if: a file is missed; the scan catches it once KEPT drops the address.
3) use what exists: fm sub and the rename scan (T-2742). Likely outcome: option 1's tooling.
4) do less: fix only README and site links. Fails if: install.sh and templates keep printing the old address.
Choice: 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: the scan counts an old-address link once KEPT drops it
2. [x] rewrite the addresses (fm sub), CHANGELOG history left alone
3. [x] run the tests
## Resume here
## Docs impact
README.md, INSTALL.md, MASTER.md
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_rename_scan 2>&1 | tail -8` → ✗ exit 1 · Ran 4 tests in 1.9s (1 classes, 16 at a time; slowest: RenameScan 1s) / FAILED (1 classes: test_rename_scan.RenameScan) [ran] [tree 8b155b74411d] [world 2f1906870a] (2026-11-03T16:42:08Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_setup test_doctor test_site_build test_foresight test_rename_scan test_site_sampo` → exit 0 · Ran 320 tests in 14.6s (92 classes, 16 at a time; slowest: PredictionBook 14s, Fences 12s, DocsProof 8s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T16:42:51Z)
- `python3 plugin/tests/run.py test_docs test_setup test_doctor test_site_build test_foresight test_rename_scan test_site_sampo` → ✗ exit 1 · Ran 320 tests in 9.8s (92 classes, 16 at a time; slowest: Fences 8s, PredictionBook 7s, ViewsRepair 4s) / FAILED (1 classes: test_rename_scan.RenameScan) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:27:03Z)
- `python3 plugin/tests/run.py test_docs test_setup test_doctor test_site_build test_foresight test_rename_scan test_site_sampo` → exit 0 · Ran 320 tests in 8.5s (92 classes, 16 at a time; slowest: Fences 8s, PredictionBook 7s, ViewsRepair 4s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:27:03Z)
- (ac 1) `python3 plugin/tests/run.py test_docs test_setup test_doctor test_site_build test_foresight` → exit 0 · Ran 307 tests in 8.5s (89 classes, 16 at a time; slowest: Fences 8s, PredictionBook 7s, ViewsRepair 4s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:27:13Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:27:13Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_setup test_doctor test_site_build test_foresight test_rename_scan test_site_sampo` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T18:27:03Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:27:13Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_setup test_doctor test_site_build test_foresight test_rename_scan test_site_sampo` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T18:27:03Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:27:13Z)
- (audit intent) `self: read the diff; 49 links in 13 files move to ChaseSunstrom/sampo; OLD_ADDR counts the old address ahead of KEPT; foreman-desktop and plugin ids left` → every tracked link points at the renamed repo and its live Pages URL [tree 07445d19b39c] (2026-11-03T18:27:13Z)
- (audit edge) `self: read the diff; 49 links in 13 files move to ChaseSunstrom/sampo; OLD_ADDR counts the old address ahead of KEPT; foreman-desktop and plugin ids left` → foreman-desktop is another repo (the regex refuses a trailing -); CHANGELOG history and the plan sentence in SAMPO.md stay [tree 07445d19b39c] (2026-11-03T18:27:13Z)
- (audit adversary) `self: read the diff; 49 links in 13 files move to ChaseSunstrom/sampo; OLD_ADDR counts the old address ahead of KEPT; foreman-desktop and plugin ids left` → links only; GitHub redirects the old repo path today, the new path keeps working if a foreman repo is ever made again [tree 07445d19b39c] (2026-11-03T18:27:13Z)
- (audit self) `self: read the diff; 49 links in 13 files move to ChaseSunstrom/sampo; OLD_ADDR counts the old address ahead of KEPT; foreman-desktop and plugin ids left` → no findings [tree 07445d19b39c] (2026-11-03T18:27:13Z)
## Log
- 2026-11-03T15:04:24Z created
- 2026-11-03T16:41:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2811.builder.md
- 2026-11-03T16:41:32Z focused
- 2026-11-03T16:41:33Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T17:07:11Z merged worktree-agent-a10abe2ed61ca921a (14 file(s))
- 2026-11-03T17:07:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a10abe2ed61ca921a
- 2026-11-03T18:26:43Z focused
- 2026-11-03T18:30:17Z done
## Follow-ups captured
## Build vs reuse
reuse: fm sub, the rename scan; nothing new
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2808 [CLEAN M, planned, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step…
- T-2807 [CLEAN M, planned, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5)
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Lessons
- A rename's links need their own ratchet, since id-shaped kept forms hide them
## Files touched
- .fm-scratch/e.json
- plugin/tests/test_rename_scan.py
- .github/workflows/pages.yml
- INSTALL.md
- MASTER.md
- README.md
- install.sh
- plugin/templates/CLAUDE.lite.md
- plugin/tests/test_docs.py
- plugin/tests/test_doctor.py
- plugin/tests/test_foresight.py
- site/build.py
- site/genesis/index.html
- site/index.html
- plugin/tests/test_site_sampo.py
