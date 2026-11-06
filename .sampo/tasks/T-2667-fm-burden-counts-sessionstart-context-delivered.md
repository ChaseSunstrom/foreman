---
id: T-2667
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T20:44:49Z
updated: 2026-11-02T20:50:25Z
builder_model: sonnet
base: 6716f9643748e59cddc470562a16753eaa827391
base_tree: b0b4477ba78db91a673827bc4ac6e8130e8cfa6c
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T20:46:02Z
plan0_scope: []
lane_stop: merged 2026-11-02T20:49:03Z
verified: strong
unproven: [docs, meaning]
---
# fm burden counts SessionStart context delivered as hook_success stdout, and fm burden --by-source splits injected characters by note source
## Raw request
> FIX: fm burden counts SessionStart context delivered as hook_success stdout (additionalContext), which fmcost.INJECTS misses, and fm burden --by-source lists each note source (SessionStart, stack card, ambient tests, Next, guard) by chars per turn; MASTER and CHANGELOG say it
> CONTEXT: Genesis gen-3 Mission 5 (#12 staying lean and safe), gen-3/mission-staying-lean-and-safe.md
## Interpretation
1. (chosen) Count what reaches the model: a hook_success attachment's stdout is the hook's JSON; its hookSpecificOutput.additionalContext (and systemMessage) go into context, so they count when they are Foreman's. Group by the attachment's hookName (SessionStart:resume, PreToolUse:Bash, …) for --by-source.
2. Count every hook_success stdout byte. Rejected: PostToolUse's updatedToolOutput replaces tool output the model would see anyway; counting it whole would charge Foreman for the tool's own output.
## Assumptions (confidence)
## Acceptance criteria
- [x] a transcript whose SessionStart hook_success stdout carries additionalContext adds its characters to injected chars, and fm burden --by-source lists each source (SessionStart, PreToolUse notes such as stack cards and ambient tests, PostToolUse, Stop, guard refusals) with chars per turn, biggest first — verify with `python3 plugin/tests/run.py test_burden_sources`
## Non-goals
## Approach (options → choice → why)
1. In fmcost.burden, parse hook_success stdout as JSON and add additionalContext and systemMessage lengths when Foreman's; keep per-source tallies keyed by hookName (or the attachment type for the other INJECTS kinds); --by-source prints them per turn, biggest first. Likely outcome: the 7-day number rises several-fold and SessionStart leads. Fails if: Claude Code changes the attachment shape again (the reader keeps the old content path as well).
2. use what exists: read the hooks' own logs (state/logs) for what each hook emitted. Fails if: the logs don't record emitted text sizes per session, and they'd miss what Claude Code dropped or truncated (hook context over ~10 KB becomes a preview).
3. do less: add hook_success to INJECTS only. Fails if: its content field is empty for SessionStart (the text is in stdout), so nothing more is counted.
Choice 1 (88%): it counts what the transcript shows reached the model, from the same pass burden already makes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a hook_success SessionStart attachment is counted, and --by-source splits sources
2. [x] fmcost.burden reads hook_success stdout's additionalContext (only Foreman's) and tallies by hookName; --by-source in fmcli
3. [x] record fm burden --days 7 before and after in the brief; CHANGELOG and MASTER (fmcost line)
## Resume here
## Docs impact
CHANGELOG.md and MASTER.md (fmcost line)
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_burden_sources 2>&1 | tail -5` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: BurdenSources 0s) / FAILED (1 classes: test_burden_sources.BurdenSources) [ran] [tree 66c91b85234c] [world 2f1906870a] (2026-11-02T20:46:24Z)
- (step 1) `python3 plugin/tests/run.py test_burden_sources` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: BurdenSources 0s) / OK [ran] [tree 349853fab470] [world 2f1906870a] (2026-11-02T20:46:54Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_burden_sources test_cli test_cost test_cost_forecast test_economics test_export test_guard_cases test_paused test_robustness test_round_g test_trials test_usage_burn test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.78s] [ran] [tree 349853fab470] [world 2f1906870a] (2026-11-02T20:47:30Z)
- `python3 plugin/tests/run.py test_burden_sources` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: BurdenSources 0s) / FAILED (1 classes: test_burden_sources.BurdenSources) (start tree + this task's tests) [ran] [tree 37b2f64af94a] [world 2f1906870a] (2026-11-02T20:49:15Z)
- `python3 plugin/tests/run.py test_burden_sources` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: BurdenSources 0s) / OK [ran] [tree 37b2f64af94a] [world 2f1906870a] (2026-11-02T20:49:15Z)
- (step 2) `python3 plugin/tests/run.py test_burden_sources test_flywheel` → exit 0 · Ran 3 tests in 0.5s (3 classes, 16 at a time; slowest: Candidate 0s, Burden 0s, BurdenSources 0s) / OK [ran] [tree 37b2f64af94a] [world 2f1906870a] (2026-11-02T20:49:16Z)
- (step 3) `fm burden --days 7 --by-source` → exit 0 · UserPromptSubmit: 0.7 / PostToolUseFailure: 0.5 [ran] [tree 37b2f64af94a] [world 2f1906870a] (2026-11-02T20:49:23Z)
- (ac 1) `python3 plugin/tests/run.py test_burden_sources` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T20:49:15Z [ran] [tree 37b2f64af94a] [world 2f1906870a] (2026-11-02T20:49:30Z)
- (audit intent) `self: reviewed the builder diff; hook_success stdout is parsed defensively (non-JSON or non-dict skipped), only additionalContext and systemMessage count, never updatedToolOutput; the per-source keys ride in the same per-session counter and cmd_burden prints named keys only` → the Mission's baseline (26 and 49 chars per turn) read low; the recount says why (SessionStart uncounted) and the new split names the biggest source [tree 37b2f64af94a] (2026-11-02T20:49:30Z)
- (audit edge) `self: reviewed the builder diff; hook_success stdout is parsed defensively (non-JSON or non-dict skipped), only additionalContext and systemMessage count, never updatedToolOutput; the per-source keys ride in the same per-session counter and cmd_burden prints named keys only` → a stdout that isn't JSON, or a hook_success with no Foreman text, adds nothing; guard refusals stay under hook_blocking_error rather than a separate guard label [tree 37b2f64af94a] (2026-11-02T20:49:30Z)
## Log
- 2026-11-02T20:44:49Z created
- 2026-11-02T20:45:44Z planned from capture
- 2026-11-02T20:45:50Z criterion 1 verify: `python3 plugin/tests/run.py test_burden` → `python3 plugin/tests/run.py test_burden_sources`
- 2026-11-02T20:45:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2667.builder.md
- 2026-11-02T20:46:02Z focused
- 2026-11-02T20:46:02Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T20:46:14Z before: working copy 2 sessions 24946 turns injected 48 chars/turn; unknown 384 sessions 10249 turns injected 26 chars/turn
- 2026-11-02T20:46:53Z after: working copy 24949 turns injected 76 chars/turn (was 48); unknown 51 (was 26); by-source: SessionStart 42.9, Stop 14.5, PreToolUse 9.0
- 2026-11-02T20:49:03Z merged worktree-agent-aa1554639d4ec5a8b (3 file(s))
- 2026-11-02T20:49:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa1554639d4ec5a8b
- 2026-11-02T20:49:09Z focused
- 2026-11-02T20:50:22Z done
- 2026-11-02T20:50:25Z committed 2317c37e (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- decision 2026-11-02: Recommendation: Mission 5 builds three measured gaps (burden counts hook_success SessionStart context and splits it by source; a guard latency test …
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
## Why not caught
burden's test fed only the attachment types it counted; no test used a real transcript's hook_success shape
## Lessons
- When a measure reads low, check what the reader skips before trusting it: Claude Code's attachment shapes change and a reader keyed on one type misses the rest
## Files touched
- plugin/tests/test_burden_sources.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
