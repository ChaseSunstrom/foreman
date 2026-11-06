---
id: T-2012
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrelease.py, plugin/lib/fmcli.py, plugin/lib/fmaway.py, plugin/lib/fmhooks.py, plugin/lib/fmplaybooks.py, plugin/lib/fmcore.py, plugin/lib/fmloop.py, plugin/tests/test_ship.py, plugin/tests/test_away.py, plugin/tests/test_playbook_machinery.py, plugin/tests/test_core.py, plugin/tests/test_loop.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-29T15:58:38Z
updated: 2026-10-29T16:40:10Z
batch: [T-2007, T-2008, T-2009, T-2010, T-2011]
base: 66d8eee818799dfd527c73841565309da2ec26b2
base_tree: c7acb6b77214100564bc60461442ccba73b6072b
plan0_at: 2026-10-29T16:20:51Z
plan0_scope: [plugin/lib/fmrelease.py, plugin/lib/fmcli.py, plugin/lib/fmaway.py, plugin/lib/fmhooks.py, plugin/lib/fmplaybooks.py, plugin/lib/fmcore.py, plugin/lib/fmloop.py, plugin/tests/test_ship.py, plugin/tests/test_away.py, plugin/tests/test_playbook_machinery.py, plugin/tests/test_core.py, plugin/tests/test_loop.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm ship --task ships a closed task, the away line on a returning prompt, playbook did-you-mean, one suite wait, the loo…
## Raw request
> T-2007: FEATURE: fm ship --task ID ships on a closed task's own publish grant, so a finished task ships without a separate ship task
> @plugin/lib/fmrelease.py
> DONE-WHEN: fm ship --task T-N pushes on T-N's grant and spends it; a task without the grant is refused, nothing pushed :: python3 plugin/tests/run.py test_ship -k ship_on_a_named_tasks_grant
> T-2008: FEATURE: a prompt that ends a silence of 2 h or more gets the away summary in its context, not only a session start
> @plugin/lib/fmaway.py
> DONE-WHEN: the prompt hook adds "Away: N h since you last spoke" after a 2 h gap and nothing after a short one :: python3 plugin/tests/run.py test_away -k on_a_prompt
> T-2009: FEATURE: fm playbooks show with a misspelled name suggests the nearest playbooks
> @plugin/lib/fmplaybooks.py
> DONE-WHEN: fm playbooks show alpah says did you mean fix/alpha :: python3 plugin/tests/run.py test_playbook_machinery -k nearest_names
> T-2010: CLEAN: one suite wait helper for fm check and fm ship, which says when it stops waiting and goes ahead
> @plugin/lib/fmcore.py
> DONE-WHEN: fm check, fm ship use c.wait_while; a wait that times out says so :: python3 plugin/tests/run.py test_core -k wait_while
> T-2011: FEATURE: when the forever loop stops, its decision and fm loop say how many rounds ran and tasks closed since it started
> @plugin/lib/fmloop.py
> DONE-WHEN: the loop-off decision names the rounds run and tasks closed :: python3 plugin/tests/run.py test_loop -k says_what_it_shipped
## Interpretation
Do T-2007, T-2008, T-2009, T-2010, T-2011 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2012. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ship --task ID pushes on that task's publish grant and spends it; a task without one is refused and nothing is pushed — verify with `python3 plugin/tests/run.py test_ship -k ship_on_a_named_tasks_grant`
- [x] a prompt ending a silence of 2 h or more gets the Away line in its context; a short gap gets none — verify with `python3 plugin/tests/run.py test_away -k on_a_prompt`
- [x] fm playbooks show with a misspelled name suggests the nearest playbooks — verify with `python3 plugin/tests/run.py test_playbook_machinery -k nearest_names`
- [x] fm check and fm ship wait through c.wait_while, which says when it stops waiting and goes ahead — verify with `python3 plugin/tests/run.py test_core -k wait_while`
- [x] the loop-off decision and fm loop off name the rounds run and tasks closed since the loop started — verify with `python3 plugin/tests/run.py test_loop -k says_what_it_shipped`
## Non-goals
## Approach (options → choice → why)
A: ship() takes args.task: that task's grant (find_brief, publish in allow) instead of the active task's; same _spend/_push_main path, so the grant is still on a task and spent on use. B: fmaway.returned(p) reads the ledger tail (never the whole ledger on a prompt) for the last two prompts; a gap of GAP or more gives line(p, s); the prompt hook appends it after the secret note. C: fmplaybooks._near via difflib over stage/name and bare name, plus substring; _one's miss and cmd_eval use it. D: c.wait_while(busy, what, who, limit, out) replaces four poll loops and says when the limit runs out. F: fmloop.tally(p, s) counts history rounds and done tasks since started; used in the off decision, fm loop off and status. Rejected: fm task finish --ship (finish would block minutes on CI); a stored last-prompt time in meta (a second write per prompt); Levenshtein by hand (difflib is stdlib).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2007: fm ship --task ID ships on a closed task's own publish grant, so a finished task ships…
2. [x] T-2008: A prompt that ends a silence of 2 h or more gets the away summary in its context, not…
3. [x] T-2009: fm playbooks show with a misspelled name suggests the nearest playbooks
4. [x] T-2010: One suite wait helper for fm check and fm ship, which says when it stops waiting and…
5. [x] T-2011: When the forever loop stops, its decision and fm loop say how many rounds ran and tasks…
## Resume here
<!-- auto -->
- 2026-10-29T16:31:41Z steps 5/5 done
- git: foreman/build; 14 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmaway.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmloop.py, plugin/lib/fmplaybooks.py, plugin/lib/fmrelease.py, plugin/tests/test_away.py
- touched since last checkpoint: plugin/tests/test_ship.py, plugin/lib/fmhooks.py, plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/lib/fmrelease.py, plugin/lib/fmcore.py, plugin/lib/fmloop.py, CHANGELOG.md, MASTER.md, plugin/lib/fmaway.py, plugin/tests/test_away.py
## Docs impact
MASTER.md: fm ship --task (T-2007), the away line on a returning prompt (T-2008), playbook did-you-mean (T-2009), c.wait_while in the fmambient entry (T-2010), the loop tally (T-2011). CHANGELOG Unreleased entry.
## Verification evidence
- `python3 plugin/tests/run.py test_ship test_away test_playbook_machinery test_core test_loop -k ship_on_a_named_tasks_grant -k on_a_prompt -k nearest_names -k wait_while -k says_what_it_shipped` → ✗ exit 1 · Ran 6 tests in 1.7s (5 classes, 16 at a time; slowest: Ship 1s, Loop 0s, Away 0s) / FAILED (5 classes) (start tree + this task's tests) [ran] [tree 7e5163985140] (2026-10-29T16:22:50Z)
- `python3 plugin/tests/run.py test_ship test_away test_playbook_machinery test_core test_loop -k ship_on_a_named_tasks_grant -k on_a_prompt -k nearest_names -k wait_while -k says_what_it_shipped` → ✗ exit 1 · Ran 6 tests in 0.9s (5 classes, 16 at a time; slowest: Ship 1s, Loop 0s, Away 0s) / FAILED (5 classes) [ran] [tree 7e5163985140] (2026-10-29T16:22:50Z)
- `python3 plugin/tests/run.py test_ship test_away test_playbook_machinery test_core test_loop -k ship_on_a_named_tasks_grant -k on_a_prompt -k nearest_names -k wait_while -k says_what_it_shipped` → ✗ exit 1 · Ran 6 tests in 1.7s (5 classes, 16 at a time; slowest: Ship 1s, Loop 0s, Away 0s) / FAILED (5 classes) (start tree + this task's tests) [ran] [tree 3aa28e7e4358] (2026-10-29T16:29:32Z)
- `python3 plugin/tests/run.py test_ship test_away test_playbook_machinery test_core test_loop -k ship_on_a_named_tasks_grant -k on_a_prompt -k nearest_names -k wait_while -k says_what_it_shipped` → exit 0 · Ran 6 tests in 1.4s (5 classes, 16 at a time; slowest: Ship 1s, WaitWhile 1s, Loop 1s) / OK [ran] [tree 3aa28e7e4358] (2026-10-29T16:29:32Z)
- (step 1) `python3 plugin/tests/run.py test_ship -k ship_on_a_named_tasks_grant` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Ship 1s) / OK [ran] [tree 3aa28e7e4358] (2026-10-29T16:29:38Z)
- (step 2) `python3 plugin/tests/run.py test_away` → exit 0 · Ran 9 tests in 1.8s (1 classes, 16 at a time; slowest: Away 1s) / OK [ran] [tree 3aa28e7e4358] (2026-10-29T16:29:40Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_machinery -k nearest_names` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Load 1s) / OK [ran] [tree 3aa28e7e4358] (2026-10-29T16:29:41Z)
- (step 4) `python3 plugin/tests/run.py test_core test_ambient test_ship -k wait_while -k Ambient -k Ship` → exit 0 · Ran 27 tests in 15.6s (3 classes, 16 at a time; slowest: Ambient 15s, Ship 13s, WaitWhile 1s) / OK [ran] [tree 3aa28e7e4358] (2026-10-29T16:29:57Z)
- (step 5) `python3 plugin/tests/run.py test_loop` → exit 0 · Ran 17 tests in 5.3s (3 classes, 16 at a time; slowest: Loop 5s, LoopReview 4s, PipeProgramDebris 0s) / OK [ran] [tree 3aa28e7e4358] (2026-10-29T16:30:03Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (50 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.1    43.8     150  [0] / SessionEnd                  35.8    37.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/* [ran] [tree b1a3f4edb487] (2026-10-29T16:35:38Z)
- (ac 1) `python3 plugin/tests/run.py test_ship -k ship_on_a_named_tasks_grant` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Ship 1s) / OK [ran] [tree b1a3f4edb487] (2026-10-29T16:35:56Z)
- (ac 2) `python3 plugin/tests/run.py test_away -k on_a_prompt` → exit 0 · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: Away 0s) / OK [ran] [tree b1a3f4edb487] (2026-10-29T16:35:56Z)
- (ac 3) `python3 plugin/tests/run.py test_playbook_machinery -k nearest_names` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Load 1s) / OK [ran] [tree b1a3f4edb487] (2026-10-29T16:35:56Z)
- (ac 4) `python3 plugin/tests/run.py test_core -k wait_while` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: WaitWhile 1s) / OK [ran] [tree b1a3f4edb487] (2026-10-29T16:35:56Z)
- (ac 5) `python3 plugin/tests/run.py test_loop -k says_what_it_shipped` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Loop 1s) / OK [ran] [tree b1a3f4edb487] (2026-10-29T16:35:56Z)
- (audit intent) `self-review of the full diff: grant lookup refuses a task without publish and names the fix; away line skips a prompt whose session start already carried it; did-you-mean only above 0.6 similarity; wait_while always says when it gives up; tally counts distinct closed tasks since the loop went on` → each of the five round-20 asks shipped as asked, measured by its own -k test [tree b1a3f4edb487] (2026-10-29T16:35:56Z)
- (audit edge) `self-review of the full diff: grant lookup refuses a task without publish and names the fix; away line skips a prompt whose session start already carried it; did-you-mean only above 0.6 similarity; wait_while always says when it gives up; tally counts distinct closed tasks since the loop went on` → session start then prompt gave the away line twice; fixed with a session_start skip and its test [tree b1a3f4edb487] (2026-10-29T16:35:56Z)
## Log
- 2026-10-29T15:58:38Z created
- 2026-10-29T16:00:10Z set tier=M, scope=['plugin/lib/fmrelease.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmaway.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmplaybooks.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmloop.py', 'plugin/tests/test_ship.py', 'plugin/tests/test_away.py', 'plugin/tests/test_playbook_machinery.py', 'plugin/tests/test_core.py', 'plugin/tests/test_loop.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T16:15:11Z steer: user wants Foreman smarter and faster, not more commands: favor speed (hooks, fm startup, suite time) and better judgment over new verbs
- 2026-10-29T16:20:50Z focused
- 2026-10-29T16:36:52Z done
- 2026-10-29T16:36:54Z committed 40373154 (14 files)
- 2026-10-29T16:37:02Z guard authorization added: publish
- 2026-10-29T16:40:10Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-2005 [FIX S, done, 2 steps] run.py suggests the test a -k meant, the loop's main-thread round sweeps every lens — lesson: A miss message that names the filter is half …
- T-1987 [FIX M, done, 3 steps] Ambient waits out fm ship's run, titles cut at a word, budget-limited loop rounds aren't dry — lesson: A loop's stop rule should count only…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_away.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_hooks.py, plugin/tests/test_loop.py, plugin/tests/test_release.py
## Lessons
- A context line added on a second hook (prompt) must check whether the first hook (session start) already carried it
## Files touched
- plugin/tests/test_core.py
- plugin/tests/test_ship.py
- plugin/tests/test_away.py
- plugin/tests/test_loop.py
- plugin/tests/test_playbook_machinery.py
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- plugin/lib/fmaway.py
- plugin/lib/fmhooks.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmloop.py
- MASTER.md
- CHANGELOG.md
