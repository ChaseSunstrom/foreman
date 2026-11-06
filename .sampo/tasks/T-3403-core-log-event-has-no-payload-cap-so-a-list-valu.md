---
id: T-3403
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/core.py, plugin/lib/sampo/ledger.py, plugin/tests/test_ledger_chain.py]
depends_on: []
source: discovered
created: 2026-11-06T08:00:21Z
updated: 2026-11-06T13:49:57Z
base: df4188f51f57a4fb522778dbaa2d230a93f2589c
base_tree: 62f4fcf71b5e89ac4b937f8c18232e7594fd25fc
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:45:32Z
plan0_scope: []
builder_returned: 2026-11-06T09:09:43Z
lane_stop: merged 2026-11-06T10:39:08Z
verified: strong
---
# core.log_event has no payload cap, so a list-valued event (check_run failed classes,…
## Raw request
> FIX: core.log_event has no payload cap, so a list-valued event (check_run failed classes, touched files) can bloat the hash-chained ledger.jsonl; cap list fields with a count (T-3397 review)
## Interpretation
Reading 1: cap top-level list and string fields of data in log_event. Reading 2: cap the whole serialized line; ruled out, it would drop fields readers need.
## Assumptions (confidence)
## Acceptance criteria
- [x] log_event caps list fields at 200 with <field>_n, long strings, chain stays valid — verify with `python3 plugin/tests/run.py test_ledger_chain`
## Non-goals
## Approach (options → choice → why)
1) cap in log_event top-level only; likely outcome: bounded ledger, fails if a nested list is huge. 2) use what exists: redact_obj walks data already, but callers differ; likely outcome: per-caller drift. 3) do less: cap only check_run in its caller; fails if another event bloats. Choice 1 (80%): one place every writer routes through, and the capped rec is what is hashed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] cap in log_event + test
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → ✗ exit 1 · Ran 37 tests in 3.3s (3 jobs, 16 at a time; slowest: Chain 2s, Receipt 2s, Cap 0s) / FAILED (1 classes: test_ledger_chain.Cap) [ran] [tree 7f77900720dd] [world 2f1906870a] (2026-11-06T08:45:54Z)
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 69 tests in 19.3s (3 jobs, 16 at a time; slowest: Chain 2s, Cap 2s, Receipt 1s) / OK [ran] [tree 4e51a77cc0ba] [world 2f1906870a] (2026-11-06T08:46:37Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_core test_doctor test_ledger_chain test_left_out test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [13.10s] [ran] [tree 4e51a77cc0ba] [world 2f1906870a] (2026-11-06T08:47:51Z)
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 70 tests in 66.6s (3 jobs, 16 at a time; slowest: Chain 4s, Receipt 3s, Cap 2s) / OK [ran] [tree 991f7ff023b6] [world 2f1906870a] (2026-11-06T08:58:43Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 991f7ff023b6] [world 2f1906870a] (2026-11-06T08:58:46Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree e864306cb1b8] (2026-11-06T10:39:10Z)
- (ac 1) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 70 tests in 2.0s (3 jobs, 16 at a time; slowest: Cap 2s, Chain 2s, Receipt 1s) / OK [ran] [tree e864306cb1b8] [world 2f1906870a] (2026-11-06T10:39:14Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree e864306cb1b8] (2026-11-06T10:39:14Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree e864306cb1b8] (2026-11-06T10:39:14Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree e864306cb1b8] (2026-11-06T10:39:14Z)
## Log
- 2026-11-06T08:00:21Z created
- 2026-11-06T08:45:10Z planned: it has criteria and steps
- 2026-11-06T08:45:31Z focused
- 2026-11-06T08:45:32Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T10:39:08Z merged worktree-agent-af58420caf3675d85 (3 file(s))
- 2026-11-06T10:39:08Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af58420caf3675d85
- 2026-11-06T10:39:09Z focused
- 2026-11-06T10:39:10Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/ledger.py', 'plugin/tests/test_ledger_chain.py']
- 2026-11-06T10:39:10Z scope: widened at merge to the reviewed lane's own diff (482b9b99f), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T10:39:38Z done
- 2026-11-06T10:39:40Z committed 3efd1dced (1 file)
- 2026-11-06T13:49:57Z not reverted: test_check_paths.CheckSkip, test_close_gates.CloseGates already fail on 482b9b99f's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-2763 [CLEAN S, done, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate slo…
- research wave1-plan-a306a171bb6861f90: === T-1044 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-30: Cold reads converge by per-line acceptance (keyed on line text + charter hash), not by majority reads or diff-only reads: every line still gets a wh…
- similar finished tasks took 2–4 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 cap in log_event + test
## Files touched
- plugin/tests/test_ledger_chain.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/ledger.py
- CHANGELOG.md
