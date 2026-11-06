---
id: T-0077
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_quiet.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-09-27T06:30:08Z
updated: 2026-10-03T08:00:20Z
base: 60a4d37af95d23cff87573440f7b0914653a1f12
base_tree: e12e4fdfb9c9e5ef2ae27aea7bdd8b0934c38a79
verified: strong
---
# FOREMAN_QUIET=1: a session another tool drives gets no Foreman context, nudges or brief requirement; the guard still runs
## Raw request
> no env var marks a claude session as driven by an external orchestrator (to quiet Foreman hooks); jarvis-code has to disable the plugin with --settings — evidence: foreman-internals research
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] With FOREMAN_QUIET=1, SessionStart, UserPromptSubmit and Stop print nothing and an edit without a task is allowed; the guard still blocks a home delete — verify with `python3 plugin/tests/run.py -k test_quiet`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests
2. [x] Quiet check in the hook dispatcher and the no-task gate
3. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (a 'Driven by another tool' line) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_quiet` → exit 0 · Ran 3 tests in 0.3s (2 classes, 16 at a time; slowest: Quiet 0s, Speed 0s) / OK [ran] [tree a387e849175a] (2026-10-03T08:00:19Z)
- (step 2) `python3 plugin/tests/run.py -k test_quiet` → exit 0 · Ran 3 tests in 0.3s (2 classes, 16 at a time; slowest: Quiet 0s, Speed 0s) / OK [ran] [tree a387e849175a] (2026-10-03T08:00:19Z)
- (step 3) `grep -q FOREMAN_QUIET MASTER.md && grep -q T-0077 CHANGELOG.md` → exit 0 · (no output) [ran] [tree a387e849175a] (2026-10-03T08:00:19Z)
- (ac 1) `python3 plugin/tests/run.py -k test_quiet` → exit 0 · Ran 3 tests in 0.4s (2 classes, 16 at a time; slowest: Quiet 0s, Speed 0s) / OK [ran] [tree a387e849175a] (2026-10-03T08:00:20Z)
- (ac 2) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 08:00 UTC); cached (fm check --fresh reruns) [ran] [tree a387e849175a] (2026-10-03T08:00:20Z)
- (audit adversary) `self: the quiet check sits before every non-guard handler and after the guard decision in PreToolUse, so only the brief requirement and notes are skipped; tests cover three events, the edit gate both ways and a guard block under quiet` → the variable is set by whoever launches claude; a model can't set it for its own hooks (hooks inherit Claude Code's environment, not a Bash call's), and quiet never skips the guard, asks or grants [tree a387e849175a] (2026-10-03T08:00:20Z)
- (audit self) `self: the quiet check sits before every non-guard handler and after the guard decision in PreToolUse, so only the brief requirement and notes are skipped; tests cover three events, the edit gate both ways and a guard block under quiet` → no findings [tree a387e849175a] (2026-10-03T08:00:20Z)
## Log
- 2026-09-27T06:30:08Z created
- 2026-10-03T07:59:10Z planned from capture
- 2026-10-03T07:59:10Z focused
- 2026-10-03T08:00:20Z done
- 2026-10-03T08:00:20Z committed b4f4bcc (4 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- research t0036-operator: The implementation matches its documented contract and is well tested. Findings below are minor.
- T-0076 [FEATURE M, done, 4 steps] fm ui --json: one view-model snapshot for every surface (incl. steps, criteria, depends)
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-09-27): CHANGELOG.md, MASTER.md, plugin/lib/fmhooks.py; re-ground the plan against them before editing
## Lessons
- Quieting a plugin for automation is one environment check at the dispatcher, placed after whatever must never be skipped.
## Files touched
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_quiet.py
