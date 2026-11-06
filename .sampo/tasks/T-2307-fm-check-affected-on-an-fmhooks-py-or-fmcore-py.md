---
id: T-2307
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T09:39:24Z
updated: 2026-10-31T09:46:56Z
builder_model: sonnet
base: 322b5ec96a206cef597498e959cd9766c9a7d775
base_tree: aa5c9c730cfbde0a44f1013469d4d4e891eb13fb
plan0_at: 2026-10-31T09:41:06Z
plan0_scope: []
verified: strong
---
# fm check --affected pulls test_core's import-budget tests into any change to a hook-path module
## Raw request
> fm check --affected on an fmhooks.py (or fmcore.py) change runs test_hooks but not test_core's LaterImports import-budget tests, so a new top-level import in a hook module passes the lane and fails only at ship (ship71, T-2305): map hook-path modules to those tests in the affected set
## Interpretation
A new top-level import in fmhooks.py passed the lane's affected run and failed only at ship (ship71, T-2305): the affected set for fmhooks.py and fmcore.py doesn't include test_core.LaterImports.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm check --affected on a change to plugin/lib/fmhooks.py (or fmcore.py) lists test_core among the tests it runs — verify with `python3 plugin/tests/run.py test_affected_hubs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test that the affected set for fmhooks.py holds test_core; then add the mapping where the affected set is built
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / OK [ran] [tree 66e2b646481c] (2026-10-31T09:41:29Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_board_verbs test_cli test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.25s] [ran] [tree 66e2b646481c] (2026-10-31T09:42:06Z)
- (step 1) `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 3 tests in 1.6s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / OK [ran] [tree 8f1c7f9ba80b] (2026-10-31T09:45:14Z)
- `python3 plugin/tests/run.py test_affected_hubs` → ✗ exit 1 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6874dd6be412] (2026-10-31T09:45:24Z)
- `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 3 tests in 1.6s (1 classes, 16 at a time; slowest: AffectedHubs 1s) / OK [ran] [tree 6874dd6be412] (2026-10-31T09:45:24Z)
- (ac 1) `python3 plugin/tests/run.py test_affected_hubs` → exit 0 · Ran 3 tests in 2.7s (1 classes, 16 at a time; slowest: AffectedHubs 2s) / OK [ran] [tree 37c357a22ed8] (2026-10-31T09:45:36Z)
- (audit intent) `self-review of the merged diff: HOOK_BUDGET names fmhooks.py and fmcore.py and test_core.py; affected() adds test_core only when one of them changed and the file exists in the project; the test checks fmhooks, fmcore and an unrelated lib file; restored the two-space comment the merge narrowed` → a new top-level import in a hook module fails in the lane's affected run, not at ship [tree 37c357a22ed8] (2026-10-31T09:45:36Z)
- (audit edge) `self-review of the merged diff: HOOK_BUDGET names fmhooks.py and fmcore.py and test_core.py; affected() adds test_core only when one of them changed and the file exists in the project; the test checks fmhooks, fmcore and an unrelated lib file; restored the two-space comment the merge narrowed` → other projects have no such files, so the rule adds nothing there; fmguard.py, also a hook module, isn't listed yet [tree 37c357a22ed8] (2026-10-31T09:45:36Z)
- (audit self) `self-review of the merged diff: HOOK_BUDGET names fmhooks.py and fmcore.py and test_core.py; affected() adds test_core only when one of them changed and the file exists in the project; the test checks fmhooks, fmcore and an unrelated lib file; restored the two-space comment the merge narrowed` → no findings [tree 37c357a22ed8] (2026-10-31T09:45:36Z)
## Log
- 2026-10-31T09:39:24Z created
- 2026-10-31T09:40:48Z planned from capture
- 2026-10-31T09:40:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2307.builder.md
- 2026-10-31T09:41:06Z focused
- 2026-10-31T09:45:10Z merged worktree-agent-abcfd38372beee5a4 (2 file(s))
- 2026-10-31T09:45:10Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abcfd38372beee5a4
- 2026-10-31T09:45:11Z focused
- 2026-10-31T09:45:12Z criterion 1 verify: `python3 plugin/tests/run.py test_check` → `python3 plugin/tests/run.py test_affected_hubs`
- 2026-10-31T09:45:31Z scope: plugin/lib/fmcli.py (HOOK_BUDGET in affected()), plugin/tests/test_affected_hubs.py, CHANGELOG.md
- 2026-10-31T09:46:29Z done
- 2026-10-31T09:46:33Z committed 283da20f (2 files)
- 2026-10-31T09:46:56Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2305 [FIX S, done, 1 steps] Hooks import no glob: T-2297's leads-record prune lists the folder without a top-level import — lesson: A new top-level import in fmhooks c…
- T-2020 [PERFORMANCE M, done, 2 steps] Hooks compile regexes on first use: importing fmcore, fmguard and fmhooks compiles none of their 191 module-level patterns — lesson…
- T-2267 [FEATURE S, done, 1 steps] fm task finish for a lane-merged task runs the always-on budget checks (test_doctor… — lesson: A folder link heuristic tuned on one rep…
- decision 2026-10-30: [revisited: feel free to push to main] [cites: user steer 2026-10-29: push to main without asking] [check: python3 plugin/tests/run.py test_ship.Shi…
## Why not caught
nothing linked the import-budget test to hook modules in the map, so the affected set skipped it
## Lessons
- A test that guards a property (an import budget) rather than a file's behaviour has no map link to the files it guards: name those links by hand
## Files touched
- plugin/tests/test_affected_hubs.py
- plugin/lib/fmcli.py
- CHANGELOG.md
