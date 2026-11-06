---
id: T-2536
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbench.py, plugin/tests/test_bench_family.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T04:14:14Z
updated: 2026-11-02T05:07:53Z
inferred_deps: [T-2534]
inferred_why: T-2534: Subtraction needs the guard-only arm's scores
group: lean ratchet and exam subtraction
base: ee895279ed9ca8a01540f8312841fc61785076cc
base_tree: dd52b282260e38abdbcafd20a15b8d4fd65c8c05
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T04:28:52Z
plan0_scope: [plugin/lib/fmbench.py, plugin/tests/test_bench_family.py, CHANGELOG.md]
verified: strong
---
# fm bench duel --ablate captures one subtraction candidate per feature whose off arm changed no pass and cost no more
## Raw request
> FEATURE: subtract by evidence: after an exam run with both the foreman and guard arms, fm doctor shows the injected chars beside the foreman-minus-guard delta per kind and on the long-horizon tier, and captures one subtraction task only where the guard arm scored no lower anywhere, held-out included
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a duel --ablate run whose off arm passes as many cases as full Foreman at no more cost captures one candidate per feature, naming the run and the confirmation a cut needs; a rerun captures no duplicate — verify with `python3 plugin/tests/run.py test_bench_family`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: after fm bench duel --ablate scope (stub: same passes), the inbox holds one candidate naming scope, the duel label and the every-kind plus long-horizon confirmation; a second run adds none
2. [x] fmbench's ablate branch calls fmeco.capture_once (source bench, key per feature) for each feature with so == sf and co <= cf
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bench_family` → ✗ exit 1 · Ran 23 tests in 24.6s (11 classes, 16 at a time; slowest: Judged 24s, Ablation 19s, Duel 16s) / FAILED (1 classes: test_bench_family.Ablation) [ran] [tree 9afb3c2a769e] [world 2f1906870a] (2026-11-02T04:29:27Z)
- (step 1) `python3 plugin/tests/run.py test_bench_family.Ablation` → ✗ exit 1 · Ran 3 tests in 9.4s (1 classes, 16 at a time; slowest: Ablation 9s) / FAILED (1 classes: test_bench_family.Ablation) [ran] [tree 15f98513ccca] [world 2f1906870a] (2026-11-02T04:30:25Z)
- (step 2) `python3 plugin/tests/run.py test_bench_family` → ✗ exit 1 · Ran 23 tests in 28.1s (11 classes, 16 at a time; slowest: Judged 28s, Ablation 24s, Duel 20s) / FAILED (1 classes: test_bench_family.Ablation) [ran] [tree abd45ad23685] [world 2f1906870a] (2026-11-02T04:31:40Z)
- (step 2) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 23 tests in 24.7s (11 classes, 16 at a time; slowest: Judged 24s, Ablation 21s, Duel 17s) / OK [ran] [tree 150449523850] [world 2f1906870a] (2026-11-02T04:32:32Z)
- (ac 1) `python3 plugin/tests/run.py test_bench_family` → exit 0 · Ran 23 tests in 13.0s (11 classes, 16 at a time; slowest: Judged 13s, Ablation 11s, Duel 8s) / OK [ran] [tree 6205a9436f42] [world 2f1906870a] (2026-11-02T04:40:35Z)
- (step 1) `python3 plugin/tests/run.py test_bench_family.Ablation` → exit 0 · Ran 3 tests in 9.8s (1 classes, 16 at a time; slowest: Ablation 10s) / OK [ran] [tree 6205a9436f42] [world 2f1906870a] (2026-11-02T04:40:35Z)
- (audit edge) `self-review: the capture sits after each feature's verdict line; only so == sf and co <= cf files; capture_once keys on a phrase in the text, so reruns and dropped candidates ask once` → a feature that helps (fewer passes off) or costs more off files nothing; a rerun with a new stamp files no duplicate; the candidate's text names the run and the confirmation a cut needs [tree 6205a9436f42] (2026-11-02T04:40:35Z)
- (audit self) `self-review: the capture sits after each feature's verdict line; only so == sf and co <= cf files; capture_once keys on a phrase in the text, so reruns and dropped candidates ask once` → no findings [tree 6205a9436f42] (2026-11-02T04:40:35Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree a452a4909a68] [world 2f1906870a] (2026-11-02T05:07:53Z)
## Log
- 2026-11-02T04:14:14Z created
- 2026-11-02T04:20:08Z blocked: waits for the end-of-run exam (rule 6): no fm bench duel --ablate run exists yet (0 in bench/ and the ledger), so a capture from its verdicts has nothing to act on; build it with that run
- 2026-11-02T04:28:49Z set status=captured
- 2026-11-02T04:28:49Z planned from capture
- 2026-11-02T04:28:50Z focused
- 2026-11-02T04:28:52Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T04:32:41Z scope: fmbench's --ablate branch captures one CLEAN candidate per tied feature through fmeco.capture_once (key in the text, so reruns and dropped candidates ask once); test in test_bench_family.Ablation
- 2026-11-02T04:41:17Z done
- 2026-11-02T04:41:19Z committed 912d89cc (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1787 [FEATURE M, done, 4 steps] Batch: Fm bench duel: hook-feature ablation, o…; Fm bench duel at an equal dollar cap: b… — lesson: Name each injected note's builder: …
- research mission-20261031-083832.pack: Mission 5, Genesis gen 1: 2. Exhaustive thinking. Before acting on anything non-trivial: list the readings of the request, every a…
- research mission-20261031-083836.pack: Mission 7, Genesis gen 1: 6. Verifying anything. Proof beyond unit tests: UI (`fm shot`, `fm flow`), data, docs against code, infr…
- decision 2026-11-01: [revisited: pause every long-horizon exam run] [cites: user steer 2026-10-31: (1) Pause every long-horizon exam run now. Keep the tier as built, but…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_bench.py
## Lessons
- capture_once's key matches the raw request text, so the key must be a literal phrase of that text, not a separate tag
## Plan gaps
- failed first: step 1 red test: after fm bench duel --ablate scope (stub: same passes), the inbox holds one candidate nam…
- failed first: step 2 fmbench's ablate branch calls fmeco.capture_once (source bench, key per feature) for each feature w…
## Files touched
- plugin/tests/test_bench_family.py
- plugin/lib/fmbench.py
- CHANGELOG.md
