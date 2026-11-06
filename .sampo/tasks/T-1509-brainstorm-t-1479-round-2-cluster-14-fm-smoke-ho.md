---
id: T-1509
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsmoke.py, plugin/lib/smoke_web.cjs, plugin/lib/fmcli.py, plugin/tests/test_smoke_profiles.py, CHANGELOG.md, plugin/skills/playbooks/references/ui/visual-qa.md, MASTER.md, plugin/tests/test_smoke.py, plugin/skills/playbooks/ratchet.json]
depends_on: []
source: followup
created: 2026-10-22T17:36:41Z
updated: 2026-10-22T19:59:46Z
base: 0da4b79f385700f42382d050996c6ef10ad33566
base_tree: 9552918d2966f53344f2862b4496c83d2b4837a7
plan0_at: 2026-10-22T18:46:30Z
plan0_scope: [plugin/lib/fmsmoke.py, plugin/lib/smoke_web.cjs, plugin/lib/fmcli.py, plugin/tests/test_smoke_profiles.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 14): fm smoke hostile profiles: torture content (long w
## Raw request
> Brainstorm T-1479 round 2 (cluster 14): fm smoke hostile profiles: torture content (long words, RTL, empty, huge numbers), offline and slow network, colour-vision simulation, frozen time and sampled frames for motion
## Interpretation
fm smoke web gains hostile profiles: torture content (very long words, RTL, empty lists, huge numbers), offline and slow-3G network, colour-vision simulation (deuteranopia, protanopia, tritanopia, achromatopsia as CSS filters), frozen time (clock fixed, animations paused) and sampled frames for motion. Each profile is a flag; results land as screenshots and a pass/fail summary. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] each profile flag is accepted, applied to the page script, and skipped with a reason when no browser is installed — verify with `cd plugin/tests && python3 -m unittest test_smoke_profiles`
- [x] fm smoke web shoots the visual-qa frame matrix (360, 768 and 1440 wide, light and dark, plus a reduced-motion pass) and keeps each run's screenshots under stable names a receipt can point at (absorbs T-1565) — verify with `python3 plugin/tests/run.py test_smoke_profiles`
## Non-goals
## Approach (options → choice → why)
Options: a second harness; chosen: extend smoke_web.cjs and fmsmoke.py with profile flags so fm smoke run --profile NAME works where a browser exists, and is skipped with a reason where it doesn't.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] profiles in smoke_web.cjs and fmsmoke.py
3. [x] fm smoke run --profile
4. [x] frame matrix 360/768/1440 × light/dark + reduced motion, stable screenshot names
## Resume here
## Docs impact
plugin/skills/playbooks/references/ui/visual-qa.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_smoke_profiles` → ✗ exit 1 · Ran 17 tests in 6.4s (3 classes, 16 at a time; slowest: ProfilesFromFm 5s, ProfilesInThePageScript 1s, ProfilesInABrowser 0s) / FAILED (2 classes) [ran] [tree 04b48576d374] (2026-10-22T18:56:06Z)
- (step 2) `FOREMAN_PLAYWRIGHT=~/.npm/_npx/9833c18b2d85bc59/node_modules/playwright PLAYWRIGHT_BROWSERS_PATH=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/browsers python3 plugin/tests/run.py -k ProfilesInABrowser 2>&1 | tail -20` → exit 0 · Ran 2 tests in 34.6s (1 classes, 16 at a time; slowest: ProfilesInABrowser 34s) / OK [ran] [tree 758b1a6c6c7c] (2026-10-22T19:05:39Z)
- (step 3) `FOREMAN_PLAYWRIGHT=~/.npm/_npx/9833c18b2d85bc59/node_modules/playwright PLAYWRIGHT_BROWSERS_PATH=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/browsers python3 plugin/tests/run.py -k ProfilesInABrowser -k SmokeInABrowser 2>&1 | grep -v "GET /" | tail -20` → exit 0 · Ran 5 tests in 88.2s (2 classes, 16 at a time; slowest: SmokeInABrowser 88s, ProfilesInABrowser 32s) / OK [ran] [tree 758b1a6c6c7c] (2026-10-22T19:07:18Z)
- (step 4) `python3 plugin/tests/run.py test_smoke_profiles test_smoke test_verification test_learning2 2>&1 | tail -6` → exit 0 · Ran 40 tests in 3.9s (18 classes, 16 at a time; slowest: ProfilesFromFm 4s, Smoke 3s, NotVerified 2s) / OK [ran] [tree 40e4b2431ada] (2026-10-22T19:09:21Z)
- (step 2) `python3 plugin/tests/run.py test_smoke_profiles test_smoke` → exit 0 · Ran 26 tests in 3.5s (5 classes, 16 at a time; slowest: ProfilesFromFm 3s, Smoke 2s, ProfilesInThePageScript 0s) / OK [ran] [tree 40e4b2431ada] (2026-10-22T19:09:29Z)
- (step 2) `FOREMAN_PLAYWRIGHT=~/.npm/_npx/9833c18b2d85bc59/node_modules/playwright PLAYWRIGHT_BROWSERS_PATH=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/browsers python3 plugin/tests/run.py -k ProfilesInABrowser -k SmokeInABrowser` → exit 0 · Ran 5 tests in 84.1s (2 classes, 16 at a time; slowest: SmokeInABrowser 84s, ProfilesInABrowser 22s) / OK [ran] [tree 40e4b2431ada] (2026-10-22T19:10:57Z)
- (step 3) `python3 plugin/tests/run.py -k ProfilesFromFm` → exit 0 · Ran 6 tests in 3.4s (1 classes, 16 at a time; slowest: ProfilesFromFm 3s) / OK [ran] [tree 40e4b2431ada] (2026-10-22T19:11:38Z)
- (step 4) `python3 plugin/tests/run.py test_smoke_profiles` → exit 0 · Ran 17 tests in 3.5s (3 classes, 16 at a time; slowest: ProfilesFromFm 3s, ProfilesInThePageScript 0s, ProfilesInABrowser 0s) / OK [ran] [tree 40e4b2431ada] (2026-10-22T19:11:42Z)
- (step 4) `FOREMAN_PLAYWRIGHT=~/.npm/_npx/9833c18b2d85bc59/node_modules/playwright PLAYWRIGHT_BROWSERS_PATH=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/browsers python3 plugin/tests/run.py test_smoke_profiles test_smoke` → exit 0 · Ran 26 tests in 88.2s (5 classes, 16 at a time; slowest: SmokeInABrowser 88s, ProfilesInABrowser 23s, ProfilesFromFm 3s) / OK [ran] [tree 03fa1f295e99] (2026-10-22T19:18:00Z)
- (step 4) `FOREMAN_PLAYWRIGHT=~/.npm/_npx/9833c18b2d85bc59/node_modules/playwright python3 plugin/tests/run.py test_smoke_profiles test_smoke` → exit 0 · Ran 26 tests in 3.7s (5 classes, 16 at a time; slowest: ProfilesFromFm 4s, ProfilesInABrowser 3s, Smoke 2s) / OK [ran] [tree 03fa1f295e99] (2026-10-22T19:18:04Z)
- (step 1) `python3 plugin/tests/run.py test_smoke_profiles` → ✗ exit 1 · Ran 26 tests in 9.4s (3 classes, 16 at a time; slowest: ProfilesFromFm 9s, ProfilesInThePageScript 1s, ProfilesInABrowser 0s) / FAILED (2 classes) [ran] [tree 3486fe0e6a2f] (2026-10-22T19:26:32Z)
- (step 3) `python3 plugin/tests/run.py -k ProfilesFromFm` → exit 0 · Ran 11 tests in 33.8s (1 classes, 16 at a time; slowest: ProfilesFromFm 33s) / OK [ran] [tree 45780e812544] (2026-10-22T19:34:18Z)
- (step 4) `python3 plugin/tests/run.py test_smoke_profiles test_smoke` → exit 0 · Ran 35 tests in 20.6s (5 classes, 16 at a time; slowest: ProfilesFromFm 20s, Smoke 8s, ProfilesInThePageScript 2s) / OK [ran] [tree 45780e812544] (2026-10-22T19:34:40Z)
- (step 4) `FOREMAN_PLAYWRIGHT=~/.npm/_npx/9833c18b2d85bc59/node_modules/playwright PLAYWRIGHT_BROWSERS_PATH=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/browsers python3 plugin/tests/run.py test_smoke_profiles test_smoke` → exit 0 · Ran 35 tests in 93.6s (5 classes, 16 at a time; slowest: SmokeInABrowser 93s, ProfilesInABrowser 37s, ProfilesFromFm 23s) / OK [ran] [tree 45780e812544] (2026-10-22T19:36:15Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_smoke_profiles` → exit 0 · Ran 26 tests in 10.469s / OK (skipped=3) [ran] [tree 182aaf3fcdf6] (2026-10-22T19:57:58Z)
- (ac 2) `python3 plugin/tests/run.py test_smoke_profiles` → exit 0 · Ran 26 tests in 10.3s (3 classes, 16 at a time; slowest: ProfilesFromFm 10s, ProfilesInThePageScript 1s, ProfilesInABrowser 0s) / OK [ran] [tree 182aaf3fcdf6] (2026-10-22T19:58:09Z)
- (step 1) `python3 plugin/tests/run.py test_smoke_profiles test_smoke test_playbook_check` → exit 0 · Ran 65 tests in 9.3s (13 classes, 16 at a time; slowest: ProfilesFromFm 9s, Smoke 3s, Snippets 3s) / OK [ran] [tree 182aaf3fcdf6] (2026-10-22T19:58:31Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_smoke_profiles` → exit 0 · Ran 26 tests in 8.108s / OK (skipped=3) [ran] [tree 697ca6d58db6] (2026-10-22T19:58:58Z)
- (ac 2) `python3 plugin/tests/run.py test_smoke_profiles` → exit 0 · Ran 26 tests in 8.6s (3 classes, 16 at a time; slowest: ProfilesFromFm 8s, ProfilesInThePageScript 0s, ProfilesInABrowser 0s) / OK [ran] [tree 697ca6d58db6] (2026-10-22T19:58:58Z)
- (audit intent) `one fm-reviewer pass: 1 HIGH (new findings failing existing gates) + 2 MEDIUM + 7 LOW fixed test-first in a9c28295; real-browser run passed` → hostile profiles and the frame matrix, reachable from Claude Code through the visual-qa playbook [tree 697ca6d58db6] (2026-10-22T19:58:58Z)
- (audit adversary) `one fm-reviewer pass: 1 HIGH (new findings failing existing gates) + 2 MEDIUM + 7 LOW fixed test-first in a9c28295; real-browser run passed` → view names are slugged (no separators), profile names come from argparse choices; each crawl holds a lock on its commit folder; dirty runs get a hashed folder [tree 697ca6d58db6] (2026-10-22T19:58:58Z)
- (audit edge) `one fm-reviewer pass: 1 HIGH (new findings failing existing gates) + 2 MEDIUM + 7 LOW fixed test-first in a9c28295; real-browser run passed` → frame findings don't fail the gate unless strict; budget exhaustion is a note; frames capped at 8000 px; the default frames don't freeze the clock; timeouts kill the browser's process group [tree 697ca6d58db6] (2026-10-22T19:58:58Z)
- (audit maintainer) `one fm-reviewer pass: 1 HIGH (new findings failing existing gates) + 2 MEDIUM + 7 LOW fixed test-first in a9c28295; real-browser run passed` → test_smoke_profiles red first; exit-code fix and timeout path tested [tree 697ca6d58db6] (2026-10-22T19:58:58Z)
## Log
- 2026-10-22T17:36:41Z created
- 2026-10-22T17:55:41Z set scope=['plugin/lib/fmsmoke.py', 'plugin/lib/smoke_web.cjs', 'plugin/lib/fmcli.py', 'plugin/tests/test_smoke_profiles.py', 'CHANGELOG.md']
- 2026-10-22T18:46:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1509.builder.md
- 2026-10-22T18:46:29Z focused
- 2026-10-22T19:12:34Z set scope=['plugin/lib/fmsmoke.py', 'plugin/lib/smoke_web.cjs', 'plugin/lib/fmcli.py', 'plugin/tests/test_smoke_profiles.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/visual-qa.md', 'MASTER.md']
- 2026-10-22T19:12:34Z scope: + visual-qa.md (the playbook that names fm smoke in Claude Code; the main thread asked for its line and matrix) and MASTER.md (docs for fmsmoke)
- 2026-10-22T19:16:26Z set scope=['plugin/lib/fmsmoke.py', 'plugin/lib/smoke_web.cjs', 'plugin/lib/fmcli.py', 'plugin/tests/test_smoke_profiles.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/visual-qa.md', 'MASTER.md', 'plugin/tests/test_smoke.py']
- 2026-10-22T19:16:26Z scope: + test_smoke.py (its browser tests now skip with the crawl's reason when Playwright has no browser)
- 2026-10-22T19:26:22Z review round 1: 10 findings (frame findings as notes unless strict, exit-code test, per-commit lock and diff-hashed dirty folders, no frozen clock in default frames, patient-profile timeouts as notes, Unicode slugs, skipped-later output, frame height cap, _kill test, background docs); red tests first
- 2026-10-22T19:48:39Z set scope=['plugin/lib/fmsmoke.py', 'plugin/lib/smoke_web.cjs', 'plugin/lib/fmcli.py', 'plugin/tests/test_smoke_profiles.py', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/visual-qa.md', 'MASTER.md', 'plugin/tests/test_smoke.py', 'plugin/skills/playbooks/ratchet.json']
- 2026-10-22T19:48:39Z scope: + skills/playbooks/ratchet.json (visual-qa.md grew 3931 → 4479 tokens with the profiles section, after a trim; recorded with fm check playbooks ratchet, design-direction's entry left as it was)
- 2026-10-22T19:51:55Z merged worktree-agent-a71cb242727a79a0c (8 file(s))
- 2026-10-22T19:51:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a71cb242727a79a0c
- 2026-10-22T19:57:46Z focused
- 2026-10-22T19:58:41Z scope: visual-qa.md, MASTER.md, test_smoke.py and ratchet.json (visual-qa growth recorded); other files from other tasks' merges
- 2026-10-22T19:59:44Z done
- 2026-10-22T19:59:46Z committed 33d90841 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261022-grounding-b: ids: b032, b034, b035, b036, b037, b038, b072, b073, b074, b075, b077, b121, b162, b177 [stale: plugin/lib/fmcli.py changed sin…
- playbook Visual QA: screenshots, an eyeball pass and a receipt (skills/playbooks/references/ui/visual-qa.md)
- research brainstorm-20261022-catalogue: Request: "super recursive brainstorm and improve foreman, way more skills/playbooks/way better more capable code, config in the t…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_smoke.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmsmoke.py, plugin/lib/smoke_web.cjs, plugin/skills/playbooks/ratchet.json, plugin/skills/playbooks/references/ui/visual-qa.md, plugin/tests/t…; re-ground the plan against them before editing
## Why not caught
the builder treated the matrix findings like the crawl's own defects
## Lessons
- A new check added to an existing gate must start as a note: findings on users' live pages (video, polling) would otherwise turn every gate red at once
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_smoke_profiles.py
- plugin/lib/smoke_web.cjs
- plugin/lib/fmsmoke.py
- plugin/lib/fmcli.py
- plugin/skills/playbooks/references/ui/visual-qa.md
- MASTER.md
- plugin/tests/test_smoke.py
- CHANGELOG.md
- README.md
- plugin/README.md
- plugin/agents/fm-reviewer.md
- plugin/commands/settings.md
- plugin/lib/fmauditrun.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcore.py
- plugin/lib/fmdesign.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmsettings.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/directions/references/cards.md
- plugin/skills/doctor/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/intake/references/audit.md
- plugin/skills/library/SKILL.md
- plugin/skills/library/cards/looks/light-and-material.md
