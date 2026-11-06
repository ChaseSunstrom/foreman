---
id: T-1519
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/templates, plugin/lib/fmcli.py, plugin/tests/test_docs.py, plugin/skills/library/cards, CHANGELOG.md, plugin/lib/fmnew.py, plugin/lib/fmdemo.py, plugin/lib/fmplaybooks.py, plugin/lib/fmrecall.py, plugin/lib/fmlib.py, plugin/skills/library/SKILL.md, plugin/skills/playbooks/references/ui/templates/scene.html, plugin/skills/playbooks/references/ui/INDEX.md, README.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:44Z
updated: 2026-10-22T21:06:04Z
base: 0298cfcc5972e0448228401b35631878bff328ab
base_tree: 140ba09c34effdbbcd85c782928579af3e23a515
plan0_at: 2026-10-22T20:04:53Z
plan0_scope: [plugin/templates, plugin/lib/fmcli.py, plugin/tests/test_docs.py, plugin/skills/library/cards, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 24): strict-by-default templates for web, 3D and fm cod
## Raw request
> Brainstorm T-1479 round 2 (cluster 24): strict-by-default templates for web, 3D and fm code panels; a release check that runs the documented command fences; 'can Foreman do X?' answered from fm help; a verified: date on library cards
## Interpretation
Templates and docs truth: strict-by-default templates for a web page, a 3D scene and an fm code app panel (fm new templates list); a release check that runs every documented command fence in README and MASTER (marked runnable); 'can Foreman do X?' answered from fm help text; a verified: date on library cards. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] documented runnable fences run green in a temp home; each template exists and passes its own check — verify with `cd plugin/tests && python3 -m unittest test_docs.Fences`
## Non-goals
## Approach (options → choice → why)
Options: hand checks; chosen: a runnable-fence marker in docs and a test that runs them in a temp home; templates as files under plugin/templates.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] templates
3. [x] fence runner
4. [x] card verified dates
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_docs.Fences -k test_docs.HelpAnswers -k test_docs.CardDates` → ✗ exit 1 · Ran 10 tests in 0.3s (3 classes, 16 at a time; slowest: HelpAnswers 0s, CardDates 0s, Fences 0s) / FAILED (3 classes) [ran] [tree 811ebfbc1ad3] (2026-10-22T20:13:15Z)
- (step 2) `python3 plugin/tests/run.py -k test_docs.Fences.test_each_template_passes_its_own_check -k test_docs.Fences.test_the_checks_catch_a_template_gone_loose` → exit 0 · Ran 2 tests in 2.0s (1 classes, 16 at a time; slowest: Fences 2s) / OK [ran] [tree 59dc390fc7af] (2026-10-22T20:23:45Z)
- (step 4) `python3 plugin/tests/run.py -k test_docs.CardDates.test_a_verified_date_is_held_to_a_real_past_day -p test_library.py` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.0s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 59dc390fc7af] (2026-10-22T20:23:48Z)
- (step 4) `python3 plugin/tests/run.py -k test_docs.CardDates` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: CardDates 0s) / OK [ran] [tree 59dc390fc7af] (2026-10-22T20:23:52Z)
- (step 3) `python3 plugin/tests/run.py -k test_docs.Fences -k test_docs.HelpAnswers` → exit 0 · Ran 8 tests in 4.1s (2 classes, 16 at a time; slowest: Fences 4s, HelpAnswers 0s) / OK [ran] [tree 4dc1bdae4e9e] (2026-10-22T20:24:59Z)
- (step 1) `python3 plugin/tests/run.py -k test_docs.Fences -k test_docs.HelpAnswers -k test_docs.CardDates` → ✗ exit 1 · Ran 12 tests in 3.3s (3 classes, 16 at a time; slowest: Fences 3s, HelpAnswers 0s, CardDates 0s) / FAILED (3 classes) [ran] [tree cd9e3943dc3a] (2026-10-22T20:34:35Z)
- (step 3) `python3 plugin/tests/run.py -k test_docs.Fences -k test_docs.HelpAnswers -k test_docs.CardDates` → exit 0 · Ran 12 tests in 8.5s (3 classes, 16 at a time; slowest: Fences 8s, HelpAnswers 0s, CardDates 0s) / OK [ran] [tree 6740e23ec830] (2026-10-22T20:39:34Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_playbook_check test_help` → exit 0 · Ran 98 tests in 10.0s (26 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 3s, Snippets 3s) / OK [ran] [tree 70f134c177f5] (2026-10-22T21:03:13Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_docs.Fences` → exit 0 · Ran 8 tests in 8.677s / OK [ran] [tree 70f134c177f5] (2026-10-22T21:03:23Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1519-review.md)` → fm new check ran any .py unbounded and fail-open: fixed (fm code's owner/writable rule, a .git-rooted file needs --run, child process with limits, a per-run token so sys.exit/os._exit/bare except/alarm(0) can't pass); fences documented as trusted like tests, TMPDIR in the fence folder [tree 70f134c177f5] (2026-10-22T21:03:42Z)
- (audit edge) `review edge lens and builder tests` → copies O_EXCL without --force, --force replaces a symlink itself; verified: dates allow one day ahead; fm help answers cut to 100 columns, --all with a question refused [tree 70f134c177f5] (2026-10-22T21:03:43Z)
- (audit operator) `fm new check PATH --run and fm help QUESTION run by hand in the lane` → messages show the trailing --run form argparse accepts; plain-no reply two lines [tree 70f134c177f5] (2026-10-22T21:03:43Z)
- (audit maintainer) `review maintainer lens` → docstrings and README/MASTER say fences are trusted like tests; fmplaybooks._run reused, no second runner [tree 70f134c177f5] (2026-10-22T21:03:44Z)
- (audit intent) `criterion: documented runnable fences run green in a temp home; each template passes its own check` → met: test_docs.Fences green after merge (8 tests), 98 tests across docs/playbook_check/help [tree 70f134c177f5] (2026-10-22T21:03:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_docs.Fences` → exit 0 · Ran 8 tests in 12.134s / OK [ran] [tree dd1e2c8772b2] (2026-10-22T21:04:10Z)
- (audit adversary) `one fm-reviewer five-lens pass; 6 findings fixed test-first by the builder; criterion green after the merge` → fm new check bounded, confined to fm code's ownership rule, token-gated [tree dd1e2c8772b2] (2026-10-22T21:04:10Z)
- (audit edge) `one fm-reviewer five-lens pass; 6 findings fixed test-first by the builder; criterion green after the merge` → O_EXCL copies, symlink --force, dated cards a day ahead [tree dd1e2c8772b2] (2026-10-22T21:04:10Z)
- (audit intent) `criterion: documented runnable fences run green in a temp home; each template passes its own check; changelog line added` → met: test_docs.Fences green after merge (8 tests), 98 tests across docs/playbook_check/help [tree dd1e2c8772b2] (2026-10-22T21:05:10Z)
- (audit adversary) `one fm-reviewer five-lens pass; 6 findings fixed test-first by the builder; criterion green after the merge` → fm new check bounded, confined to fm code's ownership rule, token-gated [tree dd1e2c8772b2] (2026-10-22T21:05:11Z)
- (audit edge) `one fm-reviewer five-lens pass; 6 findings fixed test-first by the builder; criterion green after the merge` → O_EXCL copies, symlink --force, dated cards a day ahead [tree dd1e2c8772b2] (2026-10-22T21:05:11Z)
## Log
- 2026-10-22T17:36:44Z created
- 2026-10-22T17:56:20Z set scope=['plugin/templates', 'plugin/lib/fmcli.py', 'plugin/tests/test_docs.py', 'plugin/skills/library/cards', 'CHANGELOG.md']
- 2026-10-22T20:04:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1519.builder.md
- 2026-10-22T20:04:52Z focused
- 2026-10-22T20:15:39Z set scope=['plugin/templates', 'plugin/lib/fmcli.py', 'plugin/tests/test_docs.py', 'plugin/skills/library/cards', 'CHANGELOG.md', 'plugin/lib/fmnew.py', 'plugin/lib/fmdemo.py', 'plugin/lib/fmplaybooks.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmlib.py', 'plugin/skills/playbooks/references/ui/templates/scene.html', 'plugin/skills/playbooks/references/ui/INDEX.md', 'README.md', 'MASTER.md']
- 2026-10-22T20:27:12Z set scope=['plugin/templates', 'plugin/lib/fmcli.py', 'plugin/tests/test_docs.py', 'plugin/skills/library/cards', 'CHANGELOG.md', 'plugin/lib/fmnew.py', 'plugin/lib/fmdemo.py', 'plugin/lib/fmplaybooks.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmlib.py', 'plugin/skills/library/SKILL.md', 'plugin/skills/playbooks/references/ui/templates/scene.html', 'plugin/skills/playbooks/references/ui/INDEX.md', 'README.md', 'MASTER.md']
- 2026-10-22T21:02:47Z merged worktree-agent-a95e79731a41dd6d8 (16 file(s))
- 2026-10-22T21:02:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a95e79731a41dd6d8
- 2026-10-22T21:02:51Z focused
- 2026-10-22T21:06:02Z done
- 2026-10-22T21:06:04Z committed 916ce98a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1509 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 14): fm smoke hostile profiles: torture content (long w — lesson: A new check added to an existing g…
- playbook Docs: task-first pages, examples that run (skills/playbooks/references/context/docs.md)
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- similar finished tasks took 2–4 steps
- likely tests for the scope: plugin/templates/mcp-server/test_server.py, plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmdemo.py, plugin/lib/fmlib.py, plugin/lib/fmnew.py, plugin/lib/fmplaybooks.py, plugin/lib/fmrecall.py, plugin/skills/library/SKILL…; re-ground the plan against them before editing
## Why not caught
the first tests only covered except Exception; nothing tried an early exit
## Lessons
- A check that runs user code in-process can be ended green by that code (sys.exit, os._exit, a swallowed alarm): run it in a child and count only a per-run token as a pass
## Plan gaps
- failed first: step 1 failing tests
- failed first: step 4 card verified dates
## Files touched
- plugin/tests/test_docs.py
- plugin/templates/web/index.html
- plugin/skills/playbooks/references/ui/templates/scene.html
- plugin/templates/tui/panel.py
- plugin/lib/fmnew.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmdemo.py
- plugin/lib/fmrecall.py
- plugin/lib/fmlib.py
- plugin/skills/library/cards/tools/jq.md
- plugin/skills/library/cards/tools/ripgrep.md
- plugin/skills/library/SKILL.md
- README.md
- MASTER.md
- plugin/skills/playbooks/references/ui/INDEX.md
- plugin/lib/fmcli.py
- CHANGELOG.md
