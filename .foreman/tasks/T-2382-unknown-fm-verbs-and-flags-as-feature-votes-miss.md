---
id: T-2382
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmfriction.py, plugin/tests/test_cli.py, plugin/tests/test_friction.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-31T14:02:22Z
updated: 2026-11-01T23:42:37Z
group: Mission 6 inbox and installs
base: ddd253b6b588eb112b7541d5e9a138090ec1a11b
base_tree: eb1e85af090fc432cd00a4f664c586d235f5dae5
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T23:27:25Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmfriction.py, plugin/tests/test_cli.py, plugin/tests/test_friction.py, CHANGELOG.md]
verified: strong
---
# Unknown fm verbs and flags as feature votes in fm friction
## Raw request
> Unknown fm verbs and flags as feature votes (Mission 6 inbox, tier 2): the typo-help path (T-0273) logs each unknown word once per session; fm friction lists the top ones as missing verbs
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] an unknown fm flag or verb appends one unknown_word event (command, word, session); fm friction lists the top words, counted once per session, as missing verbs and flags — verify with `python3 plugin/tests/run.py test_cli test_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: fm task drop T-1 --reason x twice in one session and once in another, fm bogus once; fm friction's section shows '2 sessions: fm task drop --reason' above 'fm bogus'
2. [x] fmcli parser error(): log unknown_word (the first unknown flag, else the invalid choice) before exiting; fmfriction.digest: a section of the top words by distinct sessions
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_friction.Friction.test_unknown_fm_words_rank_by_the_sessions_that_reached_for_them` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Friction 0s) / FAILED (1 classes: test_friction.Friction) [ran] [tree 3c1d47cfb915] (2026-11-01T23:27:29Z)
- (step 1) `python3 plugin/tests/run.py test_friction.Friction.test_unknown_fm_words_rank_by_the_sessions_that_reached_for_them` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Friction 1s) / OK [ran] [tree 1f663d79436f] (2026-11-01T23:28:47Z)
- (step 2) `python3 plugin/tests/run.py test_friction test_cli` → exit 0 · Ran 162 tests in 20.8s (49 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 9s, CaptureAndIntake 9s) / OK [ran] [tree 1f663d79436f] (2026-11-01T23:29:09Z)
- (ac 1) `python3 plugin/tests/run.py test_cli test_friction` → exit 0 · Ran 162 tests in 21.0s (49 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 9s, CaptureAndIntake 9s) / OK [ran] [tree 728f8b7d6ad6] (2026-11-01T23:35:53Z)
- (audit edge) `self-review: the parser's error path appends one unknown_word event (cmd, word, session) before exiting, inside try/except OSError so a read-only state dir never changes the exit; words are fitted (60/40 chars), redacted on write and c.plain'd on read; a T-NNNN typed as a verb is skipped; the digest dedupes by (cmd, word, session) so one session's retries count once` → a retry in the same session counts once; a top-level unknown verb has no cmd ('fm bogus'); an unwritable events file leaves the usage error unchanged [tree 728f8b7d6ad6] (2026-11-01T23:35:53Z)
- (audit self) `self-review: the parser's error path appends one unknown_word event (cmd, word, session) before exiting, inside try/except OSError so a read-only state dir never changes the exit; words are fitted (60/40 chars), redacted on write and c.plain'd on read; a T-NNNN typed as a verb is skipped; the digest dedupes by (cmd, word, session) so one session's retries count once` → no findings [tree 728f8b7d6ad6] (2026-11-01T23:35:53Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 1a3fc77f8bd8] (2026-11-01T23:37:00Z)
## Log
- 2026-10-31T14:02:22Z created
- 2026-11-01T23:03:59Z planned from capture
- 2026-11-01T23:27:24Z focused
- 2026-11-01T23:27:25Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T23:29:09Z steer: the test uses fm next --last (11 real hits; fm task drop accepts --reason, so it was no unknown flag)
- 2026-11-01T23:29:17Z scope: MASTER.md and CHANGELOG.md entries
- 2026-11-01T23:36:30Z done
- 2026-11-01T23:36:33Z committed c9705e5c (5 files)
- 2026-11-01T23:37:01Z guard authorization added: publish
- 2026-11-01T23:42:37Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0274 [FEATURE M, done, 3 steps] Gate and CLI friction: flake ledger in fm check, nearest-command help on fm typos — lesson: Before adding a mechanism, read how the cod…
- T-1658 [FEATURE M, done, 5 steps] Settings extras: log, macro, duel, replay (what-breaks), words-to-diff, undo that adapts — lesson: CLI write tests need a pty: in_claud…
- T-2109 [CLEAN S, done, 1 steps] CLEAN S: friction repeat detector skips SessionStart/UserPromptSubmit…
- decision 2026-11-01: [revisited: T-2462 (macOS 3.14 non-blocking CI jobs] [cites: user steer 2026-10-31: finish round 1 completely, in order; no new maintenance or frict…
- similar finished tasks took 1–5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_friction.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmfriction.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Lessons
- Count a missing feature by the distinct sessions that reached for it, not by attempts, so one stubborn retry loop doesn't outvote real demand
## Plan gaps
- failed first: step 1 red test: fm task drop T-1 --reason x twice in one session and once in another, fm bogus once; fm f…
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmcli.py
- plugin/lib/fmfriction.py
- MASTER.md
- CHANGELOG.md
