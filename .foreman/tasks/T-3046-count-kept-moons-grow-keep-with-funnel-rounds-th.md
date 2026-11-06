---
id: T-3046
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/moonscale.py, plugin/lib/sampo/night.py, plugin/tests/test_moons_scale.py, plugin/tests/test_night.py]
depends_on: []
source: user
created: 2026-11-05T00:08:39Z
updated: 2026-11-05T01:18:01Z
builder_model: haiku
inferred_deps: [T-3042, T-3045]
inferred_why: T-3042: named in its request; T-3045: part 2 counts survivors from part 1's funnel and yield
base: 5de167c784f44cc82a9dc40f1f944a571df03532
base_tree: f78e3fa0e0e26879c8e1e388fbad1b22b4f74474
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T00:10:07Z
plan0_scope: [plugin/lib/sampo/moonscale.py, plugin/lib/sampo/night.py, plugin/tests/test_moons_scale.py, plugin/tests/test_night.py]
lane_stop: merged 2026-11-05T01:06:24Z
verified: strong
unproven: [docs]
---
# Count kept moons: grow --keep with funnel rounds, the night counts survivors, families from stored links (T-3042 part 2)
## Raw request
> Count kept moons: grow --keep with funnel rounds, the night counts survivors, families from stored links (T-3042 part 2)
## Interpretation
Reading 1 (taken): the 10,000 goal counts kept moons, so grow continues with funnel rounds until survivors reach the target, the night job follows that count, and families stay fast at that size. Reading 2 (ruled out): keep counting the store and raise its target: a 350,000-row store at today's yield, not what the user asked.
## Assumptions (confidence)
## Acceptance criteria
- [x] grow --keep N runs grow and funnel rounds until N moons are kept (survivors at novelty), or max-calls, the budget or failures stop it — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] The night's grow job and its gate count kept moons: they grow while survivors are under 10,000 — verify with `python3 plugin/tests/run.py test_moons_scale test_night`
- [x] Families from links stored at novelty: the same groups as all pairs on a fixture, and 10,000 synthetic survivors group in under 10 s — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
1) grow --keep N interleaving grow and funnel rounds; the night reads survivors: likely outcome: one verb owns the stop rule. 2) a separate fill verb looping the two jobs: fails if: two stop rules drift apart. 3) the night alone, raising its store target nightly: fails if: a day-time fill has no verb. 4) use what exists: grow() and funnel() as they are, called in rounds; families' union-find kept, fed by links the novelty scan already computes: likely outcome: no extra similarity work. 5) do less: only change TARGET's meaning in night_ready: fails if: families take 10 minutes a rebuild at 10,000. Choice 1 (85%): with 4's reuse for families (links from the novelty scan are exact for single link).
## Risks and rollback
Blast radius (sampo graph blast): co-changes CHANGELOG.md, plugin/lib/fmnight.py, MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/rune.py; past FIXes T-2593, T-2940.
## Execution prompt
The parent's brief holds the live data, the design and the measured numbers: read its Execution prompt first (state/projects/foreman-4a056f/tasks/T-3042-and-with-the-10000-moons-thing-i-want-it-to-lite.md). Stores stay append-only (candidates.jsonl, funnel.jsonl are never rewritten; a fate is a row's last event). Never print LLM_API_KEY (models.secret() reads it). Work test-first in plugin/tests/test_moons_scale.py; run python3 plugin/tests/run.py test_moons_scale before each commit. Part 2 = the parent's item (4): grow(keep=N) and CLI --keep, night_ready and night.py counting survivors, families from stored links with a one-time chunked backfill, equality with all pairs on a fixture, 10,000 synthetic survivors grouped in under 10 s.
## Steps
1. [x] grow --keep with funnel rounds (tests first)
2. [x] night_ready and the night job count survivors (tests first)
3. [x] families from stored links, backfill, timing (tests first)
## Resume here
<!-- auto -->
- 2026-11-05T00:30:38Z steps 3/3 done
- git: worktree-agent-a23067dcc87d0e848; 1 uncommitted: plugin/lib/sampo/moonscale.py
- touched since last checkpoint: plugin/lib/sampo/night.py, plugin/tests/test_moons_scale.py, plugin/lib/sampo/moonscale.py
## Docs impact
CHANGELOG line; MASTER.md's grow line
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_moons_scale.FamilyLinks test_moons_scale.KeepGrow 2>&1 | tail -30` → exit 0 · Ran 8 tests in 1.1s (2 classes, 16 at a time; slowest: FamilyLinks 1s, KeepGrow 1s) / OK [ran] [tree d630cd76ee48] [world 2f1906870a] (2026-11-05T00:14:36Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale test_night 2>&1 | tail -8` → exit 0 · Ran 104 tests in 11.9s (29 classes, 16 at a time; slowest: Night 12s, StoreLock 5s, NightTick 5s) / OK [ran] [tree d630cd76ee48] [world 2f1906870a] (2026-11-05T00:14:52Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale test_night 2>&1 | tail -8` → exit 0 · Ran 104 tests in 11.9s (29 classes, 16 at a time; slowest: Night 12s, StoreLock 5s, NightTick 5s) / OK [ran] [tree d630cd76ee48] [world 2f1906870a] (2026-11-05T00:14:52Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale.KeepGrow` → exit 0 · Ran 4 tests in 0.9s (1 classes, 16 at a time; slowest: KeepGrow 1s) / OK [ran] [tree d630cd76ee48] [world 2f1906870a] (2026-11-05T00:14:56Z)
- (step 2) `python3 plugin/tests/run.py test_night` → exit 0 · Ran 49 tests in 11.9s (16 classes, 16 at a time; slowest: Night 12s, NightTick 3s, NightGuards 3s) / OK [ran] [tree d630cd76ee48] [world 2f1906870a] (2026-11-05T00:15:09Z)
- (step 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 56 tests in 7.6s (14 classes, 16 at a time; slowest: StoreLock 7s, Funnel 5s, Grow 4s) / OK [ran] [tree d630cd76ee48] [world 2f1906870a] (2026-11-05T00:15:18Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_left_out test_mint test_models test_moons_scale test_night test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [19.27s] [ran] [tree d630cd76ee48] [world 2f1906870a] (2026-11-05T00:17:07Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale test_night 2>&1 | tail -40` → ✗ exit 1 · Ran 108 tests in 11.9s (29 classes, 16 at a time; slowest: Night 11s, NightTick 5s, NightGuards 4s) / FAILED (2 classes: test_moons_scale.KeepGrow, test_moons_scale.FamilyLinks) [ran] [tree 270d7e4f1266] [world 2f1906870a] (2026-11-05T00:32:06Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale test_night 2>&1 | tail -30` → exit 0 · Ran 108 tests in 24.0s (29 classes, 16 at a time; slowest: Night 23s, NightGuards 9s, NightInstall 9s) / OK [ran] [tree 806b41a2c144] [world 2f1906870a] (2026-11-05T00:32:52Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale test_night` → exit 0 · Ran 108 tests in 36.7s (29 classes, 16 at a time; slowest: Night 36s, NightGuards 15s, NightInstall 12s) / OK [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:15:06Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_night` → exit 0 · Ran 108 tests in 16.1s (29 classes, 16 at a time; slowest: Night 16s, NightTick 7s, NightGuards 7s) / OK [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:15:28Z)
- (step 3) `python3 plugin/tests/run.py test_moons_scale test_night` → exit 0 · Ran 108 tests in 16.7s (29 classes, 16 at a time; slowest: Night 16s, NightTick 7s, NightGuards 7s) / OK [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:15:46Z)
- `python3 plugin/tests/run.py test_moons_scale.KeepGrow test_moons_scale.FamilyLinks` → ✗ exit 1 · Ran 12 tests in 2.6s (2 classes, 16 at a time; slowest: FamilyLinks 1s, KeepGrow 1s) / FAILED (2 classes: test_moons_scale.KeepGrow, test_moons_scale.FamilyLinks) (start tree + this task's tests) [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:16:26Z)
- `python3 plugin/tests/run.py test_moons_scale.KeepGrow test_moons_scale.FamilyLinks` → exit 0 · Ran 12 tests in 2.5s (2 classes, 16 at a time; slowest: KeepGrow 2s, FamilyLinks 1s) / OK [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:16:26Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 60 tests in 6.7s (14 classes, 16 at a time; slowest: StoreLock 6s, Funnel 3s, KeepGrow 3s) / OK [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:16:48Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale test_night` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T01:15:46Z [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:16:48Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 60 tests in 6.7s (14 classes, 16 at a time; slowest: StoreLock 6s, Funnel 3s, KeepGrow 3s) / OK [ran] [tree 33bfe050a99e] [world 2f1906870a] (2026-11-05T01:16:48Z)
- (audit intent) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 MEDIUM (the stall check counted rejected rows, so a local-only --keep run on rows admit() rejects looped forever) and 5 LOW; all fixed test-first by the builder (stall on survivors, --keep with --target refused, links keyed by method and bar, MASTER line, a real grow-and-funnel round); I read the fixes and the new tests; red→green proved on KeepGrow and FamilyLinks` → the goal counts kept moons: grow --keep N rounds until N survive, the night's gate and job count survivors (10,000), families from stored links [tree 33bfe050a99e] (2026-11-05T01:16:48Z)
- (audit edge) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 MEDIUM (the stall check counted rejected rows, so a local-only --keep run on rows admit() rejects looped forever) and 5 LOW; all fixed test-first by the builder (stall on survivors, --keep with --target refused, links keyed by method and bar, MASTER line, a real grow-and-funnel round); I read the fixes and the new tests; red→green proved on KeepGrow and FamilyLinks` → a model whose rows all fail admit stops 'stalled' after 3 rounds (pinned with a real grow); embedder down: survivors without a record stay unlinked, no all-pairs rescan under shingles; a changed family bar counts as no record [tree 33bfe050a99e] (2026-11-05T01:16:48Z)
- (audit operator) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 MEDIUM (the stall check counted rejected rows, so a local-only --keep run on rows admit() rejects looped forever) and 5 LOW; all fixed test-first by the builder (stall on survivors, --keep with --target refused, links keyed by method and bar, MASTER line, a real grow-and-funnel round); I read the fixes and the new tests; red→green proved on KeepGrow and FamilyLinks` → 10,000 synthetic survivors group in about 1 s (asserted under 10 s); the first families run on old survivors backfills once in chunks of 500 and resumes [tree 33bfe050a99e] (2026-11-05T01:16:48Z)
- (audit maintainer) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 MEDIUM (the stall check counted rejected rows, so a local-only --keep run on rows admit() rejects looped forever) and 5 LOW; all fixed test-first by the builder (stall on survivors, --keep with --target refused, links keyed by method and bar, MASTER line, a real grow-and-funnel round); I read the fixes and the new tests; red→green proved on KeepGrow and FamilyLinks` → links.jsonl is append-only and unioned, so duplicates are harmless; KeepGrow and FamilyLinks test classes, one end-to-end round with the stub model [tree 33bfe050a99e] (2026-11-05T01:16:48Z)
## Log
- 2026-11-05T00:08:39Z created
- 2026-11-05T00:09:20Z set approved=True
- 2026-11-05T00:09:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3046.builder.md
- 2026-11-05T00:10:06Z focused
- 2026-11-05T00:10:07Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T01:06:24Z merged worktree-agent-a23067dcc87d0e848 (7 file(s))
- 2026-11-05T01:06:24Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a23067dcc87d0e848
- 2026-11-05T01:14:20Z focused
- 2026-11-05T01:14:28Z scope: MASTER.md (the reviewer asked for --keep in the moons grow line), rune.py (the verb's --keep wiring), CHANGELOG.md
- 2026-11-05T01:17:58Z done
- 2026-11-05T01:18:01Z committed 53d75b0e (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- T-3042 [FEATURE L, planned, 4 steps] 10,000 moons kept and used, and moons on anything related to Sampo
- research T-2865-review: Verdict:** approve with nits. This covers only T-2865's own code, which in this diff is two later patches to moonscale.py, one hunk in rune.py an…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_moons_scale.py, plugin/tests/test_night.py, plugin/tests/test_small_cards.py
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/moonscale.py, plugin/lib/sampo/night.py, plugin/tests/test_moons_scale.py, plugin/tests/test_night.py; re-ground the plan against them before editing
## Lessons
- A loop's stop rule must count the outcome it is for: counting rows added let a run whose rows were all rejected look like progress forever
## Files touched
- plugin/tests/test_moons_scale.py
- .fm-scratch/e.json
- plugin/tests/test_night.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/night.py
- MASTER.md
- CHANGELOG.md
