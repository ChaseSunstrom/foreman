---
id: T-1876
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/tests/test_settings_extras.py, plugin/tests/test_settings_room.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-29T02:49:01Z
base: fc8b93220af8208aff8802692871b3bab5d195b6
base_tree: f514cce4598fb0ebb23e5bd1765a0f8d866a830d
plan0_at: 2026-10-29T02:41:14Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/tests/test_settings_extras.py, plugin/tests/test_settings_room.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Fm settings newcomer offers the saved macros, and fm settings log suggests a macro for a k
## Raw request
> FEATURE: fm settings newcomer offers the saved macros, and fm settings log suggests a macro for a key set by hand 3+ times
> CONTEXT: forever loop round 5 ("Offer macros inside fm settings newcomer", "Surface hidden settings verbs when the user repeats a change by hand").
## Interpretation
fm settings log ends with a tip when one key was set by hand 3+ times (the macro command that saves it, unless a macro already holds that value); fm settings newcomer names a saved macro that finishes a stuck step.
## Assumptions (confidence)
## Acceptance criteria
- [x] log tip and newcomer macro hint, tested — verify with `python3 plugin/tests/run.py test_settings_extras test_settings_room`
## Non-goals
## Approach (options → choice → why)
Options: a new verb; a hook nudge; a tail on the existing log and newcomer outputs. Choice: the tail — no new surface, read-only, reuses macros() and _norm.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests red: log tip, newcomer macro
2. [x] _macro_tips and _reaches; green
3. [x] CHANGELOG and MASTER
## Resume here
<!-- auto -->
- 2026-10-29T02:47:13Z steps 3/3 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmsettings.py, plugin/tests/test_settings_extras.py, plugin/tests/test_settings_room.py
- touched since last checkpoint: plugin/tests/test_settings_extras.py, plugin/tests/test_settings_room.py, CHANGELOG.md, MASTER.md, plugin/lib/fmsettings.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1898t.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1898i.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/hero_load.sh
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings_extras test_settings_room` → red as expected (exit 1) · Ran 35 tests in 4.4s (10 classes, 16 at a time; slowest: Page 4s, Replay 2s, Review 2s) / FAILED (2 classes) [ran] [tree 8399cc1f4e1e] (2026-10-29T02:41:20Z)
- (step 2) `python3 plugin/tests/run.py test_settings_extras test_settings_room` → exit 0 · Ran 35 tests in 4.5s (10 classes, 16 at a time; slowest: Page 4s, Log 2s, Review 2s) / OK [ran] [tree 1e0c27d7abaa] (2026-10-29T02:41:30Z)
- (step 3) `grep -c T-1876 CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:2 [ran] [tree 1e0c27d7abaa] (2026-10-29T02:41:37Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmsettings.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.4    49.1     150  [0] / SessionEnd                  35.7    37.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/forem [ran] [tree 1e0c27d7abaa] (2026-10-29T02:48:35Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_extras test_settings_room` → exit 0 · Ran 35 tests in 3.9s (10 classes, 16 at a time; slowest: Page 4s, Log 1s, Replay 1s) / OK [ran] [tree 1e0c27d7abaa] (2026-10-29T02:48:48Z)
- (audit intent) `Self-review of the diff: newcomer offer lists saved macros, settings log suggests a macro only for a key set 3+ times; tests cover both and the no-macro case` → newcomer sees saved macros; log suggests one for a repeated key — both tested [tree 1e0c27d7abaa] (2026-10-29T02:48:48Z)
- (audit edge) `Self-review of the diff: newcomer offer lists saved macros, settings log suggests a macro only for a key set 3+ times; tests cover both and the no-macro case` → no macros saved → no offer line; key set fewer than 3 times → no suggestion [tree 1e0c27d7abaa] (2026-10-29T02:48:48Z)
- (audit self) `Self-review of the diff: newcomer offer lists saved macros, settings log suggests a macro only for a key set 3+ times; tests cover both and the no-macro case` → no findings [tree 1e0c27d7abaa] (2026-10-29T02:48:48Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-29T00:38:45Z set tier=S, scope=['plugin/lib/fmsettings.py', 'plugin/tests/test_settings_extras.py', 'plugin/tests/test_settings_room.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T00:53:51Z set status=planned
- 2026-10-29T01:18:55Z plan re-read: only CHANGELOG.md moved; drafts re-applied clean in a trial tree with all queued drafts, tests green
- 2026-10-29T02:41:13Z focused
- 2026-10-29T02:48:59Z done
- 2026-10-29T02:49:01Z committed e44fb21a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1658 [FEATURE M, done, 5 steps] Settings extras: log, macro, duel, replay (what-breaks), words-to-diff, undo that adapts — lesson: CLI write tests need a pty: in_claud…
- research T-1661-review: Verdict: changes needed.** The three acceptance criteria are implemented. Pressing Enter in a served number field writes the wrong value, and `--…
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- decision 2026-10-20: T-1276 trims no fm verb: measured right, fm-only command output is 0.9% of what entered the context over three days (the 3.5% counted test runs chai…
- likely tests for the scope: plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-28): CHANGELOG.md, MASTER.md; re-ground the plan against them before editing
## Lessons
- Suggest a macro from the settings log itself: the repeats are already recorded there
## Files touched
- plugin/tests/test_settings_extras.py
- plugin/tests/test_settings_room.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmsettings.py
