---
id: T-3623
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T05:35:31Z
updated: 2026-11-07T05:35:31Z
---
# T-3593 follow-up: the costliest test classes record the whole tree ('*'), so any change…
## Raw request
> T-3593 follow-up: the costliest test classes record the whole tree ('*'), so any change reruns them. In the bench on 109 modules, 92 of ~420 recorded classes were '*' and they carried ~1470 of ~2160 class-seconds: test_ship.Ship 95s, test_bench_family.Ablation/Judged 57/56s, test_bench.Bench 57s, test_lanes.Lanes 51s, test_hooks.SessionStart 47s, test_hooks.PreToolUse 46s, test_hooks.NoTaskGateKinds 38s, test_board_verbs.BoardVerbs 36s, test_close_gates.CloseGates 30s, test_rename_scan.RenameScan 30s, test_mint.* 27-28s, test_cli.TaskLifecycle/AuditPrep 27s. Causes found: Sampo starting plugin/bin/fm by its #!/usr/bin/env python3 line (an unhooked system python), gates running 'python3 ...' from bash -c, hook tests going through a claude stand-in. Lane commit 59636b5f1 fixes those three (the coverage venv leads PATH, #! and wrappers are followed): SessionStart, TaskLifecycle, CloseGates, Lanes and Bench now record no '*'. To do: rerun the bench chain off-peak to measure what stays '*' (likely bwrap/docker sandbox tests, git run on the repo itself, non-Python children working in the repo) and follow those with care
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-07T05:35:31Z created
## Follow-ups captured
