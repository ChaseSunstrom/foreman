---
id: T-1537
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmtaste.py, plugin/lib/fmcli.py, plugin/tests/test_taste_ledger.py, CHANGELOG.md, plugin/commands/looks.md, plugin/skills/directions/SKILL.md, MASTER.md, plugin/lib/fmcodetui.py]
depends_on: []
source: followup
created: 2026-10-22T17:43:47Z
updated: 2026-10-22T21:24:32Z
base: d7e4d4751234a56ac4c7398755bdcdd0ea3094aa
base_tree: 16f971bf4af6af73000b7d69de94d326e0c85cf8
plan0_at: 2026-10-22T20:38:02Z
plan0_scope: [plugin/lib/fmtaste.py, plugin/lib/fmcli.py, plugin/tests/test_taste_ledger.py, CHANGELOG.md]
verified: strong
---
# Round 3 (T-1520): Taste ledger: learn from what the user keeps and from 'not like that', a
## Raw request
> Round 3 (T-1520): Taste ledger: learn from what the user keeps and from 'not like that', a 12-pair calibration picker, rank looks by what was kept, roll looks while idle, bisect taste across history, a style séance, and on-box learning from pages, photos or files the user explicitly chooses (a128 c155 a144 a177 c037 b003 c115 b005 b029 b082 c024). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Taste ledger: learn from what the user keeps and from 'not like that', a 12-pair calibration picker, rank looks by what was kept, roll looks while idle, bisect taste across history, a style séance, and on-box learning from pages, photos or files the user explicitly chooses (a128 c155 a144 a177 c037 b003 c115 b005 b029 b082 c024). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [x] a kept and a reverted look update the ledger; the calibration picker records 12 answers; nothing reads a file the user didn't name — verify with `cd plugin/tests && python3 -m unittest test_taste_ledger`
## Non-goals
Captured as follow-ups, not built here: rolling looks while idle; bisecting taste across history; the style séance; a foreman-ui pane surface for the ledger; detecting kept and reverted looks on their own from DESIGN.md or git history (kept and reverted are recorded only when the model runs fm looks keep/revert).
## Approach (options → choice → why)
Options: learn silently (privacy risk); chosen: a taste ledger in Foreman's state from explicit signals (kept, reverted, 'not like that'), a 12-pair calibration picker, ranking looks by kept, rolling looks while idle, bisecting taste over history; learning from pages, photos or files only those the user names, on-box, never uploaded.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] ledger and signals
3. [x] calibration and ranking
4. [x] opt-in sources
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_taste_ledger` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.2s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree c371574ad5b4] (2026-10-22T20:42:09Z)
- (step 2) `python3 plugin/tests/run.py -k test_taste_ledger.Ledger` → exit 0 · Ran 3 tests in 1.2s (1 classes, 16 at a time; slowest: Ledger 1s) / OK [ran] [tree 6dd4303074a9] (2026-10-22T20:47:01Z)
- (step 4) `python3 plugin/tests/run.py -k test_taste_ledger.Sources` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Sources 0s) / OK [ran] [tree 6dd4303074a9] (2026-10-22T20:47:01Z)
- (step 3) `python3 plugin/tests/run.py test_taste_ledger` → exit 0 · Ran 11 tests in 2.3s (5 classes, 16 at a time; slowest: Ledger 2s, Calibration 2s, Sources 0s) / OK [ran] [tree 56a8d33a6416] (2026-10-22T21:01:51Z)
- (step 1) `python3 plugin/tests/run.py test_taste_ledger` → ✗ exit 1 · Ran 13 tests in 1.8s (5 classes, 16 at a time; slowest: Ledger 2s, Calibration 1s, Sources 0s) / FAILED (5 classes) [ran] [tree f2c8209572b7] (2026-10-22T21:10:31Z)
- (step 3) `python3 plugin/tests/run.py test_taste_ledger` → exit 0 · Ran 13 tests in 2.4s (5 classes, 16 at a time; slowest: Ledger 2s, Calibration 2s, Sources 1s) / OK [ran] [tree 861d8c65dc9e] (2026-10-22T21:14:01Z)
- (step 1) `python3 plugin/tests/run.py test_taste_ledger test_doctor test_code_tui` → exit 0 · Ran 235 tests in 7.3s (46 classes, 16 at a time; slowest: Command 7s, Fuzz 6s, Events 3s) / OK [ran] [tree 51fd4b8c8fa1] (2026-10-22T21:23:06Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_taste_ledger` → exit 0 · Ran 13 tests in 1.735s / OK [ran] [tree 51fd4b8c8fa1] (2026-10-22T21:23:08Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1537-review.md)` → escape sequences drained in the picker; symlinks refused (O_NOFOLLOW, last component); --why single-quoted with quotes refused; named files only, 8 MiB / 50 cap; 40 MP bomb refused before decode (tested with Pillow) [tree 51fd4b8c8fa1] (2026-10-22T21:23:15Z)
- (audit edge) `review edge lens` → learn counted once per file and look, capped +3, trimmed first; corrupt ledger saved as .bak; learn exits 1 when all skipped [tree 51fd4b8c8fa1] (2026-10-22T21:23:16Z)
- (audit operator) `fm looks verbs and the app's L picker via tests after the merge` → 235 tests green; the TTY picker under a pseudo-terminal not run (harness refused) [tree 51fd4b8c8fa1] (2026-10-22T21:23:16Z)
- (audit maintainer) `review maintainer lens` → photo path and bomb check now tested; changelog line present [tree 51fd4b8c8fa1] (2026-10-22T21:23:16Z)
- (audit design) `review design lens` → app picker: no default highlight, Backspace goes back, counter first in the title [tree 51fd4b8c8fa1] (2026-10-22T21:23:16Z)
- (audit intent) `criterion: kept/reverted update the ledger; 12-answer calibration; only named files read` → met (13 tests); kept/reverted stay manual verbs, documented; idle rolls, taste bisect, séance, pane surface and history detection are T-1672 [tree 51fd4b8c8fa1] (2026-10-22T21:23:17Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_taste_ledger` → exit 0 · Ran 13 tests in 1.830s / OK [ran] [tree 51fd4b8c8fa1] (2026-10-22T21:23:25Z)
- (audit adversary) `one fm-reviewer five-lens + design pass; all findings fixed test-first by the builder; criterion green after the merge` → picker escape drain, symlinks refused, named files only with caps and a bomb check [tree 51fd4b8c8fa1] (2026-10-22T21:23:25Z)
- (audit edge) `one fm-reviewer five-lens + design pass; all findings fixed test-first by the builder; criterion green after the merge` → learn deduped and capped, corrupt ledger backed up [tree 51fd4b8c8fa1] (2026-10-22T21:23:25Z)
- (audit adversary) `one fm-reviewer five-lens + design pass; all findings fixed test-first by the builder; criterion green after the merge` → picker escape drain, symlinks refused, named files only with caps and a bomb check [tree 51fd4b8c8fa1] (2026-10-22T21:24:05Z)
- (audit edge) `one fm-reviewer five-lens + design pass; all findings fixed test-first by the builder; criterion green after the merge` → learn deduped and capped, corrupt ledger backed up [tree 51fd4b8c8fa1] (2026-10-22T21:24:05Z)
## Log
- 2026-10-22T17:43:47Z created
- 2026-10-22T17:58:32Z set scope=['plugin/lib/fmtaste.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_taste_ledger.py', 'CHANGELOG.md']
- 2026-10-22T20:37:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1537.builder.md
- 2026-10-22T20:38:01Z focused
- 2026-10-22T20:43:43Z set scope=['plugin/lib/fmtaste.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_taste_ledger.py', 'CHANGELOG.md', 'plugin/commands/looks.md', 'plugin/skills/directions/SKILL.md']
- 2026-10-22T20:43:45Z scope: plugin/commands/looks.md (Claude Code parity: the user-only /foreman:looks command) and plugin/skills/directions/SKILL.md (ranks its suggestions by the ledger)
- 2026-10-22T21:00:46Z set scope=['plugin/lib/fmtaste.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_taste_ledger.py', 'CHANGELOG.md', 'plugin/commands/looks.md', 'plugin/skills/directions/SKILL.md', 'MASTER.md']
- 2026-10-22T21:00:46Z scope: MASTER.md (fm doctor's self-docs check: the CLI line names fm looks, the module map names fmtaste)
- 2026-10-22T21:01:00Z set scope=['plugin/lib/fmtaste.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_taste_ledger.py', 'CHANGELOG.md', 'plugin/commands/looks.md', 'plugin/skills/directions/SKILL.md', 'MASTER.md', 'plugin/lib/fmcodetui.py']
- 2026-10-22T21:01:08Z scope: plugin/lib/fmcodetui.py (the fm code app's keyboard picker for the calibration; lease freed by T-1543)
- 2026-10-22T21:22:37Z merged worktree-agent-a1ce18f1e8a36e114 (8 file(s))
- 2026-10-22T21:22:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1ce18f1e8a36e114
- 2026-10-22T21:22:53Z focused
- 2026-10-22T21:24:04Z scope: README.md, settings.md, fmbus/fmdemo/fmlib/fmnew/fmoracle.py and test_docs.py came in from other tasks' merges (T-1519, T-1543, T-1553, T-1507) through this lane's foreman/build merges; ANDON.md was a lane-local file created and deleted in the lane's history, absent from the tree
- 2026-10-22T21:24:32Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1543 [FEATURE M, active, 4 steps] Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misren
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- research brainstorm-20261022-catalogue: Request: "super recursive brainstorm and improve foreman, way more skills/playbooks/way better more capable code, config in the t…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- similar past tasks were L: consider --tier L
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/commands/looks.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmtaste.py, plugin/skills/directions/SKILL.md, plugin/tests/test_taste_ledger.py; re-ground the plan against them before editing
## Why not caught
tests learned from one file at a time
## Lessons
- Any score fed by a bulk input (a glob of files) needs a per-source dedupe and a cap, or one command outweighs every deliberate signal
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_taste_ledger.py
- plugin/lib/fmtaste.py
- plugin/commands/looks.md
- plugin/skills/directions/SKILL.md
- ANDON.md
- plugin/lib/fmcli.py
- MASTER.md
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- README.md
- plugin/commands/settings.md
- plugin/lib/fmbus.py
- plugin/lib/fmdemo.py
- plugin/lib/fmlib.py
- plugin/lib/fmnew.py
- plugin/lib/fmoracle.py
- plugin/lib/fmplaybooks.py
- plugin/lib/fmrecall.py
- plugin/lib/fmreplay.py
- plugin/lib/fmsettings.py
- plugin/skills/library/SKILL.md
- plugin/skills/library/cards/tools/jq.md
- plugin/skills/library/cards/tools/ripgrep.md
- plugin/skills/playbooks/references/ui/INDEX.md
- plugin/skills/playbooks/references/ui/templates/scene.html
- plugin/templates/tui/panel.py
- plugin/templates/web/index.html
- plugin/tests/test_bus.py
- plugin/tests/test_docs.py
- plugin/tests/test_guard_hardening.py
