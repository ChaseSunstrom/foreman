---
id: T-1264
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/templates/CLAUDE.lite.md, README.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/tests/test_bench_family.py, plugin/tests/test_suite_hygiene.py, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-20T14:01:27Z
updated: 2026-10-23T13:06:34Z
base: a03046975777585cf04187b52892cd32ffcd47c8
base_tree: 9e69462a67ba06f96031e0b09ae7b70ba67b01b5
plan0_at: 2026-10-23T12:58:03Z
plan0_scope: [plugin/templates/CLAUDE.lite.md, README.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/tests/test_bench_family.py, plugin/tests/test_suite_hygiene.py, plugin/tests/test_docs.py, CHANGELOG.md]
verified: strong
---
# Foreman in one CLAUDE.md for people who won't install the plugin; sweep plugin/lib for lin
## Raw request
> Foreman in one CLAUDE.md for people who won't install the plugin; sweep plugin/lib for lines no test or session runs (brainstorm-20261020 C12)
## Interpretation
Two brainstorm ideas (C12). (1) People who won't install the plugin get Foreman's discipline as one CLAUDE.md of 40 lines or fewer, and the duel can measure what those rules alone are worth against full Foreman. (2) plugin/lib code nothing reaches: grounded with a scan of every function named nowhere but its def: 32 hits, 31 dispatched by name at run time (fmcodetui _on_EVENT, fminstr cmd_NAME, fmoutcomes _FLAG), one dead (fmguard._quoted, 2 lines). The premise (a large unreached share) is false for whole functions; line coverage needs coverage.py, which isn't installed and can't follow the suite's fm subprocesses cheaply.
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/templates/CLAUDE.lite.md is 40 lines or fewer, names no fm command, and covers brief, test first, evidence, one task, review and safety; the README points to it — verify with `python3 plugin/tests/run.py test_docs`
- [x] fm bench duel --vs snippet runs Claude with no plugins and that file as the worktree's CLAUDE.md against Foreman — verify with `python3 plugin/tests/run.py test_bench_family`
- [x] every plugin/lib function is named somewhere besides its def (dispatch by name counted); fmguard._quoted is gone — verify with `python3 plugin/tests/run.py test_suite_hygiene`
## Non-goals
## Approach (options → choice → why)
Complete version: the file, a README pointer, a duel arm (Foreman vs Claude with the file), a dead-function check that keeps the count at zero, the dead function removed. Options for (1): fm eject --snippet (needs the plugin installed, which the audience hasn't), a template file in the repo with a raw-URL curl line (chosen: reachable without installing, and the bench reads the same file), a site page (later, if asked). Options for (2): coverage.py report (not installed, subprocess-heavy suite), a sys.settrace pass (slow, same subprocess problem), a static name check as a hygiene test (chosen: cheap, runs in every gate, catches new dead functions). The paid three-way measurement waits for usage (82% weekly at 32% of the week).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the lite file, the snippet arm, the dead-function check
2. [x] the file and README line, the duel arm, the dead function removed, CHANGELOG
## Resume here
## Docs impact
plugin/templates/CLAUDE.lite.md (new: the rules in one file); README.md (When not to use Foreman: a line pointing to it, with the curl line and the duel); plugin/lib/fmcli.py (--vs snippet help); CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_suite_hygiene test_docs test_bench_family` → ✗ exit 1 · Ran 95 tests in 15.5s (30 classes, 16 at a time; slowest: Judged 15s, Duel 10s, Marathon 9s) / FAILED (3 classes) [ran] [tree 942cba3e2420] (2026-10-23T13:00:38Z)
- (step 1) `python3 plugin/tests/run.py test_suite_hygiene test_docs test_bench_family` → exit 0 · Ran 95 tests in 15.7s (30 classes, 16 at a time; slowest: Judged 16s, Duel 10s, Marathon 9s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:03:20Z)
- (step 2) `python3 plugin/tests/run.py test_suite_hygiene test_docs test_bench_family test_bench test_guard test_cli` → exit 0 · Ran 527 tests in 39.2s (155 classes, 16 at a time; slowest: Bench 39s, TaskLifecycle 28s, Judged 22s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:03:59Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 71 tests in 8.5s (18 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:04:09Z)
- (ac 2) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 18 tests in 15.0s (9 classes, 16 at a time; slowest: Judged 15s, Duel 9s, Marathon 8s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:04:24Z)
- (ac 3) `python3 plugin/tests/run.py test_suite_hygiene` → exit 0 · Ran 6 tests in 1.3s (3 classes, 16 at a time; slowest: UndefinedNames 1s, DeadFunctions 1s, SuiteHygiene 1s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:04:26Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 71 tests in 8.5s (18 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:05:01Z)
- (ac 2) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 18 tests in 14.9s (9 classes, 16 at a time; slowest: Judged 15s, Duel 9s, Marathon 8s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:05:01Z)
- (ac 3) `python3 plugin/tests/run.py test_suite_hygiene` → exit 0 · Ran 6 tests in 1.2s (3 classes, 16 at a time; slowest: UndefinedNames 1s, DeadFunctions 1s, SuiteHygiene 1s) / OK [ran] [tree e3f218fd2086] (2026-10-23T13:05:01Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the rules file names no fm command (tested) and reads as plain rules; the snippet arm is the bare arm plus the file appended to the worktree's CLAUDE.md, so the guard and budget still apply; the site and fm bench repro read only duel-none files, so a snippet duel never shows as a no-plugins duel; the dead-function test's exemptions each end when their dispatch code goes` → people who won't install get the discipline in 33 lines, the duel can measure it, and dead functions can't pile up again [tree e3f218fd2086] (2026-10-23T13:05:01Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the rules file names no fm command (tested) and reads as plain rules; the snippet arm is the bare arm plus the file appended to the worktree's CLAUDE.md, so the guard and budget still apply; the site and fm bench repro read only duel-none files, so a snippet duel never shows as a no-plugins duel; the dead-function test's exemptions each end when their dispatch code goes` → a case base with its own CLAUDE.md keeps it (the rules are appended); a plugin revision without the file fails that case, not the run; a rival plugin and --vs snippet together are refused; a function named only in a comment or doc counts as named (conservative: fewer false alarms) [tree e3f218fd2086] (2026-10-23T13:05:01Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the rules file names no fm command (tested) and reads as plain rules; the snippet arm is the bare arm plus the file appended to the worktree's CLAUDE.md, so the guard and budget still apply; the site and fm bench repro read only duel-none files, so a snippet duel never shows as a no-plugins duel; the dead-function test's exemptions each end when their dispatch code goes` → people who won't install get the discipline in 33 lines, the duel can measure it, and dead functions can't pile up again [tree e3f218fd2086] (2026-10-23T13:05:50Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the rules file names no fm command (tested) and reads as plain rules; the snippet arm is the bare arm plus the file appended to the worktree's CLAUDE.md, so the guard and budget still apply; the site and fm bench repro read only duel-none files, so a snippet duel never shows as a no-plugins duel; the dead-function test's exemptions each end when their dispatch code goes` → a case base with its own CLAUDE.md keeps it (the rules are appended); a plugin revision without the file fails that case, not the run; a rival plugin and --vs snippet together are refused; a function named only in a comment or doc counts as named (conservative: fewer false alarms) [tree e3f218fd2086] (2026-10-23T13:05:50Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the rules file names no fm command (tested) and reads as plain rules; the snippet arm is the bare arm plus the file appended to the worktree's CLAUDE.md, so the guard and budget still apply; the site and fm bench repro read only duel-none files, so a snippet duel never shows as a no-plugins duel; the dead-function test's exemptions each end when their dispatch code goes` → the guard change only deletes fmguard._quoted, a function nothing called or named (grep and the new test agree); no check, pattern or category changed, and test_guard passes unchanged [tree e3f218fd2086] (2026-10-23T13:05:50Z)
## Log
- 2026-10-20T14:01:27Z created
- 2026-10-23T12:57:58Z set tier=M, scope=['plugin/templates/CLAUDE.lite.md', 'README.md', 'plugin/lib/fmbench.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmguard.py', 'plugin/tests/test_bench_family.py', 'plugin/tests/test_suite_hygiene.py', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-23T12:58:02Z focused
- 2026-10-23T13:06:32Z done
- 2026-10-23T13:06:34Z committed 24748396 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1340 [FEATURE M, done, 1 steps] Fm code follow-ups (R22+U22): fm code --after T-ID "<follow-up>" (and Enter after a close — lesson: Before adding an attribute to a cla…
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
- similar finished tasks took 1–6 steps
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_cli.py, plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, README.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/tests/test_bench_family.py, plugin/tests/test_docs.py; re-ground the plan against them before editing
## Lessons
- Grounding the brainstorm's dead-code premise with a ten-line scan (1 dead function of 32 hits) turned an M deletion sweep into a hygiene test
## Plan gaps
- failed first: step 1 red tests: the lite file, the snippet arm, the dead-function check
## Files touched
- plugin/tests/test_bench_family.py
- plugin/tests/test_docs.py
- plugin/tests/test_suite_hygiene.py
- CHANGELOG.md
- README.md
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmguard.py
- plugin/templates/CLAUDE.lite.md
