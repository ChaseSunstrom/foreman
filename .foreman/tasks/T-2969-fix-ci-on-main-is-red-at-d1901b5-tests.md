---
id: T-2969
type: FIX
tier: M
status: planned
priority: normal
scope: []
depends_on: [T-3002]
source: discovered
created: 2026-11-04T13:53:41Z
updated: 2026-11-06T03:52:45Z
trigger: ci-red
trigger_key: 09aeed4b8bce88fb
group: CI-red fixes on main
---
# CI on main is green again: test_moons_scale stops needing a live embedder (T-3002) and test_ui_replay's timeout kills claude's own child on Linux
## Raw request
> FIX: CI on main is red at d1901b5 (tests)
> CONTEXT: found by the session-start sweep (T-1810): https://github.com/ChaseSunstrom/sampo/commit/d1901b57f2bd762970a78c245b9cced032e55795
> CI-red: d1901b57f2bd762970a78c245b9cced032e55795
## Interpretation
Reading 1 (chosen): CI on main has been red since d1901b5 (2026-11-04 13:22, two pushes): on ubuntu test_ui_replay.Run ('claude's own child outlived the timeout') and test_moons_scale.Families; on macOS test_moons_scale.Families and .Promote ('- Family: F-000003 (1 variant)' not found). The moons classes fail where no Ollama embedder answers (CI), which T-3002 fixes with a fake embedder; the ui_replay one is a child process that survives the replay's timeout kill on Linux. Reading 2: mark the classes skip on CI; rejected, CI would stop testing them.
## Assumptions (confidence)
## Acceptance criteria
- [ ] test_moons_scale passes with FOREMAN_NO_LOCAL_MODELS=1 (no embedder), as on CI — verify with `FOREMAN_NO_LOCAL_MODELS=1 python3 plugin/tests/run.py test_moons_scale`
- [ ] test_ui_replay.Run's timeout leaves no child of claude running: the replay starts claude in its own process group and kills the group on timeout — verify with `python3 plugin/tests/run.py test_ui_replay`
- [ ] the tests workflow on main passes on the next push — verify with `gh run list --branch main --workflow tests --limit 1 | grep -q success`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: T-3002's fake embedder for the moons classes; for ui_replay, kill the whole process group the replay starts (start_new_session and os.killpg on timeout), as Sampo's other runners do; likely outcome: both pass on CI. 2. Do less: raise the timeout; fails if: the child outlives any timeout because nothing kills it. 3. Skip on CI; fails if: CI stops testing them. Choice 1 (80%)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] T-3002's fake embedder (depends on it)  <- CURRENT
2. [ ] failing test: a fake claude that forks a sleeping child; after the timeout no child remains
3. [ ] the process-group kill in the replay runner
4. [ ] push through sampo ship and read CI
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T13:53:41Z created
- 2026-11-05T03:49:19Z planned from capture
- 2026-11-05T03:49:23Z set approved=True
- 2026-11-05T03:49:24Z set depends_on=['T-3002']
- 2026-11-05T03:49:24Z blocked: after T-3002 (the moons classes); the ui_replay part waits for a builder slot
- 2026-11-06T03:52:45Z unblocked
## Follow-ups captured
