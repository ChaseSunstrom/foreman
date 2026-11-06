---
id: T-2270
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T04:49:50Z
updated: 2026-10-31T05:32:11Z
base: a9231d9370fd6b138970f0378be7aa922f59bd6b
base_tree: de8837abb0e00cdcd53c98fa279d77161570ecbe
plan0_at: 2026-10-31T05:21:00Z
plan0_scope: []
verified: strong
---
# Capability-miss trigger (Mission 6, #5): a missing command or module names the find-or-build path once per session, and a tool missing in 2+ sessions becomes one find-or-build task
## Raw request
> Capability-miss trigger (Mission 6, #5): a missing command or module names the find-or-build path once per session, and a tool missing in 2+ sessions becomes one find-or-build task
## Interpretation
Gap map #5: failure_class (fmcli.py:4878) recognizes 'command not found' / 'No module named' only to excuse a red gate; nothing turns 'I can't do X' into finding or building X. fmplugins' suggest is never called. A session that hits a missing tool improvises or gives up, and the next session hits it again.
## Assumptions (confidence)
## Acceptance criteria
- [x] a Bash failure with 'command not found: X', 'No module named X' or 'Cannot find module X' gets one short note naming X and the path (fm plugins find X; an install needs fm ask ID plugin; or build a script with its test), once per session per tool; the second session that misses X captures one FEATURE task for it (source self), never two; a name that isn't a plain tool name is ignored; subagent failures stay out (T-1110) — verify with `python3 plugin/tests/run.py test_hooks test_plugins`
## Non-goals
## Approach (options → choice → why)
1) in the PostToolUseFailure hook (main thread only, T-1110): parse the missing name with one regex over the error (a plain tool name, [A-Za-z0-9_.+-]{1,64}, else ignored), add a ≤300-char note once per session per name (hook state g), log a capability_miss ledger event; when the ledger shows the name missed in a second session, fmeco.capture_once a FEATURE 'Missing tool X: find it (fm plugins find X) or build it (script + test)', source self. 2) call fmplugins.find in the hook — rejected: hooks stay fast and local. 3) capture on the first miss — rejected: typos would flood the inbox. Choice 1.
## Risks and rollback
A misspelled command reads as a missing tool: the note costs one line, and capture waits for a second session. The name is untrusted text: plained and fitted before it enters a note or a task.
## Execution prompt
## Steps
1. [x] red tests through the PostToolUseFailure hook: note once, capture on the second session, odd names ignored, subagent ignored
2. [x] fmhooks.post_tool_use_failure: parse the missing name, note, ledger event, capture_once
3. [x] docs: MASTER hooks line, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_hooks test_plugins 2>&1 | tail -25` → ✗ exit 1 · Ran 241 tests in 58.2s (34 classes, 16 at a time; slowest: Stop 56s, NoTaskGate 37s, PreToolUse 32s) / FAILED (1 classes) [ran] [tree e3594931ee32] (2026-10-31T05:22:28Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_plugins` → exit 0 · Ran 241 tests in 61.3s (34 classes, 16 at a time; slowest: Stop 61s, NoTaskGate 39s, PreToolUse 33s) / OK [ran] [tree 8604e9fccdc0] (2026-10-31T05:24:40Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_compact test_docs test_drive_side test_edit_cards test_goal test_guard_evasions test_hooks test_memory test_onwrite test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.83s] [ran] [tree 8604e9fccdc0] (2026-10-31T05:25:44Z)
- `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 219 tests in 35.0s (29 classes, 16 at a time; slowest: Stop 34s, NoTaskGate 24s, PreToolUse 19s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 3764f6f58280] (2026-10-31T05:28:09Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 219 tests in 37.3s (29 classes, 16 at a time; slowest: Stop 37s, NoTaskGate 26s, PreToolUse 22s) / OK [ran] [tree 3764f6f58280] (2026-10-31T05:28:09Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_plugins test_docs` → exit 0 · Ran 322 tests in 40.4s (55 classes, 16 at a time; slowest: Stop 40s, NoTaskGate 30s, PreToolUse 25s) / OK [ran] [tree 3764f6f58280] (2026-10-31T05:28:50Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_plugins test_docs` → exit 0 · Ran 322 tests in 42.9s (55 classes, 16 at a time; slowest: Stop 43s, NoTaskGate 31s, PreToolUse 26s) / OK [ran] [tree 3764f6f58280] (2026-10-31T05:29:33Z)
- (step 3) `grep -c T-2270 MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree 3764f6f58280] (2026-10-31T05:29:33Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_plugins` → exit 0 · Ran 241 tests in 62.6s (34 classes, 16 at a time; slowest: Stop 62s, NoTaskGate 44s, PreToolUse 38s) / OK [ran] [tree 3764f6f58280] (2026-10-31T05:30:46Z)
- (audit intent) `self-review of the diff: session field matches the ledger's session_id, capture keyed once ever, name validated by fullmatch before use and plained in the note, no network in the hook; test_hooks red-to-green` → a missing command or module names fm plugins find / build-with-a-test once per session; a second session's miss captures one FEATURE (Mission 6, #5's capability-miss trigger) [tree 3764f6f58280] (2026-10-31T05:30:46Z)
- (audit adversary) `self-review of the diff: session field matches the ledger's session_id, capture keyed once ever, name validated by fullmatch before use and plained in the note, no network in the hook; test_hooks red-to-green` → the name comes from tool output: only [A-Za-z0-9_.+-]{1,64} passes, then plained and fitted; subagent failures stay out (T-1110) [tree 3764f6f58280] (2026-10-31T05:30:46Z)
- (audit edge) `self-review of the diff: session field matches the ledger's session_id, capture keyed once ever, name validated by fullmatch before use and plained in the note, no network in the hook; test_hooks red-to-green` → a typo reads as a missing tool, so capture waits for a second session; the error is scanned only in its last 4000 chars [tree 3764f6f58280] (2026-10-31T05:30:46Z)
## Log
- 2026-10-31T04:49:50Z created
- 2026-10-31T05:20:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2270.builder.md
- 2026-10-31T05:20:59Z focused
- 2026-10-31T05:26:55Z merged worktree-agent-a764390b1b07317db (4 file(s))
- 2026-10-31T05:26:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a764390b1b07317db
- 2026-10-31T05:26:56Z focused
- 2026-10-31T05:29:43Z scope: plugin/lib/fmhooks.py (_capability_miss), plugin/tests/test_hooks.py, MASTER.md, CHANGELOG.md
- 2026-10-31T05:32:11Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: [revisited: every capability genesis builds must be called] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3…
## Lessons
- A trigger fed by tool output should key once-per-session on the ledger it already writes, so the memory across sessions comes free
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
