---
id: T-1760
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, README.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-23T07:42:12Z
updated: 2026-10-23T07:54:33Z
batch: [T-1373, T-1374, T-1402]
base: db53acc9d02ed2a0e48917f65cf0ffd57df3a920
base_tree: da72c2c94a20ec95efe5abeac1d422f2f88a513f
plan0_at: 2026-10-23T07:44:12Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_code_tui.py, README.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code diagnostics: fm code why explains a run, piped stdin is the request's context, and the start event and the app …
## Raw request
> T-1373: fm code why ID: explains a run from its journal and events (status, where it stopped, a stall's cause, the next command); and the TUI's stalled card with w wait / k kill / m switch runner (T-1336 follow-up)
> T-1374: echo ctx | fm code "<request>": a request with stdin piped reads it as context for the plan (T-1343 follow-up, U1)
> T-1402: FEATURE: fm code's start event names its containment (guard only, or the OS primitive found) and the app shows it (S15, A11)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: with the probe stubbed off the start event says guard only; the run view shows the label
## Interpretation
Do T-1373, T-1374, T-1402 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1760. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1373: fm code why [ID] explains a run from its journal and events: how it ended (closed, blocked, error, stopped by a kill, or running), the last step or round done, a stall's cause, and the one command to run next — verify with `python3 plugin/tests/run.py test_code.Why`
- [x] T-1374: a request with stdin piped (a pipe or file, up to 256 KB, a few seconds at most) gets it as fenced context in the plan and work prompts; a terminal or an empty pipe adds nothing — verify with `python3 plugin/tests/run.py test_code.PipedContext`
- [x] T-1402: the start event names the run's containment (Landlock with its ABI, or guard only) and the app's header shows it — verify with `python3 plugin/tests/run.py test_code.Failures test_code_tui.Waiting`
## Non-goals
## Approach (options → choice → why)
why(): read code/<ID>.events.jsonl (newest when no ID) and the journal's phase_done records; ended = closed/blocked/error event, else running when the task lock is held, else stopped by a kill; next = the event's next, or resume for a stopped run. Piped context: only when stdin is a FIFO or regular file and not a terminal, select up to 1 s for the first byte, then read until EOF, 256 KB or 5 s (a pipe that never closes, as in Claude Code's Bash tool, can't hang a run); kept as run.context and journaled, fenced into _task_text and the plan prompt. Containment: worker_confinement's paths → 'Landlock (ABI N)' else 'guard only', on the start event as containment {kind, label} and the app header's right side. Options for why: a TUI-only view (no CLI for scripts), reading fm task show (no stall or journal facts), or this CLI that the app can call later (chosen). Captured instead: the app's stalled card with w/k/m keys.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1373: Fm code why ID: explains a run from its journal and events (status, where it stopped, a st
2. [x] T-1374: Echo ctx | fm code "<request>": a request with stdin piped reads it as context for the pla
3. [x] T-1402: Fm code's start event names its containment (guard only, or the OS primitive found) and th
## Resume here
<!-- auto -->
- 2026-10-23T07:45:57Z step 1/3: T-1373: Fm code why ID: explains a run from its journal and events (status, where it stopped, a st
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/confirm_edits.txt
## Docs impact
README fm code section, CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code test_code_worker test_code_tui test_code_fakes test_code_hardening test_code_bench test_code_envelope test_code_truncation test_code_write_hygiene test_cli` → exit 0 · ✓ exit 0 (85.0 s) · OK [ran] [tree 510de6a9d1d0] (2026-10-23T07:51:00Z)
- (step 1) `python3 plugin/tests/run.py test_code.Why` → exit 0 · Ran 4 tests in 3.9s (1 classes, 16 at a time; slowest: Why 4s) / OK [ran] [tree 510de6a9d1d0] (2026-10-23T07:51:14Z)
- (step 2) `python3 plugin/tests/run.py test_code.PipedContext` → exit 0 · Ran 2 tests in 2.7s (1 classes, 16 at a time; slowest: PipedContext 3s) / OK [ran] [tree 510de6a9d1d0] (2026-10-23T07:51:17Z)
- (step 3) `python3 plugin/tests/run.py test_code.Failures test_code_tui.Waiting` → exit 0 · Ran 9 tests in 4.8s (2 classes, 16 at a time; slowest: Failures 5s, Waiting 0s) / OK [ran] [tree 510de6a9d1d0] (2026-10-23T07:51:22Z)
- (audit intent) `self: the three members re-read` → pass: why explains closed, blocked and killed runs with the next command; piped context reaches the plan and work prompts; containment on the start event and in the header. The stalled card's keys captured as T-1761 [tree 14aa1da7400d] (2026-10-23T07:51:23Z)
- (ac 1) `python3 plugin/tests/run.py test_code.Why` → exit 0 · Ran 4 tests in 3.9s (1 classes, 16 at a time; slowest: Why 4s) / OK [ran] [tree 14aa1da7400d] (2026-10-23T07:51:44Z)
- (ac 2) `python3 plugin/tests/run.py test_code.PipedContext` → exit 0 · Ran 2 tests in 2.7s (1 classes, 16 at a time; slowest: PipedContext 3s) / OK [ran] [tree 14aa1da7400d] (2026-10-23T07:51:44Z)
- (ac 3) `python3 plugin/tests/run.py test_code.Failures test_code_tui.Waiting` → exit 0 · Ran 9 tests in 4.7s (2 classes, 16 at a time; slowest: Failures 5s, Waiting 0s) / OK [ran] [tree 14aa1da7400d] (2026-10-23T07:51:44Z)
- (audit intent) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → all three criteria met; the stalled card's keys captured as T-1761 [tree 14aa1da7400d] (2026-10-23T07:51:44Z)
- (audit adversary) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → piped text is fenced as data in every prompt it reaches, bounded at 256 KB; fm code why takes only an ID matching T-NNNN, so its glob can't reach outside the code folder [tree 14aa1da7400d] (2026-10-23T07:51:44Z)
- (audit edge) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → a terminal, /dev/null or an empty pipe adds nothing; a pipe that never closes costs one second, never a hang; a resumed run keeps its context from the journal; why with no end event tells a live run (lock held) from a killed one [tree 14aa1da7400d] (2026-10-23T07:51:44Z)
## Log
- 2026-10-23T07:42:12Z created
- 2026-10-23T07:42:28Z criterion 1 text: T-1373: Fm code why ID: explains a run from its journal and events (status, where it stopped, a st works → T-1373: fm code why [ID] explains a run from its journal and events: how it ended (closed, blocked, error, stopped by a kill, or running), the last step or round done, a stall's cause, and the one command to run next :: python3 plugin/tests/run.py test_code.Why
- 2026-10-23T07:42:28Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_code.Why`
- 2026-10-23T07:42:29Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_code.PipedContext`
- 2026-10-23T07:42:29Z criterion 2 text: T-1374: Echo ctx | fm code "<request>": a request with stdin piped reads it as context for the pla works → T-1374: a request with stdin piped (a pipe or file, up to 256 KB, a few seconds at most) gets it as fenced context in the plan and work prompts; a terminal or an empty pipe adds nothing
- 2026-10-23T07:42:29Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_code.Failures test_code_tui.Waiting`
- 2026-10-23T07:42:29Z criterion 3 text: T-1402: with the probe stubbed off the start event says guard only; the run view shows the label → T-1402: the start event names the run's containment (Landlock with its ABI, or guard only) and the app's header shows it
- 2026-10-23T07:42:38Z criterion 1 text: T-1373: fm code why [ID] explains a run from its journal and events: how it ended (closed, blocked, error, stopped by a kill, or running), the last step or round done, a stall's cause, and the one command to run next :: python3 plugin/tests/run.py test_code.Why → T-1373: fm code why [ID] explains a run from its journal and events: how it ended (closed, blocked, error, stopped by a kill, or running), the last step or round done, a stall's cause, and the one command to run next
- 2026-10-23T07:42:39Z set scope=['plugin/lib/fmcode.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code.py', 'plugin/tests/test_code_tui.py', 'README.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:44:11Z focused
- 2026-10-23T07:45:58Z paused: focus moved to T-1369
- 2026-10-23T07:49:15Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-23T07:49:15Z focused
- 2026-10-23T07:54:31Z done
- 2026-10-23T07:54:33Z committed 64f9412a (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1754 [FEATURE M, done, 3 steps] fm code: a Next: line on every failure, the start event names the Foreman running it, and a registry that stops runners… — lesson: A re…
- T-1740 [FEATURE M, done, 3 steps] fm code TUI: waiting cues (title, bell, why-waiting line), press-twice quit and key help, a half-block canvas for the c… — lesson: Conf…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py
## Lessons
- Reading stdin in a CLI that agents run needs a FIFO/file check and a deadline: their stdin is often a pipe that never closes
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_code_tui.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- MASTER.md
- README.md
