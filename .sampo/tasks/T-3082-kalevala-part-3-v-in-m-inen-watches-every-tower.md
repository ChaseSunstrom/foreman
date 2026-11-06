---
id: T-3082
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/lib/sampo/kalevala.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py, plugin/tests/test_night.py, plugin/lib/sampo/budget.py, plugin/lib/sampo/cli.py, plugin/tests/test_kalevala_live.py]
depends_on: [T-3265]
source: user
created: 2026-11-05T00:34:18Z
updated: 2026-11-06T14:48:50Z
builder: 2026-11-05T20:57:25Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|431015|12747818
lane: ~/.claude/foreman/.claude/worktrees/agent-a6cdfeb01e8c00505
lane_branch: worktree-agent-a6cdfeb01e8c00505
base: fd073c44daf9d432d1398e14e3f6f50953d0af6a
base_tree: d610ab96d54cb01c4f79958dbbe34e62ad402db8
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T20:57:48Z
plan0_scope: [plugin/lib/sampo/kalevala.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py]
builder_returned: 2026-11-05T21:26:11Z
group: Kalevala towers and orchestration
lane_stop: merged 2026-11-06T00:40:37Z
lane_verified: 5c403348c1dfe9523985c9f84cf7db536080f17f
---
# Kalevala part 3: Väinämöinen watches every tower against what the user wanted and keeps them on track; the never-ending loop (T-3050)
## Raw request
> Kalevala part 3: Väinämöinen watches every tower against what the user wanted and keeps them on track; the never-ending loop (T-3050)
## Interpretation
Reading 1 (taken): Väinämöinen is Kalevala's supervisor: it reads every tower's state and acts to keep each one on what the user asked for, and Kalevala's rounds never stop on their own. Reading 2 (ruled out): a dashboard only: the user asked for it to keep them on track, which means acting.
## Assumptions (confidence)
## Acceptance criteria
- [ ] A super orchestrator monitors how they're doing: sampo kalevala watch reads each tower's generation, exam deltas, drift verdicts, stalls (no new generation in N hours), spend and open Missions, and prints one line per tower with its state — verify with `python3 plugin/tests/run.py test_kalevala`
- [ ] And keeps them on track with what the user wanted: each tower's latest seed and Missions are read cold against gen-0, the standing intent and the user's steers; an off-track tower gets a steer line in its steer file, a drifting one is paused, a stalled one restarted, two towers on the same files have one wait, a tower whose exam doesn't move in two generations gives its slot to one that improves; every act logged with its reason and shown in sampo kalevala status — verify with `python3 plugin/tests/run.py test_kalevala`
- [ ] An infinite loop: the night and the drive run Kalevala rounds (watch, then step) with no end of their own; only the user (sampo kalevala pause), a real usage limit or Väinämöinen's drift stop halts them — verify with `python3 plugin/tests/run.py test_kalevala test_night`
- [ ] Acts are reversible and watched: a snapshot and an undo line before restart or merge, merge pauses and points rather than deletes, Väinämöinen's steers pass the drift check before they're written — verify with `python3 plugin/tests/run.py test_kalevala`
- [ ] Proven live: a planted off-intent seed line and a planted stall in a real round are caught and acted on — verify with `python3 plugin/tests/run.py test_kalevala_live`
## Non-goals
## Approach (options → choice → why)
1) use what exists: rune's drift (gen-0 MUSTs and NEVERs, the cold read) per tower, steer files as the channel, lineage and exam lines for progress, the ledger for acts, night.py for the loop: likely outcome: supervision built from checks already trusted. 2) a model-only supervisor reading everything each round: fails if: costly and unverifiable; the cold read is used only where rules can't decide. 3) hard rules only: fails if: 'on track with what the user wanted' needs one judgment read per tower per round. 4) do less: alert the user: fails if: the user asked not to be asked. Choice 1 (80%).
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/sampo/cli.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/moonscale.py, plugin/tests/test_night.py, plugin/lib/fmkalevala.py; past FIXes T-3049.
## Execution prompt
Read T-3050's brief (state/projects/foreman-4a056f/tasks/T-3050-is-it-possible-to-have-orchestrators-of-orcehstr.md) and parts 1 and 2 (T-3053, T-3081) once merged. Build watch and the acts in kalevala.py, test-first in test_kalevala.py; the loop through night.py's job list and the drive. Acts are reversible and logged (ledger kalevala_act with tower, act, reason); a pause is a flag in the manifest the step respects. The cold read uses rune's existing reader with the tower's gen-0 and the user's steers; it never rewrites a MUST or NEVER.
## Steps
1. [x] watch: the per-tower readout (tests first)
2. [x] acts: steer, pause, restart, wait, move slots, each logged (tests first)
3. [x] the loop: night and drive rounds, pause and resume (tests first)
## Resume here
<!-- auto -->
- 2026-11-05T21:22:16Z steps 3/3 done
- git: worktree-agent-a6cdfeb01e8c00505; 4 uncommitted: plugin/lib/sampo/kalevala.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py, plugin/tests/test_night.py
- touched since last checkpoint: plugin/lib/sampo/cli.py, plugin/lib/sampo/kalevala.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py, plugin/tests/test_night.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 56 tests in 17.8s (8 jobs, 16 at a time; slowest: KalevalaStep 17s, Kalevala 4s, KalevalaGen 3s) / OK [ran] [tree a3095bbcd6f1] [world 2f1906870a] (2026-11-05T21:01:34Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [21.11s] [ran] [tree a3095bbcd6f1] [world 2f1906870a] (2026-11-05T21:02:44Z)
- (step 1) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 57 tests in 12.9s (8 jobs, 16 at a time; slowest: KalevalaStep 12s, Kalevala 3s, KalevalaGen 3s) / OK [ran] [tree adcee421145e] [world 2f1906870a] (2026-11-05T21:03:10Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [22.38s] [ran] [tree adcee421145e] [world 2f1906870a] (2026-11-05T21:04:00Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 57 tests in 17.3s (8 jobs, 16 at a time; slowest: KalevalaStep 16s, Kalevala 6s, KalevalaGen 5s) / FAILED (1 classes: test_kalevala.KalevalaStep) [ran] [tree 82cede9e4e8d] [world 2f1906870a] (2026-11-05T21:06:31Z)
- (step 1) `python3 plugin/tests/run.py test_kalevala test_budget` → exit 0 · Ran 70 tests in 17.4s (10 jobs, 16 at a time; slowest: KalevalaStep 17s, SessionStart 16s, Kalevala 6s) / OK [ran] [tree cab9388f182c] [world 2f1906870a] (2026-11-05T21:08:20Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | head -30` → ✗ exit 1 · Ran 63 tests in 13.6s (8 jobs, 16 at a time; slowest: KalevalaStep 13s, KalevalaWatch 3s, Kalevala 3s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 92e6eb4c19c6] [world 2f1906870a] (2026-11-05T21:11:28Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | head -30` → ✗ exit 1 · Ran 63 tests in 13.6s (8 jobs, 16 at a time; slowest: KalevalaStep 13s, KalevalaWatch 3s, Kalevala 3s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 92e6eb4c19c6] [world 2f1906870a] (2026-11-05T21:11:28Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|^FAILED" | head -30` → ✗ exit 1 · Ran 63 tests in 13.6s (8 jobs, 16 at a time; slowest: KalevalaStep 13s, KalevalaWatch 3s, Kalevala 3s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 92e6eb4c19c6] [world 2f1906870a] (2026-11-05T21:11:28Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -80` → ✗ exit 1 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 10292f1a2707] [world 2f1906870a] (2026-11-05T21:17:23Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -80` → ✗ exit 1 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 10292f1a2707] [world 2f1906870a] (2026-11-05T21:17:23Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | tail -80` → ✗ exit 1 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 10292f1a2707] [world 2f1906870a] (2026-11-05T21:17:23Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -40` → ✗ exit 1 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree add42988c23a] [world 2f1906870a] (2026-11-05T21:17:53Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -40` → ✗ exit 1 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree add42988c23a] [world 2f1906870a] (2026-11-05T21:17:53Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -40` → ✗ exit 1 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree add42988c23a] [world 2f1906870a] (2026-11-05T21:17:53Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -40` → ✗ exit 1 · Ran 63 tests in 16.0s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 637c10f67303] [world 2f1906870a] (2026-11-05T21:18:18Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -40` → ✗ exit 1 · Ran 63 tests in 16.0s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 637c10f67303] [world 2f1906870a] (2026-11-05T21:18:18Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -40` → ✗ exit 1 · Ran 63 tests in 16.0s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / FAILED (1 classes: test_kalevala.KalevalaWatch) [ran] [tree 637c10f67303] [world 2f1906870a] (2026-11-05T21:18:18Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -30` → exit 0 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / OK [ran] [tree e13627732104] [world 2f1906870a] (2026-11-05T21:19:04Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -30` → exit 0 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / OK [ran] [tree e13627732104] [world 2f1906870a] (2026-11-05T21:19:04Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -30` → exit 0 · Ran 63 tests in 16.1s (8 jobs, 16 at a time; slowest: KalevalaStep 15s, KalevalaWatch 5s, Kalevala 5s) / OK [ran] [tree e13627732104] [world 2f1906870a] (2026-11-05T21:19:04Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 63 tests in 16.2s (8 jobs, 16 at a time; slowest: KalevalaStep 16s, KalevalaWatch 5s, Kalevala 5s) / OK [ran] [tree e13627732104] [world 2f1906870a] (2026-11-05T21:19:22Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_budget test_cli test_doctor test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [12.16s] [ran] [tree e13627732104] [world 2f1906870a] (2026-11-05T21:20:01Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -50` → exit 0 · Ran 68 tests in 19.8s (8 jobs, 16 at a time; slowest: KalevalaStep 19s, KalevalaWatch 9s, Kalevala 5s) / OK [ran] [tree 3cf62e77b612] [world 2f1906870a] (2026-11-05T21:22:01Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -50` → exit 0 · Ran 68 tests in 19.8s (8 jobs, 16 at a time; slowest: KalevalaStep 19s, KalevalaWatch 9s, Kalevala 5s) / OK [ran] [tree 3cf62e77b612] [world 2f1906870a] (2026-11-05T21:22:01Z)
- (ac 4) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -50` → exit 0 · Ran 68 tests in 19.8s (8 jobs, 16 at a time; slowest: KalevalaStep 19s, KalevalaWatch 9s, Kalevala 5s) / OK [ran] [tree 3cf62e77b612] [world 2f1906870a] (2026-11-05T21:22:01Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala 2>&1 | grep -v ResourceWarning | grep -v "open(" | tail -50` → exit 0 · Ran 68 tests in 19.8s (8 jobs, 16 at a time; slowest: KalevalaStep 19s, KalevalaWatch 9s, Kalevala 5s) / OK [ran] [tree 3cf62e77b612] [world 2f1906870a] (2026-11-05T21:22:01Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala test_night 2>&1 | tail -60` → exit 0 · Ran 122 tests in 16.7s (25 jobs, 16 at a time; slowest: KalevalaStep 16s, Night 12s, KalevalaWatch 9s) / OK [ran] [tree 5300eacbea51] [world 2f1906870a] (2026-11-05T21:23:12Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala test_night` → exit 0 · Ran 122 tests in 20.1s (35 jobs, 16 at a time; slowest: KalevalaStep 20s, KalevalaWatch 8s, Kalevala 6s) / OK [ran] [tree 5300eacbea51] [world 2f1906870a] (2026-11-05T21:23:36Z)
- (ac 5) `python3 plugin/tests/run.py test_kalevala_live 2>&1 | tail -60` → exit 0 · Ran 2 tests in 1.9s (1 jobs, 16 at a time; slowest: KalevalaLive 1s) / OK [ran] [tree 19e757a097e9] [world 2f1906870a] (2026-11-05T21:24:28Z)
- (step 3) `python3 plugin/tests/run.py test_kalevala_live` → exit 0 · Ran 2 tests in 2.3s (1 jobs, 16 at a time; slowest: KalevalaLive 1s) / OK [ran] [tree 19e757a097e9] [world 2f1906870a] (2026-11-05T21:24:35Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_budget test_cli test_doctor test_kalevala test_kalevala_live test_left_out test_louhi_models test_mint test_models test_night test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [29.72s] [ran] [tree 19e757a097e9] [world 2f1906870a] (2026-11-05T21:25:50Z)
## Log
- 2026-11-05T00:34:18Z created
- 2026-11-05T00:34:21Z set approved=True
- 2026-11-05T20:57:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3082.builder.md
- 2026-11-05T20:57:45Z focused
- 2026-11-05T20:57:48Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T21:02:47Z scope: plugin/lib/sampo/cli.py widened for step 1: the kalevala verb's choices gain watch and --stall-hours (the only cli.py change)
- 2026-11-05T21:05:02Z scope: plugin/lib/sampo/budget.py widened for the spend fix: _record tags a child job's spend with FOREMAN_SPEND_TOWER (the tower's name) so watch can attribute it; kalevala.step() passes each tower its own env
- 2026-11-05T21:07:06Z set scope=['plugin/lib/sampo/kalevala.py', 'plugin/lib/sampo/night.py', 'plugin/tests/test_kalevala.py', 'plugin/lib/sampo/budget.py', 'plugin/lib/sampo/cli.py']
- 2026-11-05T21:22:53Z set scope=['plugin/lib/sampo/kalevala.py', 'plugin/lib/sampo/night.py', 'plugin/tests/test_kalevala.py', 'plugin/tests/test_night.py', 'plugin/lib/sampo/budget.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_kalevala_live.py']
- 2026-11-06T00:40:37Z merged worktree-agent-a6cdfeb01e8c00505 (7 file(s))
- 2026-11-06T00:56:36Z verified: the full suite is green on 5c403348c
- 2026-11-06T02:10:31Z set depends_on=['T-3265']
- 2026-11-06T14:48:50Z andon answered: the builder's assumption stands. Night runs Kalevala rounds in this lane; wiring the drive's Stop-hook continuation is a follow-up after T-3163 lands (it edits test_hooks.py), captured separately
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3050 [FEATURE L, blocked, 6 steps] Kalevala: many Rune towers at once on every aspect of Sampo, overseen by Väinämöinen, and evolving its own setup
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- T-2878 [FEATURE L, blocked, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- decision 2026-11-05: Kalevala (T-3050): namespaced Rune towers per aspect run at once, Väinämöinen oversees against the user's intent, Kalevala's own generations evolve …
- the similar finished task took 3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_kalevala.py, plugin/tests/test_night.py
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/kalevala.py, plugin/lib/sampo/night.py, plugin/tests/test_kalevala.py; re-ground the plan against them before editing
