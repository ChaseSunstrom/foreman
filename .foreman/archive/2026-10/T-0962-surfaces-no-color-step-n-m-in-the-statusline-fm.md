---
id: T-0962
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:51Z
updated: 2026-10-15T22:24:27Z
base: 264149dc8304b8b0c859fcfa1217b2f6fd39933a
base_tree: c138ae680255136899078c9fe35bf7cda1bec8bf
verified: strong
---
# Surfaces: NO_COLOR, step N/M in the statusline, fm ui --demo, fm page --picks, the sync join line, tmux and LSP notes
## Raw request
> Surfaces: NO_COLOR, step N/M in the statusline, fm ui --demo, fm page --picks, the sync join line, tmux and LSP notes
## Interpretation
Board clusters terminal-polish (NO_COLOR honoured by fm output — only fmdemo.py ~155 does today; statusline 'step N/M' from steps_done), ui-later #13 (fm ui --demo emits a canned view JSON), r2-board-ticking (fm page --picks - reads {id: add|veto}, refuses unknown ids, writes state picks.json, prints a summary; nothing reads picks today), r4-team-share (fm sync status prints the teammate join line), r4-editor-ui-surfaces (README: set -g status-right '#(fm state --line)') and lsp (intake's execute reference: when the LSP tool is available, check diagnostics after an edit).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm output carries no ANSI colour when NO_COLOR is set — verify with `python3 plugin/tests/run.py -k BoardSurfaces`
- [x] The statusline shows step N/M for the active task — verify with `python3 plugin/tests/run.py -k BoardSurfaces`
- [x] fm ui --demo prints a canned view that has every key a real fm ui --json view has — verify with `python3 plugin/tests/run.py -k BoardSurfaces`
- [x] fm page --picks - stores valid picks, refuses an unknown id, and prints a summary — verify with `python3 plugin/tests/run.py -k BoardSurfaces`
- [x] fm sync status prints the line a teammate runs to join — verify with `python3 plugin/tests/run.py -k BoardSurfaces`
- [x] README documents fm state --line for a tmux status bar, and the execute reference says to check LSP diagnostics after edits — verify with `python3 plugin/tests/run.py -k BoardSurfaces`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardSurfaces class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
## Docs impact
README, MASTER, CHANGELOG, plugin/skills/intake/references/execute.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardSurfaces` → ✗ exit 1 · Ran 6 tests in 1.4s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / FAILED (1 classes) [ran] [tree 98c15f14d2d0] (2026-10-15T22:15:48Z)
- (step 2) `python3 plugin/tests/run.py -k BoardSurfaces -k StatuslineUi -k Page -k Sync -k UiView` → exit 0 · Ran 50 tests in 9.2s (6 classes, 16 at a time; slowest: Sync 9s, UiView 8s, PageHardening 2s) / OK [ran] [tree e3459baf50c3] (2026-10-15T22:17:53Z)
- (step 3) `python3 plugin/tests/run.py -k BoardSurfaces.test_docs_name_the_tmux_line_and_lsp_diagnostics` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: BoardSurfaces 0s) / OK [ran] [tree e3459baf50c3] (2026-10-15T22:17:53Z)
- (step 2) `python3 plugin/tests/run.py test_board_surfaces test_statusline_ui test_statusline` → exit 0 · Ran 14 tests in 1.5s (3 classes, 16 at a time; slowest: BoardSurfaces 1s, StatuslineUi 1s, Checks 0s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:18Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardSurfaces` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardSurfaces` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardSurfaces` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (ac 4) `python3 plugin/tests/run.py -k BoardSurfaces` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (ac 5) `python3 plugin/tests/run.py -k BoardSurfaces` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (ac 6) `python3 plugin/tests/run.py -k BoardSurfaces` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (step 1) `python3 plugin/tests/run.py -k BoardSurfaces` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: BoardSurfaces 1s) / OK [ran] [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (audit intent) `one fm-reviewer pass (sonnet): 2 medium fixed test-first (step number off by one, fm state --line creating projects under tmux), 3 low: README NO_COLOR scope fixed, demo nested shapes and TS type noted` → NO_COLOR, current step N/M, ui --demo, page picks, sync join line, tmux and LSP notes [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (audit edge) `one fm-reviewer pass (sonnet): 2 medium fixed test-first (step number off by one, fm state --line creating projects under tmux), 3 low: README NO_COLOR scope fixed, demo nested shapes and TS type noted` → the step label shows the current step as fm next does; a status bar polling --line never creates a project [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
- (audit operator) `one fm-reviewer pass (sonnet): 2 medium fixed test-first (step number off by one, fm state --line creating projects under tmux), 3 low: README NO_COLOR scope fixed, demo nested shapes and TS type noted` → the tmux line follows the active pane [tree 1b820d60a75c] (2026-10-15T22:24:26Z)
## Log
- 2026-10-15T21:12:51Z created
- 2026-10-15T22:13:42Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0962.builder.md
- 2026-10-15T22:13:54Z focused
- 2026-10-15T22:19:10Z merged worktree-agent-a4e456424ad12d615 (10 file(s))
- 2026-10-15T22:19:11Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4e456424ad12d615
- 2026-10-15T22:22:46Z focused
- 2026-10-15T22:24:27Z done
- 2026-10-15T22:24:27Z committed a2ea60d (7 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- T-0960 [FEATURE M, active, 3 steps] New verbs: fm oops, fm round close, fm show, fm release-check, fm sensitive suggest, fm outcomes --readme
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- the similar finished task took 3 steps
## Lessons
- A number next to the word 'step' must match what fm next calls the step, or two surfaces disagree by one
## Plan gaps
- failed first: step 1 Failing tests in a BoardSurfaces class
## Files touched
- plugin/tests/test_board_surfaces.py
- plugin/hooks/statusline
- plugin/lib/fmsync.py
- plugin/lib/fmcli.py
- plugin/lib/fmpage.py
- plugin/lib/ui-demo.json
- plugin/lib/fmwatch.py
- README.md
- plugin/skills/intake/references/execute.md
- MASTER.md
- plugin/lib/fmcore.py
- plugin/tests/test_statusline_ui.py
- CHANGELOG.md
- plugin/lib/fmbudget.py
- plugin/lib/fmcost.py
- plugin/lib/fmlib.py
- plugin/lib/fmmap.py
- plugin/tests/test_cost_forecast.py
- plugin/tests/test_edit_cards.py
