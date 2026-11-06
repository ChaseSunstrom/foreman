---
id: T-1227
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-16T16:55:58Z
updated: 2026-10-16T20:09:40Z
base: 6004a75e9e40b58663761b730747008350fb468f
base_tree: 49e5a1e2057dbfee50fa30016a89e9fb49a97024
plan0_at: 2026-10-16T20:08:29Z
plan0_scope: []
verified: strong
---
# CI: the fm run --sandbox test needs no real bubblewrap
## Raw request
> After the next push, read the tests workflow's public annotations (curl api.github.com/.../check-runs/<job>/annotations | jq) and fix whatever fails on GitHub's runners (T-1223 follow-up)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_sandbox_runs_each_session_under_claude_codes_sandbox passes with no bwrap or socat on PATH — verify with `cd plugin/tests && python3 -m unittest test_unattended.RunModels`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Stub bwrap and socat in the test so the probe passes on any runner; prove it fails without them on PATH
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && PATH=/tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/nobwrap:$PATH python3 -m unittest test_unattended.RunModels` → exit 0 · Ran 3 tests in 1.302s / OK [ran] [tree 80cd3f7d44d5] (2026-10-16T20:08:47Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_unattended.RunModels` → exit 0 · Ran 3 tests in 1.303s / OK [ran] [tree 397fe598486e] (2026-10-16T20:08:56Z)
- (audit edge) `self: the CI annotation (FileNotFoundError …/argv in test_unattended) reproduced locally with a failing bwrap shadowing the real one; green with the stubs` → macOS keeps sandbox-exec, the stubs don't matter there [tree 397fe598486e] (2026-10-16T20:08:56Z)
- (audit self) `self: the CI annotation (FileNotFoundError …/argv in test_unattended) reproduced locally with a failing bwrap shadowing the real one; green with the stubs` → no findings [tree 397fe598486e] (2026-10-16T20:08:56Z)
## Log
- 2026-10-16T16:55:58Z created
- 2026-10-16T20:08:26Z planned from capture
- 2026-10-16T20:08:29Z focused
- 2026-10-16T20:09:39Z done
- 2026-10-16T20:09:40Z committed ed15bfb3 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1223 [FIX S, done, 1 steps] GitHub Actions' tests workflow failed on the 1.2.35 and 1.2.36 pushes (and 2e365585) while
- T-1206 [FEATURE M, done, 3 steps] A GitHub Pages site for Foreman: one modern page with the real demo, the loop, the guard and install — lesson: A marketing page for a d…
- playbook Release and changelog (skills/playbooks/references/release/release-and-changelog.md)
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- similar finished tasks took 1–3 steps
- start here (files T-1223 touched): plugin/tests/run.py, CHANGELOG.md
## Regression test
With a bwrap that exits 1 first on PATH (as on GitHub's runners), test_sandbox_runs_each_session_under_claude_codes_sandbox errored with FileNotFoundError …/argv, the CI annotation; with the stubs it passes the same way.
## Files touched
- plugin/tests/test_unattended.py
- CHANGELOG.md
