---
id: T-1042
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmideas.py, plugin/tests/test_taste.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:07Z
updated: 2026-10-16T05:26:35Z
base: 538f4e9696b8fc1b1abbf31095b0393fd17740f9
base_tree: 735261e251308ffe055fa8dbbf095053d04e2cae
verified: strong
---
# Corrections that recur become proposed rules on their own: the user's repeated corrections
## Raw request
> Corrections that recur become proposed rules on their own: the user's repeated corrections (logged per prompt) clustered, and a correction met twice proposed as an fm rule or lesson (T-1029 C3)
## Interpretation
A correction the user makes twice, in similar words, becomes a proposal: an `fm rule add` command or a lesson to keep. `fm taste` lists these proposals. Corrections are already logged per prompt (fmhooks.py:612-617, event "correction"). Vetoes are recorded from them (fmcore.py:2058). Only repeated steers are clustered (fmideas.py:234 `proposals`, threshold TASTE_REPEATS=3), and corrections are never clustered. The cluster step, the threshold of 2 and the rule proposal are missing.
## Assumptions (confidence)
## Acceptance criteria
- [x] two similar corrections yield a proposal naming the shared words and a ready `fm rule add` line; one correction yields none; a recorded veto or rule suppresses it — verify with `python3 plugin/tests/run.py test_taste`
## Non-goals
## Approach (options → choice → why)
(a) A new module. (b) Extend fmideas.proposals to also read "correction" events at a threshold of 2. (c) A separate `correction_clusters` in fmideas that reuses `_key_words`. Choose (c). It reuses `_key_words` (fmideas.py:229) and the declined/covered filters. Corrections have different semantics (no "steer:" prefix, threshold 2), so a separate function is cleaner than flags on `proposals`. `correction_clusters(p)` groups "correction" ledger events by shared key words (at least 2 words in common, or 1 if rare). It returns {words, count, said, suggest}. The suggestion is `fm rule add "<regex of words>" --warn --why "<said>"`. Skip clusters covered by `c.vetoes`, existing `c.rules`, or `taste_declined`. `cmd_taste` prints a "Corrections met twice" section and includes `corrections` in the JSON. `fm taste decline` also covers these.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: log two "correction" events ("no, don't use mocks in db tests" and "stop mocking the database") via `c.log_event`. `fm taste --json` has `corrections[0].count == 2` and a `suggest` that contains "fm rule add". A single event gives an empty list. After `fm rule add`, the proposal disappears.
2. [x] Implement `correction_clusters` in fmideas.py and render it in `cmd_taste`.
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_taste` → ✗ exit 1 · Ran 5 tests in 7.0s (3 classes, 16 at a time; slowest: Taste 6s, KeepRates 4s, CorrectionClusters 2s) / FAILED (1 classes) [ran] [tree f82e5342229f] (2026-10-16T05:11:46Z)
- (step 2) `python3 plugin/tests/run.py test_taste` → exit 0 · Ran 5 tests in 3.2s (3 classes, 16 at a time; slowest: CorrectionClusters 3s, KeepRates 3s, Taste 3s) / OK [ran] [tree b08c5d237f2b] (2026-10-16T05:12:53Z)
- (step 1) `python3 plugin/tests/run.py test_taste` → ✗ exit 1 · Ran 10 tests in 1.9s (3 classes, 16 at a time; slowest: CorrectionClusters 2s, Taste 1s, KeepRates 1s) / FAILED (1 classes) [ran] [tree a9ff8cdee38c] (2026-10-16T05:19:11Z)
- (step 2) `python3 plugin/tests/run.py test_taste test_autonomy_user` → exit 0 · Ran 25 tests in 7.4s (6 classes, 16 at a time; slowest: TasteVetoes 7s, AskDigest 3s, CorrectionClusters 2s) / OK [ran] [tree 3197b228a4b6] (2026-10-16T05:20:38Z)
- (ac 1) `python3 plugin/tests/run.py test_taste` → exit 0 · Ran 10 tests in 2.2s (3 classes, 16 at a time; slowest: CorrectionClusters 2s, Taste 1s, KeepRates 1s) / OK [ran] [tree 85d5e279543b] (2026-10-16T05:26:34Z)
- (step 1) `python3 plugin/tests/run.py test_taste test_autonomy_user` → exit 0 · Ran 25 tests in 4.4s (6 classes, 16 at a time; slowest: TasteVetoes 4s, AskDigest 3s, CorrectionClusters 2s) / OK [ran] [tree 85d5e279543b] (2026-10-16T05:26:34Z)
- (audit self) `review: one fm-reviewer full pass; 5 findings and the stem-mismatch note fixed by the builder test-first` → no findings [tree 85d5e279543b] (2026-10-16T05:26:34Z)
## Log
- 2026-10-16T03:42:07Z created
- 2026-10-16T04:22:59Z set scope=['plugin/lib/fmideas.py', 'plugin/tests/test_taste.py']
- 2026-10-16T04:22:59Z set tier=S
- 2026-10-16T05:08:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1042.builder.md
- 2026-10-16T05:08:40Z focused
- 2026-10-16T05:26:20Z merged worktree-agent-a986b5833da4ccc1e (2 file(s))
- 2026-10-16T05:26:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a986b5833da4ccc1e
- 2026-10-16T05:26:21Z focused
- 2026-10-16T05:26:27Z scope: CHANGELOG.md — release note for the merged builder work
- 2026-10-16T05:26:35Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmideas.py changed since it was written]
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_ideas.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmideas.py, plugin/tests/test_taste.py; re-ground the plan against them before editing
## Lessons
- A rarity filter has to apply to every word of a multi-word match, not just single-word ones, or filler words carry the match
## Plan gaps
- failed first: step 1 Failing tests: log two "correction" events ("no, don't use mocks in db tests" and "stop mocking the…
## Files touched
- plugin/tests/test_taste.py
- plugin/lib/fmideas.py
- CHANGELOG.md
