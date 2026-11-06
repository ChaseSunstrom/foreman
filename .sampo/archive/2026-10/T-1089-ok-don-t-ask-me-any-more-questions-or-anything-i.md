---
id: T-1089
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmedit.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmhooks.py, plugin/tests/test_batch_edit.py, plugin/tests/test_lanes.py, README.md, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T04:17:03Z
updated: 2026-10-16T05:06:24Z
base: 63256db4e60fd017e97791bf2a53c64348663463
base_tree: 7f65dd62cc9584a96bfeacc4894106579a00b64c
verified: strong
---
# Ok, don't ask me any more questions or ANYTHING, I will be AFK, do everything, etc. also m
## Raw request
> ok, don't ask me any more questions or ANYTHING, I will be AFK, do everything, etc. also make more tools and stuff to batch edit files/whatever/everything, etc. and more ideas you can come up with etc. more efficient and save on tokens, etc. and faster, etc.
## Interpretation
The user wants Foreman to get through work faster and cheaper on its own: tools that change many files in one call instead of one Edit per spot (each Edit also needs a Read first), more builders working in parallel, and cheaper ways to read and change code, so the same work costs fewer tokens and less wall time.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm edit applies a batch of replacements across files atomically (refusing a non-unique or missing old text, and files outside the task's scope), fm sub previews and applies a regex codemod, and fm lane max raises the builder cap — verify with `python3 plugin/tests/run.py test_batch_edit test_lanes`
## Non-goals
## Approach (options → choice → why)
A complete version: (1) fm edit: a batch of exact replacements across files from one spec on stdin (a file, the old text, the new text per entry; JSON or a simple block format), all-or-nothing, each old text unique in its file unless --all, a one-line diff stat per file, --dry-run, refusing files outside the active task's scope; (2) fm sub PATTERN REPL --glob G: a regex codemod with a per-file count preview, --apply to write, --max to cap; (3) fm lane max N: the builder cap (2) becomes a project setting up to 6, so an AFK run works more lanes at once; (4) the edit card and hints point Claude at fm edit for 3+ spots and fm sym/outline for reading. Options for the batch editor: (a) fm commands run through Bash (Claude Code's bash edit diff already records touched files for the task); (b) an MCP tool in Foreman's server (the edit gate and scope checks never see MCP writes); (c) documenting heredoc scripts (nothing enforced). Choice (a).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: fm edit batch (unique, all-or-nothing, dry-run stat, scope refusal), fm sub preview/apply/max, fm lane max N and the cap
2. [x] fmedit module (edit, sub) and the lane cap setting
3. [x] Hints: the edit card and the 3rd Edit on one file point at fm edit; README, MASTER, CHANGELOG, fm help
## Resume here
T-1089: tests green, docs written, awaiting fm-reviewer (a2f8ee1fb41540861)
<!-- auto -->
- 2026-10-16T04:59:53Z step 1/3: Failing tests: fm edit batch (unique, all-or-nothing, dry-run stat, scope refusal), fm sub preview/apply/max, fm lane max N and the cap
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmlanes.py, plugin/lib/fmedit.py, plugin/tests/test_batch_edit.py
- touched since last checkpoint: plugin/lib/fmedit.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/tests/test_batch_edit.py, plugin/lib/fmhooks.py, CHANGELOG.md, MASTER.md, README.md
## Docs impact
README 'Changes many spots in one call'; MASTER fmedit entry; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_batch_edit` → ✗ exit 1 · Ran 10 tests in 3.5s (3 classes, 16 at a time; slowest: BatchEdit 3s, Sub 1s, LaneMax 0s) / FAILED (3 classes) [ran] [tree 83ed2b988682] (2026-10-16T04:50:24Z)
- (step 2) `python3 plugin/tests/run.py test_batch_edit.BatchEdit test_batch_edit.Sub test_batch_edit.LaneMax test_lanes` → exit 0 · Ran 31 tests in 12.8s (7 classes, 16 at a time; slowest: Lanes 13s, BatchEdit 8s, Sub 2s) / OK [ran] [tree 80c07a6812ca] (2026-10-16T04:56:51Z)
- (step 3) `python3 plugin/tests/run.py test_batch_edit test_speed test_help test_docs` → exit 0 · Ran 58 tests in 17.4s (18 classes, 16 at a time; slowest: BatchEdit 17s, Speed 10s, Sub 5s) / OK [ran] [tree 4c27ddbdf9cf] (2026-10-16T04:58:01Z)
- (ac 1) `python3 plugin/tests/run.py test_batch_edit test_lanes` → exit 0 · Ran 40 tests in 9.5s (8 classes, 16 at a time; slowest: BatchEdit 9s, Lanes 9s, Sub 3s) / OK [ran] [tree c1679e25ac4f] (2026-10-16T05:06:04Z)
- (step 1) `python3 plugin/tests/run.py test_batch_edit test_lanes test_speed test_help test_docs` → exit 0 · Ran 85 tests in 10.3s (22 classes, 16 at a time; slowest: BatchEdit 10s, Lanes 9s, Speed 4s) / OK [ran] [tree c1679e25ac4f] (2026-10-16T05:06:04Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as its own SECURITY task` → many spots change in one call, all or none; a regex codemod previews then applies; the builder cap is a setting; the third edit in a row points at it [tree c1679e25ac4f] (2026-10-16T05:06:04Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as its own SECURITY task` → every target goes through the guard as an Edit would (same Ctx: allow, standing, trust), plus the user's path rules; realpath before checks; inside-project only; no new trust [tree c1679e25ac4f] (2026-10-16T05:06:04Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as its own SECURITY task` → CRLF kept, non-UTF-8 counted not hidden, a concurrent change aborts the write, a failed stage leaves every file as it was, malformed blocks refused [tree c1679e25ac4f] (2026-10-16T05:06:04Z)
- (audit operator) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as its own SECURITY task` → fm help lists edit and sub; the builder contract names fm edit --file; README, MASTER, CHANGELOG [tree c1679e25ac4f] (2026-10-16T05:06:04Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as its own SECURITY task` → one fmedit module (parse, check, write) shared by edit and sub [tree c1679e25ac4f] (2026-10-16T05:06:04Z)
- `python3 plugin/tests/run.py test_batch_edit test_lanes test_speed test_help test_docs` → exit 0 · Ran 85 tests in 8.5s (22 classes, 16 at a time; slowest: BatchEdit 8s, Lanes 8s, Speed 3s) / OK [ran] [tree c1679e25ac4f] (2026-10-16T05:06:22Z)
- (audit intent) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as T-1107` → many spots change in one call, all or none; a regex codemod previews then applies; the builder cap is a setting; the third edit in a row points at it [tree c1679e25ac4f] (2026-10-16T05:06:22Z)
- (audit adversary) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as T-1107` → every target goes through the guard as an Edit would (same Ctx: allow, standing, trust), plus the user's path rules; realpath before checks; inside-project only; no new trust [tree c1679e25ac4f] (2026-10-16T05:06:22Z)
- (audit edge) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as T-1107` → CRLF kept, non-UTF-8 counted not hidden, a concurrent change aborts the write, a failed stage leaves every file as it was, malformed blocks refused [tree c1679e25ac4f] (2026-10-16T05:06:22Z)
- (audit operator) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as T-1107` → fm help lists edit and sub; the builder contract names fm edit --file; README, MASTER, CHANGELOG [tree c1679e25ac4f] (2026-10-16T05:06:22Z)
- (audit maintainer) `fm-reviewer five-lens pass (research T-1089-review): 9 findings fixed test-first (atomic multi-file write, CRLF, malformed blocks, glob scopes, the user's path rules, stale reads, fm sub reach/silence/crash, lane max digits, builders can batch via --file); the .git/config guard gap captured as T-1107` → one fmedit module (parse, check, write) shared by edit and sub [tree c1679e25ac4f] (2026-10-16T05:06:22Z)
## Log
- 2026-10-16T04:17:03Z created
- 2026-10-16T04:36:11Z set tier=M, scope=['plugin/lib/fmedit.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmlanes.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_batch_edit.py', 'plugin/tests/test_lanes.py', 'README.md', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-16T04:50:09Z focused
- 2026-10-16T04:50:24Z paused: focus moved to T-1090
- 2026-10-16T04:55:13Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T04:55:13Z focused
- 2026-10-16T04:59:54Z paused: focus moved to T-1054
- 2026-10-16T05:02:46Z focused
- 2026-10-16T05:06:13Z scope: the mod files, fmcore/fmledger, ui-demo.json, test_core and test_ledger_chain are other tasks' committed work (T-1090, T-1065, T-1097) done while this task was paused; none was edited for T-1089
- 2026-10-16T05:06:23Z done
- 2026-10-16T05:06:24Z committed a097503 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- research mission-20261014-103352: Request: super improve foreman, integrate better with new CC features, super improve, smarter, faster, better, more capable, etc. etc. …
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py, plugin/tests/test_lanes.py
## Lessons
- A tool that writes on Claude's behalf from Bash must run the same checks the Edit path runs (guard Ctx, scope globs, the user's rules): reuse them, never re-derive
## Plan gaps
- failed first: step 1 Failing tests: fm edit batch (unique, all-or-nothing, dry-run stat, scope refusal), fm sub preview/…
## Files touched
- plugin/tests/test_batch_edit.py
- plugin/lib/fmedit.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
- README.md
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/lib/fmcore.py
- plugin/lib/fmledger.py
- plugin/lib/ui-demo.json
- plugin/tests/test_core.py
- plugin/tests/test_ledger_chain.py
