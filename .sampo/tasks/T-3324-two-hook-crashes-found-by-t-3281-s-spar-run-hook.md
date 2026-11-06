---
id: T-3324
type: FIX
tier: S
status: active
priority: normal
scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py]
depends_on: []
source: discovered
created: 2026-11-06T04:30:12Z
updated: 2026-11-06T05:58:53Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a307c8db10ab6c4fc
lane_branch: worktree-agent-a307c8db10ab6c4fc
base: 0e503eeeeb87000325d02673ba119e35ff08b7e8
base_tree: 5c2bb7b2f14ef72b4659b9d747b61d1c44bc9aca
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T05:52:11Z
plan0_scope: [plugin/lib/sampo/hooks.py, plugin/tests/test_hooks.py]
---
# Two hook crashes the spar fuzzer found are clean refusals
## Raw request
> Two hook crashes found by T-3281's spar run: hooks.py:1417 meta.pop('resume_after_reload') has no default and raises KeyError; hooks.py:130 json.loads on hook stdin is unguarded, so malformed input is a traceback, not a clean refusal. Test each with the malformed payload
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] malformed JSON on a hook's stdin exits cleanly with a one-line refusal, no traceback (hooks.py:~130); meta without resume_after_reload no longer raises KeyError (hooks.py:~1417) — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] two failing tests with the malformed payloads
2. [x] guard json.loads; pop with a default
## Resume here
## Docs impact
## Verification evidence
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 261 tests in 305.1s (153 jobs, 16 at a time; slowest: SessionStart.test_budget_holds_with_large_queue 27s, Approvals 26s, UserPromptSubmit 25s) / OK [ran] [tree fd3904144fd6] [world 2f1906870a] (2026-11-06T05:58:47Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.SparCrashes` → exit 0 · Ran 2 tests in 207.5s (1 jobs, 16 at a time; slowest: SparCrashes 4s) / OK [ran] [tree fd3904144fd6] [world 2f1906870a] (2026-11-06T05:58:53Z)
## Log
- 2026-11-06T04:30:12Z created
- 2026-11-06T05:51:44Z planned from capture
- 2026-11-06T05:52:07Z focused
- 2026-11-06T05:52:11Z predicted from its closes: 2 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3281 [FEATURE M, active, 3 steps] Moon C-001120: nightly spar (spar.py) feeds mutated hook payloads and CLI args to a temp home, files any traceback as a FIX with the …
- research T-1879-review: Verdict:** changes needed (two small gaps against the acceptance criterion). I read the diff and the surrounding code but did not run `plugin/tes…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py
