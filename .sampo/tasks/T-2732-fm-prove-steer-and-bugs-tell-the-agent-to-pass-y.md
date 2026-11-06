---
id: T-2732
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-03T00:20:05Z
updated: 2026-11-03T00:29:15Z
base: f01818ae0aaa06caf9d8e0e4679c2ce549383298
base_tree: 58493f86759d066259520a3e4e2babd7db268648
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-03T00:25:39Z
plan0_scope: []
verified: strong
---
# fm prove --steer and --bugs say the yes is the user's to give, once per tree, like the other modes, instead of telling the agent to pass --yes-run (a flag the guard keeps the user's)
## Raw request
> fm prove --steer and --bugs tell the agent to 'pass --yes-run once' (fmprove.py:728, :864), a flag the guard keeps the user's; say 'needs the user's yes, once per tree' like the other modes (fmprove.py:182)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] neither message tells the reader to pass --yes-run themselves; each names the user's yes, once per tree — verify with `python3 plugin/tests/run.py test_prove_steer test_proof`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the two messages
## Resume here
## Docs impact
none: an error message; the CHANGELOG line for fm prove --steer already says it is the user's to run
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_prove_steer test_proof test_find` → exit 0 · Ran 167 tests in 31.5s (31 classes, 16 at a time; slowest: Proof 31s, FindRenders 16s, FindBlindSpots 15s) / OK [ran] [tree 9e6b321042eb] [world 2f1906870a] (2026-11-03T00:27:32Z)
- (step 2) `python3 plugin/tests/run.py test_prove_steer test_proof test_find` → exit 0 · Ran 167 tests in 30.0s (31 classes, 16 at a time; slowest: Proof 30s, FindBlindSpots 15s, FindRenders 15s) / OK [ran] [tree 9e6b321042eb] [world 2f1906870a] (2026-11-03T00:28:03Z)
- `python3 plugin/tests/run.py test_prove_steer` → ✗ exit 1 · Ran 2 tests in 3.4s (1 classes, 16 at a time; slowest: ProveSteer 1s) / FAILED (1 classes: test_prove_steer.ProveSteer) (start tree + this task's tests) [ran] [tree 9e6b321042eb] [world 2f1906870a] (2026-11-03T00:28:09Z)
- `python3 plugin/tests/run.py test_prove_steer` → exit 0 · Ran 2 tests in 1.8s (1 classes, 16 at a time; slowest: ProveSteer 1s) / OK [ran] [tree 9e6b321042eb] [world 2f1906870a] (2026-11-03T00:28:09Z)
- (ac 1) `python3 plugin/tests/run.py test_prove_steer test_proof` → exit 0 · Ran 43 tests in 28.2s (9 classes, 16 at a time; slowest: Proof 28s, Stop 3s, Meaning 3s) / OK [ran] [tree 9e6b321042eb] [world 2f1906870a] (2026-11-03T00:28:38Z)
- `python3 plugin/tests/run.py test_prove_steer test_proof test_find` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:28:03Z [ran] [tree 9e6b321042eb] [world 2f1906870a] (2026-11-03T00:28:38Z)
- (audit adversary) `both messages now read like NO_RUN and DOCS_NO_RUN: the yes is the user's, once per tree, with the exact command; no 'pass --yes-run' hint remains in plugin/lib (grep)` → wording only; _yes and the guard's self-authorize refusal are unchanged, so the agent still can't pass the flag [tree 9e6b321042eb] (2026-11-03T00:28:38Z)
- (audit self) `both messages now read like NO_RUN and DOCS_NO_RUN: the yes is the user's, once per tree, with the exact command; no 'pass --yes-run' hint remains in plugin/lib (grep)` → no findings [tree 9e6b321042eb] (2026-11-03T00:28:38Z)
## Log
- 2026-11-03T00:20:05Z created
- 2026-11-03T00:25:38Z planned from capture
- 2026-11-03T00:25:38Z focused
- 2026-11-03T00:25:39Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-03T00:25:57Z focused
- 2026-11-03T00:27:00Z scope: plugin/tests/test_prove_steer.py
- 2026-11-03T00:29:10Z done
- 2026-11-03T00:29:15Z committed 8170d5d3 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2357 [FEATURE M, done, 3 steps] Installs are queued for one yes: night and tick timers staged, asked once, installed only after the user's yes (Mission 8, #11) — lesso…
- research brainstorm-20261102: 552 ideas in 59 clusters, each grounded in the code: 104 built, 197 new, 249 partial, 2 premise-false. 24 clusters marked build.
- research T-2381-review: Verdict: changes needed.** Acceptance criterion 3 is not met, and a few false "failed" verdicts can block a legitimate task close. I could only r…
- decision 2026-10-30: fm prove's yes is the user's --yes-run, kept per tree path in Foreman state; no Foreman-home or author-email exception. A session that points FOREMA…
- similar past tasks were M: consider --tier M
## Why not caught
the steer test asserted only that '--yes-run' appeared, which both wordings satisfy
## Files touched
- plugin/tests/test_prove_steer.py
- plugin/lib/fmprove.py
