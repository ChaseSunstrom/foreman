---
id: T-0785
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T16:42:00Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
base: ac8480359a4b41ebf39457a944ad189d7521a6c0
base_tree: 1b9fa94e43dd2d984f28008b7b7b9b433422ca7d
verified: strong
---
# fm doctor names the Foreman features the installed Claude Code is too old for
## Raw request
> FEATURE: fm doctor checks the Claude Code version against the features Foreman relies on
> CONTEXT: T-0760, cluster native-adoption. Foreman now relies on agent omitClaudeMd/effort/maxTurns (2.1.271), monitors (2.1.105), hook if (2.1.85), sessionTitle, updatedToolOutput (2.1.121). fmhooks._cc_version() caches claude --version daily.
> DONE-WHEN: fm doctor reports WARN naming each feature whose minimum version the installed Claude Code is below, PASS otherwise; test with a stubbed version.
## Interpretation
Foreman now leans on Claude Code features with minimum versions: hook onFailure (2.1.295), agent omitClaudeMd (2.1.271), agent effort/maxTurns (2.1.78), hook if (2.1.85), plugin monitors (2.1.105), updatedToolOutput (2.1.121), sessionTitle on UserPromptSubmit (2.1.94). On an older Claude Code each silently does nothing. A doctor check reads claude --version (fmhooks._cc_version, cached a day) and, for each feature the plugin's files actually use (a file glob and a pattern per row), WARNs naming the feature, its minimum and the upgrade; PASS otherwise.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a stubbed 2.1.100, doctor WARNs naming omitClaudeMd and onFailure; with 2.1.299 it passes; a feature no plugin file uses is never named — verify with `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features`
## Non-goals
## Approach (options → choice → why)
Options: a hard minimum version (blocks users on any older build); a static list (drifts as features come and go); a table of (feature, min, files, pattern) checked only when the pattern is present. Chose the probed table.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing doctor test
2. [x] check_cc_features; MASTER.md row
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features` → ✗ exit 1 · Ran 1 test in 0.001s / FAILED (errors=1) [ran] [tree 6963f796ad76] (2026-10-14T16:18:35Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features` → exit 0 · Ran 1 test in 0.004s / OK [ran] [tree 77d1713c1a1b] (2026-10-14T16:18:55Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_doctor test_docs` → exit 0 · Ran 43 tests in 18.188s / OK [ran] [tree 77d1713c1a1b] (2026-10-14T16:19:16Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                35.7    43.3     150  [0] / SessionEnd                  32.2    44.5     150  [0] [ran] [tree 77d1713c1a1b] (2026-10-14T16:23:15Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                61.5   113.7     150  [0] / SessionEnd                  59.3   147.2     150  [0] [ran] [tree 77d1713c1a1b] (2026-10-14T16:34:27Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · Notification                65.5    99.2     150  [0] / SessionEnd                  66.1   134.2     150  [0] [ran] [tree 77d1713c1a1b] (2026-10-14T16:37:10Z)
- `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) (start tree + this task's tests) [ran] [tree 86a8461f8dd6] (2026-10-14T16:40:03Z)
- `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features` → exit 0 · Ran 1 test in 0.002s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:40:03Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features` → exit 0 · Ran 1 test in 0.002s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:40:03Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_doctor test_docs` → exit 0 · Ran 44 tests in 4.981s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:40:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features` → exit 0 · Ran 1 test in 0.002s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:40:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_claude_code_features` → exit 0 · Ran 1 test in 0.002s / OK [ran] [tree 86a8461f8dd6] (2026-10-14T16:41:59Z)
- (audit edge) `self: merged diff read and fixed (the baseRef row probed a file that never holds it); the table is probed per row so unused features are never named; an unknown version passes; real tree at 2.1.100 names onFailure, omitClaudeMd and baseRef, at 2.1.299 passes` → a feature row whose glob matches nothing (monitors today) is skipped; doctor imports fmhooks only for the cached version read [tree 86a8461f8dd6] (2026-10-14T16:41:59Z)
- (audit self) `self: merged diff read and fixed (the baseRef row probed a file that never holds it); the table is probed per row so unused features are never named; an unknown version passes; real tree at 2.1.100 names onFailure, omitClaudeMd and baseRef, at 2.1.299 passes` → no findings [tree 86a8461f8dd6] (2026-10-14T16:41:59Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:10:43Z planned from capture
- 2026-10-14T16:12:40Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0785.builder.md
- 2026-10-14T16:12:50Z focused
- 2026-10-14T16:13:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a080be4f78fe46bd5
- 2026-10-14T16:18:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0785.builder.md
- 2026-10-14T16:18:21Z focused
- 2026-10-14T16:39:49Z merged worktree-agent-a8ce7d9e010c37ec0 (3 file(s))
- 2026-10-14T16:39:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8ce7d9e010c37ec0
- 2026-10-14T16:39:55Z focused
- 2026-10-14T16:40:09Z main thread: the baseRef row probed plugin/settings.json, which never holds it (T-0803 wires it into ~/.claude); now probes lib/fmsetup.py. Real tree: 2.1.100 names onFailure, omitClaudeMd, baseRef; 2.1.299 passes
- 2026-10-14T16:41:59Z scope: the builder's merge carried MASTER.md (doctor paragraph sentence); other files in the scope check are T-0776/T-0781's, committed by them
- 2026-10-14T16:42:00Z done
- 2026-10-14T16:42:00Z committed e4d735e (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research claude-code-features-20261014: Foreman uses: 14 hook events, 4 async hooks, 6 agents (tools/model/color only), output style, statusline.
- T-0768 [PERFORMANCE S, done, 2 steps] Subagents: effort, maxTurns and omitClaudeMd in Foreman's agent frontmatter, validated by fm doctor
- T-0673 [FEATURE M, done, 7 steps] Milestone: Features — Multi-machine, multi-project and ecosystem — lesson: a capture into another project must not run that project's e…
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 2–7 steps
- likely tests for the scope: plugin/tests/test_doctor.py
## Lessons
- a probe for a setting must look where Foreman writes it, not where a plugin could ship it
## Plan gaps
- failed first: step 1 Failing doctor test
## Files touched
- .claude/worktrees/agent-a8ce7d9e010c37ec0/plugin/tests/test_doctor.py
- .claude/worktrees/agent-a8ce7d9e010c37ec0/plugin/lib/fmdoctor.py
- .claude/worktrees/agent-a8ce7d9e010c37ec0/MASTER.md
- plugin/lib/fmdoctor.py
- MASTER.md
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmlanes.py
- plugin/lib/fmresearch.py
- plugin/lib/fmsetup.py
- plugin/tests/test_doctor.py
- plugin/tests/test_hooks.py
- plugin/tests/test_ideas.py
- plugin/tests/test_lanes.py
- plugin/tests/test_setup.py
