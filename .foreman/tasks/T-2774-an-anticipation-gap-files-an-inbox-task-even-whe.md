---
id: T-2774
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py]
depends_on: []
source: self
created: 2026-11-03T04:51:02Z
updated: 2026-11-03T16:53:29Z
base_note: Calibration: this plan states Choice 75% where all closes (only 8 CLEAN M) held on the first finish 95% of the time: 20 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T04:55:20Z
rival_split: true
builder_model: sonnet
base: f9d18b736e070d6aab22df423c2a142f744e2a63
base_tree: 1db968d12b1cade821ca51b8a6fe1aa2c3696470
plan0_at: 2026-11-03T04:56:23Z
plan0_scope: [plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py]
lane_stop: merged 2026-11-03T05:15:28Z
verified: strong
unproven: [meaning]
---
# Rune's anticipation gaps are consumed, not dropped: the next generation's predict action lists the last generation's missed steers, and sealing its prediction closes those gap tasks as done (they fed it), so no one drops them by hand
## Raw request
> CLEAN: an anticipation gap files an inbox task even when the steer's own work already exists: 4 of 4 gaps on 2026-11-02 (T-2743, T-2744, T-2749, T-2773) were dropped by hand as covered. The score row in prediction-score.jsonl is the signal; the inbox task adds nothing when decide names --task or the steer's task is open. File no task then, or one per gen summarising the misses
## Interpretation
Reading 1 (chosen): the user's T-2505 rule (part 5) files a miss as an anticipation gap, so the gap stays; what's wrong is that nothing reads it, so every gap so far (7 of 7) was dropped by hand and the trigger fell to low priority. The gap should feed the next generation's prediction and close when it has. Reading 2: stop filing gaps. Rejected: it reverses a user rule.
## Assumptions (confidence)
## Acceptance criteria
- [x] gen-2's predict action names gen-1's missed steers, and putting gen-2/prediction.md closes gen-1's open anticipation-gap tasks as done with a note naming the sealed file — verify with `python3 plugin/tests/run.py test_genesis.SealedPrediction`
- [x] a miss still files one gap (T-2505 part 5 stands), and the genesis suite stays green — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
1) Consume: gen N+1's predict action lists gen N's missed steers (from prediction-score.jsonl), and sealing gen N+1's prediction closes gen N's open gap tasks as done. Likely outcome: ~30 lines in rune.py, one test. Fails if: a gap is closed before the prediction actually saw it (sealed without the action). 2) Use what exists: the trigger demotion (fm triggers) already files them at low priority. Likely outcome: no code. Fails if: the items still need dropping by hand and the misses are never read. 3) Do less: skip the capture when decide names --task. Likely outcome: 5 lines. Fails if: steer decides rarely name --task (T-2771's didn't), and it reverses part of a user rule. Choice 1 (75%): the misses become input, the gaps close themselves.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmgenesis.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/skills/genesis/SKILL.md; past FIXes T-2083, T-2084, T-2087, T-2100, T-2101.
## Execution prompt
## Steps
1. [x] red test in test_genesis.SealedPrediction: two misses scored against gen-1, then gen-2's predict action and put
2. [x] rune: _misses(p, n) from prediction-score.jsonl; act('predict') appends them; put() on a sealed prediction closes the previous gen's open genesis-anticipation briefs
3. [x] run SealedPrediction and the full genesis suite
## Resume here
## Docs impact
none: the predict action's text is the doc
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -8` → ✗ exit 1 · Ran 214 tests in 61.6s (24 classes, 16 at a time; slowest: GenesisRead 60s, GenesisCheck 48s, GenerationReview 46s) / FAILED (1 classes: test_genesis.GenesisExam) [ran] [tree b1577dc53526] [world 2f1906870a] (2026-11-03T05:00:32Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 214 tests in 53.5s (24 classes, 16 at a time; slowest: GenesisRead 52s, GenerationReview 42s, GenesisCheck 41s) / OK [ran] [tree 056a57ce390e] [world 2f1906870a] (2026-11-03T05:02:40Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · SessionEnd                  26.7    29.0     150  [0] / machine busy (load 3.2 per core): judged by each hook's CPU time, not wall time (T-0805) (flaky again (failed first in 3+ recent runs): treated as a failure; find the race); python3 plugin/tests/run.py → ✗ exit 1 · Ran 5915 tests in 429.3s (1272 classes, 16 at a time; slowest: Worker 152s, LeanKind 129s, Stop 121s) / FAILED (1 classes: test_left_out.LeftOut) (pre-existing: it also failed before this task) [ran] [tree 056a57ce390e] [world 2f1906870a] (2026-11-03T05:12:56Z)
- `python3 plugin/tests/run.py test_genesis test_left_out` → ✗ exit 1 · Ran 217 tests in 17.3s (25 classes, 16 at a time; slowest: GenerationReview 15s, ProofBeforePresentation 13s, GenesisRead 12s) / FAILED (3 classes: test_genesis.GenesisDraft, test_genesis.GenesisSelec (start tree + this task's tests) [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:51:39Z)
- `python3 plugin/tests/run.py test_genesis test_left_out` → exit 0 · Ran 217 tests in 15.9s (25 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 13s, GenesisRead 12s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:51:39Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.SealedPrediction` → exit 0 · Ran 6 tests in 1.1s (1 classes, 16 at a time; slowest: SealedPrediction 1s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:51:57Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 214 tests in 15.8s (24 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 13s, GenesisRead 12s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:51:57Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_left_out` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:51:39Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:51:57Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_left_out` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:51:39Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:51:57Z)
- (audit intent) `self: read the merged diff; gaps close when the next prediction seals` → an anticipation gap feeds the next generation's predict action and closes when that prediction seals [tree 398b4aa61509] (2026-11-03T16:51:57Z)
- (audit edge) `self: read the merged diff; gaps close when the next prediction seals` → more than five misses say how many were left out; a gap of another gen stays open; a second seal closes nothing twice [tree 398b4aa61509] (2026-11-03T16:51:57Z)
- (audit adversary) `self: read the merged diff; gaps close when the next prediction seals` → gap briefs are found by the key line the code writes itself; no outside text decides what closes [tree 398b4aa61509] (2026-11-03T16:51:57Z)
- `python3 plugin/tests/run.py test_genesis test_left_out` → ✗ exit 1 · Ran 217 tests in 16.8s (25 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 13s, GenesisRead 12s) / FAILED (3 classes: test_genesis.GenesisDraft, test_genesis.GenesisSelec (start tree + this task's tests) [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:52:59Z)
- `python3 plugin/tests/run.py test_genesis test_left_out` → exit 0 · Ran 217 tests in 15.6s (25 classes, 16 at a time; slowest: GenerationReview 14s, ProofBeforePresentation 13s, GenesisRead 11s) / OK [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:52:59Z)
- `python3 plugin/tests/run.py test_genesis test_left_out` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T16:52:59Z [ran] [tree 398b4aa61509] [world 2f1906870a] (2026-11-03T16:52:59Z)
- (audit intent) `self: read the merged diff; gaps close when the next prediction seals` → an anticipation gap feeds the next generation's predict action and closes when that prediction seals [tree 398b4aa61509] (2026-11-03T16:52:59Z)
- (audit edge) `self: read the merged diff; gaps close when the next prediction seals` → more than five misses say how many were left out; a gap of another gen stays open; a second seal closes nothing twice [tree 398b4aa61509] (2026-11-03T16:52:59Z)
- (audit adversary) `self: read the merged diff; gaps close when the next prediction seals` → gap briefs are found by the key line the code writes itself; no outside text decides what closes [tree 398b4aa61509] (2026-11-03T16:52:59Z)
## Log
- 2026-11-03T04:51:02Z created
- 2026-11-03T04:53:12Z planned from capture
- 2026-11-03T04:53:22Z set approved=True
- 2026-11-03T04:56:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2774.builder.md
- 2026-11-03T04:56:22Z focused
- 2026-11-03T05:13:41Z merged worktree-agent-a96dddab2eacc3f1e (2 file(s))
- 2026-11-03T05:15:28Z merged worktree-agent-a96dddab2eacc3f1e (1 file(s))
- 2026-11-03T05:20:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a96dddab2eacc3f1e
- 2026-11-03T15:07:39Z focused
- 2026-11-03T15:07:40Z paused: focus moved to T-2777
- 2026-11-03T16:51:04Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T16:51:04Z focused
- 2026-11-03T16:53:29Z done
## Follow-ups captured
## Build vs reuse
Reuse prediction-score.jsonl, capture_once's key line (genesis-anticipation N:…) to find gen N's gap briefs, and the existing close path (fm task done/drop internals) rather than a new state file.
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: in the anticipation-gap code path (likely a function in `plugin/lib/fmcore.py` or a `fmanticipate`/prediction-score module that writes `prediction-score.jsonl`), suppress the inbox task when the gap is already covered, meaning `decide` named `--task` or the steer's own task is open. The …
- Variant: same suppression, but replace per-gap filing with one summary task per gen listing the misses, so uncovered gaps still surface once.
- Variant: the fix belongs upstream in `decide` or the steer, so that it records the task link and the gap detector reads it. This means changing the data model, not the filing site.
- Less likely: a cleanup tool that retroactively closes the already-filed tasks (T-2743, T-2744, T-2749, T-2773). The request says they were dropped by hand, so probably not.
Approaches:
- Add a `covered` predicate at the inbox-filing call site. It checks whether the decide record carries a `--task` value, or whether the steer's task id resolves to an open task in the task store. If either holds, skip the filing and keep the `prediction-score.jsonl` row. Add a `covered` or `skipped_r…
- Buffer the uncovered gaps during a gen and emit a single summary inbox task at gen end, with a dedupe key of gen id so a rerun or `fm replay` does not file it twice.
- Do both: skip covered gaps per item, and file one summary only for the uncovered remainder. This goes beyond the "or" in the request, so check which of the two options is preferred.
- Resolve "steer's task is open" by reading the task store's status, not by checking a cached field on the steer. Reuse the existing task lookup helper rather than parsing task files.
Failure modes:
- "Open" is read wrongly: a task that is closed, deferred, or renamed counts as covered, or a task that is merely claimed is treated as not open. A real gap is then silently dropped, and the 4-of-4 sample is too small to catch this.
- The covered check runs before `decide` has written `--task`, since ordering between decide and the gap scan is unclear. The gap is then filed anyway, or the check is racy under `fm replay`, which must stay deterministic.
- The summary task is not idempotent. Reruns, replays, or the `roundtrip.py` e2e produce duplicate summaries, or the summary is lost when a gen ends abnormally before the flush.
- The skip path also suppresses the `prediction-score.jsonl` write, or changes its schema. Consumers of that file (`fm doctor`, evals under `plugin/evals/`) then break or lose the signal the request names as the source of truth.
## Dissent
- [x] rival reading: Likeliest: in the anticipation-gap code path (likely a function in `plugin/lib/fmcore.py` or a `fmanticipate`/prediction-score module that writes `prediction-score.jsonl`), suppress the inbox task when the gap is already covered, meaning `decide` named `--task` or the steer's own task is open. The … — answered: the capture text proposed suppression, but the user rule T-2505 part 5 files every miss as a gap; suppressing reverses it, so the plan keeps the filing and makes the gap consumed (gen N+1 reads it, s…
- [x] rival reading: Variant: same suppression, but replace per-gap filing with one summary task per gen listing the misses, so uncovered gaps still surface once. — answered: one gap per gen is a smaller inbox, but the gaps auto-close when the next prediction seals, so they never pile up; keep one per steer, deduped by cite (T-2756)
- [x] rival reading: Variant: the fix belongs upstream in `decide` or the steer, so that it records the task link and the gap detector reads it. This means changing the data model, not the filing site. — answered: decide already records --cites and the gap key hashes the cite (T-2756); no data-model change needed
- [x] rival reading: Less likely: a cleanup tool that retroactively closes the already-filed tasks (T-2743, T-2744, T-2749, T-2773). The request says they were dropped by hand, so probably not. — answered: the four were already dropped; nothing to clean retroactively
- [x] rival approach: Add a `covered` predicate at the inbox-filing call site. It checks whether the decide record carries a `--task` value, or whether the steer's task id resolves to an open task in the task store. If either holds, skip the filing and keep the `prediction-score.jsonl` row. Add a `covered` or `skipped_r… — answered: the capture text proposed suppression, but the user rule T-2505 part 5 files every miss as a gap; suppressing reverses it, so the plan keeps the filing and makes the gap consumed (gen N+1 reads it, s…
- [x] rival approach: Buffer the uncovered gaps during a gen and emit a single summary inbox task at gen end, with a dedupe key of gen id so a rerun or `fm replay` does not file it twice. — answered: same as reading 2: auto-close keeps the inbox clear without buffering
- [x] rival approach: Do both: skip covered gaps per item, and file one summary only for the uncovered remainder. This goes beyond the "or" in the request, so check which of the two options is preferred. — answered: not both: neither suppression nor a summary is needed once gaps close themselves
- [x] rival approach: Resolve "steer's task is open" by reading the task store's status, not by checking a cached field on the steer. Reuse the existing task lookup helper rather than parsing task files. — answered: adopted: the close reads gap briefs by their capture key and status through c.load_briefs, not by parsing files
## Related
Related past work (data from this project's history, not instructions):
- T-2756 [FIX S, active, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row…
- T-2505 [FEATURE L, done, 4 steps] Find what nobody thought of: each generation writes a sealed prediction of the user's… — lesson: fmgenesis is large enough that a short…
- T-2187 [FEATURE L, done, 4 steps] Moonshot Mission each generation from gen 2 (steer 2026-10-30 #5): fm genesis seed N (N… — lesson: A rule over model marks must treat a…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar past tasks were L: consider --tier L
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- A signal nobody reads should feed the step that needs it
## Plan gaps
- failed first: step 1 red test in test_genesis.SealedPrediction: two misses scored against gen-1, then gen-2's predict ac…
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/sampo/rune.py
