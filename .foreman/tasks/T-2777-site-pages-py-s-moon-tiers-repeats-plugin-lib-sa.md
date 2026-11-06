---
id: T-2777
type: CLEAN
tier: S
status: done
priority: normal
scope: [site/pages.py, plugin/tests/test_site_sections.py]
depends_on: []
source: discovered
created: 2026-11-03T04:54:12Z
updated: 2026-11-03T16:54:45Z
builder_model: sonnet
base: 97537ae23c1c7a3f263e58bf78041732e4b94238
base_tree: 3b183c7c7f5d240f627147b3ee141ed40731c822
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T05:21:04Z
plan0_scope: [site/pages.py, plugin/tests/test_site_sections.py]
lane_stop: merged 2026-11-03T05:24:24Z
verified: strong
---
# The Moons page reads tiers from sampo.moons: site/pages.py imports TIERS instead of repeating them in MOON_TIERS, so the page can't drift from the catalogue
## Raw request
> CLEAN: site/pages.py's MOON_TIERS repeats plugin/lib/sampo/moons.py's TIERS (T-2767's lane couldn't touch the library); build.py should import the tiers from sampo.moons so the Moons page can't drift from the catalogue
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] site/pages.py has no tier list of its own and the Moons page orders tiers by sampo.moons.TIERS — verify with `python3 plugin/tests/run.py test_site_sections`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] after T-2767 merges: import TIERS from sampo.moons in pages.py, drop MOON_TIERS, run test_site_sections
## Resume here
## Docs impact
none
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_sections` → exit 0 · Ran 18 tests in 9.8s (3 classes, 16 at a time; slowest: Built 8s, Pages 0s, Collect 0s) / OK [ran] [tree 2e36f8ce57f8] [world 2f1906870a] (2026-11-03T05:21:26Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_design_gates test_design_lint test_design_sprint test_docs test_fmpy test_genesis test_goal test_map test_moonshot test_motion_verify test_replay test_sampo_design test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_steer test_suite_hygiene test_taste_ledger` → exit 0 · Ran 666 tests in 36.6s (135 classes, 16 at a time; slowest: GenesisRead 30s, GenerationReview 24s, GenesisCheck 22s) / OK [ran] [tree 2e36f8ce57f8] [world 2f1906870a] (2026-11-03T05:22:03Z)
- (ac 1) `python3 plugin/tests/run.py test_site_sections` → exit 0 · Ran 18 tests in 8.4s (3 classes, 16 at a time; slowest: Built 8s, Pages 0s, Collect 0s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:53:42Z)
- (audit intent) `self: read the diff; the Moons page imports TIERS from sampo.moons` → the Moons page can't drift from the catalogue's tiers [tree 398b4aa61509] (2026-11-03T16:53:42Z)
- (audit edge) `self: read the diff; the Moons page imports TIERS from sampo.moons` → a tier outside TIERS gets the smallest size and is left out of the bars, as before [tree 398b4aa61509] (2026-11-03T16:53:42Z)
- (audit adversary) `self: read the diff; the Moons page imports TIERS from sampo.moons` → no input crosses a boundary; the import is local to _moons [tree 398b4aa61509] (2026-11-03T16:53:42Z)
- (audit self) `self: read the diff; the Moons page imports TIERS from sampo.moons` → no findings [tree 398b4aa61509] (2026-11-03T16:53:42Z)
- `python3 plugin/tests/run.py test_site_sections` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:53:42Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:54:13Z)
- (audit intent) `self: read the diff; the Moons page imports TIERS from sampo.moons` → the Moons page can't drift from the catalogue's tiers [tree 398b4aa61509] (2026-11-03T16:54:13Z)
- (audit edge) `self: read the diff; the Moons page imports TIERS from sampo.moons` → a tier outside TIERS gets the smallest size and is left out of the bars, as before [tree 398b4aa61509] (2026-11-03T16:54:13Z)
- (audit adversary) `self: read the diff; the Moons page imports TIERS from sampo.moons` → no input crosses a boundary; the import is local to _moons [tree 398b4aa61509] (2026-11-03T16:54:13Z)
- (audit self) `self: read the diff; the Moons page imports TIERS from sampo.moons` → no findings [tree 398b4aa61509] (2026-11-03T16:54:13Z)
## Log
- 2026-11-03T04:54:12Z created
- 2026-11-03T04:54:42Z planned from capture
- 2026-11-03T04:54:42Z set approved=True
- 2026-11-03T04:54:43Z blocked: waits on T-2767's merge (MOON_TIERS lives in its lane)
- 2026-11-03T05:20:45Z unblocked
- 2026-11-03T05:20:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2777.builder.md
- 2026-11-03T05:21:04Z focused
- 2026-11-03T05:21:04Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T05:24:24Z merged worktree-agent-abb792e1f618bfb49 (1 file(s))
- 2026-11-03T05:25:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abb792e1f618bfb49
- 2026-11-03T15:07:40Z focused
- 2026-11-03T15:07:41Z paused: focus moved to T-2781
- 2026-11-03T16:53:31Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T16:53:31Z focused
- 2026-11-03T16:54:45Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, planned, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/out…
- T-2767 [FEATURE M, planned, 3 steps] Louhi, Moons and Underworld pages from the tower's real records (T-2742 step 7c-1): Louhi's scorecard from exam.jsonl, the Moons cat…
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-02: [costly] [reverses: queued and starts automatically once gen-0's DONE-WHEN holds] [cites: user steer 2026-11-02: Honestly integrate MOOMSHOT into ea…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_design_gates.py, plugin/tests/test_design_lint.py, plugin/tests/test_design_sprint.py, plugin/tests/test_docs.py, plugin/tests/test_fmpy.p…
## Preflight
Changed in scope since this was planned (2026-11-03): site/pages.py; re-ground the plan against them before editing
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- Import a constant, never copy it
## Files touched
- site/pages.py
