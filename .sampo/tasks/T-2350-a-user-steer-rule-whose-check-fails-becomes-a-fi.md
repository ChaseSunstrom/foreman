---
id: T-2350
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmnight.py]
depends_on: []
source: user
created: 2026-10-31T14:00:56Z
updated: 2026-10-31T14:36:18Z
builder_model: sonnet
base: 8a1b3bac0dcbfda014e9a7f02c91185c578796a5
base_tree: 1eca3780f0dacaf8038d75d386a59efe1b069460
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T14:14:30Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmnight.py]
verified: strong
---
# A user-steer rule whose check fails becomes a fix, and the checks run nightly (Mission 8, #7)
## Raw request
> A user-steer rule whose check fails becomes a fix, and the checks run nightly (Mission 8, #7)
## Interpretation
Gap map #7 'my corrections become fixes'. T-2167 gives every user steer a check (fm decide --check); steer_checks reports a failing one as a line in fm genesis sweep and fm doctor, and nothing files a fix: the user's rule broke and the only trace is a line someone has to read.
## Assumptions (confidence)
## Acceptance criteria
- [x] When steer_checks finds a user-steer rule whose check fails, one FIX 'The user's rule no longer holds: <rule>' is captured per rule and commit, naming the check and its output tail; the same failure at the same commit files nothing more; a passing check files nothing; a missing check stays a doctor line — verify with `python3 plugin/tests/run.py test_genesis test_doctor`
- [x] fm night runs the steer checks among its free jobs and its report names any rule that failed — verify with `python3 plugin/tests/run.py test_night`
## Non-goals
## Approach (options → choice → why)
1) where steer_checks runs with run=True, a failing check captures one FIX per rule and failing commit (key: rule hash + HEAD), naming the check and its output tail, trigger steer-check; fm night runs the checks (zero tokens). 2) a FIX at every failing run - rejected: floods on a red tree. 3) block fm ship on a failing steer check - later: the sweep already gates the generation. Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: failing check captures once per rule and commit; passing and missing don't; night job
2. [x] capture in the steer_checks path; the night job
3. [x] docs: MASTER, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis test_night` → ✗ exit 1 · Ran 187 tests in 24.3s (27 classes, 16 at a time; slowest: GenesisRead 23s, Night 20s, GenesisCheck 19s) / FAILED (2 classes: test_genesis.GenesisSweep, test_night.Night) [ran] [tree 0ba069fa2a66] (2026-10-31T14:16:20Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_night test_doctor test_judgment` → exit 0 · Ran 291 tests in 57.0s (64 classes, 16 at a time; slowest: GenesisRead 56s, Night 43s, GenesisCheck 39s) / OK [ran] [tree a70a151c40a7] (2026-10-31T14:17:46Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_night` → exit 0 · Ran 187 tests in 41.9s (27 classes, 16 at a time; slowest: GenesisRead 41s, Night 36s, GenesisCheck 33s) / OK [ran] [tree 38f761ae17d3] (2026-10-31T14:18:47Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_docs test_genesis test_guard_cases test_night test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [71.07s] [ran] [tree 38f761ae17d3] (2026-10-31T14:21:32Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_docs test_genesis test_guard_cases test_night test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [33.55s] [ran] [tree 38f761ae17d3] (2026-10-31T14:22:42Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_night test_doctor test_judgment` → exit 0 · Ran 291 tests in 11.9s (64 classes, 16 at a time; slowest: GenesisRead 12s, Night 10s, GenesisCheck 9s) / OK [ran] [tree 0b18b1ef3c9b] (2026-10-31T14:33:00Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_doctor` → exit 0 · Ran 256 tests in 21.6s (47 classes, 16 at a time; slowest: GenesisRead 21s, GenesisCheck 16s, GenesisLive 16s) / OK [ran] [tree fd0fb757b069] (2026-10-31T14:33:50Z)
- (ac 2) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 22 tests in 13.1s (10 classes, 16 at a time; slowest: Night 13s, NightGuards 3s, Stranger 1s) / OK [ran] [tree fd0fb757b069] (2026-10-31T14:33:50Z)
- (audit adversary) `self-review of the merged lane: a failing steer check files one FIX per rule and commit, keyed [steer-check RULEHASH@HEAD12], deduped even after the first FIX closes; rule text and output redacted and defanged; fm night's free 'steer checks' job names each failed rule; doctor's cheap pass captures nothing; 291 tests OK` → rule text and check output are redacted and defanged before entering a brief; checks run through the allowlisted steer-check path (shell=False) [tree fd0fb757b069] (2026-10-31T14:33:50Z)
- (audit edge) `self-review of the merged lane: a failing steer check files one FIX per rule and commit, keyed [steer-check RULEHASH@HEAD12], deduped even after the first FIX closes; rule text and output redacted and defanged; fm night's free 'steer checks' job names each failed rule; doctor's cheap pass captures nothing; 291 tests OK` → a refused or timed-out check counts as failing (a broken rule too); dedupe per commit, so a dirty tree doesn't refile [tree fd0fb757b069] (2026-10-31T14:33:50Z)
- (audit self) `self-review of the merged lane: a failing steer check files one FIX per rule and commit, keyed [steer-check RULEHASH@HEAD12], deduped even after the first FIX closes; rule text and output redacted and defanged; fm night's free 'steer checks' job names each failed rule; doctor's cheap pass captures nothing; 291 tests OK` → no findings [tree fd0fb757b069] (2026-10-31T14:33:50Z)
## Log
- 2026-10-31T14:00:56Z created
- 2026-10-31T14:14:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2350.builder.md
- 2026-10-31T14:14:29Z focused
- 2026-10-31T14:14:30Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T14:32:28Z merged worktree-agent-a0cd586227df62324 (7 file(s))
- 2026-10-31T14:32:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0cd586227df62324
- 2026-10-31T14:32:29Z focused
- 2026-10-31T14:33:14Z scope: plugin/lib/fmgenesis.py, plugin/lib/fmcore.py, plugin/lib/fmnight.py, plugin/lib/fmcli.py, plugin/tests/test_genesis.py, plugin/tests/test_night.py, MASTER.md, CHANGELOG.md
- 2026-10-31T14:35:08Z done
- 2026-10-31T14:35:12Z committed d9573a17 (1 file)
- 2026-10-31T14:36:18Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- research T-2167-review: Verdict:** changes needed. There are no blockers. The doctor behaviour doesn't match what the user asked for, and one enforcement hole could leav…
- decision 2026-10-30: [revisited: every user steer becomes a standing rule] [cites: the user's steer 2026-10-30 (second): standing rule] [check: python3 plugin/tests/run.…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_night.py
## Lessons
- A rule with a check that nobody runs is a hope: run it nightly and file the break
## Plan gaps
- failed first: step 1 red tests: failing check captures once per rule and commit; passing and missing don't; night job
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/test_night.py
- plugin/lib/fmcore.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmnight.py
- MASTER.md
- CHANGELOG.md
