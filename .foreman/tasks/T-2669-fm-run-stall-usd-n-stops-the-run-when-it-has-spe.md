---
id: T-2669
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T20:44:49Z
updated: 2026-11-02T20:55:05Z
builder_model: sonnet
base: 2317c37ec9824693c658d4e731c86be27009ad6e
base_tree: 5a4f7e1aad5b82ac34b19851a45483282dd2a06f
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:46:14Z
plan0_scope: []
lane_stop: merged 2026-11-02T20:53:09Z
verified: strong
unproven: [docs]
---
# fm run --stall-usd N stops the run when it has spent N dollars since its last task close and names why
## Raw request
> FEATURE: fm run --stall-usd N stops the run when it has spent N dollars since its last task close and names why in the receipt; a run that keeps closing tasks is never stopped by it
> CONTEXT: Genesis gen-3 Mission 5 (#12 staying lean and safe), gen-3/mission-staying-lean-and-safe.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a stubbed fm run whose sessions spend past N dollars with no close stops before the next task and its last line names --stall-usd; one that closes a task resets the count and keeps going — verify with `python3 plugin/tests/run.py test_serve`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test beside fm run's --max-usd tests in test_serve
2. [x] --stall-usd in fmserve.cmd_run beside run_usd, and its fmcli flag
3. [x] CHANGELOG and MASTER (fmserve line)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_serve` → exit 0 · Ran 41 tests in 17.5s (8 classes, 16 at a time; slowest: Run 17s, RunRoute 8s, Serve 2s) / OK [ran] [tree bddbb15ba8c8] [world 2f1906870a] (2026-11-02T20:50:21Z)
- (step 2) `python3 plugin/tests/run.py test_serve` → exit 0 · Ran 41 tests in 18.0s (8 classes, 16 at a time; slowest: Run 18s, RunRoute 8s, Serve 3s) / OK [ran] [tree bddbb15ba8c8] [world 2f1906870a] (2026-11-02T20:50:39Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_guard_cases test_paused test_robustness test_serve test_unattended test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [16.04s] [ran] [tree bddbb15ba8c8] [world 2f1906870a] (2026-11-02T20:51:23Z)
- (step 3) `grep -q 'stall-usd' CHANGELOG.md && grep -q 'stall-usd' MASTER.md` → exit 0 · (no output) [ran] [tree f18fc5c56c4c] [world 2f1906870a] (2026-11-02T20:53:20Z)
- (ac 1) `python3 plugin/tests/run.py test_serve` → exit 0 · Ran 41 tests in 27.0s (8 classes, 16 at a time; slowest: Run 27s, RunRoute 13s, Serve 4s) / OK [ran] [tree f18fc5c56c4c] [world 2f1906870a] (2026-11-02T20:53:48Z)
- (ac 1) `python3 plugin/tests/run.py test_serve` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T20:53:48Z [ran] [tree f18fc5c56c4c] [world 2f1906870a] (2026-11-02T20:53:54Z)
- (audit edge) `self: reviewed the builder diff; the since-close counter resets only on a close, is checked before the next task is picked, refuses a negative or NaN value, and forces one task at a time so every session's cost is read; spend is also recorded to fm budget as under --max-usd` → a stall inside one session that still closes isn't caught (between-tasks check, a stated ceiling); an unparsable cost counts as zero [tree f18fc5c56c4c] (2026-11-02T20:53:54Z)
- (audit self) `self: reviewed the builder diff; the since-close counter resets only on a close, is checked before the next task is picked, refuses a negative or NaN value, and forces one task at a time so every session's cost is read; spend is also recorded to fm budget as under --max-usd` → no findings [tree f18fc5c56c4c] (2026-11-02T20:53:54Z)
## Log
- 2026-11-02T20:44:49Z created
- 2026-11-02T20:45:33Z planned from capture
- 2026-11-02T20:45:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2669.builder.md
- 2026-11-02T20:46:13Z focused
- 2026-11-02T20:46:14Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:53:09Z merged worktree-agent-a72a746ec14e13fc2 (3 file(s))
- 2026-11-02T20:53:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a72a746ec14e13fc2
- 2026-11-02T20:53:10Z focused
- 2026-11-02T20:54:59Z done
- 2026-11-02T20:55:05Z committed 53274ebf (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-11-02: Recommendation: Mission 5 builds three measured gaps (burden counts hook_success SessionStart context and splits it by source; a guard latency test …
## Files touched
- plugin/tests/test_serve.py
- plugin/lib/fmcli.py
- plugin/lib/fmserve.py
- CHANGELOG.md
- MASTER.md
