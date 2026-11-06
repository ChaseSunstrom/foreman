---
id: T-0975
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_unattended.py, CHANGELOG.md, README.md]
depends_on: []
source: followup
created: 2026-10-15T22:08:01Z
updated: 2026-10-15T23:20:33Z
base: d2fa96a42d1d930a4d6c3802c25d1676aec20a0c
base_tree: 2343fb58f89e4b49cb3f58f280bd43124538116a
verified: strong
---
# Fm run --sandbox: headless sessions under Claude Code's native sandbox settings (confirm t
## Raw request
> fm run --sandbox: headless sessions under Claude Code's native sandbox settings (confirm the settings key in its docs first), from OpenHands (research/T-0964-catalogue.md)
## Interpretation
fm run (and its parallel lanes) can start each headless claude -p session under Claude Code's own sandbox (bubblewrap on Linux, Seatbelt on macOS): Bash commands may write only the session's cwd plus what Foreman itself needs; the session fails instead of running unsandboxed when the sandbox is unavailable. Opt-in per run.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm run --sandbox passes --settings with sandbox enabled, failIfUnavailable, no unsandboxed fallback, and writes allowed to Foreman's state and the repo's git dir (a lane commits there); without the flag nothing changes — verify with `python3 plugin/tests/run.py -k RunModels`
## Non-goals
## Approach (options → choice → why)
Options: (1) --settings JSON per claude -p (no file, per run) — chosen; (2) a settings file in state passed by path (another file to keep in sync); (3) sandbox in the project's .claude/settings.local.json (changes interactive sessions too); (4) wrap sessions in bwrap ourselves (re-implements Claude Code's sandbox). Writes outside the session's cwd that fm needs: FOREMAN state (fm commands run inside Bash) and the git common dir (a lane's commits land in the main repo's .git).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing RunModels test
2. [x] the flag and the settings JSON; docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k RunModels` → ✗ exit 1 · Ran 3 tests in 2.4s (1 classes, 16 at a time; slowest: RunModels 2s) / FAILED (1 classes) [ran] [tree 5fcec5f8d6aa] (2026-10-15T23:18:50Z)
- (step 2) `python3 plugin/tests/run.py -k RunModels` → exit 0 · Ran 3 tests in 3.5s (1 classes, 16 at a time; slowest: RunModels 3s) / OK [ran] [tree 1a19f7fe81e3] (2026-10-15T23:20:25Z)
- (ac 1) `python3 plugin/tests/run.py -k RunModels` → exit 0 · Ran 3 tests in 3.1s (1 classes, 16 at a time; slowest: RunModels 3s) / OK [ran] [tree 1a19f7fe81e3] (2026-10-15T23:20:29Z)
- (audit intent) `self: read _claude_cmd/_sandbox; opt-in flag, getattr default so other callers are unchanged; settings JSON passed as one argv element (no shell); live smoke run not done: the guard's plugin category refuses a direct claude --settings without the user's yes; keys per code.claude.com/docs/en/sandboxing.md` → opt-in sandbox for headless sessions, fail closed when unavailable [tree 1a19f7fe81e3] (2026-10-15T23:20:29Z)
- (audit adversary) `self: read _claude_cmd/_sandbox; opt-in flag, getattr default so other callers are unchanged; settings JSON passed as one argv element (no shell); live smoke run not done: the guard's plugin category refuses a direct claude --settings without the user's yes; keys per code.claude.com/docs/en/sandboxing.md` → the settings JSON is built from fixed keys plus two paths fm computes (state dir, git common dir), nothing from the task or the model; allowUnsandboxedCommands false removes the dangerouslyDisableSandbox escape; failIfUnavailable stops a silent open run [tree 1a19f7fe81e3] (2026-10-15T23:20:29Z)
- (audit operator) `self: read _claude_cmd/_sandbox; opt-in flag, getattr default so other callers are unchanged; settings JSON passed as one argv element (no shell); live smoke run not done: the guard's plugin category refuses a direct claude --settings without the user's yes; keys per code.claude.com/docs/en/sandboxing.md` → a host without bubblewrap/socat gets failed sessions, which T-0955's no-progress block then stops retrying [tree 1a19f7fe81e3] (2026-10-15T23:20:29Z)
## Log
- 2026-10-15T22:08:01Z created
- 2026-10-15T23:18:27Z set tier=M, scope=['plugin/lib/fmserve.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_unattended.py', 'CHANGELOG.md', 'README.md']
- 2026-10-15T23:18:38Z focused
- 2026-10-15T23:20:31Z done
- 2026-10-15T23:20:33Z committed a8ac369 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- research T-0964-catalogue: Sources: research/T-0964-harness.md (claude-code-harness, feature by feature), research/T-0964-workflow.md (ECC,
- research mission-20261014-130857.pack: recursively improve: review what round 1 shipped today and brainstorm improvements on top of it — super improve foreman, integrate…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_serve.py
## Preflight
Changed in scope since this was planned (2026-10-15): CHANGELOG.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmserve.py; re-ground the plan against them before editing
## Lessons
- A sandbox for an agent has to leave writable exactly what its own tooling writes outside the checkout (state, the git common dir), or every commit and fm call fails inside it.
## Plan gaps
- failed first: step 1 failing RunModels test
## Files touched
- plugin/tests/test_unattended.py
- plugin/lib/fmserve.py
- plugin/lib/fmcli.py
- README.md
- CHANGELOG.md
