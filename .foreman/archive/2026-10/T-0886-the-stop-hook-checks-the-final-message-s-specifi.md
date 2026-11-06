---
id: T-0886
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T15:29:55Z
updated: 2026-10-15T16:37:17Z
base: d9ff6a950abee22c8b15b415a147921448203967
base_tree: 450d8243610535ea2c8f5a57de8ba85d529a466b
verified: strong
---
# The Stop hook checks the final message's specific claims (tests pass, fixed, verified) aga
## Raw request
> FEATURE: The Stop hook checks the final message's specific claims (tests pass, fixed, verified) against the tool log, not only done claims
> CONTEXT: round 5 #46. claims_done and _evidence_gate in fmhooks.py gate only done; a 'tests pass' with no passing test run after the last edit should be challenged once
## Interpretation
When the final message claims tests, the suite, checks or gates pass (or are green), the Stop hook reads the turn's tool calls from the transcript: if a file was edited after the last test run (or none ran after edits), or the last test run failed, it holds the stop once with what it saw, so a claim is backed by the run that proves it. A turn with no edits and no test runs isn't judged.
## Assumptions (confidence)
## Acceptance criteria
- [x] a 'tests pass' claim after an edit with no later passing run, or after a failed run, holds the stop once; a backed claim or a turn without edits doesn't — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
1) Read the session transcript in the Stop hook (chosen: it has every tool call and result of the turn, in order; Stop already reads it for notices). 2) Log every Bash result in PostToolUse and read that log (a write per tool call for a rare check). 3) Ask a model to judge the claims (tokens, latency, non-deterministic). Complete version: claim regex with negation, test-command and failure patterns incl. Foreman's own fm check/evidence/finish runs, file-tool edits, once per session+message, tail-bounded read, never in a stop_hook_active turn.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests in test_hooks Stop, then _claims_gate reading the transcript
2. [x] docs (MASTER, CHANGELOG)
## Resume here
## Docs impact
MASTER test claims; CHANGELOG round 5
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks test_friction` → exit 0 · Ran 161 tests in 27.5s (22 classes, 16 at a time; slowest: Stop 27s, PreToolUse 14s, Approvals 11s) / OK [ran] [tree 7d7b4a5e3154] (2026-10-15T16:33:44Z)
- (step 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 31 tests in 1.0s (10 classes, 16 at a time; slowest: TaskLifecycle 1s, TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree 7d7b4a5e3154] (2026-10-15T16:33:46Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 149 tests in 27.3s (20 classes, 16 at a time; slowest: Stop 27s, PreToolUse 14s, Approvals 11s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 7d7b4a5e3154] (2026-10-15T16:34:41Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 149 tests in 27.2s (20 classes, 16 at a time; slowest: Stop 27s, PreToolUse 14s, Approvals 11s) / OK [ran] [tree 7d7b4a5e3154] (2026-10-15T16:34:41Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 149 tests in 27.3s (20 classes, 16 at a time; slowest: Stop 27s, PreToolUse 14s, Approvals 11s) / OK [ran] [tree 7d7b4a5e3154] (2026-10-15T16:37:09Z)
- (audit intent) `self review plus a dry run of the parser over this session's real transcript (267 calls, 85 test runs): after the tail-only verdict and prove's red line excluded, every run it read as failed had failed; Stop p95 unchanged (36 ms; the transcript is read only when a claim matches)` → a 'tests pass' reply is held once when an edit came after the last run or that run failed, with the reason; a backed claim or a turn without edits and runs passes (5 cases in one test) [tree 7d7b4a5e3154] (2026-10-15T16:37:09Z)
- (audit edge) `self review plus a dry run of the parser over this session's real transcript (267 calls, 85 test runs): after the tail-only verdict and prove's red line excluded, every run it read as failed had failed; Stop p95 unchanged (36 ms; the transcript is read only when a claim matches)` → negated claims ('tests don't pass yet' via _NEG), task notifications don't reset the turn, a transcript that can't be read judges nothing, Bash-made edits aren't seen (documented), one hold per message so a stop_hook_active turn never loops [tree 7d7b4a5e3154] (2026-10-15T16:37:09Z)
- (audit intent) `self review plus a dry run of the parser over this session's real transcript (267 calls, 85 test runs): after the tail-only verdict and prove's red line excluded, every run it read as failed had failed; Stop p95 unchanged (36 ms; the transcript is read only when a claim matches)` → a 'tests pass' reply is held once when an edit came after the last run or that run failed, with the reason; a backed claim or a turn without edits and runs passes (5 cases in one test) [tree 7d7b4a5e3154] (2026-10-15T16:37:16Z)
- (audit edge) `self review plus a dry run of the parser over this session's real transcript (267 calls, 85 test runs): after the tail-only verdict and prove's red line excluded, every run it read as failed had failed; Stop p95 unchanged (36 ms; the transcript is read only when a claim matches)` → negated claims ('tests don't pass yet' via _NEG), task notifications don't reset the turn, a transcript that can't be read judges nothing, Bash-made edits aren't seen (documented), one hold per message so a stop_hook_active turn never loops [tree 7d7b4a5e3154] (2026-10-15T16:37:16Z)
- (audit adversary) `self review plus a dry run of the parser over this session's real transcript (267 calls, 85 test runs): after the tail-only verdict and prove's red line excluded, every run it read as failed had failed; Stop p95 unchanged (36 ms; the transcript is read only when a claim matches)` → sha1 only keys the once-per-message memo (not a security use); transcript text is untrusted but only decides one hold, quoted back as a command name cut to 80 chars, never run; the read is capped at 4 MB [tree 7d7b4a5e3154] (2026-10-15T16:37:16Z)
## Log
- 2026-10-15T15:29:55Z created
- 2026-10-15T16:00:52Z focused
- 2026-10-15T16:31:33Z user approved core in Claude Code's permission prompt
- 2026-10-15T16:37:16Z done
- 2026-10-15T16:37:17Z committed 627409b (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round5-20261015: Probe: `fm ideas` with capability map + unspoken needs, 2 rounds, past every earlier ideas.md (brainstorm-20261015-101633): 54 new t…
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- T-0414 [FIX M, done, 3 steps] Guard: a data-reading python -c is judged by what runs before it — lesson: A parser that drops quoting can't be trusted about structure the…
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- the similar finished task took 3 steps
## Lessons
- Judge a run by its verdict, not by every failure word in it: a red-then-green proof prints ✗ on purpose, so read the last lines
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
