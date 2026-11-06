---
id: T-0950
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:53:31Z
updated: 2026-10-15T21:36:05Z
base: e932532c02629a175db49071c9187fc5f3c184dc
base_tree: d20e3643710d63995345eb8c09d6f32cc19a3630
verified: strong
---
# fm scout: Foreman finds its own work (Claude Code updates, library gaps, doctor findings, stale sources, friction, brainstorm when dry) and the drive works it, no asking
## Raw request
> I don't like how I have to ask for skills/fixes/changes/whatever, foreman should be able to figure everything out itself, without me doing anything
## Interpretation
The user doesn't want to ask for skills, fixes, playbooks, MCP, LSP, Claude Code updates or efficiency work: Foreman should notice it and do it. Today the pieces exist but wait to be asked: fm night jobs (dream, cold files, sentinel, landscape), fm friction (--every), the board, fm doctor, fm lib. Done means zero-token probes, run whenever the queue drains in full autonomy and first thing in fm night, turn what they find into grounded inbox items once each. Then the drive works them: a newer Claude Code to adopt, dependencies in your projects with no stack card, stale skill sources, doctor findings, a friction pass that's due, a brainstorm round when the queue is dry, unbuilt board items.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scout runs zero-token probes and captures each finding once under a per-probe key (cc:<version>, libgap:<deps>, doctor:<check>, friction:<week>, brainstorm:<week>), so a dropped key stays quiet and a new version is new; at most 3 captures a run, at most 5 open scout items, and at most one run per 30 min; each probe's own I/O is time-limited and a failing one is logged (a scout ledger event) and skipped, never cached as nothing; fm scout --dry lists without capturing or writing — verify with `python3 plugin/tests/run.py -k Scout` — verify with `python3 plugin/tests/run.py -k Scout`
- [x] The Claude Code probe compares the published latest (cached 12 h, successes only) with the installed version and Foreman's CC_TESTED constant (README states the same version, checked by a doc test): newer captures 'Adopt Claude Code X' (worked through the normal loop, the guard still gating any install); equal, offline, a timeout or a malformed answer capture nothing — verify with `python3 plugin/tests/run.py -k ScoutProbes`
- [x] The library-gap probe captures 'Write stack cards for …' listing dependencies used in registered projects that no card covers; the sources probe refreshes sources older than 7 days without an item — verify with `python3 plugin/tests/run.py -k ScoutProbes`
- [x] End to end: a Stop when the queue drains under full autonomy and drive on runs scout and the hook's answer names the item it found and continues; with no quick find it asks once per 6 h for fm scout --slow; an answer to a question isn't a drain; fm night runs scout first; brainstorm-due and friction-due probes each capture in a fixture — verify with `python3 plugin/tests/run.py -k ScoutDrive` — verify with `python3 plugin/tests/run.py -k ScoutDrive`
## Non-goals
## Approach (options → choice → why)
Options: (A) fm scout, deterministic probes behind a registry with dedupe keys, triggered by the idle Stop under full autonomy and by fm night (chosen: zero tokens to look, model tokens only for the work it queues, and every item says why); (B) ask the model 'what next?' at every idle stop (tokens on every stop, ungrounded); (C) system timers or cron (outward system change, and nothing happens in the interactive session); (D) only extend fm night (nothing runs until the user sets up scheduling). Budget gates (fmbudget) still apply to the work; probes with network reads are cached.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing Scout, ScoutProbes and ScoutDrive tests
2. [x] fmscout: probe registry, dedupe keys, capture; probes: claude-code, library gaps, sources, doctor, friction due, brainstorm due, board leftovers
3. [x] Wire: the Stop hook when idle under full autonomy; fm night first job; fm scout verb
4. [x] Docs: README (it finds its own work), MASTER, rules line
## Resume here
<!-- auto -->
- 2026-10-15T21:21:43Z step 1/4: Failing Scout, ScoutProbes and ScoutDrive tests
- git: foreman/build; 5 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmnight.py, plugin/lib/fmscout.py, plugin/tests/test_scout.py
- touched since last checkpoint: plugin/lib/fmscout.py, plugin/lib/fmnight.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_scout.py
## Docs impact
README, MASTER, CHANGELOG
## Verification evidence
- `python3 plugin/tests/run.py test_scout` → ✗ exit 1 · Ran 0 tests in 0.7s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b79115cd57c6] (2026-10-15T21:20:19Z)
- `python3 plugin/tests/run.py test_scout` → ✗ exit 1 · Ran 10 tests in 31.2s (3 classes, 16 at a time; slowest: Scout 31s, ScoutDrive 1s, ScoutProbes 1s) / FAILED (1 classes) [ran] [tree b79115cd57c6] (2026-10-15T21:20:19Z)
- (step 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 10 tests in 7.7s (3 classes, 16 at a time; slowest: Scout 8s, ScoutDrive 1s, ScoutProbes 0s) / OK [ran] [tree 4d4ee2cfe87a] (2026-10-15T21:23:50Z)
- (step 2) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 11 tests in 7.6s (3 classes, 16 at a time; slowest: Scout 7s, ScoutDrive 1s, ScoutProbes 0s) / OK [ran] [tree f20fc57d218a] (2026-10-15T21:24:43Z)
- (step 3) `python3 plugin/tests/run.py test_scout test_night test_hooks.Stop` → exit 0 · Ran 64 tests in 28.3s (10 classes, 16 at a time; slowest: Stop 28s, Scout 8s, NightGuards 2s) / OK [ran] [tree f20fc57d218a] (2026-10-15T21:25:12Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_doctor test_scout` → exit 0 · Ran 77 tests in 23.3s (26 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, Scout 9s) / OK [ran] [tree d86e4aa690d2] (2026-10-15T21:28:19Z)
- (step 4) `python3 plugin/tests/run.py test_scout test_night test_hooks.Stop test_docs test_doctor` → exit 0 · Ran 135 tests in 29.3s (33 classes, 16 at a time; slowest: Stop 29s, Command 22s, Scout 16s) / OK [ran] [tree 007018833231] (2026-10-15T21:35:35Z)
- (ac 1) `python3 plugin/tests/run.py -k Scout' — verify with 'python3 plugin/tests/run.py -k Scout` → exit 0 · Ran 16 tests in 24.2s (3 classes, 16 at a time; slowest: Scout 24s, ScoutDrive 2s, ScoutProbes 1s) / OK [ran] [tree 007018833231] (2026-10-15T21:36:03Z)
- (ac 2) `python3 plugin/tests/run.py -k ScoutProbes` → exit 0 · Ran 7 tests in 1.1s (1 classes, 16 at a time; slowest: ScoutProbes 1s) / OK [ran] [tree 007018833231] (2026-10-15T21:36:03Z)
- (ac 3) `python3 plugin/tests/run.py -k ScoutProbes` → exit 0 · Ran 7 tests in 1.1s (1 classes, 16 at a time; slowest: ScoutProbes 1s) / OK [ran] [tree 007018833231] (2026-10-15T21:36:03Z)
- (ac 4) `python3 plugin/tests/run.py -k ScoutDrive' — verify with 'python3 plugin/tests/run.py -k ScoutDrive` → exit 0 · Ran 3 tests in 2.2s (1 classes, 16 at a time; slowest: ScoutDrive 2s) / OK [ran] [tree 007018833231] (2026-10-15T21:36:03Z)
- (audit intent) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 9 findings, 8 fixed test-first, board probe decided out (fm decide)` → Foreman now finds its own work on a drained queue and works it; criteria 1 and 4 amended (no board probe, friction added) [tree 007018833231] (2026-10-15T21:36:03Z)
- (audit adversary) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 9 findings, 8 fixed test-first, board probe decided out (fm decide)` → manifest dependency names are filtered to plain package names before any brief text; scout reads only cached data in the hook [tree 007018833231] (2026-10-15T21:36:03Z)
- (audit edge) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 9 findings, 8 fixed test-first, board probe decided out (fm decide)` → doctor JSON shape, --dry writes nothing, DST-safe source age, gap inside 30 min, an answer isn't a drain [tree 007018833231] (2026-10-15T21:36:03Z)
- (audit operator) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 9 findings, 8 fixed test-first, board probe decided out (fm decide)` → each real run is a scout ledger event with captures and probe errors; slow probes run in the session (asked once per 6 h), not detached [tree 007018833231] (2026-10-15T21:36:03Z)
- (audit maintainer) `one fm-reviewer pass (intent, adversary, edge, operator, maintainer): 9 findings, 8 fixed test-first, board probe decided out (fm decide)` → one module, probes as (name, fn) pairs; a new probe is one function and one list entry [tree 007018833231] (2026-10-15T21:36:03Z)
## Log
- 2026-10-15T20:53:31Z created
- 2026-10-15T20:57:11Z steer: playbooks too, MCP, LSP, everything — THE plugin; super fast, efficient, least token use; the user shouldn't need to ask for any of it
- 2026-10-15T21:09:26Z planned from capture
- 2026-10-15T21:10:06Z criterion 1 text: fm scout runs zero-token probes and captures each finding once (deduplicated by a probe key, also against dropped and closed items) with source scout and its evidence; fm scout --dry lists without capturing → fm scout runs zero-token probes and captures each finding once under a per-probe key (cc:<version>, libgap:<deps>, doctor:<check>, friction:<week>, brainstorm:<week>, board:<cluster>), so a dropped key stays quiet and a new version is new; at most 3 captures a run, at most 5 open scout items, and at most one run per 30 min; each probe is time-limited and a failing one is logged and skipped, never cached as nothing; fm scout --dry lists without capturing
- 2026-10-15T21:10:06Z criterion 2 text: The Claude Code probe captures 'Adopt Claude Code X' when the published latest is newer than what's installed and Foreman's tested version; equal versions capture nothing; the network read is cached 12 h → The Claude Code probe compares the published latest (cached 12 h, successes only) with the installed version and Foreman's CC_TESTED constant (README states the same version, checked by a doc test): newer captures 'Adopt Claude Code X' (worked through the normal loop, the guard still gating any install); equal, offline, a timeout or a malformed answer capture nothing
- 2026-10-15T21:10:07Z criterion 4 text: A Stop with an empty queue under full autonomy and drive on runs scout and continues with what it found; with nothing found it stops quietly; fm night runs scout first → End to end: a Stop with an empty queue under full autonomy and drive on runs scout and the hook's answer names the item it found and continues; with nothing found it stops quietly; fm night runs scout first; brainstorm-due and board-leftover probes each capture in a fixture
- 2026-10-15T21:10:07Z second read (revise) addressed: loop bounds, per-probe keys, probe failure isolation, CC_TESTED source of truth, e2e criterion; scout only captures (sources refresh is the one action: a read-only data index); installs stay behind the guard
- 2026-10-15T21:17:01Z focused
- 2026-10-15T21:24:36Z step 2: board leftovers probe skipped: the board slate's clusters are all tasks already (T-0954..T-0963); friction added (weekly when none is scheduled)
- 2026-10-15T21:27:55Z step 4: no rules line: the rules file is at its 6000-char budget and the Stop hook's block reason already says to plan and work the find
- 2026-10-15T21:34:06Z criterion 1 text: fm scout runs zero-token probes and captures each finding once under a per-probe key (cc:<version>, libgap:<deps>, doctor:<check>, friction:<week>, brainstorm:<week>, board:<cluster>), so a dropped key stays quiet and a new version is new; at most 3 captures a run, at most 5 open scout items, and at most one run per 30 min; each probe is time-limited and a failing one is logged and skipped, never cached as nothing; fm scout --dry lists without capturing → fm scout runs zero-token probes and captures each finding once under a per-probe key (cc:<version>, libgap:<deps>, doctor:<check>, friction:<week>, brainstorm:<week>), so a dropped key stays quiet and a new version is new; at most 3 captures a run, at most 5 open scout items, and at most one run per 30 min; each probe's own I/O is time-limited and a failing one is logged (a scout ledger event) and skipped, never cached as nothing; fm scout --dry lists without capturing or writing — verify with `python3 plugin/tests/run.py -k Scout`
- 2026-10-15T21:34:06Z criterion 4 text: End to end: a Stop with an empty queue under full autonomy and drive on runs scout and the hook's answer names the item it found and continues; with nothing found it stops quietly; fm night runs scout first; brainstorm-due and board-leftover probes each capture in a fixture → End to end: a Stop when the queue drains under full autonomy and drive on runs scout and the hook's answer names the item it found and continues; with no quick find it asks once per 6 h for fm scout --slow; an answer to a question isn't a drain; fm night runs scout first; brainstorm-due and friction-due probes each capture in a fixture — verify with `python3 plugin/tests/run.py -k ScoutDrive`
- 2026-10-15T21:36:04Z done
- 2026-10-15T21:36:05Z committed 62478ad (9 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The idle-Stop loop has no stated bound. Scout captures an item, the drive works it, the queue drains, Stop fires, scout runs again. A probe that can't be satisfied, such as a failed "adopt Claude Code X" or a doctor finding the work doesn't fix, would loop forever and burn budget. Dedupe prev…
- HIGH: Several probes can trigger unreviewed, outward-facing or hard-to-reverse changes with no human in the loop. "Adopt Claude Code X" means upgrading the tool that runs Foreman itself. "Refresh sources" and "write stack cards" change the library. Full autonomy plus "no asking" is the stated inten…
- MEDIUM: Dedupe "also against dropped and closed items" is too coarse. If the user drops "Adopt Claude Code 2.4", the key should stay suppressed, but the next release (2.5) is a legitimately new finding. The same applies to library gaps, whose card list changes as dependencies change. If the probe k…
- MEDIUM: The acceptance criteria prove the mechanics but not the request. All four are unit tests of probes with fixtures, so none shows that Foreman finds work unprompted in a real run. The "brainstorm when dry" and "board leftovers" probes are in step 2 but in no criterion. The doctor and friction…
- MEDIUM: The network probe has unspecified failure behavior. The criteria cover the 12 h cache but not offline, a timeout, a malformed response, or a rate limit. A failing probe must not block Stop or abort the other probes, and a failure must not be cached for 12 h as "no update". — Run each probe …
- LOW: The "Foreman's tested version" comparison needs a defined source of truth, and the step order puts the failing tests first with no mention of the fixture design for time (7 d, 12 h) and for network access. — Name where the tested version lives. Inject the clock and the fetcher into the probes …
Verdict: revise — the design is sound and cheap, but it needs a loop bound, safe handling of the adopt and library-changing probes, and per-probe dedupe keys before tests are written.
## Dissent
- [ ] HIGH: The idle-Stop loop has no stated bound. Scout captures an item, the drive works it, the queue drains, Stop fires, scout runs again. A probe that can't be satisfied, such as a failed "adopt Claude Code X" or a doctor finding the work doesn't fix, would loop forever and burn budget. Dedupe prev…
- [ ] HIGH: Several probes can trigger unreviewed, outward-facing or hard-to-reverse changes with no human in the loop. "Adopt Claude Code X" means upgrading the tool that runs Foreman itself. "Refresh sources" and "write stack cards" change the library. Full autonomy plus "no asking" is the stated inten…
- [ ] MEDIUM: Dedupe "also against dropped and closed items" is too coarse. If the user drops "Adopt Claude Code 2.4", the key should stay suppressed, but the next release (2.5) is a legitimately new finding. The same applies to library gaps, whose card list changes as dependencies change. If the probe k…
- [ ] MEDIUM: The acceptance criteria prove the mechanics but not the request. All four are unit tests of probes with fixtures, so none shows that Foreman finds work unprompted in a real run. The "brainstorm when dry" and "board leftovers" probes are in step 2 but in no criterion. The doctor and friction…
- [ ] MEDIUM: The network probe has unspecified failure behavior. The criteria cover the 12 h cache but not offline, a timeout, a malformed response, or a rate limit. A failing probe must not block Stop or abort the other probes, and a failure must not be cached for 12 h as "no update". — Run each probe …
- [ ] LOW: The "Foreman's tested version" comparison needs a defined source of truth, and the step order puts the failing tests first with no mention of the fixture design for time (7 d, 12 h) and for network access. — Name where the tested version lives. Inject the clock and the fetcher into the probes …
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-0946 [FEATURE M, active, 3 steps] MCP: a great Foreman MCP server (state, stack library, zero-token instruments) and fm mcp new to wrap any process or CLI as a tested …
- research mission-20261015-154003: Request: have FM enforce some things so we don't rely on agents to do it themselves as they are inconsistent (context: 19 card-writer s…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- A hook's background child with stdout to DEVNULL hides its failures and its finds: ask the session to run it instead, ledger every run
## Files touched
- plugin/tests/test_scout.py
- plugin/lib/fmscout.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmnight.py
- plugin/tests/test_night.py
- MASTER.md
- README.md
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- CHANGELOG.md
