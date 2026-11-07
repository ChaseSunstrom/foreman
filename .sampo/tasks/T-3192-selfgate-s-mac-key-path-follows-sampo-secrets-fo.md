---
id: T-3192
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T10:29:10Z
updated: 2026-11-05T15:23:38Z
builder_model: haiku
base: df49cbd9424216fa55f3992a6b6e2836b9f1dd77
base_tree: 7243e93ecd68cb0508c0e54c71c8fb76e2afc17e
plan0_at: 2026-11-05T10:30:23Z
plan0_scope: []
builder_returned: 2026-11-05T10:31:34Z
lane_stop: refused 2026-11-05T15:16:00Z
postmerge_red: test_board_verbs.BoardVerbs
postmerge_sha: 2b2ac9029773e1ad4cfca65559524634c82cd6f5
verified: strong
---
# Selfgate's MAC key path follows SAMPO_SECRETS/FOREMAN_SECRETS (via models.secrets_path),…
## Raw request
> selfgate's MAC key path follows SAMPO_SECRETS/FOREMAN_SECRETS (via models.secrets_path), so a merge run with that env pointed at a key the agent wrote can forge the base-bench cache; fix the key to the account's own ~/.config/sampo (pwd home), ignoring the env
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] selfgate's MAC key lives at the account's own ~/.config/sampo/selfgate.key (pwd home) whatever SAMPO_SECRETS/FOREMAN_SECRETS say; a run with the env pointed elsewhere neither reads nor writes a key there; tests never touch the real key (they patch the key path) — verify with `python3 plugin/tests/run.py test_selfgate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: an env-redirected SECRETS path does not move the key
2. [x] key path from the password database home
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_selfgate` → ✗ exit 1 · Ran 36 tests in 1.5s (8 classes, 16 at a time; slowest: GateEndToEnd 0s, KeyPath 0s, BaseCache 0s) / FAILED (1 classes: test_selfgate.KeyPath) [ran] [tree 753c3b44b09d] [world 2f1906870a] (2026-11-05T10:30:43Z)
- (step 2) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 36 tests in 0.5s (8 classes, 16 at a time; slowest: GateEndToEnd 0s, BaseCache 0s, AaFixtures 0s) / OK [ran] [tree 2dfc316773f0] [world 2f1906870a] (2026-11-05T10:30:49Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_rename_scan test_selfgate && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [14.27s] [ran] [tree 544519e1decd] [world 2f1906870a] (2026-11-05T10:31:22Z)
- (step 1) `python3 plugin/tests/run.py test_selfgate test_lanes.SelfChangeGate test_helpers_env` → exit 0 · Ran 53 tests in 2.9s (25 jobs, 16 at a time; slowest: SelfChangeGate.test_only_the_users_yes_after_the_refusal_passes_never_a_decision_or_the_standing_yes 3s, SelfChangeGate.test_the_yes_is_bound_to_t [ran] [tree 98fe00fa1278] [world 2f1906870a] (2026-11-05T15:18:14Z)
- `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 34 tests in 1.6s (7 jobs, 16 at a time; slowest: GateEndToEnd 0s, BaseCache 0s, MedianCpu 0s) / OK (start tree + this task's tests) [ran] [tree 98fe00fa1278] [world 2f1906870a] (2026-11-05T15:18:17Z)
- `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 34 tests in 0.5s (7 jobs, 16 at a time; slowest: GateEndToEnd 0s, BaseCache 0s, WhichDiffsAreTimed 0s) / OK [ran] [tree 98fe00fa1278] [world 2f1906870a] (2026-11-05T15:18:17Z)
- `bash -c 'cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wt-3192 && python3 plugin/tests/run.py test_selfgate'` → exit 0 · Ran 34 tests in 1.6s (7 jobs, 16 at a time; slowest: GateEndToEnd 0s, BaseCache 0s, AaFixtures 0s) / OK [ran] [tree 98fe00fa1278] [world 2f1906870a] (2026-11-05T15:18:26Z)
- `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 34 tests in 0.4s (7 jobs, 16 at a time; slowest: GateEndToEnd 0s, Interleaved 0s, BaseCache 0s) / OK [ran] [tree 98fe00fa1278] [world 2f1906870a] (2026-11-05T15:18:27Z)
- (step 1) `python3 plugin/tests/run.py test_selfgate test_lanes.SelfChangeGate test_helpers_env test_board_verbs` → exit 0 · Ran 63 tests in 5.5s (34 jobs, 16 at a time; slowest: BoardVerbs.test_release_check_runs_doctor_and_demo_in_a_temporary_home 5s, BoardVerbs.test_round_close_lists_the_newest_20_and_counts_the_rest 5s, [ran] [tree 3ef130a2d3e2] [world 2f1906870a] (2026-11-05T15:23:03Z)
- `bash -c 'cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/wt-3192 && python3 plugin/tests/run.py test_selfgate'` → ✗ exit 1 · Ran 36 tests in 2.5s (8 jobs, 16 at a time; slowest: GateEndToEnd 0s, KeyPath 0s, BaseCache 0s) / FAILED (1 classes: test_selfgate.KeyPath) [ran] [tree 3ef130a2d3e2] [world 2f1906870a] (2026-11-05T15:23:15Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 36 tests in 0.7s (8 jobs, 16 at a time; slowest: GateEndToEnd 0s, BaseCache 0s, KeyPath 0s) / OK [ran] [tree 87620d8883a9] [world 2f1906870a] (2026-11-05T15:23:30Z)
- (audit adversary) `re-landed after a false revert (BoardVerbs flake, fixed by T-3216): applied by sampo edit from its own diff, selfgate.py and test_selfgate.py equal its merged tree; red on its merge base with its test (test_selfgate.KeyPath), green on main with test_lanes.SelfChangeGate, test_helpers_env and test_board_verbs (63 OK)` → the key path is pinned to the account's own ~/.config/sampo (Ward-guarded as credentials since T-3188); SAMPO_SECRETS/FOREMAN_SECRETS redirecting secrets can't move the MAC key, so a run with a planted secrets dir can neither read the real key nor sign a forged base cache with its own [tree 87620d8883a9] (2026-11-05T15:23:30Z)
- (audit edge) `re-landed after a false revert (BoardVerbs flake, fixed by T-3216): applied by sampo edit from its own diff, selfgate.py and test_selfgate.py equal its merged tree; red on its merge base with its test (test_selfgate.KeyPath), green on main with test_lanes.SelfChangeGate, test_helpers_env and test_board_verbs (63 OK)` → tests still sign with their own temp key (T-3195's patch of _keyfile), checked by test_helpers_env [tree 87620d8883a9] (2026-11-05T15:23:30Z)
- (audit self) `re-landed after a false revert (BoardVerbs flake, fixed by T-3216): applied by sampo edit from its own diff, selfgate.py and test_selfgate.py equal its merged tree; red on its merge base with its test (test_selfgate.KeyPath), green on main with test_lanes.SelfChangeGate, test_helpers_env and test_board_verbs (63 OK)` → no findings [tree 87620d8883a9] (2026-11-05T15:23:30Z)
## Log
- 2026-11-05T10:29:10Z created
- 2026-11-05T10:30:10Z planned: it has criteria and steps
- 2026-11-05T10:30:11Z set status=planned
- 2026-11-05T10:30:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3192.builder.md
- 2026-11-05T10:30:22Z focused
- 2026-11-05T15:01:19Z merged worktree-agent-ac2da58a0f8cadfad (2 file(s))
- 2026-11-05T15:01:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac2da58a0f8cadfad
- 2026-11-05T15:16:00Z red after merge: test_board_verbs.BoardVerbs; 2b2ac9029 reverted
- 2026-11-05T15:18:10Z focused
- 2026-11-05T15:20:18Z paused: focus moved to T-3216
- 2026-11-05T15:22:54Z its merge was reverted at 15:16 (20bdebe5) by the post-merge verify for test_board_verbs.BoardVerbs, a flake (green alone); re-landing
- 2026-11-05T15:22:55Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-05T15:22:55Z focused
- 2026-11-05T15:23:32Z affected tests waived: names that can't match are T-3160's modules (merged and reverted in this window, not on disk); T-3192's own tests pass (63 OK)
- 2026-11-05T15:23:34Z done
- 2026-11-05T15:23:38Z committed cdac8696 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3176 [PERFORMANCE S, done, 2 steps] A gated merge benches the base tree once per base commit: the self-change gate caches the base side's bench and guard replay by the…
- T-3080 [FIX S, done, 2 steps] Exam runs find the model key: the secrets file's default path comes from the user's real home, not $HOME, which an exam points at a throwaw…
- T-3188 [SECURITY S, active, 2 steps] Ward treats every file under ~/.config/sampo as a credential (secrets.env, selfgate.key and any later key), not only by file name, w…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar finished tasks took 2–2 steps
## Plan gaps
- failed first: step 1 failing test: an env-redirected SECRETS path does not move the key
## Files touched
- plugin/tests/test_selfgate.py
- plugin/lib/sampo/selfgate.py
- CHANGELOG.md
