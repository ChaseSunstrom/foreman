---
id: T-2639
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T21:15:46Z
base: 34a2320825e3a9e148bed545dba08e37fd3ffee4
base_tree: c1c40937f4d7bb39e5ab0dcd93fcccfb8472ec7c
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T21:13:50Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# fm doctor warns when Foreman's state directory sits on a volatile filesystem (tmpfs, ramfs), naming the mount and how to move it back
## Raw request
> FEATURE: fm doctor: audit durable state on volatile paths and cross-check ledger conservation (c06: State durability, integrity and recovery; value 4, effort M, risk med)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm doctor WARNs naming the mount when c.state_dir() is on tmpfs or ramfs (read from /proc/mounts, longest prefix), and PASSes on a disk filesystem — verify with `python3 plugin/tests/run.py test_state_volatile`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test with a stubbed mounts table
2. [x] the check in fmdoctor
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_state_volatile` → red as expected (exit 1) · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: StateVolatile 0s) / FAILED (1 classes: test_state_volatile.StateVolatile) [ran] [tree 045364f5dca2] [world 2f1906870a] (2026-11-02T21:14:13Z)
- (step 2) `python3 plugin/tests/run.py test_state_volatile test_doctor` → exit 0 · Ran 112 tests in 4.2s (40 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree aa190ec5e247] [world 2f1906870a] (2026-11-02T21:15:15Z)
- (step 3) `python3 plugin/tests/run.py test_state_volatile test_doctor` → exit 0 · Ran 112 tests in 4.2s (40 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 3s, Command 2s) / OK [ran] [tree aa190ec5e247] [world 2f1906870a] (2026-11-02T21:15:20Z)
- (ac 1) `python3 plugin/tests/run.py test_state_volatile` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: StateVolatile 0s) / OK [ran] [tree aa190ec5e247] [world 2f1906870a] (2026-11-02T21:15:21Z)
- (audit edge) `self: one more read of /proc/mounts per doctor run through the existing _fs_type (longest mount prefix); the WARN names the filesystem and the fix; the old temp-dir message stays for a fallback under /tmp that isn't RAM-backed` → no /proc/mounts (macOS) gives 'unknown', which never warns; the default on disk still passes (tested) [tree aa190ec5e247] (2026-11-02T21:15:21Z)
- (audit self) `self: one more read of /proc/mounts per doctor run through the existing _fs_type (longest mount prefix); the WARN names the filesystem and the fix; the old temp-dir message stays for a fallback under /tmp that isn't RAM-backed` → no findings [tree aa190ec5e247] (2026-11-02T21:15:21Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T21:13:49Z planned from capture
- 2026-11-02T21:13:49Z focused
- 2026-11-02T21:13:50Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T21:13:51Z steer: scoped to the volatile-path audit; ledger conservation is left out: fm verify-ledger's chain catches removed lines and fm drill's dropped-class fault (T-2648) checks the readers
- 2026-11-02T21:15:20Z scope: plugin/tests/test_doctor.py (its state-location test pins ext4: the test's /tmp is tmpfs here), CHANGELOG.md
- 2026-11-02T21:15:43Z done
- 2026-11-02T21:15:46Z committed 4e3fbf86 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2650 [FEATURE M, dropped, 0 steps] fm doctor cross-checks one self-written gauge against transcript usage and flags…
- T-2649 [FEATURE M, dropped, 0 steps] fm doctor row: list deciders with no sample size or an abstain rate near 100% (c16:…
- T-2646 [FEATURE M, dropped, 0 steps] fm guard --dry-run: replay the user's recent bash history through the guard and list…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
## Files touched
- plugin/tests/test_state_volatile.py
- plugin/lib/fmdoctor.py
- plugin/tests/test_doctor.py
- CHANGELOG.md
