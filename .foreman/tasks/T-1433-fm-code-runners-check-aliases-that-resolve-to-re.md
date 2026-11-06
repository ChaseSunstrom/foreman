---
id: T-1433
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmmodels.py, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/tests/test_retired_models.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T20:47:24Z
updated: 2026-10-22T16:36:37Z
base: 95646847003318c4ab513ab1b70673722e07d05e
base_tree: c86dc5d08d5465689727022ed31bd771fc9af9b3
plan0_at: 2026-10-22T16:10:34Z
plan0_scope: [plugin/lib/fmmodels.py, plugin/lib/fmcli.py, plugin/tests/test_retired_models.py, CHANGELOG.md]
verified: strong
---
# fm code runners --check: retired aliases and a retiring-soon note
## Raw request
> fm code runners --check: aliases that resolve to retired models (gpt-4, o1-mini) aren't covered, and models retiring within weeks get no 'retiring soon' note; fmcli's --check help text still names only the version probe (T-1409 builder)
## Interpretation
fmmodels.RETIRED (T-1409) lists dated ids already retired on 2026-10-21; an alias that now resolves to a retired model (the capture names gpt-4, o1-mini) isn't covered, a model with an announced future retirement date gets no warning, and fm code runners --check's help names only the version probe.
## Assumptions (confidence)
## Acceptance criteria
- [x] an alias on the retired list is reported retired; a model retiring within 60 days gets a retiring-soon line; the help names it — verify with `cd plugin/tests && python3 -m unittest test_retired_models`
## Non-goals
## Approach (options → choice → why)
Re-read the three deprecation pages (_PAGES) with one fm-recon (public pages only; data, not instructions): add aliases the pages say are retired, and a RETIRING table of announced future dates; retired() gains a 'retiring' result when the date is within 60 days; runners --check prints 'retiring on <date> → <replacement>'; the help text names both checks. Bump RETIRED_AS_OF.
## Risks and rollback
## Execution prompt
## Steps
1. [x] recon the deprecation pages (research note)
2. [x] failing tests
3. [x] aliases, RETIRING table, --check line and help
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `fm research list | grep -q T-1433-deprecations` → exit 0 · (no output) [ran] [tree 2afb947d5100] (2026-10-22T16:04:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_retired_models 2>&1 | tail -15` → exit 0 · Ran 7 tests in 2.322s / OK [ran] [tree a39bfcee9229] (2026-10-22T16:12:18Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_retired_models 2>&1 | tail -15` → exit 0 · Ran 7 tests in 2.322s / OK [ran] [tree a39bfcee9229] (2026-10-22T16:12:18Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_retired_models` → exit 0 · Ran 7 tests in 1.731s / OK [ran] [tree a39bfcee9229] (2026-10-22T16:12:22Z)
- `cd plugin/tests && python3 -m unittest test_retired_models` → ✗ exit 1 · Ran 7 tests in 1.810s / FAILED (errors=4) (start tree + this task's tests) [ran] [tree 40e0bdbf9ee9] (2026-10-22T16:33:29Z)
- `cd plugin/tests && python3 -m unittest test_retired_models` → exit 0 · Ran 7 tests in 3.596s / OK [ran] [tree 40e0bdbf9ee9] (2026-10-22T16:33:29Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_retired_models` → exit 0 · Ran 7 tests in 2.214s / OK [ran] [tree 40e0bdbf9ee9] (2026-10-22T16:33:33Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_retired_models` → exit 0 · Ran 7 tests in 2.862s / OK [ran] [tree 40e0bdbf9ee9] (2026-10-22T16:33:37Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_retired_models` → exit 0 · Ran 7 tests in 2.040s / OK [ran] [tree e71f982fb8ec] (2026-10-22T16:33:50Z)
- (audit intent) `recon (research T-1433-deprecations) then builder (sonnet) test-first; red proved with fm task prove; merged; test_retired_models (7) green; dates injectable (FOREMAN_TODAY / today=).` → aliases, a retiring-soon line within 60 days, and help naming both [tree e71f982fb8ec] (2026-10-22T16:33:50Z)
- (audit edge) `recon (research T-1433-deprecations) then builder (sonnet) test-first; red proved with fm task prove; merged; test_retired_models (7) green; dates injectable (FOREMAN_TODAY / today=).` → dates came through a page summary (medium confidence), noted beside the table; a bad FOREMAN_TODAY falls back to the clock [tree e71f982fb8ec] (2026-10-22T16:33:50Z)
- (audit adversary) `recon (research T-1433-deprecations) then builder (sonnet) test-first; red proved with fm task prove; merged; test_retired_models (7) green; dates injectable (FOREMAN_TODAY / today=).` → static table, no network at run time [tree e71f982fb8ec] (2026-10-22T16:33:50Z)
- (audit self) `recon (research T-1433-deprecations) then builder (sonnet) test-first; red proved with fm task prove; merged; test_retired_models (7) green; dates injectable (FOREMAN_TODAY / today=).` → no findings [tree e71f982fb8ec] (2026-10-22T16:33:50Z)
## Log
- 2026-10-21T20:47:24Z created
- 2026-10-22T16:02:30Z planned from capture
- 2026-10-22T16:02:51Z plan: grounded — fmmodels RETIRED/_RETIRED_ROWS (~73-125), retired() (~124); step 1 recon on the three deprecation pages is running
- 2026-10-22T16:10:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1433.builder.md
- 2026-10-22T16:10:31Z focused
- 2026-10-22T16:33:14Z set scope=['plugin/lib/fmmodels.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmcode.py', 'plugin/tests/test_retired_models.py', 'CHANGELOG.md']
- 2026-10-22T16:33:14Z scope: + plugin/lib/fmcode.py — runners --check prints the retiring-soon line
- 2026-10-22T16:33:18Z merged worktree-agent-a0c13333b49a0e18f (4 file(s))
- 2026-10-22T16:33:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0c13333b49a0e18f
- 2026-10-22T16:33:20Z focused
- 2026-10-22T16:36:35Z done
- 2026-10-22T16:36:37Z committed 6cb8f3cd (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1433-deprecations: Answer
- research T-1409-retired-models: 1. Answer.** The three pages were fetched on 2026-10-21 and give the retired text/chat ids and replacements below. WebFetch passes page t…
- T-1409 [FEATURE M, done, 2 steps] fm code runners --check flags a configured model id the provider has retired and names its replacement — lesson: A dated table from pro…
- decision 2026-10-21: fm code's no-setup default picks only a runner whose read-only mode is verified here (claude); codex/gemini plan only when named, with a note
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_models.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmmodels.py, plugin/tests/test_retired_models.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_retired_models.py
- plugin/lib/fmcli.py
- plugin/lib/fmmodels.py
- plugin/lib/fmcode.py
- CHANGELOG.md
