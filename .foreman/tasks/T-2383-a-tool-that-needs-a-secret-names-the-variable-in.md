---
id: T-2383
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: [T-2374]
source: self
created: 2026-10-31T14:02:22Z
updated: 2026-10-31T19:21:36Z
base: 76be00a4457cf24dff543a22b7b979ed69cb069f
base_tree: 2dcde83b4f4a467b78f5a8ec45da3dc209624eb0
plan0_at: 2026-10-31T19:13:52Z
plan0_scope: []
verified: strong
---
# A tool that needs a secret names the variable in its queued grant (Mission 6 inbox, tier…
## Raw request
> A tool that needs a secret names the variable in its queued grant (Mission 6 inbox, tier 2): the user supplies the value outside the session; a scan of the session transcript at finish finds no value
## Interpretation
Reading 1: when a queued grant (T-2374's fm ask --later) is for a tool that needs a secret, the request names only the environment variable (e.g. GITHUB_TOKEN); the user sets the value outside the session; at fm task finish a scan of the session transcript finds no value of that variable (fm's redaction patterns plus the live value if set), and refuses the close if one appears. Reading 2: just document 'never paste secrets'. Ruled out: nothing would check it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a queued grant names the secret's variable, never its value, and fm task finish refuses when this session's transcript holds that variable's live value or a redact-pattern match on NAME=value — verify with `python3 plugin/tests/run.py test_tool_queue -k secret_env`
## Non-goals
## Approach (options → choice → why)
1) the queued grant row gains a needs_env field (names only); finish scans the transcript tail with c.redact's patterns and the live value of each named var; fails if: a value appears encoded (base64), which the redact patterns partly catch. 2) use what exists: c.redact at log time only; fails if: a value pasted into chat never passes through fm. 3) do less: a doc line; fails if: unchecked. Choice 1 (80%): names in the grant, a scan at close.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: grant row names the var; a transcript with the value refuses finish; without passes
2. [x] needs_env on the queued row and the finish scan
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tool_queue -k secret_env` → exit 0 · Ran 3 tests in 3.2s (1 classes, 16 at a time; slowest: GrantQueue 3s) / OK [ran] [tree b4fa7f2d19cb] (2026-10-31T19:19:14Z)
- (step 2) `python3 plugin/tests/run.py test_tool_queue test_guard` → exit 0 · Ran 329 tests in 23.8s (91 classes, 16 at a time; slowest: GrantQueue 23s, Mutation 17s, GuardAgainstBash 15s) / OK [ran] [tree b4fa7f2d19cb] (2026-10-31T19:19:39Z)
- (ac 1) `python3 plugin/tests/run.py test_tool_queue -k secret_env` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: GrantQueue 3s) / OK [ran] [tree b4fa7f2d19cb] (2026-10-31T19:19:43Z)
- `python3 plugin/tests/run.py test_tool_queue -k secret_env` → ✗ exit 1 · Ran 3 tests in 5.0s (1 classes, 16 at a time; slowest: GrantQueue 3s) / FAILED (1 classes: test_tool_queue.GrantQueue) (start tree + this task's tests) [ran] [tree 9b8fb6ebbd69] (2026-10-31T19:20:05Z)
- `python3 plugin/tests/run.py test_tool_queue -k secret_env` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: GrantQueue 3s) / OK [ran] [tree 9b8fb6ebbd69] (2026-10-31T19:20:05Z)
- (ac 1) `python3 plugin/tests/run.py test_tool_queue -k secret_env` → exit 0 · Ran 3 tests in 3.3s (1 classes, 16 at a time; slowest: GrantQueue 3s) / OK [ran] [tree 9b8fb6ebbd69] (2026-10-31T19:20:20Z)
- (audit adversary) `main-thread review (pace gate holds): the scan's first form took 9.3 s on this session's 606 MB transcript (a leading lookbehind defeats re's literal search), rewritten to mmap.find plus a tail match, 0.14 s with the same 27 hits; criterion's verify pointed at a test file that didn't exist (test_ask), corrected to test_tool_queue` → no message or row ever carries a value (a value-shaped --needs-env is refused by position, not echoed; the finish refusal names the variable only, tested); a direct edit of the row is state-direct; with the variable set, only its exact live value counts, so a test fixture can't pin a close and a rotated secret clears it [tree 9b8fb6ebbd69] (2026-10-31T19:20:20Z)
- (audit edge) `main-thread review (pace gate holds): the scan's first form took 9.3 s on this session's 606 MB transcript (a leading lookbehind defeats re's literal search), rewritten to mmap.find plus a tail match, 0.14 s with the same 27 hits; criterion's verify pointed at a test file that didn't exist (test_ask), corrected to test_tool_queue` → OTHER_SVC_TOKEN= [REDACTED]'t count for SVC_TOKEN; $VAR and <placeholder> are references; an empty transcript or no session id fails open (logged); a value pasted in an earlier session of the task isn't seen (ponytail note in secret_gaps) [tree 9b8fb6ebbd69] (2026-10-31T19:20:20Z)
- (audit intent) `main-thread review (pace gate holds): the scan's first form took 9.3 s on this session's 606 MB transcript (a leading lookbehind defeats re's literal search), rewritten to mmap.find plus a tail match, 0.14 s with the same 27 hits; criterion's verify pointed at a test file that didn't exist (test_ask), corrected to test_tool_queue` → the row names the variable, fm todo shows it, finish and done both refuse while the transcript holds it [tree 9b8fb6ebbd69] (2026-10-31T19:20:20Z)
- (audit self) `main-thread review (pace gate holds): the scan's first form took 9.3 s on this session's 606 MB transcript (a leading lookbehind defeats re's literal search), rewritten to mmap.find plus a tail match, 0.14 s with the same 27 hits; criterion's verify pointed at a test file that didn't exist (test_ask), corrected to test_tool_queue` → no findings [tree 9b8fb6ebbd69] (2026-10-31T19:20:20Z)
## Log
- 2026-10-31T14:02:22Z created
- 2026-10-31T17:28:29Z planned: it has criteria and steps
- 2026-10-31T17:28:29Z set depends_on=['T-2374']
- 2026-10-31T19:13:51Z focused
- 2026-10-31T19:19:05Z criterion 1 verify: `python3 plugin/tests/run.py test_ask -k secret_env` → `python3 plugin/tests/run.py test_tool_queue -k secret_env`
- 2026-10-31T19:19:05Z criterion 1 text: a queued grant names the secret's variable, never its value, and fm task finish refuses when the session transcript holds that variable's live value or a redact-pattern match → a queued grant names the secret's variable, never its value, and fm task finish refuses when this session's transcript holds that variable's live value or a redact-pattern match on NAME=value
- 2026-10-31T19:21:33Z done
- 2026-10-31T19:21:36Z committed 7958b82a (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2374 [FEATURE M, done, 4 steps] Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and th…
- research mission-20261031-083834: Request: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skil…
- research mission-20261031-083834.pack: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skill or…
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
## Files touched
- plugin/tests/test_tool_queue.py
- plugin/lib/fmgrants.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
