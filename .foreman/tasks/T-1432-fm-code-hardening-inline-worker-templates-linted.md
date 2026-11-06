---
id: T-1432
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T20:44:12Z
updated: 2026-10-21T21:25:36Z
batch: [T-1418, T-1421, T-1423, T-1426]
base: a55b263cc3c8f57805a8c6da21006b835c21077c
base_tree: 4eb7e168e2957fb1ef69db3975ceb371961bec3d
plan0_at: 2026-10-21T20:46:17Z
plan0_scope: []
verified: strong
---
# fm code hardening: inline --worker templates linted, more metadata endpoints refused, odd usage counts survived, the pl…
## Raw request
> T-1418: fm code: an inline --worker 'CMD --yolo {prompt}' skips T-1395's dangerous-flag lint; gemini's -y isn't in DANGEROUS; fmcodetui._choices doesn't catch CodeError from all_runners, so a bad code.toml can break the TUI picker
> T-1421: fm code's model endpoint check: also refuse other cloud metadata addresses (Alibaba 100.100.100.200, Azure wireserver 168.63.129.16) and hostnames resolving to them (T-1395 ponytail)
> T-1423: fm code's Run.usage adds the server's reported token counts with no type check, so a server reporting usage as a string crashes the run with a TypeError (T-1404 builder)
> T-1426: fm code's planner sets FOREMAN_WORKER_OF but its claude stream gets no lean init check (T-1388 covers the worker only); and fm state without --line can create a project through resolve(create=True), a write on a read (T-1388 review)
## Interpretation
Four gaps reviewers and builders found in today's fm code hardening (T-1388, T-1395, T-1404): an inline --worker template skips the approval-off lint; two cloud metadata addresses and DNS names aren't refused; a server's odd usage field crashes the run; the planner's lean session gets no init check and fm state can create a project from inside a worker.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1418: Fm code: an inline --worker 'CMD --yolo {prompt}' skips T-1395's dangerous-flag lint; gemi works — verify with `python3 plugin/tests/run.py test_code_hardening`
- [x] T-1421: Fm code's model endpoint check: also refuse other cloud metadata addresses (Alibaba 100.10 works — verify with `python3 plugin/tests/run.py test_code_hardening`
- [x] T-1423: Fm code's Run.usage adds the server's reported token counts with no type check, so a serve works — verify with `python3 plugin/tests/run.py test_code_hardening`
- [x] T-1426: Fm code's planner sets FOREMAN_WORKER_OF but its claude stream gets no lean init check (T- works — verify with `python3 plugin/tests/run.py test_code_hardening`
- [x] fm code --worker 'gemini --yolo {prompt}' (an inline template with an approval-off flag) is refused, pointing to a code.toml runner with an [ack]; a model base_url of 100.100.100.200, 168.63.129.16, or a hostname resolving to 169.254.169.254 is refused — verify with `python3 plugin/tests/run.py test_code_hardening`
- [x] a model server reporting usage counts as strings or null doesn't crash fm code (counted as 0); a lean claude planner whose init lists an MCP server stops the plan with that named; fm state under FOREMAN_WORKER_OF in an unregistered folder creates no project — verify with `python3 plugin/tests/run.py test_code_hardening`
## Non-goals
## Approach (options → choice → why)
One batch, one lane: each member is a few lines in fmcode, fmmodels or fmcli beside code T-1388/T-1395 just added (dangerous_flags, _link_local, lean_extras), so reuse those helpers rather than add new ones. Options per member were weighed in their captures; the inline template is refused outright (it has no runner name to hang an ack on), the cheapest honest rule.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1418: Fm code: an inline --worker 'CMD --yolo {prompt}' skips T-1395's dangerous-flag lint; gemi
2. [x] T-1421: Fm code's model endpoint check: also refuse other cloud metadata addresses (Alibaba 100.10
3. [x] T-1423: Fm code's Run.usage adds the server's reported token counts with no type check, so a serve
4. [x] T-1426: Fm code's planner sets FOREMAN_WORKER_OF but its claude stream gets no lean init check (T-
5. [x] failing tests in plugin/tests/test_code_hardening.py for each of the six behaviours
6. [x] worker_argv runs fmcode.dangerous_flags on an inline template and refuses with the code.toml + [ack] route; fmmodels._link_local adds 100.100.100.200 and 168.63.129.16 and resolves a hostname (getaddrinfo, short timeout) refusing if any address is link-local or metadata; Run.usage coerces non-int counts to 0; the planner's stream path (fmmodels._cli with the claude plan runner) applies fmcode.lean_extras to its init line and raises naming them; fmcli: a read under FOREMAN_WORKER_OF resolves without create
7. [x] review fix: dangerous_flags also reads the words inside a multi-word argument (an sh -c script), so a shell wrapper can't hide the flag
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 5) `python3 plugin/tests/run.py -p test_code_hardening.py` → exit 0 · Ran 8 tests in 1.8s (5 classes, 16 at a time; slowest: InlineWorker 2s, WorkerReadCreatesNothing 1s, LeanPlanner 1s) / OK [ran] [tree 32b6e3e27901] (2026-10-21T21:01:26Z)
- (step 1) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 3.0s (5 classes, 16 at a time; slowest: InlineWorker 1s, WorkerReadCreatesNothing 1s, LeanPlanner 1s) / OK [ran] [tree 32b6e3e27901] (2026-10-21T21:01:35Z)
- (step 2) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.0s (5 classes, 16 at a time; slowest: LeanPlanner 1s, InlineWorker 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 32b6e3e27901] (2026-10-21T21:01:38Z)
- (step 3) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 1.6s (5 classes, 16 at a time; slowest: InlineWorker 1s, WorkerReadCreatesNothing 1s, LeanPlanner 1s) / OK [ran] [tree 32b6e3e27901] (2026-10-21T21:01:41Z)
- (step 4) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, WorkerReadCreatesNothing 1s, MetadataEndpoints 1s) / OK [ran] [tree 32b6e3e27901] (2026-10-21T21:01:44Z)
- (step 6) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 1.5s (5 classes, 16 at a time; slowest: WorkerReadCreatesNothing 1s, InlineWorker 1s, MetadataEndpoints 1s) / OK [ran] [tree 32b6e3e27901] (2026-10-21T21:01:47Z)
- (step 7) `python3 plugin/tests/run.py test_code_hardening` → ✗ exit 1 · Ran 8 tests in 1.6s (5 classes, 16 at a time; slowest: InlineWorker 1s, WorkerReadCreatesNothing 1s, LeanPlanner 1s) / FAILED (1 classes) [ran] [tree 4f0b8b507b82] (2026-10-21T21:24:37Z)
- (step 7) `python3 plugin/tests/run.py test_code_hardening test_runner_lint` → exit 0 · Ran 19 tests in 2.5s (7 classes, 16 at a time; slowest: RunnerLint 2s, InlineWorker 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree e3ac03d4044a] (2026-10-21T21:24:47Z)
- (audit adversary) `fm-reviewer` → approve with nits: one MEDIUM — an sh -c wrapper hid the flag from the lint — fixed failing-first (dangerous_flags reads inside multi-word arguments, depth 3); planner kill, IP forms and resolve change read as sound; nits captured (T-1438) [tree 44850c6e72aa] (2026-10-21T21:24:59Z)
- (step 1) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 1.5s (5 classes, 16 at a time; slowest: InlineWorker 1s, WorkerReadCreatesNothing 1s, MetadataEndpoints 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:09Z)
- (step 2) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 1.3s (5 classes, 16 at a time; slowest: InlineWorker 1s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:12Z)
- (step 3) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 1.4s (5 classes, 16 at a time; slowest: InlineWorker 1s, WorkerReadCreatesNothing 1s, LeanPlanner 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:14Z)
- (step 4) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 1.5s (5 classes, 16 at a time; slowest: InlineWorker 1s, WorkerReadCreatesNothing 1s, LeanPlanner 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:16Z)
- (step 5) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 1.4s (5 classes, 16 at a time; slowest: InlineWorker 1s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:18Z)
- (step 6) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:22Z)
- (ac 1) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
- (ac 2) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
- (ac 3) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
- (ac 4) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
- (ac 5) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
- (ac 6) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 8 tests in 2.1s (5 classes, 16 at a time; slowest: InlineWorker 2s, LeanPlanner 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
- (audit intent) `fm-reviewer: approve with nits; the one MEDIUM (sh -c wrapper) fixed failing-first; nits captured as T-1438` → an inline approval-off template (and one wrapped in sh -c) is refused toward code.toml + [ack]; 100.100.100.200, 168.63.129.16 and a name resolving to 169.254.169.254 are refused; string/null usage counts as 0; a lean planner loading MCP stops naming it; fm state in an unregistered folder as a worker creates no project (test_code_hardening) [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
- (audit edge) `fm-reviewer: approve with nits; the one MEDIUM (sh -c wrapper) fixed failing-first; nits captured as T-1438` → the resolver check fails open on a timeout or error (the real request would fail on NXDOMAIN too; rebinding stays a time-of-check gap, named); mycli -y and a wrapped mycli -y stay allowed; float token counts undercount to 0 [tree 44850c6e72aa] (2026-10-21T21:25:25Z)
## Log
- 2026-10-21T20:44:12Z created
- 2026-10-21T20:45:14Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_code_hardening`
- 2026-10-21T20:45:17Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_code_hardening`
- 2026-10-21T20:45:18Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_code_hardening`
- 2026-10-21T20:45:20Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_code_hardening`
- 2026-10-21T20:45:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1432.builder.md
- 2026-10-21T20:46:14Z focused
- 2026-10-21T21:21:26Z merged worktree-agent-a70f78cbc85c992a2 (6 file(s))
- 2026-10-21T21:21:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a70f78cbc85c992a2
- 2026-10-21T21:24:19Z focused
- 2026-10-21T21:25:27Z affected tests waived: UI mod JS subagent-row test times out at 5 s under load (T-1427, blocked with diagnosis); every linked Python suite runs in this gate
- 2026-10-21T21:25:31Z done
- 2026-10-21T21:25:36Z committed 8d50201f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- T-1395 [SECURITY M, done, 2 steps] Runner flag lint and grade: a dangerous runner template waits for an acknowledgement of its exact hash; runners show a guard grade; li…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- the similar finished task took 2 steps
## Why not caught
T-1395's lint read only top-level words; the reviewer's adversary lens found the wrapper
## Lessons
- A lint over argv words must also read inside a word that is itself a script (sh -c): the shell splits it again
## Plan gaps
- added late: review fix: dangerous_flags also reads the words inside a multi-word argument (an sh -c script), so a shell wrapper can…
- failed first: step 7 review fix: dangerous_flags also reads the words inside a multi-word argument (an sh -c script), so…
## Files touched
- plugin/tests/test_code_hardening.py
- plugin/lib/fmcode.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcli.py
- plugin/tests/test_runner_lint.py
- plugin/tests/test_code_worker.py
- CHANGELOG.md
- plugin/lib/fmbench.py
- plugin/skills/improve/SKILL.md
- plugin/tests/test_bench.py
