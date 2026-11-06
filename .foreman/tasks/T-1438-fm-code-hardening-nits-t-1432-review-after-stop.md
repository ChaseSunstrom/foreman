---
id: T-1438
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T21:24:58Z
updated: 2026-10-21T22:44:22Z
base: 8e10d2212fd9119789549e6a554dde4e42b07d3e
base_tree: eba25dff074b9f0657fbf0378d883f89a8ac67ca
plan0_at: 2026-10-21T22:22:20Z
plan0_scope: []
verified: strong
---
# fm code hardening nits from T-1432's review: no re-kill after STOP, probes checked too, more approval-off flags, hooks don't create projects inside a worker
## Raw request
> fm code hardening nits (T-1432 review): after STOP, _cli keeps feeding the chunk's remaining lines and re-kills the group (guard with 'not stopped'); fmmodels._probe bypasses _check_url; dangerous_flags misses aider --yes-always, q --trust-all-tools, cursor-agent --force and -anever; fmhooks SessionStart/UserPromptSubmit still find_project(create=True) under FOREMAN_WORKER_OF; resolve's 'run fm init here' message should say a worker can't
## Interpretation
Five nits the T-1432 reviewer found, each small: a second kill after STOP could hit a reused pid; the local-server probe skips the metadata check; four CLIs' approval-off flags aren't linted; two hooks can still create a project from inside a worker session that cd'd elsewhere; and a worker told to run fm init can't.
## Assumptions (confidence)
## Acceptance criteria
- [x] after a STOP, _cli kills the group once; fmmodels._probe refuses a metadata or link-local base_url like _check_url; dangerous_flags catches aider --yes-always, q --trust-all-tools, cursor-agent --force (only when the command is cursor-agent) and -anever; SessionStart and UserPromptSubmit never create a project when FOREMAN_WORKER_OF is set; resolve's refusal inside a worker says a worker can't run fm init — verify with `python3 plugin/tests/run.py test_code_hardening test_runner_lint`
## Non-goals
## Approach (options → choice → why)
Options: (A) one batch, each fix beside the code T-1388/T-1395/T-1432 added, reusing dangerous_flags, _check_url and the FOREMAN_WORKER_OF test (chosen: small, one review); (B) separate tasks (five reviews for five few-line changes). Basename-gated flags (cursor-agent --force, gemini -y) avoid false hits on other CLIs' --force.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests (extend plugin/tests/test_code_hardening.py) for each of the five
2. [x] fmmodels._cli: guard STOP with a stopped flag; _probe calls _check_url first; fmcode.dangerous_flags: add the flags, cursor-agent's --force only with that basename (as gemini -y); fmhooks: find_project(create=not os.environ.get('FOREMAN_WORKER_OF')) at the SessionStart and UserPromptSubmit sites; fmcli.resolve's worker message
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_hardening` → ✗ exit 1 · Ran 13 tests in 2.2s (6 classes, 16 at a time; slowest: ReviewNits 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / FAILED (1 classes) [ran] [tree a88e305521e2] (2026-10-21T22:23:54Z)
- (ac 1) `python3 plugin/tests/run.py test_code_hardening test_runner_lint 2>&1 | tail -15` → exit 0 · Ran 24 tests in 4.1s (8 classes, 16 at a time; slowest: RunnerLint 3s, ReviewNits 3s, InlineWorker 3s) / OK [ran] [tree 233a1e4691ac] (2026-10-21T22:24:32Z)
- (step 2) `python3 plugin/tests/run.py test_code_hardening test_runner_lint` → exit 0 · Ran 24 tests in 4.0s (8 classes, 16 at a time; slowest: RunnerLint 3s, ReviewNits 2s, WorkerReadCreatesNothing 2s) / OK [ran] [tree 9c00c9406360] (2026-10-21T22:24:50Z)
- (step 1) `python3 plugin/tests/run.py test_code_hardening test_runner_lint test_hooks` → exit 0 · Ran 216 tests in 102.9s (30 classes, 16 at a time; slowest: Stop 103s, NoTaskGate 68s, PreToolUse 62s) / OK [ran] [tree fdc6e3feec54] (2026-10-21T22:39:21Z)
- (step 2) `python3 plugin/tests/run.py test_code_hardening test_runner_lint test_hooks` → exit 0 · Ran 216 tests in 101.5s (30 classes, 16 at a time; slowest: Stop 101s, NoTaskGate 71s, PreToolUse 60s) / OK [ran] [tree fdc6e3feec54] (2026-10-21T22:41:10Z)
- (audit adversary) `fm-reviewer` → approve: no findings; the STOP guard, probe check, new flags and worker project guard do what the goal says [tree fdc6e3feec54] (2026-10-21T22:44:11Z)
- (ac 1) `python3 plugin/tests/run.py test_code_hardening test_runner_lint` → exit 0 · Ran 24 tests in 2.1s (8 classes, 16 at a time; slowest: RunnerLint 2s, InlineWorker 1s, ReviewNits 1s) / OK [ran] [tree fdc6e3feec54] (2026-10-21T22:44:14Z)
- (audit intent) `fm-reviewer (research T-1434-1417-review): approve, no findings` → all five nits fixed with failing-first tests (test_code_hardening ReviewNits) [tree fdc6e3feec54] (2026-10-21T22:44:14Z)
- (audit edge) `fm-reviewer (research T-1434-1417-review): approve, no findings` → _probe only sees LOCAL's literal 127.0.0.1 URLs, so its new guard never fires in practice; basename-gated --force errs toward flagging [tree fdc6e3feec54] (2026-10-21T22:44:14Z)
## Log
- 2026-10-21T21:24:58Z created
- 2026-10-21T22:22:03Z planned from capture
- 2026-10-21T22:22:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1438.builder.md
- 2026-10-21T22:22:19Z focused
- 2026-10-21T22:32:16Z merged worktree-agent-abc02e981e5f4ff5b (5 file(s))
- 2026-10-21T22:32:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abc02e981e5f4ff5b
- 2026-10-21T22:44:09Z focused
- 2026-10-21T22:44:16Z affected tests waived: UI mod JS tests are unrelated to fmcode/fmmodels/fmhooks changes and pass on their own
- 2026-10-21T22:44:19Z done
- 2026-10-21T22:44:22Z committed 9d4f2282 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1432 [SECURITY M, done, 7 steps] fm code hardening: inline --worker templates linted, more metadata endpoints refused, odd usage counts survived, the pl… — lesson: A l…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- the similar finished task took 7 steps
## Why not caught
nits from T-1432's review
## Lessons
- Gate CLI-specific short flags on the command's basename, or a common flag like --force flags every CLI
## Plan gaps
- failed first: step 1 failing tests (extend plugin/tests/test_code_hardening.py) for each of the five
## Files touched
- plugin/tests/test_code_hardening.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcode.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/lib/fmdoctor.py
- plugin/lib/fmplugins.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_judge_home.py
- plugin/tests/test_supply_delta.py
