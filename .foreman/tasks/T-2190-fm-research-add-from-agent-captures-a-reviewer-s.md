---
id: T-2190
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T16:49:21Z
updated: 2026-10-30T17:42:08Z
base: 0073b9b02b727850e022ff0014ec1de1b20e69b1
base_tree: cf4fa6c766541339781627336fc45b06472972be
plan0_at: 2026-10-30T17:34:54Z
plan0_scope: []
verified: strong
---
# fm research add --from-agent captures a reviewer's 'Noticed: none (…)' line as a task…
## Raw request
> FIX: fm research add --from-agent captures a reviewer's 'Noticed: none (…)' line as a task (T-2189 was 'None (T-2186 already covers …)'): a Noticed line that starts with none is no item
## Interpretation
fm research add --from-agent turns each 'Noticed:' line into a discovered task unless it is exactly none/nothing/n/a; a reviewer's 'None (T-2186 already covers …)' became T-2189. A Noticed line whose first word is none/nothing/n/a followed by punctuation or nothing is no item; 'None of the callers …' still is.
## Assumptions (confidence)
## Acceptance criteria
- [x] a 'None (…)', 'nothing - …' or 'N/A.' Noticed line is no task; 'None of the …' is one — verify with `python3 plugin/tests/run.py test_roles`
## Non-goals
## Approach (options → choice → why)
Options: (a) a fullmatch on none|nothing|n/a then end or punctuation (chosen: one line, keeps 'None of …'); (b) drop any line starting with none (rejected: loses 'None of the callers check …'); (c) ask agents to omit the line (rejected: agents vary, the parser is the boundary).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, fix the filter, fm check, finish
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_roles` → ✗ exit 1 · Ran 6 tests in 1.0s (5 classes, 16 at a time; slowest: Noticed 1s, Andon 1s, SeedReview 0s) / FAILED (1 classes) [ran] [tree 70b3d69af216] (2026-10-30T17:35:16Z)
- (step 1) `python3 plugin/tests/run.py test_roles` → exit 0 · Ran 6 tests in 1.0s (5 classes, 16 at a time; slowest: Noticed 1s, Andon 0s, SeedReview 0s) / OK [ran] [tree 0c32311f2d76] (2026-10-30T17:35:21Z)
- (step 1) `python3 plugin/tests/run.py test_roles` → exit 0 · Ran 6 tests in 1.1s (5 classes, 16 at a time; slowest: Noticed 1s, Andon 1s, SeedReview 0s) / OK [ran] [tree c962b2b0cb46] (2026-10-30T17:35:54Z)
- `python3 plugin/tests/run.py test_roles` → ✗ exit 1 · Ran 6 tests in 2.2s (5 classes, 16 at a time; slowest: Noticed 1s, Andon 0s, SeedReview 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a286530b80d4] (2026-10-30T17:36:23Z)
- `python3 plugin/tests/run.py test_roles` → exit 0 · Ran 6 tests in 1.0s (5 classes, 16 at a time; slowest: Noticed 1s, SeedReview 0s, Andon 0s) / OK [ran] [tree a286530b80d4] (2026-10-30T17:36:23Z)
- (step 1) `python3 plugin/tests/run.py test_roles` → exit 0 · Ran 6 tests in 0.6s (5 classes, 16 at a time; slowest: Noticed 0s, Andon 0s, SeedReview 0s) / OK [ran] [tree fd4febe7a2fc] (2026-10-30T17:37:51Z)
- `python3 plugin/tests/run.py test_roles` → ✗ exit 1 · Ran 6 tests in 1.5s (5 classes, 16 at a time; slowest: Noticed 0s, Andon 0s, SeedReview 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 76ab05df3f56] (2026-10-30T17:38:00Z)
- `python3 plugin/tests/run.py test_roles` → exit 0 · Ran 6 tests in 0.6s (5 classes, 16 at a time; slowest: Noticed 0s, Andon 0s, SeedReview 0s) / OK [ran] [tree 76ab05df3f56] (2026-10-30T17:38:00Z)
- (audit intent) `foreman:fm-reviewer` → approve with nits: 'None, but X' kept via a contrast word; 'None observed/at this time' now no item; fixed test-first [tree 76ab05df3f56] (2026-10-30T17:38:17Z)
- (audit maintainer) `foreman:fm-reviewer` → named helper _no_item; test asserts each kept title and exactly 5 [tree 76ab05df3f56] (2026-10-30T17:38:18Z)
- (ac 1) `python3 plugin/tests/run.py test_roles` → exit 0 · Ran 6 tests in 0.6s (5 classes, 16 at a time; slowest: Noticed 0s, Andon 0s, SeedReview 0s) / OK [ran] [tree 76ab05df3f56] (2026-10-30T17:38:26Z)
- (audit intent) `one foreman:fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 findings fixed test-first` → a Noticed line that only says nothing is no item; None of / Nothing validates / None, but stay items [tree 76ab05df3f56] (2026-10-30T17:38:26Z)
- (audit edge) `one foreman:fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 findings fixed test-first` → bare none, **None**, N/A., None yet, Nonexistent… (kept), None - of note all traced [tree 76ab05df3f56] (2026-10-30T17:38:26Z)
- (audit adversary) `one foreman:fm-reviewer pass (intent, adversary, edge, operator, maintainer); 3 findings fixed test-first` → input already redacted+defanged, capped at 200 chars, regex has no overlapping repetition [tree 76ab05df3f56] (2026-10-30T17:38:26Z)
## Log
- 2026-10-30T16:49:21Z created
- 2026-10-30T17:09:06Z planned: it has criteria and steps
- 2026-10-30T17:34:53Z focused
- 2026-10-30T17:38:59Z done
- 2026-10-30T17:39:01Z committed 90ebd1cd (4 files)
- 2026-10-30T17:39:24Z guard authorization added: publish
- 2026-10-30T17:42:08Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- playbook Deprecation: announce, shim, remove (fm playbooks show clean/deprecation)
- T-1867 [FEATURE M, dropped, 0 steps] Swipe_apply` raises `UsageError` for stale items. A `--apply` batch aborts all-or-nothing,
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- the similar finished task took 7 steps
- start here (files T-1866 touched): plugin/tests/test_inbox_more.py, plugin/lib/fmcli.py, plugin/lib/fmeco.py, plugin/lib/fmcodetui.py, plugin/commands/backlog.md, plugin/tests/test_backlog.py
## Why not caught
test_roles covered only a bare 'none'; no case had a none line with a tail
## Lessons
- A parser that filters 'nothing' replies must test the phrasings agents really write (None (…), None observed, None, but X), not only the bare word
## Plan gaps
- failed first: step 1 red test, fix the filter, fm check, finish
## Files touched
- plugin/tests/test_roles.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
