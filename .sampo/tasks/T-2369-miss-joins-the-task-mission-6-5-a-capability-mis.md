---
id: T-2369
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_tool_loop.py, plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-31T14:01:48Z
updated: 2026-10-31T14:52:50Z
builder_model: sonnet
base: 6a000b622daaff04d314e78891773d662493268d
base_tree: 2f3e60a6c6093f65ce316c4e332916993bfdbfd2
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T14:14:21Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_tool_loop.py, plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Miss joins the task (Mission 6, #5): a capability miss during an active task becomes its find-build-test-use step, and fm task finish refuses the task while the miss is unresolved
## Raw request
> Miss joins the task (Mission 6, #5): a capability miss during an active task becomes its find-build-test-use step, and fm task finish refuses the task while the miss is unresolved
## Interpretation
Gap map #5, capability-miss trigger (tier 4). T-2270 notes a missing command once per session and captures a task on a second session, so the task that met the miss goes on without the tool and the fix waits for some later task: Foreman advises and stops (the gen-1 Seed's cross-cutting finding). With a task active, the miss is that task's to resolve: find it (fm which), build and test it (fm new tool), use it, or queue the user's grant with a fallback; the task can't close while it sits open.
## Assumptions (confidence)
## Acceptance criteria
- [x] a missing command during an active task logs capability_miss with the task and the command; fm next names the open miss; fm task finish refuses on every try while it is unresolved and closes only after a later green run of the same command or of the command fmfixes pairs with it, a tool_proved event naming it, or a grant_queued event naming it plus a green run of the fallback step; a red-first test's missing module resolves only when that test command goes green; no typed line, flag or file's existence resolves a miss; a task with no miss gets no new check — verify with `python3 plugin/tests/run.py test_hooks test_tool_loop`
## Non-goals
## Approach (options → choice → why)
1) Ledger-driven: the capability_miss event gains the active task id and the failing command (fitted, redacted); fm next leads with an open miss and its paths; fm task finish refuses, every time, while a miss logged on the task is unresolved. Resolved only by run evidence, never by a typed claim or a file's existence: a later exit 0 of the same command in that task (which also covers a red-first test whose missing module the task then writes: the same test command goes green), or the later green run fmfixes pairs with the failure as what got past it (T-1032); a tool_proved event naming the miss (brief 4 writes it from runs); or a grant_queued event naming it (brief 6) plus a green run of the step that used the fallback. No flag exempts anything. The way out short of resolving is the usual one: fm task block ID with the diagnosis, so the session is never trapped and the task never closes on an open miss. A task with no miss pays nothing new. 2) A Tools section the hook writes into the brief: rejected, a hook editing brief text races the session's own edits and the ledger already holds every fact. 3) A toolsmith lane per miss: rejected, the task waits on a merge for each small tool and the proof is the same either way (brief 4); the step may still choose a lane for an M-size tool. Choice 1: the smallest change that turns the note into a closed loop.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmguard.py, plugin/tests/test_cli.py, plugin/tests/test_guard.py, README.md, plugin/lib/fmgenesis.py; past FIXes T-0875, T-0876, T-0877, T-0880, T-0907.
## Execution prompt
## Steps
1. [x] red tests first (test_tool_loop, test_hooks): miss logged with task and command, fm next names it, finish refuses and then accepts each of the four resolutions, an expect-fail run ignored, a task with no miss unchanged
2. [x] fmhooks._capability_miss records the active task and the command; fmcore.next_action leads with an open miss
3. [x] fm task finish's miss check: one refusal naming each open miss, counted with finish's retries
4. [x] docs: MASTER.md (hooks and finish lines), CHANGELOG.md
## Resume here
<!-- auto -->
- 2026-10-31T14:38:52Z steps 4/4 done
- git: worktree-agent-ad410ef21e04e069f; 2 uncommitted: plugin/lib/fmmiss.py, plugin/tests/test_tool_loop.py
- touched since last checkpoint: plugin/tests/test_hooks.py, MASTER.md, plugin/tests/test_tool_loop.py, plugin/lib/fmmiss.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tool_loop` → red as expected (exit 1) · Ran 13 tests in 37.3s (1 classes, 16 at a time; slowest: MissLoop 36s) / FAILED (1 classes: test_tool_loop.MissLoop) [ran] [tree 982aeba1b9f4] (2026-10-31T14:21:24Z)
- (step 2) `python3 plugin/tests/run.py test_tool_loop 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)|Error|assert" | head -30` → exit 0 · Ran 13 tests in 42.5s (1 classes, 16 at a time; slowest: MissLoop 41s) / OK [ran] [tree 256acfdfa0a8] (2026-10-31T14:24:44Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_tool_loop 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)|Error|assert" | head -30` → ✗ exit 1 · Ran 242 tests in 78.9s (31 classes, 16 at a time; slowest: Stop 79s, NoTaskGate 46s, PreToolUse 37s) / FAILED (1 classes: test_hooks.CapabilityMiss) [ran] [tree ed76628b5998] (2026-10-31T14:26:11Z)
- (step 3) `python3 plugin/tests/run.py test_hooks 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)|Error|assert" | head -30` → exit 0 · Ran 230 tests in 101.8s (30 classes, 16 at a time; slowest: Stop 101s, NoTaskGate 71s, PreToolUse 69s) / OK [ran] [tree 62e876148642] (2026-10-31T14:28:04Z)
- (step 2) `python3 plugin/tests/run.py test_tool_loop test_hooks` → exit 0 · Ran 243 tests in 129.6s (31 classes, 16 at a time; slowest: Stop 129s, NoTaskGate 72s, PreToolUse 69s) / OK [ran] [tree 62e876148642] (2026-10-31T14:30:17Z)
- (step 3) `python3 plugin/tests/run.py test_tool_loop` → exit 0 · Ran 13 tests in 36.1s (1 classes, 16 at a time; slowest: MissLoop 36s) / OK [ran] [tree 62e876148642] (2026-10-31T14:30:57Z)
- (step 4) `grep -c T-2369 MASTER.md` → exit 0 · 3 [ran] [tree 4748cdd06b2e] (2026-10-31T14:31:10Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_compact test_core test_docs test_drive_side test_fixes test_guard_cases test_guard_evasions test_hooks test_memory test_onwrite test_paused test_robustness test_tool_loop test_tool_taint test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.54s] [ran] [tree 4748cdd06b2e] (2026-10-31T14:32:11Z)
- (step 1) `python3 plugin/tests/run.py test_tool_loop` → red as expected (exit 1) · Ran 17 tests in 40.0s (1 classes, 16 at a time; slowest: MissLoop 40s) / FAILED (1 classes: test_tool_loop.MissLoop) [ran] [tree ea606882fd96] (2026-10-31T14:38:35Z)
- (step 2) `python3 plugin/tests/run.py test_tool_loop test_hooks` → exit 0 · Ran 247 tests in 64.8s (31 classes, 16 at a time; slowest: Stop 64s, MissLoop 43s, NoTaskGate 40s) / OK [ran] [tree a2557d59b6af] (2026-10-31T14:43:36Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_compact test_core test_docs test_drive_side test_fixes test_guard_cases test_guard_evasions test_hooks test_memory test_onwrite test_paused test_robustness test_tool_loop test_tool_taint test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [15.53s] [ran] [tree a2557d59b6af] (2026-10-31T14:45:09Z)
- (step 2) `python3 plugin/tests/run.py test_tool_loop test_hooks` → exit 0 · Ran 247 tests in 124.4s (31 classes, 16 at a time; slowest: Stop 124s, NoTaskGate 67s, PreToolUse 65s) / OK [ran] [tree aed41fa19192] (2026-10-31T14:48:56Z)
- (step 4) `grep -q 'T-2369' MASTER.md && grep -q 'T-2369' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 995a4ec41c7b] (2026-10-31T14:49:28Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_tool_loop` → exit 0 · Ran 247 tests in 123.1s (31 classes, 16 at a time; slowest: Stop 121s, NoTaskGate 72s, PreToolUse 67s) / OK [ran] [tree 995a4ec41c7b] (2026-10-31T14:51:34Z)
- (audit intent) `one fm-reviewer pass (all five lenses): changes needed; all fixed on the branch: no file resolves a miss (the _written branch removed), readers check only the ledger (PostToolUse logs miss_resolved; no events.jsonl scan, next_for with an open miss ~2.4 ms), passes count only from the task's own sessions, whole-command keys with cd prefixes stripped, pairings count only when the tool is present now and never for touch/mkdir/true, refusal prints the full command defanged with the evidence form, close gates fail open; 247 tests OK after merge` → a miss is the task's to resolve; only a later passing run of the same command, a proved tool or a queued grant plus a passing fallback closes it (tested) [tree 995a4ec41c7b] (2026-10-31T14:51:34Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): changes needed; all fixed on the branch: no file resolves a miss (the _written branch removed), readers check only the ledger (PostToolUse logs miss_resolved; no events.jsonl scan, next_for with an open miss ~2.4 ms), passes count only from the task's own sessions, whole-command keys with cd prefixes stripped, pairings count only when the tool is present now and never for touch/mkdir/true, refusal prints the full command defanged with the evidence form, close gates fail open; 247 tests OK after merge` → touch NAME, a file named after the module, another lane's run and a typed line each resolve nothing (tested) [tree 995a4ec41c7b] (2026-10-31T14:51:34Z)
- (audit operator) `one fm-reviewer pass (all five lenses): changes needed; all fixed on the branch: no file resolves a miss (the _written branch removed), readers check only the ledger (PostToolUse logs miss_resolved; no events.jsonl scan, next_for with an open miss ~2.4 ms), passes count only from the task's own sessions, whole-command keys with cd prefixes stripped, pairings count only when the tool is present now and never for touch/mkdir/true, refusal prints the full command defanged with the evidence form, close gates fail open; 247 tests OK after merge` → no per-prompt events scan; on_pass costs ~3.5 ms per passing main-thread Bash call [tree 995a4ec41c7b] (2026-10-31T14:51:34Z)
- (audit edge) `one fm-reviewer pass (all five lenses): changes needed; all fixed on the branch: no file resolves a miss (the _written branch removed), readers check only the ledger (PostToolUse logs miss_resolved; no events.jsonl scan, next_for with an open miss ~2.4 ms), passes count only from the task's own sessions, whole-command keys with cd prefixes stripped, pairings count only when the tool is present now and never for touch/mkdir/true, refusal prints the full command defanged with the evidence form, close gates fail open; 247 tests OK after merge` → a command over 1000 chars compares on its cut; a session older than the 1500-event tail resolves by a (ran] line instead [tree 995a4ec41c7b] (2026-10-31T14:51:34Z)
- (audit maintainer) `one fm-reviewer pass (all five lenses): changes needed; all fixed on the branch: no file resolves a miss (the _written branch removed), readers check only the ledger (PostToolUse logs miss_resolved; no events.jsonl scan, next_for with an open miss ~2.4 ms), passes count only from the task's own sessions, whole-command keys with cd prefixes stripped, pairings count only when the tool is present now and never for touch/mkdir/true, refusal prints the full command defanged with the evidence form, close gates fail open; 247 tests OK after merge` → the tool_proved/grant_queued payload contract is in fmmiss's docstring for briefs 3-4 to emit [tree 995a4ec41c7b] (2026-10-31T14:51:34Z)
## Log
- 2026-10-31T14:01:48Z created
- 2026-10-31T14:14:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2369.builder.md
- 2026-10-31T14:14:21Z focused
- 2026-10-31T14:14:21Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T14:18:03Z scope: new module plugin/lib/fmmiss.py and fmfixes.py (on_success returns the paired failure) keep fmcore/fmcli edits small
- 2026-10-31T14:22:03Z scope: plugin/lib/fmmiss.py (new), plugin/lib/fmfixes.py (on_success returns the failed command it paired with, for the fix_paired event)
- 2026-10-31T14:42:31Z scope: fmfixes.py docstring (on_success return, fix_paired) per review item 7
- 2026-10-31T14:46:47Z merged worktree-agent-ad410ef21e04e069f (8 file(s))
- 2026-10-31T14:46:48Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad410ef21e04e069f
- 2026-10-31T14:46:48Z focused
- 2026-10-31T14:49:28Z scope: plugin/lib/fmmiss.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmfixes.py, plugin/tests/test_tool_loop.py, plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md
- 2026-10-31T14:52:48Z done
- 2026-10-31T14:52:50Z committed 82f270ba (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261031-083834: Request: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skil…
- research mission-20261031-083834.pack: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skill or…
- research mission-20261031-083838.pack: Mission 8, Genesis gen 1: 7. Self-repair and self-improvement. Its own failures, friction, misses and my corrections become fixes,…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Lessons
- A resolution path a no-op command can trigger is a typed claim in disguise: require the capability to actually exist
## Files touched
- plugin/lib/fmmiss.py
- plugin/tests/test_tool_loop.py
- plugin/lib/fmhooks.py
- plugin/lib/fmfixes.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/tests/test_hooks.py
- MASTER.md
- plugin/tests/test_zz_timing.py
- CHANGELOG.md
