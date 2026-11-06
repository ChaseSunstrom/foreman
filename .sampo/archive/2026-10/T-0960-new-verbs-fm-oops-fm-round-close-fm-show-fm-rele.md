---
id: T-0960
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:48Z
updated: 2026-10-15T22:26:06Z
base: 9c6fd4d278adb11066609a51697fa304d2a25167
base_tree: 02021111a248789f8af1210e9763e52ea83d8d16
verified: strong
---
# New verbs: fm oops, fm round close, fm show, fm release-check, fm sensitive suggest, fm outcomes --readme
## Raw request
> New verbs: fm oops, fm round close, fm show, fm release-check, fm sensitive suggest, fm outcomes --readme
## Interpretation
Board clusters r4-data-safety (fm oops: show the newest work snapshot's restore command, restore it only with --apply; fmcore ~263, fm snapshots ~3032), r2-round-loop-automation (fm round close: tag HEAD round-N, list tasks closed since the previous round tag), r2-cli-ergonomics (fm show X: a T-id to task show, a path to why, else recall), r4-newcomer-gates (fm release-check: fm doctor and fm demo in a temp HOME, exit 0 on a clean checkout), r2-sensitive-and-redaction (fm sensitive suggest: print signals — .env*, *.pem, secret|prod in the path — and set nothing) and r4-published-metrics (fm outcomes --readme: 'N of M closed tasks held; K ungraded').
## Assumptions (confidence)
## Acceptance criteria
- [x] fm oops names the newest work snapshot and its restore command, and restores it only with --apply — verify with `python3 plugin/tests/run.py -k BoardVerbs`
- [x] fm round close tags HEAD round-N and lists the tasks closed since the previous round tag — verify with `python3 plugin/tests/run.py -k BoardVerbs`
- [x] fm show T-0001 prints what fm task show prints; fm show PATH:LINE routes to why; other words route to recall — verify with `python3 plugin/tests/run.py -k BoardVerbs`
- [x] fm release-check runs fm doctor and fm demo in a temporary HOME and exits 0 on a clean checkout — verify with `python3 plugin/tests/run.py -k BoardVerbs`
- [x] fm sensitive suggest prints each signal it found and changes no setting — verify with `python3 plugin/tests/run.py -k BoardVerbs`
- [x] fm outcomes --readme prints one sentence with held, total and ungraded counts — verify with `python3 plugin/tests/run.py -k BoardVerbs`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardVerbs class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
## Docs impact
README, MASTER, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardVerbs` → ✗ exit 1 · Ran 6 tests in 1.9s (1 classes, 16 at a time; slowest: BoardVerbs 2s) / FAILED (1 classes) [ran] [tree bccf9b8eb3ee] (2026-10-15T22:08:27Z)
- (step 2) `python3 plugin/tests/run.py -k BoardVerbs -k test_help -k test_snapshots -k test_outcomes -k test_doctor -k test_demo -k test_docsdrift -k test_cli` → exit 0 · Ran 177 tests in 27.0s (57 classes, 16 at a time; slowest: Command 26s, TaskLifecycle 22s, ViewsRepair 18s) / OK [ran] [tree b01b84b9db7a] (2026-10-15T22:13:39Z)
- (step 3) `python3 plugin/bin/fm release-check` → exit 0 · PASS  fm demo / fm release-check: OK (a temporary HOME, deleted) [ran] [tree b01b84b9db7a] (2026-10-15T22:13:49Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardVerbs` → exit 0 · Ran 6 tests in 11.1s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardVerbs` → exit 0 · Ran 6 tests in 11.1s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardVerbs` → exit 0 · Ran 6 tests in 11.1s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (ac 4) `python3 plugin/tests/run.py -k BoardVerbs` → exit 0 · Ran 6 tests in 11.1s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (ac 5) `python3 plugin/tests/run.py -k BoardVerbs` → exit 0 · Ran 6 tests in 11.1s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (ac 6) `python3 plugin/tests/run.py -k BoardVerbs` → exit 0 · Ran 6 tests in 11.1s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (step 1) `python3 plugin/tests/run.py -k BoardVerbs` → exit 0 · Ran 6 tests in 11.1s (1 classes, 16 at a time; slowest: BoardVerbs 11s) / OK [ran] [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (audit intent) `one fm-reviewer pass (sonnet): 3 medium, 3 low; all fixed (the fm show case got its test after the fix)` → six small verbs that answer common asks in one word [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (audit adversary) `one fm-reviewer pass (sonnet): 3 medium, 3 low; all fixed (the fm show case got its test after the fix)` → oops restores only inside its repo through fmcore's runner and fails closed if the current files can't be saved; sensitive suggest prints sanitised names [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (audit edge) `one fm-reviewer pass (sonnet): 3 medium, 3 low; all fixed (the fm show case got its test after the fix)` → archived tasks count, folders route to recall, a failed git log tags nothing [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
- (audit operator) `one fm-reviewer pass (sonnet): 3 medium, 3 low; all fixed (the fm show case got its test after the fix)` → release-check runs in a throwaway HOME and leaves nothing [tree d28e0744aaa8] (2026-10-15T22:26:05Z)
## Log
- 2026-10-15T21:12:48Z created
- 2026-10-15T22:05:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0960.builder.md
- 2026-10-15T22:05:49Z focused
- 2026-10-15T22:18:57Z merged worktree-agent-a3c1a041c68cad47c (6 file(s))
- 2026-10-15T22:18:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3c1a041c68cad47c
- 2026-10-15T22:24:35Z focused
- 2026-10-15T22:26:06Z done
- 2026-10-15T22:26:06Z committed 67ff8bf (3 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar finished tasks took 2–5 steps
## Lessons
- A restore verb's message must say what it overwrites, not what it spares
## Plan gaps
- failed first: step 1 Failing tests in a BoardVerbs class
## Files touched
- plugin/tests/test_board_verbs.py
- plugin/lib/fmcli.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmdemo.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/hooks/statusline
- plugin/lib/fmbudget.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmlib.py
- plugin/lib/fmmap.py
- plugin/lib/fmpage.py
- plugin/lib/fmsync.py
- plugin/lib/fmwatch.py
- plugin/lib/ui-demo.json
- plugin/skills/intake/references/execute.md
- plugin/tests/test_board_surfaces.py
- plugin/tests/test_cost_forecast.py
- plugin/tests/test_edit_cards.py
- plugin/tests/test_statusline_ui.py
