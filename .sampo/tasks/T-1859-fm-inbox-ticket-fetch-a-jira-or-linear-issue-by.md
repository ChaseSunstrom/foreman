---
id: T-1859
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T20:01:58Z
updated: 2026-10-28T22:58:34Z
base: fc2dd2e3e1d89da9784c61b24f874055faa9740e
base_tree: 42f9e5555cf75cc43d52be2943a95df65e053b59
plan0_at: 2026-10-28T22:47:59Z
plan0_scope: []
verified: strong
---
# Fm inbox ticket: fetch a Jira or Linear issue by key, not only pasted text
## Raw request
> fm inbox ticket: fetch a Jira or Linear issue by key, not only pasted text
## Interpretation
fm inbox ticket KEY|jira:KEY|linear:KEY|URL: when the argument isn't a file, fetch the issue from Jira (REST v2) or Linear (GraphQL) with env credentials and feed it to the existing ticket pipeline (type from labels/issue type, criteria from checkboxes, redacted, defanged, quoted); the same issue twice makes one brief.
## Assumptions (confidence)
## Acceptance criteria
- [x] a Jira key or URL and a Linear URL become one brief each, with the right auth sent only to the configured host; each failure is said with no token in it — verify with `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity`
## Non-goals
## Approach (options → choice → why)
Options: (1) stdlib urllib fetch turned into the paste text, reusing inbox_ticket unchanged downstream; (2) a jira/linear Python client dependency; (3) shell out to gh-like CLIs (jira-cli, linear-cli). Choice: 1 — no dependency, one small function per service, the untrusted-text handling is reused as is. Credentials only ever go to JIRA_URL's host or api.linear.app; a Jira URL on another host is refused.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests (Ticket class)
2. [x] ticket_ref, fetch_ticket, inbox_ticket wiring, backlog.md
3. [x] docs: MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-28T22:50:49Z step 1/3: failing tests (Ticket class)
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/tests/test_inbox_more.py
- touched since last checkpoint: plugin/tests/test_inbox_more.py, plugin/commands/backlog.md, plugin/lib/fmeco.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py
## Docs impact
plugin/lib/fmcli.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → ✗ exit 1 · Ran 19 tests in 6.7s (6 classes, 16 at a time; slowest: Served 6s, Swipe 4s, Pick 3s) / FAILED (1 classes) [ran] [tree e64a5e559f44] (2026-10-28T22:48:19Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity` → exit 0 · Ran 45 tests in 9.7s (11 classes, 16 at a time; slowest: Reverify 9s, Extras 9s, Served 7s) / OK [ran] [tree 0db802b7e679] (2026-10-28T22:49:01Z)
- (step 3) `grep -c 'T-1859' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree 0db802b7e679] (2026-10-28T22:49:02Z)
- (step 1) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity` → exit 0 · Ran 45 tests in 5.3s (11 classes, 16 at a time; slowest: Extras 5s, Reverify 5s, Served 5s) / OK [ran] [tree 6b7ea5e6dc2a] (2026-10-28T22:52:59Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity` → exit 0 · Ran 45 tests in 5.3s (11 classes, 16 at a time; slowest: Extras 5s, Reverify 5s, Served 5s) / OK [ran] [tree 6b7ea5e6dc2a] (2026-10-28T22:53:04Z)
- (step 3) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity` → exit 0 · Ran 45 tests in 5.3s (11 classes, 16 at a time; slowest: Extras 5s, Reverify 5s, Served 5s) / OK [ran] [tree 6b7ea5e6dc2a] (2026-10-28T22:53:10Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmeco.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                39.2    41.5     150  [0] / SessionEnd                  34.0    35.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 6b7ea5e6dc2a] (2026-10-28T22:57:03Z)
- (ac 1) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity` → exit 0 · Ran 45 tests in 5.3s (11 classes, 16 at a time; slowest: Extras 5s, Reverify 5s, Served 4s) / OK [ran] [tree 6b7ea5e6dc2a] (2026-10-28T22:57:24Z)
- (audit intent) `one fm-reviewer pass (changes needed: redirect-follow MEDIUM, credential echo, urlsplit crash, dedupe on edits, weak evil-host test), all fixed test-first; full gates green` → a key, jira:/linear:KEY or issue URL becomes the same planned brief a paste would, fetched with env tokens, never asked for [tree 6b7ea5e6dc2a] (2026-10-28T22:57:24Z)
- (audit adversary) `one fm-reviewer pass (changes needed: redirect-follow MEDIUM, credential echo, urlsplit crash, dedupe on edits, weak evil-host test), all fixed test-first; full gates green` → a 3xx never carries the token (fmmodels._OPENER), other hosts refused before any send, errors print hostnames only, ticket text defanged and redacted [tree 6b7ea5e6dc2a] (2026-10-28T22:57:24Z)
- (audit edge) `one fm-reviewer pass (changes needed: redirect-follow MEDIUM, credential echo, urlsplit crash, dedupe on edits, weak evil-host test), all fixed test-first; full gates green` → http://[x is a file name, both/no trackers said, empty labels omitted, edited ticket is a new brief [tree 6b7ea5e6dc2a] (2026-10-28T22:57:24Z)
- (audit intent) `one fm-reviewer pass (changes needed: redirect-follow MEDIUM, credential echo, urlsplit crash, dedupe on edits, weak evil-host test), all fixed test-first; full gates green` → a key, jira:/linear:KEY or issue URL becomes the same planned brief a paste would, fetched with env tokens, never asked for [tree c92e4dc17a13] (2026-10-28T22:58:07Z)
- (audit adversary) `one fm-reviewer pass (changes needed: redirect-follow MEDIUM, credential echo, urlsplit crash, dedupe on edits, weak evil-host test), all fixed test-first; full gates green` → a 3xx never carries the token (fmmodels._OPENER), other hosts refused before any send, errors print hostnames only, ticket text defanged and redacted [tree c92e4dc17a13] (2026-10-28T22:58:07Z)
- (audit edge) `one fm-reviewer pass (changes needed: redirect-follow MEDIUM, credential echo, urlsplit crash, dedupe on edits, weak evil-host test), all fixed test-first; full gates green` → http://[x is a file name, both/no trackers said, empty labels omitted, edited ticket is a new brief [tree c92e4dc17a13] (2026-10-28T22:58:07Z)
## Log
- 2026-10-28T20:01:58Z created
- 2026-10-28T22:47:59Z focused
- 2026-10-28T22:58:32Z done
- 2026-10-28T22:58:34Z committed c3d766f1 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1664-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** One MEDIUM and one LOW finding concern un…
- T-1606 [SECURITY M, done, 5 steps] Guard trust: pasted secrets, approval fatigue, fm doctor --wrong (from T-1553) — lesson: A claim like 'kept redacted' must be tested b…
- T-1664 [FEATURE M, done, 4 steps] Backlog extras: good-first list, deferred swipe, learned priorities, spike rule, ticket planner — lesson: a flag a sub-action doesn't r…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
## Lessons
- An outbound request carrying a token goes through the no-redirect opener (fmmodels._OPENER); urlopen copies Authorization to a redirect target
## Plan gaps
- failed first: step 1 failing tests (Ticket class)
## Files touched
- plugin/tests/test_inbox_more.py
- plugin/commands/backlog.md
- plugin/lib/fmeco.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
