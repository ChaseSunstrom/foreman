---
id: T-0780
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:59:46Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
group: structured reviewer findings output
base: 55e64ebdf3d1aff303f024184e23e456416813e3
base_tree: a430fb82bb64faf07e1dcf1a57b250d7044e5a52
verified: strong
---
# Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them
## Raw request
> FEATURE: Reviewer findings reach the host UI through ReportFindings
> CONTEXT: T-0760, cluster native-review (22 ideas). fm audit prep writes one fm-reviewer brief; findings come back as prose and go into fm task finish --lens. ReportFindings renders typed findings (file, line, summary, failure_scenario, severity order) and is called when review instructions say so.
> DONE-WHEN: fm audit prep's brief asks the reviewer for findings in ReportFindings' fields, and its closing note tells the main thread to report verified findings with ReportFindings before recording lenses; test pins the brief text.
## Interpretation
fm audit prep's reviewer brief (_REVIEW_OUT, fmcli.py:3028) asks for ranked prose findings; they land only in the task's lenses. Claude Code's ReportFindings tool renders typed findings (file, line, summary, short_summary, failure_scenario, category, most severe first) in the host UI when review instructions say to use it. The brief asks for those fields per finding, and prep's closing line tells the main thread to report the verified ones with ReportFindings (an empty list when none survive) before recording the lenses.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm audit prep's brief names file, line, short_summary and failure_scenario per finding and its instructions name ReportFindings; past-finding parsing still reads the ranked lines — verify with `cd plugin/tests && python3 -m unittest test_cli.AuditPrep`
## Non-goals
## Approach (options → choice → why)
Options: a new reviewer output format (breaks _FINDING parsing of past findings); extra fields in the existing ranked format plus one instruction; skip (prose only). Chose extra fields: the HIGH/MEDIUM/LOW lines still parse.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing CLI test
2. [x] _REVIEW_OUT fields and the ReportFindings instruction
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && ! python3 -m unittest test_cli.AuditPrep` → ✗ exit 1 · FAILED (failures=1) / fm: the output reports failing tests but the command exited 0 (a pipe such as | tail hides the exit), so it counts as a failure [ran] [tree 9a698c14f258] (2026-10-14T16:41:20Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_cli.AuditPrep test_verifying test_audit` → ✗ exit 1 · Ran 18 tests in 8.207s / FAILED (failures=1) [ran] [tree e53e48f70088] (2026-10-14T16:41:47Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_cli.AuditPrep test_verifying test_audit` → exit 0 · Ran 18 tests in 4.953s / OK [ran] [tree 471584832f4e] (2026-10-14T16:41:58Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                63.6   102.6     150  [0] / SessionEnd                  54.7    93.5     150  [0]; python3 plugin/tests/run.py → ✗ exit 1 · Ran 1277 tests in 198.2s (431 classes, 16 at a time; slowest: Stop 120s, TaskLifecycle 75s, Bench 74s) / FAILED (2 classes) [ran] [tree 471584832f4e] (2026-10-14T16:47:43Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification               135.8   244.8     150  [0]  OVER BUDGET / SessionEnd                 119.2   220.0     150  [0]  OVER BUDGET; python3 plugin/tests/run.py → ✗ exit 1 · Ran 1277 tests in 249.0s (431 classes, 16 at a time; slowest: Stop 209s, Recall 120s, Bench 112s) / FAILED (1 classes) [ran] [tree 471584832f4e] (2026-10-14T16:51:38Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.AuditPrep` → exit 0 · Ran 8 tests in 7.662s / OK [ran] [tree c233fc34bffa] (2026-10-14T16:56:54Z)
- `cd plugin/tests && python3 -m unittest test_cli.AuditPrep.test_brief_asks_for_report_findings_fields_and_prep_names_the_tool` → ✗ exit 1 · Ran 1 test in 1.133s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree c233fc34bffa] (2026-10-14T16:56:57Z)
- `cd plugin/tests && python3 -m unittest test_cli.AuditPrep.test_brief_asks_for_report_findings_fields_and_prep_names_the_tool` → exit 0 · Ran 1 test in 1.076s / OK [ran] [tree c233fc34bffa] (2026-10-14T16:56:57Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_cli.AuditPrep.test_brief_asks_for_report_findings_fields_and_prep_names_the_tool` → exit 0 · Ran 1 test in 1.462s / OK [ran] [tree c233fc34bffa] (2026-10-14T16:59:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_cli.AuditPrep test_verifying test_audit` → exit 0 · Ran 18 tests in 12.288s / OK [ran] [tree c233fc34bffa] (2026-10-14T16:59:36Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_cli.AuditPrep` → exit 0 · Ran 8 tests in 8.256s / OK [ran] [tree c233fc34bffa] (2026-10-14T16:59:45Z)
- (audit edge) `self: merged diff read; the ranked HIGH/MEDIUM/LOW line stays first per finding so _FINDING still parses past findings (the builder's test checks it), ReportFindings' fields follow it, and prep's closing line names the tool when there is a reviewer brief; the output-length cap of a prep test moved 700 → 800 for the new line` → a self-only audit (no reviewer sections) gets no ReportFindings line; the main thread decides which findings survived verification before reporting [tree c233fc34bffa] (2026-10-14T16:59:45Z)
- (audit self) `self: merged diff read; the ranked HIGH/MEDIUM/LOW line stays first per finding so _FINDING still parses past findings (the builder's test checks it), ReportFindings' fields follow it, and prep's closing line names the tool when there is a reviewer brief; the output-length cap of a prep test moved 700 → 800 for the new line` → no findings [tree c233fc34bffa] (2026-10-14T16:59:45Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:07:31Z planned from capture
- 2026-10-14T16:40:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0780.builder.md
- 2026-10-14T16:40:32Z focused
- 2026-10-14T16:56:44Z merged worktree-agent-a9ce1fa93e332a5e8 (2 file(s))
- 2026-10-14T16:56:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9ce1fa93e332a5e8
- 2026-10-14T16:56:45Z focused
- 2026-10-14T16:59:15Z scope: other files in the scope check are T-0784/T-0805's, committed by them
- 2026-10-14T16:59:46Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- decision 2026-10-04: Inbox build order: review family (T-0230, T-0232, T-0233, T-0235) and research family (T-0229, T-0237, T-0238, T-0239) are each built as one batch, …
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-14): plugin/lib/fmcli.py, plugin/tests/test_cli.py; re-ground the plan against them before editing
## Lessons
- extend a parsed output format by appending fields under the parsed line, never by changing the line
## Plan gaps
- failed first: step 1 Failing CLI test
- failed first: step 2 _REVIEW_OUT fields and the ReportFindings instruction
## Files touched
- .claude/worktrees/agent-a9ce1fa93e332a5e8/plugin/tests/test_cli.py
- .claude/worktrees/agent-a9ce1fa93e332a5e8/plugin/lib/fmcli.py
- MASTER.md
- plugin/hooks/hooks.json
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/tests/bench_hooks.py
- plugin/tests/test_bench_hooks.py
- plugin/tests/test_cli.py
- plugin/tests/test_docs.py
- plugin/tests/test_hooks.py
