---
id: T-1872
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-29T00:08:14Z
base: b2e26b10baa9e4fb8be4cb67efd0330a0a40dfe6
base_tree: adef9ff4c5dba83b1769ccc2e7c37240eed31bf9
plan0_at: 2026-10-28T23:59:34Z
plan0_scope: []
verified: strong
---
# Fm inbox prefer --why T-xxxx explains a learned priority (the title words that lift or sin
## Raw request
> FEATURE: fm inbox prefer --why T-xxxx explains a learned priority (the title words that lift or sink it, one line each), and fm triage opens the right backlog surface (TTY: the swipe loop; --serve: the page; else the good-first list)
> CONTEXT: forever loop round 5 ("Explain why one backlog item outranks another", "Add one fm triage entry that picks the backlog surface").
## Interpretation
Two additions. (1) fm inbox prefer --why ID: one line per title word of that inbox item with a learned weight, strongest first, saying whether it lifts or sinks it, then the tilt they add (capped at ±2); none learned says so. (2) fm triage: one entry to the backlog that picks the surface: --serve the swipe page, a terminal the swipe loop, otherwise (pipe, --json, Claude Code) the good-first list.
## Assumptions (confidence)
## Acceptance criteria
- [x] prefer --why names each weighted title word and the tilt; fm triage picks serve, the loop or the first list — verify with `python3 plugin/tests/run.py test_inbox_more test_docs`
## Non-goals
Explaining urgency/type ranking; a triage page of its own.
## Approach (options → choice → why)
Options: (a) both as new fm inbox sources; (b) --why as a prefer flag plus fm triage as a thin verb that sets source and calls cmd_inbox; (c) triage as an ALIASES entry. Choice: (b) — reuses cmd_inbox's guards and output whole; an alias can't branch on TTY. Explanation reads c.pref_words and c.learned_weights, the same terms title_tilt sums, so it can't drift from the order.
## Risks and rollback
Read-only and additive; git revert.
## Execution prompt
## Steps
1. [x] Tests first: --why lines and tilt, none learned, not in the inbox; triage routing
2. [x] prefer_why, --why flag, cmd_triage and its parser entry
3. [x] Docs: CHANGELOG, MASTER, backlog.md (why and triage)
## Resume here
<!-- auto -->
- 2026-10-29T00:04:09Z steps 3/3 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_inbox_more.py
- touched since last checkpoint: plugin/lib/fmcli.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1872d.txt, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmeco.py, plugin/tests/test_inbox_more.py, CHANGELOG.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1874t.txt
## Docs impact
~/.claude/foreman/plugin/commands/backlog.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → red as expected (exit 1) · Ran 37 tests in 8.3s (9 classes, 16 at a time; slowest: Served 8s, Swipe 7s, App 4s) / FAILED (2 classes) [ran] [tree 4231d40b5a26] (2026-10-28T23:59:44Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more` → exit 0 · Ran 37 tests in 8.7s (9 classes, 16 at a time; slowest: Served 8s, Swipe 7s, Prefer 4s) / OK [ran] [tree 1b5183b97608] (2026-10-29T00:00:09Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 74 tests in 11.9s (18 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 3s, Site 1s) / OK [ran] [tree 185affcf2d38] (2026-10-29T00:00:43Z)
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → red as expected (exit 1) · Ran 37 tests in 10.6s (9 classes, 16 at a time; slowest: Served 10s, Swipe 8s, App 4s) / FAILED (1 classes) [ran] [tree 73accf6c548c] (2026-10-29T00:02:25Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_docs` → exit 0 · Ran 111 tests in 9.4s (27 classes, 16 at a time; slowest: Fences 9s, Served 6s, Swipe 4s) / OK [ran] [tree 4e9ba681e922] (2026-10-29T00:02:35Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmeco.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.9    43.9     150  [0] / SessionEnd                  37.7    41.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree ad2e53510df2] (2026-10-29T00:07:20Z)
- (ac 1) `python3 plugin/tests/run.py test_inbox_more test_docs` → exit 0 · Ran 111 tests in 9.4s (27 classes, 16 at a time; slowest: Fences 9s, Served 6s, Swipe 4s) / OK [ran] [tree ad2e53510df2] (2026-10-29T00:07:45Z)
- (audit intent) `one fm-reviewer pass (research/T-1872-review.md); 2 findings fixed test-first, 2 LOW skipped` → the --why lines add up to the tilt before its cap; triage picks the swipe loop, the page or the list by TTY and --serve [tree ad2e53510df2] (2026-10-29T00:07:45Z)
- (audit adversary) `one fm-reviewer pass (research/T-1872-review.md); 2 findings fixed test-first, 2 LOW skipped` → titles go through c.plain; an id outside the inbox is refused, no traceback [tree ad2e53510df2] (2026-10-29T00:07:45Z)
- (audit edge) `one fm-reviewer pass (research/T-1872-review.md); 2 findings fixed test-first, 2 LOW skipped` → --json on a TTY gives the list; --why with a second item, --reset or pick is refused [tree ad2e53510df2] (2026-10-29T00:07:45Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-28T23:59:33Z focused
- 2026-10-29T00:08:12Z done
- 2026-10-29T00:08:14Z committed 5ca995bd (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-1664 [FEATURE M, done, 4 steps] Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner — lesson: a flag a sub-action doesn't r…
- research T-1866-review: Verdict:** approve with nits. All four acceptance criteria are met in the code, and I found nothing HIGH. I read the diff and the surrounding cod…
- decision 2026-10-09: user added C078/C079/C081/C082/C083/C084 on the punch-list page: T-0443, T-0444, T-0463, T-0481, T-0482, T-0574 set priority high, built right after…
## Lessons
- Explaining a score needs the same units as the score: the word lines printed raw weights while the tilt is half of them; a test that sums the lines to the head caught it.
## Files touched
- plugin/tests/test_inbox_more.py
- plugin/lib/fmcli.py
- plugin/lib/fmeco.py
- CHANGELOG.md
- MASTER.md
- plugin/commands/backlog.md
