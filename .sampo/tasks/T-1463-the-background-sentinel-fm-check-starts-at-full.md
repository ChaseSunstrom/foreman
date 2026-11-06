---
id: T-1463
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_close_gates.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T14:50:47Z
updated: 2026-10-22T15:07:09Z
base: 7a8f726330832049abcaf923cc953645fbe0742c
base_tree: 91fb64c0f34eee80e5be3f2d8f2316af31652026
plan0_at: 2026-10-22T15:00:29Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_close_gates.py, CHANGELOG.md]
verified: strong
---
# Background gate run starts at low CPU priority
## Raw request
> The background sentinel fm check starts at full priority (fmcli.py:1135) and competes for CPU with the next task's foreground finish and tests; start it under nice (os.nice in the child / preexec)
## Interpretation
_sentinel Popens the background fm check at full priority (fmcli.py:1135), so it competes with the next task's foreground finish and tests.
## Assumptions (confidence)
## Acceptance criteria
- [x] the background sentinel's argv starts with nice -n 10 — verify with `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_the_background_sentinel_runs_at_low_priority`
## Non-goals
## Approach (options → choice → why)
Prefix nice -n 10 when nice is on PATH (it execs sh, so the pid file still names the run). Options: os.nice in preexec_fn (not fork-safe with threads) → rejected.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] nice prefix
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_the_background_sentinel_runs_at_low_priority` → exit 0 · Ran 1 test in 0.931s / OK [ran] [tree b59978a6d288] (2026-10-22T15:03:25Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_the_background_sentinel_runs_at_low_priority` → exit 0 · Ran 1 test in 1.378s / OK [ran] [tree b59978a6d288] (2026-10-22T15:03:29Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_the_background_sentinel_runs_at_low_priority` → exit 0 · Ran 1 test in 0.736s / OK [ran] [tree 7d5307814710] (2026-10-22T15:04:56Z)
- (audit edge) `builder (sonnet) test-first, red seen; merged; skipUnless(nice) added after its own note; test_close_gates 14/14 green.` → no nice on PATH → starts as before; nice execs sh so the one-at-a-time pid check still works [tree 7d5307814710] (2026-10-22T15:04:56Z)
- (audit adversary) `builder (sonnet) test-first, red seen; merged; skipUnless(nice) added after its own note; test_close_gates 14/14 green.` → no new input; argv is fixed [tree 7d5307814710] (2026-10-22T15:04:56Z)
- (audit self) `builder (sonnet) test-first, red seen; merged; skipUnless(nice) added after its own note; test_close_gates 14/14 green.` → no findings [tree 7d5307814710] (2026-10-22T15:04:56Z)
## Log
- 2026-10-22T14:50:47Z created
- 2026-10-22T14:59:56Z planned from capture
- 2026-10-22T15:00:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1463.builder.md
- 2026-10-22T15:00:28Z focused
- 2026-10-22T15:03:12Z merged worktree-agent-adadcaf4b1d54408d (2 file(s))
- 2026-10-22T15:03:12Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adadcaf4b1d54408d
- 2026-10-22T15:03:13Z focused
- 2026-10-22T15:07:06Z done
- 2026-10-22T15:07:09Z committed ea84fd14 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0775 [FIX S, done, 2 steps] One-off headless claude -p sessions answer their prompt and stop; they never drive the queue — lesson: a headless session Foreman didn't st…
- research T-1044-review: Verdict: changes needed.** There is one MEDIUM regression, and the pid-reuse guard itself is sound. [stale: plugin/lib/fmideas.py changed since i…
- decision 2026-10-04: T-0224 (L) self-approved under full autonomy: tool-less mutation child, candidate on an evolve branch outside the live plugin, merge stays the user'…
- likely tests for the scope: plugin/tests/test_cli.py
## Measurements
background sentinel's CPU niceness: 0 → 10 (argv now starts nice -n 10; nice execs sh so the pid file still names the run); its competition with the next foreground finish isn't timed here — T-1462 adds per-run timing
## Files touched
- plugin/tests/test_close_gates.py
- plugin/lib/fmcli.py
- CHANGELOG.md
