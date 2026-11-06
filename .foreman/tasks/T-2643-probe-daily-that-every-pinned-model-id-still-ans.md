---
id: T-2643
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_model_probe.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T19:43:05Z
builder_model: sonnet
base: bfe7250d7a2161dd0d4c7964e7db06725fd5315c
base_tree: 3821497956f90c98971883536c793d7c9ce681c6
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T19:35:20Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_model_probe.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T19:41:44Z
verified: strong
---
# fm doctor checks, at most once a day, that each model name Foreman pins (fmgenesis.REVIEW_MODELS, the exam and steer defaults) still answers a one-line claude -p call; a dead one is a WARN naming where it is pinned
## Raw request
> FEATURE: Probe daily that every pinned model ID still answers (c10: Self-check of the runtime and upstream; value 3, effort S, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with a stub claude that refuses one model, fm doctor WARNs naming it and the module pinning it, caches the result for the day, and is quiet when all answer or claude is absent — verify with `python3 plugin/tests/run.py test_model_probe`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the cached probe and its doctor row
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_model_probe` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: ModelProbe 0s) / FAILED (1 classes: test_model_probe.ModelProbe) [ran] [tree 4b258d6a0ba0] [world 2f1906870a] (2026-11-02T19:35:42Z)
- (step 2) `python3 plugin/tests/run.py test_model_probe` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: ModelProbe 0s) / OK [ran] [tree 2420ee74c0db] [world 2f1906870a] (2026-11-02T19:35:54Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_anergy test_crash_hygiene test_doctor test_model_probe test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.56s] [ran] [tree 2420ee74c0db] [world 2f1906870a] (2026-11-02T19:36:22Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_anergy test_crash_hygiene test_doctor test_model_probe test_supply_delta && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [16.99s] [ran] [tree a8befaa55080] [world 2f1906870a] (2026-11-02T19:36:53Z)
- (step 2) `python3 plugin/tests/run.py test_model_probe test_doctor` → exit 0 · Ran 112 tests in 3.9s (40 classes, 16 at a time; slowest: ViewsRepair 3s, LockProbe 2s, Timing 2s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:42:28Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.6s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:42:38Z)
- (ac 1) `python3 plugin/tests/run.py test_model_probe` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: ModelProbe 0s) / OK [ran] [tree 1c68dd523ead] [world 2f1906870a] (2026-11-02T19:42:44Z)
- (audit operator) `builder lane (sonnet) built it test-first; my review of its diff found the probe ran a bare claude -p (it would load the user's hooks, Foreman's own included, and plugins in every probe session, with no budget check); fixed on main to go through fmideas.run_child, the stub test made to answer as claude -p --output-format json does` → at most four short isolated calls a day, cached in doctor-cache.json, skipped in tests and when claude is absent; a slow call now WARNs (the message says to check the login) rather than passing silently [tree 1c68dd523ead] (2026-11-02T19:42:44Z)
- (audit adversary) `builder lane (sonnet) built it test-first; my review of its diff found the probe ran a bare claude -p (it would load the user's hooks, Foreman's own included, and plugins in every probe session, with no budget check); fixed on main to go through fmideas.run_child, the stub test made to answer as claude -p --output-format json does` → the probe sends a fixed prompt to fixed model names from Foreman's own constants; nothing from user data reaches it [tree 1c68dd523ead] (2026-11-02T19:42:44Z)
- (audit self) `builder lane (sonnet) built it test-first; my review of its diff found the probe ran a bare claude -p (it would load the user's hooks, Foreman's own included, and plugins in every probe session, with no budget check); fixed on main to go through fmideas.run_child, the stub test made to answer as claude -p --output-format json does` → no findings [tree 1c68dd523ead] (2026-11-02T19:42:44Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T19:35:05Z planned from capture
- 2026-11-02T19:35:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2643.builder.md
- 2026-11-02T19:35:19Z focused
- 2026-11-02T19:35:20Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T19:41:44Z merged worktree-agent-ad888d01f373ef275 (2 file(s))
- 2026-11-02T19:41:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad888d01f373ef275
- 2026-11-02T19:41:59Z focused
- 2026-11-02T19:43:02Z done
- 2026-11-02T19:43:05Z committed 70245f9d (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2657 [FEATURE S, active, 3 steps] flakes.json counts each flaky test's fails and passes; fm doctor lists the three worst by fail rate with the command that flakes them
- T-2642 [FEATURE S, active, 3 steps] fm ship refuses to push when the tree it would push isn't the tree its tests ran on (an edit or checkout between the gates and the pu…
- T-2641 [FEATURE S, active, 3 steps] A removed fm verb or flag prints its tombstone (what replaced it and the task that removed it) instead of argparse's bare error; firs…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py
## Lessons
- A builder that shells out to claude reaches for a bare claude -p; every model call from fm goes through fmideas.run_child so hooks, tools and the budget stay out
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_model_probe.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
