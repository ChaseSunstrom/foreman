---
id: T-0901
type: SECURITY
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-15T17:07:03Z
updated: 2026-10-15T17:26:04Z
base: b7843974d8863d1a4eed57df1d25814cb6431de9
base_tree: 1136e0b1eb3290e41868e12b549bdb04bc9c8771
verified: strong
---
# Commands fm stores and runs later bypass the guard: a verify command (--ac "x :: CMD", fm
## Raw request
> SECURITY!: Commands fm stores and runs later bypass the guard: a verify command (--ac "x :: CMD", fm task ac add/edit --verify CMD, intake DONE-WHEN ":: CMD"), fm check affected '<template>' and fm notify '<cmd>' are never checked, and fm task finish / fm check --affected / notify run them
> CONTEXT: found while fixing fm quiet (T-0898): fmguard.check('Bash', 'fm task new t --ac "ok :: rm -rf ~"') → None; only --run values and fm check add are read
> MUST: check each stored command where the hook sees it being stored, and again where fm runs a verify command (intake --file and hand-made briefs never pass the hook), with the task's own allows
> NEVER: block ordinary test commands
## Interpretation
Every command fm stores to run later gets the guard's checks twice: when the hook sees it stored (verify commands in --ac 'x :: CMD', --verify, a positional 'x :: CMD', intake DONE-WHEN lines; fm check affected's template; fm notify's command), and when fm is about to run it (fm task finish's verify runs, fm check --affected and the ambient runner, fm sentinel, notify), with the task's own grants, standing yes and trust. Ordinary test commands are untouched.
## Assumptions (confidence)
## Acceptance criteria
- [x] stored commands are refused when stored and when run; ordinary test commands still pass — verify with `python3 plugin/tests/run.py test_guard test_cli`
## Non-goals
## Approach (options → choice → why)
1) Both: write-time in the guard's fm branch (where --run and check add are already read) and run-time in fm before a stored command runs (chosen: write-time refuses where Claude can still fix it; run-time covers what never passes the hook: intake --file, a brief written earlier, an old task's verify that sentinel reruns). 2) Run-time only (the refusal lands at close, after the work). 3) Allow-list verify runners (breaks real projects' own commands). Complete version: every storing verb, every run site, the same grants as the hook (task allow, standing, trust), table tests for both sides.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: guard table rows for each storing verb; a run-time refusal at finish for a verify from intake --file
2. [x] write-time checks in fmguard's fm branch
3. [x] run-time guard_stored in fm before finish, affected, ambient, sentinel and notify run a stored command
4. [x] docs, review
## Resume here
<!-- auto -->
- 2026-10-15T17:15:53Z step 4/4: docs, review
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmambient.py, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/lib/fmserve.py, plugin/tests/test_cli.py, plugin/tests/test_guard.py
- touched since last checkpoint: plugin/tests/test_guard.py, plugin/tests/test_cli.py, plugin/lib/fmguard.py, plugin/lib/fmcli.py, plugin/lib/fmambient.py, plugin/lib/fmserve.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER stored commands; CHANGELOG security line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree a7133ae24589] (2026-10-15T17:11:01Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff` → exit 0 · Ran 101 tests in 4.4s (43 classes, 16 at a time; slowest: GuardAgainstBash 4s, Hook 2s, RuleIds 0s) / OK [ran] [tree a7133ae24589] (2026-10-15T17:11:06Z)
- (step 3) `python3 plugin/tests/run.py test_cli test_ambient test_serve test_guard test_snapshots test_lanes` → exit 0 · Ran 237 tests in 19.1s (75 classes, 16 at a time; slowest: TaskLifecycle 19s, Run 10s, StateViews 8s) / OK [ran] [tree 744b20a4a398] (2026-10-15T17:12:32Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_guard test_guard_diff test_ambient test_serve test_smoke test_stack test_snapshots test_docs` → exit 0 · Ran 263 tests in 24.0s (83 classes, 16 at a time; slowest: TaskLifecycle 24s, Run 11s, StateViews 7s) / OK [ran] [tree cc33a5d52d1b] (2026-10-15T17:22:30Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_guard test_guard_diff test_ambient test_serve test_smoke test_stack test_snapshots test_docs` → exit 0 · Ran 263 tests in 22.2s (83 classes, 16 at a time; slowest: TaskLifecycle 22s, Run 12s, StateViews 11s) / OK [ran] [tree cc33a5d52d1b] (2026-10-15T17:22:53Z)
- (step 3) `python3 plugin/tests/run.py test_cli test_guard test_guard_diff test_ambient test_serve test_smoke test_stack test_snapshots test_docs` → exit 0 · Ran 263 tests in 19.5s (83 classes, 16 at a time; slowest: TaskLifecycle 19s, Run 10s, StateViews 8s) / OK [ran] [tree cc33a5d52d1b] (2026-10-15T17:23:13Z)
- (step 4) `python3 plugin/tests/run.py test_cli test_guard test_guard_diff test_ambient test_serve test_smoke test_stack test_snapshots test_docs` → exit 0 · Ran 263 tests in 19.1s (83 classes, 16 at a time; slowest: TaskLifecycle 19s, Run 10s, StateViews 8s) / OK [ran] [tree cc33a5d52d1b] (2026-10-15T17:23:32Z)
- (ac 1) `python3 plugin/tests/run.py test_guard test_cli` → exit 0 · Ran 191 tests in 18.1s (67 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, GuardAgainstBash 6s) / OK [ran] [tree cc33a5d52d1b] (2026-10-15T17:26:03Z)
- (audit adversary) `one fm-reviewer pass (adversary, intent, edge): 3 HIGH, 3 MEDIUM, 3 LOW; 8 fixed, 1 rejected (the {{tests}} rows are str.format escapes, the command carries {tests}); full gates and fm replay (0 newly allowed of 3507)` → before this, fm task new --ac 'x :: rm -rf ~' then fm task finish ran rm -rf ~, and fm check add/smoke set cmd/notify did the same later; now every storing verb is read at the hook as argparse reads it (options can't hide the command), and every run site re-checks with the task's grants, so briefs from another clone or from before this fix are covered; a notify that runs $1 as code is refused [tree cc33a5d52d1b] (2026-10-15T17:26:03Z)
- (audit intent) `one fm-reviewer pass (adversary, intent, edge): 3 HIGH, 3 MEDIUM, 3 LOW; 8 fixed, 1 rejected (the {{tests}} rows are str.format escapes, the command carries {tests}); full gates and fm replay (0 newly allowed of 3507)` → stored commands are refused when stored and when run (table rows for 25 forms, run-time tests for finish and fm check); ordinary test commands, notify-send "$1" and a health-check curl stay allowed [tree cc33a5d52d1b] (2026-10-15T17:26:03Z)
- (audit edge) `one fm-reviewer pass (adversary, intent, edge): 3 HIGH, 3 MEDIUM, 3 LOW; 8 fixed, 1 rejected (the {{tests}} rows are str.format escapes, the command carries {tests}); full gates and fm replay (0 newly allowed of 3507)` → finish checks every command before running any, so a refusal leaves no side effects (asserted: no evidence written); sentinel guards all candidates before --max slices; the ambient runner logs a refusal instead of going silent [tree cc33a5d52d1b] (2026-10-15T17:26:03Z)
## Log
- 2026-10-15T17:07:03Z created
- 2026-10-15T17:08:14Z focused
- 2026-10-15T17:15:53Z paused: focus moved to T-0902
- 2026-10-15T17:18:54Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T17:18:54Z focused
- 2026-10-15T17:18:55Z review (adversary/intent/edge): accepted 1-8 — fm check/smoke gates unguarded at run, option words hide stored commands (check add/affected, notify, task --json ac), notify $1 replaced by a literal hides bash -c "$1", sentinel window past --max, other run sites (resume last green, packet --check, prove --vacuous/--same, --stack/--stack-check, record/whyred CMD), task set AC text and assume --check, finish runs earlier verifies before refusing a later one, ambient silent on refusal. Rejected 9: {{tests}} is str.format's escape in the table, the command does carry {tests}
- 2026-10-15T17:26:04Z done
- 2026-10-15T17:26:04Z committed c059744 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- T-0370 [FIX M, done, 2 steps] Guard: a $(…) substitution no longer turns off variable tracking, so a literal S=/tmp/… stays known — lesson: Before widening what the guar…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- decision 2026-09-26: Full autonomy never asks mid-run but still can't grant itself core or run destructive/irreversible guard categories: those are recorded with fm ask …
- similar finished tasks took 2–3 steps
## Lessons
- A guard that reads commands must also read every place a command is stored for later: write-time where the agent can still fix it, run-time for what never passed the hook
## Files touched
- plugin/tests/test_guard.py
- plugin/tests/test_cli.py
- plugin/lib/fmguard.py
- plugin/lib/fmcli.py
- plugin/lib/fmambient.py
- plugin/lib/fmserve.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmstack.py
- plugin/lib/fmsmoke.py
