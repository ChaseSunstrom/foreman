---
id: T-1293
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T21:10:25Z
updated: 2026-10-20T23:54:08Z
base: a17c840471c7e57189a3756b4aa6198bb3bce0f6
base_tree: 152ea5ee5a2d6ed90715c3963e9e1bbafe556c16
plan0_at: 2026-10-20T23:28:40Z
plan0_scope: []
verified: strong
---
# The script-verdict cache key includes where Foreman's state lives (state_dir and its fallbacks), as it does the scratch folders
## Raw request
> fmguard's script-verdict cache key (fmguard.py:3433-3435) includes the scratch folders but not state_dir or state_fallbacks, so a verdict that depends on where state lives could be reused after it moves
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a cached verdict for a script isn't reused after state_dir or a state fallback changes: a test judges a script that writes into state, moves the state folder, and gets the new verdict — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test
2. [x] Add state_dir and state_fallbacks to the cache key (fmguard.py near 3433)
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_guard_state_key test_guard 2>&1 | tail -6` → exit 0 · Ran 195 tests in 19.7s (61 classes, 16 at a time; slowest: GuardAgainstBash 19s, GuardCases 9s, Hook 7s) / OK [ran] [tree 4ff324988319] (2026-10-20T23:29:51Z)
- (step 1) `python3 plugin/tests/run.py test_guard_state_key test_guard` → exit 0 · Ran 195 tests in 24.2s (61 classes, 16 at a time; slowest: GuardAgainstBash 23s, GuardCases 10s, Hook 7s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:50:05Z)
- (step 2) `python3 plugin/tests/run.py test_guard_state_key test_guard` → exit 0 · Ran 195 tests in 23.9s (61 classes, 16 at a time; slowest: GuardAgainstBash 23s, GuardCases 10s, Hook 8s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:50:30Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_state_key test_guard` → exit 0 · Ran 195 tests in 24.9s (61 classes, 16 at a time; slowest: GuardAgainstBash 24s, GuardCases 10s, ScriptCache 7s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:50:56Z)
- `python3 plugin/tests/run.py test_guard_state_key` → ✗ exit 1 · Ran 1 tests in 2.3s (1 classes, 16 at a time; slowest: ScriptVerdictKey 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 983fb246a7c1] (2026-10-20T23:51:01Z)
- `python3 plugin/tests/run.py test_guard_state_key` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: ScriptVerdictKey 0s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:51:01Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 195 tests in 23.7s (61 classes, 16 at a time; slowest: GuardAgainstBash 23s, GuardCases 9s, Hook 8s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:51:34Z)
- (audit intent) `self review of a one-line key change plus a test: the script-verdict cache key gains state_dir and tuple(state_fallbacks); red without, green with; guard tests green` → a cached verdict isn't reused after state moves [tree 983fb246a7c1] (2026-10-20T23:51:34Z)
- (audit adversary) `self review of a one-line key change plus a test: the script-verdict cache key gains state_dir and tuple(state_fallbacks); red without, green with; guard tests green` → only adds to the key, so a verdict can be recomputed more often, never reused wrongly [tree 983fb246a7c1] (2026-10-20T23:51:34Z)
- (audit edge) `self review of a one-line key change plus a test: the script-verdict cache key gains state_dir and tuple(state_fallbacks); red without, green with; guard tests green` → state_dir was already in the cache file's path; fallbacks now in the key [tree 983fb246a7c1] (2026-10-20T23:51:34Z)
- (audit operator) `self review of a one-line key change plus a test: the script-verdict cache key gains state_dir and tuple(state_fallbacks); red without, green with; guard tests green` → a slightly longer key; no behaviour change while state stays put [tree 983fb246a7c1] (2026-10-20T23:51:34Z)
- (audit maintainer) `self review of a one-line key change plus a test: the script-verdict cache key gains state_dir and tuple(state_fallbacks); red without, green with; guard tests green` → the key's parts sit together in one tuple [tree 983fb246a7c1] (2026-10-20T23:51:34Z)
- (audit self) `self review of a one-line key change plus a test: the script-verdict cache key gains state_dir and tuple(state_fallbacks); red without, green with; guard tests green` → no findings [tree 983fb246a7c1] (2026-10-20T23:51:34Z)
## Log
- 2026-10-20T21:10:25Z created
- 2026-10-20T23:28:18Z planned from capture
- 2026-10-20T23:28:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1293.builder.md
- 2026-10-20T23:28:39Z focused
- 2026-10-20T23:49:24Z merged worktree-agent-a1fe34d454f80d582 (2 file(s))
- 2026-10-20T23:49:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1fe34d454f80d582
- 2026-10-20T23:49:36Z focused
- 2026-10-20T23:54:05Z done
- 2026-10-20T23:54:08Z committed 19d20a0b (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0190 [FIX M, done, 3 steps] Guard: guesses never use a variable's own name; rm targets use literals set once before a branch — lesson: A replay gate turns a guard chan…
- research t0018-r4-adversary: fSTe81D17ZxNHRCBuwq4","type":"message","role":"assistant","content":[{"type":"text","text":"## Verdict: changes needed\n\n## Findings\n\n**C…
- playbook Latency Critical Systems (skills/playbooks/references/perf/latency-critical.md)
- decision 2026-10-20: Foreman Code's TUI (T-1283) is a stdlib curses client of fm code's --json event stream with a widget layer that themes and extensions build on; exte…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Lessons
- A cache key must include every input the cached verdict depends on, including where state lives
## Files touched
- plugin/tests/test_guard_state_key.py
- plugin/lib/fmguard.py
- CHANGELOG.md
