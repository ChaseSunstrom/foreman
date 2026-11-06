---
id: T-1870
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-28T23:48:11Z
base: 47c2526ff41307e58090c9a9d9ddb1ab6a70e2f5
base_tree: 9bc8e2181eac77384a1d71e098cef05beb930578
plan0_at: 2026-10-28T23:33:39Z
plan0_scope: []
verified: strong
---
# Fm inbox ticket --post T-xxxx posts the closing commit back to its source issue
## Raw request
> FEATURE: fm inbox ticket --post T-xxxx posts the closing commit back to the source issue as one comment (GitHub via gh, Jira, Linear), and fm task finish of a fetched ticket names that command
> CONTEXT: forever loop round 5 ("Post the close link back to the source ticket"). Outward: only on the explicit --post, never automatic.
## Interpretation
After a ticket fetched by fm inbox ticket (or captured by fm inbox gh) is done and committed, the user can post the closing commit back to that issue with one explicit command. Never automatic.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm inbox ticket --post ID posts one comment naming the closing commit to the brief's source issue (GitHub via gh, Jira, Linear), refuses a brief with no source, not done, no commit or already posted, and fm task finish of a fetched ticket names the command — verify with `python3 plugin/tests/run.py test_inbox_more test_execution`
## Non-goals
## Approach (options → choice → why)
Options: (a) post automatically on finish — rejected, outward and irreversible; (b) a separate fm ticket post verb — more surface; (c) --post on fm inbox ticket, explicit, with a hint at finish — chosen: the verb that fetched the ticket posts back. Body is the commit sha and task id only: no untrusted text goes back out.
## Risks and rollback
Outward and irreversible per call: only on --post, at most once per brief (a log line marks it), the body carries no untrusted text. Rollback: delete the comment on the tracker; git revert the commit.
## Execution prompt
## Steps
1. [x] Failing tests: PostBack (GitHub, inbox gh brief, Jira, Linear, refusals, forged title, flag rule) and the finish hint
2. [x] Implement: _gh split, _tracker shared by fetch and post, ticket_source, post_ticket, --post flag, finish hint
3. [x] Docs: CHANGELOG, MASTER, backlog.md, fm help
## Resume here
<!-- auto -->
- 2026-10-28T23:46:21Z steps 3/3 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_execution.py, plugin/tests/test_inbox_more.py
- touched since last checkpoint: plugin/tests/test_execution.py, CHANGELOG.md, MASTER.md
- failures met: assertionerror: tuples differ: ('pos[0 chars]anted, once pushed): fm inbox ticket --post …; fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hide…
## Docs impact
~/.claude/foreman/plugin/commands/backlog.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_inbox_more.PostBack test_execution.BoardClose` → red as expected (exit 1) · Ran 10 tests in 4.5s (2 classes, 16 at a time; slowest: BoardClose 4s, PostBack 1s) / FAILED (2 classes) [ran] [tree 6edb87d46928] (2026-10-28T23:35:09Z)
- (step 1) `python3 plugin/tests/run.py test_inbox_more.PostBack test_execution.BoardClose` → exit 0 · Ran 10 tests in 2.9s (2 classes, 16 at a time; slowest: BoardClose 3s, PostBack 0s) / OK [ran] [tree 9db9d69079f4] (2026-10-28T23:37:24Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_execution` → exit 0 · Ran 42 tests in 4.9s (16 classes, 16 at a time; slowest: Served 5s, BoardClose 3s, Swipe 2s) / OK [ran] [tree 9db9d69079f4] (2026-10-28T23:37:29Z)
- (step 3) `grep -c 'inbox ticket --post' CHANGELOG.md MASTER.md plugin/commands/backlog.md` → exit 0 · MASTER.md:1 / plugin/commands/backlog.md:1 [ran] [tree 5ca1de191a7e] (2026-10-28T23:37:45Z)
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → red as expected (exit 1) · Ran 29 tests in 4.7s (8 classes, 16 at a time; slowest: Served 4s, Swipe 2s, Pick 2s) / FAILED (1 classes) [ran] [tree c7d694227002] (2026-10-28T23:42:02Z)
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → exit 0 · Ran 29 tests in 4.7s (8 classes, 16 at a time; slowest: Served 4s, Swipe 2s, Pick 2s) / OK [ran] [tree da307928c333] (2026-10-28T23:42:59Z)
- (step 3) `grep -c 'the post failed' MASTER.md` → exit 0 · 1 [ran] [tree da307928c333] (2026-10-28T23:42:59Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_execution` → exit 0 · Ran 43 tests in 4.9s (16 classes, 16 at a time; slowest: Served 5s, BoardClose 3s, Swipe 2s) / OK [ran] [tree da307928c333] (2026-10-28T23:43:08Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmeco.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.0    42.1     150  [0] / SessionEnd                  35.2    38.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree da307928c333] (2026-10-28T23:47:04Z)
- (ac 1) `python3 plugin/tests/run.py test_inbox_more test_execution` → exit 0 · Ran 43 tests in 4.9s (16 classes, 16 at a time; slowest: Served 5s, BoardClose 3s, Swipe 2s) / OK [ran] [tree da307928c333] (2026-10-28T23:47:44Z)
- (audit intent) `one fm-reviewer pass (research/T-1870-review.md): 4 findings fixed test-first — concurrent/retried posts claimed under the lock, hint and post agree on closing_sha, unpushed sha refused, Jira host documented` → posts one comment naming the closing commit, only on explicit --post, only once pushed [tree da307928c333] (2026-10-28T23:47:44Z)
- (audit adversary) `one fm-reviewer pass (research/T-1870-review.md): 4 findings fixed test-first — concurrent/retried posts claimed under the lock, hint and post agree on closing_sha, unpushed sha refused, Jira host documented` → ticket text goes through plain/defang/redact; token only to the configured host via the no-redirect opener; a racing second run finds the claim and refuses [tree da307928c333] (2026-10-28T23:47:44Z)
- (audit edge) `one fm-reviewer pass (research/T-1870-review.md): 4 findings fixed test-first — concurrent/retried posts claimed under the lock, hint and post agree on closing_sha, unpushed sha refused, Jira host documented` → a failed post frees a retry; a timed-out post warns it may have landed; no source, not done, no sha, unpushed all refuse before any network call [tree da307928c333] (2026-10-28T23:47:44Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-28T23:33:31Z set title=Fm inbox ticket --post T-xxxx posts the closing commit back to its source issue
- 2026-10-28T23:33:38Z focused
- 2026-10-28T23:48:09Z done
- 2026-10-28T23:48:11Z committed 1188c460 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1869 [FEATURE M, done, 4 steps] Fm inbox ticket fetches GitHub issues too (gh:OWNER/REPO#N, a github.com issue URL, or #N — lesson: Snapshot tests must strip every tim…
- T-1859 [FEATURE M, done, 3 steps] Fm inbox ticket: fetch a Jira or Linear issue by key, not only pasted text — lesson: An outbound request carrying a token goes through …
- research T-1869-review: Verdict:** changes needed. Two MEDIUM findings: a duplicate-brief path and an `fm inbox ticket #7` call that bash silently breaks. The rest is LO…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
## Lessons
- an outward write needs a claim under the lock before the network call, and a timeout is not a failure: say it may have landed
## Files touched
- plugin/tests/test_inbox_more.py
- plugin/tests/test_execution.py
- plugin/lib/fmcli.py
- plugin/lib/fmeco.py
- CHANGELOG.md
- MASTER.md
- plugin/commands/backlog.md
