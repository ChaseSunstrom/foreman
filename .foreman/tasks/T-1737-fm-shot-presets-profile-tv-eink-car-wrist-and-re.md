---
id: T-1737
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmshot.py, plugin/lib/fmstories.py, plugin/lib/fmcritique.py, plugin/lib/fmcli.py, plugin/tests/test_fmshot.py, plugin/tests/test_stories.py, plugin/skills/ui-design/SKILL.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T04:12:23Z
updated: 2026-10-23T04:35:31Z
batch: [T-1725, T-1734]
base: 58a59257ef391f9da363eadedfd759e3052779d0
base_tree: 49e3981f44dc852784c16722f7896cc9f5ac64e4
plan0_at: 2026-10-23T04:13:33Z
plan0_scope: [plugin/lib/fmshot.py, plugin/lib/fmstories.py, plugin/lib/fmcritique.py, plugin/lib/fmcli.py, plugin/tests/test_fmshot.py, plugin/tests/test_stories.py, plugin/skills/ui-design/SKILL.md, CHANGELOG.md]
verified: strong
---
# fm shot presets: --profile tv|eink|car|wrist and --reduced-motion, also in fm stories
## Raw request
> T-1725: fm shot and fm stories take --profile tv, eink, car or wrist (the critique profile table) so a surface preset drives real screenshots
> T-1734: fm shot --reduced-motion: screenshot a page with prefers-reduced-motion forced, for posters and still states
## Interpretation
Do T-1725, T-1734 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1737. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1725: fm shot and fm stories take --profile tv|eink|car|wrist and use that profile's width, height and scale — verify with `python3 plugin/tests/run.py test_fmshot test_stories`
- [x] T-1734: fm shot --reduced-motion screenshots with prefers-reduced-motion: reduce emulated — verify with `python3 plugin/tests/run.py test_fmshot`
## Non-goals
## Approach (options → choice → why)
Reuse fmcritique.PROFILES as the one table (import it; don't copy). fm shot: --profile sets the viewport and device scale through the same CDP call --width/--height use; explicit --width/--height win over the profile. --reduced-motion: Emulation.setEmulatedMedia with prefers-reduced-motion: reduce before navigation. fm stories passes both through to every state. Help text and the ui-design skill name both flags.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1725: Fm shot and fm stories take --profile tv, eink, car or wrist (the critique profile table)
2. [x] T-1734: Fm shot --reduced-motion: screenshot a page with prefers-reduced-motion forced, for poster
## Resume here
## Docs impact
plugin/skills/ui-design/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_fmshot test_stories` → exit 0 · Ran 43 tests in 44.5s (7 classes, 16 at a time; slowest: Diff 44s, Stories 26s, Capture 23s) / OK [ran] [tree 3e463e9de045] (2026-10-23T04:16:00Z)
- (step 2) `python3 plugin/tests/run.py test_fmshot` → exit 0 · Ran 29 tests in 26.3s (4 classes, 16 at a time; slowest: Diff 26s, Capture 12s, Unruly 7s) / OK [ran] [tree 3e463e9de045] (2026-10-23T04:16:30Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot test_stories` → exit 0 · Ran 43 tests in 22.6s (7 classes, 16 at a time; slowest: Diff 22s, Stories 20s, Capture 10s) / OK [ran] [tree 9a5238e6aa97] (2026-10-23T04:33:38Z)
- (ac 2) `python3 plugin/tests/run.py test_fmshot` → exit 0 · Ran 29 tests in 22.8s (4 classes, 16 at a time; slowest: Diff 23s, Capture 10s, Unruly 6s) / OK [ran] [tree 9a5238e6aa97] (2026-10-23T04:34:01Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot test_stories` → exit 0 · Ran 43 tests in 25.3s (7 classes, 16 at a time; slowest: Diff 25s, Stories 21s, Untrusted 11s) / OK [ran] [tree ec2fd21daa4f] (2026-10-23T04:35:03Z)
- (ac 2) `python3 plugin/tests/run.py test_fmshot` → exit 0 · Ran 29 tests in 26.0s (4 classes, 16 at a time; slowest: Diff 26s, Capture 13s, Unruly 7s) / OK [ran] [tree ec2fd21daa4f] (2026-10-23T04:35:03Z)
- (audit intent) `self: read the diff; one table (fmcritique.PROFILES) imported lazily to avoid a cycle; the scale reaches setDeviceMetricsOverride; prefers-reduced-motion is emulated right after the viewport, before navigation; the stories page header names the real size` → posters and still states can be shot at a TV, e-ink, car or watch viewport and with motion reduced [tree ec2fd21daa4f] (2026-10-23T04:35:03Z)
- (audit edge) `self: read the diff; one table (fmcritique.PROFILES) imported lazily to avoid a cycle; the scale reaches setDeviceMetricsOverride; prefers-reduced-motion is emulated right after the viewport, before navigation; the stories page header names the real size` → an unknown profile can't reach view() (argparse choices); no profile keeps the default viewport; tests use a stub browser, so real rendering is unchecked [tree ec2fd21daa4f] (2026-10-23T04:35:03Z)
- (audit self) `self: read the diff; one table (fmcritique.PROFILES) imported lazily to avoid a cycle; the scale reaches setDeviceMetricsOverride; prefers-reduced-motion is emulated right after the viewport, before navigation; the stories page header names the real size` → no findings [tree ec2fd21daa4f] (2026-10-23T04:35:03Z)
## Log
- 2026-10-23T04:12:23Z created
- 2026-10-23T04:12:56Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_fmshot test_stories`
- 2026-10-23T04:12:56Z criterion 1 text: T-1725: Fm shot and fm stories take --profile tv, eink, car or wrist (the critique profile table) works → T-1725: fm shot and fm stories take --profile tv|eink|car|wrist and use that profile's width, height and scale
- 2026-10-23T04:12:56Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_fmshot`
- 2026-10-23T04:12:56Z criterion 2 text: T-1734: Fm shot --reduced-motion: screenshot a page with prefers-reduced-motion forced, for poster works → T-1734: fm shot --reduced-motion screenshots with prefers-reduced-motion: reduce emulated
- 2026-10-23T04:12:57Z set scope=['plugin/lib/fmshot.py', 'plugin/lib/fmstories.py', 'plugin/lib/fmcritique.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_fmshot.py', 'plugin/tests/test_stories.py', 'plugin/skills/ui-design/SKILL.md', 'CHANGELOG.md']
- 2026-10-23T04:13:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1737.builder.md
- 2026-10-23T04:13:32Z focused
- 2026-10-23T04:32:46Z merged worktree-agent-a12fbdec3c4e8e33a (6 file(s))
- 2026-10-23T04:32:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a12fbdec3c4e8e33a
- 2026-10-23T04:33:14Z focused
- 2026-10-23T04:34:10Z scope: plugin/lib/fmcli.py (two flags each on shot and stories), plugin/skills/ui-design/SKILL.md, CHANGELOG.md
- 2026-10-23T04:35:29Z done
- 2026-10-23T04:35:31Z committed c4a9fba2 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1738 [FIX S, planned, 2 steps] Layout collisions: site header at 320 px, graph poster labels in dense clusters
- T-1736 [CLEAN M, planned, 4 steps] Small cleanups: one WCAG contrast function, unique help-tier positions, doctor's variation selectors, a MASTER.md modul…
- T-1731 [FIX M, active, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_critique.py, plugin/tests/test_fmshot.py, plugin/tests/test_shot.py, plugin/tests/test_stories.py
## Lessons
- Emulate media features before the first navigation, or the first paint misses them
## Files touched
- plugin/tests/test_fmshot.py
- plugin/tests/test_stories.py
- plugin/lib/fmshot.py
- plugin/lib/fmstories.py
- plugin/lib/fmcli.py
- plugin/skills/ui-design/SKILL.md
- CHANGELOG.md
