---
id: T-2684
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T22:12:01Z
updated: 2026-11-02T22:27:58Z
builder_model: sonnet
base: f5ba1c4140b3df6e63e59c1315f8f27f16d6ba09
base_tree: 7cd38697bb297de7e1ca11d4e2fa777e149f43d3
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T22:13:12Z
plan0_scope: []
lane_stop: merged 2026-11-02T22:23:07Z
verified: strong
---
# fmserve._notify records each delivery's result, exit code included, and fm doctor warns after three failures in a row naming the command
## Raw request
> FIX: fmserve._notify records each delivery's result (exit code included) and fm doctor warns after three failures in a row, naming the notify command
> CONTEXT: Genesis gen-3 Mission 7 (#3 anticipation), gen-3/mission-anticipation.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a notify command that exits 1 is recorded as failed; after three failures in a row fm doctor WARNs naming the command; a success resets the run — verify with `python3 plugin/tests/run.py test_notify_delivery`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the record and the doctor row
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_notify_delivery 2>&1 | grep -v "^$" | tail -14` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: NotifyDeliveryCase 0s) / OK [ran] [tree 55c9690610fc] [world 2f1906870a] (2026-11-02T22:13:49Z)
- (step 1) `python3 plugin/tests/run.py test_notify_delivery 2>&1 | grep -v "^$" | tail -14` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: NotifyDeliveryCase 0s) / OK [ran] [tree 55c9690610fc] [world 2f1906870a] (2026-11-02T22:13:49Z)
- (step 2) `python3 plugin/tests/run.py test_notify_delivery` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: NotifyDeliveryCase 0s) / OK [ran] [tree 55c9690610fc] [world 2f1906870a] (2026-11-02T22:13:54Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_anergy test_crash_hygiene test_doctor test_notify_delivery test_serve test_supply_delta test_unattended && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.54s] [ran] [tree 55c9690610fc] [world 2f1906870a] (2026-11-02T22:14:48Z)
- `python3 plugin/tests/run.py test_notify_delivery` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: NotifyDeliveryCase 0s) / FAILED (1 classes: test_notify_delivery.NotifyDeliveryCase) (start tree + this task's tests) [ran] [tree 3995584de849] [world 2f1906870a] (2026-11-02T22:27:21Z)
- `python3 plugin/tests/run.py test_notify_delivery` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: NotifyDeliveryCase 0s) / OK [ran] [tree 3995584de849] [world 2f1906870a] (2026-11-02T22:27:21Z)
- (ac 1) `python3 plugin/tests/run.py test_notify_delivery` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T22:27:21Z [ran] [tree 3995584de849] [world 2f1906870a] (2026-11-02T22:27:25Z)
- (step 3) `python3 plugin/tests/run.py test_notify_delivery test_doctor` → exit 0 · Ran 111 tests in 3.8s (41 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 2s, Command 2s) / OK [ran] [tree 3995584de849] [world 2f1906870a] (2026-11-02T22:27:25Z)
- (audit edge) `read _notify and check_notify: a nonzero exit, timeout, OSError or PolicyError counts as a failure, success resets fails to 0; the meta write can't break fm run; the command and error go through c.plain and are capped` → a notify command that was changed after 3 failures keeps the old count until its next delivery (one stale warning at most) [tree 3995584de849] (2026-11-02T22:27:25Z)
- (audit adversary) `read _notify and check_notify: a nonzero exit, timeout, OSError or PolicyError counts as a failure, success resets fails to 0; the meta write can't break fm run; the command and error go through c.plain and are capped` → no new exec path: the same guard_stored check runs before the command; the stored error is plain text capped at 120 characters [tree 3995584de849] (2026-11-02T22:27:25Z)
- (audit self) `read _notify and check_notify: a nonzero exit, timeout, OSError or PolicyError counts as a failure, success resets fails to 0; the meta write can't break fm run; the command and error go through c.plain and are capped` → no findings [tree 3995584de849] (2026-11-02T22:27:25Z)
## Log
- 2026-11-02T22:12:01Z created
- 2026-11-02T22:12:38Z planned from capture
- 2026-11-02T22:12:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2684.builder.md
- 2026-11-02T22:13:11Z focused
- 2026-11-02T22:13:12Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T22:23:07Z merged worktree-agent-ae21a7488ed2c4225 (3 file(s))
- 2026-11-02T22:27:13Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae21a7488ed2c4225
- 2026-11-02T22:27:13Z focused
- 2026-11-02T22:27:14Z scope: its CHANGELOG line landed in T-2683's commit 9ff9c524 (same edit)
- 2026-11-02T22:27:58Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2666 [RESEARCH M, done, 3 steps] Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-11-02: Recommendation: Mission 7 builds four anticipation gaps where Foreman computes what the user will need but it never reaches them (the booked next-re…
## Why not caught
_notify was written fire-and-forget (T-0901) and nothing read its result
## Files touched
- plugin/tests/test_notify_delivery.py
- plugin/lib/fmserve.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
