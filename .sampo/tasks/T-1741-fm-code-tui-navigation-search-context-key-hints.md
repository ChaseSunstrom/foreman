---
id: T-1741
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcodeterm.py, plugin/tests/test_code_tui.py, plugin/commands/code.md, CHANGELOG.md]
depends_on: [T-1740]
source: followup
created: 2026-10-23T04:16:19Z
updated: 2026-10-23T05:47:32Z
batch: [T-1313, T-1346]
base: 5854397927067e3a9eb11154b53df469a57279d1
base_tree: 856dbad3a2a3bf2544fa3aa132a0e6a8d71eedd6
plan0_at: 2026-10-23T05:41:41Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcodeterm.py, plugin/tests/test_code_tui.py, plugin/commands/code.md, CHANGELOG.md]
verified: strong
---
# fm code TUI: navigation (/ search, context key hints, Tab focus ring) and a real request line editor (history, Ctrl key…
## Raw request
> T-1313: fm code tui navigation: / searches the Activity log, a context hint line names the keys that apply to the focused panel, and Tab cycles a visible focus ring across panels (C15)
> T-1346: fm code request box (U4): a real line editor (arrows, history, Ctrl-A/E/W/U, bracketed paste keeps newlines), / opens a palette of the app's commands, @ completes tracked files, a one-line preview says where the request goes and which runner takes it
## Interpretation
Do T-1313, T-1346 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1741. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1313: / filters the Activity log to lines matching what's typed (the panel title counts them; Esc clears), and the bottom bar's hints name the focused panel's keys (Tab's focus ring already existed) — verify with `python3 plugin/tests/run.py test_code_tui.Navigation`
- [x] T-1346: the request box edits like a line editor (arrows, Home/End, Ctrl-A/E/W/U/K, Up/Down history), a request starting with / names and runs an app command, Tab after @ completes a tracked file, and a preview line says where the request goes and which runner takes it — verify with `python3 plugin/tests/run.py test_code_tui.LineEditor`
## Non-goals
## Approach (options → choice → why)
Ground first: fmcodetui already has an Editors class of tests and a Paste class; extend what exists rather than adding a second editor. The line editor is a pure state machine (text, cursor, history) fed key names from fmcodeterm.parse_keys, tested without curses. Search is a filter over the Activity rows already rendered. The focus ring reuses the panel borders' colour tokens. @ completion reads git ls-files once per open (bounded). Keep Golden, HostileWidth and Fuzz green.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1313: Fm code tui navigation: / searches the Activity log, a context hint line names the keys th
2. [x] T-1346: Fm code request box (U4): a real line editor (arrows, history, Ctrl-A/E/W/U, bracketed pas
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- `python3 plugin/tests/run.py test_code_tui.Navigation test_code_tui.LineEditor` → ✗ exit 1 · Ran 7 tests in 0.9s (2 classes, 16 at a time; slowest: Navigation 0s, LineEditor 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 64cbc0bd8586] (2026-10-23T05:46:28Z)
- `python3 plugin/tests/run.py test_code_tui.Navigation test_code_tui.LineEditor` → exit 0 · Ran 7 tests in 0.3s (2 classes, 16 at a time; slowest: LineEditor 0s, Navigation 0s) / OK [ran] [tree 64cbc0bd8586] (2026-10-23T05:46:28Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.Navigation` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: Navigation 0s) / OK [ran] [tree 64cbc0bd8586] (2026-10-23T05:46:29Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui.LineEditor` → exit 0 · Ran 5 tests in 0.3s (1 classes, 16 at a time; slowest: LineEditor 0s) / OK [ran] [tree 64cbc0bd8586] (2026-10-23T05:46:29Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_settings_power` → exit 0 · Ran 222 tests in 8.3s (30 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Rules 4s) / OK [ran] [tree 64cbc0bd8586] (2026-10-23T05:46:38Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_settings_power` → exit 0 · Ran 222 tests in 8.2s (30 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Rules 4s) / OK [ran] [tree 64cbc0bd8586] (2026-10-23T05:46:47Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.Navigation` → exit 0 · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Navigation 0s) / OK [ran] [tree 5bc7acba90d0] (2026-10-23T05:47:02Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui.LineEditor` → exit 0 · Ran 5 tests in 0.3s (1 classes, 16 at a time; slowest: LineEditor 0s) / OK [ran] [tree 5bc7acba90d0] (2026-10-23T05:47:02Z)
- (audit intent) `self: LineEditor is pure (tested key by key, history back to the draft); the prompt draws a cursor at the editor's place and a preview line; /name runs the first matching command (or says none matches), never a run; @ completion reads git ls-files once with a 2 s timeout and a 20,000 cap; / filters Activity by the text a line shows (case-insensitive), the title counts matches, Esc clears; the focus ring already existed, and the focused panel now names its keys; golden snapshots differ only by that hint line; 222 TUI and settings tests pass` → typing a request feels like a shell line; app commands and files are reachable from the box; the Activity log can be narrowed [tree 5bc7acba90d0] (2026-10-23T05:47:02Z)
- (audit edge) `self: LineEditor is pure (tested key by key, history back to the draft); the prompt draws a cursor at the editor's place and a preview line; /name runs the first matching command (or says none matches), never a run; @ completion reads git ls-files once with a 2 s timeout and a 20,000 cap; / filters Activity by the text a line shows (case-insensitive), the title counts matches, Esc clears; the focus ring already existed, and the focused panel now names its keys; golden snapshots differ only by that hint line; 222 TUI and settings tests pass` → a paste lands at the cursor and is capped as before; Up with no history does nothing; a search with no match shows an empty panel titled '0 matching …'; at narrow widths the panel hint is left out [tree 5bc7acba90d0] (2026-10-23T05:47:02Z)
- (audit design) `self: LineEditor is pure (tested key by key, history back to the draft); the prompt draws a cursor at the editor's place and a preview line; /name runs the first matching command (or says none matches), never a run; @ completion reads git ls-files once with a 2 s timeout and a 20,000 cap; / filters Activity by the text a line shows (case-insensitive), the title counts matches, Esc clears; the focus ring already existed, and the focused panel now names its keys; golden snapshots differ only by that hint line; 222 TUI and settings tests pass` → the preview and hints are dim and sit where the eye already is (under the box, in the panel's edge), not in the crowded status bar [tree 5bc7acba90d0] (2026-10-23T05:47:02Z)
- (audit adversary) `self: LineEditor is pure (tested key by key, history back to the draft); the prompt draws a cursor at the editor's place and a preview line; /name runs the first matching command (or says none matches), never a run; @ completion reads git ls-files once with a 2 s timeout and a 20,000 cap; / filters Activity by the text a line shows (case-insensitive), the title counts matches, Esc clears; the focus ring already existed, and the focused panel now names its keys; golden snapshots differ only by that hint line; 222 TUI and settings tests pass` → file names from git ls-files are only shown and inserted as text; nothing runs them [tree 5bc7acba90d0] (2026-10-23T05:47:02Z)
## Log
- 2026-10-23T04:16:19Z created
- 2026-10-23T04:16:28Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_code_tui.Navigation`
- 2026-10-23T04:16:28Z criterion 1 text: T-1313: Fm code tui navigation: / searches the Activity log, a context hint line names the keys th works → T-1313: / searches the Activity log (matches highlighted, n/N step), a hint line names the keys for the focused panel, and Tab cycles a visible focus ring across panels
- 2026-10-23T04:16:28Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_code_tui.LineEditor`
- 2026-10-23T04:16:28Z criterion 2 text: T-1346: Fm code request box (U4): a real line editor (arrows, history, Ctrl-A/E/W/U, bracketed pas works → T-1346: the request box is a line editor (arrows, history, Ctrl-A/E/W/U, bracketed paste keeps newlines), / opens a command palette, @ completes tracked files, and a one-line preview says where the request goes and which runner takes it
- 2026-10-23T04:16:29Z set depends_on=['T-1740']
- 2026-10-23T04:16:30Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcodeterm.py', 'plugin/tests/test_code_tui.py', 'plugin/commands/code.md', 'CHANGELOG.md']
- 2026-10-23T05:41:32Z grounding: the request box is _prompt_key (fmcodetui.py ~1796): Enter starts, Esc backs out, Backspace deletes the last character, printable characters append; no cursor, history, Ctrl keys or palette. Paste lands whole via key() (T-1316). Panel focus exists (self.order/self.focus, Tab → next_focus at ~1869) but there's no visible ring or per-panel hint line, and no Activity search. Plan: a pure LineEditor (text, cursor, history list; keys Left/Right/Home/End/Ctrl-A/E/W/U/K, Up/Down history) used by _prompt_key and drawn with a cursor cell; '/' at an empty prompt opens a palette of COMMAND_LABELS; '@' completes from git ls-files (once per prompt open, capped); a preview line under the box names the runner (opts model/worker or the default). Navigation: '/' in main mode opens an Activity filter (n/N step), the focused panel's border uses the accent style, a hint line names that panel's keys.
- 2026-10-23T05:41:40Z focused
- 2026-10-23T05:42:30Z criterion 1 text: T-1313: / searches the Activity log (matches highlighted, n/N step), a hint line names the keys for the focused panel, and Tab cycles a visible focus ring across panels → T-1313: / filters the Activity log to lines matching what's typed (the panel title counts them; Esc clears), and the bottom bar's hints name the focused panel's keys (Tab's focus ring already existed)
- 2026-10-23T05:42:31Z criterion 2 text: T-1346: the request box is a line editor (arrows, history, Ctrl-A/E/W/U, bracketed paste keeps newlines), / opens a command palette, @ completes tracked files, and a one-line preview says where the request goes and which runner takes it → T-1346: the request box edits like a line editor (arrows, Home/End, Ctrl-A/E/W/U/K, Up/Down history), a request starting with / names and runs an app command, Tab after @ completes a tracked file, and a preview line says where the request goes and which runner takes it
- 2026-10-23T05:44:49Z hypothesis: the editor and key logic pass (LineEditor's 4 key/history/app tests are green); the 4 failures are all rendering — the prompt has no preview line, search has no filter, title note or typing line, and no panel draws its bottom-edge hint — so the next edits are in render, _panel and _log only
- 2026-10-23T05:47:01Z scope: plugin/tests/fixtures/golden/demo-*.txt (regenerated: only the focused Activity panel's bottom edge gained its hint), MASTER.md; built in a scratch worktree while the gates ran on main, copied after checking main's copies were unchanged since its base
- 2026-10-23T05:47:31Z done
- 2026-10-23T05:47:32Z committed b3d4ab4a (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1742 [FEATURE M, planned, 3 steps] fm code TUI: theme gallery, a diff view with line-by-line reveal and intra-line highlights, a third column at 160+ colu…
- T-1740 [FEATURE M, done, 3 steps] fm code TUI: waiting cues (title, bell, why-waiting line), press-twice quit and key help, a half-block canvas for the c… — lesson: Conf…
- research T-1511-review: Verdict: changes needed.** The runner test is sound. Key capture can lock the user out of list navigation, and two other findings are real but na…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- Put a panel's own key hints in its edge, not in a shared bar whose width other text already needs
## Files touched
- plugin/lib/fmcodetui.py
- plugin/tests/fixtures/golden/demo-00.0s.txt
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/tests/fixtures/golden/demo-09.1s.txt
- plugin/tests/fixtures/golden/demo-30.0s.txt
- plugin/tests/test_code_tui.py
- MASTER.md
- CHANGELOG.md
