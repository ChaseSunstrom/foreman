---
id: T-3423
type: FIX
tier: S
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T10:23:39Z
updated: 2026-11-06T10:43:12Z
lane: ~/.claude/foreman/.claude/worktrees/agent-af80c8128c6ebd118
lane_branch: worktree-agent-af80c8128c6ebd118
base: 177fdfc5a8e5cb46c67896101e880f3b96caa9c3
base_tree: d5305a9a01fce005ed7d8914ad0390e51f6ddf69
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T10:24:36Z
plan0_scope: []
builder_returned: 2026-11-06T10:43:12Z
---
# hooks.log_error appends to state/logs/hooks.log with no size cap or rotation (repeated…
## Raw request
> FIX: hooks.log_error appends to state/logs/hooks.log with no size cap or rotation (repeated per-read notices such as T-3419's grow it); rotate at a size cap (keep one .1) and collapse an identical event+text written within a minute into a count
## Interpretation
Rotate hooks.log at 1 MB; skip identical event+text within 60 s
## Assumptions (confidence)
## Acceptance criteria
- [ ] log_error rotates past the cap and collapses identical lines within 60 s — verify with `python3 plugin/tests/run.py test_hooks.LogError`
## Non-goals
## Approach (options → choice → why)
One stat per call; sidecar hooks.log.last; doctor reads .1
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then implement log_error rotation and dedup
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.LogErrorCap` → exit 0 · Ran 1 tests in 11.9s (1 jobs, 16 at a time; slowest: LogErrorCap 0s) / OK [ran] [tree efe2d7fb9757] [world 2f1906870a] (2026-11-06T10:27:15Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.LogErrorCap` → exit 0 · Ran 1 tests in 145.9s (1 jobs, 16 at a time; slowest: LogErrorCap 0s) / OK [ran] [tree efe2d7fb9757] [world 2f1906870a] (2026-11-06T10:27:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_compact test_core test_doctor test_hooks test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [21.06s] [ran] [tree efe2d7fb9757] [world 2f1906870a] (2026-11-06T10:30:32Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.LogErrorCap` → exit 0 · Ran 2 tests in 0.5s (1 jobs, 16 at a time; slowest: LogErrorCap 0s) / OK [ran] [tree 52c9de19e593] [world 2f1906870a] (2026-11-06T10:43:06Z)
## Log
- 2026-11-06T10:23:39Z created
- 2026-11-06T10:24:01Z set tier=S
- 2026-11-06T10:24:34Z planned: it has criteria and steps
- 2026-11-06T10:24:35Z focused
- 2026-11-06T10:24:36Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1606-review: Verdict: changes needed.** The core works, but the note's "logs keep it redacted" claim is false on one path, and the report-and-file flow puts t…
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- research T-3014-review: Verdict:** approve with nits. The code is sound. The tests for the two acceptance criteria that matter most don't cover the real call path. [stal…
- decision 2026-11-02: [check: python3 plugin/tests/run.py test_loop] A command a drive line names may be called again: a repeat within minutes must not advance state.
