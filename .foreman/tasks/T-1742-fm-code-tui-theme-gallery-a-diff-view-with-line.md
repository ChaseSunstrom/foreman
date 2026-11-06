---
id: T-1742
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcode.py, plugin/lib/fmcli.py, plugin/tests/test_code_tui.py, plugin/commands/code.md, CHANGELOG.md]
depends_on: [T-1741]
source: followup
created: 2026-10-23T04:16:34Z
updated: 2026-10-23T05:53:39Z
batch: [T-1311, T-1312, T-1347]
base: b3d4ab4a66286e1e15f44654b5d26d0018257845
base_tree: 5bc7acba90d02b107f987f31fc409e4bcbdd0155
plan0_at: 2026-10-23T05:47:48Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcode.py, plugin/lib/fmcli.py, plugin/tests/test_code_tui.py, plugin/commands/code.md, CHANGELOG.md]
verified: strong
---
# fm code TUI: theme gallery, a diff view with line-by-line reveal and intra-line highlights, a third column at 160+ colu…
## Raw request
> T-1311: fm code tui theme gallery: --themes shows every preset side by side on the demo run, and tui.toml is reloaded live when it changes (C9)
> T-1312: fm code tui diff view: hunks reveal line by line on open, with intra-line highlights of the changed words (C17)
> T-1347: fm code run view layout (U6): at 160+ columns a third column shows the Plan and Check-output panels; diff, history and picker open as a right-hand drawer sliding in over the run; the header shows home › project › task
## Interpretation
Do T-1311, T-1312, T-1347 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1742. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1311: fm code --themes prints every theme side by side on a sample run, in colour on a colour terminal (the settings screen's preview before keeping a look already existed, T-1573) — verify with `python3 plugin/tests/run.py test_code_tui.Themes`
- [x] T-1312: the diff view reveals hunks line by line on open (instant under reduced motion) with intra-line highlights of the changed words — verify with `python3 plugin/tests/run.py test_code_tui.DiffView`
- [x] T-1347: at 160+ columns a third column shows the Plan and Check output panels; narrower terminals keep today's layout — verify with `python3 plugin/tests/run.py test_code_tui.WideLayout`
## Non-goals
## Approach (options → choice → why)
Ground first: themes, the diff panel and the Columns layout code exist in some form (tests: Columns, Views, MotionVisuals); extend them. Intra-line highlights from difflib.SequenceMatcher on word tokens, bounded per line. The reveal is a frame-driven animation honouring the motion setting. The gallery renders each preset through the same draw path on a fixed demo run (no network, no runner). Keep Golden, HostileWidth, Width and Fuzz green.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1311: Fm code tui theme gallery: --themes shows every preset side by side on the demo run, and t
2. [x] T-1312: Fm code tui diff view: hunks reveal line by line on open, with intra-line highlights of th
3. [x] T-1347: Fm code run view layout (U6): at 160+ columns a third column shows the Plan and Check-outp
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui.Themes test_code_tui.DiffView test_code_tui.WideLayout` → red as expected (exit 1) · Ran 4 tests in 0.3s (3 classes, 16 at a time; slowest: DiffView 0s, Themes 0s, WideLayout 0s) / FAILED (3 classes) [ran] [tree e005fe3e234f] (2026-10-23T05:49:10Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui.DiffView test_code_tui.WideLayout 2>&1 | grep -E "Error|FAIL:|^OK" | head -6` → exit 0 · OK [ran] [tree 1d9ee491292d] (2026-10-23T05:49:50Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui test_help test_settings_power 2>&1 | grep -E "^(FAIL|ERROR):|^OK|FAILED \(" | head -5` → exit 0 · OK [ran] [tree 9103a9de5656] (2026-10-23T05:51:21Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.Themes` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Themes 0s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:51:30Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui.DiffView` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: DiffView 0s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:51:31Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui.WideLayout` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: WideLayout 0s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:51:31Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_help` → exit 0 · Ran 201 tests in 8.1s (34 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:51:40Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_help` → exit 0 · Ran 201 tests in 8.1s (34 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:51:48Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui test_help` → exit 0 · Ran 201 tests in 8.1s (34 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:51:57Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.Themes` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Themes 0s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:52:06Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui.DiffView` → exit 0 · Ran 2 tests in 0.3s (1 classes, 16 at a time; slowest: DiffView 0s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:52:06Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui.WideLayout` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: WideLayout 0s) / OK [ran] [tree 01979935ede2] (2026-10-23T05:52:06Z)
- (audit intent) `self: the third column only appears from 160 columns when the layout doesn't already show plan or verify, so a user's own layout is never doubled; intraline pairs a removed run with the added run right after it, word tokens through SequenceMatcher (autojunk off), lines over 400 characters not compared, tabbed lines left unmarked so marks can't land in the wrong columns; the reveal reads FX.moving, so reduced and off show everything at once; the gallery renders each preset with motion off on a built-in sample run, tiles 60+ wide, plain under depth 0; all TUI tests pass with the goldens unchanged` → themes are comparable at a glance; a diff reads at the word level; wide screens use their room [tree 01979935ede2] (2026-10-23T05:52:06Z)
- (audit design) `self: the third column only appears from 160 columns when the layout doesn't already show plan or verify, so a user's own layout is never doubled; intraline pairs a removed run with the added run right after it, word tokens through SequenceMatcher (autojunk off), lines over 400 characters not compared, tabbed lines left unmarked so marks can't land in the wrong columns; the reveal reads FX.moving, so reduced and off show everything at once; the gallery renders each preset with motion off on a built-in sample run, tiles 60+ wide, plain under depth 0; all TUI tests pass with the goldens unchanged` → changed words use the ok and bad chips the Checks panel already uses, so the meaning matches; the gallery names each tile above it [tree 01979935ede2] (2026-10-23T05:52:06Z)
- (audit edge) `self: the third column only appears from 160 columns when the layout doesn't already show plan or verify, so a user's own layout is never doubled; intraline pairs a removed run with the added run right after it, word tokens through SequenceMatcher (autojunk off), lines over 400 characters not compared, tabbed lines left unmarked so marks can't land in the wrong columns; the reveal reads FX.moving, so reduced and off show everything at once; the gallery renders each preset with motion off on a built-in sample run, tiles 60+ wide, plain under depth 0; all TUI tests pass with the goldens unchanged` → 0 matches pair nothing; a long diff reveals 40 lines a second then stays; a 159-column terminal keeps today's layout [tree 01979935ede2] (2026-10-23T05:52:06Z)
## Log
- 2026-10-23T04:16:34Z created
- 2026-10-23T04:16:43Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_code_tui.Themes`
- 2026-10-23T04:16:43Z criterion 1 text: T-1311: Fm code tui theme gallery: --themes shows every preset side by side on the demo run, and t works → T-1311: fm code --themes shows every preset side by side on the demo run, and the settings screen previews a theme before it is kept
- 2026-10-23T04:16:44Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_code_tui.DiffView`
- 2026-10-23T04:16:44Z criterion 2 text: T-1312: Fm code tui diff view: hunks reveal line by line on open, with intra-line highlights of th works → T-1312: the diff view reveals hunks line by line on open (instant under reduced motion) with intra-line highlights of the changed words
- 2026-10-23T04:16:44Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_code_tui.Columns`
- 2026-10-23T04:16:44Z criterion 3 text: T-1347: Fm code run view layout (U6): at 160+ columns a third column shows the Plan and Check-outp works → T-1347: at 160+ columns a third column shows the Plan and Check output; narrower terminals keep today's layout
- 2026-10-23T04:16:45Z set depends_on=['T-1741']
- 2026-10-23T04:16:46Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcode.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code_tui.py', 'plugin/commands/code.md', 'CHANGELOG.md']
- 2026-10-23T05:47:47Z focused
- 2026-10-23T05:48:57Z criterion 1 text: T-1311: fm code --themes shows every preset side by side on the demo run, and the settings screen previews a theme before it is kept → T-1311: fm code --themes prints every theme side by side on a sample run, in colour on a colour terminal (the settings screen's preview before keeping a look already existed, T-1573)
- 2026-10-23T05:48:57Z criterion 3 verify: `python3 plugin/tests/run.py test_code_tui.Columns` → `python3 plugin/tests/run.py test_code_tui.WideLayout`
- 2026-10-23T05:48:57Z criterion 3 text: T-1347: at 160+ columns a third column shows the Plan and Check output; narrower terminals keep today's layout → T-1347: at 160+ columns a third column shows the Plan and Check output panels; narrower terminals keep today's layout
- 2026-10-23T05:51:57Z scope: plugin/lib/fmcode.py (the --themes branch), plugin/lib/fmcli.py (the flag), MASTER.md, CHANGELOG.md
- 2026-10-23T05:53:38Z done
- 2026-10-23T05:53:39Z committed 8d63c36d (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1741 [FEATURE M, done, 2 steps] fm code TUI: navigation (/ search, context key hints, Tab focus ring) and a real request line editor (history, Ctrl key… — lesson: Put …
- T-1740 [FEATURE M, done, 3 steps] fm code TUI: waiting cues (title, bell, why-waiting line), press-twice quit and key help, a half-block canvas for the c… — lesson: Conf…
- T-1738 [FIX S, done, 2 steps] Layout collisions: site header at 320 px, graph poster labels in dense clusters — lesson: Layout claims need a measurement in a real browse…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- Give a gallery tiles wide enough that each variant shows what tells it apart
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- CHANGELOG.md
- MASTER.md
