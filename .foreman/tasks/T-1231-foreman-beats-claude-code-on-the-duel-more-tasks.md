---
id: T-1231
type: PERFORMANCE
tier: L
status: deferred
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T17:04:20Z
updated: 2026-10-28T09:56:23Z
base: 03444605f297fd97f67960ec2d78a7c941d3fb25
base_tree: 98bc0062a4b12b8ad2247f478a33ed07ba87e6c4
plan0_at: 2026-10-16T17:04:30Z
plan0_scope: []
paused_tree: 793e6e1f862758863511efd4b05dd2556e181049
revisit: 2026-11-11
---
# Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time
## Raw request
> Foreman beats Claude Code on the duel: more tasks passed, lower cost, less time
## Interpretation
The user: 'I want foreman to be better than CC though, and cheaper/faster' after the first duel showed Foreman 0/6 vs Claude Code 1/6 at +33% cost. Better = more tasks passed blind; cheaper = lower total USD; faster = less wall time, on a benchmark that measures fairly. The result is published as measured; no cherry-picked runs.
## Assumptions (confidence)
## Acceptance criteria
- [ ] On a valid duel (court cases excluded, every case's reference solution green under the same grading, --runs 3), Foreman passes at least as many tasks as Claude Code with the guard only, at no more total cost and time; the result is published on the Benchmarks page whichever way it falls — verify with `fm bench duel --vs none --json`
## Non-goals
## Approach (options → choice → why)
Chosen: fix the benchmark's validity first (court cases out, references validated, --runs 3), then let transcripts decide what to cut and what to strengthen, so changes target measured cost and failures rather than guesses. Considered: (a) a public benchmark like SWE-bench (heavy setup; captured for later); (b) blanket lean mode that drops audits for all work (loses what Foreman is for); (c) tuning prompts against the six cases (overfits; rejected); (d) cheaper subagent routing in headless runs (likely more spend there).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Benchmark validity: duel skips court cases unless named, gains --runs and parallel cases; fresh hidden-test cases from recent work, each reference solution green under grading
2. [x] Diagnose: transcripts of both arms on 2-3 cases; tally turns, tokens, refusals, injected context and gate time by kind
3. [x] Cut Foreman's overhead where the tally shows it (ceremony turns, refusals, injection size, gates on S work)
4. [x] Raise the pass rate where the failed hidden tests show it (ground in existing tests and code first, test per criterion)
5. [ ] Rerun the duel with --runs 3, publish on the Benchmarks page, release  <- CURRENT
## Resume here
<!-- auto -->
- 2026-10-16T23:13:34Z step 5/5: Rerun the duel with --runs 3, publish on the Benchmarks page, release
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: plugin/tests/test_bench.py, plugin/lib/fmbench.py, plugin/tests/test_hooks.py, site/stats.py, site/build.py, site/data/stats.json, site/pages.py, site/style.css, plugin/tests/test_first_note.py, plugin/lib/fmhooks.py, CHANGELOG.md
- failures met: failed (0 classes)
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench_family test_board_posture test_help` → exit 0 · Ran 25 tests in 18.9s (9 classes, 16 at a time; slowest: Judged 19s, Duel 13s, BoardPostureBench 9s) / OK [ran] [tree 9a25a7dbe595] (2026-10-16T17:07:28Z)
- (step 3) `python3 plugin/tests/run.py test_task_ergonomics -k test_a_one_request_full_autonomy -k test_a_second_request_or_standard` → exit 0 · Ran 9 tests in 6.6s (2 classes, 16 at a time; slowest: TaskErgonomics 6s, NoTaskGate 2s) / OK [ran] [tree eee819f688c9] (2026-10-16T17:19:37Z)
- (step 2) `python3 scratchpad/tally.py on 4 kept duel transcripts (T-0205, T-0207 x both arms)` → Foreman arm 23 calls each vs bare 17-25; Foreman's extra turns: first-edit refusal + fm task new (2), plan sections/--help/state write (3-4), a broken check forcing drop+recreate (6); per-turn context +~2k tokens only (skill/agent listings); both arms hit core-protection refusals in Foreman's own repo [tree eee819f688c9] (2026-10-16T17:19:44Z)
- (step 3) `python3 plugin/tests/run.py test_task_ergonomics -k NoTaskGate -k HookClaudeShape` → exit 0 · Ran 27 tests in 5.8s (3 classes, 16 at a time; slowest: NoTaskGate 6s, TaskErgonomics 5s, HookClaudeShape 0s) / OK [ran] [tree 0d79b0703de6] (2026-10-16T18:02:09Z)
- (step 4) `python3 plugin/tests/run.py test_first_note test_hooks` → exit 0 · Ran 191 tests in 37.7s (22 classes, 16 at a time; slowest: Stop 38s, PreToolUse 22s, NoTaskGate 21s) / OK [ran] [tree 9437afe4652a] (2026-10-16T23:05:41Z)
## Log
- 2026-10-16T17:04:20Z created
- 2026-10-16T17:04:29Z set approved=True
- 2026-10-16T17:04:30Z focused
- 2026-10-16T17:19:56Z includes T-1225: Fm task ac/step: 'fm task ac T-1 "text"' and 'fm task ac add T-1 …' fail with a bare argpa
- 2026-10-16T17:21:05Z includes T-1228: Unattended (-p) Foreman runs end with a reply that shows the checks that ran (✓ lines with
- 2026-10-16T17:25:37Z paused for T-1233 (security review of T-1226: chat approval bound to the asking Claude process); both touch fmhooks.py
- 2026-10-16T17:25:38Z paused: focus moved to T-1233
- 2026-10-16T17:27:59Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T17:27:59Z focused
- 2026-10-16T17:27:59Z scope: carries T-1233's code (fmhooks _hook_claude/_claude_id, pid binding in _record_asks/_resolve_approvals, fmcli fm ask 'claude' field, helpers stand-in opt-in, test_hooks same-process test); T-1233's commit 1daa4218 held its changelog line only
- 2026-10-16T17:31:47Z paused: closing T-1232 (merged spec suite)
- 2026-10-16T17:31:47Z paused: focus moved to T-1232
- 2026-10-16T17:33:37Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T17:33:37Z focused
- 2026-10-16T17:38:48Z paused: closing T-1234 (overhead cuts) with the full suite green
- 2026-10-16T17:38:49Z paused: focus moved to T-1234
- 2026-10-16T17:43:39Z focused
- 2026-10-16T17:46:27Z paused: focus moved to T-1236
- 2026-10-16T17:47:14Z focused
- 2026-10-16T18:42:48Z paused: focus moved to T-1237
- 2026-10-16T18:43:45Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T18:43:45Z focused
- 2026-10-16T19:01:37Z includes T-1229: Unattended Foreman runs don't open side tasks (a brainstorm round) and drop them mid-run;
- 2026-10-16T19:21:44Z measured (final, committed code, snapshot): neutral Sonnet 8/8 vs 8/8, cost $0.55 vs $0.50 (+10%), time 145 vs 144 s; harder Sonnet 8/8 vs 8/8, $0.66 vs $0.59 (+12%), 185 vs 179 s; harder Haiku 8/8 vs 8/8, $0.081 vs $0.063 (+29%), 328 vs 257 s. Was +164% cost (smoke) and +35%/+35% (first full duel). AC not met yet: cost still above Claude Code; quality can't separate on these tasks (both pass everything). Left open; next levers: hide user-only skills from the model listing, a lighter stop-time close, larger multi-file tasks.
- 2026-10-16T19:21:59Z paused: focus moved to T-1238
- 2026-10-16T20:24:47Z includes T-1230: Rerun the duel with --runs 3 on all 11 cases after the two duel fixes, and publish the new
- 2026-10-16T22:54:43Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T22:54:43Z focused
- 2026-10-16T23:05:03Z step 4: the pass-rate gap the duels showed was in long sessions (Foreman 86 and 44 of 105 in the first smokes); fixed in T-1242 (requests survive compaction), after which Foreman passed 105 of 105 in all 3 long runs to Claude Code's 1 of 3. This step adds the unattended test-first cut (fewer evidence calls)
- 2026-10-16T23:13:38Z paused: focus moved to T-1248
- 2026-10-16T23:15:58Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T23:15:58Z focused
- 2026-10-17T00:12:12Z numbers: short Sonnet +10% cost / ~same time (8/8 both); harder Haiku rerun +14% cost, +13% time (8/8 both; was +29/+27); long session (8 requests, compaction at 40k, Haiku) Foreman 6/6 runs all 105 hidden tests vs Claude Code 3/6, ~+60% cost ($0.095 vs $0.059). Remaining gap on short tasks: Foreman's fixed context (~3.2k chars of skill listing, its hook notes) and the per-request finish; in long sessions, more compactions from a faster-growing context
- 2026-10-17T00:12:19Z deferred: criterion unmet: Foreman passes as many or more (more in long sessions) but costs 10-14% more on short tasks and ~60% more on long ones; published as measured. Next levers: a smaller skill listing (model-invocation off for user-only skills), a lighter per-request close, slower context growth in long runs (revisit 2026-10-18)
- 2026-10-20T14:28:17Z deferred: round 1 (T-1256 piped evidence, T-1257 Foreman's context share, T-1258 context-tax ratchet) attacks the same long-session premium; re-measure after it (revisit 2026-10-27)
- 2026-10-27T22:38:21Z deferred: weekly usage 95%; take it up after the 2026-10-28 reset with T-1797/T-1798 (revisit 2026-10-28)
- 2026-10-28T00:53:11Z deferred: waits for the weekly usage reset (95% used) (revisit 2026-10-28T02:00)
- 2026-10-28T09:56:23Z deferred: revisited 2026-10-28: still waits on a paid hard-suite duel (none run since); fm cost and the T-1796 measurements cover overhead meanwhile (revisit 2026-11-11)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-16: T-1231 L plan approval under standard autonomy: the user's explicit request ('I want foreman to be better than CC though, and cheaper/faster') is th…
- T-1222 [FEATURE L, done, 3 steps] Benchmarks page: Foreman against plain Claude Code (and other plugins) on real tasks, published with the method — lesson: Validate a be…
- T-1089 [FEATURE M, done, 3 steps] Ok, don't ask me any more questions or ANYTHING, I will be AFK, do everything, etc. also m — lesson: A tool that writes on Claude's beh…
- T-0223 [FEATURE M, done, 1 steps] Fm bench models — replay the cases once per model and recommend the cheapest model that pa — lesson: Recommend from measured pass total…
