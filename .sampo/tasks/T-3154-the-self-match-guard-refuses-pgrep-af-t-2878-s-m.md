---
id: T-3154
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T05:57:19Z
updated: 2026-11-05T15:22:47Z
builder_model: haiku
base: fc8cc431f4e896bd3a6be82bba0594911c0d1d52
base_tree: e5a1b77726a42ac49c68a8babd492caa7c8f97fd
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T10:08:25Z
plan0_scope: []
builder_returned: 2026-11-05T10:14:30Z
lane_stop: refused 2026-11-05T15:04:40Z
postmerge_red: test_board_verbs.BoardVerbs
postmerge_sha: 1c85b07e7d8d656d27723eac7a49d94a5e4ed24b
verified: strong
unproven: [data]
---
# The self-match guard judges each alternative of a process-search pattern, and only patterns that are really run
## Raw request
> The self-match guard refuses pgrep -af "[t]2878|[s]mith|[l]ouhi" as matching its own shell, though every alternative is bracketed so it can't match itself: judge each alternative of an alternation pattern, not the whole string
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A process-search pattern whose every alternative is bracketed ([t]2878|[s]mith|[l]ouhi) passes the self-match check, also when it only appears inside a quoted argument of another command (a task's text); a pattern with one unbracketed alternative that the command line contains is still refused — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests then the per-alternative check
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → exit 0 · Ran 258 tests in 69.7s (36 classes, 16 at a time; slowest: Stop 69s, PreToolUse 35s, SessionStart 34s) / OK [ran] [tree f1c9802fa5bd] [world 2f1906870a] (2026-11-05T10:11:33Z)
- (step 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -12` → exit 0 · Ran 258 tests in 69.7s (36 classes, 16 at a time; slowest: Stop 69s, PreToolUse 35s, SessionStart 34s) / OK [ran] [tree f1c9802fa5bd] [world 2f1906870a] (2026-11-05T10:11:33Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 258 tests in 80.3s (36 classes, 16 at a time; slowest: Stop 80s, PreToolUse 40s, SessionStart 37s) / OK [ran] [tree f1c9802fa5bd] [world 2f1906870a] (2026-11-05T10:12:56Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [16.21s] [ran] [tree f1c9802fa5bd] [world 2f1906870a] (2026-11-05T10:14:27Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_guard` → exit 0 · Ran 587 tests in 27.5s (376 jobs, 16 at a time; slowest: Mutation 16s, SessionStart.test_budget_holds_with_large_queue 15s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_pyt [ran] [tree 837175d2ecc0] [world 2f1906870a] (2026-11-05T15:16:14Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 258 tests in 26.7s (152 jobs, 16 at a time; slowest: Approvals 20s, UserPromptSubmit 18s, PromptApprovals 16s) / OK (start tree + this task's tests) [ran] [tree 837175d2ecc0] [world 2f1906870a] (2026-11-05T15:17:01Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 258 tests in 19.7s (224 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 14s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 837175d2ecc0] [world 2f1906870a] (2026-11-05T15:17:01Z)
- `bash -c 'cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wt-3154 && python3 plugin/tests/run.py test_hooks.PreToolUse'` → ✗ exit 1 · Ran 28 tests in 4.6s (28 jobs, 16 at a time; slowest: PreToolUse.test_a_broken_core_library_keeps_grants_visible_and_protection_on 3s, PreToolUse.test_a_bare_stdin_reader_is_refused_before_it_hangs 2s [ran] [tree 837175d2ecc0] [world 2f1906870a] (2026-11-05T15:17:28Z)
- `python3 plugin/tests/run.py test_hooks.PreToolUse` → exit 0 · Ran 28 tests in 3.4s (28 jobs, 16 at a time; slowest: PreToolUse.test_a_broken_core_library_keeps_grants_visible_and_protection_on 3s, PreToolUse.test_a_bare_stdin_reader_is_refused_before_it_hangs 2s [ran] [tree 837175d2ecc0] [world 2f1906870a] (2026-11-05T15:17:32Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 258 tests in 19.9s (233 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 14s, NoTaskGateMulti.test_at_stop_the_requests_with_evidence_close_when_every_python_start_take [ran] [tree 98fe00fa1278] [world 2f1906870a] (2026-11-05T15:18:00Z)
- (audit adversary) `re-ran test_hooks + test_guard on main after the merge (587 OK); red on its merge base with its new cases, green on main` → each alternative of a pgrep/pkill pattern is judged on its own, so one unbracketed alternative ('[t]2878|fm check') still refuses a self-matching wait; a pgrep only quoted in another command's argument isn't run, so it isn't refused; a quoted pgrep that bash -c does run stays refused (tested) [tree 98fe00fa1278] (2026-11-05T15:18:00Z)
- (audit edge) `re-ran test_hooks + test_guard on main after the merge (587 OK); red on its merge base with its new cases, green on main` → all-bracketed alternatives pass; -x whole-line matches pass as before [tree 98fe00fa1278] (2026-11-05T15:18:00Z)
- (audit self) `re-ran test_hooks + test_guard on main after the merge (587 OK); red on its merge base with its new cases, green on main` → no findings [tree 98fe00fa1278] (2026-11-05T15:18:00Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_guard test_board_verbs` → exit 0 · Ran 595 tests in 39.7s (329 jobs, 16 at a time; slowest: Mutation 21s, SessionStart.test_budget_holds_with_large_queue 19s, GuardAgainstBash.test_fuzzed_forms_never_run_a_dangerous_call_unblocked 10s) [ran] [tree 5bc92a73d37e] [world 2f1906870a] (2026-11-05T15:22:31Z)
- (audit adversary) `re-landed after a false revert (BoardVerbs flake, fixed by T-3216): applied by sampo edit from its own diff; test_hooks now holds its new cases and passes with test_guard and test_board_verbs (595 OK); red on its merge base with the new cases (recorded earlier)` → each alternative of a pgrep/pkill pattern is judged on its own, so one unbracketed alternative still refuses a self-matching wait; a pgrep only quoted in another command's argument isn't run, so it isn't refused; a quoted pgrep that bash -c runs stays refused (tested) [tree 5bc92a73d37e] (2026-11-05T15:22:40Z)
- (audit edge) `re-landed after a false revert (BoardVerbs flake, fixed by T-3216): applied by sampo edit from its own diff; test_hooks now holds its new cases and passes with test_guard and test_board_verbs (595 OK); red on its merge base with the new cases (recorded earlier)` → all-bracketed alternatives pass; -x whole-line matches pass as before [tree 5bc92a73d37e] (2026-11-05T15:22:40Z)
- (audit self) `re-landed after a false revert (BoardVerbs flake, fixed by T-3216): applied by sampo edit from its own diff; test_hooks now holds its new cases and passes with test_guard and test_board_verbs (595 OK); red on its merge base with the new cases (recorded earlier)` → no findings [tree 5bc92a73d37e] (2026-11-05T15:22:40Z)
## Log
- 2026-11-05T05:57:19Z created
- 2026-11-05T10:08:07Z planned from capture
- 2026-11-05T10:08:11Z set approved=True
- 2026-11-05T10:08:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3154.builder.md
- 2026-11-05T10:08:24Z focused
- 2026-11-05T10:08:25Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T14:37:34Z merged worktree-agent-ac96042578b6ba24f (2 file(s))
- 2026-11-05T14:37:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac96042578b6ba24f
- 2026-11-05T15:04:40Z red after merge: test_board_verbs.BoardVerbs; 1c85b07e7 reverted
- 2026-11-05T15:15:45Z focused
- 2026-11-05T15:18:01Z affected tests waived: names that can't match are T-3160's modules (merged and reverted in this window, not on disk); T-3154's test_hooks and test_guard pass (587 OK)
- 2026-11-05T15:18:02Z done
- 2026-11-05T15:18:04Z committed 3949c329 (1 file)
- 2026-11-05T15:21:43Z set status=planned
- 2026-11-05T15:21:44Z correction: closed at 3949c329 by mistake: its merge had been reverted at 15:04 (38ba1592) by the post-merge verify for test_board_verbs.BoardVerbs (a flake: green alone); the close's 'green on main' ran the reverted test file. Re-landing now.
- 2026-11-05T15:21:44Z focused
- 2026-11-05T15:22:42Z affected tests waived: names that can't match are T-3160's modules (merged and reverted in this window, not on disk); T-3154's test_hooks, test_guard and test_board_verbs pass (595 OK)
- 2026-11-05T15:22:44Z done
- 2026-11-05T15:22:47Z committed 52ef1799 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1839 [FIX S, done, 1 steps] A pgrep -f/pkill -f whose pattern matches its own command is refused — lesson: A background wait is only safe if it can end: a process matc…
- T-2845 [FEATURE M, done, 2 steps] Every parser that reads typed commands or goals accepts sampo as well as fm (cost, repeats, friction, bench, long, smithtui, smith, man…
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
## Regression test
test_hooks.PreToolUse: on T-3154's merge base with its new cases it fails (recorded ✗), on main it passes
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
- plugin/cards/_lib/cardkit.py
- plugin/cards/failing-frame/card.json
- plugin/cards/failing-frame/check.py
- plugin/cards/failing-frame/gen.py
- plugin/cards/failing-frame/harness.py
- plugin/cards/failing-frame/tests.json
- plugin/cards/py-callers/card.json
- plugin/cards/py-callers/check.py
- plugin/cards/py-callers/gen.py
- plugin/cards/py-callers/tests.json
- plugin/cards/py-none-guard/card.json
- plugin/cards/py-none-guard/check.py
- plugin/cards/py-none-guard/gen.py
- plugin/cards/py-none-guard/tests.json
- plugin/cards/py-outline/card.json
- plugin/cards/py-outline/check.py
- plugin/cards/py-outline/gen.py
- plugin/cards/py-outline/tests.json
- plugin/lib/fmcallcards.py
- plugin/lib/sampo/callcards.py
- plugin/lib/sampo/landlock.py
- plugin/lib/sampo/smith.py
- plugin/tests/test_callcards.py
- plugin/tests/test_smith_cards.py
- research/callcards/pilot.jsonl
- research/callcards/slice.md
