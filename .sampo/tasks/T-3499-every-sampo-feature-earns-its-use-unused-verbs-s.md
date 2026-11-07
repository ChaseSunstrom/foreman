---
id: T-3499
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T19:05:56Z
updated: 2026-11-06T19:26:30Z
lane: ~/.claude/foreman.lanes/T-3499
lane_branch: foreman/T-3499
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: cc5fffae3f8171d193ad5413161d55c2c5e43df5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T19:13:51Z
plan0_scope: []
predict_noted: 2026-11-06T19:26:36Z
---
# Every Sampo feature earns its use: unused verbs, skills and playbooks whose situation holds now are named, and the read-only ones run themselves
## Raw request
> Every Sampo feature earns its use: unused verbs, skills and playbooks whose situation holds now are named, and the read-only ones run themselves
## Interpretation
Reading 1 (chosen): name the unused features whose situation holds now, with numbers, in sampo next (a self-check), and let the night run the read-only ones; sampo usage counts unused features with no probe. Reading 2 (ruled out): auto-run every unused verb or trim unused features from the plugin; running write verbs unasked is unsafe and trimming loses features the user wants used, not removed.
## Assumptions (confidence)
## Acceptance criteria
- [ ] sampo next names an unused verb, skill or playbook whose situation holds now with its numbers (tidy: stale worktrees and days since the last tidy; release: unreleased changelog lines and days since the version moved; debug-test: failed closes today with the skill never loaded; doctor: days since it ran), the drive runs the read-only ones itself, and sampo usage counts the features with no situation yet — verify with `python3 plugin/tests/run.py test_fits`
## Non-goals
## Approach (options → choice → why)
1) A new sampo fits verb the night calls. Likely outcome: works, but adds a verb to an already 171-verb CLI that itself goes unused. 2) Probes inline in selfcheck.py. Fails if: the night and usage need them too, then they're imported from a check module. 3) fits.py PROBES dict + selfcheck.feature_fit + night jobs named 'fits <verb>' through the existing night loop; cmd_usage's counting extracted as cost.counts(p, since) so fits shares it. Likely outcome: small diff, reuses the night's run/log/breaker and selfcheck's 5 min cache. 4) do less: only the self-check line, no night job. Fails if: read-only reports still never run, the user's ask. Choice 3 (80%): smallest diff covering all four asks; reuses doctor.check_release_age, ledger close_affected, meta last_tidy (+ doctor_at, written by cmd_doctor) and one git worktree list.
## Risks and rollback
## Execution prompt
## Steps
1. [x] situation probes (fits.py), each a cheap state read returning a line or None, test-first
2. [x] self-check line plus the drive running read-only verbs itself
3. [x] sampo usage: features with no situation, most-used-by-description first
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_fits` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 32.3s (1 jobs, 16 at a time; slowest: loader._FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree f7cbdd887db5] [world 2f1906870a] (2026-11-06T19:16:48Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_fits` → exit 0 · Ran 7 tests in 15.5s (1 jobs, 16 at a time; slowest: Fits 4s) / OK [ran] [tree e8d65afbda4f] [world 2f1906870a] (2026-11-06T19:26:09Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_fits test_selfcheck test_night` → exit 0 · Ran 68 tests in 5.9s (26 jobs, 16 at a time; slowest: Fits 4s, Night.test_a_night_runs_its_jobs_and_the_digest_says_so 2s, NightInstall 2s) / OK [ran] [tree e8d65afbda4f] [world 2f1906870a] (2026-11-06T19:26:19Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_fits test_cost` → exit 0 · Ran 29 tests in 3.8s (17 jobs, 16 at a time; slowest: Fits 3s, SkillUsage 2s, TaskCostCap.test_a_cap_hit_asks_for_a_checkpoint_and_no_cap_changes_nothing 1s) / OK [ran] [tree e8d65afbda4f] [world 2f1906870a] (2026-11-06T19:26:30Z)
## Log
- 2026-11-06T19:05:56Z created
- 2026-11-06T19:06:15Z lane: ~/.claude/foreman.lanes/T-3499 on foreman/T-3499
- 2026-11-06T19:13:49Z focused
- 2026-11-06T19:13:51Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-11-05: [costly] T-3219: the standing core yes now passes self-change gate holds made only of footprint, verb-count or hook-speed rows, per the user's 'I sa…
- similar finished tasks took 3–3 steps
