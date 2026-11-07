---
id: T-1869
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-28T23:32:20Z
base: 5d776079bb108fa536be030cdb087eda4737f0e5
base_tree: a1f7a82214fc507048538ffa05cbdb3e3400f0b1
plan0_at: 2026-10-28T23:20:35Z
plan0_scope: []
verified: strong
---
# Fm inbox ticket fetches GitHub issues too (gh:OWNER/REPO#N, a github.com issue URL, or #N
## Raw request
> FEATURE: fm inbox ticket fetches GitHub issues too (gh:OWNER/REPO#N, a github.com issue URL, or #N in a repo with a GitHub remote) through the user's own gh CLI, and a re-fetch of a changed issue refreshes its unstarted brief in place instead of making a second one
> CONTEXT: forever loop round 5 (brainstorm-20261028-175927: "Add GitHub issues", "Refresh a fetched ticket brief instead of making a second one"). A started or closed brief still gets a new one.
## Interpretation
fm inbox ticket takes a GitHub issue: gh:OWNER/REPO#N, https://github.com/OWNER/REPO/issues/N, or #N (this repo's remote), fetched with the user's own gh (gh issue view --json), so no new token handling. Re-fetching an issue whose text changed refreshes its brief in place while that brief is captured (Raw request, title, criteria, steps, scope from the new text) or planned (Raw request and title only; the plan stays); a started or closed brief gets a new brief. The same text still dedupes.
## Assumptions (confidence)
## Acceptance criteria
- [x] gh refs fetch through gh issue view and a changed issue refreshes a captured/planned brief in place, a started/closed one gets a new brief — verify with `python3 plugin/tests/run.py test_inbox_more`
## Non-goals
## Approach (options → choice → why)
1) the GitHub REST API with GH_TOKEN (new credential path); 2) gh issue view, like fm inbox gh already uses gh issue list; 3) shell out to fm inbox gh and filter. Choice: 2 (no token in Foreman, same untrusted-text handling). Refresh: key the brief by 'CONTEXT: ticket SERVICE KEY ' without the hash, compare the hash, refresh by status; option of a separate refresh verb rejected (the user re-runs the same command).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: gh ref forms, gh fetch via a stub, refresh by status
2. [x] ticket_ref + fetch_ticket github; refresh in inbox_ticket
3. [x] docs: CHANGELOG, fm inbox help, backlog skill
4. [x] review fixes: inbox gh skips ticket briefs, the held text wins over a sibling, refresh rechecks status, tier, JSON new stays bool, comment URLs, '#7' quoted
## Resume here
<!-- auto -->
- 2026-10-28T23:30:24Z steps 4/4 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_inbox_more.py, plugin/tests/test_robustness.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1869b.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1869b.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/d1869b.txt, plugin/tests/test_inbox_more.py, CHANGELOG.md, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_robustness.py
## Docs impact
~/.claude/foreman/plugin/commands/backlog.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → red as expected (exit 1) · Ran 23 tests in 6.2s (7 classes, 16 at a time; slowest: Served 6s, Swipe 4s, Pick 3s) / FAILED (2 classes) [ran] [tree 2e089ec02a32] (2026-10-28T23:20:59Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_inbox test_eco` → exit 0 · Ran 52 tests in 8.2s (18 classes, 16 at a time; slowest: HarnessCanary 8s, Served 7s, InboxSpec 5s) / OK [ran] [tree af2a5ec4aa6c] (2026-10-28T23:21:48Z)
- (step 3) `grep -c 'gh:OWNER/REPO#N' CHANGELOG.md MASTER.md plugin/commands/backlog.md plugin/lib/fmcli.py` → exit 0 · plugin/commands/backlog.md:1 / plugin/lib/fmcli.py:1 [ran] [tree af2a5ec4aa6c] (2026-10-28T23:21:49Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmeco.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · SessionEnd                  61.8    70.7     150  [0] / machine busy (load 1.2 per core): judged by each hook's CPU time, not wall time (T-0805) (slower: 33.3 s vs a usual 20.8 s); [ran] [tree af2a5ec4aa6c] (2026-10-28T23:26:40Z)
- (step 4) `python3 plugin/tests/run.py test_inbox_more` → red as expected (exit 1) · Ran 24 tests in 4.6s (7 classes, 16 at a time; slowest: Served 4s, Swipe 2s, Pick 1s) / FAILED (1 classes) [ran] [tree 9cbe950633e9] (2026-10-28T23:26:52Z)
- (step 4) `python3 plugin/tests/run.py test_inbox_more test_robustness` → exit 0 · Ran 27 tests in 8.1s (8 classes, 16 at a time; slowest: Robustness 8s, Served 4s, Swipe 2s) / OK [ran] [tree 9bc8e2181eac] (2026-10-28T23:27:38Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmeco.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.1    43.0     150  [0] / SessionEnd                  35.0    36.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 9bc8e2181eac] (2026-10-28T23:31:38Z)
- (ac 1) `python3 plugin/tests/run.py test_inbox_more` → exit 0 · Ran 24 tests in 4.6s (7 classes, 16 at a time; slowest: Served 4s, Swipe 2s, Pick 1s) / OK [ran] [tree 9bc8e2181eac] (2026-10-28T23:31:53Z)
- (audit intent) `one fm-reviewer pass: 8 findings fixed test-first (inbox gh/ticket dedupe both ways, comment URLs, refresh race, held-text sibling, quoted #N, JSON booleans, closed tickets), 1 limit documented` → #N, gh:OWNER/REPO#N and github.com URLs fetch through gh and plan one brief, matching Jira/Linear [tree 9bc8e2181eac] (2026-10-28T23:31:53Z)
- (audit adversary) `one fm-reviewer pass: 8 findings fixed test-first (inbox gh/ticket dedupe both ways, comment URLs, refresh race, held-text sibling, quoted #N, JSON booleans, closed tickets), 1 limit documented` → quoted issue lines start with '> ', so an issue body can't forge a CONTEXT: ticket line; gh runs with the user's own auth, no token handled [tree 9bc8e2181eac] (2026-10-28T23:31:53Z)
- (audit edge) `one fm-reviewer pass: 8 findings fixed test-first (inbox gh/ticket dedupe both ways, comment URLs, refresh race, held-text sibling, quoted #N, JSON booleans, closed tickets), 1 limit documented` → comment-link URLs, an unquoted #7 eaten by bash, a brief started between scan and refresh, done briefs, inbox gh run before or after ticket [tree 9bc8e2181eac] (2026-10-28T23:31:53Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-28T23:20:34Z focused
- 2026-10-28T23:27:18Z steer: widened to plugin/tests/test_robustness.py — T-1879's snapshot kept the 1-second _Generated stamp, so a tidy run twice across a second boundary failed on 3.12 and blocked the push
- 2026-10-28T23:32:19Z done
- 2026-10-28T23:32:20Z committed 47c2526f (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1859-review: Verdict:** changes needed. One MEDIUM finding breaks the acceptance criterion's "auth sent only to the configured host". I read the code only. No…
- T-1859 [FEATURE M, done, 3 steps] Fm inbox ticket: fetch a Jira or Linear issue by key, not only pasted text — lesson: An outbound request carrying a token goes through …
- research mission-20261028-175912: Request: forever loop round 5: improve past everything shipped
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- the similar finished task took 3 steps
## Lessons
- Snapshot tests must strip every timestamp; a one-second _Generated stamp flaked only on the slower 3.12 run
## Plan gaps
- added late: review fixes: inbox gh skips ticket briefs, the held text wins over a sibling, refresh rechecks status, tier, JSON new …
## Files touched
- plugin/tests/test_inbox_more.py
- plugin/lib/fmcli.py
- plugin/lib/fmeco.py
- CHANGELOG.md
- MASTER.md
- plugin/commands/backlog.md
- plugin/tests/test_robustness.py
