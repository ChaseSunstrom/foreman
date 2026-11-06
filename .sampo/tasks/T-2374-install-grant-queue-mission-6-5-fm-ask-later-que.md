---
id: T-2374
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmmcp.py, plugin/lib/fmgrants.py, plugin/lib/fmserve.py, plugin/tests/test_tool_queue.py, plugin/tests/test_todo.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-31T14:02:01Z
updated: 2026-10-31T18:31:57Z
builder_model: sonnet
base: 7a6779b03918cc0da672cda152e5fa5220829790
base_tree: 1c790f3e62b3a598921713160d59e9ba9d13f87e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T17:37:00Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/lib/fmmcp.py, plugin/tests/test_tool_queue.py, plugin/tests/test_todo.py, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-10-31T18:24:59Z
verified: strong
---
# Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and the fallback in use; fm todo and the end of the run list it, a no is remembered, and a yes resumes the work
## Raw request
> Install-grant queue (Mission 6, #5): fm ask --later queues a user-only grant that never expires, with the miss, the alternatives and the fallback in use; fm todo and the end of the run list it, a no is remembered, and a yes resumes the work
## Interpretation
Reading 1: Mission 6's install-grant queue is the capability-miss captures plus fm ask --later, recorded on the task itself and listed by fm todo (decisions.md 2026-10-31). Reading 2: build a separate queue store with its own surface. Rejected: the captures already persist and dedupe, so a second store would duplicate them.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm ask ID plugin --pin P --why W --later in full autonomy or headless records one request on task ID (an identical second one dedupes), logs grant_queued and grants nothing, with no new state file; fm todo lists the task first with what it unblocks; the request is still listed past APPROVAL_TTL; a request answered no logs grant_refused and the same pin is not requested again; fm mcp register records its plugin request; the task's other steps stay runnable — verify with `python3 plugin/tests/run.py test_todo test_tool_queue`
## Non-goals
## Approach (options → choice → why)
1) fm ask ID CATEGORY --pin TARGET --why ... --later (any user-only category: plugin, core, remote, and install once the guard has it) records the request on task ID: a structured grant-request line in its brief {category, pin, why, miss, alternatives from the last tool_search, fallback, at}, deduplicated by category and pin, logged as grant_queued, never expiring because the task is the record. A missing tool's request lands on its capability-miss capture task (T-2270). It grants nothing: the guard reads only the user's dialog answer. The step that needs the install waits (fm task defer --until 'installed NAME'); the rest runs on the fallback, logged provisional and recorded with fm decide --kind reversible. fm todo lists tasks with queued requests first; fm next says to raise them as fm ask dialogs at the end of the run, never mid-run; a no logs grant_refused and the same pin is never requested again; fm mcp register queues its plugin request. Fails if: the headless ask path still refuses, so fmhooks._ask_prompt lets --later through since it grants nothing. 2) Use what exists: today's free-text block, 'fm task block ... and stop'. Likely outcome: the whole task stops and the list can't be ranked, deduplicated or resumed. 3) Do less: only fm todo reading capability-miss captures, no --later. Fails if: pending approvals still expire after APPROVAL_TTL and the user gets no why or fallback. 4) A separate queue file. Breaks by that decision: a second store duplicating the captures. Choice 1 (80%): no new store, and the task is the durable record.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_hooks.py, plugin/lib/fmguard.py, plugin/tests/test_cli.py, README.md, plugin/tests/test_guard.py; past FIXes T-0875, T-0876, T-0877, T-0880, T-0907.
## Execution prompt
## Steps
1. [x] red tests first (test_tool_queue, test_todo): queue, dedupe, no grant, survives the TTL, refusal memory, fm mcp register, other steps runnable
2. [x] fm ask --later and the queue store (fmcli, fmhooks._ask_prompt lets --later through headless since it grants nothing)
3. [x] fm todo and fm next lines; grant_refused on a no; fm mcp register queues
4. [x] docs: MASTER.md, CHANGELOG.md
## Resume here
<!-- auto -->
- 2026-10-31T17:49:21Z step 1/4: red tests first (test_tool_queue, test_todo): queue, dedupe, no grant, survives the TTL, refusal memory, fm mcp register, other steps runnable
- git: worktree-agent-a448b421b7ff9c473; 6 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_todo.py, plugin/lib/fmgrants.py, plugin/tests/test_tool_queue.py
- touched since last checkpoint: plugin/lib/fmgrants.py, plugin/tests/test_tool_queue.py, plugin/tests/test_todo.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py
## Docs impact
CHANGELOG.md, MASTER.md (builder, fmgrants line)
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_todo test_tool_queue 2>&1 | tail -30` → ✗ exit 1 · Ran 25 tests in 11.6s (2 classes, 16 at a time; slowest: GrantQueue 10s, Todo 4s) / FAILED (2 classes: test_tool_queue.GrantQueue, test_todo.Todo) [ran] [tree 0703ed5f6852] (2026-10-31T17:47:53Z)
- (step 1) `python3 plugin/tests/run.py test_todo test_tool_queue` → ✗ exit 1 · Ran 25 tests in 8.9s (2 classes, 16 at a time; slowest: GrantQueue 9s, Todo 3s) / FAILED (2 classes: test_tool_queue.GrantQueue, test_todo.Todo) [ran] [tree 0703ed5f6852] (2026-10-31T17:48:15Z)
- (ac 1) `python3 plugin/tests/run.py test_todo test_tool_queue 2>&1 | tail -40` → ✗ exit 1 · Ran 25 tests in 20.4s (2 classes, 16 at a time; slowest: GrantQueue 20s, Todo 6s) / FAILED (1 classes: test_tool_queue.GrantQueue) [ran] [tree fafa9a54ba4c] (2026-10-31T17:50:52Z)
- (step 2) `python3 plugin/tests/run.py test_tool_queue` → exit 0 · Ran 16 tests in 24.0s (1 classes, 16 at a time; slowest: GrantQueue 24s) / OK [ran] [tree d7b2a1edffcc] (2026-10-31T17:52:41Z)
- (step 3) `python3 plugin/tests/run.py test_todo test_tool_queue` → exit 0 · Ran 25 tests in 24.7s (2 classes, 16 at a time; slowest: GrantQueue 24s, Todo 9s) / OK [ran] [tree d7b2a1edffcc] (2026-10-31T17:53:06Z)
- (step 4) `grep -c fmgrants MASTER.md` → exit 0 · 1 [ran] [tree d7b2a1edffcc] (2026-10-31T17:53:09Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_core test_docs test_drive_side test_guard_cases test_guard_evasions test_hooks test_mcp test_memory test_onwrite test_parallel test_paused test_robustness test_serve test_todo test_tool_loop test_tool_queue test_tool_taint test_ui_signals test_unattended test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [35.76s] [ran] [tree d7b2a1edffcc] (2026-10-31T17:56:26Z)
- (step 1) `python3 plugin/tests/run.py test_tool_queue test_todo test_hooks` → exit 0 · Ran 265 tests in 83.6s (33 classes, 16 at a time; slowest: Stop 83s, NoTaskGate 55s, PreToolUse 49s) / OK [ran] [tree dada2ccec507] (2026-10-31T18:29:35Z)
- (ac 1) `python3 plugin/tests/run.py test_todo test_tool_queue` → exit 0 · Ran 25 tests in 11.0s (2 classes, 16 at a time; slowest: GrantQueue 11s, Todo 4s) / OK [ran] [tree 877242ef34b5] (2026-10-31T18:30:02Z)
- (audit intent) `coordinator review in the main thread (pace gate held subagents): adversary on every grant path; one MEDIUM fixed red-first` → queued requests listed everywhere the final report reads; a yes resumes the task [tree 877242ef34b5] (2026-10-31T18:30:02Z)
- (audit adversary) `coordinator review in the main thread (pace gate held subagents): adversary on every grant path; one MEDIUM fixed red-first` → --later never creates a pending approval or dialog and never grants; _grant stays the only approval_granted writer; forged rows grant nothing [tree 877242ef34b5] (2026-10-31T18:30:02Z)
- (audit edge) `coordinator review in the main thread (pace gate held subagents): adversary on every grant path; one MEDIUM fixed red-first` → an ignored dialog leaves the request queued; dedupe by row; past APPROVAL_TTL still listed [tree 877242ef34b5] (2026-10-31T18:30:02Z)
- (audit operator) `coordinator review in the main thread (pace gate held subagents): adversary on every grant path; one MEDIUM fixed red-first` → no new state file; one Stop-line clause [tree 877242ef34b5] (2026-10-31T18:30:02Z)
## Log
- 2026-10-31T14:02:01Z created
- 2026-10-31T16:07:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2374.builder.md
- 2026-10-31T16:08:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2374.builder.md
- 2026-10-31T16:08:46Z builder slot freed
- 2026-10-31T16:11:16Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2374.builder.md
- 2026-10-31T16:11:16Z builder slot freed
- 2026-10-31T17:11:32Z ground: fm ask is fmcli.cmd_ask (:3819): pending asks are dicts {task, allow, why, session, at} with APPROVAL_TTL expiry, approval_requested logged, the user's yes applied only by fmhooks._grant (approval_granted). grant_queued is already read by fmmiss (T-2369) as a miss resolution, so --later must log exactly that kind. T-2357 (night timer install as one system ask) will reuse this queue, so it now depends on T-2374.
- 2026-10-31T17:13:00Z plan (second-plan review, taken): (1) resume: when the user's yes lands (fmhooks._grant logs approval_granted for a queued request), the queued line is marked granted and the task's defer clears in the same mutate, so fm next resumes it; a test covers yes→resume; (2) end of run: fm run's finish path and the Stop hook's final-report line print the queued requests (task, what it unblocks, the fm ask to raise), tested; (3) the headless --later path never reaches the grant code: negative tests that a queued record, a forged queued line or a --later in a non-headless session grants nothing; fmhooks._grant stays the only writer of approval_granted; (4) the queued line is a fixed-format row written and read by one parser with a round-trip test, and dedupe/refusal state is also on the ledger (grant_queued, grant_refused) so a brief edit can't drop a refusal; (5) no prior tool_search = no alternatives listed; no capture = queue on the named task.
- 2026-10-31T17:36:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2374.builder.md
- 2026-10-31T17:37:00Z focused
- 2026-10-31T17:37:00Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T17:40:43Z scope: widening to plugin/lib/fmserve.py::cmd_run (end-of-run listing per plan); leases on fmcli.py/fmserve.py taken with --warn: T-2353's lane edits other symbols in its own worktree, so the merges are textual and disjoint
- 2026-10-31T17:46:24Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmmcp.py', 'plugin/lib/fmgrants.py', 'plugin/lib/fmserve.py', 'plugin/tests/test_tool_queue.py', 'plugin/tests/test_todo.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-31T17:46:24Z scope widened: fmgrants.py (new module for the queue), fmserve.py (end-of-run listing)
- 2026-10-31T18:24:59Z merged worktree-agent-a448b421b7ff9c473 (9 file(s))
- 2026-10-31T18:26:08Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a448b421b7ff9c473
- 2026-10-31T18:26:09Z focused
- 2026-10-31T18:29:35Z scope: files outside the globs came from the lane merge and the review fix in fmhooks/test_tool_queue; changelog line next
- 2026-10-31T18:31:54Z done
- 2026-10-31T18:31:57Z committed e00fcd84 (3 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The "yes resumes the work" half of the request has no step or criterion. The only wiring is `fm task defer --until 'installed NAME'`, and nothing says what detects the grant, clears the defer, or restarts the step. The acceptance line covers queue, dedupe, no-grant, TTL, refusal and mcp regis…
- HIGH: "The end of the run list it" is only a `fm next` hint ("raise them as fm ask dialogs"), not an actual end-of-run listing. Nothing says where "end of run" is detected or that the list is shown. — Define the end-of-run hook, for example a final summary printed from the run-finish path. Add a te…
- HIGH: Letting `--later` through `fmhooks._ask_prompt` in headless mode is a change to the security guard, and the plan only says it "grants nothing". The safety claim ("guard reads only the user's dialog answer") is asserted, not tested. A bug here could let a queued record be read as an approval. …
- MEDIUM: Dedupe, refusal memory and "never expiring" live in a structured line inside the free-text brief, with no new state file. Parsing that line is fragile, since a brief edit or a task rewrite can corrupt or drop it, and a lost refusal means the same pin gets re-requested. — Specify the line fo…
- MEDIUM: The "alternatives from the last tool_search" and the capture-task routing (T-2270) depend on state that may be absent or stale (no prior search, or a task with no capture). The plan doesn't say what happens then. — Define the fallbacks (empty alternatives, queue on the named task) and cover…
- LOW: Acceptance has a single compound criterion with one verify command, so a partial failure is hard to attribute. "Still runnable" and "listed first" are also vague. — Split it into one criterion per behavior, each tied to a named test. Define the ordering rule for `fm todo`.
Verdict: revise — the resume and end-of-run parts of the request are unaddressed, and the guard change needs negative tests before coding starts.
## Dissent
- [ ] HIGH: The "yes resumes the work" half of the request has no step or criterion. The only wiring is `fm task defer --until 'installed NAME'`, and nothing says what detects the grant, clears the defer, or restarts the step. The acceptance line covers queue, dedupe, no-grant, TTL, refusal and mcp regis…
- [ ] HIGH: "The end of the run list it" is only a `fm next` hint ("raise them as fm ask dialogs"), not an actual end-of-run listing. Nothing says where "end of run" is detected or that the list is shown. — Define the end-of-run hook, for example a final summary printed from the run-finish path. Add a te…
- [ ] HIGH: Letting `--later` through `fmhooks._ask_prompt` in headless mode is a change to the security guard, and the plan only says it "grants nothing". The safety claim ("guard reads only the user's dialog answer") is asserted, not tested. A bug here could let a queued record be read as an approval. …
- [ ] MEDIUM: Dedupe, refusal memory and "never expiring" live in a structured line inside the free-text brief, with no new state file. Parsing that line is fragile, since a brief edit or a task rewrite can corrupt or drop it, and a lost refusal means the same pin gets re-requested. — Specify the line fo…
- [ ] MEDIUM: The "alternatives from the last tool_search" and the capture-task routing (T-2270) depend on state that may be absent or stale (no prior search, or a task with no capture). The plan doesn't say what happens then. — Define the fallbacks (empty alternatives, queue on the named task) and cover…
- [ ] LOW: Acceptance has a single compound criterion with one verify command, so a partial failure is hard to attribute. "Still runnable" and "listed first" are also vague. — Split it into one criterion per behavior, each tied to a named test. Define the ordering rule for `fm todo`.
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: Mission 6's install-grant queue is the capability-miss captures (one durable task per missing tool, filed once ever by the hook, the tool rung and t…
- T-2369 [FEATURE M, done, 4 steps] Miss joins the task (Mission 6, #5): a capability miss during an active task becomes its find-build-test-use step, and fm task finish r…
- T-2378 [FEATURE M, planned, 4 steps] #5 on every surface (Mission 6): fm code's shell failures get the miss note and the same finish checks, other agents get it through …
- research mission-20261031-083834: Request: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skil…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_hooks.py, plugin/tests/test_mcp.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmgrants.py, plugin/lib/fmhooks.py, plugin/lib/fmmcp.py, plugin/lib/fmserve.py, plugin/tests/test_todo.py, plugin/tests/…; re-ground the plan against them before editing
## Lessons
- Silence is not a refusal: remember only an explicit no, or one missed prompt suppresses a request forever
## Plan gaps
- failed first: step 1 red tests first (test_tool_queue, test_todo): queue, dedupe, no grant, survives the TTL, refusal me…
## Files touched
- plugin/lib/fmgrants.py
- plugin/tests/test_tool_queue.py
- plugin/tests/test_todo.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmserve.py
- plugin/lib/fmmcp.py
- MASTER.md
- CHANGELOG.md
- README.md
- plugin/lib/fmincident.py
- plugin/lib/fmlanes.py
- plugin/lib/fmlong.py
- plugin/lib/fmreverify.py
- plugin/skills/intake/SKILL.md
- plugin/skills/playbooks/references/ops/incident.md
- plugin/tests/test_incident.py
- plugin/tests/test_lanes.py
- plugin/tests/test_serve.py
